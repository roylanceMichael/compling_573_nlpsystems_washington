import cPickle as pickle
from compressionCacheGen import Alligned
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
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


print(allFeatures[0])
print(allFeatures[3])

partition = len(allFeatures) * 9 / 10
trainWordFeatures = allFeatures[:partition]
trainLabels = labels[:partition]
testWordFeatures = allFeatures[partition:]
testLabels = labels[partition:]

#print(wordFeatures)
vec = DictVectorizer()
trainfeaturevectors = vec.fit_transform(trainWordFeatures)
testfeaturevectors = vec.transform(testWordFeatures)

classifiers = [BernoulliNB(), DecisionTreeClassifier(), OneVsRestClassifier(LinearSVC(random_state=0)) ]

allscores = list()
for keep in range(10, 101, 10):
    selector = SelectPercentile(chi2, keep)
    trainfeaturevectors = selector.fit_transform(trainfeaturevectors, trainLabels)
    testfeaturevectors = selector.transform(testfeaturevectors)

    scores = list()
    for classifier in classifiers:
        #classifier = BernoulliNB()
        #classifier = DecisionTreeClassifier()
        #classifier = OneVsRestClassifier(LinearSVC(random_state=0))
        classifier.fit(trainfeaturevectors, trainLabels)
        scores.append((classifier.score(testfeaturevectors, testLabels), keep, classifier))

    print(str(keep)+"\t"+"\t".join(str(s[0]) for s in scores))
    allscores += scores

print(max(allscores))

#print(featurearray)
#print(vec.get_feature_names())

