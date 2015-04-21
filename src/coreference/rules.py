__author__ = 'mroylance'
import collections
import npModel

nounPhraseKey = "NP"
i = "i"
me = "me"
it = "it"

pronounTypes = {"PRP": None, "PRP$": None, "WP": None, "WP$": None}
badWords = ["a", "an", "the", "of"]

# this will determine if the np's match in number
# give higher weight to npModel2 being a pronoun
# generic rules
def articleRule(npModel):
    return False

def appositiveRule(npModel, sentIdx, sentences):
    return False

def wordMatchingRule(npModel, sentIdx, sentences):
    return False

# comparison rules
def matchPlurality(npModel1, npModel2):
    return False

def matchGender(npModel1, npModel2):
    return False

def properNamesRule(npModel1, npModel2):
    return False

def pronounTypesRule(npModel1, npModel2):
    return False

def mismatchWordsRule(npModel1, npModel2):
    return False

def headNounsDifferRule(npModel1, npModel2):
    return False

def subsumeRule(npModel1, npModel2):
    firstNp = str(npModel1).lower().strip()
    secondNp = str(npModel2).lower().strip()

    if len(firstNp) <= 1 or len(secondNp) <= 1:
        return 0

    if firstNp == it and secondNp == it:
        return -9999

    if npModel1.tag not in pronounTypes or npModel2.tag not in pronounTypes:
        return 0

    for badWord in badWords:
        if badWord in firstNp or badWord in secondNp:
            return 0

    if firstNp in secondNp:
        return -9999
    return 0

def iMeRule(npModel1, npModel2):
    norm1 = str(npModel1).lower().strip()
    norm2 = str(npModel2).lower().strip()

    if (norm1 == me and norm2 == i) or (norm1 == i and norm2 == me):
        return -9999

    return False

# not implementing for now
def specialThisRule(npModel1, npModel2):
    return 0

def findCorrectAntecedent(npModel, previousNps, sentences):
    # right now, just going to find the first np in the preceding sentence
    # get last noun phrase before current one
    scoringDict = {}

    distance = 0
    for previousNp in previousNps:
        distance += 1

        subsumeScore = subsumeRule(npModel, previousNp)
        reverseSubsumeScore = subsumeRule(previousNp, npModel)

        # we don't need to compare anymore if this is true
        # mismatch words score
        score1 = mismatchWordsRule(npModel, previousNp) * 10
        # head noun differ score
        score2 = headNounsDifferRule(npModel, previousNp)
        # difference in position score, testing out heavy emphasis on it...
        score3 = distance / float(5000)
        # pronoun score
        score4 = pronounTypesRule(npModel, previousNp)
        # plurality score
        score5 = matchPlurality(npModel, previousNp)
        # proper names score
        score6 = properNamesRule(npModel, previousNp)
        # gender score
        score7 = matchGender(npModel, previousNp)
        # article score
        score8 = articleRule(previousNp)
        # special this rule
        specialThisScore = specialThisRule(npModel, previousNp)

        totalScore = score1 + score2 + score3 + score4 + score5 + score6 + score7 + score8

        totalScore = totalScore + subsumeScore
        totalScore = totalScore + reverseSubsumeScore
        totalScore = totalScore + iMeRule(npModel, previousNp)
        totalScore = totalScore + specialThisScore

        scoringDict[totalScore] = previousNp

    od = collections.OrderedDict(sorted(scoringDict.items()))
    for item in od.items():
        if item[0] > 0:
            return None
        return item[1]
    return None

def updateDocumentWithCoreferences(docModel):
    previousItems = []
    sentences = []
    coreferencePairs = []

    for paragraph in docModel.paragraphs:
        for sentence in paragraph:
            for chunk in sentence:
                np = npModel.NpModel(chunk)

                if np.tag == nounPhraseKey:
                    result = findCorrectAntecedent(np, previousItems, sentences)
                    if result != None:
                        coreferencePairs.append((np, result))

                previousItems.insert(0, np)
            sentences.insert(0, sentence)

    return coreferencePairs