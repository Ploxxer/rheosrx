Documentation for automatic folder structure creation for instrument local machines and egnyte

stuff needed:
1. file_creation_windows_prod.py
2. instrument_name.txt
3. README.txt


instruction:
1. check if login credentials for program work (ie. egnyte auth bearer token, egnyte auth and guid with dev access), to get bearer token, look at authenticating internal applications(must have password set for egnyte specifically to do this)
2. get access to instrument computer somehow(ie. ssh, physical access, remote desktop)
3. install latest version of python 2.7, as of now latest version is 2.7.15
4. make sure to auto include creation of the path to speed up process
5. pip install requests, pip install simplejson
6. put python file somewhere, create log_folder directory under the drive letter specified within sapio under the instruments panel(most likely the C:\\ drive) and change the copy destination of the shutil.copy path to within the log_folder
7. put instrument_name.txt in same folder as the python file and change the contents of the file to the instrument the name of the instrument it is on
8. make sure there is an experiment within sapio that has a instrument with the same name as that of the local machine so you can test properly
9. if you run the program, you should be able to find the folder structure created on the local machine and within egnyte
10. the program should print out the paths for both egnyte and the local machine for easier searching
11. if something related to the paths breaks, check the instruments page to see if every field is entered in correctly
11. if everything works, make a scheduled task for the program to run every x amount of time
12. the log_folder folder should always have no more than 3 log files at a time, the date of the file's time of creation appended to the log name will make it easier to figure out age of the log file
13. the test.log file within the working directory will be constantly created and removed since this was the only solution I could come up with to circumvent windows not allowing multiple processes to open a file at the same time
