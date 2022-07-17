import logging
import os
from dataclasses import dataclass
import functools
from typing import Any

import jinja2
import markdown2
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse

from config import settings

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass()
class HTML:
    html: Any
    toc: Any
    metadata: dict[str, Any]


@dataclass
class TOC:
    url: str
    title: str | None
    description: str | None


def cache(func, /):
    if settings.IS_DEV:
        return func
    return functools.cache(func)


@cache
def get_path(filename: str) -> str:
    return os.getcwd() + f"/docs/{filename}"


def md_to_html(md: str) -> HTML:
    data = markdown2.markdown(
        md, extras=["fenced-code-blocks", "header-ids", "metadata", "toc"]
    )
    return HTML(html=data, toc=data.toc_html, metadata=data.metadata)


@cache
def get_md(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not find file."
        )
    with open(filepath) as md:
        return md.read()


@cache
def get_html(md: str) -> str:
    try:
        data = md_to_html(md)
        with open(get_path("template.html")) as file_:
            return jinja2.Template(file_.read()).render(
                title=data.metadata.get("title", None),
                toc=data.toc,
                content=data.html,
            )
    except Exception:
        raise HTTPException(
            status.HTTP_424_FAILED_DEPENDENCY, detail="Could not hydrate HTML."
        )


@cache
def get_toc() -> dict[str, TOC]:
    res: dict[str, TOC] = {}
    for path, _, files in os.walk(f"{os.getcwd()}/docs"):
        for file in files:
            if file.endswith(".md"):
                _path = os.path.join(path, file)
                data = md_to_html(get_md(_path))
                url = _path.removeprefix("/application").removesuffix(".md")
                res[_path] = TOC(
                    url=url,
                    title=data.metadata.get("title", url),
                    description=data.metadata.get(
                        "description", "No description provided."
                    ),
                )
    return res


@cache
def get_toc_markdown() -> str:
    data = """---
title: Written documentation
---
### Listed documentation\n
"""
    for _, toc in get_toc().items():
        data += f"\n - [🔗]({toc.url}) {toc.title}"
    return data


@router.get("/docs/", response_class=HTMLResponse)
async def get_doc_toc() -> str:
    return get_html(get_toc_markdown())


@router.get("/docs/{filepath:path}", response_class=HTMLResponse)
async def get_extra_doc(filepath: str) -> str:
    return get_html(get_md(get_path(f"{filepath}.md")))
