#!/usr/bin/python
import sys
import pickle

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

features_list = [
'poi',
'salary',
 'exercised_stock_options',
 'bonus'
 ]


### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


### Task 2: Remove outliers
data_dict.pop("TOTAL", 0)
data_dict.pop("THE TRAVEL AGENCY IN THE PARK", 0)

### Task 3: Create new feature(s)
def computeFraction( poi_messages, all_messages ):
   
    if poi_messages == "NaN" or all_messages == "NaN":
        fraction = 0.
    else:
        fraction = float(poi_messages)/all_messages

    return fraction

def calcFractionToPOI():

	for name in data_dict:

		data_point = data_dict[name]

		from_poi_to_this_person = data_point["from_poi_to_this_person"]
		to_messages = data_point["to_messages"]
		fraction_from_poi = computeFraction( from_poi_to_this_person, to_messages )
		data_point["fraction_from_poi"] = fraction_from_poi


		from_this_person_to_poi = data_point["from_this_person_to_poi"]
		from_messages = data_point["from_messages"]
		fraction_to_poi = computeFraction( from_this_person_to_poi, from_messages )
		data_point["fraction_to_poi"] = fraction_to_poi


### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

from sklearn.neighbors import KNeighborsClassifier
from sklearn import cross_validation
from sklearn.model_selection import GridSearchCV

skf = cross_validation.StratifiedKFold(labels, n_folds=4, shuffle=True)
knn = KNeighborsClassifier()
parameters = {'n_neighbors': [4,6,8,10]}
clf = GridSearchCV(knn, param_grid=parameters, cv=skf)
clf.fit(features,labels)

clf = KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_neighbors=4, p=2, weights='distance')

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)