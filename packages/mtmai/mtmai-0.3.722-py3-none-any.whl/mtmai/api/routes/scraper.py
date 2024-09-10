import logging

from fastapi import APIRouter
from opentelemetry import trace
from pydantic import BaseModel

from mtmai.toolsv2.readable import get_readable_text

tracer = trace.get_tracer_provider().get_tracer(__name__)
logger = logging.getLogger()


router = APIRouter()


class ScraperReadableReq(BaseModel):
    url: str


@router.post("/readable")
async def test_readable(req: ScraperReadableReq):
    content = get_readable_text(req.url)
    return content
