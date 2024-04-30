from Loot.Items import coin, bashingMace, smallHealingPotion, mediumHealingPotion, largeHealingPotion, map, claymoore, falchion

Pools = {

	1 : {

		'Rolls' : (2, 3),
		'Bonus Rolls' : (0, 1),
		'Entries' : {

			'Coin' : [coin, 20, (1, 3)],
			'Health Vial' : [smallHealingPotion, 4, (1, 2)],
			'Health Potion' : [mediumHealingPotion, 2, (1, 1)],
			'Health Elixer' : [largeHealingPotion, 0.5, (1, 1)],
			'Bashing Mace' : [bashingMace, 2, (1, 1)],
			'Falchion' : [falchion, 3, (1, 1)],
			'Claymoore' : [claymoore, 0.2, (1, 1)],
			"Explorer's Map" : [map, 0.1, (1, 1)],
			
		},
		
	},
	
}