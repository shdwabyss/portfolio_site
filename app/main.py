import json
import time
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.logging import logger

SCRIPT_DIR = Path(__file__).resolve().parent
LOCALE_PATH = SCRIPT_DIR / "data" / "locale.json"

try:
    with open(LOCALE_PATH, "r", encoding="utf-8") as file:
        locale = json.load(file)
except FileNotFoundError as e:
    raise RuntimeError(f"Critical error: locale file not found {LOCALE_PATH}") from e

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    log_message = (
        f"Method: {request.method} | "
        f"Path: {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Duration: {process_time:.2f}ms"
    )

    if response.status_code >= 400:
        logger.warning(log_message)
    else:
        logger.info(log_message)

    return response


@app.get(path="/", response_class=HTMLResponse)
async def get_portfolio(request: Request, lang: str = "ru"):
    correct_lang = lang if lang in ["ru", "en"] else "ru"
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "lang": correct_lang,
            "content": locale[correct_lang],
        },
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    lang = request.query_params.get("lang", "ru")
    correct_lang = lang if lang in ["ru", "en"] else "ru"

    return templates.TemplateResponse(
        request=request,
        name="404.html",
        context={
            "request": request,
            "lang": correct_lang,
            "content": locale[correct_lang],
        },
        status_code=404,
    )


@app.exception_handler(Exception)
async def internal_server_error(request: Request, exc: Exception):
    lang = request.query_params.get("lang", "ru")
    correct_lang = lang if lang in ["ru", "en"] else "ru"

    return templates.TemplateResponse(
        request=request,
        name="500.html",
        context={
            "request": request,
            "lang": correct_lang,
            "content": locale[correct_lang],
        },
        status_code=500,
    )


@app.get("/500")
async def trigger_500():
    result = 1 / 0
    return {"result": result}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {"status": "healthy", "timestamp": time.time}
