from fastapi import FastAPI, Request
from .load_balancer import get_next_instance
from .metrics import REQUEST_COUNT, REQUEST_LATENCY
from fastapi.middleware.cors import CORSMiddleware
import requests
import httpx

app = FastAPI()

origins = [
    "https://pdist-front.vercel.app/",
    "https://pdist-front-felipes-projects-ed3c083c.vercel.app/",
    "https://pdist-front-git-main-felipes-projects-ed3c083c.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.middleware("http")
async def add_prometheus_metrics(request: Request, call_next):
    endpoint = request.url.path
    method = request.method
    REQUEST_COUNT.labels(method = method, endpoint = endpoint).inc()

    with REQUEST_LATENCY.labels(endpoint = endpoint).time():
        response = await call_next(request)

    return response

@app.get("/load-balanced/{service_name}/{path:path}")
async def load_balanced_proxy(service_name: str, path:str, request: Request):
    instance_url = get_next_instance(service_name)
    backend_url = f"{instance_url}/{path}"
    print(backend_url)
    headers = dict(request.headers)
    data = await request.body()

    backend_response = requests.request(
        method=request.method,
        url=backend_url,
        headers=headers,
        data=data,
    )

    return backend_response.json()

@app.post("/load-balanced/{service_name}/{path:path}")
async def proxy_post(service_name: str, path: str, payload: dict):
    instance_url = get_next_instance(service_name)
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{instance_url}/{path}", json=payload)
        return response.json()

@app.get("/metrics")
def metrics():
    from prometheus_client import generate_latest
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    