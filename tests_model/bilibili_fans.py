import os
# import subprocess
import sys, json
from tqdm import tqdm
result = input()
# print(type(result))
data = json.loads(result)["data"]["rank_list"]
# print(data)
# 100018555028,100017892158,100017786414

# 100018555028,100017892158,100017786414

json_key = ["dynamic_act", "video_act", "video_play"]
print_name = ["F君动态沙发排行榜", "F君视频互动排行榜", "F君视频观看排行榜"]


for key, name in zip(json_key, print_name):
    print(name)
    for i, user in enumerate(data[key]):
        print(i + 1, user['uname'])
    print('--------')

print('感谢所有的粉丝朋友')

# cmd = open("/Users/faith/AI_Commander/tests_model/cmd.txt", "r").read()
# # cmd = "ls -all"
# # print(cmd)
# # fans_info = os.system(cmd)

# cmd =cmd.replace("\\", "").replace("'", "")
# print(cmd)
# split_cmds = []
# for i, c in enumerate(cmd.split("-H")):
#     if i == 0:
#         args = c.replace("\n", "").split(" ")
#         for arg in args:
#             if arg != "":
#                 split_cmds.append(arg)
#     else:
#         split_cmds.append("-H")
#         split_cmds.append(c) 
#         # print("++", c)
# print(split_cmds)
# result = subprocess.run(split_cmds, stdout=subprocess.PIPE)
# print(result.stdout)

