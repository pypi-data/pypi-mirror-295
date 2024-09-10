from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.air_purifier import AirPurifierDevice


class TestAirPurifier(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[AirPurifierDevice]:
        return AirPurifierDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.AIR_PURIFIER

    async def check_control(self, device: AirPurifierDevice):
        # NOTE: AIR_910604_WW 제어 테스트이고, 시뮬레이터 기기로 테스트 시 전원 켠 후 Mode를 Single로 변경하고 Speed를 Turbo로 변경 필요
        await device.set_wind_strength("LOW")
        await device.set_absolute_time_to_stop(13, 30)
        await device.set_air_purifier_operation_mode("POWER_OFF")
        await device.set_absolute_time_to_start(12, 30)
        await device.set_air_purifier_operation_mode("POWER_ON")
