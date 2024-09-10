from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.washtower import DryerDeviceSingle, WasherDeviceSingle, WashtowerDevice


class TestWashtower(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[WashtowerDevice]:
        return WashtowerDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.WASHTOWER

    async def check_washer_control(self, washer: WasherDeviceSingle):
        await washer.set_washer_operation_mode("POWER_OFF")
        await washer.set_relative_hour_to_stop(4)

    async def check_dryer_control(self, dryer: DryerDeviceSingle):
        await dryer.set_dryer_operation_mode("POWER_OFF")
        await dryer.set_relative_time_to_stop(4)
