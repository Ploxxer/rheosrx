import os
import datetime
import shutil


date = datetime.datetime.now()


dir_num = os.listdir('./log_folder')

print(len(dir_num))

if len(dir_num) > 1:
    print('hi')


path = './log_folder'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getctime)

print(files)
oldest = files[0]
newest = files[-1]

print(oldest)
print(newest)


