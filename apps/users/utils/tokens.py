import hashlib
import time
from django.http import Http404
from root.settings import SECRET_KEY, TOKEN_EXPIRATION_TIME


def generate_one_time_link(user):
    if user.used_token:
        raise Http404
    user.used_token = True
    user.save()
    user_id = int_to_base36(user.id)
    last_login = int_to_base36(int(user.last_login.timestamp() if user.last_login else 'Null'))
    date_joined = int_to_base36(int(user.date_joined.timestamp()))
    current_time = int_to_base36(int(time.time()))
    data = f"{current_time}-{user_id}-{last_login}-{date_joined}-{SECRET_KEY}"
    token = hashlib.sha256(data.encode()).hexdigest()
    return f'{user_id}-{token}-{current_time}'


def validate_one_time_link(user, token, created_at_token):
    if not user.used_token:
        return False
    user.used_token = False
    user.save()
    user_id = int_to_base36(user.id)
    last_login = int_to_base36(int(user.last_login.timestamp() if user.last_login else 'Null'))
    date_joined = int_to_base36(int(user.date_joined.timestamp()))
    now = int(time.time())
    if now > (base36_to_int(created_at_token) + TOKEN_EXPIRATION_TIME):
        return False
    data = f"{created_at_token}-{user_id}-{last_login}-{date_joined}-{SECRET_KEY}"
    expected_token = hashlib.sha256(data.encode()).hexdigest()
    return token == expected_token


def int_to_base36(num: int) -> str:
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'

    result = ''

    while num > 0:
        num, remainder = divmod(num, 36)
        result = chars[remainder] + result

    return result


def base36_to_int(base36_str) -> int:
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'

    result = 0

    for char in str(base36_str):
        digit = chars.index(char)
        result = result * 36 + digit

    return result
