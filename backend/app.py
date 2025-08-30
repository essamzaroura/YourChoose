from flask import Flask, jsonify, request
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup, Comment
import traceback
import os
import requests
import re
import google.generativeai as genai
import sys
import time
from google.api_core import exceptions

app = Flask(__name__, static_folder="public", static_url_path="")
CORS(app)

try:
    from config import GEMINI_API_KEY
    print("--- Successfully loaded GEMINI_API_KEY from config ---")
except (ImportError, ValueError) as e:
    print(f"!!! ERROR: {e} !!!")
    sys.exit(1)

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    print("--- Gemini AI Model configured successfully. ---")
except Exception as e:
    print(f"!!! ERROR configuring Gemini AI: {e} !!!")
    sys.exit(1)

def extract_final_price_info(price_container_tag):
    if not price_container_tag:
        return "N/A"
    for comment in price_container_tag.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    raw_text = price_container_tag.get_text(separator=' ', strip=True)
    if not raw_text:
        return "N/A"
    print(f"Raw price text after comment removal: '{raw_text}'")
    match = re.search(r'([€$£₪]|\b[A-Za-z]{1,3}\s*)?(\d[\d,.]*)', raw_text)
    if match:
        symbol = match.group(1) if match.group(1) else ""
        number = match.group(2).replace(',', '') if match.group(2) else ""
        if number:
            if not symbol.strip() and raw_text and not raw_text[0].isdigit():
                first_part = raw_text.split(number)[0].strip()
                if re.match(r'^[€$£₪]', first_part):
                    symbol = first_part
            return f"{symbol.strip()}{number}".strip()
    just_numbers = re.findall(r'\d[\d,.]*', raw_text)
    if just_numbers:
        print(f"--- Only numbers found in price: '{just_numbers[0]}', symbol might be missing. ---")
        return just_numbers[0].replace(',', '')
    if not any(char.isdigit() for char in raw_text):
        return raw_text
    return "N/A"

def retry_on_quota_error(func):
    def wrapper(*args, **kwargs):
        max_retries = 3
        retry_delay = 60  # Start with 60 seconds, adjust based on response
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except exceptions.QuotaExceeded as e:
                if attempt == max_retries - 1:
                    raise
                retry_delay = getattr(e, 'retry_delay', {}).get('seconds', 60) or 60
                print(f"Quota exceeded, retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
    return wrapper

@app.route("/api/deals")
def get_deals():
    print("\n--- Request received for /api/deals ---")
    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")
        if not os.path.exists(driver_path):
            return jsonify({"error": "ChromeDriver executable not found."}), 500
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        target_url = "https://www.blik.co.il/Deals/Deals.aspx?index=1"
        driver.get(target_url)

        deal_page_container_selector = ".kd-slides"
        wait_time = 25
        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, deal_page_container_selector))
            )
        except TimeoutException:
            print(f"--- Timeout: Main deals container '{deal_page_container_selector}' not found after {wait_time}s. ---")
            if driver: driver.quit()
            return jsonify([])

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        deals = []
        card_selector = ".kd-slide .wrap"
        cards = soup.select(card_selector)[:3] 
        print(f"--- Found {len(cards)} deal cards (limited to 3 for processing) ---")

        if not cards:
            if driver: driver.quit()
            return jsonify([])

        for idx, card_soup in enumerate(cards):
            print(f"\n--- Processing Card {idx + 1} ---")
            img_selector = ".deal-img img"
            destination_selector = ".row.title .destination"
            details_selector = ".row.details span"
            dates_selector = ".row.dates span"
            hotel_name_selector = ".row.hotel-name span"
            old_price_selector = ".row.price .old"
            new_price_selector = ".row.price .new"
            link_selector = ".row.price a.button.buy-now"

            img_tag = card_soup.select_one(img_selector)
            destination_tag = card_soup.select_one(destination_selector)
            details_tag = card_soup.select_one(details_selector)
            dates_tag = card_soup.select_one(dates_selector)
            hotel_name_tag = card_soup.select_one(hotel_name_selector)
            old_price_tag = card_soup.select_one(old_price_selector)
            new_price_tag = card_soup.select_one(new_price_selector)
            link_tag = card_soup.select_one(link_selector)

            deal_data = {}
            original_image_url = ""
            if img_tag and img_tag.get("src"):
                original_image_url = img_tag.get("src")
                if original_image_url.startswith('/'): original_image_url = "https://www.blik.co.il" + original_image_url
                if not original_image_url.startswith('http'): original_image_url = "" 
            deal_data["image"] = original_image_url

            deal_data["destination"] = destination_tag.get_text(strip=True) if destination_tag else "Destination N/A"
            deal_data["details"] = details_tag.get_text(strip=True) if details_tag else "Details N/A"
            deal_data["dates"] = dates_tag.get_text(strip=True) if dates_tag else "Dates N/A"
            deal_data["hotel_name"] = hotel_name_tag.get_text(strip=True) if hotel_name_tag else "Hotel N/A"
            deal_data["old_price"] = extract_final_price_info(old_price_tag)
            deal_data["new_price"] = extract_final_price_info(new_price_tag)
            deal_data["price"] = deal_data["new_price"] if deal_data["new_price"] != "N/A" else deal_data["old_price"]
            
            deal_link_url = ""
            if link_tag and link_tag.get("href"):
                deal_link_url = link_tag.get("href")
                if deal_link_url.startswith('/'): deal_link_url = "https://www.blik.co.il" + deal_link_url
            deal_data["link_url"] = deal_link_url
            
            if deal_data.get("price", "N/A") != "N/A" or deal_data.get("destination", "Destination N/A") != "Destination N/A":
                deals.append(deal_data)
        
        print(f"\n--- Finished processing deals. Returning {len(deals)} deals. ---")
        if driver: driver.quit()
        return jsonify(deals)

    except Exception as e:
        print(f"!!! EXCEPTION in /api/deals: {type(e).__name__} - {e} !!!")
        traceback.print_exc()
        if driver: driver.quit()
        return jsonify({"error": f"An internal server error occurred while fetching deals: {str(e)}"}), 500

@app.route('/api/chat', methods=['POST'])
@retry_on_quota_error
def chat_with_ai():
    if not model:
        return jsonify({"error": "AI model is not configured. Check API key or library version."}), 503

    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        print(f"--- Sending to Gemini: '{user_message}' ---")
        response = model.generate_content(user_message)
        ai_reply = response.text if hasattr(response, 'text') else str(response)
        print(f"--- Received from Gemini: '{ai_reply}' ---")
        return jsonify({"reply": ai_reply})
    except Exception as e:
        print(f"!!! ERROR interacting with Gemini API: {e} !!!")
        traceback.print_exc()
        return jsonify({"error": f"Error communicating with AI service: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)