from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.wine_cellar import WineCellarDevice, WineCellarSubDevice


class TestWineCellar(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[WineCellarDevice]:
        return WineCellarDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.WINE_CELLAR

    async def check_control(self, device: WineCellarDevice):
        await device.set_optimal_humidity("OFF")
        await device.set_light_brightness("100%")

    async def check_sub_device_control(self, sub_device: WineCellarSubDevice):
        await sub_device.set_target_temperature(14)
        await sub_device.set_target_temperature(5)
        await sub_device.set_target_temperature(0)
