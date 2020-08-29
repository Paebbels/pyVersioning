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
from dataclasses  import make_dataclass, dataclass
from os           import environ

@dataclass
class Platform():
	ci_service : str


class CIService:
	ENV_INCLUDE_FILTER =  ()
	ENV_EXCLUDE_FILTER =  ()
	ENV_INCLUDES =        []
	ENV_EXCLUDES =        []

	def getPlatform(self):
		raise NotImplemented()

	def getEnvironment(self):
		filteredEnv = {key:value for (key,value) in environ.items() if key.startswith(self.ENV_INCLUDE_FILTER) and not key.endswith(self.ENV_EXCLUDE_FILTER)}

		# manually add some variables
		for key in self.ENV_INCLUDES:
			try:
				filteredEnv[key] = environ[key]
			except:
				pass

		# manually delete some variables
		for key in self.ENV_EXCLUDES:
			try:
				del filteredEnv[key]
			except:
				pass

		Environment = make_dataclass(
			"Environment",
			[(name, str) for name in filteredEnv.keys()],
			namespace={
				'as_dict': lambda self: filteredEnv
			}
		)

		return Environment(**filteredEnv)

	def getGitHash(self) -> str:
		raise NotImplemented()

	def getGitBranch(self) -> str:
		raise NotImplemented()

	def getGitTag(self) -> str:
		raise NotImplemented()

	def getGitRepository(self) -> str:
		raise NotImplemented()


class WorkStation(CIService):
	def getPlatform(self):
		return Platform("NO-CI")
