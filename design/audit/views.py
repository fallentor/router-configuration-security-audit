import os
import json
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.paginator import Paginator    # 导入分页器
from . models import AuditResult
from . visualize import show_result
from device.models import Device
from tactic.models import Tactic
from device.ping_check import check_device_status
from audit.my_thrift.rpc_client import rpc_client_start
from audit.config_.audit_all import check_all_object
from django.template.loader import render_to_string

# Create your views here.


def audit_list(request):
	devices = Device.objects.all().order_by('pk')
	paginator = Paginator(devices, 6)    # 将设备列表数据分页，一页为6个数据
	page_num = request.GET.get('page', 1)    # 获取当前页码，默认为1
	page = paginator.get_page(page_num)    # 获取当前页的设备列表数据
	context = {'page': page}    # 定义上下文

	return render(request, 'audit_list.html', context)


def visualization(request):
	if request.method == 'POST':
		address = request.POST.get('address')
		latest_audit_result = AuditResult.objects.get(address=address)
	else:
		latest_audit_result = AuditResult.objects.last()
		address = latest_audit_result.address
		# 获取所有Address

	addresses = AuditResult.objects.values_list('address', flat=True).distinct()

	json_file = os.path.join(settings.BASE_DIR, 'static', 'audit_files', 'json_', f"{address}.json")
	context = show_result(json_file)
	context['address'] = address
	context['addresses'] = addresses
	context['auditResult'] = latest_audit_result
	return render(request, 'visualization.html', context)
	


def report_export(request):
	auditResults = AuditResult.objects.all().order_by('id')
	paginator = Paginator(auditResults, 6)    # 将设备列表数据分页，一页为6个数据
	page_num = request.GET.get('page', 1)    # 获取当前页码，默认为1
	page = paginator.get_page(page_num)    # 获取当前页的设备列表数据
	context = {'page': page}    # 定义上下文
	return render(request, 'report_export.html', context)


def export_configuration(request):
	if request.method == "POST":
		
		device_id = request.POST.get("device_id")
		device = Device.objects.get(id=device_id)
		device.node_status = check_device_status(device.node_ip)
		device.save()

		context = {"device": device}
		return render(request, "export.html", context)

	return render(request, 'empty_template.html')


def export(request):
	if request.method == "POST":
		device_id = request.POST.get("device_id")
		device = Device.objects.get(id=device_id)
		radioType = request.POST.get("radioType")
		upload_path = os.path.join(settings.BASE_DIR, 'static', 'audit_files')

		if radioType == "online":
			hostname = request.POST.get("hostname")
			username = request.POST.get("username")
			password = request.POST.get("password")
			input_file = os.path.join(upload_path, f"{device.node_ip}.txt")
			response_ = rpc_client_start(hostname, username, password, input_file)
			if response_.success:
				return JsonResponse({'status': 'success'})
			else:
				return JsonResponse({'status': 'error'})
				
		elif radioType == "offline":
			file = request.FILES['config-file']
			target_file_name = f"{device.node_ip}{os.path.splitext(file.name)[-1]}"
			
			with open(os.path.join(upload_path, target_file_name), 'wb+') as destination:
				for chunk in file.chunks():
					destination.write(chunk)
			return JsonResponse({'status': 'success'})

	return redirect(request, 'export_configuration')


def audit_(request):
	if request.method == "POST":
		device_id = request.POST.get("device_id")
		device = Device.objects.get(id=device_id)
		name = device.node_name
		address = device.node_ip
		config_path = os.path.join(settings.BASE_DIR, 'static', 'audit_files', f"{address}.txt")
		json_file = os.path.join(settings.BASE_DIR, 'static', 'audit_files', 'json_', f"{address}.json")
		try:
			with open(config_path, 'r', encoding='utf-8') as f:
				config = f.read()
			pattern = r'Building configuration'
			match = re.findall(pattern, config)
			if not match:
				raise Exception('This is not a config_path')

			check_all_object(config_path, json_file)
			if not AuditResult.objects.filter(sort_id=device_id).exists():
				auditResult = AuditResult.objects.create(sort_id=device_id, name=name, address=address,remark='已审计')

			return JsonResponse({'success': True})
		except Exception as e:
			return JsonResponse({'success': False})
		
	return render(request, 'empty_template.html')


def audit_result_show(request):
	if request.method == "POST":
		device_id = request.POST.get("device_id")
		auditResult = AuditResult.objects.get(sort_id=device_id)
		address = auditResult.address
		json_file = os.path.join(settings.BASE_DIR, 'static', 'audit_files', 'json_', f"{address}.json")
		with open(json_file, 'r', encoding='utf-8') as f:
			data = json.load(f)

		failed_ids = [item['id'] for item in data if not item['audit_result']]
		failed_tactics = Tactic.objects.filter(id__in=failed_ids)
		grouped_tactics = {'UM': [], 'OG': [], 'C': [], 'AC': []}

		for tactic in failed_tactics:
			grouped_tactics[tactic.tactic_group].append(tactic)

		grouped_tactics_list = [(key, value) for key, value in grouped_tactics.items()]

		flags = [['UM', '用户管理类'],['OG', '对象类'], ['C', '通信类'], ['AC', '访问控制类']]
		context = {
			'grouped_tactics_list': grouped_tactics_list,
			'auditResult': auditResult,
			'flags': flags	
		}

		content = render_to_string('show.html', context=context)
    
		filename = os.path.join(settings.BASE_DIR, 'static', 'audit_export', f"{address}.html")

	    # 将字符串写入文件中
		with open(filename, 'w', encoding='utf-8') as f:
			f.write(content)
		
		return render(request, 'show.html', context)


def delete_(request):
	if request.method == "POST":
		device_id = request.POST.get("device_id")
		try:
			auditResult = AuditResult.objects.get(sort_id=device_id)
			auditResult.delete()
			return JsonResponse({'status': True})
		except Exception as e:
			return JsonResponse({'status': False})




