from Loot.Items import bashingMace, smallHealingPotion, mediumHealingPotion, largeHealingPotion, map, claymoore, falchion

Pools = {

	1 : {

		'Rolls' : (3, 10),
		'Bonus Rolls' : (0, 1),
		'Entries' : {

			'Health Vial' : [smallHealingPotion, 4, (1, 2)],
			'Health Potion' : [mediumHealingPotion, 3, (1, 1)],
			'Health Elixer' : [largeHealingPotion, 2, (1, 1)],
			'Bashing Mace' : [bashingMace, 2, (1, 1)],
			'Falchion' : [falchion, 3, (1, 1)],
			'Claymoore' : [claymoore, 0.2, (1, 1)],
			"Explorer's Map" : [map, 1, (1, 1)],
			
		},
		
	},
	
}