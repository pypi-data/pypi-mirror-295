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
from httpx import URL, Headers
from typing import Optional
import logging
from .._exceptions import HopError
from .user import User
from .records import Record

logger = logging.getLogger(__name__)


class Group(BaseModel):
    """
    Group contains uuid for the records. Its used to group records.
    A Group is syncronized using Hop
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    uuid: UUID = Field(default=None)
    """Hop-managed record UUID"""
    group_id: str = Field(serialization_alias="groupId")
    """ID assigned by the client"""
    application_id: str = Field(serialization_alias="applicationId")
    """
    Application_id is the application id
        for example salesforce application id will be "SF"
    """
    object_type: str = Field(serialization_alias="objectType")
    """ Type of objects in the group e.g. ACCOUNT, CONTACT.
        For more than one type in the group append the type names. e.g. ACCOUNT_CONTACT
        Combination of application id and object type together form the object_id or campaign id(<application_id>_<object_id>).
        e.g. "SF_ACCOUNT" , "SF_CONTACT"
    """
    partner_id: str = Field(serialization_alias="partnerId")
    """Company Id"""
    group_name: str = Field(serialization_alias="groupName")
    """Group Name for the group. Unique for a particular Application Id"""
    owner_uuid: UUID = Field(default=None, serialization_alias="ownerUUID")
    """uuid of group owner"""
    # Excluded Fields
    session: Optional[Session] = Field(default=None, exclude=True)
    """session object connects this record to a particular instance of Hop"""
    groups_endpoint: Optional[httpx.URL] = Field(default=None, exclude=True)
    groups_add_records_endpoint: Optional[httpx.URL] = Field(default=None, exclude=True)
    """Groups Endpoint"""
    records: list[Record] = []

    @field_validator("uuid", "owner_uuid")
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

    @field_serializer("uuid", "owner_uuid")
    def serialize_uuid(self, value: UUID):
        if value == None:
            return None
        return str(value)

    def set_session(self, session: Session):
        self.session = session
        self.groups_endpoint = URL((str(session.base_url)) + "/groups")
        self.groups_add_records_endpoint = URL(
            str(session.base_url) + "/groups/add_records"
        )
        logger.debug(f"GROUPS ENDPOINT : {str(self.groups_endpoint)}")

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
            if self.owner_uuid == None:
                raise HopError("owner uuid must be provided")
            if self.isConnected():
                request_body = self.model_dump(by_alias=True)
                request_body["force"] = force
                logger.debug(f"Request Body : {request_body}")
                headers = Headers({"Content-Type": "application/json"})
                response = httpx.post(
                    url=self.groups_endpoint, json=request_body, headers=headers
                )
                logger.debug(response.json())
                if response.status_code == httpx.codes.CREATED:
                    response_body = dict(response.json())
                    self.uuid = UUID(str(response_body["data"]["uuid"]))
                elif response.status_code == httpx.codes.BAD_REQUEST:
                    response_body = dict(response.json())
                    error_code = response_body["data"]["errorCode"]
                    message = response_body["data"]["message"]
                    logger.debug(f"Error Code {error_code} message {message}")
                    raise HopError(message)
                else:
                    logger.debug("Server Error. Raising Exception")
                    raise HopError("Server Error")

        except httpx.HTTPError as exc:
            logger.error(f"HTTP Exception for {exc.request.url} - {exc}")
            raise exc
        logger.debug("EXEC COMPLETE : get_uuid")

    def add_record(self, record: Record):
        try:
            if self.isConnected():
                request_body = {
                    "groupUUID": str(self.uuid),
                    "records": [str(record.uuid)],
                }
                headers = Headers({"Content-Type": "application/json"})
                response = httpx.post(
                    url=self.groups_add_records_endpoint,
                    json=request_body,
                    headers=headers,
                )
                logger.debug(response.json())
        except Exception as e:
            logger.debug("Exception thrown when adding records")
            logger.debug(e)
