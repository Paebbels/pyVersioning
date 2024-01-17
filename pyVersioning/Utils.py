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
from enum       import Enum, auto
from subprocess import run as subprocess_run, PIPE

from pyTooling.Decorators  import export
from pyTooling.MetaClasses import ExtendedType


@export
class GitShowCommand(Enum):
	CommitDateTime =       auto()
	CommitAuthorName =     auto()
	CommitAuthorEmail =    auto()
	CommitCommitterName =  auto()
	CommitCommitterEmail = auto()
	CommitHash =           auto()
	CommitComment =        auto()


@export
class ToolException(Exception):
	command:      str
	errorMessage: str

	def __init__(self, command: str, errorMessage: str) -> None:
		self.command = command
		self.errorMessage = errorMessage


@export
class GitHelper(metaclass=ExtendedType, mixin=True):
	__GIT_SHOW_COMMAND_TO_FORMAT_LOOKUP = {
		GitShowCommand.CommitHash:           "%H",
		GitShowCommand.CommitDateTime:       "%ct",
		GitShowCommand.CommitAuthorName:     "%an",
		GitShowCommand.CommitAuthorEmail:    "%ae",
		GitShowCommand.CommitCommitterName:  "%cn",
		GitShowCommand.CommitCommitterEmail: "%ce",
		GitShowCommand.CommitComment:        "%B",
	}

	def ExecuteGitShow(self, cmd: GitShowCommand, ref: str = "HEAD") -> str:
		format = f"--format='{self.__GIT_SHOW_COMMAND_TO_FORMAT_LOOKUP[cmd]}'"

		command = "git"
		arguments = ("show", "-s", format, ref)
		try:
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except Exception as ex:
			raise ToolException(f"{command} {' '.join(arguments)}", str(ex))

		if completed.returncode == 0:
			comment = completed.stdout.decode("utf-8")
			return comment[1:-2]
		else:
			message = completed.stderr.decode("utf-8")
			raise ToolException(f"{command} {' '.join(arguments)}", message)
