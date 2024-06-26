import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(1337)  # for reproducibility
#from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import MinMaxScaler

from dbn.tensorflow import SupervisedDBNRegression

data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]

# Loading dataset
#boston = load_boston()
#X, Y = boston.data, boston.target
X, Y = data, target

# Splitting data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1337)

# Data scaling
min_max_scaler = MinMaxScaler()
X_train = min_max_scaler.fit_transform(X_train)

# Training
regressor = SupervisedDBNRegression(hidden_layers_structure=[100],
                                    learning_rate_rbm=0.01,
                                    learning_rate=0.01,
                                    n_epochs_rbm=20,
                                    n_iter_backprop=200,
                                    batch_size=16,
                                    activation_function='relu')
regressor.fit(X_train, Y_train)

# Test
X_test = min_max_scaler.transform(X_test)
Y_pred = regressor.predict(X_test)
print('Done.\nR-squared: %f\nMSE: %f' % (r2_score(Y_test, Y_pred), mean_squared_error(Y_test, Y_pred)))

plt.plot(list(Y_test), label='groundtruth-test')
plt.plot(list(Y_pred), label='predict-test')
plt.xlabel('data samples')
plt.ylabel('output')
plt.legend()
plot_title = 'comparison between predicted and groundtruth output' #+ appliance_name + ', model: ' + args.cnn + '. Running time: ' + str(running_time) + ' seconds'

plt.title(plot_title)
plt.show()
plt.savefig('result.jpg')
