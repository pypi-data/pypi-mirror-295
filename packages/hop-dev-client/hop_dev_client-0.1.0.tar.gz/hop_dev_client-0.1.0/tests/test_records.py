import logging
from hop import Hop
from hop import Record
import pytest
from uuid import uuid4
from hop import HopError

logger = logging.getLogger(__name__)


@pytest.fixture
def session():
    return Hop.startSession(
        base_url="https://d7byn99lnj.execute-api.us-east-1.amazonaws.com/prod",
        token_endpoint="https://hopjoinsdev.auth.us-east-1.amazoncognito.com/oauth2/token",
        client_id="4qvb32q7f6e69fph4qeq7pcef3",
        client_secret="1tqfg52dcdbge11ltq0issc9cpqdb0bhocsboo9fp3t8nmomp3ci",
    )


# case 1 : no UUID, send a record details. Get UUID generated
@pytest.mark.skip
def test_get_uuid_case_1(session):
    logger.debug("Testing test_get_uuid")
    """Create a local Record object"""
    record = Record(
        record_id=str("AAAAA"), partner_id=str("INT-CRM"), object_id=str("ACCOUNT")
    )
    record.set_session(session=session)
    logger.debug(record)

    record.get_uuid()

    assert record.uuid != None


# case 2: UUID and record details sent. UUID Matches the record details and the uuid is returned.
@pytest.mark.skip
def test_get_uuid_case_2(session):
    logger.debug("CASE 2: test_get_uuid")
    """Create a local Record object"""

    try:
        record = Record(
            record_id=str("AAAA1"),
            partner_id=str("INT-CRM"),
            object_id=str("ACCOUNT"),
        )

        record.set_session(session=session)
        record.get_uuid()
        # when you call get_uuid for second time it resends the UUID that was generated.
        record.get_uuid()
        logging.debug(record.uuid)
        assert record.uuid != None
    except Exception as e:
        logging.debug(e)
        assert False


# case 3: UUID and record details sent. Force flag set to false. UUID mismatch occurs. Return error message.
@pytest.mark.skip
def test_get_uuid_case_3(session):
    logger.debug("Testing test_get_uuid")
    """Create a local Record object"""
    try:
        record = Record(
            record_id=str("AAAA2"), partner_id=str("INT-CRM"), object_id=str("ACCOUNT")
        )
        record.set_session(session=session)

        record.get_uuid()
        record.record_id = "FFFF"
        # when you call get_uuid for second time it resends the UUID that was generated.
        # Record Id doesnt match the UUID.
        record.get_uuid()
        raise AssertionError(
            "This should not execute. Expecting a HopError thrown from previous step."
        )
    except Exception as e:
        logging.debug("Exception caught")
        logging.debug(e)
        assert isinstance(e, HopError)

    assert record.uuid != None


# case 4: UUID and record details sent. Force flag set to True. UUID mismatch occurs.
#           Force the record to the UUID from client side.
@pytest.mark.skip
def test_get_uuid_case_4(session):
    logger.debug("Testing test_get_uuid")
    """Create a local Record object"""
    try:
        record = Record(
            record_id=str("AAAA2"), partner_id=str("INT-CRM"), object_id=str("ACCOUNT")
        )
        record.set_session(session=session)

        record.get_uuid()
        record.record_id = "FFFF"
        # when you call get_uuid for second time it resends the UUID that was generated.
        # Record Id doesnt match the UUID
        record.get_uuid(force=True)
        assert record.uuid != None

    except Exception as e:
        logging.debug("Exception caught")
        logging.debug(e)
        assert not isinstance(e, HopError)

    assert record.uuid != None


# Case 1 : Send a valid uuid
@pytest.mark.skip
def test_delete_case1(session):
    logger.debug("Testing delete Case 1")
    record = Record(
        record_id=str("AAAA56"), partner_id=str("INT-CRM"), object_id=str("ACCOUNT")
    )
    record.set_session(session=session)

    record.get_uuid()
    logger.debug(f"UUID : {record.uuid}")

    assert record.delete() == True


# Case 2 : Send a invalid uuid. Exception is thrown.
@pytest.mark.skip
def test_delete_case2(session):
    logger.debug("Testing delete Case 1")
    try:
        record = Record(
            record_id=str("AAAA56"), partner_id=str("INT-CRM"), object_id=str("ACCOUNT")
        )
        record.set_session(session=session)
        record.get_uuid()
        record.uuid = uuid4()
        record.delete()

        logger.debug(f"UUID : {record.uuid}")
    except Exception as e:
        logger.debug(f"Exception thrown : {e}")
        assert isinstance(e, HopError)


# Case 1 : update record id
@pytest.mark.skip
def test_update_case1(session):
    logger.debug("Testing update Case 1")
    record = Record(
        record_id=str("DDDDD"), partner_id=str("INT-CRM"), object_id=str("ACCOUNT")
    )
    record.set_session(session=session)
    record.get_uuid()
    record.record_id = "JJJJJJ"
    assert record.update() == True


# Case 1 : update record id. Send invalid uuid
@pytest.mark.skip
def test_update_case1(session):
    logger.debug("Testing update Case 1")
    try:
        record = Record(
            record_id=str("DDDDD"), partner_id=str("INT-CRM"), object_id=str("ACCOUNT")
        )
        record.set_session(session=session)
        record.get_uuid()
        record.uuid = uuid4()
        record.record_id = "JJJJJJ"
        record.update()
    except Exception as e:
        logger.debug(f"Exception thrown : {e}")
        assert isinstance(e, HopError)
