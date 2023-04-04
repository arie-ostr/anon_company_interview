import pytest
from infra import utils
from infra.response_validator import ResponseValidator

dict_flat = {
    "dict": {},
    "list": [],
    "str": "str",
    "int": 1,
    "float": 1.1,
    "bool": True,
    "none": None,
}



def test_dict_comparator_types():
    """
    given a dict of None, float, int, str, bool, list, dict keys
    when we validate it 
    then we get a res dict without errors
    """
    mask = ResponseValidator.create_mask(dict_flat)
    assert False, "Not implemented yet"