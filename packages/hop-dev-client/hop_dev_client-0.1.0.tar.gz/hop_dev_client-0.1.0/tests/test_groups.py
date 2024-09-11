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
        base_url="https://d7byn99lnj.execute-api.us-east-1.amazonaws.com/prod/",
        token_endpoint="https://hopjoinsdev.auth.us-east-1.amazoncognito.com/oauth2/token",
        client_id="4qvb32q7f6e69fph4qeq7pcef3",
        client_secret="1tqfg52dcdbge11ltq0issc9cpqdb0bhocsboo9fp3t8nmomp3ci",
    )


# case 1
# create group successfully
@pytest.mark.skip
def test_get_uuid_case1(session):

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

    group_id = randomString(10)
    group = Group(
        group_id=group_id,
        partner_id="INT-CRM",
        object_type="ACCOUNT",
        application_id="SF",
        group_name="Group Name 1",
        owner_uuid=record.uuid,
    )
    group.set_session(session=session)
    group.get_uuid()
    logging.debug(group.model_dump())
    assert group.uuid != None


# case 2 :
# try creating group with same name for the same application id
# except to fail. Group Name must be unique for a particular application id
@pytest.mark.skip
def test_get_uuid_case2(session):
    try:

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

        group_1_id = randomString(10)
        group_1 = Group(
            group_id=group_1_id,
            partner_id="INT-CRM",
            object_type="ACCOUNT",
            application_id="SF",
            group_name="Group Name 2",
            owner_uuid=record.uuid,
        )
        group_1.set_session(session=session)
        group_1.get_uuid()

        group_2_id = randomString(10)
        group_2 = Group(
            group_id=group_2_id,
            partner_id="INT-CRM",
            object_type="ACCOUNT",
            application_id="SF",
            group_name="Group Name 2",
            owner_uuid=record.uuid,
        )
        group_2.set_session(session=session)
        group_2.get_uuid()
    except Exception as e:
        logging.debug(f"Exception thrown : {e}")
        assert isinstance(e, HopError)


# case 3
# try calling get_uuid twice
@pytest.mark.skip
def test_get_uuid_case3(session):

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

    group_1_id = randomString(10)
    group_1 = Group(
        group_id=group_1_id,
        partner_id="INT-CRM",
        object_type="ACCOUNT",
        application_id="SF",
        group_name="Group Name 3",
        owner_uuid=record.uuid,
    )
    group_1.set_session(session=session)
    group_1.get_uuid()
    group_1.get_uuid()
    assert group_1.uuid != None


# case 4
# try create group object with same details
@pytest.mark.skip
def test_get_uuid_case4(session):

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

    group_1_id = randomString(10)
    group_1 = Group(
        group_id=group_1_id,
        partner_id="INT-CRM",
        object_type="ACCOUNT",
        application_id="SF",
        group_name="Group Name 4",
        owner_uuid=record.uuid,
    )
    group_1.set_session(session=session)
    group_1.get_uuid()

    group_2 = Group(
        group_id=group_1_id,
        partner_id="INT-CRM",
        object_type="ACCOUNT",
        application_id="SF",
        group_name="Group Name 4",
        owner_uuid=record.uuid,
    )
    group_2.set_session(session=session)
    group_2.get_uuid()

    assert group_2.uuid != None


# Testing methods for add records
@pytest.mark.skip
def test_add_records_case1(session):
    try:

        record_id = randomString(10)

        record = Record(
            record_id=record_id,
            partner_id="INT-CRM",
            object_id="SF_ACCOUNT",
        )

        record.set_session(session=session)

        record.get_uuid()

        logger.debug("Record Created")

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

        group_id = randomString(10)
        group = Group(
            group_id=group_id,
            partner_id="INT-CRM",
            object_type="ACCOUNT",
            application_id="SF",
            group_name="Group Name 1",
            owner_uuid=user.uuid,
        )
        group.set_session(session=session)
        group.get_uuid()
        logger.debug(f"Group Created : {group}")
        group.add_record(record=record)

    except Exception as e:
        logger.debug("Exception is thrown in test method")
        logger.debug(e)
