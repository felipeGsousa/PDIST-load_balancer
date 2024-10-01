from prometheus_client import Counter, Histogram

# Contador de requisições
REQUEST_COUNT = Counter('request_count', 'Total number of requests received', ['method', 'endpoint'])

# Métrica de latência das requisições
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Latency of requests in seconds', ['endpoint'])