import requests
import json
from environs import Env
env = Env()
env.read_env()
BASE_URL=f"{env.str('URL')}/api"

# Get Categories
def categories():
    try:
        response = requests.get(url=f"{BASE_URL}/category/")
        rest = json.loads(response.text)
        return rest
    except:
        return []

# Get Category's Test
def get_test(category,telegram_id=None):
       response = requests.get(url=f"{BASE_URL}/withcategory/{category}/{telegram_id}/")
       try:
           if response.status_code == 204:
               rest = []
           else:
               rest = json.loads(response.text)
           return rest
       except:
           return []
# Create user
def create_user(telegram_id,name=None):
    try:
        response = requests.post(url=f"{BASE_URL}/users/", data={'telegram_id': telegram_id, 'name': name})
        return response.status_code
    except:
        pass
# Get all users
def get_all_users():
    try:
        response = requests.get(url=f"{BASE_URL}/users/")
        data = json.loads(response.text)
        return data
    except:
        return []
# Test Done Users
def test_done(telegram_id,name,test_code,true_answers,false_answers):
   try:
       response = requests.post(url=f"{BASE_URL}/donetestcreate/",
                                data={'telegram_id': telegram_id, 'name': name, 'test_code': test_code,
                                      'true_answers': true_answers, 'false_answers': false_answers})
       return response.status_code
   except:
       pass
# Users' results
def results_of_test(telegram_id):
    try:
        response = requests.post(url=f"{BASE_URL}/gettestdone/", data={'telegram_id': telegram_id})
        data = json.loads(response.text)
        return data
    except:
        []
# Daily Test Status
def dailytest(telegram_id):
    response = requests.get(url=f"{BASE_URL}/daily/{telegram_id}/")
    return response.status_code
# Daily Test Create
def dailytestcreate(telegram_id,test_code):
    try:
        response = requests.post(url=f"{BASE_URL}/dailycreate/",
                                data={'telegram_id': telegram_id, 'test_code': test_code})

        return response.status_code
    except Exception as e:
        print(e)
# Delete Done Tests
def delete_done_test(telegram_id):
    try:
        response = requests.post(url=f"{BASE_URL}/deletedonetest/", data={"telegram_id": telegram_id})
    except:
        pass


