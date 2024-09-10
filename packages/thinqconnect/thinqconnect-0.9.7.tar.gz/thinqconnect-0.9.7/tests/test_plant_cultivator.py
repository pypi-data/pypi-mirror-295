from __future__ import annotations

from tests.device_test_base import DeviceTestBase
from thinqconnect.const import DeviceType
from thinqconnect.devices.plant_cultivator import PlantCultivatorDevice


class TestPlantCultivator(DeviceTestBase):
    @classmethod
    def get_device_class(cls) -> type[PlantCultivatorDevice]:
        return PlantCultivatorDevice

    @classmethod
    def get_device_type(cls) -> str:
        return DeviceType.PLANT_CULTIVATOR
