class TreeNode():
	"""docstring for TreeNode"""
	def __init__(self, key, parent=None, right=None, left=None, color=0):
		self.parent = parent
		self.right = right
		self.left = left
		self.key = key
		self.color = color # red = 0, black = 1


class RBTree():
	"""docstring for RBTree"""
	def __init__(self):
		self.nil = TreeNode(key="NIL", color = 1)
		self.root = self.nil
		self.queue = []

	# insertion
	def insert(self, key):
		# new node
		insertNode = TreeNode(key=key, right=self.nil, left=self.nil)
		x = self.root
		y = self.nil

		while x.key != "NIL":
			y = x
			if key < x.key:
				x = x.left
			else:
				x = x.right

		insertNode.parent = y

		if y.key == "NIL":
			self.root = insertNode
		elif key < y.key:
			y.left = insertNode
		else:
			y.right = insertNode

		self.insertFixUp(insertNode)

	def transverse(self, root):
		if root == self.root:
			self.queue = []
		if root.key != "NIL":
			self.transverse(root.left)
			# print("Key: {} parent: {} color: {}".format(root.key, root.parent.key, root.color))
			self.queue.append([root.key, root.parent.key, root.color])
			self.transverse(root.right)

	def leftRotation(self, currentNode):
		y = currentNode.right
		currentNode.right = y.left

		if y.left.key != "NIL":
			y.left.parent = currentNode

		y.parent = currentNode.parent

		if currentNode.parent.key == "NIL":
			self.root = y
		elif currentNode == currentNode.parent.right:
			currentNode.parent.right = y
		else:
			currentNode.parent.left = y
		
		y.left = currentNode
		currentNode.parent = y

	def rightRotation(self, currentNode):
		x = currentNode.left
		currentNode.left = x.right

		if x.right.key != "NIL":
			x.right.parent = currentNode

		x.parent = currentNode.parent

		if currentNode.parent.key == "NIL":
			self.root = x
		elif currentNode == currentNode.parent.left:
			currentNode.parent.left = x
		else:
			currentNode.parent.right = x
		
		x.right = currentNode
		currentNode.parent = x

	def insertFixUp(self, currentNode):
		# check if fix-up needed
		while currentNode.parent.color == 0:
			# check parent side
			if currentNode.parent == currentNode.parent.parent.left:
				# get uncle
				uncle = currentNode.parent.parent.right
				''' case 1: uncle color is red, no matter currentNode located at which side of parent'''
				if uncle.color == 0:
					currentNode.parent.color = 1
					uncle.color = 1
					currentNode.parent.parent.color = 0
					currentNode = currentNode.parent.parent
				else:
					'''case 2 and case 3'''
					if currentNode == currentNode.parent.right:
						currentNode = currentNode.parent
						self.leftRotation(currentNode) 
					
					currentNode.parent.color = 1
					currentNode.parent.parent.color = 0
					self.rightRotation(currentNode.parent.parent)
			else:
				uncle = currentNode.parent.parent.left
				if uncle.color == 0:
					currentNode.parent.color = 1
					uncle.color = 1
					currentNode.parent.parent.color = 0
					currentNode = currentNode.parent.parent
				else:
					if currentNode == currentNode.parent.left:
						currentNode = currentNode.parent
						self.rightRotation(currentNode) ## strange

					currentNode.parent.color = 1
					currentNode.parent.parent.color = 0
					self.leftRotation(currentNode.parent.parent)


		self.root.color = 1

	def search(self, currentNode, key):
		while currentNode.key != "NIL":
			if key < currentNode.key:
				currentNode = currentNode.left
			elif key > currentNode.key:
				currentNode = currentNode.right
			else:
				return currentNode
		return False

	def findMin(self, currentNode):
		while currentNode.key != "NIL":
			if currentNode.left.key == "NIL":
				break
			currentNode = currentNode.left
		return currentNode

	def findMax(self, currentNode):
		while currentNode.right.key != "NIL":
			currentNode = currentNode.right
		return currentNode.parent

	def findSuccessor(self, currentNode):
		if currentNode.right.key != "NIL":
			return self.findMin(currentNode.right)
		else:
			return self.findMax(currentNode.left)

	def delete(self, key):
		# check exists or not
		deleteNode = self.search(self.root, key)

		if not deleteNode:
			print("{} not exists.".format(key))
			return

		deleteColor = deleteNode.color

		if deleteNode.right.key == "NIL" or deleteNode.left.key == "NIL":
			if deleteNode.left.key == "NIL":
				deleteNodeChild = deleteNode.right
			else:
				deleteNodeChild = deleteNode.left

			deleteNodeChild.parent = deleteNode.parent

			if deleteNode.parent.key == "NIL":
				self.root = deleteNodeChild
			elif deleteNode == deleteNode.parent.left:
				deleteNode.parent.left = deleteNodeChild
			else:
				deleteNode.parent.right = deleteNodeChild

		else:
			successor = self.findSuccessor(deleteNode)
			deleteColor = successor.color
			# print('delete success', key, " ", successor.key, " ", successor.left.)
			if successor.left.key != "NIL":
				# print('delete success', key, " ", successor.key)
				successorChild = successor.left
				successorChild.parent = successor.parent
			else:	
				successorChild = successor.right
				successorChild.parent = successor.parent
			

			if successor == successor.parent.right:
				successor.parent.right = successorChild
			else:
				successor.parent.left = successorChild
			deleteNode.key = successor.key
			# deleteNode.color = successor.color
			deleteNodeChild = successorChild


		if deleteColor == 1:
			self.deleteFixUp(deleteNodeChild)

	def deleteFixUp(self, currentNode):
		while currentNode != self.root and currentNode.color == 1:
			if currentNode == currentNode.parent.left:
				sibling = currentNode.parent.right
				if sibling.color == 0: # case 1
					sibling.color = 1
					currentNode.parent.color = 0
					self.leftRotation(currentNode.parent)
					sibling = currentNode.parent.right
				else:
					if sibling.left.color == 1 and sibling.right.color == 1: # case 2
						sibling.color = 0
						currentNode = currentNode.parent
					else:
						if sibling.right.color == 1: # case 3
							sibling.left.color = 1
							sibling.color = 0
							self.rightRotation(sibling)
							sibling = currentNode.parent.right

						sibling.color = currentNode.parent.color # case 4
						currentNode.parent.color = 1
						sibling.right.color = 1
						self.leftRotation(currentNode.parent)
						currentNode = self.root
			elif currentNode == currentNode.parent.right:
				sibling = currentNode.parent.left
				if sibling.color == 0: # case 1
					sibling.color = 1
					currentNode.parent.color = 0
					self.rightRotation(currentNode.parent)
					sibling = currentNode.parent.left
				else:
					if sibling.left.color == 1 and sibling.right.color == 1: # case 2
						sibling.color = 0
						currentNode = currentNode.parent
					else:
						if sibling.left.color == 1: # case 3
							sibling.right.color = 1
							sibling.color = 0
							self.leftRotation(sibling)
							sibling = currentNode.parent.left

						sibling.color = currentNode.parent.color # case 4
						currentNode.parent.color = 1
						sibling.left.color = 1
						self.rightRotation(currentNode.parent)
						currentNode = self.root
		currentNode.color = 1


def tansferNodeToString(node):
	if node[1] == "NIL":
		node[1] = " "
	if node[2] == 0:
		node[2] = "red"
	else:
		node[2] = "black"
	return "key: {} parent: {} color: {}".format(node[0], node[1], node[2])


tree = RBTree()


# input data
with open("input.txt") as f:
	inputFile = f.read().splitlines()

f = open('output.txt', 'w')

action = int(inputFile[0])
inputFile = inputFile[1:]

for i in range(len(inputFile)):	
	if action == 0:
		break

	if inputFile[i] == "1":
		insertList = inputFile[i+1].split(' ')
		outString = ', '.join((insertList))
		f.write("Insert: {}".format(outString) + '\n')
		for key in insertList:
			tree.insert(int(key))
	elif inputFile[i] == "2":
		deleteList = inputFile[i+1].split(' ')
		outString = ', '.join((deleteList))
		f.write("Delete: {}".format(outString) + '\n')
		for key in deleteList:
			tree.delete(int(key))
	else:
		action -= 1
		tree.transverse(tree.root)
		for i in tree.queue:
			f.write(tansferNodeToString(i) + '\n')
		continue





# sequence = [5, 11, 9, 7, 6, 12, 5, 4, 1]
# sequence = [12, 1, 9, 2, 0, 11, 7, 19, 4, 15, 18, 5, 14, 13, 10, 16, 6, 3, 8, 17]
# for i in sequence:
# 	tmp.insert(i)


# tmp.transverse(tmp.root)

# for i in tmp.queue:
# 	print(tansferNodeToString(i))

	