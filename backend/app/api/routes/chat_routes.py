import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.connection import get_db
from backend.app.api.schemas.chat_schema import ChatRequest
from backend.app.agents.stockland_agent import StocklandAgent



router = APIRouter()

@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):

    session_id = getattr(request, "session_id", "chat_1")
    try:

        result = await StocklandAgent.run(
            db,
            request.message,
            session_id=session_id
        )

        return {"answer": result["answer"]}

    except Exception as e:
        print("\n=========== AGENT ERROR ===========")
        traceback.print_exc()
        print("===================================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/clear-redis-cache-danger-zone")
async def clear_redis():
    from backend.app.core.redis_cache import redis_client
    # This deletes EVERYTHING in your Redis instance
    await redis_client.flushall()
    return {"status": "Success", "message": "Redis Cache has been completely cleared!"}
