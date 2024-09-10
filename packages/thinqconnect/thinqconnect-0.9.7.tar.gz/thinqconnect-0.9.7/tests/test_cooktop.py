from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.cooktop import CooktopDevice


class TestCooktop(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[CooktopDevice]:
        return CooktopDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.COOKTOP

    async def check_control(self, device: CooktopDevice):
        await device.set_operation_mode("POWER_OFF")
        await device.set_power_level("left_rear", 1)
        # await device.set_power_level("left_rear", 15)  # negative
        await device.set_remain_hour("right_front", 1)
        await device.set_remain_minute("left_rear", 5)
