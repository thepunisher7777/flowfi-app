const CACHE='ledger-beta-1-2-arx-analytics';
const CORE=[
  './',
  './index.html',
  './ledger-core.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png',
  './posthog-bridge.js',
  './arx-analytics-guard.js'
];

self.addEventListener('install',event=>event.waitUntil(
  caches.open(CACHE).then(cache=>cache.addAll(CORE)).then(()=>self.skipWaiting())
));

self.addEventListener('activate',event=>event.waitUntil(
  caches.keys()
    .then(keys=>Promise.all(keys.filter(key=>key!==CACHE).map(key=>caches.delete(key))))
    .then(()=>self.clients.claim())
));

async function networkFirst(request,fallbackKey){
  try{
    const response=await fetch(request,{cache:'no-store'});
    if(response && response.ok){
      const copy=response.clone();
      caches.open(CACHE).then(cache=>cache.put(fallbackKey||request,copy));
    }
    return response;
  }catch(error){
    const cached=await caches.match(fallbackKey||request);
    if(cached) return cached;
    throw error;
  }
}

self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET') return;
  const url=new URL(event.request.url);

  if(event.request.mode==='navigate'){
    event.respondWith(networkFirst(event.request,'./index.html'));
    return;
  }

  if(url.origin===self.location.origin && url.pathname.endsWith('/ledger-core.html')){
    event.respondWith(networkFirst(event.request,'./ledger-core.html'));
    return;
  }

  event.respondWith(
    caches.match(event.request).then(hit=>hit||fetch(event.request).then(response=>{
      if(response && response.ok && url.origin===self.location.origin){
        const copy=response.clone();
        caches.open(CACHE).then(cache=>cache.put(event.request,copy));
      }
      return response;
    }))
  );
});
