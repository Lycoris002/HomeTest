import fastapi

router = fastapi.APIRouter()


@router.get('/v1/files/{file_id}/transactions')
async def get_file_transactions(file_id: int):
    pass


