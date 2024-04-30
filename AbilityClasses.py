import random
from Enemies import EnemyInstance
from Player import Player

class SwingAttack():
	def __init__(self, name, baseDamage, bleedChance, bleedDuration, energyUse):
		self.Name = name
		self.DMG = baseDamage
		self.BleedChance = bleedChance
		self.BleedDuration = bleedDuration
		self.RequiredEnergy = energyUse
	def Trigger(self, target):
		damageToDeal = random.randint(self.DMG[0], self.DMG[1])
		if type(target) is EnemyInstance:
			target.Health -= damageToDeal
			if random.uniform(1, 100) <= self.BleedChance:
				target.BleedDuration += self.BleedDuration
		elif type(target) is Player:
			target.HP -= damageToDeal
			if random.uniform(1, 100) <= self.BleedChance:
				target.BleedDuration += self.BleedDuration
		return damageToDeal