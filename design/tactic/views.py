from django.shortcuts import render, redirect
from django.http import JsonResponse
from . models import TacticRemarks, Tactic
from django.core.paginator import Paginator    # 导入分页器
# Create your views here.

def tacticGroup_list(request):

	tactic_remarks_data = TacticRemarks.objects.all()
	context = {"tactic_remarks_data": tactic_remarks_data}

	return render(request, 'tacticGroup_list.html', context)


def tactic_list(request):
	tactics = Tactic.objects.all().order_by("id")
	paginator = Paginator(tactics, 6)    # 将设备列表数据分页，一页为6个数据
	page_num = request.GET.get('page', 1)    # 获取当前页码，默认为1
	page = paginator.get_page(page_num)    # 获取当前页的设备列表数据
	context = {"page": page}
	return render(request, 'tactic_list.html', context)


def delete_tactic_group(request):
	if request.method == 'POST':
		tactic_remark_id = request.POST.get("tactic_remark_id")
		tactic = TacticRemarks.objects.get(id=tactic_remark_id)
		tactic_group = tactic.tactic_group
		# print(tactic_group)
		tactic.delete()

		# 删除 Tactic 中 tactic_group=tactic_group 的 所有策略的信息
		# Tactic.objects.filter(tactic_group=tactic_group).delete()
		
		return redirect('tacticGroup_list')

	# 如果不是POST请求，则渲染空白模板以避免错误
	return render(request, 'empty_template.html')

def delete_tactic(request):
	if request.method == 'POST':
		tactic_id = request.POST.get("tactic_id")
		tactic = Tactic.objects.get(id=tactic_id)
		tactic.delete()

		return redirect('tactic_list')

	return render(request, 'empty_template.html')


def tactic_edit(request):
	if request.method == "POST":
		tactic_id = request.POST.get("tactic_id")
		tactic = Tactic.objects.get(id=tactic_id)
		context = {"tactic": tactic}
		return render(request, "tactic_edit.html", context)

	return render(request, 'empty_template.html')

def edit_tactic(request):
	if request.method == "POST":
		risk_level = request.POST.get('risk_level')
		tactic_remarks = request.POST.get('tactic_remarks')
		risk_description = request.POST.get('risk_description')
		edit_suggestion = request.POST.get('edit_suggestion')

		# 当以上四个字段都为空时，返回错误信息
		if not(risk_level or tactic_remarks or risk_description or edit_suggestion):
			return JsonResponse({'status': 'error', 'msg': '修改字段为空，无需修改'})  # 返回错误响应 

		id = request.POST.get('tactic_id')
		tactic = Tactic.objects.get(id=id)

		if risk_level:
			if risk_level in ['低级', '中级']:
				tactic.risk_level = risk_level
			else:
				return JsonResponse({'status': 'error', 'msg': '风险等级值不合法'})  # 返回错误响应
		if tactic_remarks:
			tactic.tactic_remarks = tactic_remarks
		if risk_description:
			tactic.risk_description = risk_description
		if edit_suggestion:
			tactic.edit_suggestion = edit_suggestion

		tactic.save()
		
		return JsonResponse({'status': 'success', 'msg': '修改更新完成！'})
	else:
		return render(request, 'tactic_edit.html')