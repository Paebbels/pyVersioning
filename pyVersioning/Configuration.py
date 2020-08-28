from pathlib        import Path
from re             import Pattern, compile, MULTILINE
from typing         import Dict, List

from ruamel.yaml    import YAML


class Base():
	root = None
	parent = None

	def __init__(self, root, parent):
		self.root = root
		self.parent = parent

class Configuration():
	class Project(Base):
		name    : str = None
		variant : str = None

		def __init__(self, root, parent, settings):
			super().__init__(root, parent)

			self.name     = settings['name']
			self.variant  = settings['variant']

	class Build(Base):
		class Compiler(Base):
			name          : str = None
			version       : str = None
			configuration : str = None
			options       : str = None

			def __init__(self, root, parent, settings):
				super().__init__(root, parent)

				self.name          = settings['name']
				self.version       = settings['version']
				self.configuration = settings['configuration']
				self.options       = settings['options']

		compiler     : Compiler = None

		def __init__(self, root, parent, settings):
			super().__init__(root, parent)

			if ('compiler' in settings):
				self.compiler = self.Compiler(root, self, settings['compiler'])


	version:          int =               None
	project:          Project =           None
	build:            Build =             None

	def __init__(self, configFile):
		yaml =   YAML()
		config = yaml.load(configFile)

		self.version =        int(config['version'])

		if self.version == 1:
			self.loadVersion1(config)

	def loadVersion1(self, config):
		self.project =        self.Project(self, self, config['project'])
		self.build =          self.Build(self, self, config['build'])
