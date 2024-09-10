# Function 1: SVM Code (from 7.txt)
def p7():
    print("""
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

iris = datasets.load_iris()
x = iris.data[:, :2]
y = iris.target
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

model = SVC(kernel='linear', C=1.0)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

def plot_decision_boundaries(x, y, model):
    h = 0.02
    x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
    y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)
    plt.contourf(xx, yy, z, alpha=0.8)
    plt.scatter(x[:, 0], x[:, 1], c=y, edgecolors='k', marker='o')
    plt.xlabel('Sepal Length')
    plt.ylabel('Sepal Width')
    plt.title('SVM Decision Boundaries')
    plt.show()

plot_decision_boundaries(x, y, model)
    """)

# Function 2: KMeans & EM Algorithm Code (from 9.txt)
def p8():
    print("""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

data=pd.read_csv("EM.csv")
print("Input data and shape")
print(data.shape)
print(data.head())

f1=data['V1'].values
f2=data['V2'].values
x=np.array(list(zip(f1,f2)))

print("X: ",x)
print("Graph for whole data set: ")
plt.scatter(f1,f2,c="black",s=7)
plt.show()

Kmeans=KMeans(2,random_state=0)
labels=Kmeans.fit(x).predict(x)
centroids=Kmeans.cluster_centers_
print("Centroids : ",centroids)
plt.scatter(x[:,0],x[:,1],c=labels,s=40,cmap='viridis')
print("Graph using Kmeans algorithm : ")
plt.scatter(centroids[:,0],centroids[:,1],s=200,marker='*',c='#050505')
plt.show()

gmm=GaussianMixture(n_components=3).fit(x)
labels=gmm.predict(x)
prob=gmm.predict_proba(x)
size=10*prob.max(1)**3
print("Graph using EM algorithm")
plt.scatter(x[:,0],x[:,1],c=labels,s=size,cmap='viridis')
plt.show()
    """)

# Function 3: Naive Bayes Classification Code (from 8.txt)
def p9():
    print("""
import csv
import math
import random
import statistics

# Calculate the probability based on the Gaussian distribution
def cal_probability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent

# Read the dataset
dataset = []
dataset_size = 0

# Open the CSV file
with open('NaiveBC.csv') as csvfile:
    lines = csv.reader(csvfile)
    for row in lines:
        dataset.append([float(attr) for attr in row])

dataset_size = len(dataset)
print("Size of dataset is: ", dataset_size)

# Split the dataset into train and test sets (70% training data)
train_size = int(0.7 * dataset_size)
print("Training set size: ", train_size)

X_train = []
X_test = dataset.copy()

# Select random training indices
training_indexes = random.sample(range(dataset_size), train_size)

# Split the dataset into X_train and X_test
for i in training_indexes:
    X_train.append(dataset[i])
    X_test.remove(dataset[i])

# Organize the training data by class
classes = {}
for sample in X_train:
    class_value = int(sample[-1])  # Assume the last attribute is the class label
    if class_value not in classes:
        classes[class_value] = []
    classes[class_value].append(sample)

# Calculate mean and standard deviation for each attribute in each class
summaries = {}
for class_value, training_data in classes.items():
    summary = [(statistics.mean(attribute), statistics.stdev(attribute)) for attribute in zip(*training_data)]
    del summary[-1]  # Remove the class label summary
    summaries[class_value] = summary

# Print the class summaries (mean and stdev for each attribute)
print("Summaries by class:")
print(summaries)

# Classify the test data
X_prediction = []
for i in X_test:
    probabilities = {}
    for class_value, class_summary in summaries.items():
        probabilities[class_value] = 1
        for index, attr in enumerate(class_summary):
            probabilities[class_value] *= cal_probability(i[index], attr[0], attr[1])

    # Choose the class with the highest probability
    best_label, best_prob = None, -1
    for class_value, probability in probabilities.items():
        if best_label is None or probability > best_prob:
            best_prob = probability
            best_label = class_value
    X_prediction.append(best_label)

# Calculate the accuracy
correct = 0
for index, key in enumerate(X_test):
    if X_test[index][-1] == X_prediction[index]:
        correct += 1

print("Accuracy: ", (correct / float(len(X_test))) * 100)
    """)

# Function 4: DBSCAN Algorithm Code (from the initial message)
def p10():
    print("""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN

# Define the data points
points = np.array([[8, 7], [4, 6], [5, 5], [6, 4], [7, 3], [6, 7], [2, 8], [4, 3], [3, 3], [2, 6], [3, 5], [2, 4]])

# Plot the data points
plt.figure(figsize=(6,6))
plt.scatter(points[:,0], points[:,1], color='b')
plt.title("Raw Data Points")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

# Apply DBSCAN
db = DBSCAN(eps=1.9, min_samples=4).fit(points)
labels = db.labels_

# Extract core points, border points, and noise points
core_points_mask = np.zeros_like(labels, dtype=bool)
core_points_mask[db.core_sample_indices_] = True
border_points_mask = (labels != -1) & ~core_points_mask
noise_points_mask = labels == -1

# Plot core points, border points, and noise points
plt.figure(figsize=(6,6))
plt.scatter(points[core_points_mask, 0], points[core_points_mask, 1], color='red', marker='o', label='Core Points')
plt.scatter(points[border_points_mask, 0], points[border_points_mask, 1], color='green', marker='o', label='Border Points')
plt.scatter(points[noise_points_mask, 0], points[noise_points_mask, 1], color='black', marker='x', label='Noise Points')

# Plot circles around core points
for point in points[core_points_mask]:
    circle = plt.Circle((point[0], point[1]), 1.9, color='blue', fill=False, linestyle='dotted')
    plt.gca().add_artist(circle)

plt.title("DBSCAN Clustering with Approximate Boundaries")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.axis('equal')
plt.show()

print("DBSCAN Labels:", labels)
    """)

# Call these functions to print their respective code
