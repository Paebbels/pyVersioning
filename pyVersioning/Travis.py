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
"""Travis  specific code to collect the build environment."""
from os import environ

from pyVersioning.CIService import CIService, Platform, ServiceException


class Travis(CIService):
	ENV_INCLUDE_FILTER =  ("TRAVIS_")
	ENV_EXCLUDE_FILTER =  ("_TOKEN")
	ENV_INCLUDES =        ['CI', 'CONTINUOUS_INTEGRATION', 'TRAVIS']
	ENV_EXCLUDES =        []

	def getPlatform(self) -> Platform:
		return Platform("travis")

	def getGitHash(self) -> str:
		try:
			return environ['TRAVIS_COMMIT']
		except KeyError as ex:
			raise ServiceException from ex

	def getGitBranch(self) -> str:
		try:
			return environ['TRAVIS_BRANCH']
		except KeyError:
			pass

		return None

	def getGitTag(self) -> str:
		try:
			return environ['TRAVIS_TAG']
		except KeyError:
			pass

		return None

	def getGitRepository(self) -> str:
		try:
			return environ['TRAVIS_REPO_SLUG']
		except KeyError as ex:
			raise ServiceException from ex
