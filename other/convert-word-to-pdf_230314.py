import os


path1 = '/home/sun/data/other_data/mj_file/'

path2 = os.listdir(path1)

for i in path2:
    path3 = path1 + i
    os.system('rm -rf ' + path3 + '/*pdf')
    list1 = os.listdir(path3)
    #os.chdir(path3)
    for j in list1:
        #print(j)
        #a = j
        #a = a.replace(" ", "-")
        #a = a.replace("(", "-")
        #a = a.replace(")", "-")
        #os.system("mv "+ path3 +'/' + j + path3 +'/' + a)
        #os.system('rm -rf ' + path3 +'/' + j)
        os.system('libreoffice --headless --convert-to pdf --outdir '+ path3 + ' ' + '"' + path3 +'/' + j + '"')