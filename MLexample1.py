import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import KFold, cross_validate
from sklearn.decomposition import PCA

def test_clasifier(clasifier, inputs, targets):
    fullpredictions = []

    for train_index, test_index in kf.split(data):
        #print("TRAIN:", train_index, "TEST:", test_index)
        clasifier.fit(inputs[train_index], targets[train_index])

        predictions = clasifier.predict(inputs[test_index])

        #print(predictions.tolist())

        fullpredictions += predictions.tolist()

        print("Predicted classes: ", predictions)
        print("Actual classes:    ", targets[test_index])
        print("Mean abs error: ", np.mean(abs(predictions-targets[test_index])))
        print("="*60)

    return fullpredictions


forest = RandomForestClassifier()
MLP = MLPClassifier(max_iter=700)
VEC = SVC()

data = pd.read_csv("Glass/glass.data")

#shuffle the rows so that like classes
#don't clump together.
data = data.sample(frac=1)

targets = np.array(data.loc[:, "type"])
data = data.loc[:, :"iron oxide"]

print(data)

scaler = StandardScaler()
scaled = scaler.fit_transform(data)

print(scaled)

kf = KFold(n_splits=10)

print("Random Forrest: ")

forestpredictions = test_clasifier(forest, scaled, targets)

forestcv = cross_validate(forest, scaled, targets, cv=5, return_train_score=True)
ftrain = forestcv["train_score"]
ftest = forestcv["test_score"]
plt.figure()
plt.boxplot([ftrain, ftest])
plt.title("Forrest training/testing results")
plt.show()

print("MLP: ")

MLPpredictions = test_clasifier(MLP, scaled, targets)

MLPcv = cross_validate(MLP, scaled, targets, cv=5, return_train_score=True)
mtrain = MLPcv["train_score"]
mtest = MLPcv["test_score"]
plt.figure()
plt.boxplot([mtrain, mtest])
plt.title("MLP training/testing results")
plt.show()

print("SVC: ")

SVCpredictions = test_clasifier(VEC, scaled, targets)

VECcv = cross_validate(VEC, scaled, targets, cv=5, return_train_score=True)
vtrain = VECcv["train_score"]
vtest = VECcv["test_score"]
plt.figure()
plt.boxplot([vtrain, vtest])
plt.title("SVC training/testing results")
plt.show()


##Scatter plots

pca = PCA(n_components=2)

actualcompressed = pca.fit_transform(data)

plt.figure()
plt.scatter(actualcompressed[:,0], actualcompressed[:,1], c=targets, cmap="viridis")
plt.title("PCA projection - Actual classes")
plt.show()

plt.figure()
plt.scatter(actualcompressed[:,0], actualcompressed[:,1], c=forestpredictions, cmap="viridis")
plt.title("PCA projection - Forest Predictions")
plt.show()

plt.figure()
plt.scatter(actualcompressed[:,0], actualcompressed[:,1], c=MLPpredictions, cmap="viridis")
plt.title("PCA projection - MLP Predictions")
plt.show()

plt.figure()
plt.scatter(actualcompressed[:,0], actualcompressed[:,1], c=SVCpredictions, cmap="viridis")
plt.title("PCA projection - SVC Predictions")
plt.show()
