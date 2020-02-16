from datetime import datetime

def check_and_convert_string_to_date(string):
    """
    User Story 42: Reject Illegitimate dates.

    Converts string to date.
    GEDCOM date format: dd MMM YYYY

    returns: a datetime object
    """
    try:
        return datetime.strptime(string, '%d %b %Y')
    except ValueError:
        print("Invalid date provided.")
        return None

def convert_date_to_string(date):
    return date.strftime('%b %d %Y')


