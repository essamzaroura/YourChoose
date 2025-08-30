/* eslint-disable no-restricted-globals */

const CACHE_NAME = 'yourchoose-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/static/js/main.chunk.js',
  '/static/js/0.chunk.js',
  '/static/js/bundle.js',
  '/manifest.json',
  '/favicon.ico',
  '/logo192.png',
  '/logo512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return Promise.all(
        urlsToCache.map(url => {
          return fetch(url).then(response => {
            if (!response.ok) {
              console.warn(`Failed to cache ${url}: ${response.status}`);
              return Promise.resolve();
            }
            return cache.put(url, response);
          }).catch(err => {
            console.warn(`Error caching ${url}: ${err}`);
            return Promise.resolve();
          });
        })
      );
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET' || event.request.url.includes('/api/')) return;

  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});