const CACHE_NAME = "smriticare-v2";

const FILES_TO_CACHE = [
    "/",
    "/dashboard",
    "/memory-game",
    "/attention-game",
    "/recall-game",
    "/object-match",
    "/static/css/style.css",
    "/static/js/script.js",
    "/static/espeak/espeakng.min.js",
    "/static/espeak/espeakng.worker.js",
    "/static/espeak/espeakng.worker.data"
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(async (cache) => {
            for (const file of FILES_TO_CACHE) {
                try {
                    await cache.add(file);
                    console.log("Cached:", file);
                } catch (error) {
                    console.warn("Could not cache:", file, error);
                }
            }
        })
    );

    self.skipWaiting();
});


self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((cacheName) => cacheName !== CACHE_NAME)
                    .map((cacheName) => caches.delete(cacheName))
            );
        })
    );

    self.clients.claim();
});


self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;
            }

            return fetch(event.request).catch(() => {
                return caches.match("/");
            });
        })
    );
});