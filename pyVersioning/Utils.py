from typing import List


class SelfDescriptive:
	_public: List

	def Keys(self):
		for element in self._public:
			yield element

	def KeyValuePairs(self):
		for element in self._public:
			value = self.__getattribute__(element)
			yield (element, value)
