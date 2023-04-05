import re
import random

# get all crossed names
crossed_names = []
with open("data/crossed_names.txt") as f:
        crossed_names = f.read().splitlines()
        

# get a predictably random sample
random.seed(25000)
n = 20
with open("pytest.ini","r") as f:
    lines = f.readlines()
    for line in lines:
        res = re.findall(r"^maxparams=(\d+)\n", line)
        if res:
            n=int(res[0])

crossed_names_sample = random.sample(crossed_names, n)