import os
LOGIN_NAME = os.getenv('LOGIN_NAME')
PASSWORD = os.getenv('PASSWORD')
SCHOOL_ID = os.getenv('SCHOOL_ID')
LENGTH = int(os.getenv('LENGTH'))

URL = "http://englishservice.siboenglish.com//MobService/index"
HEADER = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/3.12.12"
}
