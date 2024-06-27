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
# Copyright 2020-2024 Patrick Lehmann - Bötzingen, Germany                                                             #
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
from pathlib               import Path
from typing                import Dict, Optional as Nullable

from ruamel.yaml           import YAML
from pyTooling.Decorators  import export
from pyTooling.MetaClasses import ExtendedType
from pyTooling.Versioning  import SemanticVersion


@export
class Base(metaclass=ExtendedType):
	"""Base-class for all configuration items."""

	root:   'Base'              #: Reference to configuration root node (document node).
	parent: Nullable['Base']    #: Reference to parent configuration node.

	def __init__(self, root: 'Base', parent: Nullable['Base']) -> None:
		"""
		Initialize base-class fields.

		:param root:   Reference to configuration root node (document node).
		:param parent: Reference to parent configuration node.
		"""
		self.root = root
		self.parent = parent


class Project(Base):
	"""Configuration class describing a *project*."""

	name:    str
	variant: Nullable[str]
	version: Nullable[SemanticVersion]

	def __init__(self, root: 'Base', parent: 'Base', settings: Dict) -> None:
		super().__init__(root, parent)

		self.name =    settings["name"]
		self.variant = settings["variant"] if "variant" in settings else None
		self.version = SemanticVersion.Parse(settings["version"]) if "version" in settings else None


class Compiler(Base):
	"""Configuration class describing a *compiler*."""

	name:          str
	version:       str
	configuration: str
	options:       str

	def __init__(self, root: 'Base', parent: 'Base', settings: Dict) -> None:
		super().__init__(root, parent)

		self.name =          settings["name"]
		self.version =       settings["version"]
		self.configuration = settings["configuration"]
		self.options =       settings["options"]


class Build(Base):
	"""Configuration class describing a *build*."""

	compiler: Nullable[Compiler]

	def __init__(self, root: 'Base', parent: 'Base', settings: Dict) -> None:
		super().__init__(root, parent)

		self.compiler = Compiler(root, self, settings["compiler"]) if "compiler" in settings else None


@export
class Configuration(Base):
	"""Configuration root node (document node)."""

	version: int
	project: Nullable[Project]
	build:   Nullable[Build]

	def __init__(self, configFile: Nullable[Path] = None) -> None:
		super().__init__(self, None)

		if configFile is None:
			self.version = 1
			self.project = Project(self, self, {
				"name":    "",
				"variant": "",
				"version": "v0.0.0"
			})
			self.build = Build(self, self, {
				"compiler": {
					"name": "",
					"version": "v0.0.0",
					"configuration": "",
					"options": ""
				}
			})
		else:
			self.load(configFile)

	def load(self, configFile: Path):
		# TODO: change to pyTooling.Configuration
		yaml =   YAML()
		config = yaml.load(configFile)

		self.version = int(config["version"]) if "version" in config else 1

		if self.version == 1:
			self.loadVersion1(config)

	def loadVersion1(self, config):
		self.project = Project(self, self, config["project"]) if "project" in config else None
		self.build =   Build(self, self, config["build"])     if "build" in config   else None
