from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.styler import StylerDevice


class TestStyler(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[StylerDevice]:
        return StylerDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.STYLER

    async def check_control(self, device: StylerDevice):
        await device.set_styler_operation_mode("START")
        await device.set_relative_hour_to_stop(3)
