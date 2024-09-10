from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.washtower_dryer import WashtowerDryerDevice


class TestWashtowerDryer(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[WashtowerDryerDevice]:
        return WashtowerDryerDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.WASHTOWER_DRYER
