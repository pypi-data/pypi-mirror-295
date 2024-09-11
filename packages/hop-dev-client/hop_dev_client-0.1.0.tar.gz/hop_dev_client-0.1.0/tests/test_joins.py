import logging
from hop import Hop
from hop import Group, User, Record
import pytest
from uuid import uuid4
from hop import HopError
from .utilities_test import randomString

logger = logging.getLogger(__name__)


@pytest.fixture
def session():
    return Hop.startSession(
        base_url="https://kj2bju0c9f.execute-api.us-east-1.amazonaws.com/prod",
        token_endpoint="https://hopjoinsdev.auth.us-east-1.amazoncognito.com/oauth2/token",
        client_id="5blm794ina9nbvjr98j9lm1v7o",
        client_secret="s1a8jm3mbjbeodf9eterqslfrelsqnt35fuf6gvnm9mgoo7s47p",
    )


# Testing methods for add records
# @pytest.mark.skip
def test_add_records_case1(session):
    try:

        record_1_id = randomString(10)

        record_1 = Record(
            record_id=record_1_id,
            partner_id="INT-CRM",
            object_id="SF_ACCOUNT",
        )

        record_1.set_session(session=session)

        record_1.get_uuid()

        record_2_id = randomString(10)

        record_2 = Record(
            record_id=record_2_id,
            partner_id="INT-CRM",
            object_id="SF_ACCOUNT",
        )

        record_2.set_session(session=session)

        record_2.get_uuid()

        record_3_id = randomString(10)

        record_3 = Record(
            record_id=record_3_id,
            partner_id="INT-CRM",
            object_id="SF_ACCOUNT",
        )

        record_3.set_session(session=session)

        record_3.get_uuid()

        user_record_id = randomString(10)
        user = User(
            record_id=user_record_id,
            partner_id=str("INT-CRM"),
            object_id=str("ACCOUNT"),
            user_name="username1",
        )
        user.set_session(session=session)

        user.get_uuid()

        logger.debug(f"User Created {user}")

        group_1_id = randomString(10)
        group_1 = Group(
            group_id=group_1_id,
            partner_id="INT-CRM",
            object_type="ACCOUNT",
            application_id="SF",
            group_name="Group Name 21",
            owner_uuid=user.uuid,
        )
        group_1.set_session(session=session)
        group_1.get_uuid()
        logger.debug(f"Group Created : {group_1}")
        group_1.add_record(record=record_1)
        group_1.add_record(record=record_2)

        group_2_id = randomString(10)
        group_2 = Group(
            group_id=group_2_id,
            partner_id="INT-CRM",
            object_type="ACCOUNT",
            application_id="SF",
            group_name="Group Name 22",
            owner_uuid=user.uuid,
        )
        group_2.set_session(session=session)
        group_2.get_uuid()
        logger.debug(f"Group Created : {group_2}")
        group_2.add_record(record=record_1)
        group_2.add_record(record=record_3)

    except Exception as e:
        logger.debug("Exception is thrown in test method")
        logger.debug(e)
