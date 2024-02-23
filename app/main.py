import datetime
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from sqlalchemy import select
from models import DomainItem
import schemas
from db import get_db
from sqlmodel import Session

app = FastAPI()


@app.exception_handler(Exception)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    status_code = 500
    content = {"status": f"{str(exc)}"}
    if type(exc) == RequestValidationError:
        status_code = 422
    return JSONResponse(status_code=status_code, content=content)


@app.post("/visited_links")
async def post_visited_links(
    data: schemas.UniqueDomainList, db: Annotated[Session, Depends(get_db)]
):
    domains = data.domains
    items_to_add = [
        DomainItem(domain=domain, date_visited=datetime.datetime.utcnow())
        for domain in domains
    ]
    db.add_all(items_to_add)
    return {"status": "ok"}


@app.get("/visited_domains")
async def get_visited_domains(
    db: Annotated[Session, Depends(get_db)],
    date_from: datetime.datetime | None = None,
    date_to: datetime.datetime | None = None,
):
    query = select(DomainItem.domain).distinct()
    if date_from is not None:
        query = query.where(DomainItem.date_visited >= date_from)
    if date_to is not None:
        query = query.where(DomainItem.date_visited <= date_to)

    unique_domains_visited = db.execute(query).scalars().all()

    return {"status": "ok", "domains": unique_domains_visited}
