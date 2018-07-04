import xml.etree.ElementTree as ET

class World:
	def __init__(self,path='data/'):
		self.data = {'items':ET.parse(path + 'items.xml').getroot(),'rooms':ET.parse(path + 'rooms.xml').getroot(),'doors':ET.parse(path + 'doors.xml').getroot(),'init':ET.parse(path + 'init.xml').getroot()}
		
		self.items = {}
		self.rooms = {}
		
		# CREATE items
		for item in self.data['items']:
			self.items[item.get('id')] = Item(item)
		# CREATE rooms
		for room in self.data['rooms']:
			self.rooms[room.get('id')] = Room(room.find('name').text,room.find('desc').text)
		
		# MOVE items into containers
		for container in self.data['init'].find('containers'):
			for item in container.findall('item'):
				self.items[item.text].actMove(self.items[container.get('id')])
		# MOVE items into rooms
		for room in self.data['init'].find('rooms'):
			for item in room.findall('item'):
				self.items[item.text].actMove(self.rooms[room.get('id')])



				
				
				
				
				
class Item:
	def __init__(self,dataInit):
		self.id = dataInit.get('id')
		self.name = dataInit.find('name').text
		self.desc = dataInit.find('desc').text
		
		self.movable = True
		self.container = False
		
		self.owner = abyss
		self.inventory = []
		abyss.inventory.append(self)
		
		
		if (dataInit.find('flags').find('movable') is not None and dataInit.find('flags').find('movable').text == 'False'):
			self.movable = False
		
		if (dataInit.find('flags').find('container') is not None and dataInit.find('flags').find('container').text == 'True'):
			self.container = True

	def actMove(self,target,silent=False):
		if (self.movable or self.owner == abyss):
			if (target.container or target == abyss):
				self.owner.inventory.remove(self)
				self.owner = target
				
				self.owner.inventory.append(self)
				self.owner.inventory.sort(key=lambda item:item.name)
				
				return [True,"The {} has been moved inside the {}.".format(self.name,self.owner.name)]
			else:
				return [False,"The {} won't fit inside of the {}.".format(self.name,target.name)]
		else:
			return [False,"The {} cannot be moved.".format(self.name)]
		
	def listInventory(self):
		if (self.container):
			if (len(self.inventory)):
				return [True,", ".join(map(lambda item: item.name,self.inventory))]
			else:
				return [True,"The {} is empty.".format(self.name)]
		else:
			return [False,"The {} is not a container.".format(self.name)]
				
				
				
				
				
				
				
				
				
				
				
				
				




class Object:
	def __init__(self,name,desc):
		self.name = name
		self.desc = desc
		
class MovableObject(Object):
	def __init__(self,name,desc,movable=False):		
		Object.__init__(self,name,desc)
		self.movable = movable
		self.inventory = []
			
	def itemAdd(self,item):
		self.inventory.append(item)
		self.inventory.sort(key=lambda item:item.name)
	
	def itemRemove(self,item):
		try:
			self.inventory.remove(item)
			return True
		except:
			return False
	
	def listInventory(self):
		return ", ".join(map(lambda item: item.name,self.inventory))
		
				

class Player(MovableObject):
	def __init__(self):
		
		self.name = 'Cheese' #input("Enter your name:\n")
		
		container = True
		
		
		self.curRoom = world.rooms['0']
		self.inventory = []
	
	def actLook(self):
		print("\n= {}\n  Looking around, you see {}".format(self.curRoom.name,self.curRoom.desc))
		if (len(self.curRoom.inventory)):
			print("  You see: {}".format(self.curRoom.listInventory()))
		
	def actLookin(self,objectName):
		container = list(filter(lambda container: container.name == objectName,self.curRoom.inventory + self.inventory))

		if (not len(container)):
			print("- You can't see {}.".format(objectName))
		else:
			if (len(container[0].inventory)):
				print("    The {} contains: {}.".format(container[0].name,container[0].listInventory()))
			else:
				print("    The {} has nothing of value.".format(container[0].name))
	
		
		
		
	
	def invLook(self):
		if (len(self.inventory)):
			print("  You are carrying: {}.".format(self.listInventory()))
		else:
			print("  Your inventory is empty.")
			
		
		
		

		
		
		
		
		
		




			
		
		
		

		
class Room(MovableObject):
	def __init__(self,name,desc,movable=False):		
		MovableObject.__init__(self,name,desc,movable)
		
		self.container = True
		
	def listInventory(self):
		if (self.container):
			if (len(self.inventory)):
				return [True,", ".join(map(lambda item: item.name,self.inventory))]
			else:
				return [True,"The {} is empty.".format(self.name)]
		else:
			return [False,"The {} is not a container.".format(self.name)]
		
		
class Abyss(Room):
	def __init__(self):
		self.name = 'The Abyss'
		self.inventory = []
		
		
		
		
		
print("\n")
# CREATE GAME WORLD
abyss = Abyss()	
world = World()
# CREATE PLAYER CHARACTER	
player = Player()


'''
print("{} in room {}.".format(player.name,player.curRoom.name))
player.actLook()
player.actLookin('Bureau')
player.invLook()



player.itemAdd(world.containers['boxofcards'])
world.containers['aptroom2305bureau'].itemRemove(world.containers['boxofcards'])


print("\n\n\n{} in room {}.".format(player.name,player.curRoom.name))
player.actLook()
player.actLookin('Bureau')
player.invLook()

player.actLookin('Box of Cards')

for i in world.items:
	print(world.items[i].actMove(world.items['key1']))

print("\n\n")

for i in world.items:
	print(world.items[i].actMove(world.rooms['0']))

print("\n\n")

for i in world.items:
	print(world.items[i].actMove(world.items['container1']))

print("\n\n")
'''








for item in world.items:
	print("{} : {}\t\t{}".format(item,world.items[item].name,world.items[item].listInventory()))
	print('\n')

	
print("\n+++\n")
for room in world.rooms:
	print("{} : {}\t\t{}".format(room,world.rooms[room].name,world.rooms[room].listInventory()))
	print('\n')
	
	#for item in world.rooms[room].inventory:
	#	print("  {}".format(item.name))
print("\n===\n")
'''
'''

	
	
	
	
	
	
	
	
	
	
	
'''
	
	
	
for i in world.items:
	print("{} : {} - {}".format(i,world.items[i].name,world.items[i].owner))
	world.items[i].actMove(world.rooms['1'])
	print('---')
	
	
for i in world.items:
	print("{} : {} - {}".format(i,world.items[i].name,world.items[i].owner))
	world.items[i].actMove()
	print('---')
	
	
	
	
for i in world.items:
	print("{} : {} - {}".format(i,world.items[i].name,world.items[i].owner))
	print('===\n')

print("\n\n")

'''