from typing import List
from typing import NamedTuple

from cvk.cvk.models import County


def parse_county(counties: List[NamedTuple]) -> List[County]:
    final_counties = []
    # skip first line since it included non essential data
    for item in counties[1:]:
        final_counties.append(
            County(
                identifier=int(item[0]),
                name=item[1],
                streets=item[3]
            )
        )
    return final_counties
