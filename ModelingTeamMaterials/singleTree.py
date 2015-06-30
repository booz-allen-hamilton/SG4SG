import numpy as np
from sklearn import tree
from sklearn.externals.six import StringIO
import os
import pydot
import csv

image_name = "HumanTraffickingTree"
maxdepth = 8
data = csv.reader(open("../data/humantrafficking_data.csv","r"),delimiter=",")

Xnames = data.next()[2:]          # feature names
X = []            # training data
Y = []                      # targets of training data
for line in data:
    X.append(np.array(line[2:],dtype='i8'))
    Y.append(np.array(line[0],dtype='i8'))

clf = tree.DecisionTreeClassifier(criterion='entropy',max_depth=maxdepth) #initialize classifier
clf = clf.fit(X, Y)             # train the tree
#Z = [0,1]
#clf.predict([Z])         # predict the class of samples
#clf.predict_proba([Z])   # probability of each class can be predicted, which is the fraction of training samples of the same class in a leaf

training_accuracy =  sum(Y == clf.predict(X))/float(len(Y))         # predict the class of training data
print training_accuracy
#clf.predict_proba([Z])   # probability of each class can be predicted, which is the fraction of training samples of the same class in a leaf
#
#with open(image_name + ".dot", 'w') as f:
#     f = tree.export_graphviz(clf, out_file=f)  # create a graphic using graphviz

# we can use Graphvizs dot tool to create a PDF file (or any other supported file type)
# dot -Tpdf iris.dot -o iris.pdf
# dot -Tps iris.dot -o iris.ps
# dot -Tpng iris.dot -o iris.png

dot_data = StringIO() 
tree.export_graphviz(clf, out_file=dot_data, feature_names = Xnames) 
graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
#graph.write_pdf(image_name + ".pdf") 
graph.write_png(image_name + "_" + str(maxdepth) + "_" + ".png") 


def get_rules(dtree, feature_names):
        left      = dtree.tree_.children_left
        right     = dtree.tree_.children_right
        threshold = dtree.tree_.threshold
        features  = [feature_names[i] for i in dtree.tree_.feature]
        value = dtree.tree_.value

        def recurse(left, right, threshold, features, node):
                if (threshold[node] != -2):
                        print "if ( " + features[node] + " <= " + str(threshold[node]) + " ) {"
                        if left[node] != -1:
                                recurse (left, right, threshold, features,left[node])
                        print "} else {"
                        if right[node] != -1:
                                recurse (left, right, threshold, features,right[node])
                        print "}"
                else:
                        print "return " + str(value[node])

        recurse(left, right, threshold, features, 0)

#get_rules(clf,Xnames)
