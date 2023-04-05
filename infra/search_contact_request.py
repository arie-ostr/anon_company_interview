from infra.lusha_request import LushaRequest


_example_valid_response = {
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

class SearchContactRequest(LushaRequest):
    def __init__(self, full_name: str, company: str, is_current_company: bool) -> None:
        super().__init__(
            endpoint="search_contact",
            method="POST",
            payload={
                "full_name": full_name,
                "company_name": company,
                "is_current_company": is_current_company,
            },
        )
        self.company = company
        self.is_current_company = is_current_company
        self.full_name = full_name
        self.example_valid_response = _example_valid_response
