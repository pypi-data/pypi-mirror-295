"""Module to test the field converter class from the record convertor module"""

from copy import deepcopy
from data.data_field_convertor_tests import (
    PARAMS_TO_LOWER_STR,
)
from record_convertor.field_convertors import BaseFieldConvertor

convertor = BaseFieldConvertor()


def test_to_lower_str_with_target_field():
    """
    test to_lower_str method turns str into lowercase with target field
    """
    test_set = deepcopy(PARAMS_TO_LOWER_STR)
    test_set["conversion_rule"] = {
        "fieldname": "to_lower",
        "actions": [{"to_lower_str": None, "target_field_name": "to_lower_target"}],
    }
    converted_record = convertor.convert_field(**test_set)
    assert converted_record["to_lower"] == "LOWERCASE"
    assert converted_record["to_lower_target"] == "lowercase"


def test_to_update_target_field_option():
    """
    test add_data_from_dict updates a target_field specified in the fieldname field.
    """

    test_set = {
        "record": {
            "dict1": {"key1": "a"},
            "dict2": {"key2": "a"},
        },
        "conversion_rule": {
            "fieldname": "target_field",
            "actions": [
                {"add_data_from_dict": "dict1"},
                {"add_data_from_dict": "dict2"},
            ],
        },
    }
    converted_record = convertor.convert_field(**test_set)
    assert converted_record["target_field"] == {"key1": "a", "key2": "a"}


def test_to_update_nested_target_field_option_true():
    """
    test add_data_from_dict updates a nested target_field specified in the fieldname
    field.
    """

    test_set = {
        "record": {
            "dict1": {"key1": "a"},
            "dict2": {"key2": "a"},
        },
        "conversion_rule": {
            "fieldname": "target_field.nested_field",
            "actions": [
                {"add_data_from_dict": "dict1"},
                {"add_data_from_dict": "dict2"},
            ],
        },
    }
    converted_record = convertor.convert_field(**test_set)
    assert converted_record["target_field"]["nested_field"] == {
        "key1": "a",
        "key2": "a",
    }
