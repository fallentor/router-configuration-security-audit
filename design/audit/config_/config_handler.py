import ipaddress
import socket
import re
import csv


services = {
    'ftp': 21,
    'ssh': 22,
    'telnet': 23,
    'smtp': 25,
    'dns': 53,
    'dhcp': 67,
    'tftp': 69,
    'http': 80,
    'pop3': 110,
    'nntp': 119,
    'ntp': 123,
    'imap': 143,
    'snmp': 161,
    'ldap': 389,
    'https': 443,
    'ftp-data': 20,
    'sql-net': 1521,
    'bgp': 179,
    'syslog': 514,
    'ldaps': 636,
    'diameter': 3868,
    'bittorrent-tracker': 6969,
    'bittorrent': 6881,
    'smb': 445,
    'mssql': 1433,
    'echo-reply': 2000,
    'www': 80,
    'time-exceeded': 11,
    'established': 'any',
    'any': 'any'
}


def format_ip(ip):
    '''
    格式化 IP 地址
    1. 将任意地址或为空转为 any  
    2. 将单个IP地址（host xxx.xxx.xxx.xxx）转为 xxx.xxx.xxx.xxx/32 的形式
    3. 将 IP 地址段 (xxx.xxx.xxx.xxx/xx, xxx.xxx.xxx.xxx 子网掩码, "192.168.1.0 255.255.255.0") 转化为 xxx.xxx.xxx.xxx/xx 的形式
    4. 处理主机名形式的 IP 地址，如解析失败则返回原始值。
    '''

    if not ip or ip.lower() == 'any':
        # 任意地址和空地址统一变成 any
        return 'any'
    
    elif ip.startswith('host '):
        # host xxx.xxx.xxx.xxx 形式转为 xxx.xxx.xxx.xxx/32
        return ip[5:] + '/32'
        
    else:
        parts = ip.split('/')
        if len(parts) == 2: # IP 地址段的形式 xxx.xxx.xxx.xxx/xx
            try:
                network = ipaddress.ip_network(ip, strict=False)
                return str(network.with_prefixlen)
            except Exception as e:
                return ip
        
        elif len(parts) == 1:
            try:
                ipaddress.ip_address(ip) # 检查IP地址是否有效
                return ip + '/32'
            except ValueError:
                pass
            
            try:
                # 处理 "192.168.1.0 255.255.255.0" 的形式
                network, mask = parts[0].split(' ')
                mask = handle_subnet_equivalent(mask)
                network = ipaddress.IPv4Interface(f"{network}/{mask}")
                return network
            except Exception as e:
                pass

            try:
                # 处理域名形式的地址
                ip_addr = socket.gethostbyname(ip)
                return format_ip(ip_addr)
            except Exception as e:
                return ip

        else:
            # 只剩下“xxx.xxx.xxx.xxx”子网掩码格式
            try:
                mask = parts[0]
                network = ipaddress.IPv4Interface(f"0.0.0.0/{mask}")
                return str(network.network) + '/' + str(network.network_prefix_length)
            except Exception as e:
                return ip


def handle_subnet_equivalent(mask):
    """
    处理 0.0.0.0 的等价情况
    """

    # 处理等价子网掩码
    if mask == '0.255.255.255':
        mask = '255.0.0.0'
    elif mask == '0.0.255.255':
        mask = '255.255.0.0'
    elif mask == '0.0.0.255' or mask == '':
        mask = '255.255.255.0'

    return mask


def extract_ip(text):
    '''
    从文本中提取 IP 地址
    '''

    pattern = r'(host\s+)?((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))|(any)', re.IGNORECASE
    match = re.match(pattern, text)
    if match:
        # 在分组中查找IP地址
        ip_group = match.group(3) or match.group(4) or match.group(5)
        if ip_group:
            return ip_group.strip()
        elif match.group(6):
            return 'any'
        else:
            # 处理主机名的情况
            try:
                hostname = match.group(2)
                ip_addr = socket.gethostbyname(hostname)
                return ip_addr
            except Exception as e:
                return None
    else:
        return None


def format_port(port):
    '''
    格式化端口号
    1. 将 eq xx 形式的文本转为纯数字
    2. 如果是纯文本，尝试查找对应的服务并转为对应的端口号，默认为0，
       支持 echo-reply、www、time-exceeded 和 (range xxx xx) 等特殊情况。
    '''
    if isinstance(port, str) and port.startswith('eq '):
        # 将 "eq xx" 形式的文本转为纯数字
        return format_port(port[3:])
    elif isinstance(port, str) and port.startswith('neq '):
        return '~' + format_port(port[4:])
    elif port.isdigit():
        # 端口号已经是数字直接返回
        return port
    elif 'gt' in port or 'lt' in port:
        match = re.search(r'(gt|lt)\s+(\S+)', port)
        if match:
            flag = match.group(1)
            port_ = match.group(2)
            if port_.isdigit():
                return '>' + str(port_) if flag == 'gt' else '<' + str(port_)
            else:
                return '>' + str(services[port_.lower()]) if flag == 'gt' else '<' + str(services[port_.lower()])
    else:
        # 尝试将文本解析成服务名，并返回对应的端口号
        match = re.search(r'range\s+(\S+)\s+(\S+)', port)
        if match:
            # 特殊格式 "(range xxx xx)" 的情况，取其中两个数字范围内的端口号
            start, end = int(match.group(1)), int(match.group(2))
            return str(start) + '-' + str(end)
        elif port.lower() in services:
            # 能在内置服务列表中找到对应服务的情况
            return str(services[port.lower()])
        else:
            # 仍然无法识别则默认为0
            return '0'



def get_acl_rules_csv(filename, config_path):
    # 打开 test.txt 文件，读取其中内容
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()


    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'action', 'protocol', 'source_address', 'dest_address', 'source_port', 'dest_port'])
    # pattern = r'access\-list\s+(\d+)\s+(permit|deny)\s+(\w+)\s+((?:\d{1,3}\.){3}\d{1,3}\s+(?:255|0|\.){7}|any|(?:host )?(?:\d{1,3}\.){3}\d{1,3}(?:/\d+)?|\w+(?:\.\w+)+)\s+((?:\d{1,3}\.){3}\d{1,3}\s(?:255|0|\.){7}|any|(?:host )?(?:\d{1,3}\.){3}\d{1,3}(?:/\d+)?|\w+(?:\.\w+)+)?\s*((?:eq|neq)\s+\w+|(?:range(?:\s+\d+){2})|(?:gt|lt)\s+\S+|(?:\w|-)+)\s*((?:eq|neq)\s+\w+|(?:range(?:\s+\d+){2})|(?:gt|lt)\s+\S+|\S+)?$'
        pattern = r'access\-list\s+(\d+)\s+(permit|deny)\s+(\w+)\s+(any|(?:host )?(?:\d{1,3}\.){3}\d{1,3}(?:/\d+)?(?:\s+(?:255|0|\.){7})?|\w+(?:\.\w+)+)\s+(any|(?:host )?(?:\d{1,3}\.){3}\d{1,3}(?:/\d+)?(?:\s(?:255|0|\.){7})?|\w+(?:\.\w+)+)?\s*((?:eq|neq)\s+\w+|(?:range(?:\s+\d+){2})|(?:gt|lt)\s+\S+|(?:\w|-)+)?\s*((?:eq|neq)\s+\w+|(?:range(?:\s+\d+){2})|(?:gt|lt)\s+\S+|\S+)?$'
        results = re.findall(pattern, content, re.MULTILINE)
        for r in results:
            id = r[0]
            action = r[1]
            protocol = r[2]
            source_address = format_ip(r[3])
            dest_address = 'any' if not r[4] else format_ip(r[4].strip())
            source_port = 'any' if not r[5] else format_port(r[5].strip())
            dest_port = 'any' if not r[6] else format_port(r[6].strip())
            # print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(id, action, protocol, source_address, dest_address, source_port, dest_port))
            writer.writerow([id, action, protocol, source_address, dest_address, source_port, dest_port])





