import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle

if __name__ == '__main__':
    data_dir = '../features/'
    model_dir = '../models/sentence_splitting/'
    x = np.load(data_dir + 'sentence_train_features.npy')
    y = np.load(data_dir + 'sentence_train_labels.npy')
    x_test = np.load(data_dir + 'sentence_test_features.npy')
    y_test = np.load(data_dir + 'sentence_test_labels.npy')
    solver = 'liblinear'
    model = LogisticRegression(solver=solver, penalty='l1', verbose=1)
    model.fit(x, y)
    train_acc = model.score(x, y)
    test_acc = model.score(x_test, y_test)
    if test_acc > 0.9:
        with open(model_dir + 'model_' + solver + '.pkl', 'wb') as f:
            pickle.dump(model, f)
    print('Training set accuracy: ' + str(train_acc))
    print('Test set accuracy: ' + str(test_acc))