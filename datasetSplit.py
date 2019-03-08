def dataset_split(index, value, dataset):
    leftSide, rightSide = list(), list()
    for row in dataset:
        # print(row)

        if row[index] < value:
            leftSide.append(row)
            # print(leftSide)
        else:
            rightSide.append(row)
            # print(rightSide)

    return leftSide, rightSide

def gini_index(groups, classes):

    a = sum([len(group) for group in groups])
    lengthOfDataset = float(a)
    # print(n_instances)

    gini = 0.0
    for group in groups:
        size = float(len(group))
        print('size of that group %.3f' % size)

        if size == 0:
            continue
        score = 0.0

        x = [row[2] for row in group]
        print(x)

        for class_val in classes:
            y = x.count(class_val)  # ai line dia bujhasse kon group e kon class koyta ase
            print('class value is %d' % y)

            proportion = y / size
            print('proportion is %.3f' % proportion)

            score += proportion * proportion
            print('score is %.3f' % score)

        gini += (1.0 - score) * (size / lengthOfDataset)
        print('gini score is %.3f' % gini)
    return gini



def split_datset(dataset):
    class_values = list(set(row[2] for row in dataset))
    #print(class_values) #aikhane class 0 and 1 print hbe

    b_index, b_value, b_score, b_groups = 999, 999, 999, None

    x = len(dataset[0])-1
    # print(x) # aikhane dataset er length class bade 2 print hbe

    for index in range(x):
        # print(index)
        for row in dataset:
            # print(row)
            # print(row[index])
            groups = dataset_split(index, row[index], dataset)
            print(groups)
            gini = gini_index(groups, class_values)
            print('X%d < %.3f Gini=%.3f' % ((index + 1), row[index], gini))
            if gini < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    return {'index': b_index, 'value': b_value, 'groups': b_groups}


dataset = [[2.771244718, 1.784783929, 0],
           [1.728571309, 1.169761413, 0],
           [3.678319846, 2.81281357, 0],
           [3.961043357, 2.61995032, 0],
           [2.999208922, 2.209014212, 0],
           [7.497545867, 3.162953546, 1],
           [9.00220326, 3.339047188, 1],
           [7.444542326, 0.476683375, 1],
           [10.12493903, 3.234550982, 1],
           [6.642287351, 3.319983761, 1]]
split = split_datset(dataset)
print(split)
print('Split: [X%d < %.3f]' % ((split['index'] + 1), split['value']))
