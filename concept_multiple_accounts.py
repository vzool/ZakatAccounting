import time
import pprint

pp = pprint.PrettyPrinter()

account = {}
log = {}

def newStep():
	print("STEP: %s" % step)
	return time.time()

def newAccountID():
	if len(account) == 0:
		return 0
	return sorted(account.keys())[-1]+1

def createAccount(name):
	id = newAccountID()
	account[id] = {
		'name': name,
		'box': [],
	}
	return id

def add(account_no, value, step=0):
	print('add (%d)(%d): %d' % (account_no, len(account[account_no]['box']), value))
	addLog(account_no, value, step)
	account[account_no]['box'].append({'index': len(account[account_no]['box']),'capital': value, 'rest': value, 'time': time.time()})
	return step

def addLog(account_no, value, step=0, index=0):
	# print('AddLog(Pre): value(%d) step(%d) index(%d)' % (value, step, index))
	if value == 0:
		return
	current = len(account[account_no]['box'])
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
	log[step].append({'account': account_no, 'index': current, 'value': value})
	return step

def balance(account_no=-1):
	total = 0
	if account_no == -1:
		accounts = list(account.keys())
	else:
		accounts = [account_no]
	for acc in accounts:
		for row in account[acc]['box']:
			total += row['rest']
	return total

def sub(account_no, value, step=0, debug=False):

	print('sub: %d' % value)

	rest = value
	total = balance(account_no)

	if total < value:
		print('Warning: ask for %d insufficient balance: %d' % (value,total))

	bcount = len(account[account_no]['box'])
	if step == 0:
		step = newStep()
	limit = -(bcount+1)

	for index in range(-1, limit, -1):

		if rest <= account[account_no]['box'][index]['rest']:
			account[account_no]['box'][index]['rest'] -= rest
			addLog(account_no, -rest, step, index)
			break
		else:
			total = balance(account_no) # debug
			current = account[account_no]['box'][index]['rest']
			change = current - rest

			if debug:
				print("Loop: account(%d) - index(%d) - current(%d) - rest(%d) - change(%d) - total(%d) - limit(%d)" % 
					(account_no, index, current, rest, change, total, limit)) # debug

			if current < 0:
				account[account_no]['box'][index]['rest'] += -rest
				addLog(-rest, step, index)
				break

			if change < 0:
				if total < 0:
					account[account_no]['box'][-1]['rest'] = change
					addLog(account_no, -rest, step, index)
					break

				extra = 0
				rest = -change

				if index-1 == limit:
					extra = -rest
					account[account_no]['box'][-1]['rest'] = extra
				else:
					account[account_no]['box'][index]['rest'] = 0

				addLog(account_no, -current, step, index)

				if index-1 == limit:
					addLog(account_no, extra, step, -1)
			else:
				addLog(account_no, -current, step, index)
				account[account_no]['box'][index]['rest'] -= rest
				break
		return step

def revert(step):
	if step in log.keys():
		for move in log[step]:
			account[move['account']]['box'][move['index']]['rest'] -= move['value']
		del log[step]

def check():
	bsum = balance()
	total = 0
	for step in log:
		for move in log[step]:
			total += move['value']
	if total == bsum:
		print('[CORRECT]: Valid chain total_log(%d) == balance(%d)' % (total, bsum))
	else:
		print('[ERROR]: Invalid chain total_log(%d) != balance(%d)' % (total, bsum))
	assert total == bsum
	return total == bsum

def transfer(from_account, to_account, value, debug=True):
	step = newStep()
	sub(from_account, value, step=step, debug=debug)
	add(to_account, value, step=step)
	return step


pp.pprint(account)
wallet = createAccount('Wallet')
alinma = createAccount('Alinma Bank')
alBilad = createAccount('Al-Bilad Bank')
# check()
# add(wallet, 1000)
# check()
# add(wallet, 2500)
# check()
# add(wallet, 5000)
# check()
# add(alinma, 13500)
# check()
add(alBilad, 60000)
check()
pp.pprint(balance())
# print('Wallet: %d' % balance(wallet))
# print('Alinma: %d' % balance(alinma))
# print('Al-Bilad: %d' % balance(alBilad))
sub(alBilad, 60001)
# check()
# print('Wallet: %d' % balance(wallet))
# print('Alinma: %d' % balance(alinma))
print('Al-Bilad: %d' % balance(alBilad))
pp.pprint(account)
pp.pprint(log)
# pp.pprint(balance())
# print('\nRevert:\n')
# revert(list(log.keys())[-1])
# pp.pprint(account)
# pp.pprint(log)
check()
# print('\nTransfer:\n')
# transfer(alBilad, alinma, 60001, True)
# check()
# add(alBilad, 100)
# pp.pprint(account)
# pp.pprint(log)
# check()

# for step1 in list(log.keys()):
# 	revert(step1)
# 	check()