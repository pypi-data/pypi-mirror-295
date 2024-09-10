from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.humidifier import HumidifierDevice


class TestHumidifier(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[HumidifierDevice]:
        return HumidifierDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.HUMIDIFIER

    async def check_control(self, device: HumidifierDevice):
        # NOTE: 실기기 테스트 필요
        await device.set_current_job_mode("AIR_CLEAN")
        await device.set_humidifier_operation_mode("POWER_OFF")
        await device.set_humidifier_operation_mode("POWER_ON")
        await device.set_sleep_mode("SLEEP_OFF")
        await device.set_sleep_mode("SLEEP_ON")
