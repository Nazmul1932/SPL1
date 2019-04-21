
import random
from csv import reader
from random import seed


def load_CSV_file(filename):
    file = open(filename)
    lines = reader(file)
    dataset = list(lines)
    return dataset




from random import randrange
def  split_dataset_cross_validation(dataset, n_folds):
    dataset_s = list()
    dataset_copy = list(dataset)
    #print(dataset_copy)
    fold_size = int(len(dataset) / n_folds)
    #print(fold_size)
    for i in range(n_folds):
        fold = list()
        while len(fold) < fold_size:
            index = randrange(len(dataset_copy))
            #print(index)
            fold.append(dataset_copy.pop(index))
        dataset_s.append(fold)
    #print(dataset_split)
    return dataset_s


def calculate_accuracy_(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual [ i ] == predicted [ i ]:
            correct += 1
    return correct / float(len(actual)) * 100.0


def split_dataset(index, value, dataset):
    left, right = list(), list()
    for row in dataset:
        if row [ index ] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right



def find_Gini(groups, classes):
    length_of_splitting_groups = float(sum([ len(group) for group in groups ]))

    weighted_Gini =  0.0
    for group in groups:
        group_size = float(len(group))

        if group_size == 0:
            continue
        score = 0.0

        for class_values_of_dataset in classes:
            probability = [ row [ -1 ] for row in group ].count(class_values_of_dataset) / group_size
            score += probability * probability

        weighted_Gini  += (1.0 - score) * (group_size / length_of_splitting_groups)
    return weighted_Gini


def getting_Split_Dataset(dataset):
    class_values_of_dataset = list(set(row [ -1 ] for row in dataset))
    n_index, n_value, n_score, n_groups = 1000, 1000, 1000, None
    for index in range(len(dataset [ 0 ]) - 1):
        for row in dataset:
            groups = split_dataset(index, row [ index ], dataset)
            gini = find_Gini(groups, class_values_of_dataset)
            if gini < n_score:
                n_index, n_value, n_score, n_groups = index, row [ index ], gini, groups
    return {'index': n_index, 'value': n_value, 'groups': n_groups}

def to_terminal(group):
    outcomes = [ row [ -1 ] for row in group ]
    #print(outcomes)
    #aaa = outcomes.count
    #print(aaa)
    #print(set(outcomes))
    bbb = max(set(outcomes), key= outcomes.count)
    #print(bbb)
    return bbb



def  make_TREE(node, max_depth, min_size, depth):
    left, right = node [ 'groups' ]
    del (node [ 'groups' ])

    if not left or not right:
        node [ 'left' ] = node [ 'right' ] = to_terminal(left + right)
        return

    if depth >= max_depth:
        node [ 'left' ], node [ 'right' ] = to_terminal(left), to_terminal(right)
        return

    if len(left) <= min_size:
        node [ 'left' ] = to_terminal(left)
    else:
        node [ 'left' ] = getting_Split_Dataset(left)
        make_TREE(node [ 'left' ], max_depth, min_size, depth + 1)


    if len(right) <= min_size:
        node [ 'right' ] = to_terminal(right)
    else:
        node [ 'right' ] =getting_Split_Dataset(right)
        make_TREE(node [ 'right' ], max_depth, min_size, depth + 1)


def  build_decision_TREE(train, max_depth, min_size):
    root = getting_Split_Dataset(train)
    #print(root)
    make_TREE(root, max_depth, min_size, 1)
    return root


def predict(node, row):
    if row [ node [ 'index' ] ] < node [ 'value' ]:
        if isinstance(node [ 'left' ], dict):
            return predict(node [ 'left' ], row)
        else:
            return node [ 'left' ]
    else:
        if isinstance(node [ 'right' ], dict):
            return predict(node [ 'right' ], row)
        else:
            return node [ 'right' ]


def decision_tree(train, test, max_depth, min_size):
    tree =  build_decision_TREE(train, max_depth, min_size)
    predictions = list()
    for row in test:
        prediction = predict(tree, row)
        predictions.append(prediction)
    return (predictions)


def  make_algorithm(dataset, algorithm, n_folds, *args):
    folds = split_dataset_cross_validation(dataset, n_folds)
    #print(folds)
    scores = list()
    for fold in folds:
        train_set = list(folds)
        train_set.remove(fold)
        train_set = sum(train_set, [ ])
        test_set = list()
        for row in fold:
            row_copy = list(row)
            test_set.append(row_copy)
            row_copy [ -1 ] = None
        predicted = decision_tree(train_set, test_set, *args)
        actual = [ row [ -1 ] for row in fold ]
        accuracy = calculate_accuracy_(actual, predicted)
        scores.append(accuracy)
    return scores


def shuffle_data(dataset):
    length = len(dataset)
    #print(length)
    random.seed(30)
    for i in range(length):
        j = random.randint(1, length-1)
        #print(j)
        data = dataset[i]
        dataset[i] = dataset[j]
        dataset[j] = data
    #print(dataset)
    return dataset


if __name__ == '__main__':
    file_name = 'demo.csv'
    data_set = load_CSV_file(file_name)

dataset = shuffle_data(data_set)
#print(dataset)


n_folds = 4
max_depth = 3
min_size = 10
scores_of_every_folds = make_algorithm(dataset, decision_tree, n_folds, max_depth, min_size)
print('Scores: %s' % scores_of_every_folds)
print('Mean Accuracy: %.3f%%' % (sum(scores_of_every_folds) / float(len(scores_of_every_folds))))
