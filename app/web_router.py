import json

import markdown
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from pathlib import Path

router = APIRouter(prefix="/web", tags=["web"])
templates = Jinja2Templates(directory="app/templates")

TOPICS_PATH = Path("app/theory/topics.json")
CARDS_DIR = Path("app/theory/cards")

@router.get("", response_class=HTMLResponse)
def get_index(request: Request):
    with open(TOPICS_PATH, encoding="utf-8") as f:
        topics = json.load(f)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "topics": topics,
        },
    )

@router.get("/theory/{slug}", response_class=HTMLResponse)
async def theory_topic_page(
    request: Request,
    slug: str,
):
    """
    Страница темы теории (Markdown версия)
    """
    md_path = CARDS_DIR / f"{slug}.md"

    if not md_path.exists():
        raise HTTPException(status_code=404, detail="Topic not found")

    md_text = md_path.read_text(encoding="utf-8")

    html_content = markdown.markdown(
        md_text,
        extensions=["fenced_code", "tables"]
    )

    return templates.TemplateResponse(
        "theory.html",
        {
            "request": request,
            "slug": slug,
            "content": html_content,
        }
    )
