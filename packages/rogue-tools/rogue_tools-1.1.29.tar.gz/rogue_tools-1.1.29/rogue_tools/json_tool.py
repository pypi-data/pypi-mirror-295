import json
from deepdiff import DeepDiff
from rogue_tools import file_tool

def load_json_by_file(file_path)->dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_json_by_str(json_str)->dict:
    return json.loads(json_str)

def output_json_by_dict(dict_obj)->str:
    return json.dumps(dict_obj)

def save_json_by_dict(path,dict_obj):
    json_str = json.dumps(dict_obj)
    file_tool.write_str(path,json_str,'w+')

def compare_json(json1, json2):
    '''有差异返回差异结果，没有差异返回None'''
    diff = DeepDiff(json1, json2, ignore_order=True)
    if diff:
        return format_diff(diff)
    else:
        return None

def format_diff(diff):
    formatted_diff = []
    for diff_type, changes in diff.items():
        formatted_diff.append(f"差异类型: {diff_type}")
        if isinstance(changes, dict):
            for change, detail in changes.items():
                formatted_diff.append(f"  {change}: {detail}")
        elif isinstance(changes, list):
            for change in changes:
                formatted_diff.append(f"  {change}")
        else:
            formatted_diff.append(f"  {changes}")
    return "\n".join(formatted_diff)






if __name__ == "__main__":
    file1 = r'C:\Users\luohao\Desktop\fsdownload\1_3133.json'
    file2 = r'C:\Users\luohao\Desktop\fsdownload\1_3143.json'
    
    differences = compare_json(load_json_by_file(file1), load_json_by_file(file2))
    
    if differences:
        print("两个JSON文件之间的差异如下：")
        print(differences)
    else:
        print("两个JSON文件没有差异。")
