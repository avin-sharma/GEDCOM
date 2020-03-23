from helpers import convert_date_to_string, check_and_convert_string_to_date
from datetime import date, datetime, timedelta
from collections import defaultdict


def US_39(individuals, families, tag_positions):
    warnings = []
    ua: str = ""
    for fam_id in families:
        family = families[fam_id]
        fm: datetime = family.married
        if family.divorced is None:
            if fm is not None:
                delta = datetime.today() + timedelta(days=30)
                if fm.strftime("%Y") <= datetime.today().strftime("%Y"):
                    if fm.strftime("%m %d") >= datetime.today().strftime("%m %d"):
                        if delta.strftime("%m %d") >= fm.strftime("%m %d"):
                            fm = convert_date_to_string(fm)
                            if fm != ua:
                                num1 = tag_positions[family.hid]['NAME']
                                num2 = tag_positions[family.wid]['NAME']
                                warnings.append(
                                    f'ANOMALY: FAMILY: US39: line {num1} and {num2}, The upcoming anniversaries in next 30 days is of {family.hname} and {family.wname} on {fm}')
                                ua = fm
    return warnings
