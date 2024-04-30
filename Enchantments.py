
class Enchantment():
	def __init__(self, name, maxLevel, damageMult):
		self.Name = name
		self.MaxLevel = maxLevel

		self.DamageModifier = damageMult

class AppliedEnchantment():
	def __init__(self, enchant, level):
		self.Enchant = enchant
		self.Level = level