'''
2021/3/25
转移小姐姐图片
'''
import os
files = os.listdir("/data5/2019swh/picture/sandu")
os.chdir("/data5/2019swh/picture/sandu/")
for fff in files:
    os.system("mv "+fff+"/* ..")
