# bugs found

## search_company status code 500 , should be 405
**steps to reproduce**: 
1. run a valid request and verify its ok
2. change its method to GET,PUT,DELETE etc (not post)

**expected result:**
4.status code 405
**actual result:**
correct error message, internal server error code. 


## users have more than one current compant,
**steps to reproduce**:
1. search for the following in POST /search_contact
    { 
        "full_name": "EMMA smith", 
        "company_name": "millard public schools",
        "is_current_company": true 
    }
    as well as:
    { 
        "full_name": "EMMA smith", 
        "company_name": "Connacher Oil And Gas",
        "is_current_company": true 
    }
**expected result** 
we shouldn't be able to locate both companies

**actual result**
we can find users such as the above with multiple current companies

**impact**
this means that stale sata is likely present in the db, make sure only current data is used.

## company names are mutating
**steps to reproduce**
1. this is unlikely to be reproduced manually
2. run the test test_company_details_in_contacy_match_actual_company_details
3. watch the logs : we see cases such as 
    - 'new_value':'Millard Public Schools'
    - 'old_value':'Nillard Public Schools'
```
2023-04-05 19:39:31,661 - test - ERROR - found weird values: {"root['name']": {'new_value': 'Millard Public Schools', 'old_value': 'Lillard Public Schools'}}
```
**expected result**
non existant companies not found

**actual result**
spooky companies foud

**impact**
there is some error in data collection that is propogating, or user typo. 



## company names are mutating
**steps to reproduce**
1. execute request to search_contact
2. alternatively run the test test_contact_phone_integrity
3. check phone number for validity

**expected result**
valid phone numbers for country

**actual result**
invalid phone numbers

**impact**
phone numbers are improperly generated
(I know its faked)

## phone is potentially private
while many workers get a company phone it is unclear from this endpoint

**steps to reproduce**
1. execute request to search_contact
2. also check test test_contact_different_phone_numbers_across_companies

**expected result**
response field states if phone is company phone

**actual result**
it might be private, we can't know

**impact**
privacy violation 


## keys in responses change
**steps to reproduce**
1. you can run the test test_keys_stable_for_all_contacts
2. or you can try different search_contact requests
3. check keys such as work_email 

**expected result**
keys are consistent

**actual result**
keys change - we find "work mail" 
keys can disappear

**impact**
inconsistent data souces


## mutating value in search_contact
**steps to reproduce**
1. search for this contact:
    { 
    "full_name": "emma smith", 
    "company_name": "Millard Public Schools", 
    "is_current_company": true 
    }
2. or run the test test_search_contact_for_data_stability
3. do it repeatedly and watch for the response

**expected result**
result is stable

**actual result** 
result changes 

**impact**
possible duplicate data.

## company names mutate in search_company
**steps to reproduce**
1. run the following test
    ``test_company_names_stability```
2. alternatively you can search for a company such as:
    ```Api engineering```
3. might have to run several times

**expected result**
company name stable 

**actual result**
```Api engineering``` yields ```Vpi engineering```

**impact**
corrupt data sources or pipeline.