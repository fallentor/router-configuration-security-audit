import json


def show_result(json_file):

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    tactic_group_count = {}
    risk_level_count = {}

    for item in data:
        if item['audit_result'] == False:   
            tactic_group_count[item['tactic_group']] = tactic_group_count.get(item['tactic_group'], 0) + 1
            risk_level_count[item['risk_level']] = risk_level_count.get(item['risk_level'], 0) + 1

    new_tactic_group_count = {}

    new_dict = tactic_group_count.copy()  

    for k, v in new_dict.items(): 
        if k == "UM" and "用户管理类" not in new_tactic_group_count:
            new_tactic_group_count["用户管理类"] = new_dict.get("UM")  
        if k == "OG" and "对象类" not in new_tactic_group_count:
            new_tactic_group_count["对象类"] = new_dict.get("OG")
        if k == "C" and "通信类" not in new_tactic_group_count:
            new_tactic_group_count["通信类"] = new_dict.get("C")  
        if k == "AC" and "访问控制类" not in new_tactic_group_count:
            new_tactic_group_count["访问控制类"] = new_dict.get("AC")


    context = {
        'tactic_group_count': new_tactic_group_count, 
        'risk_level_count': risk_level_count
    }

    return context
