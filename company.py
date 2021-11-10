from bottle import run, get, view, post, request
import json
import jwt
import requests
import random

##############################


@get("/company")
@view("index_company.html")
def do():
    return dict(company_name="SUPER")


@get("/company-token")
@view("index_company_token.html")
def do():
    return dict(company_name="Token stuff")


@get("/company-twoAuth")
@view("index_company_twoAuth.html")
def do():
    return dict(company_name="twoAuth")


@post("/get-name-by-cpr")
def do():
    # Connect to db
    # Execute a SQL/Document query
    data_from_client = json.load(request.body)
    print("cpr", data_from_client)
    cpr = data_from_client['cpr']
    file_name = "./data/" + cpr + ".txt"
    opened_file = open(file_name, "r")
    read_file = opened_file.read()
    print(read_file)
    return read_file


num = random.randint(1000, 9999)


# Here we process the jwt-token
@post("/process-jwt-token")
def do():
    result = ""
    send_sms(num)
    try:
        # Here we load the jwt-token from https://ecuaguia.com/nemid.php.
        token = json.load(request.body)["jwt"]
        try:
            # Here we decode the token.
            result = jwt.decode(
                token, "jwt-secret-key", algorithms=["HS256"])
        except Exception as jwt_error:
            send_sms(jwt_error)

        try:
            # Here we check if email exist.
            if(result["email"] != None):
                print("great")
        except Exception as emailException:
            send_sms("Email missing")

    except Exception as json_error:
        send_sms(json_error)

    return str(result)


def send_sms(message):
    endpoint = "https://fatsms.com/send-sms"
    phone = "40956619"
    my_api_key = "50af23a4-4ed0-4fa0-a3de-448a961f602f"
    data_dict = {"to_phone": phone, "api_key": my_api_key, "message": message}
    requests.post(endpoint, data=data_dict)

    for x in range(2, -1, -1):

        code = int(input("Enter Code: "))
        if (code == num):
            print("welcome to the website")
            break
        else:
            print("You have " + str(x) + " tries left, try again")

    print(str(data_dict))


##############################
run(host="127.0.0.1", port=4444, debug=True, reloader=True, server="paste")
