# src/apps/shortener/models.py
from xmlrpc.client import DateTime
from sqlalchemy.sql import func
from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, func, UniqueConstraint
from datetime import datetime


class ShortenedUrl(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    main_url: str = Field(nullable=False)
    short_url: str = Field(index=True, nullable=False, unique=True)
    custom_domain: Optional[str] = Field(default=None, index=True)
    click_count: int = Field(default=0, nullable=False)
    max_clicks: Optional[int] = Field(default=None)
    active: bool = Field(default=True)
    expired: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    expires_at: Optional[datetime] = Field(default=None)


class VisitLog(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    short_url: str = Field(nullable=False)
    client_ip: str = Field(nullable=False)
    system_id: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    device: Optional[str] = None
    os: Optional[str] = None
    browser: Optional[str] = None
    visited_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)

Base = declarative_base()


#-----------------------------Campaign Model-----------------------#

class CampaignSource(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "campaign_source_tag", name="uq_source_user_tag"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    unique_id: str = Field(max_length=6, index=True)
    user_id: str = Field(index=True)
    campaign_source_tag: str
    campaign_source_name: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=func.now(), onupdate=func.now())
    )


class CampaignMedium(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "campaign_medium_tag", name="uq_medium_user_tag"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    unique_id: str = Field(max_length=6, index=True, nullable=False)
    user_id: str = Field(index=True, nullable=False)
    campaign_medium_tag: str = Field(nullable=False)
    campaign_medium_name: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )


class CampaignName(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "campaign_name_tag", name="uq_name_user_tag"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    unique_id: str = Field(max_length=6, index=True, nullable=False)
    user_id: str = Field(index=True, nullable=False)
    campaign_name_tag: str = Field(nullable=False)
    campaign_name: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )
