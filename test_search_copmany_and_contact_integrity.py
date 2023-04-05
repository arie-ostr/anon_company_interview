import pytest
from infra.data_validator import is_valid_ph_number

from infra.dict_comparator import compare_dicts
from infra.search_company_request import SearchCompanyRequest

from data.error_responses import NOT_ALLOWED_RESPONSE_BODY as response405
from data.error_responses import NOT_FOUND_CONTACT as response404


@pytest.mark.search_contact
def test_name_in_contact_response_matches_request(logger, contacts_across_companies):
    """
    given a user queries search_contact for a full name
    when the user checks various companies
    then the full name in the response matches other responses

    note: this could cause inconsistencies if violated.
    """
    names = set()
    for res in contacts_across_companies:
        full_name = res["payload"]["full_name"]
        company = res["payload"]["company_name"]
        is_current_company = res["payload"]["is_current_company"]
        if res["json"] != response404:
            names.add(res["json"]["full_name"])
            if len(names) > 1:
                #we fail right now to boost performance
                #however in a nightly run we would want all names
                err = f"mismatching names found: {names}"
                assert len(names) == 1, err


@pytest.mark.search_contact
def test_only_one_current_company_full_list(logger, contacts_across_companies):
    """
    given a full list of contact names
        and companies
    when searching for each contact with company
    then it has only one current company
    """
    current_company_count = 0
    for res in contacts_across_companies:
        full_name = res["payload"]["full_name"]
        company = res["payload"]["company_name"]
        is_current_company = res["payload"]["is_current_company"]
        if is_current_company and res["json"] != response404:
            current_company_count += 1
            logger.info(f"found {company} as current company for {full_name}")
            if current_company_count > 1:
                assert False, f"more than one current company for {full_name}"


@pytest.mark.search_contact
def test_company_details_in_contacy_match_actual_company_details(
    logger, contacts_across_companies
):
    """
    given a full list of contact names
        and companies
    when searching for each contact with company
        and searching for this comany
    then company details match
    """
    for res in contacts_across_companies:
        if res["status"] == 404:
            continue  # skip not found

        company = res["payload"]["company_name"]
        expected_json = res["json"]["company"]
        company_request = SearchCompanyRequest(name=company)
        company_request.execute_request()
        request_json = company_request.get_response_json()[0]  # pop name

        diff = compare_dicts(request_json, expected_json)
        if diff:
            logger.error(f"found weird values: {str(diff)}")
            assert False, f"company details do not match for {company}"


@pytest.mark.search_contact
def test_contact_phone_integrity(logger, contacts_across_companies):
    """
    given a contact result
    when we check phone number
    then it is valid
    """
    for res in contacts_across_companies:
        if res["status"] == 404:
            continue  # skip not found

        phone = res["json"]["phone"]
        is_valid_phone = is_valid_ph_number(phone,logger)

        if is_valid_phone == True:
            logger.info(f"phone number {phone} is fully valid")
        else:
            logger.error(f"phone number {phone} is invalid")
            assert False,"invalid phone"


@pytest.mark.skip(reason="the phone number field should be redone, is it private?")
@pytest.mark.search_contact
def test_contact_different_phone_numbers_across_companies(
    logger, contacts_across_companies
):
    """
    given a contact name
    when we check phone number across different companies
    then it is the same

    note: stale/changed phone numbers are a problem
    """
    phones = {}
    for res in contacts_across_companies:
        if res["status"] == 404:
            continue  # skip not found

        phone = res["json"]["phone"]
        phones[phone] = res["payload"]["company_name"]

    logger.info(f"found {str(phones)}")
    assert len(phones) == 1, f"found more than one phone number: {str(phones)}"


@pytest.mark.search_contact
def test_private_email_integrity(logger, contacts_across_companies):
    """
    given a user who has at most 5 private emails
    when we search him across companies
    then we find at most 5 emails

    note:
    """
    private_mails = {}
    for res in contacts_across_companies:
        if res["status"] == 404:
            continue  # skip not found

        private_mail = res["json"]["private_email"]
        private_mails[private_mail] = res["payload"]["company_name"]

        logger.info(f"found {str(private_mails)}")
        assert (
            len(private_mails) <= 5 #we terminate on 6th mail, to save time
        ), f"found more than one phone number: {str(private_mails)}"


@pytest.mark.search_contact
def test_keys_stable_for_all_contacts(logger, contacts_across_companies):
    """
    given data on user contains various keys
    when we search for it in one endpoint
    then we expect consistent keys
    """
    for res in contacts_across_companies:
        if res["status"] == 404:
            continue  # skip not found
        
        keys = res["json"].keys()
        expected_keys = {'company', 'full_name', 'phone', 'private_email', 'work_email'}
        logger.info("found keys: " + str(keys))
        assert keys == expected_keys, f"found unexpected keys: {str(keys)}"
        #to save time, we could skip the test if we find one mutation
        
        company_keys = res["json"]["company"].keys()
        expected_company_keys = {'company_size', 'domain', 'name', 'revenue_range'}
        logger.info("found company keys: " + str(company_keys))
        assert company_keys == expected_company_keys, f"found unexpected keys: {str(keys)}"




@pytest.mark.search_contact
def test_user_name_reflected_in_work_email(logger, contacts_across_companies):
    """
    given a user who has work emails across companies
    when we find his work email
    then it contains his name with high probability

    note: normally I wouldn't use try/catch for this situation
        rather: I would skip or add above test as condition
    """
    for res in contacts_across_companies:
        if res["status"] == 404:
            continue  # skip not found

        try:  # we dump data from tests that fail on other bugs
            # normally I wouldnt do this on production tests
            # but here I want to catch more bugs that might be masked
            if "work_mail" in res["json"]:
                logger.info("found incorrect key 'work_mail'")
                continue  # we dump this attempt
            elif "work_email" in res["json"]:
                work_mail = res["json"]["work_email"]
                first_name = res["json"]["full_name"].split(" ")[0].lower()
                last_name = res["json"]["full_name"].split(" ")[1].lower()

                logger.info(f"checking {first_name} in {work_mail}")

                first_name_in = first_name in work_mail.lower()
                last_name_in = last_name in work_mail.lower()
                assert any(
                    [first_name, last_name_in]
                ), f"{first_name} or {last_name} not in {work_mail}"

                continue
            elif "work_mail" not in res["json"] and "work_email" not in res["json"]:
                logger.info(f"found no work email at all in {res['json'].keys()}")
                continue
        except KeyError as err:
            assert False, f"key error: {str(err)}"
