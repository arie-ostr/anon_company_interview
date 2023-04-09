import pandas as pd
from infra.lusha_request import LushaRequest
from infra.dict_comparator import is_equal_dicts

_example_valid_response_one_company = [
    {
        "company_size": {"max": 500, "min": 251},
        "domain": "www.lupprians.com",
        "name": "Rhenus Lupprians",
        "revenue_range": {"max": 50000000, "min": 10000000},
    }
]


class SearchCompanyRequest(LushaRequest):
    def __init__(self, name=None) -> None:
        super().__init__(
            endpoint="search_company",
            method="POST",
            payload={"company_name": name},
        )
        self.company_name = name
        self.example_valid_response_one_company = _example_valid_response_one_company

    def no_companies_found_response(self):
        return {"error_description": "no companies where found"}

    def validate_not_found_response(self):
        assert self.response.status_code == 404, "status code not 404"
        assert (
            self.response.json() == self.no_companies_found_response()
        ), "response is not no companies found response"

    def get_company_size(self):
        if len(self.response.json()) == 1:
            if "company_size" in self.response.json()[0]:
                return self.response.json()[0]["company_size"]
            else:
                assert False, "company_size not in response"
        elif len(self.response.json() > 1):
            assert False, "more than one company returned"

    def get_revenue_range(self):
        if len(self.response.json()) == 1:
            if "revenue_range" in self.response.json()[0]:
                return self.response.json()[0]["revenue_range"]
            else:
                assert False, "revenue_range not in response"
        elif len(self.response.json() > 1):
            assert False, "more than one company returned"

    def validate_company_size(self):
        """
        makes sure company size section per response is valid
        """
        res = self.get_company_size()
        assert isinstance(res, dict), "company size is not a dict"
        assert isinstance(res["min"], int), "company size min is not an int"
        assert isinstance(res["max"], int), "company size min is not an int"
        assert len(res) == 2, "company size dict has more than 2 keys"
        assert res["max"] >= res["min"], "company size max is smaller than min"

    def validate_revenue_range(self):
        """
        makes sure revenue range section per response is valid
        """
        res = self.get_revenue_range()
        # logging.info("validating revenue range for search company")
        assert isinstance(res, dict), "revenue range is not a dict"
        assert isinstance(res["min"], int), "revenue range min is not an int"
        assert isinstance(res["max"], int), "revenue range min is not an int"
        assert len(res) == 2, "revenue range dict has more than 2 keys"
        assert res["max"] >= res["min"], "revenue range max is smaller than min"

    def validate_found_results(self):
        """
        makes sure we found some results and their structure seems normal
        """
        # logging.info(f"validating response for {self.company_name}")
        assert isinstance(self.response.json(), list), "response is not a list"
        assert len(self.response.json()) > 0, "response is empty"
        for company in self.response.json():
            assert "company_size" in company, "company_size not in company"
            assert "domain" in company, "domain not in company"
            assert "revenue_range" in company, "revenue_range not in company"
            assert "name" in company, "company_name not in company"


    def get_company_names(self,name):
        """
        gets company names, as aa list
        """
        return self.get_items_in_res9("name")