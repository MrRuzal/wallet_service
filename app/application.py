from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.v1.endpoints import router

app = FastAPI()

app.include_router(router, prefix="/api/v1")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return RedirectResponse(url="/docs")
