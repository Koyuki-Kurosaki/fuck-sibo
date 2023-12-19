import json
import requests
from datetime import datetime
import date_format_string
from config import *


# 请求中ts作用未知， 2 为抓包结果
def login(login_name, password, school_id="7fffb34f4e254b34a056448cd86c7d53", app_version="4.5.0"):
    """
    :param login_name:
    :param password:
    :param school_id: 学校id  默认为聊城大学
    :param app_version: 思博英语app版本 作用未知
    :return: user_id
    """

    parm = {
        "schoolID": school_id,
        "loginName": login_name,
        "password": password,
        "ts": 2,
        "appVersion": app_version
    }
    print(str(parm))
    data = {
        "jyh": "4002_01",
        "parm": str(parm),
        "sign": "",
        "ts": ""
    }

    req = requests.post(URL, headers=HEADER, data=data)
    req_data = json.loads(req.json()['result'])
    print(req_data['Data']['DeptID'])
    return req_data['Data']['ID']


def get_teacher_id(user_id):
    parm = {
        "userID": user_id,
        "ts": "2"
    }
    data = {
        "jyh": 1001,
        "parm": str(parm),
        "sign": "",
        "ts": ""
    }

    req = requests.post(URL, headers=HEADER, data=data)
    req_data = req.json()["result"]  # Json String
    req_data = json.loads(req_data)
    return req_data["Data"][0]["ClassID"]


def get_essay_ids(user_id, class_id, start_page=0, length=2147483647, grade=0):
    parm = {
        "keyWord": "",
        "eassyType": "",
        "grade": grade,
        "orderType": 1,
        "pageStart": start_page,
        "pageSize": length,
        "ts": 2,
        "userID": user_id,
        "classID": class_id
    }
    print(str(parm))
    data = {
        "jyh": 2002,
        "parm": str(parm),
        "sign": "",
        "ts": ""
    }

    req = requests.post(URL, headers=HEADER, data=data)

    req_data = req.json()["result"]
    req_data = json.loads(req_data)
    return [essay["EssayID"] for essay in req_data['Data']]


def get_essay_answer(essay_id):
    parm = {
        "essayID": essay_id
    }
    data = {
        "jyh": 2009,
        "parm": str(parm),
        "sign": "",
        "ts": ""
    }

    req = requests.post(URL, headers=HEADER, data=data)

    req_data = req.json()['result']
    req_data = json.loads(req_data)
    return "".join([
        f"{test['TestItemNumber']}-{test['Answer']};"
        for test in req_data['Data']
    ])[:-1]


def submit_test(essay_id, user_id, class_id, answer, create_time=datetime.now().replace(microsecond=0).isoformat()):
    parm = {
        "essayID": essay_id,
        "userID": user_id,
        "classID": class_id,
        "createTime": create_time,
        "itemResult": answer
    }
    data = {
        "jyh": 2010,
        "parm": str(parm),
        "sign": "",
        "ts": ""
    }
    print(f"{essay_id}: {data}")
    req = requests.post(URL, headers=HEADER, data=data)
    print(f"{essay_id}: {req.json()}")
    return json.loads(req.json()["result"])["Code"] == "1"


if __name__ == "__main__":
    USERID = login(LOGIN_NAME, PASSWORD)
    teacher_id = get_teacher_id(USERID)
    essay_ids = get_essay_ids(USERID, teacher_id)
    # 设置起始日期和结束日期
    start_date = datetime(2024, 1, 20)
    end_date = datetime(2027, 7, 31)
    # 创建迭代器实例
    date_iterator = date_format_string.DateIterator(start_date, end_date)
    i = 0
    j = 0

    while i < 2 and j < len(essay_ids):
        if submit_test(essay_ids[j], USERID, teacher_id, get_essay_answer(essay_ids[j])):
            i += 1
        j += 1
