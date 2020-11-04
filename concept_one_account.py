import time
import pprint
import random

random.seed(3)

pp = pprint.PrettyPrinter()

log = {}
box = []

def newStep():
	step = time.time()
	print("STEP: %s" % step)
	return step

def add(value, step=0):
	print('add (%d): %d' % (len(box), value))
	if step == 0:
		step = newStep()
	addLog(value, step=step)
	box.append({'index': len(box),'capital': value, 'rest': value, 'time': time.time()})
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

			if current < 0:
				box[index]['rest'] += -rest
				addLog(-rest, step, index)
				break

			if change <= 0:
				if total < 0:
					box[-1]['rest'] = change
					addLog(-rest, step, index)
					break

				extra = 0
				rest = -change

				if index-1 == limit:
					extra = -rest
					print("HIT(A): index(%d) - limit(%d) - change(%d) - extra(%d) - bcount(%d)" % (index, limit, change, extra, bcount))
					box[-1]['rest'] = extra
				
				if bcount > 1:
					box[index]['rest'] = 0
				addLog(-current, step, index)

				if index-1 == limit:
					print("HIT(B): index(%d) - limit(%d) - change(%d) - extra(%d) - bcount(%d)" % (index, limit, change, extra, bcount))
					addLog(extra, step, -1)
			else:
				addLog(-current, step, index)
				box[index]['rest'] -= rest
				break

	return step

def revert(step):
	if step in log.keys():
		for move in log[step]:
			box[move['index']]['rest'] -= move['value']
		del log[step]

def check():
	bsum = balance()
	total = 0
	for step in log:
		for move in log[step]:
			total += move['value']
	if total == bsum:
		print('[CORRECT]: Valid chain total_log(%d) == balance(%d) : box_len(%d) - log_len(%d)' % (total, bsum, len(box), len(log)))
	else:
		print('[ERROR]: Invalid chain total_log(%d) != balance(%d) : box_len(%d) - log_len(%d)' % (total, bsum, len(box), len(log)))
		print('#====================== [REPORT] ======================: ')
		pp.pprint(box)
		pp.pprint(log)
	assert total == bsum
	return total == bsum

def reset():
	print("-- RESET --")
	global log, box
	log = {}
	box = []

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
			sub(x)
		check()
	check()

	pp.pprint(box)
	pp.pprint(log)
