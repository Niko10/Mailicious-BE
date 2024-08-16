from utils import *
import sys
import json

def test_login(username, password):
    print("Logging in - ", username, " - ", password)
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

def test_create_module(headers, name, description, enabled=True):
    analysis_response = create_module(headers, name, description, enabled)
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
                                to_time=None, text=None, verdict_id=None, analysis_id=None, final_verdict=None):
    search_params = {}
    if sender:
        search_params["sender"] = sender
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
    if final_verdict:
        search_params["final_verdict"] = final_verdict
    
    print("\nSearch Params:\n", json.dumps(search_params, indent=4))
    search_response = search_emails_advanced(headers, search_params)
    return search_response


# Create a user
DETECTION_SERVER_USER_NAME = "demo@example.com"
DETECTION_SERVER_USER_PASSWORD = "demo"
DETECTION_SERVER_USER_FULL_NAME = "demo test"

# Test functions message:
INVALID_TEST_NUMBER = "Invalid test number"
AVAILABLE_TESTS = """
Here are available tests:
1. Initial Setup - 
    - Create a user
    - Login
    - Create Verdicts
    - Create Modules
    - Create Emails
    - Create Analysis
2. Advanced Search Test -
    - Perform advanced search
3. Add Analysis to Email -
    - Add analysis to email
4. Create Fields Enum Test -
    - Create fields enum
5. Get Fields Enum Test -
    - Get fields enum
6. Create Blacklist Items Test -
    - Create blacklist items
7. Get Blacklist Items Test -
    - Get blacklist items
8. Set POC User -
    - Create a POC user
    - Login as POC user

To run a test, use the following command:
python tests.py <test_number>

Example:
python tests.py 1
python tests.py 1 2 3
python tests.py 3 4 1
"""


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
    verdicts = [("Benign", "This is a benign email."), ("Suspicious", "This is not a suspicious email."), ("Malicious", "This is a malicious email.")]
    for name, description in verdicts:
        verdict_response = create_verdict(headers, name, description)
        print("Create Verdict Response:", verdict_response)
        if not verdict_response.get("id"):
            print("[X] Failed to create verdict")
        else:
            print("[V] Verdict created successfully")
    print("-------------------\n")

def create_modules_enum(headers):
    modules = [("Final Verdict", "Detect by final verdict", True), ("External Data Sources", "Detect by External Data Sources", True), ("Blacklist", "Detect by blacklist", True)]
    for name, description, enabled in modules:
        modules = create_module(headers, name, description, enabled)
        print("Create Module Response:", modules)
        if not modules.get("id"):
            print("[X] Failed to create module")
        else:
            print("[V] Module created successfully")
    print("-------------------\n")


def initial_setup():
    user_created = create_test_user()
    if not user_created:
        return
    
    headers = login_test_user()
    create_verdicts_enums(headers) # Creates 3 verdicts
    create_modules_enum(headers) # Creates 3 modules
    
    # create emails for example
    emails = [
        ("user1@corp.com", "user2@corp.com", datetime.now().isoformat(), "Test Subject 1", "Test Content 1", "link1.com", "SPF_IP1", "SPF_status1", [(2,2), (3,2)]),
        ("user1@corp.com", "user2@corp.com, user3@corp.com", datetime.now().isoformat(), "Test Subject 2", "Test Content 2", "link1.com, link2.com", "SPF_IP1, SPF_IP2", "SPF_status1", [(2,3), (3,1)]),
        ("user2@corp.com", "user1@corp.com, user3@corp.com", datetime.now().isoformat(), "Test Subject 3", "Test Content 3", "link2.com", "SPF_IP1, SPF_IP2, SPF_IP3, SPF_IP4", "SPF_status2", [(2,1), (3,2)]),
        ("user2@corp.com", "user4@corp.com, user5@corp.com", "2023-05-27 18:07:28.155490", "Test Subject 4", "Test Content 4", "link2.com", "SPF_IP1, SPF_IP2, SPF_IP3, SPF_IP4", "SPF_status2", [(2,2), (3,2)]),
        ("user1@corp.com", "user2@corp.com", "2023-05-27 18:07:28.155490", "Test Subject 5", "Test Content 5", "link1.com", "SPF_IP1", "SPF_status1", [(2,2), (3,1)]),
        ("user5@corp.com", "user2@corp.com", "2023-09-01 15:07:28.155490", "Test Subject 6", "Test Content 6", "link1.com", "SPF_IP1", "SPF_status1", [(2,3), (3,1)]),
    ]

    # get all vericts
    verdicts = get_all_verdicts(headers)
    print("All Verdicts:", verdicts)
    if len(verdicts) == 3:
        print("[V] All verdicts fetched successfully")
    else:
        print("[X] Failed to fetch all verdicts")
    print("-------------------\n")

    # get all modules
    analysis_types = get_all_analysis_types(headers)
    print("All Modules:", analysis_types)
    if len(analysis_types) == 3:
        print("[V] All Modules fetched successfully")
        
    else:
        print("[X] Failed to fetch all modules")
    print("-------------------\n")
    
    # create emails
    print("Creating emails...")
    try:
        for sender, recipients, email_datetime, subject, content, attachments, SPF_IPs, SPF_status, analysis_pairs in emails:
            email_response = create_email(headers, sender, recipients, email_datetime, subject, content, attachments, SPF_IPs, SPF_status)
            print("Create Email Response:", email_response)
            if email_response.get("id"):
                print("[V] Email created successfully")
            else:
                print("[X] Failed to create email")
            print("-------------------\n")

            for analysis_id, verdict_id in analysis_pairs:
                # create analysis
                analysis_response = create_email_analysis(headers, email_response['id'], analysis_id, verdict_id)
                print("Create Analysis Response:", analysis_response)
    except Exception as e:
        print("[X] Failed to create emails beacuse of an exception: ")
        print(e)
        for email in emails:
            print("Email length:", len(email))
            print("Current email:", email)
        print("-------------------\n")
        exit(1)
    

def add_analysis_to_email(email_id=1, analysis_id=2, verdict_id=2):
    # Login
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)

    # create analysis
    analysis_response = test_create_analysis(headers, email_id, analysis_id, verdict_id)
    print("Create Analysis Response:", analysis_response)
    if analysis_response.get("id"):
        print("[V] Analysis created successfully")
    else:
        print("[X] Failed to create analysis")
    print("-------------------\n")


def advanced_search_test():
    # Login
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)

    # perform advanced search
    search_response = test_search_emails_advanced(headers,
                                                   #sender=["user1", "ori"],
                                                   #recipients=["test", "user2@"],
                                                   #text="Test",
                                                   #sender=["user2@"]
                                                   #from_time="2024-07-26T19:00",
                                                   #to_time="2024-08-03T19:00",
                                                   final_verdict = ["Suspicious"]
    )
    print("[DEBUG] Search Response 1:\n", json.dumps(search_response, indent=4))


def create_fields_enum_test():
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    fields = ["domain", "subject", "SPF_IP", "country"]
    for name in fields:
        fields_response = create_fields_enum(headers, name)
        print("Create Fields Response:", fields_response)
        if not fields_response.get("id"):
            print("[X] Failed to create fields enum")
        else:
            print("[V] Fields enum created successfully")
    print("-------------------\n")

def get_fields_enum_test():
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    print("Getting all fields...")
    fields = get_fields_enums(headers)
    print("All Fields:", fields)
    if len(fields) == 4:
        print("[V] All fields fetched successfully")
    else:
        print("[X] Failed to fetch all fields")
    print("-------------------\n")


def create_blacklist_items_test():
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)

    fields = get_fields_enums(headers)

    blacklist = create_blacklist(headers, fields[0]['id'], "example.com")
    print("Create 1st Blacklist Response:", blacklist)
    if blacklist.get("id"):
        print("[V] 1st Blacklist created successfully")
    else:
        print("[X] 1st Failed to create blacklist")

    blacklist = create_blacklist(headers, fields[2]['id'], "SPF_IP1")
    print("Create 3rd Blacklist Response:", blacklist)
    if blacklist.get("id"):
        print("[V] 3rd Blacklist created successfully")
    else:
        print("[X] 3rd Failed to create blacklist")
    
    blacklist = create_blacklist(headers, fields[2]['id'], "SPF_IP2")
    print("Create 4th Blacklist Response:", blacklist)
    if blacklist.get("id"):
        print("[V] 4th Blacklist created successfully")
    else:
        print("[X] 4th Failed to create blacklist")
    print("-------------------\n")

def delete_blacklist_item_test():
    # create blacklist item
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    fields = get_fields_enums(headers)
    blacklist = create_blacklist(headers, fields[0]['id'], "example.com")
    print("Create Blacklist Response:", blacklist)
    if blacklist.get("id"):
        print("[V] Blacklist created successfully")
    else:
        print("[X] Failed to create blacklist")
    blacklist_id = blacklist.get("id")
    delete_blacklist = delete_blacklist_item(headers, blacklist_id)
    print("Delete Blacklist Response:", delete_blacklist)

def get_blacklist_items_test():
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    blacklists = get_blacklists_grouped(headers)
    print("All Blacklists grouped:\n", json.dumps(blacklists, indent=4))
    if len(blacklists) == 4:
        print("[V] All blacklists fetched successfully")
    else:
        print("[X] Failed to fetch all blacklists")
    print("-------------------\n")

def get_blacklist_items_list_test():
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    blacklists = get_blacklists(headers)
    print("All Blacklists:\n", json.dumps(blacklists, indent=4))
    if len(blacklists) == 4:
        print("[V] All blacklists fetched successfully")
    else:
        print("[X] Failed to fetch all blacklists")
    print("-------------------\n")

def set_poc_user(username = "poc@test.com", password = "poc", fullname = "poc"):
    user = test_create_user(username, password, fullname)
    if not user:
        print("[X] Failed to POC create user")
        return False
    
    print("[V] POC User created successfully, trying to login")

    headers = test_login(username, password)
    if not headers:
        print("[X] Failed to POC login")
        return False
    
    print("[V] POC User logged in successfully")
    print("-------------------\n")


def create_and_update_and_get_bulk_actions_test():
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    actions = [
        {
            "verdict_id": 1,
            "module_id": 1,
            "block": False,
            "alert": True
        },
        {
            "verdict_id": 2,
            "module_id": 1,
            "block": True,
            "alert": True
        },
        {
            "verdict_id": 3,
            "module_id": 1,
            "block": True,
            "alert": True
        },
        {
            "verdict_id": 1,
            "module_id": 2,
            "block": False,
            "alert": False
        },
        {
            "verdict_id": 2,
            "module_id": 2,
            "block": False,
            "alert": True
        },
        {
            "verdict_id": 3,
            "module_id": 2,
            "block": False,
            "alert": True
        },
        {
            "verdict_id": 1,
            "module_id": 3,
            "block": False,
            "alert": False
        },
        {
            "verdict_id": 2,
            "module_id": 3,
            "block": False,
            "alert": True
        },
        {
            "verdict_id": 3,
            "module_id": 3,
            "block": False,
            "alert": True
        }
    ]

    for action in actions:
        print("Creating action - ", action)
        action_response = create_action(headers, action["verdict_id"],  action["module_id"], action["block"], action["alert"])
        print("Create Action Response:", action_response)
        if not action_response.get("id"):
            print("[X] Failed to create action")
        else:
            print("[V] Action created successfully")

    print("Updating actions...")
    actions_response = update_actions_bulk(headers, actions)
    print("Create Bulk Actions Response:", actions_response)
    if actions_response.get("id"):
        print("[V] Bulk Actions created successfully")
    else:
        print("[X] Failed to create bulk actions")
    
    print("Getting all actions...")
    actions = get_actions(headers)
    print("All Actions:", actions)
    if len(actions) == 4:
        print("[V] All actions fetched successfully:")
        for action in actions:
            print("\t", action)
    else:
        print("[X] Failed to fetch all actions")
    print("-------------------\n")

def test_update_actions_bulk():
    updated_actions = [
        {   
            "id":8,
            "verdict_id": 2,
            "module_id": 3,
            "block": True,
            "alert": True
        },
        {
            "id": 9,
            "verdict_id": 3,
            "module_id": 3,
            "block": True,
            "alert": True
        }
    ]

    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    actions = get_actions(headers)
    for action in actions:
        print("Before updating action - ", action)
    
    actions = update_actions_bulk(headers, updated_actions)
    for action in actions:
        print("After updating action - ", action)
    
    print("-------------------\n")
    


def read_all_enums():
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    print("Reading all enums...")
    print("All Verdicts:", get_all_verdicts(headers))
    print("All Modules Types:", get_all_analysis_types(headers))
    print("All Fields:", get_fields_enums(headers))


def test_get_email_decision():
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    email_id = 1
    decision = get_email_decision(headers, email_id)
    print("for email_id:", email_id, "Decision:", "Block" if decision else "Allow")
    email_id = 2
    decision = get_email_decision(headers, email_id)
    print("for email_id:", email_id, "Decision:", "Block" if decision else "Allow")
    email_id = 3
    decision = get_email_decision(headers, email_id)
    print("for email_id:", email_id, "Decision:", "Block" if decision else "Allow")
    return decision

def test_update_module():
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)
    modules = get_all_analysis_types(headers)
    print("---------------Debugging-------------------")
    print("All Modules before update:")
    for module in modules:
        print(module)
    
    print("Before update: 2nd module.enabled: " , modules[1]['enabled'])
    module_id = modules[1]['id']
    enabled = not modules[1]['enabled']
    print("Updating module - ", module_id, enabled)
    module_response = update_module(headers, id=module_id, enabled=enabled)
    print("Update Module Response:", module_response)
    if module_response.get("id") and module_response.get("enabled") == enabled:
        print("[V] Module updated successfully")
    
    print("All Modules after update:")
    modules = get_all_analysis_types(headers)
    for module in modules:
        print(module)
    
    print("Reverting back to original state")
    enabled = not enabled
    print("Updating module - ", module_id, enabled)
    module_response = update_module(headers, id=module_id, enabled=enabled)
    print("Update Module Response:", module_response)
    if module_response.get("id") and module_response.get("enabled") == enabled:
        print("[V] Module updated successfully")

    print("---------------Debugging-------------------\n")

def test_big_data():
    headers = test_login(DETECTION_SERVER_USER_NAME, DETECTION_SERVER_USER_PASSWORD)



if __name__ == "__main__":
    # Defult to setup - 1 4 6 8 11 2 3 5 7 9 10 12 13 14 15
    print("\n\nRunning tests...\n\n")
    tests = sys.argv[1:]
    tests_map = [initial_setup, # 1
                advanced_search_test, # 2
                add_analysis_to_email, # 3
                create_fields_enum_test, # 4
                get_fields_enum_test, # 5
                create_blacklist_items_test, # 6
                get_blacklist_items_test, # 7
                set_poc_user, # 8
                delete_blacklist_item_test, # 9
                get_blacklist_items_list_test, # 10
                create_and_update_and_get_bulk_actions_test, # 11
                read_all_enums, # 12
                test_get_email_decision, # 13
                test_update_actions_bulk, # 14
                test_update_module, # 15
                test_big_data # 16
                ]
    
    if not tests:
        tests = ['1', '4', '6', '8', '11','16']

    for test in tests:
        if test.isdigit():
            test = int(test) - 1
            if test < len(tests_map):
                print(f"Running test name: {tests_map[test].__name__}")
                tests_map[test]()
            else:
                print(INVALID_TEST_NUMBER)
                print(AVAILABLE_TESTS)
                
        else:
            print(INVALID_TEST_NUMBER)
            print(AVAILABLE_TESTS)
            break
    
    set_poc_user(username="poc@user.com", password="POCPass123!", fullname="POC User")

    
# on module 1, verdict 2 - block
# on module 2, verdict 2 - alert