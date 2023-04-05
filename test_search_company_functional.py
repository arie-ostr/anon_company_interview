import pytest

from infra.search_company_request import SearchCompanyRequest
from infra.dict_comparator import is_equal_dicts
from data.error_responses import NOT_ALLOWED_RESPONSE_BODY as response405
from data.error_responses import NO_COMPANY_FOUND as not_found_response

@pytest.fixture(scope="module")
def valid_request_invalid_method():
    """returns a cache of requests for each method"""
    rd = {}
    for method in ["GET", "PUT", "DELETE", "PATCH"]:
        contact_request = SearchCompanyRequest(name="Millard Public Schools")
        contact_request.modify_method("GET")
        contact_request.execute_request()
        rd[method] = contact_request

    return rd


@pytest.fixture(scope="module")
def valid_request_example():
    """returns a cache of requests for each method"""
    contact_request = SearchCompanyRequest(name="Millard Public Schools")
    contact_request.execute_request()
    return contact_request

@pytest.fixture(scope="module")
def non_existant_request_example():
    """returns a cache of requests for each method"""
    contact_request = SearchCompanyRequest(name="Rasf33df3fj39kdfkj32fdaf")
    contact_request.execute_request()
    return contact_request


@pytest.fixture(scope="module")
def empty_company_request():
    """returns a cache of requests for each method"""
    contact_request = SearchCompanyRequest(name="")
    contact_request.execute_request()
    return contact_request

@pytest.mark.sanity
@pytest.mark.search_company
def test_sanity_sattus_code_200(logger, valid_request_example):
    """
    when valid request
    then its result status code is 200
    """
    response_code = valid_request_example.get_response_code()
    logger.info(f"for company search we got response code {response_code}")
    assert response_code == 200, "status code not 200"

@pytest.mark.sanity
def test_sanity_response_length_1(logger, valid_request_example):
    """
    when valid request that fits 1 company
    then response length is 1
    """
    assert len(valid_request_example.get_response_json()) == 1, (
        "" "we should only get one company"
    )


@pytest.mark.search_company
@pytest.mark.sanity
def test_sanity_for_search_company(logger, valid_request_example):
    """
    given valid request
    when we get good response
    then its format keys are of the right type
    """
    logger.info(f"making sure key types are ok...")
    keys = valid_request_example.get_response_json()[0].keys()
    assert set(keys) == {"company_size","domain","name","revenue_range"}


@pytest.mark.failing
@pytest.mark.search_company
@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE", "PATCH"])
def test_search_company_alt_method_check_statuscode(logger, valid_request_invalid_method, method):
    """
    given user has valid company name
        and user uses GET method to look for it
    when user searches for company
    then response code is 405 "not allowed"
    """
    # checking status code
    status_code = valid_request_invalid_method[method].get_response_code()
    logger.info(f"we got searched company and got response code : {status_code}")
    if status_code != 405:
        pytest.fail("wrong status code, should be 405")


@pytest.mark.search_company
@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE", "PATCH"])
def test_search_company_alt_method_check_response(logger, valid_request_invalid_method, method):
    """
    given user has valid company name
        and user uses GET method to look for it
    when user searches for company
    then response body contains error
    """
    # get response
    response_json = valid_request_invalid_method[method].get_response_json()
    logger.info(f"we got response body : {response_json}")

    # make sure its an error response
    same_response = is_equal_dicts(response_json, response405)
    if not same_response:
        pytest.fail("response body does not match")


@pytest.mark.search_company
def test_search_for_nothing_code_200(logger,empty_company_request):
    """
    when search for nothing
    then result has 200 status code
    """
    assert empty_company_request.response_code() == 200, "status code not 200"

@pytest.mark.search_company
def test_search_for_nothing_code_200(logger,empty_company_request):
    """
    when search for nothing
    then result has 200 status code
    """
    logger.info(f"request latency: {empty_company_request.request_latency}")
    assert empty_company_request.request_latency < 2000, "status code not 200"


@pytest.mark.search_company
def test_search_for_nothing(logger,empty_company_request):
    """
    when search for nothing
    then we get 100 companies
    """
    companies_results = len(empty_company_request.get_response_json())
    logger.info(f"response length is {companies_results}")
    assert companies_results == 100, (""
        "100 companies should be returned "
        "for empty search in staging env")


@pytest.mark.search_company
def test_search_for_nonexistent_company_status_code(logger,non_existant_request_example):
    """
    when search for nothing
    then result has 200 status code
    """
    status_code = non_existant_request_example.get_response_code()
    logger.info(f"status code is {status_code}")
    assert status_code == 404, "status code not 200"


@pytest.mark.search_company
def test_search_for_nonexistent_company_response_body(logger,non_existant_request_example):
    """
    when search for nothing
    then result has 200 status code
    """
    response_json = non_existant_request_example.get_response_json()
    logger.info(f"response body is {response_json}")
    assert response_json == not_found_response, "response body not correct"
