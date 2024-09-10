from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.dish_washer import DishWasherDevice


class TestDishWasher(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[DishWasherDevice]:
        return DishWasherDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.DISH_WASHER

    async def check_control(self, device: DishWasherDevice):
        await device.set_dish_washer_operation_mode("START")
        await device.set_relative_hour_to_start(1)
