def splitDataset(index, value, dataset):
	leftSide, rightSide = list(), list()
	for row in dataset:
		if row[index] < value:
			leftSide.append(row)
		else:
			rightSide.append(row)
	return leftSide, rightSide

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


def findGiniIndex(groups, classes):

	lengthOfDataset = int(sum([len(group) for group in groups]))
	# print(lengthOfDataset)

	weighted_gini = 0.0
	for group in groups:
		sizeOfGroup = int(len(group))
		# print(size)

		if sizeOfGroup == 0:
			continue

		score = 0.0

		for class_value in classes:
			aa = [row[-1] for row in group]

			proportion = (aa. count(class_value)) / sizeOfGroup
			# print(proportion)
			score += proportion * proportion
			# print(score)

		gini = 1.0 - score
		weighted_gini += gini * (sizeOfGroup / lengthOfDataset)

	return weighted_gini

def get_Node(dataset):
	classValues = list(set(row[-1] for row in dataset))
	# print(classValues)

	indexOfNode, valueOfNode, scoreOfNode, groupsOfNode = 1000, 1000, 1000, None

	for index in range(len(dataset[0])-1):
		for row in dataset:
			groups = splitDataset(index, row[index], dataset)
			# print(groups)
			gini_found = findGiniIndex(groups, classValues)
			# print(gini)
			if gini_found < scoreOfNode:
				indexOfNode, valueOfNode, scoreOfNode, groups_OfNode = index, row[index], gini_found, groups
	return {'index of node': indexOfNode, 'value of that node ': valueOfNode, 'groups of node': groups_OfNode}

def leaf_Node(group):

	outcomes = [row[-1] for row in group]
	cc = max(set(outcomes), key=outcomes.count)
	# print(cc)
	return cc

def splitTree(node, max_Depth, min_Size, current_depth):
	leftGroup, rightGroup = node['groups of node']
	del(node['groups of node'])

	if current_depth >= max_Depth:
		node['left'], node['right'] = leaf_Node(leftGroup), leaf_Node(rightGroup)
		return

	if len(leftGroup) <= min_Size:
		node['left'] = leaf_Node(leftGroup)
	else:
		node['left'] = get_Node(leftGroup)
		splitTree(node['left'], max_Depth, min_Size, current_depth+1)


	if len(rightGroup) <= min_Size:
		node['right'] = leaf_Node(rightGroup)
	else:
		node['right'] = get_Node(rightGroup)
		splitTree(node['right'], max_Depth, min_Size, current_depth+1)


	if not leftGroup or not rightGroup:
		node['left'] = node['right'] = leaf_Node(leftGroup + rightGroup)
		return


def tree_Builder(train_Dataset, max_Depth, min_Size):
	root_Node = get_Node(train_Dataset)
	splitTree(root_Node, max_Depth, min_Size, 1)
	return root_Node



def predict(node, row):
	# print(row[node['index']])
	# print(node['value'])
	# print(node['left'])
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']


file_name = 'demo.csv'
data_set = readCSVfile(file_name)

aa = len(data_set[0])
for i in range(aa):
	stringToFloat(data_set, i)

max_Depth = int(input('enter depth of the tree : '))
min_Size = int(input('enter size of the tree :  '))

make_tree = tree_Builder(data_set, max_Depth, min_Size)

stump = {'index': 0, 'right': 1, 'value': 5.12458963, 'left': 0}
for row in data_set:
	predicted_value = predict(stump, row)
	print('Expected Class = %d, Got Class = %d' % (row[-1], predicted_value))
