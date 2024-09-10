from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.oven import OvenDevice, OvenSubDevice


class TestOven(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[OvenDevice]:
        return OvenDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.OVEN

    async def check_sub_device_control(self, sub_device: OvenSubDevice):
        await sub_device.set_oven_operation_mode("START")
        await sub_device.set_cook_mode("CONVECTION_BAKE")
        await sub_device.set_target_temperature_f(368)
        await sub_device.set_target_temperature_c(150)
