from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.home_brew import HomeBrewDevice


class TestHomeBrew(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[HomeBrewDevice]:
        return HomeBrewDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.HOME_BREW
