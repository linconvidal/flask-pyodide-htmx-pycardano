console.log('Service Worker: Loading');

self.addEventListener('install', (event) => {
    console.log('Service Worker: Installing...');
    // Force the waiting service worker to become the active service worker.
    event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activating...');
    // Become available to all pages
    event.waitUntil(self.clients.claim());
});

// Service Worker to intercept Flask routes and handle them with Pyodide
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);
    
    // Skip cross-origin requests so external resources (e.g. PyPI wheels)
    // are fetched normally without being intercepted by this service worker.
    if (url.origin !== self.location.origin) {
        // Let the browser handle the request as usual.
        return;
    }
    
    // Skip requests for static files (those with file extensions)
    const staticFileExtensions = ['.js', '.css', '.html', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot', '.json', '.xml', '.txt', '.py', '.wasm', '.mjs', '.zip', '.whl'];
    const hasFileExtension = staticFileExtensions.some(ext => url.pathname.toLowerCase().endsWith(ext));
    
    // Handle CORS preflight requests
    if (event.request.method === 'OPTIONS') {
        event.respondWith(new Response(null, {
            status: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            }
        }));
        return;
    }
    
    // If it's not a static file and it's a GET request, try to handle it as a Flask route
    if (!hasFileExtension && event.request.method === 'GET') {
        console.log('Service Worker: Intercepting potential Flask route:', url.pathname);
        event.respondWith(handleFlaskRequest(event.request));
        return;
    }
});

async function handleFlaskRequest(request) {
    try {
        const url = new URL(request.url);
        console.log('Service Worker: Handling Flask request to', url.pathname);
        
        // Communicate with main thread to execute Flask route
        const messageChannel = new MessageChannel();
        
        const response = await new Promise((resolve, reject) => {
            messageChannel.port1.onmessage = (event) => {
                if (event.data.error) {
                    reject(new Error(event.data.error));
                } else {
                    resolve(event.data);
                }
            };
            
            // Send message to main thread
            self.clients.matchAll().then(clients => {
                if (clients.length > 0) {
                    clients[0].postMessage({
                        type: 'FLASK_REQUEST',
                        path: url.pathname,
                        method: request.method
                    }, [messageChannel.port2]);
                } else {
                    reject(new Error('No clients available'));
                }
            });
        });
        
        // If Flask returns a 404, fall back to normal fetch (for static files)
        if (response.status === 404) {
            console.log('Service Worker: Flask returned 404, trying normal fetch for', url.pathname);
            return fetch(request);
        }
        
        // Create response with CORS headers
        const headers = new Headers();
        headers.set('Access-Control-Allow-Origin', '*');
        headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
        headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
        
        // Set content type based on response type
        if (response.data.startsWith('{') || response.data.startsWith('[')) {
            headers.set('Content-Type', 'application/json');
        } else if (response.data.includes('<html') || response.data.includes('<!DOCTYPE')) {
            headers.set('Content-Type', 'text/html');
        } else {
            headers.set('Content-Type', 'text/plain');
        }
        
        return new Response(response.data, {
            status: response.status || 200,
            headers: headers
        });
        
    } catch (error) {
        console.error('Service Worker error:', error);
        console.log('Service Worker: Falling back to normal fetch for', request.url);
        // Fall back to normal fetch if Flask handling fails
        return fetch(request);
    }
} 