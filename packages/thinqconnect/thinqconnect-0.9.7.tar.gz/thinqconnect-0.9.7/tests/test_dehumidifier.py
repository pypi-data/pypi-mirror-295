from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.dehumidifier import DehumidifierDevice


class TestDehumidifier(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[DehumidifierDevice]:
        return DehumidifierDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.DEHUMIDIFIER

    async def check_control(self, device: DehumidifierDevice):
        await device.set_dehumidifier_operation_mode("POWER_ON")
        await device.set_wind_strength("LOW")
        await device.set_dehumidifier_operation_mode("POWER_OFF")
