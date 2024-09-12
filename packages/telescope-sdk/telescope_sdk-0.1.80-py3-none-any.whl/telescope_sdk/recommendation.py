from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class RecommendationType(str, Enum):
    STANDARD = "STANDARD"
    DAILY = "DAILY"
    LIST = "LIST"


class RecommendationStatus(str, Enum):
    PENDING = "PENDING"
    IGNORED = "IGNORED"
    SKIPPED = "SKIPPED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class RecommendationMode(str, Enum):
    COMPANY = "COMPANY"
    LEAD = "LEAD"


class RecommendationRejectionReason(str, Enum):
    WRONG_POSITION_RIGHT_COMPANY = "WRONG_POSITION_RIGHT_COMPANY"
    NOT_RELEVANT = "NOT_RELEVANT"
    RIGHT_POSITION_WRONG_COMPANY = "RIGHT_POSITION_WRONG_COMPANY"
    DISCARDED = "DISCARDED"
    OTHER = "OTHER"
    EXISTING_CUSTOMER = "EXISTING_CUSTOMER"
    ALREADY_CONTACTED = "ALREADY_CONTACTED"


class Recommendation(BaseModel):
    id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime
    status: RecommendationStatus
    company_recommendation_id: Optional[str]
    person_id: Optional[str]
    company_id: Optional[str]
    deleted_at: Optional[str] = None
    model_info: Optional[dict] = None
    rejection_reason: Optional[RecommendationRejectionReason] = None
    ranker_version: Optional[float] = None
    type: Optional[RecommendationType] = None
    additional_data: Optional[dict] = None
    icp_match_confidence: Optional[int] = None
    mode: Optional[RecommendationMode] = None
    special_criteria_evaluation_results: Optional[dict] = None
    resolved_at: Optional[str | datetime] = None
    recommendation_reason: Optional[str] = None
    email_enrichment_result_id: Optional[str] = None
    phone_number_enrichment_result_id: Optional[str] = None
    recommendations_list_id: Optional[str] = None
    campaign_id: Optional[str] = None
    candidate_origin: Optional[str] = None
    candidate_version: Optional[str] = None
    ranker_score: Optional[str] = None
    person_record_id: Optional[str] = None
    company_record_id: Optional[str] = None
    icp_id: Optional[str] = None
    merge_crm_lead_id: Optional[str] = None
    merge_crm_contact_id: Optional[str] = None
    merge_crm_account_id: Optional[str] = None
