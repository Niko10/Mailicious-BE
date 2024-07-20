# Mailicious-BE
Backend for Mailicious Product

1. Create venv - `python -m venv venv`
2. Use your venv 
3. Install the reqs - `pip install -r requirments.txt`
4. run the server - `uvicorn app.main:app`
5. browse http://127.0.0.1:8000/docs#/
6. You should see that page:

![alt text](image.png)

# API Calls
### If no user exist yet use this to create your first:
```
curl -X 'POST' 'http://127.0.0.1:8000/users/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"email": "oriori@example.com","full_name": "ori hadad","is_active": true,"password": "1234"}'
```

### Then login:
```
curl -X POST "http://127.0.0.1:8000/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=oriori@example.com&password=1234"
```

You will get something like this as a response
```
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvcmlvcmlAZXhhbXBsZS5jb20iLCJleHAiOjE3MTkwNTMxMjR9.eCqVhXT9kU0YUoz7vw1MlxgVnwGHLhI10r0oCLLn8_A","token_type":"bearer"}
```

### Then use the access token in every request like this one:

```
curl -X GET "http://127.0.0.1:8000/users/1" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvcmlvcmlAZXhhbXBsZS5jb20iLCJleHAiOjE3MTkwNTMxMjR9.eCqVhXT9kU0YUoz7vw1MlxgVnwGHLhI10r0oCLLn8_A"
```

And you will get the response:
```
{"email":"user@example.com","full_name":"string","is_active":true,"id":1}%
```


### Easy

<br>

# Even easier? checkout examples/1.py and see 'copy & paste' code to consume the api from your python code
* It contains 2 functions: 
    - 'example_1()' - show general usage of some of the apis 
    - 'initial_setup_example()' - set up initial use of the api and db. It will resulted with this data:
    ## users table
    ![alt text](image-1.png)

    ## enum_verdicts table
    ![alt text](image-2.png)

    ## enum_modules table
    ![alt text](image-3.png)

    ## emails table
    ![alt text](image-4.png)

    ## users table
    ![alt text](image-5.png)