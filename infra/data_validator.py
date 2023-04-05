import re
import phonenumbers

from data.top_level_domains import TLDs


def is_valid_email(email):
    """
    Return True if the email address is valid, False otherwise.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_domain(domain):
    """
    run over tlds and see if one is valid
    we can also address HTTP
    """
    for tld in TLDs:
        if domain.lower().endswith(tld.lower()) and domain.lower().startswith("www."):
            return True

    return False

def is_valid_ph_number(ph,logger):
    """
    for use with the kind of values search_contact returns
    otherwise it can be different.
    """
    try:
        string_phone = f"+{ph}"
        parsed_number = phonenumbers.parse(string_phone, None)
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.NumberParseException:
        if ph[0] == "+" and all([x.isdigit() for x in ph[1:]]):
            logger.info(f"weird phone number {ph}")
            return False  #interesting case
        else:
            raise ValueError("error parsing phone number")