import pytest
from pymycobot import Mercury

m = Mercury("/dev/ttyAMA1")


class TestMercury:
    def test_power_on(self):
        