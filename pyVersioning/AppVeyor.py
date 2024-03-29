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
"""AppVeyor specific code to collect the build environment."""
from os     import environ
from typing import Optional as Nullable

from pyTooling.Decorators import export

from pyVersioning.CIService import CIService, Platform, ServiceException


@export
class AppVeyor(CIService):
	"""Collect Git and other platform and environment information from environment variables provided by AppVeyor."""

	ENV_INCLUDE_FILTER =  ("APPVEYOR_", )
	ENV_EXCLUDE_FILTER =  ("_TOKEN", )
	ENV_INCLUDES =        ('CI', 'APPVEYOR', 'PLATFORM', 'CONFIGURATION')
	ENV_EXCLUDES =        ()

	def GetPlatform(self) -> Platform:
		return Platform("appveyor")

	def GetGitHash(self) -> str:
		try:
			return environ['APPVEYOR_REPO_COMMIT']
		except KeyError as ex:
			raise ServiceException from ex

	def GetGitBranch(self) -> Nullable[str]:
		try:
			return environ['APPVEYOR_REPO_BRANCH']
		except KeyError:
			return None

	def GetGitTag(self) -> Nullable[str]:
		try:
			return environ['APPVEYOR_REPO_TAG_NAME']
		except KeyError:
			return None

	def GetGitRepository(self) -> str:
		try:
			return environ['APPVEYOR_PROJECT_SLUG']
		except KeyError as ex:
			raise ServiceException from ex
