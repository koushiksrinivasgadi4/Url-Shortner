from typing import List
from sqlalchemy import func
from redis.asyncio import Redis
from fastapi import Query, Request, APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from services import campaign_services
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from pydantic import BaseModel
from apps.shortener.schemas import CampaignMediumCreate, CampaignMediumUpdate, CampaignNameCreate, CampaignNameUpdate, CampaignSourceCreate, CampaignSourceUpdate, ShortenUrlRequest, ShortenUrlResponse
from apps.shortener.models import ShortenedUrl, VisitLog
from apps.shortener.controllers import shortener_controller
from services.redis import get_redis
from services.visit_service import visit_service
from services.database import async_session, get_session, engine, Base
from apps.shortener import schemas as campaign_schemas
from services import campaign_services




campaign_router = APIRouter(
    tags=["Campaign"],  # 👈 this controls the heading in Swagger UI
    prefix="/campaign"
)

shortener_router = APIRouter(
    tags=["Shortener"],
    prefix=""
)
utm_router = APIRouter(prefix="/utm", tags=["UTM"])

# --- Shorten URL API ---
@shortener_router.post(
    "/shorten",
    response_model=ShortenUrlResponse,
    status_code=status.HTTP_200_OK,
)
async def shorten(
    payload: ShortenUrlRequest,
    db: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis)
):
    return await shortener_controller.shorten(
        db=db,
        redis=redis,
        payload=payload
    )


# --- Redirect API ---
@shortener_router.get("/{short_url}", status_code=status.HTTP_200_OK)
async def redirect_to_main_url(
    short_url: str,
    request: Request,
    db: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis)
):
    short_url = short_url.strip().strip('"').strip("'")

    response = await shortener_controller.redirect_to_main_url(
        db=db,
        redis=redis,
        short_url=short_url,
        request=request
    )

    user_agent = request.headers.get("user-agent", "").lower()
    accept = request.headers.get("accept", "").lower()

    if isinstance(response, RedirectResponse):
        if "swagger" in user_agent or "json" in accept:
            return JSONResponse(
                status_code=200,
                content={
                    "details": {
                        "message": "Redirection successful.",
                        "redirect_to": response.headers.get("location"),
                        "short_code": short_url,
                        "domain": request.headers.get("host", "")
                    },
                    "status_code": 200
                }
            )
        return response

    return response


# --- Click Count API ---
@shortener_router.get("/stats/{short_url}")
async def get_click_count(short_url: str, db: AsyncSession = Depends(get_session)):
    query = select(VisitLog).where(VisitLog.short_url == short_url)
    result = await db.execute(query)
    logs = result.fetchall()
    click_count = len(logs)

    return {"short_url": short_url, "click_count": click_count}


# --- Visit Logs by Client IP API ---
@shortener_router.get("/visitlogs/client/{client_ip}")
async def get_visits_by_client_ip(
    client_ip: str,
    db: AsyncSession = Depends(get_session)
):
    visits = await visit_service.get_visits_by_client_ip(db, client_ip)
    if visits:
        return {"client_ip": client_ip, "visit_logs": visits}

    raise HTTPException(status_code=404, detail="No visit logs found for this client IP")





#-------------Campaign------------------#

@campaign_router.post("/campaign/source")
async def create_campaign_source(
    payload: CampaignSourceCreate,
    db: AsyncSession = Depends(get_session)
):
    return await campaign_services.create_campaign_source(
        db,
        payload.user_id,
        payload.campaign_source_tag,
        payload.campaign_source_name
    )

@campaign_router.get("/campaign/source/{user_id}")
async def get_campaign_sources(user_id: str, db: AsyncSession = Depends(get_session)):
    return await campaign_services.get_campaign_sources_by_user(db, user_id)


@campaign_router.put("/campaign/source/{user_id}/{unique_id}")
async def update_campaign_source(
    user_id: str,
    unique_id: str,
    payload: CampaignSourceUpdate,
    db: AsyncSession = Depends(get_session)
):
    return await campaign_services.update_campaign_source(
        db,
        user_id,
        unique_id,
        payload
    )

@campaign_router.delete("/campaign/source/{user_id}/{unique_id}")
async def delete_campaign_source(user_id: str, unique_id: str, db: AsyncSession = Depends(get_session)):
    return await campaign_services.delete_campaign_source(db, user_id, unique_id)

# ===========================
# Campaign Medium APIs
# ===========================

@campaign_router.post("/campaign/medium")
async def create_campaign_medium(

    payload: CampaignMediumCreate,
    db: AsyncSession = Depends(get_session)
):
    return await campaign_services.create_campaign_medium(
        db,
        payload.user_id,
        payload.campaign_medium_tag,
        payload.campaign_medium_name
    )

@campaign_router.get("/campaign/medium/{user_id}")
async def get_campaign_mediums(user_id: str, db: AsyncSession = Depends(get_session)):
    return await campaign_services.get_campaign_mediums_by_user(db, user_id)


@campaign_router.put("/campaign/medium/{user_id}/{unique_id}")
async def update_campaign_medium(
    user_id: str,
    unique_id: str,
    payload: CampaignMediumUpdate,
    db: AsyncSession = Depends(get_session)
):
    return await campaign_services.update_campaign_medium(
        db,
        user_id,
        unique_id,
        payload
    )


@campaign_router.delete("/campaign/medium/{user_id}/{unique_id}")
async def delete_campaign_medium(user_id: str, unique_id: str, db: AsyncSession = Depends(get_session)):
    return await campaign_services.delete_campaign_medium(db, user_id, unique_id)

# ===========================
# Campaign Name APIs
# ===========================

@campaign_router.post("/campaign/name")
async def create_campaign_name(
    payload: CampaignNameCreate,
    db: AsyncSession = Depends(get_session)
):
    return await campaign_services.create_campaign_name(
        db,
        payload.user_id,
        payload.campaign_name_tag,
        payload.campaign_name
    )


@campaign_router.get("/campaign/name/{user_id}")
async def get_campaign_names(user_id: str, db: AsyncSession = Depends(get_session)):
    return await campaign_services.get_campaign_names_by_user(db, user_id)


@campaign_router.put("/campaign/name/{user_id}/{unique_id}")
async def update_campaign_name(
    user_id: str,
    unique_id: str,
    payload: CampaignNameUpdate,
    db: AsyncSession = Depends(get_session)
):
    return await campaign_services.update_campaign_name(
        db,
        user_id,
        unique_id,
        payload
    )



@campaign_router.delete("/campaign/name/{user_id}/{unique_id}")
async def delete_campaign_name(user_id: str, unique_id: str, db: AsyncSession = Depends(get_session)):
    return await campaign_services.delete_campaign_name(db, user_id, unique_id)

# ===========================
# UTM URL Builder API
# ===========================

# @campaign_router.post("/campaign_utm_url")
# async def campaign_utm_url(payload: campaign_schemas.UTMBuildRequest, db: AsyncSession = Depends(get_session)):
#     sources = await campaign_services.get_campaign_sources(db, payload.user_id)
#     mediums = await campaign_services.get_campaign_mediums(db, payload.user_id)
#     names = await campaign_services.get_campaign_names(db, payload.user_id)

#     if not (sources and mediums and names):
#         raise HTTPException(status_code=404, detail="Campaign details not found for user")

#     # Pick the latest one (or apply your logic here)
#     source = sources[-1]
#     medium = mediums[-1]
#     name = names[-1]

#     # Build UTM URL
#     campaign_url = (
#         f"{payload.main_url}?"
#         f"campaign_source_tag={source.campaign_source_tag}&campaign_source_name={source.campaign_source_name}"
#         f"&campaign_medium_tag={medium.campaign_medium_tag}&campaign_medium_name={medium.campaign_medium_name}"
#         f"&campaign_name_tag={name.campaign_name_tag}&campaign_name={name.campaign_name}"
#     )
#     return {"campaign_url": campaign_url}
