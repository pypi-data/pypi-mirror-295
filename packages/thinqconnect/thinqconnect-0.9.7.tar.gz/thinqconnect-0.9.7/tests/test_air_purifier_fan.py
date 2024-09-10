from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.air_purifier_fan import AirPurifierFanDevice


class TestAirPurifierFan(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[AirPurifierFanDevice]:
        return AirPurifierFanDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.AIR_PURIFIER_FAN

    async def check_control(self, device: AirPurifierFanDevice):
        # NOTE: 밀웜 동작 확인 불가
        # await device.set_current_job_mode("DIRECT_CLEAN")
        # await device.set_relative_time_to_stop(5)
        # await device.set_wind_angle("ANGLE_45")
        # await device.set_warm_mode("WARM_ON")
        # await device.set_wind_temperature(35)

        # NOTE: 밀웜 테스트 완료
        await device.set_air_fan_operation_mode("POWER_ON")
        await device.set_absolute_time_to_stop(13, 30)
        await device.set_display_light("LEVEL_2")
        await device.set_wind_strength("AUTO")
        await device.set_uv_nano("ON")
        await device.set_air_fan_operation_mode("POWER_OFF")
        await device.set_absolute_time_to_start(12, 30)
