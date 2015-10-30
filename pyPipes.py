#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import select
import random
import time

up    = u"╚╩╠╬╣║╝"

down  = u"╔╦╠╬╣║╗"

left  = u"╩╦═╬╣╗╝"

right = u"╚╔╩╦╠═╬"

directions = [up, down, left, right]

keypress = None
old_row = None

#Detects Enter keypress
def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False

#Returns a new row of pipes
def generate_row(length):
	row = u""
	for i in range(length):
		row += unicode(randomPipe(getConnections(row)))
	return row

#Returns a bool array denoting if connections should be made
#pos is the position in the row (indexed from 0)
def getConnections(progress_row):
	# not doing - 1 because the progress is up to 
	# but not including the current pipe
	pos = len(progress_row)
	result = [True]*2
	up_pos = 0
	left_pos = 1

	# Check if it needs a connection above
	if old_row != None and old_row[pos] in down:
		result[up_pos] = True
	else:
		result[up_pos] = False

	# Check if it needs a connection to the right
	if pos > 0 and progress_row[pos - 1] in right:
		result[left_pos] = True
	else:
		result[left_pos] = False

	return result

def randomPipe(connections):
	up_pos = 0
	left_pos = 1
	rightdown = stringIntersection(right, down)

	possible_pipes = u""

	if connections[up_pos] and connections[left_pos]:
		#Needs an up and right conn
		possible_pipes = stringIntersection(up, left)
	elif connections[up_pos]:
		possible_pipes = removeDirection(left, up)
	elif connections[left_pos]:
		possible_pipes = removeDirection(up, left)
	else:
		possible_pipes = removeDirection(
							up, 
							removeDirection(left, stringUnion(right, down))
							)

	#random index from 0 to len(possible_pipes) - 1
	pipe = possible_pipes[random.randint(0, len(possible_pipes) - 1)]

	return pipe

def removeDirection(direction, unicodeStr):
	result = u""
	for c1 in unicodeStr:
		if c1 not in direction:
			result += unicode(c1)
	return result

def stringUnion(unicode1, unicode2):
	result = unicode(unicode1)
	for c2 in unicode2:
		if c2 not in result:
			result += unicode(c2)
	return result

def stringIntersection(unicode1, unicode2):
	result = u""
	for c1 in unicode1:
		if c1 in unicode2:
			result += unicode(c1)
	return result

#Start
while True:
	#Update keypress
	if heardEnter():
		break;
	#Generate a row
	time.sleep(.1)
	new_row = generate_row(60);
	print new_row
	old_row = new_row