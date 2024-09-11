from abc import abstractmethod
from typing import Optional
from uuid import UUID
from datetime import datetime
from lqs.interface.base.create import CreateInterface as BaseCreateInterface
import lqs.interface.dsm.models as models


class CreateInterface(BaseCreateInterface):
    @abstractmethod
    def _announcement(self, **kwargs) -> models.AnnouncementDataResponse:
        pass

    def announcement(
        self,
        datastore_id: Optional[UUID] = None,
        subject: Optional[str] = None,
        content: Optional[str] = None,
        context: Optional[dict] = None,
        status: Optional[str] = None,
        starts_at: Optional[datetime] = None,
        ends_at: Optional[datetime] = None,
    ):
        return self._announcement(
            datastore_id=datastore_id,
            subject=subject,
            content=content,
            context=context,
            status=status,
            starts_at=starts_at,
            ends_at=ends_at,
        )

    def _announcement_by_model(self, data: models.AnnouncementCreateRequest):
        return self.announcement(**data.model_dump())

    @abstractmethod
    def _comment(self, **kwargs) -> models.CommentDataResponse:
        pass

    def comment(
        self,
        user_id: Optional[UUID] = None,
        datastore_id: Optional[UUID] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[UUID] = None,
        subject: Optional[str] = None,
        content: Optional[str] = None,
        context: Optional[dict] = None,
    ):
        return self._comment(
            user_id=user_id,
            datastore_id=datastore_id,
            resource_type=resource_type,
            resource_id=resource_id,
            subject=subject,
            content=content,
            context=context,
        )

    def _comment_by_model(self, data: models.CommentCreateRequest):
        return self.comment(**data.model_dump())

    @abstractmethod
    def _configuration(self, **kwargs) -> models.ConfigurationDataResponse:
        pass

    def configuration(
        self,
        value: dict,
        name: Optional[str] = None,
        note: Optional[str] = None,
        default: bool = False,
        disabled: bool = False,
    ):
        return self._configuration(
            value=value,
            name=name,
            note=note,
            default=default,
            disabled=disabled,
        )

    def _configuration_by_model(self, data: models.ConfigurationCreateRequest):
        return self.configuration(**data.model_dump())

    @abstractmethod
    def _datastore(self, **kwargs) -> models.DataStoreDataResponse:
        pass

    def datastore(
        self,
        name: str,
        note: Optional[str] = None,
        context: Optional[dict] = None,
        owner_id: Optional[UUID] = None,
        config: Optional[dict] = None,
        version: Optional[str] = None,
        region: Optional[str] = None,
        endpoint: Optional[str] = None,
        disabled: bool = False,
    ):
        return self._datastore(
            name=name,
            note=note,
            context=context,
            owner_id=owner_id,
            config=config,
            version=version,
            region=region,
            endpoint=endpoint,
            disabled=disabled,
        )

    def _datastore_by_model(self, data: models.DataStoreCreateRequest):
        return self.datastore(**data.model_dump())

    @abstractmethod
    def _datastore_association(
        self, **kwargs
    ) -> models.DataStoreAssociationDataResponse:
        pass

    def datastore_association(
        self,
        user_id: UUID,
        datastore_id: UUID,
        manager: bool = False,
        disabled: bool = False,
        datastore_user_id: Optional[UUID] = None,
        datastore_username: Optional[str] = None,
        datastore_role_id: Optional[UUID] = None,
        datastore_admin: bool = False,
        datastore_disabled: bool = False,
    ):
        return self._datastore_association(
            user_id=user_id,
            datastore_id=datastore_id,
            manager=manager,
            disabled=disabled,
            datastore_user_id=datastore_user_id,
            datastore_username=datastore_username,
            datastore_role_id=datastore_role_id,
            datastore_admin=datastore_admin,
            datastore_disabled=datastore_disabled,
        )

    def _datastore_association_by_model(
        self, data: models.DataStoreAssociationCreateRequest
    ):
        return self.datastore_association(**data.model_dump())

    @abstractmethod
    def _ticket(self, **kwargs) -> models.TicketDataResponse:
        pass

    def ticket(
        self,
        type: models.TicketType,
        description: str,
        email: str,
    ):
        return self._ticket(
            type=type,
            description=description,
            email=email,
        )

    def _ticket_by_model(self, data: models.TicketCreateRequest):
        return self.ticket(**data.model_dump())

    @abstractmethod
    def _usage_record(self, **kwargs) -> models.UsageRecordDataResponse:
        pass

    def usage_record(
        self,
        timestamp: models.Int64,
        datastore_id: UUID,
        duration: Optional[models.Int64] = None,
        category: Optional[str] = None,
        usage_data: Optional[dict | list] = None,
    ):
        return self._usage_record(
            timestamp=timestamp,
            datastore_id=datastore_id,
            duration=duration,
            category=category,
            usage_data=usage_data,
        )

    def _usage_record_by_model(
        self, datastore_id: UUID, data: models.UsageRecordCreateRequest
    ):
        return self.usage_record(datastore_id=datastore_id, **data.model_dump())
