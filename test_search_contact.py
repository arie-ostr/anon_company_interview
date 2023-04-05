import time
import pytest

from infra.search_contact_request import SearchContactRequest
from infra.dict_comparator import compare_dicts



@pytest.fixture(scope="module")
def valid_contact():
    """returns a valid contact request"""
    contact_request = SearchContactRequest(
        full_name="Emma Smith",
        company="Millard Public Schools",
        is_current_company=True,
    )
    contact_request.execute_request()
    return contact_request


@pytest.mark.sanity
@pytest.mark.search_contact
def test_sanity_for_search_contact_response_code(logger, valid_contact):
    """
    sanity: make sure we have 200 respons ecode
    """
    response_code = valid_contact.get_response_code()
    logger.info(f"response status: {response_code}")
    assert response_code == 200, "response status is not 200"


@pytest.mark.sanity
@pytest.mark.search_contact
def test_sanity_for_search_contact_response_json(logger, valid_contact):
    """
    sanity - make sure we have proper json
    """
    res_json = valid_contact.get_response_json()
    logger.info(f"response body: {res_json.keys()}")
    assert set(res_json.keys()) == {'company', 'full_name', 'phone', 'private_email', 'work_email'}
    
@pytest.mark.search_contact
def test_search_contact_for_data_stability(logger):
    """
    given parameters that locate a valid contact
    when we search for this contact
    then we get the same details in sequential searches

    note: we use staging data that dodesn't change
    """
    results = []
    for i in range(5):
        contact_request = SearchContactRequest(
            full_name="Emma Smith",
            company="Millard Public Schools",
            is_current_company=True,
        )
        contact_request.execute_request()
        res1 = contact_request.get_response_json()
        time.sleep(1)
        if results == []:
            results.append(res1)
        else:
            diff = compare_dicts(results[0], res1)
            if diff:
                logger.info(f"found mutated values: {str(diff)}")
                assert False, f"contact details do not match"


