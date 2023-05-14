from django.shortcuts import render
from django.core.paginator import Paginator 
from . models import RequestLog

# Create your views here.


def log_view(request):

    #从数据库获取log信息并分页
    logs = RequestLog.objects.all().order_by('-timestamp')
    paginator = Paginator(logs, 6)
    
    page_number = request.GET.get('page')
    # try:
    #     request_log_list = paginator.page(page_number)
    # except PageNotAnInteger:
    #     request_log_list = paginator.page(1)
    # except EmptyPage:
    #     request_log_list = paginator.page(paginator.num_pages)
    page_obj = paginator.get_page(page_number)

    context = {
        'logs': page_obj.object_list,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'username': request.user.username
    }
    

    #使用Bootstrap对页面进行美化渲染
    return render(request, 'log.html', context)