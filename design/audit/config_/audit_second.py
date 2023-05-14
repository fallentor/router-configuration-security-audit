import csv
import json
from collections import defaultdict
from audit.config_.audit_first import make_audit_data


class AclRuleChecker:
    def __init__(self, filename, json_file):   # filename 为 acl_rules.csv  json_file 为 audit.json
        self.rules = []
        self.read_rules(filename)
        self.build_tree()

        self.json_file = json_file

        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.json_data = json.load(f)
        except FileNotFoundError:
            self.json_data = []

        # print(self.json_data)


    def save_data_in_json(self, data):
        self.json_data.append(data)
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.json_data, f, ensure_ascii=False, indent=4)
        
    def read_rules(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.rules.append(row)
    
    def check_excessive_service_authorization(self):
        for rule in self.rules:
            protocol = rule['protocol']
            if protocol == 'any':
                audit_result = False
            else:
                audit_result = True
        data = make_audit_data(
            14,
            "AC",
            "服务授权过度检测",
            "中级",
            audit_result
        )

        # 将审计结果添加到 JSON 数据中，并写入文件
        self.save_data_in_json(data)
        return


    def check_excessive_authorization_dest(self):
        for rule in self.rules:
            protocol = rule['dest_address']
            if protocol == 'any':
                data = make_audit_data(
                    15,
                    "AC",
                    "目的地址授权过度检测",
                    "中级",
                    False
                )

                # 将审计结果添加到 JSON 数据中，并写入文件
                self.save_data_in_json(data)
                return


    def build_tree(self):
        # 以协议为根节点,源地址、目的地址、源端口、目的端口作为节点的决策树
        self.tree = defaultdict(list)
        
        for rule in self.rules:
            protocol = rule['protocol']
            source_addr = self.format_addr(rule['source_address'])
            dest_addr = self.format_addr(rule['dest_address'])
            source_port = self.format_port(rule['source_port'])
            dest_port = self.format_port(rule['dest_port'])
            
            tree_node = (protocol, source_addr, dest_addr, source_port, dest_port)
            self.tree[tree_node].append(rule)
            
    def format_addr(self, addr):
        if addr == 'any':
            return addr
        else:
            return tuple(addr.split('/'))
            
    def format_port(self, port):
        if port.startswith('>') or port.startswith('<'):
            return (port[0], int(port[1:]))
        elif '-' in port:
            ports = port.split('-')
            return (ports[0], ports[1])
        elif port == 'any':
            return port
        elif port.startswith('~'):
            return ('not', int(port[1:]))
        else:
            return int(port)
      
    # 冗余 与 冲突检测        
    def check(self):
        # 检查冗余
        for rules in self.tree.values():
            if len(rules) > 1:

                data = make_audit_data(
                    16,
                    "AC",
                    "服务冗余检测",
                    "低级",
                    False
                )

                # 将审计结果添加到 JSON 数据中，并写入文件
                self.save_data_in_json(data)
                 
        
        # 检查冲突
        for source in self.tree:
            rules = self.tree[source]
            permit_rules = []
            deny_rules = []
            for rule in rules:
                if rule['action'] == 'permit':
                    permit_rules.append(rule)
                else:
                    deny_rules.append(rule)
            
            # 检查同一节点
            if permit_rules and deny_rules:  
                data = make_audit_data(
                    17,
                    "AC",
                    "服务异常检测",
                    "中级",
                    False
                )
                
                # 将审计结果添加到 JSON 数据中，并写入文件
                self.save_data_in_json(data)

                return
                
            # 检查相邻节点
            source_addr = source[1]
            dest_addr = source[2]
            for neighbor in self.tree:
                if neighbor[1] == source_addr and neighbor[2] == dest_addr:
                    neighbor_rules = self.tree[neighbor]
                    for rule in neighbor_rules:
                        if rule['action'] == 'permit':
                            permit_rules.append(rule)
                        else:
                            deny_rules.append(rule)
                            
            if permit_rules and deny_rules:
                data = make_audit_data(
                    17,
                    "AC",
                    "服务异常检测",
                    "中级",
                    False
                )
                
                # 将审计结果添加到 JSON 数据中，并写入文件
                self.save_data_in_json(data)
                return

    def check_all(self):
        try:
            if self.rules:
                self.check_excessive_service_authorization()
                self.check_excessive_authorization_dest()
                self.check()
        except Exception as e:
            print("审计出错")


# if __name__ == '__main__':
#     checker = AclRuleChecker('acl_rules.csv', 'audit.json')
#     checker.check_all()
