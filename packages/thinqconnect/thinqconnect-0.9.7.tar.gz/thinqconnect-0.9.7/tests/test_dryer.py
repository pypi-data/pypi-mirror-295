from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.dryer import DryerDevice


class TestDryer(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[DryerDevice]:
        return DryerDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.DRYER

    async def check_control(self, device: DryerDevice):
        await device.set_dryer_operation_mode("POWER_OFF")
