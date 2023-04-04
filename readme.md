# Lusha home assignment
testing search_contact, search_company


### how to run: 
    ```
    pytest -m "search_content or search_company" && /
    cat test.log
    ```

### Scope 
- There is no use of authorization/tokens
- Test two endpoints (see test cases)
- attempt to load test them
- containerize the tests in a docker 
- attempt to run the test with a reporter  

### logging:
I'm using basic logging to test.log this can be forwarded to alure and refined.
logging is great to see test steps up to failure and point of failure with
data dump (on high verbosity level) 
however I will not delve into this

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
- boiler plate

not for:
- project structure
- dict comparator function 
I have also used black formatter 
