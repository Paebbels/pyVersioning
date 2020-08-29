# EMACS settings: -*-  tab-width: 2; indent-tabs-mode: t -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
# =============================================================================
#            __     __            _             _
#  _ __  _   \ \   / /__ _ __ ___(_) ___  _ __ (_)_ __   __ _
# | '_ \| | | \ \ / / _ \ '__/ __| |/ _ \| '_ \| | '_ \ / _` |
# | |_) | |_| |\ V /  __/ |  \__ \ | (_) | | | | | | | | (_| |
# | .__/ \__, | \_/ \___|_|  |___/_|\___/|_| |_|_|_| |_|\__, |
# |_|    |___/                                          |___/
# =============================================================================
# Authors:            Patrick Lehmann
#
# Python package:     pyVersioning configuration file in YAML format
#
# Description:
# ------------------------------------
#		TODO
#
# License:
# ============================================================================
# Copyright 2020-2020 Patrick Lehmann - Bötzingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============================================================================
#
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
