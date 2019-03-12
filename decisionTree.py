
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
	# count all samples at split point
	lengthOfDataset = float(sum([len(group) for group in groups]))
	# sum weighted Gini index for each group
	gini = 0.0
	for group in groups:
		size = float(len(group))
		# avoid divide by zero
		if size == 0:
			continue
		score = 0.0
		# score the group based on the score for each class
		for class_value in classes:
			proportion = [row[-1] for row in group].count(class_value) / size
			score += proportion * proportion
		# weight the group score by its relative size
		gini += (1.0 - score) * (size / lengthOfDataset)
	return gini



# Select the best split point for a dataset
def get_split(dataset):
	class_values = list(set(row[-1] for row in dataset))
	# print(class_values) #aikhane class 0 and 1 print hbe

	rootNodeindex, rootNodevalue, rootNodescore, rootNodegroups = 999, 999, 999, None

	for index in range(len(dataset[0])-1):
		for row in dataset:
			groups = split_Dataset(index, row[index], dataset)
			# print(groups)
			gini = find_gini_index(groups, class_values)
			if gini < rootNodescore:
				rootNodeindex, rootNodevalue, rootNodescore, rootNodegroups = index, row[index], gini, groups
	return {'index': rootNodeindex, 'value': rootNodevalue, 'groups': rootNodegroups}



# Create a terminal node value
def toTerminal(group):
	outcomes = [row[-1] for row in group]
	cc = max(set(outcomes), key=outcomes.count)
	# print(cc)
	return cc



# Create child splits for a node or make terminal
def split(node, maxDepth, minSize, depth):
	left, right = node['groups']
	del(node['groups'])
	# check for a no split
	if not left or not right:
		node['left'] = node['right'] = toTerminal(left + right)
		return
	# check for max depth
	if depth >= maxDepth:
		node['left'], node['right'] = toTerminal(left), toTerminal(right)
		return


	# process left child
	if len(left) <= minSize:
		node['left'] = toTerminal(left)
	else:
		node['left'] = get_split(left)
		split(node['left'], maxDepth, minSize, depth+1)


	# process right child
	if len(right) <= minSize:
		node['right'] = toTerminal(right)
	else:
		node['right'] = get_split(right)
		split(node['right'], maxDepth, minSize, depth+1)




# Build a decision tree
def tree_Builder(train, maxDepth, minSize):
	root_Node = get_split(train)
	split(root_Node, maxDepth, minSize, 1)
	return root_Node



# Print a decision tree
def print_tree(node, depth=0):
	if isinstance(node, dict):
		print('%s[X%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
		print_tree(node['left'], depth+1)
		print_tree(node['right'], depth+1)
	else:
		print('%s[%s]' % ((depth*' ', node)))



file_name = 'bank.csv'
data_set = readCSVfile(file_name)

aa = len(data_set[0])
# print(aa)
for i in range(aa):
	stringToFloat(data_set, i)

tree = tree_Builder(data_set, 2, 2)
print_tree(tree)
