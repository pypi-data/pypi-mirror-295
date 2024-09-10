from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.refrigerator import RefrigeratorDevice, RefrigeratorSubDevice


class TestRefrigerator(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[RefrigeratorDevice]:
        return RefrigeratorDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.REFRIGERATOR

    async def check_control(self, device: RefrigeratorDevice):
        await device.set_express_mode(True)
        await device.set_rapid_freeze(True)
        await device.set_fresh_air_filter("AUTO")

    async def check_sub_device_control(self, sub_device: RefrigeratorSubDevice):
        await sub_device.set_target_temperature(7)
        await sub_device.set_target_temperature(10)
        await sub_device.set_target_temperature(-7)
