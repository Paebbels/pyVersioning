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
"""Module for CI service base classes."""
from dataclasses  import make_dataclass
from datetime     import datetime
from os           import environ
from typing       import Dict, Optional as Nullable

from pyTooling.Decorators import export
from pyTooling.MetaClasses import ExtendedType, abstractmethod

from pyVersioning import SelfDescriptive, GitHelper, GitShowCommand


@export
class ServiceException(Exception):
	""".. todo:: ServiceException needs documentation"""


@export
class Platform(SelfDescriptive):
	""".. todo:: Platform needs documentation"""

	_ciService: str

	_public = ['ci_service']

	def __init__(self, ciService: str):
		self._ciService = ciService

	@property
	def ci_service(self) -> str:
		return self._ciService


@export
class BaseService(metaclass=ExtendedType):
	"""Base-class to collect platform and environment information from e.g. environment variables."""

	@abstractmethod
	def getPlatform(self) -> Platform:
		""".. todo:: getPlatform needs documentation"""


@export
class CIService(BaseService, GitHelper):
	"""Base-class to collect Git and other platform and environment information from CI service environment variables."""

	ENV_INCLUDE_FILTER = ()
	ENV_EXCLUDE_FILTER = ()
	ENV_INCLUDES =       []
	ENV_EXCLUDES =       []

	def getEnvironment(self) -> Dict[str, str]:
		""".. todo:: getEnvironment needs documentation"""

		filteredEnv = {key:value for (key,value) in environ.items() if key.startswith(self.ENV_INCLUDE_FILTER) and not key.endswith(self.ENV_EXCLUDE_FILTER)}

		# manually add some variables
		for key in self.ENV_INCLUDES:
			try:
				filteredEnv[key] = environ[key]
			except KeyError:
				pass

		# manually delete some variables
		for key in self.ENV_EXCLUDES:
			try:
				del filteredEnv[key]
			except KeyError:
				pass

		def func(s):
			for e in filteredEnv.keys():
				yield (e, s.__getattribute__(e))

		Environment = make_dataclass(
			"Environment",
			[(name, str) for name in filteredEnv.keys()],
			bases=(SelfDescriptive,),
			namespace={
				'as_dict':       lambda self: filteredEnv,
				'Keys':          lambda self: filteredEnv.keys(),
				'KeyValuePairs': lambda self: func(self)
			},
			repr=True
		)

		return Environment(**filteredEnv)

	@abstractmethod
	def getGitHash(self) -> str:
		""".. todo:: getGithash needs documentation"""

	# @abstractmethod
	def getCommitDate(self) -> datetime:
		""".. todo:: getCommitDate needs documentation"""

		datetimeString = self.execGitShow(GitShowCommand.CommitDateTime, self.getGitHash())
		return datetime.fromtimestamp(int(datetimeString))

	@abstractmethod
	def getGitBranch(self) -> Nullable[str]:
		""".. todo:: getGitBranch needs documentation"""

	@abstractmethod
	def getGitTag(self) -> Nullable[str]:
		""".. todo:: getGitTag needs documentation"""

	@abstractmethod
	def getGitRepository(self) -> str:
		""".. todo:: getGitRepository needs documentation"""


@export
class WorkStation(BaseService):
	def getPlatform(self) -> Platform:
		return Platform("NO-CI")
