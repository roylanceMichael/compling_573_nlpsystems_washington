#!/bin/bash
# Mike Roylance (roylance@uw.edu)

firstCorporaPath=$1
secondCorporaPath=$2
topicXmlFile=$3
summaryOutputPath=$4
modelSummaryPath=$5
rougePath=$6
evalOutputPath=$7

if [ -z "$1" ]; then
	firstCorporaPath="/corpora/LDC/LDC02T31/"
fi
if [ -z "$2" ]; then
	secondCorporaPath="/corpora/LDC/LDC08T25/data/"
fi
if [ -z "$3" ]; then
	topicXmlFile="../doc/Documents/devtest/GuidedSumm10_test_topics.xml"
fi
if [ -z "$4" ]; then
	summaryOutputPath="../outputs"
fi
if [ -z "$5" ]; then
	modelSummaryPath="/opt/dropbox/14-15/573/Data/models/devtest"
fi
if [ -z "$6" ]; then
	rougePath="/opt/dropbox/14-15/573/code/ROUGE"
fi
if [ -z "$7" ]; then
	evalOutputPath="../outputs/evaluations"
fi


python2.7 summarizer.py --doc-input-path $firstCorporaPath --doc-input-path2 $secondCorporaPath --topic-xml $topicXmlFile --summary-output-path $summaryOutputPath --gold-standard-summary-path modelSummaryPath --rouge-path $rougePath --evaluation-output-path evalOutputPath