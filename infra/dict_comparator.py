
import deepdiff

def compare_dicts(tested_dict, reference_dict):
    """
    compare dict values, for verifying exact responses.
    """
    diff = deepdiff.DeepDiff(tested_dict, reference_dict, ignore_order=True)
    return diff

def is_equal_dicts(tested_dict, reference_dict):
    """
    compare dict values, for verifying exact responses.
    """
    diff = deepdiff.DeepDiff(tested_dict, reference_dict, ignore_order=True)
    if diff:
        return False
    return True



def check_dict_keys_missing(tested_dict, reference, dict_name=None):
    """makes sure first level keys are present in tested dict"""
    for key in reference.keys():
        if key not in tested_dict.keys():
            dict_name = dict_name or "tested_dict"
            #logging.error(f"Key {key} is missing from {dict_name}")
            return False
    return True

def check_dict_keys_extra(tested_dict, reference, dict_name=None):
    """makes sure first level keys are present in tested dict"""
    for key in tested_dict.keys():
        if key not in reference.keys():
            dict_name = dict_name or "tested_dict"
            #logging.error(f"Key {key} is extra in {dict_name}")
            return False
    return True
