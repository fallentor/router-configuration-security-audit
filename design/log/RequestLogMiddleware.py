from datetime import datetime
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from . models import RequestLog  # 假设您的日志模型名称为 RequestLog

class RequestLogMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):

        RequestLog.objects.all().delete()
        # 获取请求信息
        if isinstance(request, HttpRequest) and request.method in ['GET', 'POST']:
            # 获取请求信息
            request_url = 'http://127.0.0.1:8000' + request.path
            user_agent = request.META.get('HTTP_USER_AGENT', '')


        if 'login' in request_url:
            # 如果该属性存在，则表示用户是第一次登录
            is_logged_in_first_time = True
        else:
            is_logged_in_first_time = False
        
        
        log_record = RequestLog(request_method=request.method, request_url=request_url,
                                user_agent=user_agent, is_logged_in_first_time=is_logged_in_first_time)
        log_record.save()
