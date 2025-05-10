// frontend/src/serviceWorkerRegistration.js

// Function to register the service worker
export const registerSW = () => {
  // Check if the browser supports service workers
  if ('serviceWorker' in navigator) {
    // Add an event listener to register the service worker once the page loads
    window.addEventListener('load', () => {
      // Define the path to the service worker file
      // Assumes your service worker is at 'public/Service-worker.js'
      // The path should be relative to the root of your domain.
      const swUrl = '/Service-worker.js'; // Ensure 'Service-worker.js' matches your actual filename case

      navigator.serviceWorker.register(swUrl)
        .then(registration => {
          // Log success message with the scope of the registration
          console.log('✅ Service Worker registered with scope:', registration.scope);
        })
        .catch(error => {
          // Log error message if registration fails
          console.error('❌ Service Worker registration failed:', error);
        });
    });
  } else {
    // Log message if service workers are not supported
    console.log('Service workers are not supported in this browser.');
  }
};

// Optional: Function to unregister the service worker (useful for development)
export const unregister = () => {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready
      .then(registration => {
        registration.unregister();
        console.log('Service Worker unregistered');
      })
      .catch(error => {
        console.error('Error during service worker unregistration:', error);
      });
  }
};