from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.microwave_oven import MicrowaveOvenDevice


class TestMicrowaveOven(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[MicrowaveOvenDevice]:
        return MicrowaveOvenDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.MICROWAVE_OVEN

    async def check_control(self, device: MicrowaveOvenDevice):
        await device.set_fan_speed(2)
        await device.set_lamp_brightness(1)
