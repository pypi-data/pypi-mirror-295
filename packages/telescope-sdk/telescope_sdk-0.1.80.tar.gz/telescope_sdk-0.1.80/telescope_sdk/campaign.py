from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime

from pydantic import BaseModel


class ICPAssistantChatMessageType(str, Enum):
    MESSAGE = "MESSAGE"
    ERROR = "ERROR"


class ICPAssistantChatMessageSender(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class ICPAssistantChatMessage(BaseModel):
    type: ICPAssistantChatMessageType
    sender: ICPAssistantChatMessageSender
    text: str
    sent_at: str


class OutreachStatus(str, Enum):
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    ERROR = 'DISABLED'


class RecommendationMode(str, Enum):
    COMPANY = "COMPANY"
    LEAD = "LEAD"


class ProfileBuilderMessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ProfileBuilderToolCall(BaseModel):
    id: str
    type: str
    function: Dict[str, Any]


class ProfileBuilderMessage(BaseModel):
    role: ProfileBuilderMessageRole
    content: Optional[str]
    tool_calls: Optional[List[ProfileBuilderToolCall]]
    tool_call_id: Optional[str]


class Campaign(BaseModel):
    name: str
    id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime
    outreach_status: OutreachStatus
    sequence_id: Optional[str] = None
    active_icp_id: Optional[str] = None
    recommendation_mode: Optional[RecommendationMode] = None
    active_recommendations_list_id: Optional[str] = None
    company_profile_builder_messages: Optional[List[ProfileBuilderMessage]] = None
    company_profile_data: Optional[Dict[str, Any]] = None
    prospect_profile_builder_messages: Optional[List[ProfileBuilderMessage]] = None
    prospect_profile_data: Optional[Dict[str, Any]] = None
    clay_auto_sync: Optional[bool] = None
    clay_webhook_url: Optional[str] = None
    deleted_at: Optional[datetime] = None
    outreach_enabled: Optional[bool] = None
    icp_assistant_chat_history: Optional[List[ICPAssistantChatMessage]] = None
    icp_assistant_chat_enabled: Optional[bool] = None
    selected_extracted_icp: Optional[Any] = None
