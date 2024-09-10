from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.air_conditioner import AirConditionerDevice


class TestAirConditioner(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[AirConditionerDevice]:
        return AirConditionerDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.AIR_CONDITIONER

    async def check_control(self, device: AirConditionerDevice):
        await device.set_current_job_mode("COOL")
        await device.set_air_con_operation_mode("POWER_ON")
        await device.set_air_con_operation_mode("POWER_OFF")
        await device.set_current_job_mode("AIR_DRY")
        await device.set_air_clean_operation_mode("START")
        await device.set_monitoring_enabled("ON_WORKING")
        await device.set_wind_strength("MID")
        await device.set_relative_time_to_stop(1, 10)
        await device.set_sleep_timer_relative_time_to_stop(1, 10)
        await device.set_target_temperature(20)
        await device.set_cool_target_temperature(24)
        await device.set_power_save_enabled(False)
