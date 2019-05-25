from csv import reader
import math
import random


def count_class_wise_dist(Y, classes):
    prob = [0] * len(classes)
    if len(Y) == 0:
        return prob

    for i in range(classes):
        class_val = classes[i]
        prob[i] = Y.count(class_val) / len(Y)

    return prob


def claculate_entropy(prob):
    num = len(prob)
    entropy = 0.0

    for i in range(len(prob)):
        if prob[i] > 0:
            entropy = entropy - (prob[i] * math.log2(prob[i]) / math.log2(num))
    return entropy


def find_Gini(Y_tr, Y_left, Y_right):
    classes = set(Y_tr)

    prob_tr = count_class_wise_dist(Y_tr, classes)
    prob_left = count_class_wise_dist(Y_left, classes)
    prob_right = count_class_wise_dist(Y_right, classes)

    parent_ent = claculate_entropy(prob_tr)
    left_ent = claculate_entropy(prob_left)
    right_ent = claculate_entropy(prob_right)

    gini = parent_ent - left_ent*len(Y_left)/len(Y_tr) - right_ent*len(Y_right)/len(Y_tr)

    return gini


def getting_Split_Dataset(X_tr, Y_tr):
    unique_class = len(set(Y_tr))
    if unique_class == 1:
        return {'decision': True, 'result': Y_tr[0], 'index': '', 'value': ''}

    max_gini = 1000
    n_index = -1
    n_value = -1

    for index in range(len(X_tr[0])):
        for row in X_tr:
            _, _, Y_left, Y_right = split_dataset(index, row[index], X_tr, Y_tr)
            if len(Y_right) == 0:
                continue

            gini = find_Gini(Y_tr, Y_left, Y_right)
            if gini < max_gini:
                n_index, n_value, n_score, n_groups = index, row[index], gini
    return {'decision': False, 'result': '', 'index': n_index, 'value': n_value}


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


def build_decision_TREE(X_tr, Y_tr, max_depth, min_size):
    root = getting_Split_Dataset(X_tr, Y_tr)
    #print(root)
    #build_decision_TREE(X_tr, Y_tr, max_depth, min_size)
    return root


def decision_tree(X_train, Y_train, min_size, max_depth):
    tree = build_decision_TREE(X_train, Y_train, max_depth, min_size)


def load_CSV_file(file_name):
    read_file = open(file_name)
    read_lines = reader(read_file)
    data_set = list(read_lines)
    return data_set


def str2float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())


def split_dataset(index, value, X, Y):
    left = []
    right = []
    Y_left, Y_right = [], []

    for i in len(X):
        row = X[i]
        if row[index] <= value:
            left.append(row)
            Y_left.append(Y[i])
        else:
            right.append(row)
            Y_right.append(Y[i])

    return left, right, Y_left, Y_right


def shuffle_data(dataset):
    length = len(dataset)
    random.seed(30)
    for i in range(length):
        j = random.randint(1, length-1)
        data = dataset[i]
        dataset[i] = dataset[j]
        dataset[j] = data
    return dataset


def train_test_split(data_set, index, k=10):
    data_set = shuffle_data(data_set)
    #print(str(data_set))
    train = []
    test = []

    for i in range(len(data_set)):
        if i % k == index:
            test.append(data_set[i])
        else:
            train.append(data_set[i])

    return train,test


def feature_class_split(dataset):
    length = len(dataset)
    fea_len = len(dataset[0])-1
    x = []
    y = []
    for i in range(length):
        x.append(dataset[i][:-1])
        y.append(dataset[i][fea_len])

    return x, y


if __name__ == '__main__':
    file_name = 'bank.csv'
    data_set = load_CSV_file(file_name)

    for i in range(len(data_set[0])):
        str2float(data_set, i)

    train, test = train_test_split(data_set, 6, k=10)

    max_depth = 5
    min_size = 10

    X_tr, Y_tr = feature_class_split(train)
    X_te, Y_te = feature_class_split(test)
    tree = decision_tree(X_tr, Y_tr, max_depth, min_size)

    actual = [row[-1] for row in X_tr]







'''


'''
