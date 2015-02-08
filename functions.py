from selenium import webdriver
import time
import os
import _tkinter
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
	usersOnline = []
	os.system("clear")
	for x in range(1,len(a),3):
		usersOnline.append(a[x].replace(" ", ""));
		print(a[x] + " = option " + str((x+2)/3 ))	

	option = input("Please enter which you would like to see (in number): ")-1
	p = Popen(['livestreamer', 'twitch.tv/'+usersOnline[option], 'best']) # something long running
	# ... do other stuff while subprocess is running
	lastChat = ""
	if (chat == "y" or chat == "yes"):
		print "loading chat..."

		bot_owner = 'jastuh192'
		nick = 'jastuh192'
		channel = '#'+usersOnline[option]
		server = 'irc.twitch.tv'
		password = 'oauth:sai9s3p0b80dy1758xpr3gtyt4g0ql'

		irc = socket.socket()
		irc.connect((server, 6667)) #connects to the server

		#sends variables for connection to twitch chat
		irc.send('PASS ' + password + '\r\n')
		irc.send('USER ' + nick + ' 0 * :' + bot_owner + '\r\n')
		irc.send('NICK ' + nick + '\r\n')
		irc.send('JOIN ' + channel.lower() + '\r\n') 
		lookFor = "#"+usersOnline[option].lower()+" :"
		while True:
			try:

				babadata = irc.recv(1204) #gets output from IRC server
				if (len(babadata.split('\n')) == 2):
					babauser = babadata.split(':')[1]
					babauser = babauser.split('!')[0] #determines the sender of the messages
					# print babauser + ": " + babadata
					if (babadata.find(lookFor) != -1):
						print babauser + ": "+ babadata[babadata.find(lookFor) + len(lookFor):]

			except (IndexError, UnicodeDecodeError):
				continue
			except KeyboardInterrupt:
				print "Thanks for using the app!"
				p.terminate()
				driver.quit()
				exit(1)
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
	p = Popen(['livestreamer', 'twitch.tv/'+gameToShow, 'best']) # something long running
	# ... do other stuff while subprocess is running
	lastChat = ""
	if (chat == "y" or chat == "yes"):
		print "loading chat..."

		bot_owner = 'jastuh192'
		nick = 'jastuh192'
		channel = '#'+gameToShow.lower()
		server = 'irc.twitch.tv'
		password = 'oauth:sai9s3p0b80dy1758xpr3gtyt4g0ql'

		irc = socket.socket()
		irc.connect((server, 6667)) #connects to the server

		#sends variables for connection to twitch chat
		irc.send('PASS ' + password + '\r\n')
		irc.send('USER ' + nick + ' 0 * :' + bot_owner + '\r\n')
		irc.send('NICK ' + nick + '\r\n')
		irc.send('JOIN ' + channel.lower() + '\r\n') 
		lookFor = "#"+gameToShow.lower()+" :"
		while True:
			try:

				babadata = irc.recv(1204) #gets output from IRC server
				if (len(babadata.split('\n')) == 2):
					babauser = babadata.split(':')[1]
					babauser = babauser.split('!')[0] #determines the sender of the messages
					# print babauser + ": " + babadata
					if (babadata.find(lookFor) != -1):
						print babauser + ": "+ babadata[babadata.find(lookFor) + len(lookFor):]

			except (IndexError, UnicodeDecodeError):
				continue
			except KeyboardInterrupt:
				print "Thanks for using the app!"
				p.terminate()
				driver.quit()
				exit(1)

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
		if x < 20:
			print(a[x] + ", " + a[x+1] + " = option " + str((x+2)/2) + '\n')

	gameToShow = a[input("Please enter which you would like to see (in number): ")*2 -1].split("on ")[1].replace(" ", "")
	print "game to show = " + gameToShow
	p = Popen(['livestreamer', 'twitch.tv/'+gameToShow, 'best']) # something long running
	# ... do other stuff while subprocess is running
	lastChat = ""
	print "loading chat..."
	if (chat == "y" or chat == "yes"):
		bot_owner = 'jastuh192'
		nick = 'jastuh192'
		channel = '#'+gameToShow.lower()
		server = 'irc.twitch.tv'
		password = 'oauth:sai9s3p0b80dy1758xpr3gtyt4g0ql'

		irc = socket.socket()
		irc.connect((server, 6667)) #connects to the server

		#sends variables for connection to twitch chat
		irc.send('PASS ' + password + '\r\n')
		irc.send('USER ' + nick + ' 0 * :' + bot_owner + '\r\n')
		irc.send('NICK ' + nick + '\r\n')
		irc.send('JOIN ' + channel.lower() + '\r\n') 
		lookFor = "#"+gameToShow.lower()+" :"
		while True:
			try:

				babadata = irc.recv(1204) #gets output from IRC server
				if (len(babadata.split('\n')) == 2):
					babauser = babadata.split(':')[1]
					babauser = babauser.split('!')[0] #determines the sender of the messages
					# print babauser + ": " + babadata
					if (babadata.find(lookFor) != -1):
						print babauser + ": "+ babadata[babadata.find(lookFor) + len(lookFor):]

			except (IndexError, UnicodeDecodeError):
				continue
			except KeyboardInterrupt:
				print "Thanks for using the app!"
				p.terminate()
				driver.quit()
				exit(1)