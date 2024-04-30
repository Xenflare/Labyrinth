import Loot.Items as Items

class EnemyType():
	def __init__(self, name, description):
		self.Name = name
		self.Explanation = description

skeleton = EnemyType('Skeleton', 'Creatures of bone, held together by the magic of the labyrinth')

class EnemyInstance():
	def __init__(self, name, type, maxHealth, lootTable):
		self.Health = maxHealth
		self.MaxHealth = maxHealth
		self.Type = type
		self.DropLoot = lootTable
		self.Name = name

		self.BleedDuration = 0
		self.BattleEnergy = 0
		self.Inventory = {}

	def GiveItem(self, item, amount):
		inventory = self.Inventory
		if item.Name in inventory:
			inventory[item.Name].Amount += amount
			if inventory[item.Name].Amount > inventory[item.Name].Item.MaxAmount and inventory[item.Name].Item.MaxAmount > 0:
				inventory[item.Name].Amount = inventory[item.Name].Item.MaxAmount
		else:
			inventory[item.Name] = Items.StoredItem(item, amount)