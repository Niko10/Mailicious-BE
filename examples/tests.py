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

def test_create_email(headers, sender, receiver, email_datetime, content):
    email_response = create_email(headers, sender, receiver, email_datetime, content)
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

def test_search_emails_advanced(headers, sender=None, receiver=None, content=None, from_time=None, to_time=None, text=None, verdict_id=None):
    search_params = {}
    if sender:
        search_params["sender"] = sender
    if receiver:
        search_params["receiver"] = receiver
    if content:
        search_params["content"] = content
    if from_time:
        search_params["from_time"] = from_time
    if to_time:
        search_params["to_time"] = to_time
    if text:
        search_params["text"] = text
    if verdict_id != None:
        print("Verdict ID:", verdict_id)
        search_params["verdict"] = verdict_id
    
    print("Search Params:", search_params)
    search_response = search_emails_advanced(headers, search_params)
    print("Search Email Response:", search_response)
    return search_response

def test1():
    success_counter = 0
    failure_counter = 0

    # Create a user
    DETECTION_SERVER_USER_NAME = "demo@example.com"
    DETECTION_SERVER_USER_PASSWORD = "demo"
    DETECTION_SERVER_USER_FULL_NAME = "demo test"

    user = test_create_user(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD, DETECTION_SERVER_USER_FULL_NAME)
    if not user:
        print("[X] Failed to create user")
        failure_counter += 1
    else:
        print("[V] User created successfully")
        success_counter += 1
    print("-------------------\n")
    
    # Login
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    if not headers:
        print("[X] Failed to login")
        failure_counter += 1
    else:
        print("[V] Logged in successfully")
        success_counter += 1
    print("-------------------\n")

    # # create verdicts
    # verdicts = [("Legit", "This is a legit email."), ("Evil", "This is not a evil email.")]
    # for name, description in verdicts:
    #     verdict_response = create_verdict(headers, name, description)
    #     print("Create Verdict Response:", verdict_response)
    #     if not verdict_response.get("id"):
    #         print("[X] Failed to create verdict")
    #         failure_counter += 1
    #     else:
    #         print("[V] Verdict created successfully")
    #         success_counter += 1
    # print("-------------------\n")

    # # create analysis types
    # analysis_types = [("Demo Anaysis", "Detect by demo")]
    # for name, description in analysis_types:
    #     analysis_response = create_analysis_type(headers, name, description)
    #     print("Create Analysis Response:", analysis_response)
    #     if not analysis_response.get("id"):
    #         print("[X] Failed to create analysis type")
    #         failure_counter += 1
            
    #     else:
    #         print("[V] Analysis type created successfully")
    #         success_counter += 1
    # print("-------------------\n")

    # # create emails for example
    # emails = [
    #     ("user11@corp.com", "user2@corp.com", "2023-01-01T12:00:00", "This is a test email.", 1, 1),
    #     ("user11@corp.com", "user2@corp.com", "2023-01-02T12:00:00", "This is a test email.", 1, 1),
    #     ("user22@corp.com", "user1@corp.com", "2023-01-02T12:05:00", "This is a test email.", 1, 1),
    #     ("user22@corp.com", "user1@corp.com", "2023-01-02T12:10:00", "This is a test email.", 1, 1),
    #     ("user11@corp.com", "user3@corp.com", "2023-01-02T12:11:00", "This is a test email.", 1, 1),
    #     ("user33@corp.com", "user1@corp.com", "2023-01-02T12:15:00", "This is a mock email.", 1, 1),
    # ]

    # # get all vericts
    # verdicts = get_all_verdicts(headers)
    # print("All Verdicts:", verdicts)
    # if len(verdicts) == 2:
    #     print("[V] All verdicts fetched successfully")
    #     success_counter += 1
    # else:
    #     print("[X] Failed to fetch all verdicts")
    #     failure_counter += 1
    # print("-------------------\n")

    # # get all analysis types
    # analysis_types = get_all_analysis_types(headers)
    # print("All Analysis Types:", analysis_types)
    # if len(analysis_types) == 1:
    #     print("[V] All analysis types fetched successfully")
    #     success_counter += 1
    # else:
    #     print("[X] Failed to fetch all analysis types")
    #     failure_counter += 1
    # print("-------------------\n")
    
    # # create emails analysis for the analysis type
    # for sender, receiver, email_datetime, content, analysis_id, verdict_id in emails:
    #     email_response = create_email(headers, sender, receiver, email_datetime, content)
    #     print("Create Email Response:", email_response)

    #     # create the email analysis
    #     analysis_response = create_email_analysis(headers, email_response['id'], analysis_id, verdict_id)
    #     print("Create Analysis Response:", analysis_response)

    # test advanced search
    # search_response = test_search_emails_advanced(headers, sender="user11")
    # print("Search Response:", search_response)
    # if len(search_response) == 3:
    #     print("[V] Search 1 successful")
    #     success_counter += 1
    # else:
    #     print("[X] Search 1 failed")
    #     failure_counter += 1
    # print("-------------------\n")

    search_response = test_search_emails_advanced(headers)
    print("Search Response:", search_response)
    if len(search_response) == 6:
        print("[V] Search 2 successful")
        success_counter += 1
    else:
        print("[X] Search 2 failed")
        failure_counter += 1
    print("-------------------\n")

    search_response = test_search_emails_advanced(headers, verdict_id=1)
    print("Search Response:", search_response)
    if len(search_response) == 6:
        print("[V] Search 2.1 successful")
        success_counter += 1
    else:
        print("[X] Search 2.1 failed")
        failure_counter += 1
    print("-------------------\n")

    search_response = test_search_emails_advanced(headers, verdict_id=0)
    print("Search Response:", search_response)
    if len(search_response) == 6:
        print("[V] Search 3.1 successful")
        success_counter += 1
    else:
        print("[X] Search 3.1 failed")
        failure_counter += 1
    print("-------------------\n")

    # search_response = test_search_emails_advanced(headers, text="user11")
    # print("Search Response:", search_response)
    # if len(search_response) == 3:
    #     print("[V] Search 3 successful")
    #     success_counter += 1
    # else:
    #     print("[X] Search 3 failed")
    #     failure_counter += 1
    # print("-------------------\n")

    # search_advanced_response = test_search_emails_advanced(headers, sender="user11", text="mock")
    # print("Search Response:", search_advanced_response)
    # if len(search_advanced_response) == 1:
    #     print("[V] Search successful")
    #     success_counter += 1
    # else:
    #     print("[X] Search failed")
    #     failure_counter += 1
    # print("-------------------\n")

    

if __name__ == "__main__":
    test1()
