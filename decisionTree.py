from csv import reader
import random


def load_CSV_file(file_name):
	read_file = open(file_name)
	read_lines = reader(read_file)
	data_set = list(read_lines)
	return data_set





def split_dataset(index, value, dataset):
	left, right = list(), list()
	for row in dataset:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	#print(left)
	#print(right)
	return left, right


def find_Gini(groups, classes):
	length_of_splitting_groups = float(sum([len(group) for group in groups]))

	weighted_Gini = 0.0
	for group in groups:
		group_size = float(len(group))

		if group_size == 0:
			continue
		score = 0.0

		for class_values_of_dataset in classes:
			probability = [row[-1] for row in group].count(class_values_of_dataset) / group_size
			score += probability * probability

		weighted_Gini += (1.0 - score) * (group_size / length_of_splitting_groups)
	return weighted_Gini


def getting_Split_Dataset(dataset):
	class_values_of_dataset = list(set(row[-1] for row in dataset))
	n_index, n_value, n_score, n_groups = 1000, 1000, 1000, None
	for index in range(len(dataset[0]) - 1):
		for row in dataset:
			groups = split_dataset(index, row[index], dataset)
			#print(groups)
			gini = find_Gini(groups, class_values_of_dataset)
			#print(gini)
			if gini < n_score:
				n_index, n_value, n_score, n_groups = index, row[index], gini, groups
	return {'index': n_index, 'value': n_value, 'groups': n_groups}


def to_terminal(group):
	outcomes = [row[-1] for row in group]
	return max(set(outcomes), key=outcomes.count)


def make_TREE(node, max_depth, min_size, depth):
	left, right = node['groups']
	del (node['groups'])

	if not left or not right:
		node['left'] = node['right'] = to_terminal(left + right)
		return

	if depth >= max_depth:
		node['left'], node['right'] = to_terminal(left), to_terminal(right)
		return

	if len(left) <= min_size:
		node['left'] = to_terminal(left)
	else:
		node['left'] = getting_Split_Dataset(left)
		make_TREE(node['left'], max_depth, min_size, depth + 1)

	if len(right) <= min_size:
		node['right'] = to_terminal(right)
	else:
		node['right'] = getting_Split_Dataset(right)
		make_TREE(node['right'], max_depth, min_size, depth + 1)


def build_decision_TREE(train, max_depth, min_size):
	root = getting_Split_Dataset(train)
	#print(root)
	make_TREE(root, max_depth, min_size, 1)
	return root


def decision_tree(train, min_size, max_depth):
	tree = build_decision_TREE(train, max_depth, min_size)
	#print(tree)
	#print_tree(tree)
	return tree

def shuffle_data(dataset):
	length = len(dataset)
	random.seed(30)
	for i in range(length):
		j = random.randint(1, length-1)
		data = dataset[i]
		dataset[i] = dataset[j]
		dataset[j] = data
	return dataset


def feature_class_split(dataset):
	length = len(dataset)
	fea_len = len(dataset[0])-1
	x = []
	y = []
	for i in range(length):
		x.append(dataset[i][:-1])
		y.append(dataset[i][fea_len])
	#print(x)
	#print(y)
	return x, y


def train_test_split(data_set, index, k=10):
	data_set = shuffle_data(data_set)
	train = []
	test = []
	length = len(data_set)
	for i in range(length):
		if i % k == index:
			test.append(data_set[i])
		else:
			train.append(data_set[i])
	#print(test)
	#print(train)
	X_tr, Y_tr = feature_class_split(train)
	X_ts, Y_ts = feature_class_split(test)
	return X_tr, Y_tr, X_ts, Y_ts

if __name__ == '__main__':
	file_name = 'demo.csv'
	data_set = load_CSV_file(file_name)
	#print("Dataset Lenght: ", len(data_set))

	X_tr, Y_tr, X_te, Y_te = train_test_split(data_set, 6, k=10)
	print(X_te)
	max_depth = 3
	min_size = 5

	train_score = decision_tree(X_tr,max_depth,min_size)
	#print(train_score)
	test_score = decision_tree(X_te,max_depth,min_size)
	#print(test_score)

