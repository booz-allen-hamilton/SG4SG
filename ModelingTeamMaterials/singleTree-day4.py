import numpy as np
from sklearn import tree
from sklearn.externals.six import StringIO
import os
import pydot
import csv

print "\nDecision Tree using Human Trafficking Case File Data"
print "\tpowered by Booz Allen Hamiltion and Girls Inc.\n"
image_name = "HumanTraffickingTree"
maxdepth = int(input('Max Depth: '))
while maxdepth <= 1:
    print 'Max Depth must be greater than 1.'
    maxdepth = int(input('Max Depth: '))

data = csv.reader(open("../data/humantrafficking_data.csv","r"),delimiter=",")
testdata = csv.reader(open("../data/humantrafficking_TEST_data.csv","r"),delimiter=",")
Xnames = data.next()[2:]          # feature names
X = []                            # training data
Y = []                            # targets of training data
TX = []
TY = []

select = raw_input("Would you like to select features? (y/n) ")
while not (select == 'y' or select == 'n'):
    select = raw_input("Would you like to select features? (y/n) ")

if select == 'y':
    for ind, name in enumerate(Xnames):
        print "%s. %s" %(ind,name)
    feats = raw_input("Enter the features you would like to use. Example 1,2,3:  ").split(",")
    Xnames = [Xnames[int(f)] for f in feats]
    feats = [int(f) + 2 for f in feats]
else:
    print "All features available will be used"

for line in data:
    if select == 'y':
        X.append(np.array([line[f] for f in feats],dtype='i8'))
    else:
        X.append(np.array(line[2:],dtype='i8'))
    Y.append(np.array(line[0],dtype='i8'))

clf = tree.DecisionTreeClassifier(criterion='entropy',max_depth=maxdepth) #initialize classifier
clf = clf.fit(X, Y)             # train the tree

print "Decision tree training accuracy"
training_accuracy =  sum(Y == clf.predict(X))/float(len(Y))         # predict the class of training data
print training_accuracy

dot_data = StringIO() 
tree.export_graphviz(clf, out_file=dot_data, feature_names = Xnames) 
graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
#graph.write_pdf(image_name + ".pdf") 
graph.write_png(image_name + "_" + str(maxdepth) + "_" + ".png") 
