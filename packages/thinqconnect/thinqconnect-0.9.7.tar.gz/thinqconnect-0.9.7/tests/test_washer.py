from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.washer import WasherDevice, WasherSubDevice


class TestWasher(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[WasherDevice]:
        return WasherDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.WASHER

    async def check_sub_device_control(self, sub_device: WasherSubDevice):
        await sub_device.set_relative_hour_to_stop(4)
        await sub_device.set_washer_operation_mode("POWER_OFF")
