from selenium import webdriver
import time
import os
from subprocess import Popen
from functions import *
import socket

def find_online_following(driver, chat):
	driver.get("http://www.twitch.tv/directory")
	print "loaded directory"
	time.sleep(2)
	try:
		a = driver.find_element_by_css_selector(".following-list").text.split("\n")
	except:
		time.sleep(3)
		try:
			a = driver.find_element_by_css_selector(".following-list").text.split("\n")
		except:
			driver.quit()
			print "Following list cannot be loaded, internet may be down."
			exit(1)
	usersOnline = []
	os.system("clear")
	for x in range(1,len(a),3):
		usersOnline.append(a[x].replace(" ", ""));
		print(a[x] + " = option " + str((x+2)/3 ))	

	option = input("Please enter which you would like to see (in number): ")-1
	
	# ... do other stuff while subprocess is running
	lastChat = ""
	custom(driver, usersOnline[option], chat)
	
def browse_popular_games(driver, chat):

	driver.get("http://www.twitch.tv/directory")
	print "loaded directory"
	time.sleep(2)
	try:
		a = driver.find_element_by_css_selector(".js-games.games.items").text.split("\n")
	except:
		time.sleep(3)
		try:
			a = driver.find_element_by_css_selector(".js-games.games.items").text.split("\n")
		except:
			driver.quit()
			print "Games cannot be loaded, internet may be down."
	gamesArray = []
	os.system("clear")
	for x in range(0,len(a),2):
		if x <= 12:
			gamesArray.append(a[x]);
			print(a[x] + " = option " + str((x+2)/2 ))
	gameToShow = gamesArray[input("Please enter which you would like to see (in number): ")-1]
	driver.get("http://www.twitch.tv/directory/game/"+(gameToShow.replace(" ","%20")))	
	time.sleep(2)
	os.system("clear")

	# GAMES
	try:
		a = driver.find_element_by_css_selector(".js-streams.streams.items").text.split("\n")
	except:
		time.sleep(3)
		try:
			a = driver.find_element_by_css_selector(".js-streams.streams.items").text.split("\n")
		except:
			driver.quit()
			print "Streams cannot be loaded, internet may be down."
	for x in range(0,len(a),2):
		if x < 12:
			print(a[x] + ", " + a[x+1] + " = option " + str((x+2)/2 ))

	gameToShow = a[input("Please enter which you would like to see (in number): ")*2 -1].split("on ")[1].replace(" ", "")
	print "game to show = " + gameToShow
	
	# ... do other stuff while subprocess is running
	custom(driver, gameToShow, chat)
def browse_top_channels(driver, chat):
	driver.get("http://www.twitch.tv/directory/all")
	try:
		a = driver.find_element_by_css_selector(".js-streams.streams.items").text.split("\n")
	except:
		time.sleep(3)
		try:
			a = driver.find_element_by_css_selector(".js-streams.streams.items").text.split("\n")
		except:
			driver.quit()
			print "Streams cannot be loaded, internet may be down."
	for x in range(0,len(a),2):
		if x < 20 and x+1 < len(a):
			print(a[x] + ", " + a[x+1] + " = option " + str((x+2)/2) + '\n')

	gameToShow = a[input("Please enter which you would like to see (in number): ")*2 -1].split("on ")[1].replace(" ", "")
	print "game to show = " + gameToShow
	custom(driver, gameToShow, chat)
def start(driver):
	print "Welcome to a CLI for twitch.tv"
	print "We have four options: \n1 view the people that you follow that are online\n2 browse the most popular games\n3 browse the top channels\n4 Enter a stream name."
	whatToDo = input("Please enter which you would like to do: ")
	chat = raw_input("Do you want your terminal window to show twitch chat? (y/n): ")
	# try:
	if whatToDo == 1:
		find_online_following(driver, chat)
	elif whatToDo == 2:
		browse_popular_games(driver, chat)
	elif whatToDo == 3:
		browse_top_channels(driver, chat)
	elif whatToDo == 4:
		streamer = raw_input("Enter the streamer you want to watch: ")
		custom(driver, streamer, chat)
def custom(driver, streamer, chat):
	if (chat == "y" or chat == "yes" or chat =="just"):
		if chat != "just":
			p = Popen(['livestreamer', 'twitch.tv/'+streamer, 'best', '--hls-segment-threads', '10']) # something long running
		print "loading chat..."
		bot_owner = 'jastuh192'
		nick = 'jastuh192'
		channel = '#'+streamer.lower()
		server = 'irc.twitch.tv'
		password = 'this should be a secrets file'

		irc = socket.socket()
		irc.connect((server, 6667)) #connects to the server
		#sends variables for connection to twitch chat
		irc.send('PASS ' + password + '\r\n')
		irc.send('USER ' + nick + ' 0 * :' + bot_owner + '\r\n')
		irc.send('NICK ' + nick + '\r\n')
		irc.send('JOIN ' + channel.lower() + '\r\n') 
		lookFor = channel+" :"
		while True:
			try:

				babadata = irc.recv(1204) #gets output from IRC server
				if (len(babadata) == 0):
					print "The length of babadata is 0, this is may be why chat stops..."
					irc = socket.socket()
					irc.connect((server, 6667)) #connects to the server
					#sends variables for connection to twitch chat
					irc.send('PASS ' + password + '\r\n')
					irc.send('USER ' + nick + ' 0 * :' + bot_owner + '\r\n')
					irc.send('NICK ' + nick + '\r\n')
					irc.send('JOIN ' + channel.lower() + '\r\n') 
				if (len(babadata.split('\n')) == 2):
					babauser = babadata.split(':')[1]
					babauser = babauser.split('!')[0] #determines the sender of the messages
					# print babauser + ": " + babadata
					if (babadata.find(lookFor) != -1):
						print babauser + ": "+ babadata[babadata.find(lookFor) + len(lookFor):]

			except IndexError:
				pass
			except UnicodeDecodeError:
				pass
			except KeyboardInterrupt:
				try:
					p.terminate()
					os.system("clear")
					a = raw_input("Thanks for using the app!\nPress control-c again to quit or press enter to start over")
					os.system("clear")
					f = open(".userinfo.csv", "r")
					a = f.read()
					nameArr = a.split(",")
					if len(nameArr) != 2:
						raise NameError("hello")
					userName = nameArr[0]
					password = nameArr[1]
					driver = webdriver.PhantomJS()
					driver.set_window_size(1120, 550)
					driver.get("http://www.twitch.tv/login")
					driver.find_element_by_id('login_user_login').send_keys(userName)
					driver.find_element_by_id('user[password]').send_keys("This should be a secrets file")
					driver.find_element_by_css_selector(".button.primary").click()
					start(driver)
				except KeyboardInterrupt:
					exit(1)
			except:
				print "unknown error"
	else:
		try:
			p = Popen(['livestreamer', 'twitch.tv/'+streamer, 'best', '--hls-segment-threads', '10']) # something long running
			while True:
				a = "a"
		except KeyboardInterrupt:
			try:
				os.system("clear")
				a = raw_input("Thanks for using the app!\nPress control-c again to quit or press enter to start over")
				f = open(".userinfo.csv", "r")
				a = f.read()
				nameArr = a.split(",")
				if len(nameArr) != 2:
					raise NameError("hello")
				userName = nameArr[0]
				password = nameArr[1]
				driver = webdriver.PhantomJS()
				driver.set_window_size(1120, 550)
				driver.get("http://www.twitch.tv/login")
				driver.find_element_by_id('login_user_login').send_keys(userName)
				driver.find_element_by_css_selector(".button.primary").click()
				start(driver)
			except KeyboardInterrupt:
				exit(1)
