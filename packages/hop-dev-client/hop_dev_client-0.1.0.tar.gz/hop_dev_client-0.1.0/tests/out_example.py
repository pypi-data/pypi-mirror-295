from hop import Hop
from hop import Record
import logging

LOGGER = logging.getLogger(__name__)

session = Hop.startSession(
    base_url="BASE_URL",
    token_endpoint="TOKEN_ENDPOINT",
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
)

print(session.get_access_token())

"""Create a local Record object"""
record = Record(salesforceId="AAAAA", partnerId="INT-CRM", campaignId="ACCOUNT")

"""when we set the session within the Record Object, It is connected to a particular instance of hop.
        You can then do the hop functions on the object and get it synced with the hop instance.
    """
record.set_session(session=session)

record.get_uuid()

print(record.uuid)
