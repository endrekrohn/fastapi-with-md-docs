from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import docs


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI with extra docs",
        description="""<a href="/docs/">Written documentation<span>🔗</span></a>""",
        openapi_url="/openapi.json",
    )

    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(docs.router, include_in_schema=False)

    return app


app = create_app()


@app.get("/health", tags=["Status"])
def healthcheck():
    """
    This route has additional written documentation at:

    - 📄 [Health](/docs/health)
    """
    return "ok"
