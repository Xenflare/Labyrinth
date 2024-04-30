from Player import Player


class Heal():
	def __init__(self, healing):
		self.Healing = healing
	def Trigger(self, target):
		if type(target) is Player:
			target.HP += self.Healing
			if target.HP > target.MHP:
				target.HP = target.MHP

class Coagulate():
	def Trigger(self, target):
		if type(target) is Player:
			target.BleedDuration = 0