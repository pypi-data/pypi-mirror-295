import logging

import pytest
from aiohttp import ClientSession

from thinqconnect.thinq_api import ThinQApi

logger = logging.getLogger("test")

TEST_ACCESS_TOKEN = "f9de2cd6043b0ce0e392d1f521a3754897fd919dbbae9c31e560"
TEST_CLIENT_ID = "home-assistant-KR2403128039821"
COUNTRY = "KR"


@pytest.fixture
async def client_session():
    session = ClientSession()
    yield session
    await session.close()


@pytest.fixture
def thinq_api(client_session):
    return ThinQApi(
        session=client_session,
        access_token=TEST_ACCESS_TOKEN,
        country_code=COUNTRY,
        client_id=TEST_CLIENT_ID,
    )


@pytest.mark.asyncio
async def test_device_apis(thinq_api):
    logger.info("ThinQ API Test - Device APIs")
    response = await thinq_api.async_get_device_list()
    device_list = response
    logger.info("device_list : %s", response)

    assert device_list is not None, "No devices found in the response"
    assert len(device_list) > 0, "Device list is empty"

    device_id = device_list[0].get("deviceId")
    assert device_id is not None, "First device does not have a device ID"

    response = await thinq_api.async_get_device_profile(device_id)

    profile = response
    logger.info("profile : %s", profile)
    assert profile is not None, "Profile is empty"
    assert profile.get("property") is not None, "Profile does not have properties"

    response = await thinq_api.async_get_device_status(device_id)
    status = response
    logger.info("status : %s", status)
    assert status is not None, "Status is empty"

    response = await thinq_api.async_get_push_list()
    logger.info("push list : %s", response)

    response = await thinq_api.async_post_push_subscribe(device_id)
    logger.info("push subscribe : %s", response)

    response = await thinq_api.async_delete_push_subscribe(device_id)
    logger.info("push unsubscribe : %s", response)

    response = await thinq_api.async_get_event_list()
    logger.info("event list : %s", response)

    response = await thinq_api.async_post_event_subscribe(device_id)
    logger.info("event subscribe : %s", response)

    response = await thinq_api.async_delete_event_subscribe(device_id)
    logger.info("event unsubscribe : %s", response)

    response = await thinq_api.async_get_push_devices_list()
    logger.info("push devices list : %s", response)

    response = await thinq_api.async_post_push_devices_subscribe()
    logger.info("push devices subscribe : %s", response)

    response = await thinq_api.async_get_push_devices_list()
    logger.info("push devices list : %s", response)

    response = await thinq_api.async_delete_push_devices_subscribe()
    logger.info("push devices unsubscribe : %s", response)
