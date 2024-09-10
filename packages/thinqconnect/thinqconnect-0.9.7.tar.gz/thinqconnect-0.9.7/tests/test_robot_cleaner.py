from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.robot_cleaner import RobotCleanerDevice


class TestRobotCleaner(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[RobotCleanerDevice]:
        return RobotCleanerDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.ROBOT_CLEANER

    async def check_control(self, device: RobotCleanerDevice):
        await device.set_clean_operation_mode("START")
        await device.set_absolute_time_to_start(1, 10)
