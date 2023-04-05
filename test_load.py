import pytest
from infra.search_contact_request import SearchContactRequest
from infra.search_company_request import SearchCompanyRequest
import time


@pytest.mark.load
@pytest.mark.parametrize("n", [10, 100, 1000, 10000, 100000])
def test_search_contact_for_basic_load_100_requests(
    n, logger, get_all_contacts_requests_unparametrized
):
    """
    let us see how much performance drop we get as we get 100 reqs

    note : needs to be run on a setup that isn't a potato
    note2 : we can also increace load by providing long incorrect names
            lets do this.
    """
    start_time = time.time()
    single_request = get_all_contacts_requests_unparametrized.pop()
    single_request.execute_request()
    end_time = time.time()
    result_ms = (end_time - start_time) * 1000
    logger.info(f"single request took {result_ms} ms")

    start_time_2 = time.time()
    SearchContactRequest.execute_requests_async(
        get_all_contacts_requests_unparametrized[:n]
    )
    end_time_2 = time.time()
    result2_ms = (end_time_2 - start_time_2) * 1000

    logger.info(f"{n} requests took {result2_ms} ms")
    assert (1.5) * n * result_ms > result2_ms, "we see load problems"


@pytest.mark.load
@pytest.mark.parametrize("n", [10, 100, 1000])
def test_all_companies_at_once_times(n,logger,all_companies):
    names = all_companies.get_items_in_res("name")
    request_list = [SearchCompanyRequest(name=name) for name in names] * n
    start_time = time.time()

    single_request = request_list.pop()
    single_request.execute_request()
    end_time = time.time()
    result_ms = (end_time - start_time) * 1000
    logger.info(f"single request took {result_ms} ms")

    start_time_2 = time.time()
    SearchCompanyRequest.execute_requests_async(request_list)
    end_time_2 = time.time()
    result2_ms = (end_time_2 - start_time_2) * 1000

    m = len(names) * n
    logger.info(f"{m} requests took {result2_ms} ms")
    assert (1.2) * m * result_ms > result2_ms, "we see load problems"
