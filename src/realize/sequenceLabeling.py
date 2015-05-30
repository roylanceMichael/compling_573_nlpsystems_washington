import cPickle as pickle
from compressionCacheGen import Alligned
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import SelectPercentile, chi2, VarianceThreshold
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC


compressionCorpusCache = "/home/thcrzy1/proj/cache/compressionCorpusCache/"
#compressionCorpusCache = "../cache/compressionCorpusCache/"

c_corpus = pickle.load(open(compressionCorpusCache+'c_Sentences_basic_features', 'r'))

wordFeatures = list()
allFeatures = list()
labels = list()
for a in c_corpus:
    for i in range(len(a)):
        f = a.features[i].copy()

        f.update(a.posfeatures[i])

        f["stem_"+a.stemmed[i][0]] = True
        f["affix_"+a.stemmed[i][1]] = True

        f.update(a.treefeatures[i])

        wordFeatures.append(f)
        f = f.copy()


        for prev in range(2):
            if i > prev:
                prevstring = "prev"+str(prev)+"_"
                f[prevstring+labels[-1-prev]] = True

                prevfeatures = wordFeatures[-2-prev]
                for k,v in prevfeatures.items():
                    if not k.startswith("in"):
                        f[prevstring+k] = v
                """
                #just pos
                for k,v in a.posfeatures[i-1-prev].items():
                    f[prevstring+k] = v
                """

        allFeatures.append(f)
        labels.append(a.labels[i])


#print(allFeatures[0])
#print(allFeatures[3])

partition = len(allFeatures) * 9 / 10
trainWordFeatures = allFeatures[:partition]
trainLabels = labels[:partition]
testWordFeatures = allFeatures[partition:]
testLabels = labels[partition:]

#print(wordFeatures)
vec = DictVectorizer()
trainfeaturevectors = vec.fit_transform(trainWordFeatures)
testfeaturevectors = vec.transform(testWordFeatures)

"""
vth = 0.1
varthresh = VarianceThreshold(threshold=vth*(1.0-vth))
trainfeaturevectors = varthresh.fit_transform(trainfeaturevectors, trainLabels)
testfeaturevectors = varthresh.transform(testfeaturevectors)
"""

#classifiers = [BernoulliNB(), DecisionTreeClassifier(), LogisticRegression(), OneVsRestClassifier(LinearSVC(random_state=0)) ]
#classifier_names = ["BernoulliNB", "DecisionTreeClassifier", "MaxEnt", "SVM"]

#classifiers = [LogisticRegression(), OneVsRestClassifier(LinearSVC(random_state=0)) ]
#classifier_names = ["MaxEnt", "SVM"]

classifiers = [LogisticRegression(), OneVsRestClassifier(LinearSVC(random_state=0)) ]
classifier_names = ["MaxEnt", "SVM"]

allscores = list()
for keep in range(3, 30, 3):
    selector = SelectPercentile(chi2, keep)
    selected_trainfeaturevectors = selector.fit_transform(trainfeaturevectors, trainLabels)
    selected_testfeaturevectors = selector.transform(testfeaturevectors)

    scores = list()
    for c in range(len(classifiers)):
        classifier = classifiers[c]

        classifier.fit(selected_trainfeaturevectors, trainLabels)
        scores.append((classifier.score(selected_testfeaturevectors, testLabels), keep, classifier_names[c], c))

    print(str(keep)+"\t"+"\t".join(str(s[0]) for s in scores))
    allscores += scores

print("saving the best classifier:")

bestsettings = max(allscores)
print(bestsettings)

bestselector = SelectPercentile(chi2, bestsettings[1])
selected_trainfeaturevectors = bestselector.fit_transform(trainfeaturevectors, trainLabels)
bestclassifier = classifiers[bestsettings[3]]
bestclassifier.fit(selected_trainfeaturevectors, trainLabels)

print(bestselector)
print(bestclassifier)

pickle.dump((vec, bestselector, bestclassifier), open(compressionCorpusCache+"compressionClassifier", 'wb'))

