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

### Day 4 Testing and Training sets
testdata.next() #skipping header
for line in testdata:
    if select == 'y':
        TX.append(np.array([line[f] for f in feats],dtype='i8'))
    else:
        TX.append(np.array(line[2:],dtype='i8'))
    TY.append(np.array(line[0],dtype='i8'))

print "\nDecision tree test accuracy"
test_accuracy =  sum(TY == clf.predict(TX))/float(len(TY))         # predict the class of test data
print test_accuracy

#### Creating their own person of interest
Z = []
print "Your models features: ", Xnames
for name in Xnames:
    Z.append(int(raw_input("%s: " % name)))
print "___________________"
print "Predicted as class:", clf.predict([Z])[0]         # predict the class of POI

#clf.predict_proba([Z])   # probability of each class can be predicted, which is the fraction of training samples of the same class in a leaf

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
