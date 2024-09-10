from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.stick_cleaner import StickCleanerDevice


class TestStickCleaner(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[StickCleanerDevice]:
        return StickCleanerDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.STICK_CLEANER
