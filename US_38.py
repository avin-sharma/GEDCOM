from helpers import convert_date_to_string, check_and_convert_string_to_date
from datetime import date, datetime, timedelta
from collections import defaultdict


def US_38(individuals, families, tag_positions):
    warnings = []
    ub: str = ""
    for indi_id in individuals:
        individual = individuals[indi_id]
        ib: datetime = individual.birth
        num = tag_positions[indi_id]['NAME']
        if individual.death is None:
            if ib is not None:
                if ib.strftime("%Y") <= datetime.today().strftime("%Y"):
                    delta: datetime = datetime.today() + timedelta(days=30)
                    if ib.strftime("%m %d") >= datetime.today().strftime("%m %d"):
                        if delta.strftime("%m %d") >= ib.strftime("%m %d"):
                            ib = convert_date_to_string(ib)
                            if ib != ub:
                                warnings.append(
                                    f'ANOMALY: INDIVIDUAL: US38, line {num}, The upcoming birthday in next 30 days is of {individual.name} on {ib}')
                                ub = ib
                            # names[individual.name] |= num
    return warnings
