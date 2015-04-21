__author__ = 'mroylance'
import operator


class Rules:
    # this will determine if the np's match in number
    # give higher weight to npModel2 being a pronoun
    def __init__(self):
        pass

    # generic rules
    def articleRule(self, npModel):
        return False

    def appositiveRule(self, npModel, sentIdx, sentences):
        return False

    def wordMatchingRule(self, npModel, sentIdx, sentences):
        return False

    # comparison rules
    def matchPlurality(self, npModel1, npModel2):
        return False

    def matchGender(self, npModel1, npModel2):
        return False

    def properNamesRule(self, npModel1, npModel2):
        return False

    def pronounTypesRule(self, npModel1, npModel2):
        return False

    def mismatchWordsRule(self, npModel1, npModel2):
        return False

    def headNounsDifferRule(self, npModel1, npModel2):
        return False

    def subsumeRule(self, npModel1, npModel2):
        return False

    def iMeRule(self, npModel1, npModel2):
        return False

    def specialThisRule(self, npModel1, npModel2):
        return False

    def findCorrectAntecedent(self, npModel, previousNps, sentences):
        # right now, just going to find the first np in the preceding sentence
        # get last noun phrase before current one
        scoringDict = {}

        for previousNp in previousNps:
            subsumeScore = self.subsume(npModel, previousNp)
            reverseSubsumeScore = self.subsume(previousNp, npModel)

            # we don't need to compare anymore if this is true
            # mismatch words score
            score1 = self.mismatchWords(npModel, previousNp) * 10
            #head noun differ score
            score2 = self.headNounsDiffer(npModel, previousNp)
            #difference in position score, testing out heavy emphasis on it...
            score3 = (npModel.position - previousNp.position).abs.to_f / 5000
            #pronoun score
            score4 = self.pronounTypes(npModel, previousNp)
            #plurality score
            #shouldn't this be ? 0 : 999? or maybe i don't understand ruby's ternary op's-ben
            #oh i see, your doing a change from greatest to least weighted np matching
            score5 = self.matchPlurality(npModel, previousNp)
            #proper names score
            score6 = self.properNames(npModel, previousNp)
            #gender score
            score7 = self.matchGender(npModel, previousNp)
            #article score
            score8 = self.articleRule(previousNp)
            #special this rule
            specialThisScore = self.specialThisRule(npModel, previousNp)

            totalScore = score1 + score2 + score3 + score4 + score5 + score6 + score7 + score8

            totalScore = totalScore + subsumeScore
            totalScore = totalScore + reverseSubsumeScore
            totalScore = totalScore + self.imerule(npModel, previousNp)
            totalScore = totalScore + specialThisScore

            scoringDict[previousNp] = totalScore

        sortedDict = sorted(scoringDict.items(), key=operator.itemgetter(1))
        return sortedDict[len(sortedDict) - 1]

    @staticmethod
    def updateDocumentWithCoreferences(docModel):
        return docModel