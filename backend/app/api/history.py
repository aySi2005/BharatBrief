"""History API endpoints — view, search, delete, favorite summaries."""
import logging
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, or_

from app.schemas.summary import HistoryItem, HistoryListResponse
from app.services.auth_service import decode_token
from app.database import get_db
from app.models.summary import Summary

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/history", tags=["history"])


async def _get_user_id(token: str) -> str:
    """Extract user_id from JWT token."""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload["sub"]


@router.get("", response_model=HistoryListResponse)
async def list_history(
    token: str,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    search: str = Query(default=""),
    favorites_only: bool = Query(default=False),
    db: AsyncSession = Depends(get_db),
):
    """List user's summarization history."""
    user_id = await _get_user_id(token)
    
    query = select(Summary).where(Summary.user_id == user_id)
    count_query = select(func.count(Summary.id)).where(Summary.user_id == user_id)
    
    if favorites_only:
        query = query.where(Summary.is_favorite == True)
        count_query = count_query.where(Summary.is_favorite == True)
    
    if search:
        search_filter = or_(
            Summary.title.ilike(f"%{search}%"),
            Summary.summary_text.ilike(f"%{search}%"),
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)
    
    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Get paginated results
    offset = (page - 1) * per_page
    query = query.order_by(desc(Summary.created_at)).offset(offset).limit(per_page)
    result = await db.execute(query)
    summaries = result.scalars().all()
    
    items = [
        HistoryItem(
            id=s.id,
            title=s.title,
            summary_text=s.summary_text,
            source_type=s.source_type,
            source_url=s.source_url,
            summary_length=s.summary_length,
            original_word_count=s.original_word_count,
            is_favorite=s.is_favorite,
            created_at=s.created_at,
        )
        for s in summaries
    ]

    return HistoryListResponse(items=items, total=total, page=page, per_page=per_page)


@router.delete("/{summary_id}")
async def delete_summary(
    summary_id: str,
    token: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete a summary."""
    user_id = await _get_user_id(token)
    
    result = await db.execute(
        select(Summary).where(Summary.id == summary_id, Summary.user_id == user_id)
    )
    summary = result.scalar_one_or_none()
    
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    await db.delete(summary)
    return {"message": "Summary deleted"}


@router.patch("/{summary_id}/favorite")
async def toggle_favorite(
    summary_id: str,
    token: str,
    db: AsyncSession = Depends(get_db),
):
    """Toggle favorite status of a summary."""
    user_id = await _get_user_id(token)
    
    result = await db.execute(
        select(Summary).where(Summary.id == summary_id, Summary.user_id == user_id)
    )
    summary = result.scalar_one_or_none()
    
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    summary.is_favorite = not summary.is_favorite
    return {"is_favorite": summary.is_favorite}
