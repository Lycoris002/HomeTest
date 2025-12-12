import fastapi

router = fastapi.APIRouter()


@router.post("/auth/token")
async def login():
    return {"token": f"Bearer"}
