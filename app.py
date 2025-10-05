from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Input schema
class TelemetryRequest(BaseModel):
    regions: list[str]
    threshold_ms: int

# Simulated telemetry data (replace with your bundle or DB if given)
# Suppose telemetry is a dict of region -> list of latencies (ms)
# Each record also includes uptime (1 = up, 0 = down)
sample_telemetry = {
    "apac": [
        {"latency": 170, "uptime": 1},
        {"latency": 185, "uptime": 1},
        {"latency": 200, "uptime": 0},
    ],
    "emea": [
        {"latency": 150, "uptime": 1},
        {"latency": 182, "uptime": 1},
        {"latency": 195, "uptime": 1},
    ],
    "americas": [
        {"latency": 160, "uptime": 1},
        {"latency": 190, "uptime": 1},
    ],
}

@app.post("/analytics")
async def analytics(request: TelemetryRequest):
    response = {}

    for region in request.regions:
        data = sample_telemetry.get(region, [])
        if not data:
            continue

        latencies = [d["latency"] for d in data]
        uptimes = [d["uptime"] for d in data]

        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies, 95))
        avg_uptime = float(np.mean(uptimes))
        breaches = sum(1 for l in latencies if l > request.threshold_ms)

        response[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches,
        }

    return response
