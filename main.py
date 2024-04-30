import os, math, time, random
from Loot import TableReader, Items
from Loot.LootTables import Wood_Chest, Skeleton_Enemy, SkeletonTheif_Enemy, Shop
import Enemies
from Player import Player

registeredCharacters = []
inventory = {}
enemyPresets = {

	'Skeleton' : {

		'Health' : 80,
		'Type' : Enemies.skeleton,
		'Loot' : Skeleton_Enemy,
		'StartingItems' : [(Items.falchion, 1)],
		
	},

	'Skeleton Theif' : {

		'Health' : 60,
		'Type' : Enemies.skeleton,
		'Loot' : SkeletonTheif_Enemy,
		'StartingItems' : [(Items.dagger, 1)],

	},
	
}
enemies = ['Skeleton', 'Skeleton Theif']
enemyWeights = [25, 20]

class StarterCharacter():
	def __init__(self, name, description, startingItemPairs):
		self.Name = name
		self.Description = description
		self.DefaultItems = startingItemPairs
		
		registeredCharacters.append(self)

class Container():
	def __init__(self, name, linkedLootTable):
		self.Name = name
		self.Locked = random.choice([False, True])
		self.Loot = linkedLootTable

class Room():
	def __init__(self, isFirstRoom=False, connectedToShop=False):
		self.ForwardExit = random.choice([False, True])
		self.BackwardExit = True
		self.LeftExit = random.choice([False, True])
		self.RightExit = random.choice([False, True])
		self.HasFight = False
		self.HasShop = False
		if not isFirstRoom:
			self.HasFight = random.choice([False, True])
			if self.HasFight is False and not connectedToShop:
				self.HasShop = random.choices([False,True],[4,1])
		self.Choices = []
		self.Enemies = []
		self.Containers = []

		if self.ForwardExit is True:
			self.Choices.append('Go Forward')
		if self.RightExit is True:
			self.Choices.append('Go Right')
		if self.LeftExit is True:
			self.Choices.append('Go Left')
		self.Choices.append('Go Backward')
		
		if self.HasFight:
			selectedEnemies = random.choices(enemies, weights=enemyWeights, k=random.randint(1,2))
			for eNum in range(len(selectedEnemies)):
				enemyObject = Enemies.EnemyInstance(selectedEnemies[eNum], enemyPresets[selectedEnemies[eNum]]['Type'], enemyPresets[selectedEnemies[eNum]]['Health'], enemyPresets[selectedEnemies[eNum]]['Loot'])
				self.Enemies.append([selectedEnemies[eNum], enemyObject])
				for startItem in enemyPresets[selectedEnemies[eNum]]['StartingItems']:
					enemyObject.GiveItem(startItem[0], startItem[1])
		chance = 25
		for _ in range(4):
			if random.uniform(1, 100) < chance:
				break
			else:
				chance += 10
				containerRand = random.uniform(1,100)
				if containerRand < 100:
					self.Containers.append(['Wood Chest', Container('Wood_Chest', Wood_Chest)])

	def Loaded(self):
		if self.ForwardExit is True:
			self.FRoom = Room(False, self.HasShop)
		if self.RightExit is True:
			self.RRoom = Room(False, self.HasShop)
		if self.LeftExit is True:
			self.LRoom = Room(False, self.HasShop)
		self.BRoom = Room(False, self.HasShop)

class NPC():
	def __init__(self, name, playerKnowsName=False, nameColor='white'):
		self.Name = name
		self.Known = playerKnowsName
		self.NameColor = nameColor

	def Talk(self, string):
		sName = self.Name
		if self.Known is not True:
			sName = '???'
		print(f"\n({ColoredString(sName, self.NameColor)}): {string}\n")

def Clear():
	os.system('clear')

def ColoredString(string='', color='white', formatNumber=0):
	color = color.lower()
	colors = {'white' : f'\033[{formatNumber};37m',
						'red' : f'\033[{formatNumber};31m',
						'green' : f'\033[{formatNumber};32m',
						'blue' : f'\033[{formatNumber};34m',
						'orange' : f'\033[{formatNumber};33m',
					 	'yellow' : f'\033[{formatNumber};93m',
					 	'purple' : f'\033[{formatNumber};35m'}
	return colors[color] + string + '\033[0m'

def ShowTitle():
	titleText = ColoredString('• THE LABYRINTH •', 'red', 1)
	print('\n\n' + titleText + '\n')
	print('|  Play  |')
	print('\n')

def ShowOptions(options, optionIndex=None, added=0, style='Normal'):
	if optionIndex is None:
		if style == 'Normal':
			print('------------------\n')
			for num in range(len(options)):
				print(f'({num+added}) - {options[num]}\n')
			print('------------------\n')
		elif style == 'Enemies':
			print('------------------\n')
			for num in range(len(options)):
				bleedAdd = ''
				if options[num][1].BleedDuration > 0:
					bleedAdd = ColoredString(f'(Bleeding for {options[num][1].BleedDuration} turns)', 'red')
				print(f'({num+added}) - {options[num][0]} : ({options[num][1].Health}/{options[num][1].MaxHealth}) ({options[num][1].BattleEnergy} Energy) {bleedAdd}\n')
			print('------------------\n')
		elif style == 'Rooms':
			print('------------------\n')
			for num in range(len(options)):
				enemyAdd = ''
				if ((options[num] == 'Go Left' and occupiedRoom.LRoom.HasFight is True) or (options[num] == 'Go Right' and occupiedRoom.RRoom.HasFight is True) or (options[num] == 'Go Forward' and occupiedRoom.FRoom.HasFight is True) or (options[num] == 'Go Backward' and occupiedRoom.BRoom.HasFight is True)) and "Explorer's Map" in inventory:
					enemyAdd = '(The map displays a sword on this room)'
				print(f'({num+added}) - {options[num]} {enemyAdd}\n')
			print('------------------\n')
		elif style == 'ShopItems':
			print('------------------\n')
			for num in range(len(options)):
				print(f'({num+added}) - {options[num].Name}')
				print(f"  | {options[num].SaleDescription}")
				print(f"  | Costs {ColoredString(str(options[num].Value), 'yellow', 1)} coins\n")
			print('------------------\n')
	else:
		if style == 'Normal':
			print('------------------\n')
			for num in range(len(options)):
				print(f'({num+added}) - {options[num][optionIndex]}\n')
			print('------------------\n')
		elif style == 'Enemies':
			print('------------------\n')
			for num in range(len(options)):
				bleedAdd = ''
				if options[num][1].BleedDuration > 0:
					bleedAdd = ColoredString(f'(Bleeding for {options[num][1].BleedDuration} turns)', 'red')
				print(f'({num+added}) - {options[num][optionIndex]} : ({options[num][1].Health}/{options[num][1].MaxHealth}) ({options[num][1].BattleEnergy} Energy) {bleedAdd}\n')
			print('------------------\n')
		elif style == 'Rooms':
			print('------------------\n')
			for num in range(len(options)):
				enemyAdd = ''
				if ((options[num][optionIndex] == 'Go Left' and occupiedRoom.LRoom.HasFight is True) or (options[num][optionIndex] == 'Go Right' and occupiedRoom.RRoom.HasFight is True) or (options[num][optionIndex] == 'Go Forward' and occupiedRoom.FRoom.HasFight is True) or (options[num][optionIndex] == 'Go Backward' and occupiedRoom.BRoom.HasFight is True)) and "Explorer's Map" in inventory:
					enemyAdd = '(The map displays a sword on this room)'
				print(f'({num+added}) - {options[num][optionIndex]} {enemyAdd}\n')
			print('------------------\n')
		elif style == 'ShopItems':
			print('------------------\n')
			for num in range(len(options)):
				print(f'({num+added}) - {options[num][optionIndex].Name}')
				print(f"  | {options[num][optionIndex].SaleDescription}")
				print(f"  | Costs {ColoredString(str(options[num][optionIndex].Value), 'yellow', 1)} coins\n")
			print('------------------\n')
			
def ShowInventory(categoryToShow=None, invTitle='Inventory', isSelectionMenu=False, categoryToExclude=None, showSellAmounts=False):
	print(f'\n	{invTitle}')
	print('------------------\n')
	shownItems = []
	cNum = -1
	for item in inventory:
		item = inventory[item]
		if (item.Item.Category == categoryToShow or categoryToShow is None) and (item.Item.Category != categoryToExclude or categoryToExclude is None):
			if type(item.Item) is Items.Item:
				cNum += 1
				shownItems.append(item.Item.Name)
				addin = ''
				if isSelectionMenu:
					addin = ColoredString('(Type ' + str(cNum) + ' to select)', 'blue', 1)
				print(f" ({item.Amount}x) {ColoredString(item.Item.Name, 'white', 1)} {addin}")
				if not showSellAmounts:
					print(f"  | {item.Item.Description}")
					print(f"  | {item.Item.SaleDescription}")
				else:
					print(f"  | Sells for {ColoredString(str(item.Item.Value), 'yellow', 1)} coins")
			elif type(item.Item) is Items.StatItem:
				print(f" ({item.Amount}x) {item.Item.Name}")
			print()
	print('------------------\n')
	return shownItems

def ShowPlayerStats(isActing=True):
	bleedAdd = ''
	if player.BleedDuration > 0:
		bleedAdd = ColoredString(f'(Bleeding for {player.BleedDuration} turns)', 'red')
	print(f'			{ColoredString(player.Name, "white", 1)}')
	print('--------------------------------', bleedAdd)
	print(f"HP: {player.HP} / {player.MHP} | Energy: {player.BattleEnergy}")
	if isActing:
		print(f'	{ColoredString("Attack", "white", 1)} - {ColoredString("Items", "white", 1)} - {ColoredString("End turn", "white", 1)}\n')
	else:
		print(f'	{ColoredString("It is not your turn", "red", 1)}\n')
	

def showWeaponAbilitiesAsChoices(abilityList):
	print('\n	Weapon Abilities')
	print('-------------------------')
	print(ColoredString(f"You have {player.BattleEnergy} energy\n", 'yellow', 1))
	for a in range(len(abilityList)):
		dmgDescribe = ''
		critDescribe = ''
		bleedDescribe = ''
		if abilityList[a].DMG[1] < 1:
			dmgDescribe = 'Cannot deal damage'
		else:
			dmgDescribe = f"{abilityList[a].DMG[0]}-{abilityList[a].DMG[1]} damage"
		if abilityList[a].BleedChance > 0 and abilityList[a].BleedDuration > 0:
			bleedDescribe = f", {abilityList[a].BleedChance}% chance to cause {abilityList[a].BleedDuration} turns of bleeding"
		print(f"  ({a}) - {abilityList[a].Name} : {dmgDescribe}{bleedDescribe}")
		print(ColoredString(f"	  {abilityList[a].RequiredEnergy} energy will be used", 'yellow'))
		print()
	print('-------------------------\n')

def showCharacterOptions():
	print('\nChoose a character:\n')
	for charNum in range(len(registeredCharacters)):
		print(ColoredString(f"	({charNum + 1}) - {registeredCharacters[charNum].Name}", 'white', 1))
		print(f"	  {registeredCharacters[charNum].Description}")
		print()

def GiveItem(item, amount):
	if item.Name in inventory:
		inventory[item.Name].Amount += amount
		if inventory[item.Name].Amount > inventory[item.Name].Item.MaxAmount and inventory[item.Name].Item.MaxAmount > 0:
			inventory[item.Name].Amount = inventory[item.Name].Item.MaxAmount
	else:
		inventory[item.Name] = Items.StoredItem(item, amount)

def TakeItem(item, amount):
	if item.Name in inventory:
		inventory[item.Name].Amount -= amount
		if inventory[item.Name].Amount <= 0:
			del inventory[item.Name]

basicCharacter = StarterCharacter('Fighter',
																	'Skilled with weapons, slight training in magic',
																 [(Items.coin, 35), (Items.mediumHealingPotion, 5), (Items.armingSword, 1)])

quickCharacter = StarterCharacter('Assassin',
																	'Quick and precise but not made to take a hit',
																 [(Items.coin, 35), (Items.mediumHealingPotion, 5), (Items.dagger, 1)])

magicCharacter = StarterCharacter('Mage',
																	'Well trained with magic but missing advanced combat abilities',
																 [(Items.coin, 35), (Items.mediumHealingPotion, 5), (Items.staff, 1)])

strongCharacter = StarterCharacter('Brute',
																	 'Tough and very good with weapons, has never even heard of magic',
																	[(Items.coin, 35), (Items.mediumHealingPotion, 5), (Items.warAxe, 1)])

ISTxt = ['stop','quit','exit','leave','finish','done','close']

while True:
	blacksmith = NPC('Blacksmith', False, 'yellow')
	titleScreenLoop = True
	gameLoop = True
	player = Player('', None, 100)
	occupiedRoom = None
	inventory = {}
	while titleScreenLoop:
		Clear()
		ShowTitle()
		action = input("Choose what to do > ").lower()
		if action == 'play':
			Clear()
			titleScreenLoop = False
	chooseLoop = True
	while chooseLoop:
		showCharacterOptions()
		charChoice = input('> ')
		if charChoice.isdigit():
			charChoice = int(charChoice)
			if charChoice < (len(registeredCharacters) + 1) and charChoice > 0:
				player.Class = registeredCharacters[charChoice - 1]
				for startItem in player.Class.DefaultItems:
					GiveItem(startItem[0], startItem[1])
				chooseLoop = False
		Clear()
	namingLoop = True
	while namingLoop:
		player.Name = input(f"\nWhat is your {player.Class.Name.lower()}'s name? > ").title()
		if len(player.Name) >= 2 and len(player.Name) <= 15:
			namingLoop = False
		elif len(player.Name) < 2:
			Clear()
			print(ColoredString('Name too short!', 'red', 0))
		elif len(player.Name) > 15:
			Clear()
			print(ColoredString('Name too long!', 'red', 0))
	Clear()
	print('\nThe world fades in around you...\n')
	input('> ')
	Clear()
	print("\nYou see someone standing in the corner of the room you're in, they are near an anvil.\n")
	input('> ')
	Clear()
	blacksmith.Talk("Ah. Another of The Fallen.")
	tcnb = "'Another of the fallen'"
	t1Options = ['Say Nothing', f'" What do you mean, {tcnb}? "', '" Who are you? "']
	talkin1 = True
	while talkin1:
		ShowOptions(t1Options)
		tOption = input('Text choice > ').lower()
		Clear()
		if tOption.isdigit():
			tOption = int(tOption)
			if tOption == 1 and f'" What do you mean, {tcnb}? "' in t1Options:
				t1Options.remove(f'" What do you mean, {tcnb}? "')
				blacksmith.Talk("People are here often, I named them 'The Fallen'")
				input('> ')
			elif tOption == 2 and '" Who are you? "' in t1Options:
				t1Options.remove('" Who are you? "')
				blacksmith.Known = True
				blacksmith.Talk("I am the blacksmith, known by no other name")
				input('> ')
			else:
				talkin1 = False
				print("\nYou say nothing\n")
				input('> ')
		else:
			talkin1 = False
			print("\nYou say nothing\n")
			input('> ')
		Clear()
	blacksmith.Talk("When you are ready, enter the door on the other side of this room.")
	input('> ')
	Clear()
	blacksmith.Talk("It will take you into The Labyrinth")
	input('> ')
	Clear()
	blacksmith.Talk("I cannot say exactly what you will find, or when you will get out. The layout changes every time you go through a room.")
	input('Press enter when ready > ')
	Clear()
	occupiedRoom = Room(True)
	while gameLoop:
		occupiedRoom.Loaded()
		if occupiedRoom.HasFight:
			battleLoop = True
			player.BattleEnergy = 0
			player.BleedDuration = 0
			print('\nBattle Initiated')
			ShowOptions(occupiedRoom.Enemies, None, 1, 'Enemies')
			input('> ')
			Clear()
			while battleLoop:
				player.BattleEnergy += len(occupiedRoom.Enemies)
				pTurnLoop = True
				for enemy in occupiedRoom.Enemies:
					if enemy[1].BleedDuration > 0:
						enemy[1].BleedDuration -= 1
						enemy[1].Health -= 2
				while pTurnLoop:
					print('\n	Enemies')
					ShowOptions(occupiedRoom.Enemies, None, 1, 'Enemies')
					ShowPlayerStats()
					decision = input('Select an action > ').lower()
					atkPossibilities = ['attack', 'a', 'atk', 'atack', 'sttack', 'attakc']
					itmPossibilities = ['items', 'i', 'item', 'inventory']
					if decision in atkPossibilities:
						looking = True
						while looking:
							Clear()
							weapons = ShowInventory('Weapons', 'Weapons', True)
							act = input('Choose a weapon > ').lower()
							if act in ISTxt:
								looking = False
							elif act.isdigit():
								act = int(act)
								if act >= 0 and act < len(weapons):
									looking = False
									usingWeapon = inventory[weapons[act]]
									Clear()
									print('\n	Enemies')
									ShowOptions(occupiedRoom.Enemies, None, 1, 'Enemies')
									print(f"You are using your {ColoredString(usingWeapon.Item.Name, 'white', 1)}")
									showWeaponAbilitiesAsChoices(usingWeapon.Item.Abilities)
									aNum = input('Number of the ability to use > ')
									if aNum.isdigit():
										aNum = int(aNum)
										if aNum >= 0 and aNum < len(usingWeapon.Item.Abilities):
											Clear()
											print('\n	Enemies')
											ShowOptions(occupiedRoom.Enemies, None, 1, 'Enemies')
											if player.BattleEnergy >= usingWeapon.Item.Abilities[aNum].RequiredEnergy:
												target = input(f"Which enemy do you want to target with {ColoredString(usingWeapon.Item.Abilities[aNum].Name, 'white', 1)} > ")
												if target.isdigit():
													target = int(target) - 1
													if target >= 0 and target < len(occupiedRoom.Enemies):
														TargetedEnemy = occupiedRoom.Enemies[target][1]
														damageDealt = usingWeapon.Item.Abilities[aNum].Trigger(TargetedEnemy)
														player.BattleEnergy -= usingWeapon.Item.Abilities[aNum].RequiredEnergy
														if TargetedEnemy.Health <= 0:
															player.Kills += 1
															Clear()
															rItems = TableReader.Execute(TargetedEnemy.DropLoot)
															print('\n		 ' + TargetedEnemy.Type.Name + ' Drops')
															print('---------------------------------\n')
															for item in rItems:
																print(f'  {rItems[item][1]}x - {item}\n')
																GiveItem(rItems[item][0], rItems[item][1])
															print('---------------------------------\n')
															input('> ')
															occupiedRoom.Enemies.remove(occupiedRoom.Enemies[target])
											else:
												print(ColoredString('You do not have enough energy to use this ability\n', 'red', 1))
												input('> ')
					elif decision in itmPossibilities:
						looking = True
						while looking:
							Clear()
							invItems = ShowInventory('Usable', 'Items')
							act = input('(use or discard) > ').lower()
							if act in ISTxt:
								looking = False
							elif act == 'use':
								Clear()
								ShowInventory('Usable', 'Items', True)
								selectItem = input('Type the number of the item to use > ')
								if selectItem.isdigit():
									selectItem = int(selectItem)
									if selectItem >= 0 and selectItem < len(invItems):
										itemUsing = inventory[invItems[selectItem]]
										TakeItem(itemUsing.Item, 1)
										for event in itemUsing.Item.UseEvents:
											event.Trigger(player)
					if len(occupiedRoom.Enemies) <= 0 or player.BattleEnergy <= 0 or decision == 'end turn':
						pTurnLoop = False
					Clear()
				for enemy in occupiedRoom.Enemies:
					enemy[1].BattleEnergy += 1
				if len(occupiedRoom.Enemies) > 0:
					Clear()
					print('\n	Enemies')
					ShowOptions(occupiedRoom.Enemies, None, 1, 'Enemies')
					print("It is the enemies' turn\n")
					input('> ')
					eNum = 0
					if player.BleedDuration > 0:
						player.BleedDuration -= 1
						player.HP -= 2
					for enemy in occupiedRoom.Enemies:
						eNum += 1
						eTurnLoop = False
						if player.HP > 0:
							eTurnLoop = True
						while eTurnLoop:
							if random.randint(1,100) < 75:
								enemyUsingWeapon = None
								abilityToUse = None
								highestDamage = 0
								for item in enemy[1].Inventory:
									if enemy[1].Inventory[item].Item.Category == 'Weapons':
										totalDamageFactor = 0
										for ability in enemy[1].Inventory[item].Item.Abilities:
											totalDamageFactor += ability.DMG[1]
										totalDamageFactor /= len(enemy[1].Inventory[item].Item.Abilities)
										if totalDamageFactor > highestDamage:
											highestDamage = totalDamageFactor
											enemyUsingWeapon = enemy[1].Inventory[item]
								if enemyUsingWeapon is not None:
									highestOutput = 0
									for ability in enemyUsingWeapon.Item.Abilities:
										if ability.DMG[1] > highestOutput and enemy[1].BattleEnergy >= ability.RequiredEnergy:
											highestOutput = ability.DMG[1]
											abilityToUse = ability
								if abilityToUse is not None:
									dealtDamage = abilityToUse.Trigger(player)
									enemy[1].BattleEnergy -= abilityToUse.RequiredEnergy
									Clear()
									print('\n	Enemies')
									ShowOptions(occupiedRoom.Enemies, None, 1, 'Enemies')
									ShowPlayerStats(False)
									print(f"{ColoredString(f'({eNum}) - {enemy[0]}', 'white', 1)} used {ColoredString(abilityToUse.Name, 'white', 1)} with their {ColoredString(enemyUsingWeapon.Item.Name, 'white', 1)} and dealt {ColoredString(str(dealtDamage), 'red', 1)} damage\n")
									input('> ')
									if player.HP <= 0:
										Clear()
										print(f"\nYou died to {ColoredString(enemy[0], 'white', 1)}")
										print(f"You killed {ColoredString(str(player.Kills), 'red', 1)} enemies on your journey")
										print()
										input('> ')
										eTurnLoop = False
										gameLoop = False
										battleLoop = False
								else:
									eTurnLoop = False
									Clear()
									print('\n	Enemies')
									ShowOptions(occupiedRoom.Enemies, None, 1, 'Enemies')
									ShowPlayerStats(False)
									print(f"{ColoredString(f'({eNum}) - {enemy[0]}', 'white', 1)} skipped their turn\n")
									input('> ')
								if enemy[1].BattleEnergy < 1:
									eTurnLoop = False
							else:
								eTurnLoop = False
								Clear()
								print('\n	Enemies')
								ShowOptions(occupiedRoom.Enemies, None, 1, 'Enemies')
								ShowPlayerStats(False)
								print(f"{ColoredString(f'({eNum}) - {enemy[0]}', 'white', 1)} skipped their turn\n")
								input('> ')
				if len(occupiedRoom.Enemies) <= 0:
					battleLoop = False
				Clear()
		if occupiedRoom.HasShop:
			shopLoop = True
			shopItems = []
			itemsToBeInShop = TableReader.Execute(Shop)
			for item in itemsToBeInShop:
				shopItems.append(itemsToBeInShop[item][0])
			while shopLoop:
				Clear()
				blacksmith.Talk('Look around the shop as long as you like.')
				bOs = input('(buy or sell) > ').lower()
				bA = ['buy', 'by', 'b']
				sAlt = ['sell', 'sel', 's']
				if bOs in bA:
					purchasingLoop = True
					while purchasingLoop:
						Clear()
						print('\n	Shop Items')
						ShowOptions(shopItems, None, 0, 'ShopItems')
						numberOfCoins = 0
						if 'Coin' in inventory:
							numberOfCoins = inventory['Coin'].Amount
						print(f"You have {ColoredString(str(numberOfCoins), 'yellow', 1)} coins")
						buyer = input('Type the number for the item you want to buy > ').lower()
						if buyer.isdigit():
							buyer = int(buyer)
							if buyer >= 0 and buyer < len(shopItems):
								Clear()
								print(f'\nHow many {ColoredString(shopItems[buyer].Name, "white", 1)}s do you want to buy?\n')
								purchaseNum = input('enter an integer > ')
								if purchaseNum.isdigit():
									purchaseNum = int(purchaseNum)
									itemToBuy = shopItems[buyer]
									totalCost = itemToBuy.Value * purchaseNum
									if totalCost > numberOfCoins:
										Clear()
										print(f"\nThis transaction requires {ColoredString(str(totalCost), 'yellow', 1)} coins, you only have {ColoredString(str(numberOfCoins), 'yellow', 1)}\n")
										input('> ')
									else:
										TakeItem(Items.coin, totalCost)
										GiveItem(itemToBuy, purchaseNum)
						elif buyer in ISTxt:
							purchasingLoop = False
				elif bOs in sAlt:
					Clear()
					SellableItems = ShowInventory(None, "Items", True, 'Stats', True)
					seller = input('Type the number for the item you want to sell > ').lower()
				elif bOs in ISTxt:
					Clear()
					shopLoop = False
					moveOpt = 0
					if occupiedRoom.Choices[moveOpt] == 'Go Forward':
						occupiedRoom = occupiedRoom.FRoom
					elif occupiedRoom.Choices[moveOpt] == 'Go Right':
						occupiedRoom = occupiedRoom.RRoom
					elif occupiedRoom.Choices[moveOpt] == 'Go Left':
						occupiedRoom = occupiedRoom.LRoom
					elif occupiedRoom.Choices[moveOpt] == 'Go Backward':
						occupiedRoom = occupiedRoom.BRoom
		else:
			decision = False
			while not decision and player.HP > 0:
				print("\nBefore each number type 'P' to specify player action")
				ShowOptions(['View inventory'])
				if len(occupiedRoom.Containers) > 0:
					print("Before each number type 'I' to specify interacting")
					ShowOptions(occupiedRoom.Containers, 0)
				print("Before each number type 'M' to specify movement")
				ShowOptions(occupiedRoom.Choices, None, 0, 'Rooms')
				moveOpt = input('Type action > ')
				if len(moveOpt.split('M')) == 2:
					moveOpt = moveOpt.split('M')[1]
					if moveOpt.isnumeric:
						moveOpt = int(moveOpt)
						if moveOpt <= len(occupiedRoom.Choices) - 1 and moveOpt >= 0:
							if occupiedRoom.Choices[moveOpt] == 'Go Forward':
								occupiedRoom = occupiedRoom.FRoom
							elif occupiedRoom.Choices[moveOpt] == 'Go Right':
								occupiedRoom = occupiedRoom.RRoom
							elif occupiedRoom.Choices[moveOpt] == 'Go Left':
								occupiedRoom = occupiedRoom.LRoom
							elif occupiedRoom.Choices[moveOpt] == 'Go Backward':
								occupiedRoom = occupiedRoom.BRoom
							decision = True
				elif len(moveOpt.split('I')) == 2:
					moveOpt = moveOpt.split('I')[1]
					if moveOpt.isnumeric:
						moveOpt = int(moveOpt)
						if moveOpt <= len(occupiedRoom.Containers) - 1 and moveOpt >= 0:
							Clear()
							rItems = TableReader.Execute(occupiedRoom.Containers[moveOpt][1].Loot)
							print('\n		  ' + occupiedRoom.Containers[moveOpt][0])
							print('---------------------------------\n')
							for item in rItems:
								print(f'  {rItems[item][1]}x - {item}\n')
								GiveItem(rItems[item][0], rItems[item][1])
							print('---------------------------------\n')
							input('> ')
							occupiedRoom.Containers.remove(occupiedRoom.Containers[moveOpt])
				elif len(moveOpt.split('P')) == 2:
					moveOpt = moveOpt.split('P')[1]
					if moveOpt.isdigit():
						moveOpt = int(moveOpt)
						if moveOpt == 0:
							looking = True
							while looking:
								Clear()
								ShowInventory()
								act = input('What to do > ').lower()
								if act in ISTxt:
									looking = False
				Clear()