from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from thestage.services.logging.dto.log_type import LogType


class LogMessage(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )

    log_type: Optional[LogType] = Field(None, alias='log_type')
    message: Optional[str] = Field(None, alias='message')
    timestamp: Optional[str] = Field(None, alias='timestamp')
