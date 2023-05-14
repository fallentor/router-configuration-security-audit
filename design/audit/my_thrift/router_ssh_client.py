import paramiko

class RouterSshClient:
    def __init__(self, hostname, username, password, input_file):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.input_file = input_file
        self.client = None
    
    def connect(self):
        # 创建 SSH 客户端对象
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 连接到远程路由器
        self.client.connect(self.hostname, username=self.username, password=self.password, allow_agent=False, look_for_keys=False)
    
    def disconnect(self):
        # 关闭 SSH 连接
        if self.client is not None and self.client.get_transport().is_active():
            self.client.close()
            self.client = None

    def get_running_config(self):
        # 执行 show running-config 命令，并获取输出
        stdin, stdout, stderr = self.client.exec_command('show running-config')
        output = stdout.read().decode()

        # 将输出保存至指定的文件中
        with open(self.input_file, mode='w', encoding='utf-8') as file:
            file.write(output)

        return output