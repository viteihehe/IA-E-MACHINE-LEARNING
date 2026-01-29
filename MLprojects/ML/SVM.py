import sklearn.svm as SVM
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, learning_curve
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#importando o dataset e o modelo de SVM

def grafico(data):
    #Tornando a leutura dos dados melhor
    breast_df = pd.DataFrame(data=data.data, columns=data.feature_names)
    breast_df['Target'] = data.target
    breast_df['Target Name'] = pd.Categorical.from_codes(data.target, data.target_names)
    print(breast_df.head())
    breast_df.plot.scatter('mean radius','mean texture', c=data.target, cmap='viridis')
    plt.show()

#Carregando o dataset
data = load_breast_cancer()
grafico(data)

def main():
    X = data.data
    y = data.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=33, test_size=0.3)
    clf = SVM.SVC(C=1, kernel='poly')
    clf.fit(X_train, y_train)
    clf.predict(X_test)
    score = clf.score(X_test, y_test)
    print(score)
main()