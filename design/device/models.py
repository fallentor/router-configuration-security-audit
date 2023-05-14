from django.db import models

# Create your models here.


class Device(models.Model):
    NODE_STATUS_CHOICES = (
        ('online', '在线'),
        ('offline', '离线')
    )
    node_name = models.CharField(max_length=20)
    node_ip = models.CharField(max_length=20)
    node_status = models.CharField(choices=NODE_STATUS_CHOICES, max_length=10)
    last_checked = models.DateTimeField()
    remark = models.CharField(max_length=20)

    def __str__(self):
        # 显示对象名称
        return self.node_name

    @staticmethod
    def add_device(node_name, node_ip, node_status, last_checked, remark):
        """
        添加设备
        :param node_name: 设备名称
        :param node_ip: 设备 IP 地址
        :param node_status: 设备状态
        :param last_checked: 最后检查时间
        :param remark: 备注
        :return: 新增的设备的 ID 号
        """
        device = Device(
            node_name=node_name,
            node_ip=node_ip,
            node_status=node_status,
            last_checked=last_checked,
            remark=remark
        )
        device.save()
        return device.id

    @staticmethod
    def delete_device(device_id):
        """
        删除设备
        :param device_id: 设备的 ID 号
        :return: 是否删除成功（True/False）
        """
        try:
            device = Device.objects.get(id=device_id)
            device.delete()
            return True
        except Device.DoesNotExist:
            return False

    @staticmethod
    def update_device(device_id, **kwargs):
        """
        更新设备
        :param device_id: 设备的 ID 号
        :param kwargs: 需要更新的字段对应的值
        :return: 是否更新成功（True/False）
        """
        try:
            device = Device.objects.get(id=device_id)
            for key, value in kwargs.items():
                setattr(device, key, value)
            device.save()
            return True
        except Device.DoesNotExist:
            return False

    @staticmethod
    def get_all_devices():
        """
        获取所有设备列表
        :return: 设备列表
        """
        devices = Device.objects.all()
        return devices

    @staticmethod
    def get_device_by_id(device_id):
        """
        根据 ID 获取设备信息
        :param device_id: 设备的 ID 号
        :return: 设备信息
        """
        try:
            device = Device.objects.get(id=device_id)
            return device
        except Device.DoesNotExist:
            return None
