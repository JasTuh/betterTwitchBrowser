from selenium import webdriver
import time
import os
import _tkinter
from subprocess import Popen
from functions import *
import socket
os.system("clear")
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
driver.find_element_by_id('user[password]').send_keys("Hihi47")
driver.find_element_by_css_selector(".button.primary").click()
if driver.current_url != "http://www.twitch.tv/":
	print "The username and password that you entered are not correct. \nPlease rerun the program and enter your username and password."
	os.remove(".userinfo.csv")
	driver.quit()
	exit(1)
print "logged in as " + userName
print "Welcome to a CLI for twitch.tv"
print "We have three options: \n1 view the people that you follow that are online\n2 browse the most popular games\n3 browse the top channels"
whatToDo = input("Please enter which you would like to do: ")
chat = raw_input("Do you want your terminal window to show twitch chat? (y/n): ")
try:
	if whatToDo == 1:
		find_online_following(driver, chat)
	elif whatToDo == 2:
		browse_popular_games(driver, chat)
	elif whatToDo == 3:
		browse_top_channels(driver, chat)
except:
	print "An error occured, please rerun the program."
	driver.quit()
	exit(1)
driver.quit()	
