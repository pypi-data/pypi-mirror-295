from hop import Hop
from hop import Record
import pytest

import logging

# logging.basicConfig(
#     level=logging.INFO, filename="hop_log.log", encoding="utf-8", filemode="w"
# )

LOGGER = logging.getLogger(__name__)


@pytest.mark.skip
def test_get_session():

    session = Hop.startSession(
        base_url="https://2h40kyqc06.execute-api.us-east-1.amazonaws.com/prod",
        token_endpoint="https://hopjoinsdev.auth.us-east-1.amazoncognito.com/oauth2/token",
        client_id="2kqhbbf0kv7e5bieidsfp0tn98",
        client_secret="1p263ln7budi4tdgmhngi067plu1m1eusksr06k7kdlgdrlecf3g",
    )

    # print(session.get_access_token())

    LOGGER.debug(session.get_access_token())

    assert session.get_access_token() != None


@pytest.mark.skip
def test_post_record():

    session = Hop.startSession(
        base_url="https://2h40kyqc06.execute-api.us-east-1.amazonaws.com/prod",
        token_endpoint="https://hopjoinsdev.auth.us-east-1.amazoncognito.com/oauth2/token",
        client_id="2kqhbbf0kv7e5bieidsfp0tn98",
        client_secret="1p263ln7budi4tdgmhngi067plu1m1eusksr06k7kdlgdrlecf3g",
    )

    """Create a local Record object"""
    record = Record(salesforceId="AAAAA", partnerId="INT-CRM", campaignId="ACCOUNT")

    """when we set the session within the Record Object, It is connected to a particular instance of hop.
        You can then do the hop functions on the object and get it synced with the hop instance.
    """
    record.set_session(session=session)

    """We update the backend with changes made in the local object."""
    record.update()
