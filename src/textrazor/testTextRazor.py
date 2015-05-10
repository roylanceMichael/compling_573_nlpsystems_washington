__author__ = 'thomas'
from textrazor import TextRazor

client = TextRazor(api_key="99cb513961595f163f4ab253a8aaf167970f8a49981e229a3c8505a0", \
				   extractors=["entities", "topics"])

text = """The druid was small and old.
He was the last of the druids, and he was very ill.
Oliver was his best friend, but he didn't know how to help the poor druid with his failing health.
Oliver went to the High King of the Faerie and asked for magic to help with the druid's ailment.
The Faerie King told Oliver that there was a special flower that grew high in the Mountains of the Giants.
He said that the flower could cure all known diseases, but that in order for it's magic to work, a deep sacrifice needed to be made.
The Elf King would not elaborate on what that sacrifice might entail.
Oliver said he was ready and set out upon the journey to help his friend, the druid.
"""

response = client.analyze(text)

for entity in response.entities():
	print entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types

