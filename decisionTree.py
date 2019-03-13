


from csv import reader


def readCSVfile(fileName):
	openFile = open(fileName)
	readFileBylines = reader(openFile)
	dataset = list(readFileBylines)
	# print(dataset)
	return dataset


def stringToFloat(dataset, column):
	for row in dataset:
		bb = row[column].strip()
		row[column] = float(bb)
		# print(row[column])


# Split a dataset based on an attribute and an attribute value
def split_Dataset(index, value, dataset):

	left, right = list(), list()
	for row in dataset:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	return left, right



# Calculate the Gini index for a split dataset
def find_gini_index(groups, classes):

	lengthOfDataset = float(sum([len(group) for group in groups]))
	# print(lengthOfDataset)

	gini = 0.0
	for group in groups:
		size = float(len(group))
		# print(size)

		if size == 0:
			continue

		score = 0.0

		for class_value in classes:
			proportion = [row[-1] for row in group].count(class_value) / size
			# print(proportion)
			score += proportion * proportion
			# print(score)

		gini += (1.0 - score) * (size / lengthOfDataset)
	return gini




def get_split(dataset):
	class_values = list(set(row[-1] for row in dataset))
	# print(class_values)

	rootNodeindex, rootNodevalue, rootNodescore, rootNodegroups = 999, 999, 999, None

	for index in range(len(dataset[0])-1):
		for row in dataset:
			groups = split_Dataset(index, row[index], dataset)
			# print(groups)
			gini = find_gini_index(groups, class_values)
			# print(gini)
			if gini < rootNodescore:
				rootNodeindex, rootNodevalue, rootNodescore, rootNodegroups = index, row[index], gini, groups
	return {'index': rootNodeindex, 'value': rootNodevalue, 'groups': rootNodegroups}




def toTerminal(group):
	outcomes = [row[-1] for row in group]
	cc = max(set(outcomes), key=outcomes.count)
	# print(cc)
	return cc




def split(node, maxDepth, minSize, depth):
	left, right = node['groups']
	del(node['groups'])

	if not left or not right:
		node['left'] = node['right'] = toTerminal(left + right)
		return

	if depth >= maxDepth:
		node['left'], node['right'] = toTerminal(left), toTerminal(right)
		return

	if len(left) <= minSize:
		node['left'] = toTerminal(left)

	else:
		node['left'] = get_split(left)
		split(node['left'], maxDepth, minSize, depth+1)

	if len(right) <= minSize:
		node['right'] = toTerminal(right)
	else:
		node['right'] = get_split(right)
		split(node['right'], maxDepth, minSize, depth+1)


def tree_Builder(train, maxDepth, minSize):
	root_Node = get_split(train)
	split(root_Node, maxDepth, minSize, 2)
	return root_Node



def print_tree(node):

		print('[X%d < %.4f]' % ((node['index']), node['value']))
		print('[%s]' % ((node)))


file_name = 'bank.csv'
data_set = readCSVfile(file_name)

aa = len(data_set[0])
# print(aa)
for i in range(aa):
	stringToFloat(data_set, i)

maxDepth = int(input('enter depth of the tree : '))
maxSize = int(input('enter size of the tree :  '))

tree = tree_Builder(data_set, maxDepth, maxSize)

print_tree(tree)
