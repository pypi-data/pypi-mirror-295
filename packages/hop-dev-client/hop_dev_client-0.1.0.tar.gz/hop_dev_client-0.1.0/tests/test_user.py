import logging
from hop import Hop
from hop import User
import pytest
from uuid import uuid4
from hop import HopError
from .utilities_test import randomString

logger = logging.getLogger(__name__)


@pytest.fixture
def session():
    return Hop.startSession(
        base_url="https://d7byn99lnj.execute-api.us-east-1.amazonaws.com/prod/",
        token_endpoint="https://hopjoinsdev.auth.us-east-1.amazoncognito.com/oauth2/token",
        client_id="4qvb32q7f6e69fph4qeq7pcef3",
        client_secret="1tqfg52dcdbge11ltq0issc9cpqdb0bhocsboo9fp3t8nmomp3ci",
    )


@pytest.mark.skip
def test_get_uuid_case_1(session):
    logger.debug("Testing test_get_uuid")
    """Create a local Record object"""
    record_id = randomString(10)
    record = User(
        record_id=record_id,
        partner_id=str("INT-CRM"),
        object_id=str("ACCOUNT"),
        user_name="username1",
    )
    record.set_session(session=session)
    logger.debug(record)

    record.get_uuid()

    assert record.uuid != None
