import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()

def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json

def test_login_system():
    # PASSING CONDITION
    user_json = {"user_email": "app123@gmail.com", "user_password": "ericiscool"}
    resp = TEST_CLIENT.post(ep.LOGIN_SYSTEM, json=user_json)
    assert resp.status_code == 200
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "PASSED" in resp_json["SYSTEM_STATUS"]

    # FAILING CONDITION
    user_json = {"user_email": "FAKE_ACCOUNT@gmail.com", "user_password": "FAKE_ACCOUNT"}
    resp = TEST_CLIENT.post(ep.LOGIN_SYSTEM, json=user_json)
    assert resp.status_code == 200
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

    # Make sure email and passwords are strings
    user_json = {"user_email": 21412, "user_password": 1231242}
    resp = TEST_CLIENT.post(ep.LOGIN_SYSTEM, json=user_json)
    assert resp.status_code == 406
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

    # Wrong JSON data
    user_json = {"WRONG_USER": "example@gmail.com", "WRONG_PASSWORD": "example"}
    resp = TEST_CLIENT.post(ep.LOGIN_SYSTEM, json=user_json)
    assert resp.status_code == 406
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

    # No JSON data
    user_json = {}
    resp = TEST_CLIENT.post(ep.LOGIN_SYSTEM, json=user_json)
    assert resp.status_code == 406
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]


