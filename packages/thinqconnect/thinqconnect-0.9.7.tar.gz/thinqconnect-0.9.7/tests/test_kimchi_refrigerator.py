from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.kimchi_refrigerator import KimchiRefrigeratorDevice


class TestKimchiRefrigerator(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[KimchiRefrigeratorDevice]:
        return KimchiRefrigeratorDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.KIMCHI_REFRIGERATOR
