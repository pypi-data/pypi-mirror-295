from typing import Optional, Tuple

from thestage.services.clients.thestage_api.dtos.container_response import DockerContainerDto
from thestage.entities.container import DockerContainerEntity
from thestage.services.abstract_mapper import AbstractMapper


class ContainerMapper(AbstractMapper):

    def build_entity(self, item: DockerContainerDto) -> Optional[DockerContainerEntity]:
        if not item:
            return None

        return DockerContainerEntity(
            status=item.frontend_status.status_translation if item.frontend_status else '',
            slug=item.slug or '',
            title=item.title or '',
            instance_rented_slug=item.instance_rented.slug if item.instance_rented else '',
            selfhosted_rented_slug=item.selfhosted_instance.slug if item.selfhosted_instance else '',
            docker_image=item.docker_image or '',
        )
