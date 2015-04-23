#!/bin/bash
# Mike Roylance (roylance@uw.edu)

firstCorporaPath=$1
secondCorporaPath=$2
topicXmlFile=$3
outputPath=$4
modelSummaryPath=$5
rougePath=$6


if [ -z "$1" ]; then
	firstCorporaPath="/corpora/LDC/LDC02T31/"
fi
if [ -z "$2" ]; then
	secondCorporaPath="/corpora/LDC/LDC08T25/data/"
fi
if [ -z "$3" ]; then
	topicXmlFile="../doc/Documents/devtest/simpleTest.xml"
fi
if [ -z "$4" ]; then
	outputPath="../outputs"
fi
if [ -z "$5" ]; then
	modelSummaryPath="/opt/dropbox/14-15/573/Data/models/devtest"
fi
if [ -z "$6" ]; then
	rougePath="../ROUGE"
fi



python2.7 summarizer.py --doc-input-path $firstCorporaPath --doc-input-path2 $secondCorporaPath --topic-xml $topicXmlFile --output-path $outputPath --gold-standard-summary-path $modelSummaryPath --rouge-path $rougePath
