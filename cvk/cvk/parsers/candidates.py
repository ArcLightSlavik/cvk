from typing import List
from typing import NamedTuple

import re

from cvk.cvk.models import Candidate


def parse_candidates(candidates: List[NamedTuple]) -> List[Candidate]:
    candidates_list = []
    party = None
    # skip initial table
    for item in candidates[1:]:
        # get the party
        if item[1] == item[2]:
            party = item[1]
            continue

        # county number can be either a number or 'First Candidate'
        try:
            number_in_country = int(item[5])
        except ValueError:
            number_in_country = item[5]

        # Spacing issue fix
        full_name = re.sub(r"(\w)([А-ЯҐЄІЇ])", r"\1 \2", item[1])

        candidates_list.append(Candidate(
            party_identifier=int(item[0]),
            full_name=full_name,
            birthday_and_place_of_birth=item[2],
            info=item[3],
            county=item[4],
            number_in_county=number_in_country,
            party=party
        ))

    return candidates_list
