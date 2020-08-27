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
# Python package:     AppVeyor specific code to collect the build environment
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
from os import environ

from pyVersioning.CIService import CIService, Platform


class AppVeyor(CIService):
	ENV_INCLUDE_FILTER =  ("APPVEYOR_")
	ENV_EXCLUDE_FILTER =  ("_TOKEN")
	ENV_INCLUDES =        ['CI', 'APPVEYOR', 'PLATFORM', 'CONFIGURATION']
	ENV_EXCLUDES =        []

	def getPlatform(self):
		return Platform("appveyor")

	def getGitHash(self):
		return environ['APPVEYOR_REPO_COMMIT']

	def getGitBranch(self):
		try:
			return environ['APPVEYOR_REPO_BRANCH']
		except:
			pass

		return None

	def getGitTag(self):
		try:
			return environ['APPVEYOR_REPO_TAG_NAME']
		except:
			pass

		return None

	def getGitRepository(self):
		return environ['APPVEYOR_PROJECT_SLUG']
