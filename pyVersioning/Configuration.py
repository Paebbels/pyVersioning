# ==================================================================================================================== #
#            __     __            _             _                                                                      #
#  _ __  _   \ \   / /__ _ __ ___(_) ___  _ __ (_)_ __   __ _                                                          #
# | '_ \| | | \ \ / / _ \ '__/ __| |/ _ \| '_ \| | '_ \ / _` |                                                         #
# | |_) | |_| |\ V /  __/ |  \__ \ | (_) | | | | | | | | (_| |                                                         #
# | .__/ \__, | \_/ \___|_|  |___/_|\___/|_| |_|_|_| |_|\__, |                                                         #
# |_|    |___/                                          |___/                                                          #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2020-2021 Patrick Lehmann - Bötzingen, Germany                                                             #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
#                                                                                                                      #
# SPDX-License-Identifier: Apache-2.0                                                                                  #
# ==================================================================================================================== #
#
"""pyVersioning configuration file in YAML format."""
from pathlib        import WindowsPath, PosixPath
from typing         import Dict

from pyTooling.MetaClasses  import Overloading
from ruamel.yaml            import YAML

from pyTooling.Versioning   import SemVersion


class Base():
	root:   'Base' =  None
	parent: 'Base' =  None

	def __init__(self, root: 'Base', parent: 'Base'):
		self.root =   root
		self.parent = parent

class Configuration(Base, metaclass=Overloading):
	class Project(Base):
		name    : str     = None
		variant : str     = None
		version : SemVersion = None

		def __init__(self, root: 'Base', parent: 'Base', settings: Dict):
			super().__init__(root, parent)

			self.name     = settings['name']
			if 'variant' in settings:
				self.variant  = settings['variant']
			if 'version' in settings:
				self.version  = SemVersion(settings['version'])

	class Build(Base):
		class Compiler(Base):
			name          : str = None
			version       : str = None
			configuration : str = None
			options       : str = None

			def __init__(self, root: 'Base', parent: 'Base', settings: Dict):
				super().__init__(root, parent)

				self.name          = settings['name']
				self.version       = settings['version']
				self.configuration = settings['configuration']
				self.options       = settings['options']

		compiler : Compiler = None

		def __init__(self, root: 'Base', parent: 'Base', settings: Dict):
			super().__init__(root, parent)

			if ('compiler' in settings):
				self.compiler = self.Compiler(root, self, settings['compiler'])


	version : int =     None
	project : Project = None
	build   : Build =   None

	def __init__(self):
		self.version = 1
		self.project = self.Project(self, self, {
			"name": "",
			"variant": "",
			"version": "v0.0.0"
		})

	def __init__(self, configFile: PosixPath):
		self.load(configFile)

	def __init__(self, configFile: WindowsPath):
		self.load(configFile)

	def load(self, configFile):
		yaml =   YAML()
		config = yaml.load(configFile)

		if 'version' in config:
			self.version = int(config['version'])
		else:
			self.version = 1

		if self.version == 1:
			self.loadVersion1(config)

	def loadVersion1(self, config):
		if 'project' in config:
			self.project = self.Project(self, self, config['project'])

		if 'build' in config:
			self.build = self.Build(self, self, config['build'])
