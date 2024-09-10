from collections import OrderedDict
import pytest
import conftext


def test_get_conftext_schemas():
    assert conftext.conftext.get_schemas()

def test_read_from_file():
    assert conftext.conftext.read_from_file(False)


class TestGetConfig:
    
    def test_passing_arguments(self):
        test_conf = dict(service='dummy', context='devdb')
        assert conftext.get_config(**test_conf) == test_conf
    
    def test_NoConftext_exception(self):
        print(conftext.get_config())


class TestGetConfigV2:
    
    def test_passing_arguments(self):
        test_conf = dict(service='dummy', context='devdb')
        assert conftext.get_config_v2(**test_conf).defaults() == test_conf
    
    def test_NoConftext_exception(self):
        print(conftext.get_config_v2())
