#!/bin/bash
# Mike Roylance (roylance@uw.edu)

firstCorporaPath=$1
secondCorporaPath=$2
topicXmlFile=$3

if [ -z "$1" ]; then
	firstCorporaPath="/corpora/LDC/LDC02T31/"
fi
if [ -z "$2" ]; then
	secondCorporaPath="/corpora/LDC/LDC08T25/data/"
fi
if [ -z "$3" ]; then
	topicXmlFile="../doc/Documents/devtest/GuidedSumm10_test_topics.xml"
fi

python2.7 summarizer.py --doc-input-path $firstCorporaPath --doc-input-path2 $secondCorporaPath --topic-xml $topicXmlFile