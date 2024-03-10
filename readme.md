#  home assignment
testing search_contact, search_company
we have an API that is unfortunately buggy:
I must find the bugs ( with emphasis on data integrity ) make tests for them
and present them here along with my work. 

### how to run: 
first we make sure we have python 3.10 and install requirements:
```pip install -r requirements.txt```

I have marked the tests according to their uses and types
the markers are:
    search_contact: search contact
    search_company: search company
    failing: failing tests
    data_integrity: data integrity tests
    data_integrity_nightly : full runs for data integrity
    sanity: sanity tests
    load: load tests
we can clean the log:
```
> logs/test.log
```
to run sanity tests for example:
    ```
    pytest -m "not load" && /
    cat logs/test.log
    ```

> note - tests will fail... its because there are bugs.  they are documented in readme_bugs.md and failing tests leave informative messages and logs. 

**running tests with more sample names**
to add params (default - 12)
edit "maxparams" in ```pytest.ini``

## overall project architecture:
The project is divided into the following:
- tests files: found in root directory, contain some fixtures and test tests
- documentation : ```.md``` files found in root directory.
- conftest.py : handles logging and some fixtures.
- logs: found in logs/test.log : it contains info about test runs and data
- infra directory : contains utility functions for validating or processing python objects and data
- data directory : contains data such as example names, urls, error messages. used in tests
- request class : a lusha request class that has 2 children for each API endpoint, encapsulates thee endpoint

***typical test architecture***
a test setups a request that it shares via a fixture and also has access to logging.
after a request is made by the fixture, test steps are taken, often in async fashion 
typically they include finding data from one API call and comparing it to other API calls.
data is validated with functions from ```/infra``` directory

### bugs:
please check ```readme_bugs.md```

### Scope 
- There is no use of authorization/tokens
- Test two endpoints (see test cases)
- We use a script to generate test data from names list and company list
    - however in other scenario we can do so daily or before test start 
    - if we have dynamic data
- some names are taken from a limited set:
    - domain names are of a simple format
    - there aren't any weird localizations or special chars
- we use a mock for stored urls (same place for secrets normally)


### logging:
I am using one log for logs/test.log
I wanted to implement a log for each test file but:
- it ended up generating 1000000 files+ 
- it was hard to pass the logger to utils functions without hacking fixtures
   and I feared it will slow me down. 

## problems and limitations:
- logging is in a single file
- I didn't give fixtures and request class access to logging because It was enough to have logs in test level
- I do not produce alure reports as its OOS
- some tests had truncated param lists:
    - this is because running them with 2500+ params even async is heavy
    - pytest is limited in its ability to produce fixtures with params
- I'm not sure I used fixtures correctly: 
    - my goal was caching the results of large batches of requests for reuse.
    - I have used pytests cache for it, however it might introduce bugs in some cases
    - for example if resources that the request represents change as a result of the test.

## tools used:
I have built this project with vscode and python 3.11 
I know lusha is using python 3.8 but as I'm not using new features
I was satisfied to test it once with this python version

I have used postman for exploratory testing of the API 

I have also used :
- requests
- deep diff
- pytest

I have used chatGPT for:
- Idea generation
- boilerplate
however most of everything else is mine incl util functions. 


## API behavior
Overall it seems that we are getting random emails
have some overlap with active companies(users active in many companies)
I know some users are "advisors" and are indeed active in many companies
but for the scope of the test I consider it a bug!

and some emails have invalid content in them

I suspected the API would 'lock out' after getting many requests
but after sending 100k requests to it over 200sec this doesn't seem to be the case
I kept this test in

### Other notes:

## running a lot of parameters:
I could have provided example values to trigger each bug / test failure
Instead I ran a lot of requests with async
I think this is how I would have done tests normally
Later on I started to suspect I was expected to provide single calls with handpicked examples
after "manually testing" the API 
I think this is a valid approach for adding regression coverage after exploratory testing
but I had in mind the coverage of the entire endpoint assuming data is changing
So there is that, it did help me practice async http. 

Than again - some API outputs are random

## sensetive data in logs:
To have meaningful value from such tests we often log results and they can 
include emails, names etc. 
This exposes the logs (that must be sitting on AWS, frequently hacked)
to leaks
so there must be some solution to prevent logs from having sensetive data
esp on live environments....

## test run times
if we run from command line, everything including load tests.. 
its quite a while until we get results for everything
This is a common situation in tests aimed for CD
We might want to save run times for each (test,param) combo
and drop some params if their runtime is too high or if 
we had N failures already in the run 
This should help boost performance. 
