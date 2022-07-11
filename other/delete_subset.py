'''
2021/1/12
下载merra2模式层的数据，只下载从3.1到6.30的数据，把无关的剔除
31+30+31+30 = 121
'''
f = open("/data5/2019swh/subset_M2T3NPTDT_5.12.4_20210123_063658.txt","r")
files = f.readlines()
month = ["03","04","05","06"]
files_out = []
for line in files:
    if line[162:164] in month:
        files_out.append(line)
    else:
        continue

with open("/data5/2019swh/tdt_subset1.txt","w") as f2:
    for lines in files_out[0:1000]:
        f2.write(lines)
with open("/data5/2019swh/tdt_subset2.txt","w") as f3:
    for lines in files_out[1000:2000]:
        f3.write(lines)
with open("/data5/2019swh/tdt_subset3.txt","w") as f4:
    for lines in files_out[2000:3000]:
        f4.write(lines)
with open("/data5/2019swh/tdt_subset4.txt","w") as f5:
    for lines in files_out[3000:4000]:
        f5.write(lines)
with open("/data5/2019swh/tdt_subset5.txt","w") as f6:
    for lines in files_out[4000:]:
        f6.write(lines)