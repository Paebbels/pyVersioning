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
# Python package:     GitHub specific code to collect the build environment
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


class GitHub(CIService):
	ENV_INCLUDE_FILTER =  ("GITHUB_")
	ENV_EXCLUDE_FILTER =  ("_TOKEN")
	ENV_INCLUDES =        ['CI']
	ENV_EXCLUDES =        []

	def getPlatform(self):
		return Platform("github")

	def getGitHash(self):
		return environ['GITHUB_SHA']

	def getGitBranch(self):
		branchPrefix = "refs/heads/"

		try:
			ref = environ['GITHUB_REF']
			if ref.startswith(branchPrefix):
				return ref[len(branchPrefix):]
		except:
			pass

		return None

	def getGitTag(self):
		tagPrefix    = "refs/tags/"

		try:
			ref = environ['GITHUB_REF']
			if ref.startswith(tagPrefix):
				return ref[len(tagPrefix):]
		except:
			pass

		return None

	def getGitRepository(self):
		return environ['GITHUB_REPOSITORY']
