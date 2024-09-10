import logging

from fastapi import APIRouter, Depends
from opentelemetry import trace
from pydantic import BaseModel

from mtmai.api.deps import get_current_active_superuser
from mtmai.toolsv2.readable import get_readable_text

tracer = trace.get_tracer_provider().get_tracer(__name__)
logger = logging.getLogger()


router = APIRouter()


class ScraperReadableReq(BaseModel):
    url: str


@router.post(
    "/readable",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
    include_in_schema=False,
)
async def test_readable(req: ScraperReadableReq):
    content = get_readable_text(req.url)
    return content
