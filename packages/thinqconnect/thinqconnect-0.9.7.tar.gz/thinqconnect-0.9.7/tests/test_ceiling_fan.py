from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.ceiling_fan import CeilingFanDevice


class TestCeilingFan(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[CeilingFanDevice]:
        return CeilingFanDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.CEILING_FAN

    async def check_control(self, device: CeilingFanDevice):
        await device.set_ceiling_fan_operation_mode("POWER_ON")
        await device.set_ceiling_fan_operation_mode("POWER_OFF")
        await device.set_wind_strength("TURBO")
        await device.set_wind_strength("HIGH")
        await device.set_wind_strength("LOW")
        await device.set_wind_strength("MID")
