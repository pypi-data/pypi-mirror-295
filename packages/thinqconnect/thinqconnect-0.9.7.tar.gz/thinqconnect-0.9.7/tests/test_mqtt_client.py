import json
import logging
from time import sleep

import pytest
from aiohttp import ClientSession
from awscrt import exceptions, mqtt

from thinqconnect.mqtt_client import ThinQMQTTClient
from thinqconnect.thinq_api import ThinQApi

logger = logging.getLogger("test")
TEST_ACCESS_TOKEN = "ab3f3fa8443d91d48a2e331c6489ae0c1133acd441e539035ac1"
# TEST_ACCESS_TOKEN = "a1ff38f79ddb7170876e75144e02dd42c3488af4f47cea7ba1a4"
TEST_CLIENT_ID = "home-assistant-KR2403128039821559999"
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


def on_connection_interrupted(
    connection: mqtt.Connection,
    error: exceptions.AwsCrtError,
    **kwargs: dict,
) -> None:
    """The MQTT connection is lost."""
    logger.error("Connection interrupted. error:=%s", error)


def on_message_received(topic: str, payload: bytes, **kwargs: dict) -> None:
    """A message matching the topic is received."""
    try:
        received = json.loads(payload.decode())
    except ValueError:
        logger.error("Error parsing JSON payload: %s", payload.decode())
        return None
    logger.info(
        "_on_message_received. topic:%s, received:%s",
        topic,
        received,
    )


def on_connection_success(
    connection: mqtt.Connection,
    callback_data: mqtt.OnConnectionSuccessData,
) -> None:
    """The MQTT connection is established."""
    logger.info("Connection success.")


@pytest.fixture
async def mqtt_client(client_session):
    thinq_api = await ThinQApi(
        session=client_session,
        access_token=TEST_ACCESS_TOKEN,
        country_code=COUNTRY,
        client_id=TEST_CLIENT_ID,
    )
    logger.info("ThinQ API Test - MQTT Server : %s", thinq_api)

    return await ThinQMQTTClient(
        thinq_api=thinq_api,
        on_message_received=on_message_received,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_success=on_connection_success,
        client_id=TEST_CLIENT_ID,
    )


# @pytest.mark.asyncio
# async def test_push_subscribe(thinq_api):
#     logger.info("ThinQ API Test - Push Subscribe API")

#     device_list = await thinq_api.async_get_device_list()
#     logger.info("device_list : %s", device_list)
#     device_list = device_list.get("response")

#     for device in device_list:
#         device_id = device.get("deviceId")
#         try:
#             result = await thinq_api.async_post_push_subscribe(device_id=device_id)
#             logger.info("Push Subscribe Result : %s", result)
#         except ThinQApiError as e:
#             if e.message.get("error").get("code") == "1207":
#                 logger.info("Already Subscribed Push. So skip... : %s", device_id)
#             else:
#                 raise e

#     event_payload = {"expire": {"unit": "HOUR", "timer": 24}}
#     for device in device_list:
#         if not device.get("reportalble", False):
#             continue
#         device_id = device.get("deviceId")
#         try:
#             result = await thinq_api.async_post_event_subscribe(device_id=device_id, payload=event_payload)
#             logger.info("Event Subscribe Result : %s", result)
#         except ThinQApiError as e:
#             if e.message.get("error").get("code") == "1207":
#                 logger.info("Already Subscribed Event. So skip... : %s", device_id)
#             else:
#                 raise e


@pytest.mark.asyncio
async def test_mqtt_client(mqtt_client):
    logger.info("ThinQ API Test - MQTT Client : %s", mqtt_client)

    await mqtt_client.async_prepare_mqtt()
    sleep(2)

    # Connect to MQTT Broker
    try:
        await mqtt_client.async_connect_mqtt()
    except Exception as e:
        # Try again if fails (OSx keychain issue)
        logger.info("MQTT Connection Error. Try again.. : %s", e)
        await mqtt_client.async_connect_mqtt()
        # Keep the connection alive
        while True:
            await sleep(3600)  # sleep for 1 hour
