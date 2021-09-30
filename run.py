from routers import demo_area
import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import sys

app = FastAPI(
    title="simages",
    description="Consume image data from sentinel API",
    version="0.0.1",
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["ndvi", "last_updated"],
    expose_headers=["*"]
)


@app.get("/", include_in_schema=False)
def read_docs():
    return RedirectResponse(url="/docs")


app.include_router(
    demo_area.router,
    prefix="/demo",
    tags=["demo"],
)


if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=5000,
                debug=True, log_level="info")
