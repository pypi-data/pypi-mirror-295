from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.system_boiler import SystemBoilerDevice


class TestSystemBoiler(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[SystemBoilerDevice]:
        return SystemBoilerDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.SYSTEM_BOILER

    async def check_control(self, device: SystemBoilerDevice):
        await device.set_boiler_operation_mode("POWER_ON")
        await device.set_boiler_operation_mode("POWER_OFF")
        await device.set_current_job_mode("AUTO")
        await device.set_current_job_mode("HEAT")
        await device.set_current_job_mode("COOL")
        await device.set_heat_target_temperature(50)
        await device.set_cool_target_temperature(50)
        await device.set_hot_water_mode("ON")
