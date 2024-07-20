from utils import *


def test_login(username, password):
    headers = login(username, password)
    if headers:
        print("Login successful")
        return headers
    else:
        print("Login failed")
        return False

def test_create_user(username, password, full_name):
    user_response = create_user(username, password, full_name)
    print("Create User Response:", user_response)
    if user_response.get("id") and user_response.get("email") == username:
        return user_response
    
    return False

def test_create_email(headers, sender, recipients, email_datetime, content):
    email_response = create_email(headers, sender, recipients, email_datetime, content)
    print("Create Email Response:", email_response)
    if email_response.get("id"):
        return email_response
    return False

def test_create_verdict(headers, name, description):
    verdict_response = create_verdict(headers, name, description)
    print("Create Verdict Response:", verdict_response)
    if verdict_response.get("id") and verdict_response.get("name") == name:
        return verdict_response
    return False

def test_create_analysis_type(headers, name, description):
    analysis_response = create_analysis_type(headers, name, description)
    print("Create Analysis Response:", analysis_response)
    if analysis_response.get("id"):
        return analysis_response
    return False

def test_create_analysis(headers, email_id, analysis_id, verdict_id):
    analysis_response = create_email_analysis(headers, email_id, analysis_id, verdict_id)
    print("Create Analysis Response:", analysis_response)
    if analysis_response.get("id"):
        return analysis_response
    return False

def test_search_emails_advanced(headers, sender=None, recipients=None, 
                                content=None, subject=None, from_time=None, 
                                to_time=None, text=None, verdict_id=None, analysis_id=None):
    search_params = {}
    if sender:
        search_params["senders"] = sender
    if recipients:
        search_params["recipients"] = recipients
    if subject:
        search_params["subject"] = subject
    if content:
        search_params["content"] = content
    if from_time:
        search_params["from_time"] = from_time
    if to_time:
        search_params["to_time"] = to_time
    if text:
        search_params["text"] = text
    if verdict_id != None:
        search_params["verdict"] = {"verdict_id": verdict_id, "analysis_id": analysis_id}
    
    print("\nSearch Params:\n\t", search_params)
    search_response = search_emails_advanced(headers, search_params)
    print("Search Email Response:\n\t", search_response)
    return search_response


# Create a user
DETECTION_SERVER_USER_NAME = "demo@example.com"
DETECTION_SERVER_USER_PASSWORD = "demo"
DETECTION_SERVER_USER_FULL_NAME = "demo test"

def create_test_user():
    user = test_create_user(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD, DETECTION_SERVER_USER_FULL_NAME)
    if not user:
        print("[X] Failed to create user")
        return False
    
    print("[V] User created successfully")
    print("-------------------\n")
    return True

def login_test_user():
    # Login
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    if not headers:
        print("[X] Failed to login")
    else:
        print("[V] Logged in successfully")
    print("-------------------\n")
    return headers

def create_verdicts_enums(headers):
    verdicts = [("Legit", "This is a legit email."), ("Evil", "This is not a evil email.")]
    for name, description in verdicts:
        verdict_response = create_verdict(headers, name, description)
        print("Create Verdict Response:", verdict_response)
        if not verdict_response.get("id"):
            print("[X] Failed to create verdict")
        else:
            print("[V] Verdict created successfully")
    print("-------------------\n")

def create_modules_enum(headers):
    modules = [("External Data Sources", "Detect by External Data Sources"), ("Blacklist", "Detect by blacklist")]
    for name, description in modules:
        modules = create_analysis_type(headers, name, description)
        print("Create Analysis Response:", modules)
        if not modules.get("id"):
            print("[X] Failed to create analysis type")
        else:
            print("[V] Analysis type created successfully")
    print("-------------------\n")


def initial_setup():
    user_created = create_test_user()
    if not user_created:
        return
    
    headers = login_test_user()
    create_verdicts_enums(headers) # Creates 2 verdicts
    create_modules_enum(headers) # Creates 2 modules
    
    # create emails for example
    emails = [
        ("user1@corp.com", "user2@corp.com", datetime.now().isoformat(), "Test Subject 1", "Test Content 1", "link1.com", "ASN1", 1, 1),
        ("user1@corp.com", "user2@corp.com, user3@corp.com", datetime.now().isoformat(), "Test Subject 2", "Test Content 2", "link1.com, link2.com", "ASN1, ASN2", 1, 2),
        ("user2@corp.com", "user1@corp.com, user3@corp.com", datetime.now().isoformat(), "Test Subject 3", "Test Content 3", "link2.com", "ASN1, ASN2, ASN3, ASN4", 2, 2)
    ]

    # get all vericts
    verdicts = get_all_verdicts(headers)
    print("All Verdicts:", verdicts)
    if len(verdicts) == 2:
        print("[V] All verdicts fetched successfully")
    else:
        print("[X] Failed to fetch all verdicts")
    print("-------------------\n")

    # get all modules
    analysis_types = get_all_analysis_types(headers)
    print("All Modules:", analysis_types)
    if len(analysis_types) == 2:
        print("[V] All Modules fetched successfully")
        
    else:
        print("[X] Failed to fetch all modules")
    print("-------------------\n")
    
    # create emails
    print("Creating emails...")
    for sender, recipients, email_datetime, subject, content, attachments, ASNs, verdict_id, analysis_id in emails:
        email_response = create_email(headers, sender, recipients, email_datetime, subject, content, attachments, ASNs)
        print("Create Email Response:", email_response)
        if email_response.get("id"):
            print("[V] Email created successfully")
        else:
            print("[X] Failed to create email")
        print("-------------------\n")

        # create analysis
        analysis_response = create_email_analysis(headers, email_response['id'], analysis_id, verdict_id)
        print("Create Analysis Response:", analysis_response)
    
    

def advanced_search_test():
    # Login
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)

    # perform advanced search
    search_response = test_search_emails_advanced(headers,
                                                   sender="user1, ori",
                                                   recipients="test, user2@",
                                                   text="Test",
                                                   verdict_id=1,
                                                   analysis_id=1
    )
    print("[DEBUG] Search Response 1:", search_response)

if __name__ == "__main__":
    initial_setup()
    advanced_search_test()

    
