from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class TacticGroup(models.TextChoices):
    """策略组枚举类型"""
    USER_MANAGEMENT = 'UM', _('用户管理类')
    OBJECT_GROUP = 'OG', _('对象类')
    COMMUNICATION = 'C', _('通信类')
    ACCESS_CONTROL = 'AC', _('访问控制类')

class Tactic(models.Model):
    """策略模型"""
    id = models.AutoField(primary_key=True)
    tactic_group = models.CharField(
        max_length=2,
        choices=TacticGroup.choices,
        verbose_name='策略组'
    )
    tactic_name = models.CharField(
        max_length=50,
        verbose_name='策略名称'
    )
    risk_level = models.CharField(
        max_length=2,
        choices=(('L', '低级'), ('M', '中级')),
        verbose_name='风险等级',
    )
    tactic_remarks = models.CharField(
        max_length=100,
        verbose_name='策略备注',
    )
    risk_description = models.CharField(
        max_length=200,
        verbose_name='策略风险描述',
    )
    edit_suggestion = models.CharField(
        max_length=100,
        verbose_name='修改建议',
    )

    class Meta:
        verbose_name = '策略'
        verbose_name_plural = '策略'

    def __str__(self):
        return self.tactic_name


class TacticRemarks(models.Model):
    """策略备注模型"""
    id = models.AutoField(primary_key=True)
    tactic_group = models.CharField(
        max_length=2,
        choices=TacticGroup.choices,
        verbose_name='策略组'
    )
    remarks = models.CharField(
        max_length=30,
        verbose_name='备注',
    )

    class Meta:
        verbose_name = '策略备注'
        verbose_name_plural = '策略备注'

    def __str__(self):
        return self.remarks


# 插入实例

# TacticRemarks.objects.create(
#     id=4,
#     tactic_group=TacticGroup.ACCESS_CONTROL.value,   # 设置值为 'access_control'
#     remarks='策略组：访问控制类',
# )

# 查找实例
# tactic_remarks_objs = TacticRemarks.objects.all()
# for obj in tactic_remarks_objs:
#     print(f'id: {obj.id}, tactic_group: {obj.get_tactic_group_display()}, remarks: {obj.remarks}')



# for obj in test:
#     print(f'id:{obj.id}, tactic_group:{obj.get_tactic_group_display()}, tactic_name:{obj.tactic_name}, risk_level:{obj.risk_level}, tactic_remarks:{obj.tactic_remarks}, risk_description:{obj.risk_description}, edit_suggestion:{obj.edit_suggestion}')