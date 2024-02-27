import requests
from datetime import  timedelta


def build_payload(date):
    """
    Constructs the payload data for the Neobus ticket search request.
    Args:
        date (datetime.date): The date for which to search tickets.
    Returns:
        dict: The payload data.
    """

    formatted_date = date.strftime("%d.%m.%Y")
    initial_stop = 75
    final_stop = 76
    passengers = 1
    return {
        "ajax": "true",
        "dataType": "json",
        "module": "neotickets",
        "step": 1,
        "initial_stop": initial_stop,
        "final_stop": final_stop,
        "passengers": passengers,
        "date_there": formatted_date
    }

def fetch_available_tickets(date):
    """
    Fetches available Neobus tickets for a specific date.
    Args:
        date (datetime.date): The date for which to search tickets.
    Returns:
        list: A list of available tickets if found, otherwise None.

    Raises:
        Exception: If an error occurs during the request.
    """

    payload = build_payload(date)
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    response = requests.post("https://neobus.pl/", data=payload, headers=headers, verify=False)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch tickets: {response.status_code}")
    try:
        return response.json()["neotickets"]["ga4_data"][0]["items"]
    except (KeyError, IndexError, TypeError) as e:
        return False



def find_first_available_date(start_date, end_date):
    """
    Performs a binary search to find the first date with available Neobus tickets
    within the given date range.

    Args:
        start_date (datetime.date): The start date of the search range.
        end_date (datetime.date): The end date of the search range.
    Returns:
        datetime.date: The first date with available tickets, or None if no tickets
        are found within the given range.
    """

    print("NEOBUS: Checking date:", start_date.strftime("%d.%m.%Y"))
    available_tickets = fetch_available_tickets(start_date + timedelta(days=1))
    if not available_tickets:
        return start_date

    while start_date <= end_date:
        mid_date = start_date + (end_date - start_date) // 2
        print("NEOBUS: Checking date:", mid_date.strftime("%d.%m.%Y"))
        available_tickets = fetch_available_tickets(mid_date)
        if available_tickets:
            start_date = mid_date + timedelta(days=1)
        else:
            end_date = mid_date - timedelta(days=1)

    return start_date - timedelta(days=1)


def check_neobus_tickets(start_date):
    """
    Checks for available Neobus tickets for the next 3 months.
    """
    end_date = start_date + timedelta(days=90)
    print(f"Checked date from: {start_date.strftime('%d.%m.%Y')} to: {end_date.strftime('%d.%m.%Y')}")

    max_date_found = find_first_available_date(start_date, end_date)

    if max_date_found:
        print(f"NEOBUS: Tickets available up to: {max_date_found.strftime('%d.%m.%Y')}")
        return max_date_found
    else:
        print("NEOBUS: No tickets found in the next 3 months.")

