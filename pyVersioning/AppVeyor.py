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

from pyTooling.Decorators      import export
from pyTooling.Exceptions      import ToolingException
from pyTooling.GenericPath.URL import URL


from pyVersioning.CIService import CIService, Platform, ServiceException


@export
class AppVeyor(CIService):
	"""Collect Git and other platform and environment information from environment variables provided by AppVeyor."""

	ENV_INCLUDE_FILTER =  ("APPVEYOR_", )                                    #: List of environment variable name pattern for inclusion.
	ENV_EXCLUDE_FILTER =  ("_TOKEN", )                                       #: List of environment variable name pattern for exclusion.
	ENV_INCLUDES =        ("CI", "APPVEYOR", "PLATFORM", "CONFIGURATION")    #: List of environment variable to include.
	ENV_EXCLUDES =        ()                                                 #: List of environment variable to exclude.

	def GetPlatform(self) -> Platform:
		return Platform("appveyor")

	def GetGitHash(self) -> str:
		"""
		Returns the Git hash (SHA1 - 160-bit) as a string.

		:return:                  Git hash as a hex formated string (40 characters).
		:raises ServiceException: If environment variable ``APPVEYOR_REPO_COMMIT`` was not found.
		"""
		try:
			return environ["APPVEYOR_REPO_COMMIT"]
		except KeyError as ex:
			raise ServiceException(f"Can't find AppVeyor environment variable 'APPVEYOR_REPO_COMMIT'.") from ex

	def GetGitBranch(self) -> Nullable[str]:
		"""
		Returns Git branch name or ``None`` is not checked out on a branch.

		:return:                  Git branch name or ``None``.
		:raises ServiceException: If environment variable ``APPVEYOR_REPO_BRANCH`` was not found.
		"""
		try:
			return environ["APPVEYOR_REPO_BRANCH"]
		except KeyError:
			return None

	def GetGitTag(self) -> Nullable[str]:
		"""
		Returns Git tag name or ``None`` is not checked out on a branch.

		:return:                  Git tag name or ``None``.
		:raises ServiceException: If environment variable ``APPVEYOR_REPO_TAG_NAME`` was not found.
		"""
		try:
			return environ["APPVEYOR_REPO_TAG_NAME"]
		except KeyError:
			return None

	def GetGitRepository(self) -> str:
		"""
		Returns the Git repository URL.

		:return:                  Git repository URL.
		:raises ServiceException: If environment variable ``APPVEYOR_PROJECT_SLUG`` was not found.
		:raises ServiceException: If repository URL from ``APPVEYOR_PROJECT_SLUG`` couldn't be parsed.
		"""
		try:
			repositoryURL = environ["APPVEYOR_PROJECT_SLUG"]
		except KeyError as ex:
			raise ServiceException(f"Can't find AppVeyor environment variable 'APPVEYOR_PROJECT_SLUG'.") from ex

		try:
			url = URL.Parse(repositoryURL)
		except ToolingException as ex:
			raise ServiceException(f"Syntax error in repository URL '{repositoryURL}'.") from ex

		return str(url.WithoutCredentials())
