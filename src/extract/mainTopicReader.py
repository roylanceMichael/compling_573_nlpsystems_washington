import json
import re
import topicReader

def main():
	for topic in topicReader.Topic.factoryMultiple("doc/Documents/devtest/GuidedSumm10_test_topics.xml"):
		print topic

if __name__ == '__main__':
    main()