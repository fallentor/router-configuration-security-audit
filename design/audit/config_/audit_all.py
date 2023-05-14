import os
from audit.config_.audit_first import Audit
from audit.config_.audit_second import AclRuleChecker
from audit.config_.config_handler import get_acl_rules_csv



"""
filename 为 清洗后的 acl_rulse.csv 文件  
	json_file 为 保存审计结果的 json 文件
	config_path 为 路由器配置文件
"""
def check_all_object(config_path, json_file):
	path = os.path.dirname(os.path.abspath(__file__))
	parent_dir_path = os.path.dirname(os.path.dirname(path))
	filename = f"{parent_dir_path}\\static\\audit_files\\acl_rules.csv"
	get_acl_rules_csv(filename, config_path)
	audit = Audit(config_path, json_file)
	audit.check_all()
	aclRuleChecker = AclRuleChecker(filename, json_file)
	aclRuleChecker.check_all()




