import logging
import pytest

from data.get_crossed_names import crossed_names_sample, crossed_names
from infra.search_company_request import SearchCompanyRequest
from infra.search_contact_request import SearchContactRequest



@pytest.fixture(scope="session")
def all_companies():
    """returns a cache of requests for each method"""
    contact_request = SearchCompanyRequest(name="")
    contact_request.execute_request()
    return contact_request


@pytest.fixture(scope="session", params=crossed_names_sample)
def get_some_contacts_requests(request, all_companies):
    """makes a list of all requests for companies and contacts
    uses all companies, uses all contacts
    """
    company_names = all_companies.get_items_in_res("name")
    request_list = []
    full_name = request.param
    for company_name in company_names:
        for b in [True, False]:
            contact_request = SearchContactRequest(
                full_name=full_name, company=company_name, is_current_company=b
            )
            request_list.append(contact_request)
            
    return request_list #returns 100*2 companies per contact param


@pytest.fixture(scope="session", params=crossed_names)
def get_all_contacts_requests(request, all_companies):
    """makes a list of all requests for companies and contacts
    uses all companies, uses all contacts
    """
    company_names = all_companies.get_items_in_res("name")
    request_list = []
    full_name = request.param
    for company_name in company_names:
        for b in [True, False]:
            contact_request = SearchContactRequest(
                full_name=full_name, company=company_name, is_current_company=b
            )
            request_list.append(contact_request)
            
    return request_list #returns 100*2 companies per contact param'
        

@pytest.fixture(scope="session")
def get_all_contacts_requests_unparametrized(all_companies):
    """
    returns a giant list of crossed names and companies, not parametrized!
    this way we can run a single test with tons of requests
    used in load testing
    """
    company_names = all_companies.get_items_in_res("name")
    request_list = []
    for full_name in crossed_names:
        for company_name in company_names:
            for b in [True, False]:
                contact_request = SearchContactRequest(
                    full_name=full_name, company=company_name, is_current_company=b
                )
                request_list.append(contact_request)
                
    return request_list #returns 100*2 companies per contact param'




@pytest.fixture(scope="session")
@pytest.mark.cache # improve performance
def contacts_across_companies(get_some_contacts_requests):
    """executes all requests in asyncmode 
    otherwise it would be impossible to run reasonably"""
    rl = SearchContactRequest.execute_requests_async(get_some_contacts_requests)
    return rl

@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    # I use one log file for simplicity
    log_file = 'logs/test.log'

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger('test')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    yield

    logger.removeHandler(handler)
    handler.close()


@pytest.fixture(scope='function', autouse=True)
def log_test_start_end(request, setup_logging):
    """Log each test start and test end with its name."""
    test_name = request.node.name
    logger = logging.getLogger('test')
    logger.info(f'Test "{test_name}" starts.')
    yield
    logger.info(f'Test "{test_name}" ends.')


@pytest.fixture(scope='function')
def logger():
    """Return the logger with the name 'test'."""
    logger = logging.getLogger('test')
    return logger
