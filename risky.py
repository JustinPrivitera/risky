#!/usr/bin/python3

class Game:
	def __init__(self, regions, factions):
		self.regions = regions
		self.factions = factions

class Faction:
	def __init__(self, name, base_faction = None):
		self.name = name					# name of this faction
		self.base_faction = base_faction	# the base faction in the video game for this faction

class Region:
	def __init__(self, name, owner = None, continent = None, maps = [], troops = 0, neighbors = []):
		self.name = name 			# name of the region
		self.owner = owner			# the faction that owns the region
		self.continent = continent	# the continent the region is a part of
		self.maps = maps			# the maps that this region may be best played on
		self.troops = troops		# the number of troops in the region
		self.neighbors = neighbors	# the neighboring regions

def setup(stuff):
	regions = []
	regions.append(Region("Leon", "Spain", None, [], 3, ["Lisbon", "Cordoba", "Toledo"]))
	regions.append(Region("Toledo", "Spain", None, [], 3, ["Leon", "Cordoba", "Pamplona", "Zaragoza", "Valencia"]))
	regions.append(Region("Lisbon", "Portugal", None, [], 3, ["Leon", "Cordoba"]))
	regions.append(Region("Pamplona", "Portugal", None, [], 3, ["Toledo", "Zaragoza"]))
	regions.append(Region("Cordoba", "Moors", None, [], 3, ["Lisbon", "Toledo", "Granada", "Leon", "Valencia"]))
	regions.append(Region("Granada", "Moors", None, [], 3, ["Cordoba", "Valencia"]))
	regions.append(Region("Zaragoza", None, None, [], 0, ["Valencia", "Toledo", "Pamplona"]))
	regions.append(Region("Valencia", None, None, [], 0, ["Granada", "Cordoba", "Toledo", "Zaragoza"]))

	factions = []
	factions.append(Faction("Spain"))
	factions.append(Faction("Portugal"))
	factions.append(Faction("Moors"))

	return Game(regions, factions)

def tally_reinforcements(faction_name, regions):
	count = 0
	for reg in regions:
		if reg.owner == faction_name:
			count += 1
	reinforcements = count // 3
	if reinforcements < 3:
		reinforcements = 3
	# TODO add continent reinforcement bonuses
	return reinforcements

def lookup_region_by_name(name, regions):
	for reg in regions:
		if name == reg.name:
			return reg
	print("ERROR region not found")
	return None

def get_num_neighboring_enemies(faction_name, reg, regions):
	num_enemies = 0
	for border in reg.neighbors:
		border_reg = lookup_region_by_name(border, regions)
		if border_reg.owner != faction_name and border_reg.owner != None:
			num_enemies += border_reg.troops
	return num_enemies

def get_least_protected_region(faction_name, regions):
	least_protected_index = -1
	biggest_diff = 0
	for i in range(0, len(regions)):
		if regions[i].owner == faction_name:
			# ratio of neighboring enemies to friendly troops in this territory
			diff = get_num_neighboring_enemies(faction_name, regions[i], regions) / regions[i].troops
			if diff > biggest_diff:
				biggest_diff = diff
				least_protected_index = i
	return [least_protected_index, biggest_diff]

# oops this turned out to be the same function...
def get_region_bordering_weakest_enemy_region(faction_name, regions):
	ind = -1
	smallest = 1000000000
	for i in range(0, len(regions)):
		if regions[i].owner == faction_name:
			diff = get_num_neighboring_enemies(faction_name, regions[i], regions)
			if diff < smallest:
				smallest = diff
				ind = i
	return [ind, smallest]

def reinforce(faction_name, game):
	reinforcements = tally_reinforcements(faction_name, game.regions)
	
	# defensive placement
	while reinforcements > 0:
		info = get_least_protected_region(faction_name, game.regions)
		if info[1] >= 2: # neighboring regions have twice as many troops total as this region
			game.regions[info[0]].troops += 1
			reinforcements -= 1
		else:
			break

	# offensive placement
	while reinforcements > 0:
		info = get_region_bordering_weakest_enemy_region(faction_name, game.regions)
		game.regions[info[0]].troops += 1
		reinforcements -= 1

def attack_eligibility(faction_name, reg, regions):
	# does this region have more than 3 troops
	if reg.troops <= 3:
		return False

	# does this region border an enemy region
	border = False
	for neighbor_name in reg.neighbors:
		if lookup_region_by_name(neighbor_name, regions).owner != faction_name:
			border = True
	if not border:
		return False

	# does the enemy region have less troops? - then attack
	# does the enemy region have more than 1.5x as many troops? - then attack
	for neighbor_name in reg.neighbors:
		enemy_reg = lookup_region_by_name(neighbor_name, regions)
		if enemy_reg.owner != faction_name:
			if enemy_reg.troops < reg.troops || enemy_reg.troops > 1.5 * reg.troops:
				return True

def dice_roll(attack_faction, attack_region, defend_region, game):
	print(attack_faction + " is attacking " + defend_region.name + " with " + str(attack_region.troops) + " troops from " + attack_region.name + ".")
	print(defend_region.name + " is owned by " + defend_region.owner + " and has " + str(defend_region.troops) + " defending it.")
	# ok left off here



def attack(faction_name, game):
	# iterate through regions and decide for each one if it is eligible to attack
	attack_list = []
	for reg in game.regions:
		if reg.owner == faction_name:
			if attack_eligibility(faction_name, reg, game.regions):
				attack_list.append(reg)

	# ok i left off here


	# choose weak region to attack (or not to attack at all?)
	# attack the region
	# choose how many troops to move
	# decide if we attack again or stop
	pass

def take_turn(faction_name, game):
	reinforce(faction_name, game)
	# attack
	# move armies

	# check if game is won and return that value


def main():
	game = setup(0)
	while True:
		for fact in game.factions:
			if take_turn(fact.name, game): # if the game is won
				break




