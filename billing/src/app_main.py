import uvicorn
from fastapi import FastAPI

from api import api_router
from app_config import settings

app = FastAPI(title=settings.PROJECT_NAME, docs_url="/")
app.include_router(api_router, prefix=settings.API_VSTR)

if __name__ == '__main__':
    uvicorn.run("__main__:app", host='otus.billing', port=81, reload=True)
