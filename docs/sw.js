// Offline support: keeps the app itself on the phone. Orders are stored offline by Firestore.
const VERSION = "soma-467d3d7d6a";
const SHELL = [
  "./", "./index.html", "./manifest.webmanifest", "./firebase-config.js",
  "./assets/soma-mark.png", "./assets/soma-logo.jpg", "./assets/icon-192.png", "./assets/icon-512.png",
];
// Versioned third-party files that never change at the same URL
const STATIC_HOSTS = ["www.gstatic.com", "fonts.googleapis.com", "fonts.gstatic.com"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  if (url.origin === self.location.origin) {
    // App files: use the network when it answers, the saved copy when offline
    e.respondWith(
      fetch(req).then((res) => {
        if (res.ok) { const copy = res.clone(); caches.open(VERSION).then((c) => c.put(req, copy)); }
        return res;
      }).catch(() => caches.match(req, { ignoreSearch: true })
        .then((hit) => hit || (req.mode === "navigate" ? caches.match("./index.html") : Response.error())))
    );
    return;
  }

  if (STATIC_HOSTS.includes(url.hostname)) {
    // Firebase library and fonts: saved copy first
    e.respondWith(
      caches.match(req).then((hit) => hit || fetch(req).then((res) => {
        const copy = res.clone(); caches.open(VERSION).then((c) => c.put(req, copy));
        return res;
      }))
    );
  }
  // Everything else (Firestore, sign-in) goes straight to the network
});
