import re
import random

# get a list of company names
company_names = []
with open("data/companies.txt") as f:
        company_names = f.read().replace("\n","").split(", ")
        

# get a predictably random sample
random.seed(25000)
n = 20
with open("pytest.ini","r") as f:
    lines = f.readlines()
    for line in lines:
        res = re.findall(r"^maxparams=(\d+)\n", line)
        if res:
            n=int(res[0])

company_names_sample = random.sample(company_names, n)