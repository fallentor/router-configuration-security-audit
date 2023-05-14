from django.shortcuts import render, redirect
from . models import Device
from django.utils import timezone
from django.core.paginator import Paginator    # 导入分页器
from django.http import JsonResponse, HttpResponseBadRequest
from datetime import datetime
from . ping_check import check_device_status
# Create your views here.


def device_list_view(request):

	return render(request, 'device_list.html')



def device(request):
	devices = Device.objects.all().order_by('last_checked')    # 获取设备列表
	paginator = Paginator(devices, 6)    # 将设备列表数据分页，一页为6个数据
	page_num = request.GET.get('page', 1)    # 获取当前页码，默认为1
	page = paginator.get_page(page_num)    # 获取当前页的设备列表数据
	context = {'page': page}    # 定义上下文

	return render(request, 'device.html', context)    # 渲染模板并将上下文传递给模板


def delete_device(request):
    if request.method == 'POST':
        device_id = request.POST.get('device_id')
        device = Device.objects.get(id=device_id)
        device.delete()
        
        # 重定向到设备列表页面
        return redirect('device')

    # 如果不是POST请求，则渲染空白模板以避免错误
    return render(request, 'empty_template.html')


def device_add(request):

	return render(request, 'device_add.html')


def add_device(request):
    if request.method == 'POST':
        node_name = request.POST.get('node_name')
        node_ip = request.POST.get('node_ip')
        node_status = request.POST.get('node_status')
        
        node_status = check_device_status(node_ip)
        try:
            last_checked = datetime.strptime(request.POST.get('last_checked'), '%Y-%m-%dT%H:%M')
        except ValueError as e:
            return JsonResponse({'status': 'error', 'msg': '时间格式不正确，请按照YYYY-MM-DDTHH:MM:SS格式输入！'})
        remark = request.POST.get('remark')
       
        # 查询是否存在相同的 IP
        if Device.objects.filter(node_ip=node_ip).exists():
            return JsonResponse({'status': 'error', 'msg': '该 IP 地址已存在，请勿重复添加！'})

        # 不存在相同的 IP，创建新设备记录并保存到数据库
        device = Device(node_name=node_name, node_ip=node_ip, node_status=node_status, last_checked=last_checked, remark=remark)
        device.save()
        return JsonResponse({'status': 'success', 'msg': '添加设备成功！'})
    else:
        return render(request, 'device_add.html')



def search_device(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword', None)
        status = request.POST.get('status', None)

        # 组合查询条件
        filter_conditions = {}
        if keyword:
            filter_conditions['node_ip'] = keyword
        if status:
            filter_conditions['node_status'] = status

        # 查询Device对象列表
        devices = Device.objects.filter(**filter_conditions)

        # 分页：每页显示10条数据
        per_page_count = 6
        paginator = Paginator(devices, per_page_count)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        # 渲染模板
        return render(request, 'test.html', {'page': page})

    else:
        return redirect('device')