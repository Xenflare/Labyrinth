import random

def Execute(lootTable):
	pools = lootTable.Pools
	chosenPool = pools[random.randint(1, len(pools))]
	rolls = random.randint(chosenPool['Rolls'][0], chosenPool['Rolls'][1])
	rolls += random.randint(chosenPool['Bonus Rolls'][0], chosenPool['Bonus Rolls'][1])

	recievedItems = {}

	totalWeight = 0
	for entry in chosenPool['Entries']:
		totalWeight += chosenPool['Entries'][entry][1]
	
	for _ in range(rolls):
		randomWeight = random.uniform(0, totalWeight)
		currentWeight = 0
		for entry in chosenPool['Entries']:
			currentWeight += chosenPool['Entries'][entry][1]
			if randomWeight <= currentWeight:
				if entry not in recievedItems:
					recievedItems[entry] = [chosenPool['Entries'][entry][0], random.randint(chosenPool['Entries'][entry][2][0], chosenPool['Entries'][entry][2][1])]
				else:
					recievedItems[entry][1] += random.randint(chosenPool['Entries'][entry][2][0], chosenPool['Entries'][entry][2][1])
				break

	for item in recievedItems:
		if recievedItems[item][1] > recievedItems[item][0].MaxAmount and recievedItems[item][0].MaxAmount > 0:
			recievedItems[item][1] = recievedItems[item][0].MaxAmount
	return recievedItems