from fastapi import APIRouter

from api.app.constants import API_PREFIX

router = APIRouter(
    prefix=f"{API_PREFIX}/health",
    tags=["Health"],
)


@router.get("")
def health():
    return {
        "status": "healthy"
    }