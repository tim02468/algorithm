class young_tableaus():
	def __init__(self, table):
		self.table = table
		self.row = len(table)
		self.col = len(table[0])

	def insert(self, *args):
		for arg in args:
			row = self.row-1
			col = self.col-1
			self.table[row][col] = arg
			while True:
				if row == 0 and col > 0:
					if arg < self.table[row][col-1]:
						self.table[row][col] = self.table[row][col-1]
						self.table[row][col-1] = arg
						col -= 1
					else:
						break
				elif col == 0 and row > 0:
					if arg < self.table[row-1][col]:
						self.table[row][col] = self.table[row-1][col]
						self.table[row-1][col] = arg
						row -= 1
					else:
						break
				elif (row>0 and col>0):
					if (arg < self.table[row][col-1]) or (arg < self.table[row-1][col]):
						if self.table[row][col-1] < self.table[row-1][col]:
							self.table[row][col] = self.table[row-1][col]
							self.table[row-1][col] = arg
							row -= 1
						else:
							self.table[row][col] = self.table[row][col-1]
							self.table[row][col-1] = arg
							col -= 1
					else:
						break
				else:
					break			

		return self.table

	def extract_min(self):
		row = 0
		col = 0
		self.table[row][col] = float('inf')
		while True:
			if row == self.row - 1 and col < self.col:
				if self.table[row][col] > self.table[row][col+1]:
					self.table[row][col] = self.table[row][col+1]
					self.table[row][col+1] = float('inf')
					col += 1 
				else:
					break
			elif col == self.col - 1 and row < self.row: 
				if self.table[row][col] > self.table[row+1][col]:
					self.table[row][col] = self.table[row+1][col]
					self.table[row+1][col] = float('inf')
					row += 1 
				else:
					break
			elif (row < self.row and col < self.col):
				if self.table[row][col] > self.table[row][col+1] or self.table[row][col] > self.table[row+1][col]:
					if self.table[row][col+1] < self.table[row+1][col]:
						self.table[row][col] = self.table[row][col+1]
						self.table[row][col+1] = float('inf')
						col += 1 
					else:
						self.table[row][col] = self.table[row+1][col]
						self.table[row+1][col] = float('inf')
						row += 1
				else:
					break
			else:
				break 

		return self.table




# input data
with open("algorithms_hw/hw1/input.txt") as f:
	x = f.read().splitlines()

if x[len(x)-1] != '':
	x.append('')	


line_break = [index for index, item in enumerate(x) if x[index] == '']

table_count = int(x[0])
f = open('output.txt', 'w')

start = 0
for breaks in line_break:
	sub_list = x[start+1:breaks]
	start = breaks
	action = int(sub_list[0])
	# insert values
	if action == 1:
		f.write('Insert')
		insert_values = sub_list[1]
		matrix = []
		for row in sub_list[2:]:
			row = [float('inf') if r == 'x' else int(r) for r in row.split(' ')]
			matrix.append(row)
		young = young_tableaus(matrix)
		for item in insert_values.split(' '):
			young.insert(int(item))
			f.write(' {}'.format(item))
		f.write('\n')
		
	# extract min
	if action == 2:
		f.write('Extract-min ')
		matrix = []
		for row in sub_list[1:]:
			row = [float('inf') if r == 'x' else int(r) for r in row.split(' ')]
			matrix.append(row)
		young = young_tableaus(matrix)
		f.write(str(young.table[0][0]))
		young.extract_min()
		f.write('\n')
	# output

	for i in xrange(0,len(young.table)):
		for item in young.table[i]:
			if item == float('inf'):
				item = 'x'
			f.write('{} '.format(item))	
		f.write('\n')
	f.write('\n')
	table_count -= 1
	if table_count == 0:
		break

f.close()

