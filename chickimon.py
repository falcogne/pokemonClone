""" STRUCTURE

	MOVEMENT AND RANDOM ENCOUNTERS *NOT GONNA DO YET*

	BATTLE:
	load pokemon - text file likely
	store who is in battle
	while loop for turns
		speed for who goes first:

		function for choice - based on pokemon class (cpu, human, random, idk)
		do the move
		check if dead

		function for choice
		do the move
		check if dead

	
	PLAYER CLASS:
	def action():
		pkmn.chooseaction
		check if viable (error checking loop)

	POKEMON CLASS:
	var = attack, defense, speed, evasiveness, totalhp, currhp, skip ranged att and ranged def for now
	#not gonna have pp

	def chooseaction


	DO MOVE FUNCTION:
	accuracy to see if miss:
	calculate health reduction based on
		attack / ranged attack of attacker
		defense / ranged defense of defender
		types?
	

"""

import os
# os.listdir() for the computer player's mons
import random

class Mon:
	def __init__(self, name):
		folder = "Fighters"
		with open(folder + "/" + name + ".txt", 'r') as file:
			# list(file)
			#or
			data = file.read().splitlines()

			# don't know how im gonna structure it yet
			self.name = data[0]
			self.thp = int(data[1])
			self.atk = int(data[2])
			self.dfn = int(data[3])
			self.spd = int(data[4])
			self.evs = int(data[5])

			self.chp = self.thp

			flag = True
			i = 7
			self.moves = []
			while flag:
				self.moves.append([data[i], int(data[i+1]), int(data[i+2])])

				if i+4 >= len(data):
					flag = False

				i+=5


	def numMoves(self):
		return len(self.moves)

	def move(self, num):
		return self.moves[num]

	def calcPower(self, moveInd, opponent):
		move = self.moves[moveInd]
		if move[2] >= random.randint(1, 100):
			dmg = move[1] * self.atk / opponent.dfn + (self.atk - opponent.dfn) / 4
		else:
			dmg = 0
		return dmg


	#returns true if dead but jus does the damage reduciton
	def takeDamage(self, value): #, oppType
		self.chp -= value
		if self.chp < 0:
			self.chp = 0
			return True
		return False



	def movesStr(self):
		string = "--MOVES--\n"
		string += "%4s %20s %6s %9s\n" % ("Ind", "Move name", "Power", "Accuracy")
		i=0
		for move in self.moves:
			string += "%3d: %20s %6d %9d\n" % (i, move[0],move[1],move[2])#format("{index:1d} {movename:20} ")
			i+=1
		return string

	def statsStr(self):
		string = "--STATS--\n%7s %8s %6s %12s\n" % ("Attack", "Defense", "Speed", "Evasiveness")
		string += "%7s %8s %6s %12s\n" % (self.atk, self.dfn, self.spd, self.evs)
		return string

	def healthStr(self):
		string = "Health: " + str(self.chp) + " out of " + str(self.thp) + "\n"
		return string

	def simpleStateStr(self):
		string = self.name + "\n"
		string += "HP: " + str(self.chp) + " out of " + str(self.thp)
		return string

	def __str__(self):
		string = "OVERVIEW OF: " + self.name + "\n"
		string += "\n" + self.healthStr()
		string += "\n" + self.statsStr()
		string += "\n" + self.movesStr()
		return string

class Player:
	def __init__(self, name):
		self.name = name
		self.pmons = [Mon("adam")] # prolly go by name.txt
		self.activeInd = 0
	"""
	HOW DO I DEAL WITH FAINTING? I DON'T HAVE ANY ITEMS SO NO NEED TO REVIVE?
	"""
	def chooseaction(self):
		# input whether battle or switch
		print(self.name + "'s choice")
		print("Input -1 to switch instead of fighting")
		
		# BATTLE
		numM = self.pmons[self.activeInd].numMoves()
		i = numM
		print(self.pmons[self.activeInd].movesStr())
		while i >= numM or i < -1:
			try:
				i = int(input("Which one: "))
			except ValueError:
				pass
			
		return i

	def switch(self):
		# SWITCH
		i = 0
		for mon in self.pmons:
			print(str(i) + ": " + mon.name)
			i+=1

		numM = i
		while i >= numM or i < 0 or self.pmons[i].chp == 0:
			try:
				i = int(input("Which one: "))
			except ValueError:
				pass

		
		else:
			self.activeInd = i


	def getActiveMon(self):
		return self.pmons[self.activeInd]

	def isDead(self):
		for mon in self.pmons:
			if mon.chp != 0:
				return False
		return True

	def die(self):
		print(self.name + " is dead")


class ComputerPlayer(Player):

	def switch(self):
		i = -100
		choices = []
		index = 0
		for possible in self.pmons:
			if possible.chp != 0:
				choices.append(index)
			index += 1

		if len(choices) > 0:
			i = random.choice(choices)
		else:
			self.die()
		self.activeInd = i

	def chooseaction(self):
		#complete random
		i = -100
		numM = self.pmons[self.activeInd].numMoves()
		while i >= numM or i < -1:
			i = random.randint(-1, numM-1)
		return i




class Battle():
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2


	def start(self):
		turns = 1
		while self.p1.isDead() == False and self.p2.isDead() == False:
			print("\n\n-------TURN " + str(turns) + "--------")
			print(self.p1.name + ": " + self.p1.getActiveMon().simpleStateStr())
			print("VS")
			print(self.p2.name + ": " + self.p2.getActiveMon().simpleStateStr())
			print()
			isDead1 = False
			isDead2 = False
			choice1 = self.p1.chooseaction()
			choice2 = self.p2.chooseaction()

			#val is an int, who to switch to
			if choice1 == -1:
				print(self.p1.name + " decides to switch pokemon")
				self.p1.switch()
			if choice2 == -1:
				print(self.p2.name + " decides to switch pokemon")
				self.p2.switch()

			#somehow have to put speed into this
			if choice1 != -1:
				movePower = self.p1.getActiveMon().calcPower(choice1, self.p2.getActiveMon())
				print(self.p1.name + " uses " + self.p1.getActiveMon().move(choice1)[0])
				if movePower == 0:
					print("It missed")
				else:
					isDead2 = self.p2.getActiveMon().takeDamage(movePower)

			if isDead2:
				self.p2.switch()
			elif choice2 != -1:
				movePower = self.p2.getActiveMon().calcPower(choice2, self.p1.getActiveMon())
				print(self.p2.name + " uses " + self.p2.getActiveMon().move(choice2)[0])
				if movePower == 0:
					print("It missed")
				else:
					isDead1 = self.p1.getActiveMon().takeDamage(movePower)

			turns+=1

Battle(Player("Adam"), ComputerPlayer("BBB")).start()



