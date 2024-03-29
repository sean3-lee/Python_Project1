import os
import matplotlib.pyplot as plt
from LogisticRegression import logistic_regression
from LRM import logistic_regression_multiclass
from DataReader import *

data_dir = "../data/"
train_filename = "training.npz"
test_filename = "test.npz"
    
def visualize_features(X, y):
    '''This function is used to plot a 2-D scatter plot of training features. 

    Args:
        X: An array of shape [n_samples, 2].
        y: An array of shape [n_samples,]. Only contains 1 or -1.


    plt.clf()
    plt.plot(X[y==1,0],X[y==1,1],'or' ,markersize=3)
    plt.plot(X[y==-1,0],X[y==-1,1],'ob' ,markersize=3)
    plt.legend(['1','2'],loc="lower left", title="Classes")
    plt.xlabel("Symmetry")
    plt.ylabel("Intensity")
    plt.xlim([-1,0])
    plt.ylim([-1,0])



def visualize_result(X, y, W):


    
    
    
    
    plt.clf()
    plt.plot(X[y==1,0],X[y==1,1],'or' ,markersize=3)
    plt.plot(X[y==-1,0],X[y==-1,1],'ob' ,markersize=3)
    plt.legend(['1','2'],loc="lower left", title="Classes")
    plt.xlabel("Symmetry")
    plt.ylabel("Intensity")
    #decision boundary
    symmetry = np.array([X[:,0].min(), X[:,0].max()])
    db = (-W[0] - W[1]*symmetry)/W[2]
    plt.plot(symmetry,db,'--k')
    plt.xlim([-1,0])
    plt.ylim([-1,0])


def visualize_result_multi(X, y, W):

    plt.clf()
    plt.plot(X[y==0,0],X[y==0,1],'og',markersize=3)
    plt.plot(X[y==1,0],X[y==1,1],'or',markersize=3)
    plt.plot(X[y==2,0],X[y==2,1],'ob',markersize=3)
    plt.legend(['0','1','2'],loc="lower left", title="Classes")
    plt.xlabel("Symmetry")
    plt.ylabel("Intensity")
    symrange = np.linspace(X[:,0].min(), X[:,0].max())
    db1 = np.zeros(symrange.shape)
    db2 = np.zeros(symrange.shape)
    for ix,x1 in enumerate(symrange):
        w0, w1, w2 = (W[0], W[1], W[2])
        db1[ix] = np.max([((w1[0] - w0[0]) + (w1[1] - w0[1])*x1)/(w0[2] - w1[2]),((w2[0] - w0[0]) + (w2[1] - w0[1])*x1)/(w0[2] - w2[2])])
        db2[ix] = np.min([((w0[0] - w1[0]) + (w0[1] - w1[1])*x1)/(w1[2] - w0[2]),((w2[0] - w1[0]) + (w2[1] - w1[1])*x1)/(w1[2] - w2[2])])
        plt.plot(symrange,db1,'--k')
        plt.plot(symrange,db2,'--k')
        plt.ylim([-1,0])
        plt.xlim([-1,0])



def main():
	# ------------Data Preprocessing------------
	# Read data for training.
    
    raw_data, labels = load_data(os.path.join(data_dir, train_filename))
    raw_train, raw_valid, label_train, label_valid = train_valid_split(raw_data, labels, 2300)

    ##### Preprocess raw data to extract features
    train_X_all = prepare_X(raw_train)
    valid_X_all = prepare_X(raw_valid)
    ##### Preprocess labels for all data to 0,1,2 and return the idx for data from '1' and '2' class.
    train_y_all, train_idx = prepare_y(label_train)
    valid_y_all, val_idx = prepare_y(label_valid)  

    ####### For binary case, only use data from '1' and '2'  
    train_X = train_X_all[train_idx]
    train_y = train_y_all[train_idx]
    ####### Only use the first 1350 data examples for binary training. 
    train_X = train_X[0:1350]
    train_y = train_y[0:1350]
    valid_X = valid_X_all[val_idx]
    valid_y = valid_y_all[val_idx]
    ####### set lables to  1 and -1. Here convert label '2' to '-1' which means we treat data '1' as postitive class. 

    train_y[np.where(train_y==2)] = -1
    valid_y[np.where(valid_y==2)] = -1

    data_shape = train_y.shape[0] 

#    # Visualize training data.
    visualize_features(train_X[:, 1:3], train_y)


   # ------------Logistic Regression Sigmoid Case------------

   ##### Check BGD, SGD, miniBGD
    logisticR_classifier = logistic_regression(learning_rate=0.5, max_iter=100)

    logisticR_classifier.fit_BGD(train_X, train_y)
    print(logisticR_classifier.get_params())
    print(logisticR_classifier.score(train_X, train_y))

    logisticR_classifier.fit_miniBGD(train_X, train_y, data_shape)
    print(logisticR_classifier.get_params())
    print(logisticR_classifier.score(train_X, train_y))

    logisticR_classifier.fit_SGD(train_X, train_y)
    print(logisticR_classifier.get_params())
    print(logisticR_classifier.score(train_X, train_y))

    logisticR_classifier.fit_miniBGD(train_X, train_y, 1)
    print(logisticR_classifier.get_params())
    print(logisticR_classifier.score(train_X, train_y))

    logisticR_classifier.fit_miniBGD(train_X, train_y, 10)
    print(logisticR_classifier.get_params())
    print(logisticR_classifier.score(train_X, train_y))


    # Explore different hyper-parameters.

    best_logisticR = logistic_regression(learning_rate=0.1, max_iter=1000)
    best_logisticR.fit_SGD(train_X, train_y)
    print("\n\nLogistic Regression Sigmoid - Best")
    print("weights:\n", best_logisticR.get_params())
    print("train accuracy: ",best_logisticR.score(train_X,train_y))
    print("validation accuracy: ",best_logisticR.score(valid_X,valid_y))


	# Visualize the your 'best' model after training.
	# visualize_result(train_X[:, 1:3], train_y, best_logisticR.get_params())


    visualize_result(train_X[:, 1:3], train_y, best_logisticR.get_params())
    



    # Use the 'best' model above to do testing. Note that the test data should be loaded and processed in the same way as the training data.

    raw_test, label_test = load_data(os.path.join(data_dir, test_filename))
    
    test_X_all = prepare_X(raw_test)
    ##### Preprocess labels for all data to 0,1,2 and return the idx for data from'1' and '2' class.
    
    test_y_all, test_idx = prepare_y(label_test)
    ####### For binary case, only use data from '1' and '2'
    
    test_X = test_X_all[test_idx]
    
    test_y = test_y_all[test_idx]####### set lables to1 and -1. Here convert label '2' to '-1' which means wetreat data '1' as postitive class.
    
    test_y[np.where(test_y==2)] = -1
    data_shape= test_y.shape[0]####### get score on test data
    print("test accuracy:", best_logisticR.score(test_X, test_y))
    print("\n\nMulticlass default params:")
    ### END YOUR CODE


    # ------------Logistic Regression Multiple-class case, let k= 3------------
    ###### Use all data from '0' '1' '2' for training
    train_X = train_X_all
    train_y = train_y_all
    valid_X = valid_X_all
    valid_y = valid_y_all

    #########  miniBGD for multiclass Logistic Regression
    
    # Explore different hyper-parameters.

    best_logistic_multi_R = logistic_regression_multiclass(learning_rate=0.1,max_iter=1000,k= 3)
    print("\n\nLR-Multiclass - best")
    best_logistic_multi_R.fit_miniBGD(train_X, train_y, 10)
    print("weights:\n", best_logistic_multi_R.get_params())
    print("train accuracy: ",best_logistic_multi_R.score(train_X, train_y))
    print("validation accuracy: ",best_logistic_multi_R.score(valid_X, valid_y))


	# Visualize the your 'best' model after training.
	# visualize_result_multi(train_X[:, 1:3], train_y, best_logistic_multi_R.get_params())


    # Use the 'best' model above to do testing.

    visualize_result_multi(train_X[:, 1:3], train_y,best_logistic_multi_R.get_params())
    print("test accuracy: ", best_logistic_multi_R.score(test_X_all, test_y_all))



    # ------------Connection between sigmoid and softmax------------
    ############ Now set k=2, only use data from '1' and '2' 

    #####  set labels to 0,1 for softmax classifer
    train_X = train_X_all[train_idx]
    train_y = train_y_all[train_idx]
    train_X = train_X[0:1350]
    train_y = train_y[0:1350]
    valid_X = valid_X_all[val_idx]
    valid_y = valid_y_all[val_idx] 
    train_y[np.where(train_y==2)] = 0
    valid_y[np.where(valid_y==2)] = 0  
    
    ###### First, fit softmax classifer until convergence, and evaluate 

    logisticR_classifier_multiclass =logistic_regression_multiclass(learning_rate=0.01, max_iter=10000,k= 2)
    logisticR_classifier_multiclass.fit_miniBGD(train_X, train_y, 10)
    print("\n\n2-Class Softmax LR")
    print("weights:\n", logisticR_classifier_multiclass.get_params())
    print("train accuracy: ", logisticR_classifier_multiclass.score(train_X,train_y))
    print("validation accuracy: ", logisticR_classifier_multiclass.score(valid_X,valid_y))
    test_X = test_X_all[test_idx]
    test_y = test_y_all[test_idx]
    test_y[np.where(test_y==2)] = 0
    print("test accuracy: ", logisticR_classifier_multiclass.score(test_X, test_y))







    train_X = train_X_all[train_idx]
    train_y = train_y_all[train_idx]
    train_X = train_X[0:1350]
    train_y = train_y[0:1350]
    valid_X = valid_X_all[val_idx]
    valid_y = valid_y_all[val_idx] 
    #####       set lables to -1 and 1 for sigmoid classifer

    best_logisticR = logistic_regression(learning_rate=0.02, max_iter=10000)
    best_logisticR.fit_BGD(train_X, train_y)
    print("\n\nBinary Sigmoid LR")
    print("weights:\n", best_logisticR.get_params())
    print("train accuracy: ",best_logisticR.score(train_X,train_y))
    print("validation accuracy: ", best_logisticR.score(valid_X,valid_y))
    test_X = test_X_all[test_idx]
    test_y = test_y_all[test_idx]
    test_y[np.where(test_y==2)] = -1
    print("test accuracy: ", best_logisticR.score(test_X,test_y))


    ###### Next, fit sigmoid classifer until convergence, and evaluate

    sigmoid = logistic_regression(learning_rate=1, max_iter=1)
    softmax = logistic_regression_multiclass(learning_rate=0.5, max_iter=1,k= 2)
    sigmoid.fit_miniBGD(train_X, train_y,10)
    train_y[np.where(train_y==-1)] = 0
    print("sigma weights:\n", sigmoid.get_params())
    print("softm weights:\n", softmax.get_params())
    softmax.fit_miniBGD(train_X,train_y, 1)
    



    # ------------End------------
    

if __name__ == '__main__':
	main()
    
    
