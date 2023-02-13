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
# Copyright 2020-2023 Patrick Lehmann - Bötzingen, Germany                                                             #
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
"""GitHub specific code to collect the build environment."""
from datetime import datetime
from os     import environ
from typing import Optional as Nullable

from pyTooling.Decorators import export

from pyVersioning.CIService import CIService, Platform, ServiceException


@export
class GitHub(CIService):
	"""Collect Git and other platform and environment information from environment variables provided by GitHub Actions."""

	ENV_INCLUDE_FILTER =  ("GITHUB_", )
	ENV_EXCLUDE_FILTER =  ("_TOKEN", )
	ENV_INCLUDES =        ('CI', )
	ENV_EXCLUDES =        []

	def getPlatform(self) -> Platform:
		return Platform("github")

	def getGitHash(self) -> str:
		try:
			return environ['GITHUB_SHA']
		except KeyError as ex:
			raise ServiceException from ex

	def getGitBranch(self) -> Nullable[str]:
		branchPrefix = "refs/heads/"

		try:
			ref = environ['GITHUB_REF']
			if ref.startswith(branchPrefix):
				return ref[len(branchPrefix):]
		except KeyError:
			pass

		return None

	def getGitTag(self) -> Nullable[str]:
		tagPrefix    = "refs/tags/"

		try:
			ref = environ['GITHUB_REF']
			if ref.startswith(tagPrefix):
				return ref[len(tagPrefix):]
		except KeyError:
			pass

		return None

	def getGitRepository(self) -> str:
		try:
			return environ['GITHUB_REPOSITORY']
		except KeyError as ex:
			raise ServiceException from ex
