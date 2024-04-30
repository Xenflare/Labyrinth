class Player():
	def __init__(self, name, pClass, maxHealth):
		self.Name = name
		self.Class = pClass
		self.HP = maxHealth
		self.MHP = maxHealth

		self.BattleEnergy = 0
		self.Kills = 0
		self.BleedDuration = 0
		self.Armor = 0