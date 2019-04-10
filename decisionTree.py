from random import randrange
from csv import reader


# Load a CSV file
def load_CSV_FILE(file_NAME):
    read_FILE = open(file_NAME)
    read_LINES = reader( read_FILE)
    Data_Set = list(read_LINES)

    return Data_Set

# Convert string column to float
def string_TO_float(data_SET,column):
    for row in data_SET:
        row[column] = float(row[column].strip())

# Split a dataset into k folds
def split_dataset_cross_validation(data_SET,n_Folds):
    data_SET_split = list()
    data_SET_copy = list(data_SET)
    length = len(data_SET)
    folds_Size = int (length / n_Folds)

    for jj in range(n_Folds):
        folds = list()
        while len(folds) < folds_Size:
            index_of_dataset = randrange(len(data_SET_copy))
            folds.append(data_SET_copy.pop(index_of_dataset))
        data_SET_split.append(folds)

    return data_SET_split


# Calculate accuracy percentage
def accuracy_metric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual [ i ] == predicted [ i ]:
            correct += 1
    return correct / float(len(actual)) * 100.0



# Evaluate an algorithm using a cross validation split
def implement_decision_tree(data_SET,make_algorithm,n_Folds,*args):
    fold_dataset = split_dataset_cross_validation(data_SET,n_Folds)
    scores_of_every_parts = list()
    for fold in fold_dataset:
        train_data_SET = list(fold_dataset)
        train_data_SET.remove(fold)
        train_data_SET = sum(train_data_SET,[])
        test_data_SET = list()
        for row in fold:
            row_copy = list(row)
            test_data_SET.append(row_copy)
            row_copy[-1] = None
        predicted_Scores = make_algorithm(train_data_SET,test_data_SET,*args)
        actual = [ row [ -1 ] for row in fold ]
        accuracy = accuracy_metric(actual, predicted_Scores)
        scores_of_every_parts.append(accuracy)
    return scores_of_every_parts

# Split a train dataset based on an attribute and an attribute value
def split_train_dataset(index, value, dataset):
    left_GROUPS,right_GROUPS = list(), list()
    for row in dataset:
        if row[index] < value:
            left_GROUPS.append(row)
        else:
            right_GROUPS.append(row)
    return left_GROUPS, right_GROUPS


# Calculate the Gini index for a split dataset
def find_gini_index(groups, classes):
    length_of_splitting_groups = float(sum([len(group) for group in groups]))
    weighted_gini = 0.0

    for group in groups:
        group_size = float(len(group))
        if group_size==0.0:
            continue
        score = 0.0
        for class_values_of_dataset in classes:
            probability = [ row [ -1 ] for row in group ].count(class_values_of_dataset) / group_size
            score += probability
        weighted_gini += (1.0 - score) * (group_size / length_of_splitting_groups)
    return weighted_gini

# Select the best split point for a train dataset for finding a root node
def get_split_dataset(dataset):
    class_values_of_dataset = list(set(row[-1] for row in dataset))
    n_index, n_value, n_score, n_groups = 1000, 1000, 1000, None
    for index in range(len(dataset[0])-1):
        for row in dataset:
            groups_of_dataset = split_train_dataset(index, row[index], dataset)
            gini_Score = find_gini_index(groups_of_dataset, class_values_of_dataset)
            if gini_Score < n_score:
                n_index, n_value, n_score, n_groups = index, row [ index ], gini_Score, groups_of_dataset

    return {'index': n_index, 'value': n_value, 'groups': n_groups}


# Create a terminal node value
def to_leaf_node(group):
    outcomes = [ row [ -1 ] for row in group ]
    return max(set(outcomes), key=outcomes.count)



# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth):
    left_tree, right_tree = node['groups']
    del(node['groups'])

    # check for max depth
    if depth >= max_depth:
        node['left'], node['right'] = to_leaf_node(left_tree), to_leaf_node(right_tree)
        return

    # process left child
    if len(left_tree) <= min_size:
       node [ 'left' ] = to_leaf_node(left_tree)
    else:
        node [ 'left' ] = get_split_dataset(left_tree)
        split(node [ 'left' ], max_depth, min_size, depth + 1)

    # process right child
    if len(right_tree) <= min_size:
         node [ 'right' ] = to_leaf_node(right_tree)
    else:
         node [ 'right' ] = get_split_dataset(right_tree)
         split(node [ 'right' ], max_depth, min_size, depth + 1)

    # check for a no split
    if not left_tree or not right_tree:
        node [ 'left' ] = node [ 'right' ] = to_leaf_node(left_tree + right_tree)
        return



# Build a decision tree
def build_decision_TREE(train_set,max_depth,min_size):
    root_NODE = get_split_dataset(train_set)
    split(root_NODE,max_depth,min_size,1)
    return root_NODE

def predict_SCORES(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict_SCORES(node['left'], row)
        else:
            return node ['left']
    else:
        if isinstance(node['right'], dict):
            return predict_SCORES(node['right'], row)
        else:
            return node['right']


def decision_TREE(train_set,test_set,max_depth,min_size):
    make_tree = build_decision_TREE(train_set,max_depth,min_size)
    predictions = list()
    for row in test_set:
        prediction = predict_SCORES(make_tree, row)
        predictions.append(prediction)
    return (predictions)


#load and prepare data
file_NAME = 'demo.csv'
data_SET = load_CSV_FILE(file_NAME)

# convert string attributes to integers
for j in range(len(data_SET[0])):
    string_TO_float(data_SET,j)

#implement algorithm
n_Folds = int(input('Divide dataset: '))
maximum_Depth = int(input('Enter depth of the tree: '))
minimum_Size = int(input('Enter size of the tree: '))

scores_of_every_folds = implement_decision_tree(data_SET,decision_TREE,n_Folds,
                                                maximum_Depth,minimum_Size)
print('Scores: %s' % scores_of_every_folds)
print('Mean Accuracy: %.3f%%' % (sum(scores_of_every_folds) / float(len(scores_of_every_folds))))
