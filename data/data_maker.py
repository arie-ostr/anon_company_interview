import itertools
import random
import json


def generate_names():
    """
    since we only have 50 names per file, we avoid using complex processing tools
    we simply one shot the names, create a cross product and save it to a new file

    notice that this tool is meant to be ran once
    """
    first_names = []
    with open("data/first_names.txt", "r") as f:
        text = f.read()
        first_names.extend([name.strip().replace("\n", "") for name in text.split(",")])

    last_names = []
    with open("data/last_names.txt", "r") as f:
        text = f.read()
        last_names.extend([name.strip() for name in text.split(",")])

    cross_product = itertools.product(first_names, last_names)

    output_file = "data/crossed_names.txt"
    with open(output_file, "w") as file:
        for item in cross_product:
            try:
                file.write(f"{item[0].lower()} {item[1].lower()}\n")
            except AttributeError as err:
                raise err


def crossed_companies():
    res = []
    with open("data/crossed_names.txt", "r") as f:
        with open("data/companies.txt", "r") as f2:
            company_names = f2.read().split(",")
            crossed_names = [line.strip() for line in f.readlines()]
            for name in crossed_names:
                sample_50 = random.sample(company_names, 50)
                pairs = [
                    {
                        "name": name.strip(),
                        "company": company.strip(),
                        "expected_result": None,
                    }
                    for company in sample_50
                ]
                res.extend(pairs)

    with open("data/crossed_companies.json", "w") as f:
        json.dump(res, f)


if __name__ == "__main__":
    names = crossed_companies()
