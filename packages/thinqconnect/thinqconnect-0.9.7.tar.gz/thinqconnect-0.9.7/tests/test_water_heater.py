from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.water_heater import WaterHeaterDevice


class TestWaterHeater(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[WaterHeaterDevice]:
        return WaterHeaterDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.WATER_HEATER

    async def check_control(self, device: WaterHeaterDevice):
        await device.set_current_job_mode("AUTO")
        await device.set_current_job_mode("HEAT_PUMP")
        await device.set_current_job_mode("VACATION")
        await device.set_current_job_mode("TURBO")
        await device.set_target_temperature(50)
