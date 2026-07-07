import time
import uuid
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Replace with your assigned allowed origin
ALLOWED_ORIGIN = "https://dash-tat57p.example.com"

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Middleware to add required headers
@app.middleware("http")
async def add_headers(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    return response


@app.get("/stats")
async def stats(values: str = Query(...)):
    try:
        nums = [int(x.strip()) for x in values.split(",") if x.strip()]

        if len(nums) == 0:
            return JSONResponse(
                status_code=400,
                content={"error": "No values provided"}
            )

        result = {
            "email": "24f2005647@ds.study.iitm.ac.in", 
            "count": len(nums),
            "sum": sum(nums),
            "min": min(nums),
            "max": max(nums),
            "mean": sum(nums) / len(nums),
        }

        return result

    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Values must be comma-separated integers"}
        )
