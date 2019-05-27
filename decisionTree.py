from csv import reader
import math
import random


def load_CSV_file(file_name):
    read_file = open(file_name)
    read_lines = reader(read_file)
    data_set = list(read_lines)
    return data_set


def str2float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())


def count_class_wise_dist(Y, classes):
    prob = [0] * len(classes)
    if len(Y) == 0:
        return prob

    index = 0
    for class_val in classes:
        prob[index] = Y.count(class_val) / len(Y)
        index = index + 1

    return prob


def claculate_entropy(prob):
    entropy = 0.0

    for i in range(len(prob)):
        if prob[i] > 0:
            entropy = entropy - (prob[i] * math.log2(prob[i]))
    return entropy


def find_Info_Gain(Y_tr, Y_left, Y_right):
    classes = set(Y_tr)

    prob_tr = count_class_wise_dist(Y_tr, classes)
    prob_left = count_class_wise_dist(Y_left, classes)
    prob_right = count_class_wise_dist(Y_right, classes)

    parent_ent = claculate_entropy(prob_tr)
    left_ent = claculate_entropy(prob_left)
    right_ent = claculate_entropy(prob_right)

    gain = parent_ent - left_ent*len(Y_left)/len(Y_tr) - right_ent*len(Y_right)/len(Y_tr)

    return gain


def split_dataset(index, value, X, Y):
    left = []
    right = []
    Y_left, Y_right = [], []

    for i in range(len(X)):
        row = X[i]
        if row[index] <= value:
            left.append(row)
            Y_left.append(Y[i])
        else:
            right.append(row)
            Y_right.append(Y[i])

    return left, right, Y_left, Y_right





def getting_Node(X_tr, Y_tr, current_depth, max_depth):
    unique_class = len(set(Y_tr))
    if unique_class == 1:
        return {'decision': True, 'result': Y_tr[0], 'depth': current_depth, 'index': '', 'value': '', 'left': '',
                'right': ''}

    if current_depth == max_depth:
        return {'decision': True, 'result': find_decision(Y_tr), 'depth': current_depth, 'index': '', 'value': '',
                'left': '', 'right': ''}

    max_gain = -1
    n_index = -1
    n_value = -1

    for index in range(len(X_tr[0])):
        for row in X_tr:
            _, _, Y_left, Y_right = split_dataset(index, row[index], X_tr, Y_tr)
            if len(Y_right) == 0:
                continue

            gain = find_Info_Gain(Y_tr, Y_left, Y_right)
            if gain > max_gain:
                n_index, n_value, max_gain = index, row[index], gain

    X_left, X_right, Y_left, Y_right = split_dataset(n_index, n_value, X_tr, Y_tr)

    return {'decision': False, 'result': '', 'depth': current_depth, 'index': n_index, 'value': n_value,
            'left': getting_Node(X_left, Y_left, current_depth + 1, max_depth),
            'right': getting_Node(X_right, Y_right, current_depth + 1, max_depth)}


def build_decision_TREE(X_tr, Y_tr, max_depth):
    root = getting_Node(X_tr, Y_tr, 0, max_depth)
    return root


def shuffle_data(dataset):
    length = len(dataset)
    random.seed(30)
    for i in range(length):
        j = random.randint(1, length-1)
        data = dataset[i]
        dataset[i] = dataset[j]
        dataset[j] = data
    return dataset


def get_unique_classes(dataset):
    fea_len = len(dataset[0]) - 1
    labels = []

    for row in dataset:
        labels.append(row[fea_len])

    unique_classes = set(labels)

    return len(unique_classes)


def train_test_split(data_set, index, k=10):
    data_set = shuffle_data(data_set)

    train = []
    test = []

    for i in range(len(data_set)):
        if i % k == index:
            test.append(data_set[i])
        else:
            train.append(data_set[i])

    return train, test


def feature_class_split(dataset):
    length = len(dataset)
    fea_len = len(dataset[0])-1
    x = []
    y = []
    for i in range(length):
        x.append(dataset[i][:-1])
        y.append(int(dataset[i][fea_len]))

    return x, y


def predict_label(tree, sample):
    node = tree
    while node['decision'] != True:
        fea_index = node['index']
        fea_value = node['value']

        if sample[fea_index] <= fea_value:
            node = node['left']
        else:
            node = node['right']

    return node['result']


def get_confusion_matrix(tree, X_te, Y_te, classes):
    conf_mat = []
    for i in range(classes):
        conf_mat.append([0] * classes)

    for i in range(len(X_te)):
        Y_act = Y_te[i]
        Y_pred = predict_label(tree, X_te[i])
        conf_mat[Y_act][Y_pred] = conf_mat[Y_act][Y_pred] + 1

    return conf_mat


def add_conf_mat(conf_mat, conf_mat_te):
    for i in range(len(conf_mat)):
        for j in range(len(conf_mat[0])):
            conf_mat[i][j] = conf_mat[i][j] + conf_mat_te[i][j]

    return conf_mat


if __name__ == '__main__':
    file_name = 'bank.csv'
    data_set = load_CSV_file(file_name)

    for i in range(len(data_set[0])):
        str2float(data_set, i)

    classes = get_unique_classes(data_set)
    total_sample = len(data_set)
    conf_mat = []
    max_depth = 5
    k_cv = 10

    for i in range(classes):
        conf_mat.append([0] * classes)

    for i in range(k_cv):
        train, test = train_test_split(data_set, i, k=k_cv)

        X_tr, Y_tr = feature_class_split(train)
        X_te, Y_te = feature_class_split(test)

        tree = build_decision_TREE(X_tr, Y_tr, max_depth)
        conf_mat_te = get_confusion_matrix(tree, X_te, Y_te, classes)
        conf_mat = add_conf_mat(conf_mat, conf_mat_te)

    print(conf_mat)

    correct = 0
    for i in range(classes):
        correct = correct + conf_mat[i][i]

    print('Accuracy: ' + str(correct/total_sample))







'''


'''
