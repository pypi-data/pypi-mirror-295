from fastapi import APIRouter

router = APIRouter()


@router.get("/github", include_in_schema=False)
def get_dash_memus():
    return "webhook-github called"
