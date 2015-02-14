from selenium import webdriver
import time
import os
from subprocess import Popen
from functions import *
import socket
import platform
if platform.system() == "Windows":
	clearText = "cls"
else:
	clearText = "clear"
os.system(clearText)
try:
	f = open(".userinfo.csv", "r")
	a = f.read()
	nameArr = a.split(",")
	if len(nameArr) != 2:
		raise NameError("hello")
	userName = nameArr[0]
	password = nameArr[1]
except:
	print "First time set up!"
	userName = raw_input("Enter your username: ")
	password = raw_input("Enter your password: ")
	f = open(".userinfo.csv", "w")
	f.write(userName+","+password)
driver = webdriver.PhantomJS()

driver.set_window_size(1120, 550)

print "preparing login page"
driver.get("http://www.twitch.tv/login")
driver.find_element_by_id('login_user_login').send_keys(userName)
driver.find_element_by_id('user[password]').send_keys(password)
driver.find_element_by_css_selector(".button.primary").click()
if driver.current_url != "http://www.twitch.tv/":
	print "The username and password that you entered are not correct. \nPlease rerun the program and enter your username and password."
	os.remove(".userinfo.csv")
	driver.quit()
	exit(1)
print "logged in as " + userName
start(driver, clearText)
# except:
# 	print "An error occured, please rerun the program making sure you enter valid choices."
# 	driver.quit()
# 	exit(1)
driver.quit()	
