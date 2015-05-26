__author__ = 'mroylance'

from entitygrid.entityGrid import EntityGrid

#
# AsasEntityGrid:  generates an entity grid ala Barsilay and Lapata (2005)
#			   uses ASAS to mark named entities.
#
class AsasEntityGrid(EntityGrid):
	# build entity grid
	def __init__(self, sentences):
		EntityGrid.__init__(self, sentences)
		self.entities = []

		for sentence in sentences:
			for entity in sentence.entities:
				self.entities.append(entity)
				# print entity

		self.matrixIndices = self.getMatrixIndices(self.getEntityIdsFromAsasEntities())
		self.grid = self.fillMatrix()
		self.compressMatrix()

	def fillMatrix(self):
		matrix = self.makeEmptyMatrix(len(self.matrixIndices))

		sNum = 0
		for sentence in self.sentences:
			for entity in sentence.entityScores:
				self.setEntityUseType(entity[4], matrix, sNum, sentence.entityScores[entity])
			sNum += 1

		return matrix

	def getEntityIdsFromAsasEntities(self):
		entityIds = set()
		for entity in self.entities:
			if entity[4] not in entityIds:
				entityIds.add(entity[4])
		return entityIds




