import random

from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__,
                   url_prefix='/api',
                   template_folder='templates',
                   static_folder='static', static_url_path='static/api')

facts = []
facts_list = [
    "Four in ten U.S. adults are planning to take a family vacation in 2019",
    "In 2020, international travelers spent $83 billion compared to $233 billion in 2019, a loss of 64%",
    "US travel spending in 2019 totaled $1,172.6 billion ($993.5 billion domestic travel spending and $179.1 billion international spending)",
    "On average, Americans plan to spend $737 on their upcoming trip. Gen Xers will spend more than other age groups, and parents of kids under 18 plan to shell out more than $1,000",
    "58% of business travelers say they are traveling in the summer of 2021 for work",
    "77% of US adults have stayed in a hotel or resort, 65% have flown and 27% have taken a cruise",
    "American women rank first in solo traveling and are more likely to take three trips or more in a given year",
    "51% of business travelers said they traveled for business at least four times a year pre-pandemic compared to 31% during the pandemic",
]

def find_next_id():
    return max(facts["id"] for fact in facts) + 1


def _init_facts():
    id = 1
    for fact in facts_list:
        facts.append({"id": id, "fact": fact, "haha": 0, "boohoo": 0})
        id += 1

@api_bp.route('/fact')
def get_fact():
    if len(facts) == 0:
        _init_facts()
    return jsonify(random.choice(facts))

@api_bp.route('/facts')
def get_facts():
    if len(facts) == 0:
        _init_facts()
    return jsonify(facts)


if __name__ == "__main__":
    print(random.choice(facts_list))