from django.test import TestCase

data = [
    {"id": 1, "parent_id": None, "children": []},
    {"id": 2, "parent_id": 1, "children": []},
    {"id": 3, "parent_id": 1, "children": []},
    {"id": 4, "parent_id": 2, "children": []},
    {"id": 5, "parent_id": 2, "children": []},
    {"id": 6, "parent_id": 3, "children": []},
    {"id": 7, "parent_id": None, "children": []},
]

# res_p = [
#     {
#         "id": 1,
#         "parent_id": None,
#         "children": [
#             {
#                 "id": 2,
#                 "parent_id": 1,
#                 "children": [
#                     {
#                         "id": 4,
#                         "parent_id": 2,
#                         "children": []
#                     },
#                     {
#                         "id": 5,
#                         "parent_id": 2,
#                         "children": []
#                     }
#                 ]
#             },
#             {
#                 "id": 3,
#                 "parent_id": 1,
#                 "children": [
#                     {
#                         "id": 6,
#                         "parent_id": 3,
#                         "children": []
#                     }
#                 ]
#             }
#         ]
#     },
#     {
#         "id": 7,
#         "parent_id": None,
#         "children": []
#     }
# ]

res_p = []
# 创建数据字典
data_dict = {item["id"]: item for item in data}
print(data_dict)
# 遍历数据，找出最高级节点（parent_id为None）
for item in data:
    if item["parent_id"] is None:
        res_p.append(item)

print(res_p)

# 递归构建树形结构
def build_tree(node, data_dict):
    node["children"] = [
        build_tree(data_dict[child_id], data_dict)
        for child_id in data_dict
        if data_dict[child_id]["parent_id"] == node["id"]
    ]
    return node


# 构建树形结构
for item in res_p:
    build_tree(item, data_dict)

print(res_p)
# for node in data:
#     if node['parent_id'] is None:
#         res_p.update(node)
#         res_p["children"] = []
#     else:
