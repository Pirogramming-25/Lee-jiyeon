from functools import wraps
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect


def model_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        # 로그인 페이지로 보내되 next + required=1 을 붙임
        query = urlencode({"next": request.path, "required": "1"})
        return redirect(f"{settings.LOGIN_URL}?{query}")

    return wrapper