# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import traceback
import os
import requests
import re

app = Flask(__name__, static_folder="public", static_url_path="")
CORS(app)

def extract_full_price_info(price_container_tag):
    """
    Extracts the full price string including currency symbol directly from the container.
    Example: Input is the div with class 'old' or 'new'.
    It should contain text like '€737' or '$479'.
    """
    if not price_container_tag:
        return "N/A"
    
    # Get all text content, including from children like span.currency and direct text nodes
    price_text_parts = [part.strip() for part in price_container_tag.find_all(string=True, recursive=True) if part.strip()]
    full_price_str = "".join(price_text_parts)

    if full_price_str:
        # Basic validation: check if it contains a digit.
        if any(char.isdigit() for char in full_price_str):
            return full_price_str
        else: # If no digit, it might be something like "Call for price"
            return price_container_tag.get_text(strip=True) # Fallback to simple text extraction
    return "N/A"

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
        print(f"--- Using ChromeDriver from: {driver_path} ---")

        if not os.path.exists(driver_path):
            print(f"!!! ChromeDriver not found at {driver_path} !!!")
            return jsonify({"error": "ChromeDriver executable not found."}), 500

        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("--- Headless Chrome driver initialized ---")

        target_url = "https://www.blik.co.il/Deals/Deals.aspx?index=1"
        print(f"--- Navigating to {target_url} ---")
        driver.get(target_url)

        deal_page_container_selector = ".kd-slides"
        wait_time = 25

        print(f"--- Waiting up to {wait_time}s for main deals container using selector: '{deal_page_container_selector}' ---")
        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, deal_page_container_selector))
            )
            print(f"--- Main deals container found! Proceeding to parse page source. ---")
        except TimeoutException:
            print(f"--- Timeout: Main deals container '{deal_page_container_selector}' not found after {wait_time}s. Returning empty list. ---")
            return jsonify([])

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        print("--- Page source parsed with BeautifulSoup ---")

        deals = []
        card_selector = ".kd-slide .wrap"
        cards = soup.select(card_selector)[:3] 
        print(f"--- Found {len(cards)} deal cards (limited to 3 for processing) using selector '{card_selector}' ---")

        if not cards:
            print("--- No deal cards found. Check your card_selector or the website structure. ---")
            return jsonify([])

        for idx, card_soup in enumerate(cards):
            print(f"\n--- Processing Card {idx + 1} ---")
            img_selector = ".deal-img img"
            destination_selector = ".row.title .destination"
            details_selector = ".row.details span"
            dates_selector = ".row.dates span"
            hotel_name_selector = ".row.hotel-name span"
            old_price_selector = ".row.price .old"         # Selector for the <div> with class 'old'
            new_price_selector = ".row.price .new"         # Selector for the <div> with class 'new'
            link_selector = ".row.price a.button.buy-now"

            img_tag = card_soup.select_one(img_selector)
            destination_tag = card_soup.select_one(destination_selector)
            details_tag = card_soup.select_one(details_selector)
            dates_tag = card_soup.select_one(dates_selector)
            hotel_name_tag = card_soup.select_one(hotel_name_selector)
            old_price_tag = card_soup.select_one(old_price_selector)
            new_price_tag = card_soup.select_one(new_price_selector) # This is the div.new tag
            link_tag = card_soup.select_one(link_selector)

            deal_data = {}
            original_image_url = ""

            if img_tag and img_tag.get("src"):
                original_image_url = img_tag.get("src")
                if original_image_url.startswith('/'):
                    original_image_url = "https://www.blik.co.il" + original_image_url
                if not original_image_url.startswith('http'):
                    original_image_url = "" 
            deal_data["image"] = original_image_url
            print(f"Image URL: {deal_data['image'] or 'Not found'}")

            if destination_tag:
                deal_data["destination"] = destination_tag.get_text(strip=True)
            else:
                deal_data["destination"] = "Destination not specified"
            print(f"Destination: {deal_data['destination']}")

            if details_tag:
                deal_data["details"] = details_tag.get_text(strip=True)
            else:
                deal_data["details"] = "Details not specified"
            print(f"Details: {deal_data['details']}")

            if dates_tag:
                deal_data["dates"] = dates_tag.get_text(strip=True)
            else:
                deal_data["dates"] = "Dates not specified"
            print(f"Dates: {deal_data['dates']}")

            if hotel_name_tag:
                deal_data["hotel_name"] = hotel_name_tag.get_text(strip=True)
            else:
                deal_data["hotel_name"] = "Hotel name not specified"
            print(f"Hotel Name: {deal_data['hotel_name']}")
            
            deal_data["old_price"] = extract_full_price_info(old_price_tag)
            print(f"Old Price (full): {deal_data['old_price']}")

            deal_data["new_price"] = extract_full_price_info(new_price_tag)
            print(f"New Price (full): {deal_data['new_price']}")
            
            # 'price' field for primary display, prioritize new_price
            deal_data["price"] = deal_data["new_price"] if deal_data["new_price"] != "N/A" else deal_data["old_price"]

            deal_link_url = ""
            if link_tag and link_tag.get("href"):
                deal_link_url = link_tag.get("href")
                if deal_link_url.startswith('/'):
                    deal_link_url = "https://www.blik.co.il" + deal_link_url
            deal_data["link_url"] = deal_link_url
            print(f"Deal Link: {deal_data['link_url'] or 'Not found'}")
            
            if deal_data.get("price", "N/A") != "N/A" or deal_data.get("destination", "Destination not specified") != "Destination not specified":
                deals.append(deal_data)
            else:
                print(f"--- Card {idx+1} skipped due to missing essential data. ---")
        
        total_cards_found_on_page = len(soup.select(card_selector))
        print(f"\n--- Finished processing. Returning {len(deals)} deals (out of {total_cards_found_on_page} initially found on page, processed max 3). ---")
        return jsonify(deals)

    except Exception as e:
        print(f"!!! EXCEPTION in /api/deals !!!")
        traceback.print_exc()
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500
    finally:
        if driver:
            print("--- Quitting Chrome driver ---")
            driver.quit()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)