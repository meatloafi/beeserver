import requests
from datetime import datetime,timedelta
import json
import time

API = "https://16.16.30.75/bee-hive/owl/owlws/v2"
API_ENDPOINT_LOGIN = f"{API}/login"
API_ENDPOINT_EXECUTE = f"{API}/auto/execute"
USERNAME = "kip_api"
PASSWORD = "KIPbee1"

def login_to_owl():
    session = requests.Session()
    login_data = {"username": USERNAME, "password": PASSWORD}
    headers = {"Content-type": "application/json"}
    try:
        session.post(url=API_ENDPOINT_LOGIN, data=json.dumps(login_data), headers=headers, verify=False)
        print("Login successful")
        return session
    except requests.exceptions.RequestException as e:
        print(f"Error logging in: {e}")
        return None

session = login_to_owl()


def post_owl_data_new(record, datatype, data):
    if not session:
        print("No valid session available")
        return {}

    post_url = f"{API}/storage/records/data/{record}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "data": [
        "{\n    \"" + datatype + "\": \"" + data + "\"\n}"
        ],
        "score": int(time.time() * 1000)
        }
    
    try:
        response = session.put(post_url, headers=headers, data=json.dumps(payload), verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error posting data: {e}")
        return {}
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return {}


def delete_owl_data(data_name, score):
    if not session:
        print("No valid session available")
        return {}
    
    delete_url = f"{API}/storage/records/data/{data_name}"
    headers = {"Content-Type": "application/json"}
    payload = {"scores": [score]}
    
    try:
        response = session.delete(delete_url, headers=headers, data=json.dumps(payload), verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error deleting data: {e}")
        return {}
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return {}


def delete_old_owl_data(data_name, days_to_retain):
    data = retrieve_data(data_name)
    today = datetime.utcnow()
    cutoff_date = today - timedelta(days=days_to_retain)
    
    if data_name in data and data[data_name]:
        for record in data[data_name]:
            if "score" in record:
                score = record["score"]
                record_date = datetime.utcfromtimestamp(score / 1000)
                
                if record_date < cutoff_date:
                    print(f"Deleting record with score {score} dated {record_date.strftime('%Y-%m-%d')}")
                    delete_response = delete_owl_data(data_name, score)
                    print(delete_response)
    else:
        print("No data found for the specified data_name.")

def retrieve_data(data_name):
    base_url = "https://16.16.30.75/bee-hive/owl/owlws/v2"
    storage_url = f"{base_url}/storage/records/data?name="
    headers = {"Content-Type": "application/json"}

    data_url = f"{storage_url}{data_name}"
    data_response = requests.get(data_url, headers=headers, verify=False)

    data = data_response.json()
    return data

def get_owl_data(data_name, param):
    data = retrieve_data(data_name)
    if data_name in data and data[data_name]:
        last_record = data[data_name][-1]
        if param in last_record.get("data", {}):
            return last_record["data"][param]
    return None

def get_owl_data_periodical_last_updated(data_name, param, days):
    data = retrieve_data(data_name)
    collected_values = {}
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Calculate the start date by subtracting 'days' from today's date
    start_date = (datetime.now() - timedelta(days=days-1)).strftime('%Y-%m-%d')

    if data_name in data and data[data_name]:
        # Sort records by score (timestamp) to ensure we process them in chronological order
        sorted_records = sorted(data[data_name], key=lambda x: x.get('score'))

        for record in sorted_records:
            if "data" in record and param in record["data"]:
                score = record.get("score")
                date = datetime.utcfromtimestamp(score / 1000).strftime('%Y-%m-%d')
                time = datetime.utcfromtimestamp(score / 1000).strftime('%H:%M:%S')
                
                # Check if the record date is within the range of start_date and today
                if start_date <= date <= today:
                    if date == today:
                        # For today's date, always take the most recent record
                        collected_values[date] = (time, record["data"][param])
                    else:
                        # For other dates, select the entry closest to 12:00 PM
                        target_time = datetime.strptime("12:00:00", '%H:%M:%S')
                        current_time = datetime.strptime(time, '%H:%M:%S')
                        
                        if date not in collected_values:
                            collected_values[date] = (time, record["data"][param])
                        else:
                            existing_time = datetime.strptime(collected_values[date][0], '%H:%M:%S')
                            if abs((current_time - target_time).total_seconds()) < abs((existing_time - target_time).total_seconds()):
                                collected_values[date] = (time, record["data"][param])

    else:
        print("No data found for the specified data_name.")

    # Convert collected values dictionary to sorted list of tuples
    collected_values_list = [(date, value) for date, (time, value) in sorted(collected_values.items())]
    for date, value in collected_values_list:
        print(f"Date: {date}, Value for {param}: {value}")

    return collected_values_list

def get_owl_data_periodical(data_name, param, days):
    data = retrieve_data(data_name)
    collected_values = []
    printed_dates = set()
    days_count = 1

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Calculate the start date by subtracting 'days' from today's date
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    if data_name in data and data[data_name]:

        for record in data[data_name]:
            if "data" in record and param in record["data"]:
                score = record.get("score")
                date = datetime.utcfromtimestamp(score / 1000).strftime('%Y-%m-%d')
                
                # Check if the record date is within the range of start_date and today
                if start_date <= date <= today and date not in printed_dates:
                    value = record["data"][param]
                    collected_values.append((date, value))
                    print(f"Date: {date}, Value for {param}")
                    printed_dates.add(date)
                    days_count += 1
                    if days_count >= days:
                        break
    else:
        print("No data found for the specified data_name.")
    

    return collected_values
