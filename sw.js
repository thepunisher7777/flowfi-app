const CACHE='ledger-beta-1-1-posthog';
const CORE=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png','./apple-touch-icon.png','./posthog-bridge.js'];

async function injectPostHogBridge(response){
  if(!response) return response;
  const text=await response.text();
  if(text.includes('posthog-bridge.js')) return new Response(text,{status:response.status,statusText:response.statusText,headers:response.headers});
  const injected=text.replace('</head>','  <script src="./posthog-bridge.js"></script>\n</head>');
  const headers=new Headers(response.headers);
  headers.delete('content-length');
  return new Response(injected,{status:response.status,statusText:response.statusText,headers});
}

self.addEventListener('install',e=>e.waitUntil(
  caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting())
));

self.addEventListener('activate',e=>e.waitUntil(
  caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())
));

self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET') return;

  if(e.request.mode==='navigate'){
    e.respondWith((async()=>{
      try{
        const network=await fetch(e.request,{cache:'no-store'});
        const bridged=await injectPostHogBridge(network);
        const copy=bridged.clone();
        caches.open(CACHE).then(c=>c.put('./index.html',copy));
        return bridged;
      }catch{
        const cached=await caches.match('./index.html');
        return cached ? injectPostHogBridge(cached) : cached;
      }
    })());
    return;
  }

  e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request).then(r=>{
    const copy=r.clone();
    caches.open(CACHE).then(c=>c.put(e.request,copy));
    return r;
  })));
});
