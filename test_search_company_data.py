import pytest

from collections import Counter

from infra.search_company_request import SearchCompanyRequest
from data.error_responses import NOT_ALLOWED_RESPONSE_BODY as response405
from infra.data_validator import is_valid_domain


@pytest.fixture(scope="module")
def all_companies_request():
    """returns a cache of requests for each method"""
    contact_request = SearchCompanyRequest(name="")
    contact_request.execute_request()
    return contact_request


@pytest.mark.search_company
def test_no_duplicate_compant_names(logger, all_companies_request):
    """
    when user makes empty search
        and it yields all companies
    then no duplicate company names are returned


    Note: we might get individual exceptions: we can add those to blacklist
        we prefer to have exceptions than false positive results
    """
    total_names = all_companies_request.get_items_in_res("name")
    # lets strip whitespaces
    total_names = [name.strip() for name in total_names]
    # lets remove spaces inside such that Micro Soft becomes Microsoft
    total_names = [name.replace(" ", "") for name in total_names]
    # lets lowercase it all
    total_names = [name.lower() for name in total_names]

    # we can also use pandas groupby , might add it as the need arises.
    counter = Counter(total_names)
    for item in counter:
        if counter[item] > 1:
            logger.error(f"company name: {item} appears {counter[item]} times")
            assert False


@pytest.mark.search_company
def test_all_domains_valid(logger, all_companies_request):
    """
    when user makes empty search
        and it yields all companies
    then all domains are valid

    Note: we might get individual exceptions: we can add those to blacklist
        we prefer to have exceptions than false positive results
    """
    total_domains = all_companies_request.get_items_in_res("domain")
    logger.info(f"total domains: {total_domains}")
    for domain in total_domains:
        valid_domain = is_valid_domain(domain)
        error = f"domain: {domain} is not valid"
        assert valid_domain, error


@pytest.mark.search_company
def test_no_duplicate_domains(logger, all_companies_request):
    """
    when user makes search for all domains
    then no duplicate domains are returned for any company
    """
    total_domains = all_companies_request.get_items_in_res("domain")
    for item in total_domains:
        if total_domains.count(item) > 1:
            logger.error(f"domain: {item} appears {total_domains.count(item)} times")
            assert False


@pytest.mark.search_company
def test_revenue_ranges(logger, all_companies_request):
    """
    when user makes search for all domains
    then no duplicate domains are returned for any company
    """
    ranges = all_companies_request.get_items_in_res(
        ["revenue_range.min", "revenue_range.max"]
    )
    for r in ranges:
        assert r[0] <= r[1], f"min: {r[0]} is greater than max: {r[1]}"