from AbilityClasses import SwingAttack
from UseEvents import Coagulate, Heal


class Item(): # A usable object, such as armor or weapons
	def __init__(self, name, description, shopDescription, price, limit, category, weaponValues=None, consumableValues=None):
		self.Name = name
		self.Description = description
		self.SaleDescription = shopDescription
		self.Value = price
		self.MaxAmount = limit
		self.Category = category
		self.IsWeapon = False
		self.IsConsumable = False
		if weaponValues:
			self.IsWeapon = True
			self.Abilities = weaponValues[0]
		if consumableValues:
			self.IsConsumable = True
			self.UseEvents = consumableValues[0]

class StatItem(): # A non-physical item that has no value in combat or interaction, such as coins
	def __init__(self, name):
		self.Name = name
		self.MaxAmount = -1
		self.Category = 'Stats'

class StoredItem(): # These are used as an inventory container of an item
	def __init__(self, item, amount):
		self.Item = item
		self.Amount = amount

coin = StatItem('Coin')
armingSword = Item('Arming Sword', 'A medium sword with a thin hilt', '10-20 Damage, 2x Crit', 20, 1, 'Weapons', [[SwingAttack('Slash', (10,20), 0, 0, 1), SwingAttack('Critical Strike', (20,40), 0, 0, 2)]])
claymoore = Item('Claymoore', 'A long sword with a wide hilt', '12-25 Damage, 2x Crit', 145, 1, 'Weapons', [[SwingAttack('Slash', (12,25), 0, 0, 1), SwingAttack('Critical Strike', (24,50), 0, 0, 2)]])
falchion = Item('Falchion', 'A single edged sword similar to an arming sword', '8-18 Damage, 2.4x Crit', 65, 1, 'Weapons', [[SwingAttack('Slash', (8,18), 0, 0, 1), SwingAttack('Critical Strike', (19,43), 0, 0, 2)]])
warAxe = Item('War Axe', 'An axe head attached to a short pole', '17-25 Damage, 1.5x Crit', 20, 1, 'Weapons', [[SwingAttack('Chop', (17,25), 0, 0, 1), SwingAttack('Critical Strike', (26,38), 0, 0, 2)]])
bashingMace = Item('Bashing Mace', 'A studded ball on the end of a large handle', '8-22 Damage, 1.75x Crit, penetrates armor', 100, 1, 'Weapons', [[SwingAttack('Bash', (8,22), 0, 0, 1), SwingAttack('Critical Strike', (14,39), 0, 0, 2)]])
dagger = Item('Dagger', 'A small curved blade with a short hilt', '7-12 Damage, 2x Crit, causes bleed', 20, 1, 'Weapons', [[SwingAttack('Stab', (7,12), 40, 3, 1), SwingAttack('Critical Strike', (14,24), 60, 8, 2)]])
staff = Item('Arcane Staff', 'The roots of a tree curved around a crystal', 'Able to use many magic abilities', 20, 1, 'Weapons', [[]])
smallHealingPotion = Item('Health Vial', 'A thin glass tube containing a red liquid', 'Heals 10 HP when used', 5, -1, 'Usable', None, [[Heal(10)]])
mediumHealingPotion = Item('Health Potion', 'A rounded bottle containing a red liquid', 'Heals 25 HP when used', 12, -1, 'Usable', None, [[Heal(25)]])
largeHealingPotion = Item('Health Elixer', 'A triangular flask containing a bright red liquid', 'Heals 50 HP when used, and stops bleeding', 25, -1, 'Usable', None, [[Heal(50), Coagulate()]])
map = Item("Explorer's Map", 'Old parchment that seems to shift with the labyrinth', 'Shows the contents of nearby rooms', 120, 1, 'Passive')