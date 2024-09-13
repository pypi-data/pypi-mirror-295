from typing import Optional, List

from pydantic import Field, BaseModel, ConfigDict

from thestage.services.clients.thestage_api.dtos.enums.container_pending_action import ContainerPendingActionEnumDto

class DockerContainerActionRequestDto(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    container_id: Optional[int] = Field(None, alias='dockerContainerId')
    action: ContainerPendingActionEnumDto = Field(ContainerPendingActionEnumDto.UNKNOWN, alias='action')
