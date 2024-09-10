from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.washcombo_main import WashcomboMainDevice


class TestWashcomboMain(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[WashcomboMainDevice]:
        return WashcomboMainDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.WASHCOMBO_MAIN

    async def check_control(self, device: WashcomboMainDevice):
        await device.set_washer_operation_mode(operation="POWER_OFF")
        await device.set_relative_hour_to_stop(4)
