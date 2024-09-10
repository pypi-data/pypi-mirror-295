from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.water_purifier import WaterPurifierDevice


class TestWaterPurifier(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[WaterPurifierDevice]:
        return WaterPurifierDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.WATER_PURIFIER
