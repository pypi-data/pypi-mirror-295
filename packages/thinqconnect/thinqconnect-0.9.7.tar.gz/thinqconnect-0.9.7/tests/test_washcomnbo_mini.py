from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.washcombo_mini import WashcomboMiniDevice


class TestWashcomboMini(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[WashcomboMiniDevice]:
        return WashcomboMiniDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.WASHCOMBO_MINI

    async def check_control(self, device: WashcomboMiniDevice):
        await device.set_washer_operation_mode(operation="POWER_OFF")
        await device.set_relative_hour_to_stop(4)
