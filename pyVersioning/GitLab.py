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
"""GitLab specific code to collect the build environment."""
from datetime import datetime
from os       import environ
from typing   import Optional as Nullable

from pyTooling.Decorators   import export

from pyVersioning.CIService import CIService, Platform, ServiceException


@export
class GitLab(CIService):
	"""Collect Git and other platform and environment information from environment variables provided by GitLab-CI."""

	ENV_INCLUDE_FILTER = ("CI_", "GITLAB_")
	ENV_EXCLUDE_FILTER = ("_TOKEN", )
	ENV_INCLUDES =       ('CI', )
	ENV_EXCLUDES =       ('CI_JOB_TOKEN', )

	def GetPlatform(self) -> Platform:
		return Platform("gitlab")

	def GetGitHash(self) -> str:
		try:
			return environ['CI_COMMIT_SHA']
		except KeyError as ex:
			raise ServiceException from ex

	def GetCommitDate(self) -> datetime:
		try:
			iso8601 = environ['CI_COMMIT_TIMESTAMP']
			return datetime.strptime(iso8601, "%Y-%m-%dT%H:%M:%S%z")
		except KeyError as ex:
			raise ServiceException from ex

	def GetGitBranch(self) -> Nullable[str]:
		try:
			return environ['CI_COMMIT_BRANCH']
		except KeyError:
			return None

	def GetGitTag(self) -> Nullable[str]:
		try:
			return environ['CI_COMMIT_TAG']
		except KeyError:
			return None

	def GetGitRepository(self) -> str:
		try:
			return environ['CI_REPOSITORY_URL']
		except KeyError as ex:
			raise ServiceException from ex
