import requests
import logging
import pytest

example_response = [
    {
        "company_size": {"max": 5000, "min": 1001},
        "domain": "www.mpsomaha.org",
        "name": "Millard Public Schools",
        "revenue_range": {"max": 500000000, "min": 250000000},
    }
]

example_company_response = {
    "company": {
        "company_size": {
            "max": 5000,
            "min": 1001
        },
        "domain": "www.mpsomaha.org",
        "name": "Millard Public Schools",
        "revenue_range": {
            "max": 500000000,
            "min": 250000000
        }
    },
    "full_name": "Emma Smith",
    "phone": 75825066414,
    "private_email": "emma.s@mailbox.org",
    "work_email": "emma.smith@mpsomaha.org"
}

payload_company_example = {
        "company_name": "Millard Public Schools",
    }

payload_contact_example = {
        "full_name": "emma smith",
        "company_name": "Millard Public Schools",
        "is_current_company": True,
    }

headers_example = {
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.31.3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }

@pytest.mark.draft
def test_make_basic_request():
    """
        my drafts , I'm adding them to repo in order to show my work
        however in a normal situation I would not commit them
    """
    logging.info("test started")
    url = "https://lusha-ha-automation-api.dev.lusha.co/search_company"
    res = requests.post(url, headers=headers_example, json=payload_company_example)
    assert res.status_code == 200 , "status code not 200"
    print(res.json())
    #assert res.json() == example_response , "response content differs"
    logging.info("test passed")
