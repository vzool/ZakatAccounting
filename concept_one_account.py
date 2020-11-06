import time
import pprint
import random
import collections

random.seed(3)

pp = pprint.PrettyPrinter()

log = {}
box = []

def newStep():
	step = time.time()
	print("STEP: %s" % step)
	return step

def add(value, step=0, date=0):
	print('add (%d): %d' % (len(box), value))
	if step == 0:
		step = newStep()
	if date == 0:
		date = time.time()
	addLog(value, step=step)
	box.append({'index': len(box),'capital': value, 'rest': value, 'time': date})
	return step

def addLog(value, step=0, index=0):
	# print('AddLog(Pre): value(%d) step(%d) index(%d)' % (value, step, index))
	if value == 0:
		return
	current = len(box)
	if step == 0:
		step = newStep()
	if value < 0:
		if index >= 0:
			current = index
		else:
			current += index
	# print('AddLog(Post): value(%d) step(%d) index(%d)' % (value, step, index))
	if not step in log.keys():
		log[step] = []
	log[step].append({'index': current, 'value': value})
	return step

def balance():
	total = 0
	for row in box:
		total += row['rest']
	return total

def sub(value, debug=False):

	print('sub: %d' % value)

	rest = value
	total = balance()

	if total < value:
		print('Warning: ask for %d insufficient balance: %d' % (value,total))

	bcount = len(box)
	step = newStep()
	limit = -(bcount+1)

	if debug:
		print("bcount(%d) - limit(%d)" % (bcount, limit))

	if bcount == 0:
		add(-value, step)
		return step

	# seekIndex = seekPlain()

	# Negative is a Hole, Zero is a Plain and Positive is a Mountain
	for index in range(-1, limit, -1):

		if rest <= box[index]['rest']:
			box[index]['rest'] -= rest
			addLog(-rest, step, index)
			break
		else:
			
			total = balance() # debug
			current = box[index]['rest']
			change = current - rest

			if debug:
				print("Loop: index(%d) - current(%d) - rest(%d) - change(%d) - total(%d) - limit(%d) - bcount(%d)" % 
					(index, current, rest, change, total, limit, bcount)) # debug

			# if current is less than zero then put in the hole
			if current < 0:
				# if seekIndex != None:
				# 	index = seekIndex
				box[index]['rest'] += -rest
				stats()
				addLog(-rest, step, index)
				break
			# if change is less than or equal zero 
			if change <= 0:
				
				# if total < 0:
				# 	pp.pprint(box[index:-1])
				# 	highestValue = -1	
				# 	highestIndex = -1	
				# 	for b in box[index:-1]:
				# 		if b['rest'] > highestValue:
				# 			highestValue = b['rest']
				# 			highestIndex = b['index']

				# 	print("Negative-Total: index(%d) - current(%d) - rest(%d) - change(%d) - total(%d) - limit(%d) - bcount(%d) - highestValue(%d), highestIndex(%d)" % 
				# 		(index, current, rest, change, total, limit, bcount, highestValue, highestIndex))

				# 	box[-1]['rest'] = change
				# 	addLog(-rest, step, index)
				# 	break

				extra = 0
				rest = -change

				# highestValue = -1	
				# highestIndex = -1
				# lowestValue = -1	
				# lowestIndex = -1
				# for b in box[0:index]:
				# 	if b['rest'] < lowestValue:
				# 		lowestValue = b['rest']
				# 		lowestIndex = b['index']
				# for b in box[lowestIndex:index]:
				# 	if b['rest'] > highestValue:
				# 		highestValue = b['rest']
				# 		highestIndex = b['index']

				# if highestValue >= 0:
				# 	print("SCAN: index(%d) - current(%d) - rest(%d) - change(%d) - total(%d) - limit(%d) - bcount(%d) - highValue(%d), highIndex(%d), lowValue(%d), lowIndex(%d), WRange(%d), LRange(%d)" % 
				# 		(index, current, rest, change, total, limit, bcount, highestValue, highestIndex, lowestValue, lowestIndex, len(box[0:index]), len(box[lowestIndex:index])))

				# In reverse Detection(A) about first item in second position
				# So, we can put the rest in the hole.
				if index-1 == limit:
					extra = -rest
					print("HIT(A): index(%d) - limit(%d) - change(%d) - extra(%d) - bcount(%d)" % (index, limit, change, extra, bcount))
					box[-1]['rest'] = extra
				
				if bcount > 1:
					box[index]['rest'] = 0
				addLog(-current, step, index)

				# In reverse Detection(B) about first item in second position.
				# So, we log things in order.
				if index-1 == limit:
					print("HIT(B): index(%d) - limit(%d) - change(%d) - extra(%d) - bcount(%d)" % (index, limit, change, extra, bcount))
					addLog(extra, step, -1)
			else:
				addLog(-current, step, index)
				box[index]['rest'] -= rest
				break

	return step

def check():
	# Rule1: log = box
	bsum = balance()
	total = 0
	for step in log:
		for move in log[step]:
			total += move['value']
	if total == bsum:
		print('Rule1 [CORRECT]: Valid chain total_log(%d) == balance(%d) : box_len(%d) - log_len(%d)' % (total, bsum, len(box), len(log)))
	else:
		print('Rule1 [ERROR]: Invalid chain total_log(%d) != balance(%d) : box_len(%d) - log_len(%d)' % (total, bsum, len(box), len(log)))
		print('#====================== [REPORT] ======================: ')
		pp.pprint(box)
		pp.pprint(log)
	assert total == bsum
	# Rule2: no Hole after Mountain [CANCELED]
	# bcount = len(box)
	# for a in box:
	# 	if a['rest'] > 0:
	# 		for b in box[a['index']:bcount]:
	# 			if b['rest'] < 0:
	# 				print('Rule2 b(%d) - index(%d) < a(%d) - index(%d)' % (b['rest'], b['index'], a['rest'], a['index']))
	# 				assert b['rest'] < 0

	return total == bsum

def stats():
	mountain = 0
	hole = 0
	plain = 0
	for b in box:
		if b['rest'] > 0:
			mountain += 1
		if b['rest'] < 0:
			hole += 1
		if b['rest'] == 0:
			plain += 1
	print("STATS: mountain(%d) - hole(%d) - plain(%d)" % (mountain, hole, plain))
	return mountain, hole, plain

def seekPlain():
	bcount = len(box)
	for a in box:
		if a['rest'] < 0:
			for b in box[a['index']: bcount]:
				if b['rest'] > 0:
					index = b['index'] - 1
					print("SEEK: %d" % index)
					return index

def revert(step):
	if step in log.keys():
		total = 0
		for move in log[step]:
			total += move['value']
			box[move['index']]['rest'] -= move['value']
		print("Revert total(%d)" % total)
		del log[step]
		vacuum(True)

def vacuum(debug=False):
	print("Vacuum started")
	for b in box:
		index = b['index']
		isLogged = False
		try:
			for step in log:
				# print("Vacuum-step")
				# pp.pprint(step)
				for move in log[step]:
					# print("Vacuum-move")
					# pp.pprint(move)
					if index == move['index']:
						# print("Vacuum-match")
						# pp.pprint(b)
						# pp.pprint(move)
						isLogged = True
						raise Exception("Break")
		except:
			isLogged = True

		if not isLogged:
			try:
				print(type(index))
				del box[index]
				# ReIndexing Log
				for step in log:
					for move in log[step]:
						if move['index'] > index:
							log[step]['index'] -= 1
				if debug:
					print('Box Remove(%d) %d -- [DONE]' % (b['index'], isLogged))
			except Exception as e:
				if debug:
					print('Box Remove(%d) %d -- [FAILED]' % (b['index'], isLogged))
					pp.pprint(e)

def distribution():
	result = {}
	# init
	for b in box:
		result[b['index']] = 0

	for step in log:
		for move in log[step]:
			result[move['index']] += 1
	sorted_x = sorted(result.items(), key=lambda kv: kv[1])
	result = collections.OrderedDict(sorted_x)
	return result

def reset():
	print("-- RESET --")
	global log, box
	log = {}
	box = []

###########################
########## TESTS ##########
###########################

case0 = True
case1 = True
case2 = True
case3 = True
case4 = True

if case0:
	print("############")
	print("# CASE #0  #")
	print("############")

	values = [50, 100, 250, -4000, -1000, 10000, 10000, -5000, -5000, -5000, -5000, -10, 75, -100, -100, -3, 500, -2000, 6000, -6001, 10000, -10001] 
	for value in values:
		if value > 0:
			add(value)
		else:
			sub(-value)
		check()

	pp.pprint(box)
	pp.pprint(log)

	reset()

if case1:
	print("############")
	print("# CASE #1  #")
	print("############")

	check()
	add(50)
	assert box[0]['rest'] == 50
	check()
	add(100)
	assert box[0]['rest'] == 50
	assert box[1]['rest'] == 100
	check()
	add(250)
	assert box[0]['rest'] == 50
	assert box[1]['rest'] == 100
	assert box[2]['rest'] == 250
	assert balance() == 400
	check()
	sub(4000)
	assert box[0]['rest'] == 0
	assert box[1]['rest'] == 0
	assert box[2]['rest'] == -3600
	check()
	# pp.pprint(box)
	sub(1000)
	# pp.pprint(box)
	check()
	add(75)
	check()
	#pp.pprint(box)
	sub(100)
	check()
	#pp.pprint(box)
	sub(100)
	check()
	sub(3)
	check()
	add(500)
	pp.pprint(box)
	# print('balance: %d' % balance())
	check()
	sub(2000)
	check()
	add(6000)
	check()
	sub(6001)
	pp.pprint(box)
	print('\nLog:\n')
	pp.pprint(log)
	print('balance: %d' % balance())
	print('\nRevert:\n')
	check()
	revert(list(log.keys())[0])
	check()
	for step1 in list(log.keys()):
		revert(step1)
		check()
	check()
	pp.pprint(box)
	pp.pprint(log)
	print('balance: %d' % balance())

	reset()

if case2:
	print("############")
	print("# CASE #2  #")
	print("############")

	pp.pprint(box)
	pp.pprint(log)

	check()
	add(50)
	assert box[0]['rest'] == 50
	sub(51)
	assert box[0]['rest'] == -1
	# pp.pprint(box)
	# pp.pprint(log)
	check()
	# exit()
	add(100)
	assert box[0]['rest'] == -1
	assert box[1]['rest'] == 100
	check()
	add(250)
	assert box[0]['rest'] == -1
	assert box[1]['rest'] == 100
	assert box[2]['rest'] == 250
	assert balance() == 349
	check()
	sub(4000, True)
	pp.pprint(box)
	pp.pprint(log)
	assert box[0]['rest'] == -3651
	assert box[1]['rest'] == 0
	assert box[2]['rest'] == 0
	check()
	sub(1000)
	# pp.pprint(box)
	check()
	add(75)
	check()
	#pp.pprint(box)
	sub(100)
	check()
	#pp.pprint(box)
	sub(100)
	check()
	sub(3)
	check()
	add(500)
	pp.pprint(box)
	# print('balance: %d' % balance())
	check()
	sub(2000)
	check()
	add(6000)
	check()
	sub(6001)
	pp.pprint(box)
	print('\nLog:\n')
	pp.pprint(log)
	print('balance: %d' % balance())
	print('\nRevert:\n')
	check()
	revert(list(log.keys())[0])
	check()
	for step1 in list(log.keys()):
		revert(step1)
		check()
	check()
	pp.pprint(box)
	pp.pprint(log)
	print('balance: %d' % balance())

	reset()

if case3:
	print("############")
	print("# CASE #3  #")
	print("############")

	step = sub(100, True)
	assert step >  0
	assert step != None
	assert box[0]['rest'] == -100
	assert log[step][0]['index'] == 0
	assert log[step][0]['value'] == -100
	step = sub(50)
	assert step >  0
	assert step != None
	assert box[0]['rest'] == -150
	assert log[step][0]['index'] == 0
	assert log[step][0]['value'] == -50
	step = sub(25)
	assert step >  0
	assert step != None
	assert box[0]['rest'] == -175
	assert log[step][0]['index'] == 0
	assert log[step][0]['value'] == -25
	step = add(1000)
	assert step >  0
	assert step != None
	assert box[1]['rest'] == 1000
	assert log[step][0]['index'] == 1
	assert log[step][0]['value'] == 1000
	pp.pprint(box)
	pp.pprint(log)

	reset()

if case4:
	print("############")
	print("# CASE #4  #")
	print("############")

	for i in range(9):
		# if i % 2 == 0:
		reset()
		for j in range(1000):
			x = int(random.uniform(0, 1) * 100000)
			if x % 2 == 0:
				add(x)
			else:
				sub(x, x==93093)
			check()
		check()

		# stats()
		# sub(2423228+18450+25406+73356+51369+1)

		pp.pprint(box)
		pp.pprint(log)

		seekPlain()

		pp.pprint(distribution())
		print('Balance: %d' % balance())
		stats()

		# keys = list(log.keys())
		# while len(log) > 0:
		# 	index = int(random.random()*len(keys))
		# 	step = keys[index]
		# 	del keys[index]
		# 	revert(step)
		# 	check()

		# pp.pprint(box)
		# pp.pprint(log)
		# vacuum()
		# pp.pprint(log)
