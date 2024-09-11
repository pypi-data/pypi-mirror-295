from uuid import UUID
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    ValidationError,
    field_serializer,
)
from .._utilities import Session
import httpx
from httpx import URL, Headers, Response
from typing import Optional
import logging
from .._exceptions import HopError

logger = logging.getLogger(__name__)


class Record(BaseModel):
    """
    A Record that is syncronized using Hop

    Records are not back-linked to parent Groups for simplicity
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    uuid: UUID = Field(default=None)
    """Hop-managed record UUID"""
    record_id: str = Field(serialization_alias="recordId")
    """ID assigned by the client"""
    object_id: str = Field(serialization_alias="objectId")
    """ Type of record, e.g. ACCOUNT, CONTACT.
        This is combination of application id and object id (<application_id>_<object_id>).
        Example : "SF_ACCOUNT" , "SF_CONTACT"
    """
    partner_id: str = Field(serialization_alias="partnerId")
    """Company Id"""
    session: Optional[Session] = Field(default=None, exclude=True)
    """session object connects this record to a particular instance of Hop"""
    records_endpoint: Optional[httpx.URL] = Field(default=None, exclude=True)

    @field_validator("uuid")
    @classmethod
    def validate_uuids(cls, value) -> UUID:
        try:
            if isinstance(value, str):
                logger.debug(f"{value} in string")
                return UUID(value, version=4)
            elif isinstance(value, UUID):
                logger.debug(f"{value} in UUID")
                return value
            else:
                logger.debug("Validation error raised")
                raise ValidationError(
                    "Field uuid must be a valid uuid in string format or UUID"
                )
        except:
            logger.debug("Validation error raised")
            raise ValidationError(
                "Field uuid must be a valid uuid in string format or UUID"
            )

    @field_serializer("uuid")
    def serialize_uuid(self, value: UUID):
        if value == None:
            return None
        return str(value)

    def set_session(self, session: Session):
        self.session = session
        self.records_endpoint = URL((str(session.base_url)) + "/records")
        logger.debug(f"RECORDS ENDPOINT : {str(self.records_endpoint)}")

    def isConnected(self):
        if self.session != None:
            return True
        else:
            raise HopError(
                "Hop Object not connected to hop instance. Please connect the object to an instance of hop using a session object"
            )

    def get_uuid(self, force=False):
        """Generate UUID for a for paricular combination of client_id and systemId(partner_id)"""
        try:
            if self.isConnected():
                request_body = self.model_dump(by_alias=True)
                request_body["force"] = force
                logger.debug(f"Request Body : {request_body}")
                headers = Headers({"Content-Type": "application/json"})
                response = httpx.post(
                    url=self.records_endpoint, json=request_body, headers=headers
                )
                logger.debug(response.json())
                if response.status_code == httpx.codes.CREATED:
                    response_body = dict(response.json())
                    self.uuid = UUID(str(response_body["data"]["uuid"]))
                else:
                    logger.debug("uuid mismatch. Raising Exception")
                    raise HopError(
                        "Error while assigning uuid. uuid doesnt match record id sent. Set force flag, If the uuid needs to be overidden on hop"
                    )

        except httpx.HTTPError as exc:
            logger.error(f"HTTP Exception for {exc.request.url} - {exc}")
            raise exc
        logger.debug("EXEC COMPLETE : get_uuid")

    def delete(self) -> bool:
        """Delete the record. Explore Casacade delete in a async way"""
        try:
            if self.uuid == None:
                raise HopError("Object doesnt have uuid assigned yet.")
            if self.isConnected():
                # delete the record using UUID.
                delete_url = URL((str(self.records_endpoint)) + f"/{str(self.uuid)}")
                response = httpx.delete(url=delete_url)
                if response.status_code == httpx.codes.OK:
                    return True
                else:
                    raise HopError("Deletion failed. Please provide a valid uuid")
        except Exception as e:
            logger.error(f"Method delete : {e}")
            raise e
        pass

    def update(self):
        """For a UUID change anyone of the following partner_id, object_id and record_id"""
        pass
        try:
            if self.uuid == None:
                raise HopError("Object doesnt have uuid assigned yet.")
            if self.isConnected():
                request_body = self.model_dump(by_alias=True, exclude={"uuid"})
                update_url = URL((str(self.records_endpoint)) + f"/{str(self.uuid)}")
                headers = Headers({"Content-Type": "application/json"})
                response = httpx.put(url=update_url, json=request_body, headers=headers)
                logger.debug(response.json())
                if response.status_code == httpx.codes.OK:
                    return True
                else:
                    raise HopError(
                        "Record Updation failed. Please provide a valid uuid"
                    )
        except Exception as e:
            logger.error(f" Method update : {e}")
            raise e
