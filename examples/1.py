import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def create_user(email, password, full_name):
    url = f"{BASE_URL}/users/"
    payload = {
        "email": email,
        "password": password,
        "full_name": full_name
    }
    response = requests.post(url, json=payload)
    return response.json()

def login(email, password):
    url = f"{BASE_URL}/token"  # Ensure the endpoint is correct
    payload = {
        "username": email,
        "password": password
    }
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    print(f"Login payload: {payload}")
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        token = response.json().get("access_token")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return headers
    else:
        print(f"Login failed: {response.json()}")
        return None

def create_email(headers, sender, receiver, email_datetime, content):
    url = f"{BASE_URL}/emails/"
    payload = {
        "sender": sender,
        "receiver": receiver,
        "email_datetime": email_datetime,
        "content": content
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def create_verdict(headers, name, description):
    url = f"{BASE_URL}/enum_verdicts/"
    payload = {
        "name": name,
        "description": description
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def create_analysis_type(headers, name, description):
    url = f"{BASE_URL}/enum_analysis/"
    payload = {
        "name": name,
        "description": description
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def create_email_analysis(headers, email_id, analysis_id, verdict_id):
    url = f"{BASE_URL}/analysis/"
    payload = {
        "email_id": email_id,
        "analysis_id": analysis_id,
        "verdict_id": verdict_id
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def get_all_emails(headers):
    url = f"{BASE_URL}/emails/"
    response = requests.get(url, headers=headers)
    return response.json()

def get_all_analysis(headers):
    url = f"{BASE_URL}/analysis/"
    response = requests.get(url, headers=headers)
    return response.json()

def get_all_verdicts(headers):
    url = f"{BASE_URL}/enum_verdicts/"
    response = requests.get(url, headers=headers)
    return response.json()

def get_all_analysis_types(headers):
    url = f"{BASE_URL}/enum_analysis/"
    response = requests.get(url, headers=headers)
    return response.json()

def search_emails_by_sender(headers, sender):
    url = f"{BASE_URL}/search/email"
    payload = {
        "sender": sender
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def search_emails_by_receiver(headers, receiver):
    url = f"{BASE_URL}/search/email"
    payload = {
        "receiver": receiver
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def search_emails_by_sender_and_receiver(headers, sender, receiver):
    url = f"{BASE_URL}/search/email"
    payload = {
        "sender": sender,
        "receiver": receiver
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def search_emails_by_time_range(headers, from_time, to_time):
    url = f"{BASE_URL}/search/email"
    payload = {
        "from_time": from_time,
        "to_time": to_time
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def search_emails_by_time_range_and_sender(headers, from_time, to_time, sender):
    url = f"{BASE_URL}/search/email"
    payload = {
        "from_time": from_time,
        "to_time": to_time,
        "sender": sender
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def get_current_user(headers):
    url = f"{BASE_URL}/users/me"
    response = requests.get(url, headers=headers)
    return response.json()

def search_advanced(params, headers):
    url = f"{BASE_URL}/search/advanced"
    response = requests.get(url, json=params, headers=headers)
    return response.json()


def example_1():
    # Create a user
    user_response = create_user("testuser@example.com", "testpassword", "Test User")
    print("Create User Response:", user_response)

    # Login and get headers
    headers = login("testuser@example.com", "testpassword")
    if headers:
        print("Login successful")

        # Create an email
        email_response = create_email(headers, "testuser@example.com", "receiver@example.com", "2023-01-01T12:00:00", "This is a test email.")
        print("Create Email Response:", email_response)

        # Create a verdict
        verdict_response = create_verdict(headers, "Test Verdict", "This is a test verdict.")
        print("Create Verdict Response:", verdict_response)

        # Create an analysis type
        analysis_type_response = create_analysis_type(headers, "Test Analysis", "This is a test analysis.")
        print("Create Analysis Type Response:", analysis_type_response)

        # Create an analysis
        analysis_response = create_email_analysis(headers, email_response['id'], analysis_type_response['id'], verdict_response['id'])
        print("Create Analysis Response:", analysis_response)

        # Get all emails
        emails = get_all_emails(headers)
        print("All Emails:", emails)

        # Get all analysis
        analyses = get_all_analysis(headers)
        print("All Analysis:", analyses)

        # Search emails by sender
        search_sender = search_emails_by_sender(headers, "testuser@example.com")
        print("Search Emails by Sender:", search_sender)

        # Search emails by receiver
        search_receiver = search_emails_by_receiver(headers, "receiver@example.com")
        print("Search Emails by Receiver:", search_receiver)

        # Search emails by sender and receiver
        search_sender_receiver = search_emails_by_sender_and_receiver(headers, "testuser@example.com", "receiver@example.com")
        print("Search Emails by Sender and Receiver:", search_sender_receiver)

        # Search emails by time range
        from_time = "2024-01-01T00:00:00"
        to_time = datetime.now().isoformat()
        search_time_range = search_emails_by_time_range(headers, from_time, to_time)
        print("Search Emails by Time Range:", search_time_range)

        # Search emails by time range and sender
        search_time_range_sender = search_emails_by_time_range_and_sender(headers, from_time, to_time, "testuser@example.com")
        print("Search Emails by Time Range and Sender:", search_time_range_sender)
    else:
        print("Login failed")

def initial_setup_example():
    # Create a user
    DETECTION_SERVER_USER_NAME = "test@test.com"
    DETECTION_SERVER_USER_PASSWORD = "test"
    DETECTION_SERVER_USER_FULL_NAME = "test"

    user_response = create_user(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD, DETECTION_SERVER_USER_FULL_NAME)
    print("Create User Response:", user_response)

    # login and get headers
    headers = login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    if headers:
        print("Login successful")

        # get current user
        current_user = get_current_user(headers)
        print("Current User:", current_user)
       
        # create verdicts
        verdicts = [
            ("Benign", "This email is legit."),
            ("Malicious", "This email is malicious."),
        ]
        for name, description in verdicts:
            verdict_response = create_verdict(headers, name, description)
            print("Create Verdict Response:", verdict_response)
        
        # create analysis types
        analysis_types = [
            ("ExternalDataSources", "This Module interacts with several external data sources to enrich and globalize the detection capabilities"),
        ]
        for name, description in analysis_types:
            analysis_type_response = create_analysis_type(headers, name, description)
            print("Create Analysis Type Response:", analysis_type_response)
        
        # create emails for example
        emails = [
            ("user11@corp.com", "user2@corp.com", "2023-01-01T12:00:00", "This is a test email."),
            ("user11@corp.com", "user2@corp.com", "2023-01-02T12:00:00", "This is a test email."),
            ("user22@corp.com", "user1@corp.com", "2023-01-02T12:05:00", "This is a test email."),
            ("user22@corp.com", "user1@corp.com", "2023-01-02T12:10:00", "This is a test email."),
            ("user11@corp.com", "user3@corp.com", "2023-01-02T12:11:00", "This is a test email."),
            ("user33@corp.com", "user1@corp.com", "2023-01-02T12:15:00", "This is a test email."),
        ]

        # get all vericts
        verdicts = get_all_verdicts(headers)
        print("All Verdicts:", verdicts)

        # get all analysis types
        analysis_types = get_all_analysis_types(headers)
        print("All Analysis Types:", analysis_types)

        # create emails analysis for the analysis type
        for sender, receiver, email_datetime, content in emails:
            email_response = create_email(headers, sender, receiver, email_datetime, content)
            print("Create Email Response:", email_response)

            # create an analysis for the email randomly
            i = 0
            analysis_type = analysis_types[i % len(analysis_types)]
            verdict = verdicts[i % len(verdicts)]

            # create the email analysis
            analysis_response = create_email_analysis(headers, email_response['id'], analysis_type['id'], verdict['id'])
            print("Create Analysis Response:", analysis_response)
        
    else:
        print("Login failed")
    

def search_examples():
    
    # Create a user
    DETECTION_SERVER_USER_NAME = "poc@test.com"
    DETECTION_SERVER_USER_PASSWORD = "poc"
    DETECTION_SERVER_USER_FULL_NAME = "poc"

    user_response = create_user(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD, DETECTION_SERVER_USER_FULL_NAME)
    print("Create User Response:", user_response)

    # Login and get headers
    headers = login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)

    if headers:
        print("Login successful")

        # Create Email to search:
        email_response = create_email(headers, "user11@corp.com", "orih@corp.com", "2023-01-01T12:00:00", "This is a mock email.")
        print("Create Email Response:", email_response)

        # Search emails by sender
        search_advanced_results = search_advanced({"sender": 'user', "text": "mock"}, headers)
        print("Search Advanced Results:", search_advanced_results)
                    

# Example usage
if __name__ == "__main__":
    # example_1()
    #initial_setup_example()
    search_examples()