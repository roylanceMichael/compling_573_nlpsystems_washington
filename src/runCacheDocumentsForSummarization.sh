#!/bin/bash
# Author:  Mike Roylance (roylance@uw.edu)
#
# run summarizer (without reordering) on all data from topic file
#

dataType=$1


# can be "devtest", "training", or "evaltest"
if [ -Z "$1" ]; then
	dataType="evaltest"
fi

if [ "devtest" == "$dataType" ]; then
	# for devtest Data
	corporaPath="/corpora/LDC/LDC02T31/"
	topicXmlFile="/opt/dropbox/14-15/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml"
elif [ "evaltest" == "$dataType" ]; then
	# for training data
	corporaPath="/corpora/LDC/LDC08T25/data/"
	topicXmlFile="/opt/dropbox/14-15/573/Data/Documents/training/2009/UpdateSumm09_test_topics.xml"
else
	# for evaltest data
	corporaPath="/corpora/LDC/LDC11T07/data/"
	topicXmlFile="/opt/dropbox/14-15/573/Data/Documents/evaltest/GuidedSumm11_test_topics.xml"
fi


python2.7 cacheDocumentsForSummarizationAsas.py --doc-input-path $corporaPath --topic-xml $topicXmlFile --data-type $dataType
