import re
import json
from audit.config_.config_handler import format_port, format_ip

def make_audit_data(id, tactic_group, tactic_name, risk_level, audit_result):
    data = {
        "id": id,
        "tactic_group": tactic_group,
        "tactic_name": tactic_name,
        "risk_level": risk_level,
        "audit_result": audit_result
    }
    return data


class Audit:
    def __init__(self, config_path, json_file):
        self.config_path = config_path
        self.json_file = json_file

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = f.read()

        self.json_data = []
    

    def save_data_in_json(self, data):
        self.json_data.append(data)
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.json_data, f, ensure_ascii=False, indent=4)


    def check_max_admin_sessions(self):
        max_admin_pattern = r'aaa\s+new-model[\s\S]*aaa\s+max-sessions\s+(\d+)'
        max_admin_match = re.search(max_admin_pattern, self.config)

        if max_admin_match:
            max_admin_num = int(max_admin_match.group(1))
            if max_admin_num <= 5:
                audit_result = True
            else:
                audit_result = False
        else:
            max_admin_num = 0
            audit_result = False

        data = make_audit_data(
            1,
            "UM",
            "管理员最大在线人数检测",
            "低级",
            audit_result
        )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)


    def check_failed_login_attempts(self):
        failed_login_pattern = r"login block-for (\d+) attempts (\d+) within (\d+)"
        failed_login_match = re.search(failed_login_pattern, self.config)

        if failed_login_match:
            max_attempts = int(failed_login_match.group(2))
            time_window = int(failed_login_match.group(3))
            if max_attempts < 5 and time_window <= 2:
                audit_result = True
            else:  
                audit_result = False
        else:
            max_attempts = 0
            audit_result = False

        data = make_audit_data(
            2,
            "UM",
            "用户登录失败次数检测",
            "中级",
            audit_result
        )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)


    def check_user_timeout_disconnect(self):
        timeout_pattern = r"exec-timeout (\d+)"
        timeout_match = re.search(timeout_pattern, self.config)

        if timeout_match:
            timeout = int(timeout_match.group(1))
            if timeout >= 1 and timeout <= 15:
                audit_result = True
            else:
                audit_result = False
        else:
            audit_result = False

        data = make_audit_data(
            3,
            "UM",
            "用户超时断连检测",
            "低级",
            audit_result
        )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)


    def check_detect_console_auth(self):
        # 通过正则表达式匹配控制台用户登录验证方式
        pattern = r'line\s+console.+(?:\n.*?)*?login\s+(.*?)\n'
        match = re.search(pattern, self.config)

        if match:
            login_type = match.group(1)
            aaa_pattern = r'aaa\s+authentication\s+login\s+(default|local|group\s+\S+)'

            aaa_match = re.search(aaa_pattern, self.config)

            # 如果 aaa 认证已经启用，设置审计结果为 True，否则为 False
            if aaa_match:
                audit_result = True
            else: 
                audit_result = False
        else:
            audit_result = False

        data = make_audit_data(
            4,
            "UM",
            "console用户登录验证方式检测",
            "低级",
            audit_result
        )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)


    def check_vty_login(self):
        # 通过正则表达式查找 vty 登录验证方式
        pattern = r'line\s+vty\s+.+(?:\n.*?)*?(?:(transport\s+input\s+(?:ssh|telnet)(?:\s+|$))|)login\s+(.*?)\n'
        match = re.search(pattern, self.config)

        if match:
            login_type = match.group(1)
            aaa_pattern = r'aaa\s+authentication\s+login\s+(default|local|group\s+\S+)'
            aaa_match = re.search(aaa_pattern, self.config)

            # 如果 aaa 认证已经启用，设置审计结果为 True，否则为 False
            if aaa_match:
                audit_result = True
            else: 
                audit_result = False
        else:
            audit_result = False

        data = make_audit_data(
            5,
            "UM",
            "vty用户登录验证方式检测",
            "中级",
            audit_result
        )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)


    def check_telnet_service(self):
        # 通过正则表达式匹配 telnet 服务是否在配置中开启
        pattern = r'line\s+vty\s+.+(?:\n.*?)*?transport\s+input\s+(.*)'
        match = re.search(pattern, self.config)

        # 如果找到相应行，并且其中包含关键字“telnet” ，设置审计结果为 False，否则为 True
        if match:
            transport_input = match.group(1)
            if 'telnet' in transport_input.lower():
                audit_result = False
            else:
                audit_result = True

        # 如果没有找到相应行，说明未开启 Telnet 服务
        else:
            audit_result = True

        data = make_audit_data(
            10,
            'C',
            'telnet服务检测',
            '中级',
            audit_result
        )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)


    def check_ssh_ip_limit(self):
        # 通过正则表达式匹配 vty 行中的输入传输模式`transport input`
        pattern = r'\s*line\s+vty\s+.+(?:\n.*?)*?transport\s+input\s+(.*?)(?:\n.*?)*?(?=.*?access-class\s+\d+\s+in)'
        match = re.search(pattern, self.config)

        if match:
            transport_input = match.group(1)
            if 'ssh' in transport_input.lower():
                audit_result = True
            else:
                audit_result = False
        else:
            audit_result = False

        data = make_audit_data(
            11,
            'C',
            'ssh IP限制检测',
            '低级',
            audit_result
        )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)


    def check_snmp_status(self):
        pattern = r'^\s*snmp-server\s+(?:\n.*?)*'
        match = re.search(pattern, self.config, re.MULTILINE)

        if match:
            audit_result = False
        else:
            audit_result = True

        data = make_audit_data(
            12,
            'C',
            'snmp服务检测',
            '中级',
            audit_result
        )

        self.save_data_in_json(data)


    def check_web_security(self):
    
        pattern = r'^\s*ip\s+http\s+server'
        match = re.search(pattern, self.config, re.MULTILINE)

        if match:
            https_pattern = r'^\s*ip\s+http\s+secure-server'
            https_match = re.search(https_pattern, self.config, re.MULTILINE)
            if https_match:
                audit_result = True
            else:
                audit_result = False
        else:
            audit_result = True

        data = make_audit_data(
            13,
            'C',
            'web服务安全检测',
            '低级',
            audit_result
        )
        
        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)


    def check_empty_service_objects(self):
        """
        检测配置文件中是否存在空服务对象组（Service Objects）。
        如果不存在空服务对象组，则将审计结果设置为 True，并更新 JSON 数据；
        否则将审计结果设置为 False，并更新 JSON 数据。
        """
        pattern = r'^\s*ip\s+access-list\s+extended'
        match = re.findall(pattern, self.config, re.MULTILINE)

        if match:
            d_pattern = r'\s*ip\s+access-list\s+extended\s+\S+(?:\n.*?)*?\s*(?:permit|deny)\s+'
            d_match = re.findall(d_pattern, self.config)
            if d_match:
                audit_result = True
            else:
                audit_result = False
        else:
            audit_result = True

        data = make_audit_data(
                6,
                'OG',
                '空服务对象组检测',
                '低级',
                audit_result
            )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)


    def check_service_og_redundancy(self):
        tuples = []
        acl_pattern = r"ip access-list extended \S+([\s\S]*?)\n!"
        acl_result = re.findall(acl_pattern, self.config, re.DOTALL)
        if acl_result:
            for acl in acl_result:
                pattern = r'(?:permit|deny)\s+(\S+)\s+((?:host\s+\S+)|any)\s+((?:host\s+\S+)|any)\s+((?:eq|neq)\s+\w+|(?:range(?:\s+\d+){2})|(?:gt|lt)\s+\S+|\S+)'
                match = re.findall(pattern, acl)
                if match:
                    for m in match:
                        tuples.append((m[0], format_ip(m[1]), format_ip(m[2]), format_port(m[3])))
                    tuples_set = set(tuples)
                    if len(tuples_set) != len(tuples):
                        audit_result = False
                    else:
                        audit_result = True
                else:
                    audit_result = True
        else:
            audit_result = True

        data = make_audit_data(
                7,
                'OG',
                '服务对象组冗余检测',
                '中级',
                audit_result
            )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)



    def check_address_og_redundancy(self):
        tuples = []
        acl_pattern = r"ip access-list extended \S+([\s\S]*?)\n!"
        acl_result = re.findall(acl_pattern, self.config, re.DOTALL)
        if acl_result:
            for acl in acl_result:
                pattern = r'(?:permit|deny)\s+(\S+)\s+((?:host\s+\S+)|any)\s+((?:host\s+\S+)|any)\s+((?:eq|neq)\s+\w+|(?:range(?:\s+\d+){2})|(?:gt|lt)\s+\S+|\S+)'
                match = re.findall(pattern, acl)
                if match:
                    for m in match:
                        tuples.append((format_ip(r[1]), format_ip(m[2])))
                    tuples_set = set(tuples)
                    if len(tuples_set) != len(tuples):
                        audit_result = False
                    else:
                        audit_result = True
                else:
                    audit_result = True
        else:
            audit_result = True

        data = make_audit_data(
                8,
                'OG',
                '地址对象组冗余检测',
                '低级',
                audit_result
            )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)


    def check_custom_service_redundancy(self):
        tuples = []
        acl_pattern = r"ip access-list extended \S+([\s\S]*?)\n!"
        acl_result = re.findall(acl_pattern, self.config, re.DOTALL)
        if acl_result:
            for acl in acl_result:
                pattern = r'(?:permit|deny)\s+(\S+)\s+((?:host\s+\S+)|any)\s+((?:host\s+\S+)|any)\s+((?:eq|neq)\s+\w+|(?:range(?:\s+\d+){2})|(?:gt|lt)\s+\S+|\S+)'
                match = re.findall(pattern, acl)
                if match:
                    for m in match:
                        tuples.append((m[0], format_port(m[1])))
                    tuples_set = set(tuples)
                    if len(tuples_set) != len(tuples):
                        audit_result = False
                    else:
                        audit_result = True
                else:
                    audit_result = True
        else:
            audit_result = True

        data = make_audit_data(
                9,
                'OG',
                '自定义服务冗余检测',
                '中级',
                audit_result
            )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)    


    def check_all(self):

        # audit = Audit('running-config.txt', 'audit.json')
        self.check_max_admin_sessions()
        self.check_failed_login_attempts()
        self.check_user_timeout_disconnect()
        self.check_detect_console_auth()
        self.check_vty_login()
        self.check_empty_service_objects()
        self.check_service_og_redundancy()
        self.check_address_og_redundancy()
        self.check_custom_service_redundancy()
        self.check_telnet_service()
        self.check_ssh_ip_limit()
        self.check_snmp_status()
        self.check_web_security()
        


# d_pattern = r'\s*ip\s+access-list\s+extended\s+\S+(?:\n.*?)*?\s*(?:permit|deny)\s+'
# d_match = re.findall(d_pattern, 'ip access-list extended aa-bb\n permit tcp any any eq 80')
# print(d_match)

# d_pattern = r'\s*ip\s+access-list\s+extended\s+\S+(?:\n.*?)*?\s*(?:permit|deny)\s+'
# d_match = re.findall(d_pattern, 'ip access-list extended aa-bb\n\ndeny tcp any any eq 80')
# print(d_match)

# tuples = []
# pattern = r'\s*ip\s+host\s+(\S+)\s+(\S+)'
# match = re.findall(pattern, 'ip host a 11\nip host b 192.168.0.1\nip host c 70\n ip host d 127.0.0.1\nip host a 11')
# for m in match:
#     tuples.append(m)

# tuples_set = set(tuples)
# if len(tuples_set) != len(tuples):
#     print(152)

# tuples = []
# with open('running-config.txt') as f:
#     config = f.read()
# acl_pattern = r"ip access-list extended \S+([\s\S]*?)\n!"
# acl_result = re.findall(acl_pattern, config, re.DOTALL)
# # 打印所有匹配的规则
# for acl in acl_result:
#     pattern = r'(?:permit|deny)\s+(\S+)\s+((?:host\s+\S+)|any)\s+((?:host\s+\S+)|any)\s+((?:eq|neq)\s+\w+|(?:range(?:\s+\d+){2})|(?:gt|lt)\s+\S+|\S+)'
#     match = re.findall(pattern, acl)
#     if match:
#         for m in match:
#             tuples.append((m[0], format_ip(m[1]), format_ip(m[2]), format_port(m[3])))

# print(tuples)

