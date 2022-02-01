# Written by Mansur Yeşilbursa
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import random

def load_data(dir):
    train_line_data = []
    test_line_data = []
    with open(dir, 'r') as f:
        for line in f.readlines():
            sample_type = random.uniform(0, 1)
            if sample_type < 0.2: # test sample
                test_line_data.append(line.rstrip('\n').split('\t'))
            else: # training sample
                train_line_data.append(line.rstrip('\n').split('\t'))
    train_data = np.asarray(train_line_data).astype(np.int)
    test_data = np.asarray(test_line_data).astype(np.int)
    return train_data[:, :4], train_data[:, 4], test_data[:, :4], test_data[:, 4]
    # x train, y train, x test, y test


if __name__ == '__main__':
    dir = '../features/tokenization_features_and_labels.txt'
    model_dir = '../models/tokenization/'
    x_train, y_train, x_test, y_test = load_data(dir)  # separate 20% for test data
    solver = 'liblinear'
    model = LogisticRegression(solver=solver, penalty='l1', verbose=1)
    model = model.fit(x_train, y_train)
    acc_train = model.score(x_train, y_train)
    acc_test = model.score(x_test, y_test)
    if acc_test > 0.8:
        model_name = 'tokenization_model_' + solver + '.pkl'
        with open(model_dir + model_name, 'wb') as f:
            pickle.dump(model, f)
    else:
        print('model accuracy is below 80%, it won\'t be saved')

    print('Training set accuracy: ' + str(acc_train))
    print('Test set accuracy: ' + str(acc_test))

