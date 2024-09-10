from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.hood import HoodDevice


class TestHood(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[HoodDevice]:
        return HoodDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.HOOD

    async def check_control(self, device: HoodDevice):
        await device.set_fan_speed(2)
        await device.set_lamp_brightness(1)
