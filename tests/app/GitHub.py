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
"""Unit tests for GitLab CI."""
from os               import environ as os_environ
from subprocess       import run as subprocess_run, PIPE as subprocess_PIPE, STDOUT as subprocess_STDOUT, CalledProcessError

from pyTooling.Common import CurrentPlatform

from unittest         import TestCase


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class GitHubEnvironment(TestCase):
	@staticmethod
	def __getExecutable(command: str, *args):
		callArgs = [
			"pyVersioning",
			command
		]

		if len(args) > 0:
			callArgs.extend(args)

		return callArgs

	def test_NoCommand(self):
		print()

		callArgs = ["pyVersioning"]

		try:
			prog = subprocess_run(
				args=callArgs,
				stdout=subprocess_PIPE,
				stderr=subprocess_STDOUT,
				check=True,
				encoding="utf-8"
			)
		except CalledProcessError as ex:
			print("CALLED PROCESS ERROR")
			print(ex.returncode)
			print(ex.output)
			exit(1)
		except Exception as ex:
			print("EXCEPTION")
			print(ex)
			exit(3)

		output = prog.stdout
		for line in output.split("\n"):
			print(line)

	def test_HelpCommand(self):
		print()

		callArgs = self.__getExecutable("help")

		try:
			prog = subprocess_run(
				args=callArgs,
				stdout=subprocess_PIPE,
				stderr=subprocess_STDOUT,
				check=True,
				encoding="utf-8"
			)
		except CalledProcessError as ex:
			print("CALLED PROCESS ERROR")
			print(ex.returncode)
			print(ex.output)
			exit(1)
		except Exception as ex:
			print("EXCEPTION")
			print(ex)
			exit(3)

		output = prog.stdout
		for line in output.split("\n"):
			print(line)

	def test_VariablesCommand(self):
		print()

		callArgs = self.__getExecutable("variables")
		print(callArgs)

		try:
			prog = subprocess_run(
				args=callArgs,
				stdout=subprocess_PIPE,
				stderr=subprocess_STDOUT,
				check=True,
				encoding="utf-8"
			)
		except CalledProcessError as ex:
			print("CALLED PROCESS ERROR")
			print(ex.returncode)
			print(ex.output)
			exit(1)
		except Exception as ex:
			print("EXCEPTION")
			print(ex)
			exit(3)

		output = prog.stdout
		for line in output.split("\n"):
			print(line)

	def test_YAMLCommand(self):
		print()

		callArgs = self.__getExecutable("yaml")
		print(callArgs)

		try:
			prog = subprocess_run(
				args=callArgs,
				stdout=subprocess_PIPE,
				stderr=subprocess_STDOUT,
				check=True,
				encoding="utf-8"
			)
		except CalledProcessError as ex:
			print("CALLED PROCESS ERROR")
			print(ex.returncode)
			print(ex.output)
			exit(1)
		except Exception as ex:
			print("EXCEPTION")
			print(ex)
			exit(3)

		output = prog.stdout
		for line in output.split("\n"):
			print(line)

	def test_JSONCommand(self):
		print()

		callArgs = self.__getExecutable("json")
		print(callArgs)

		try:
			prog = subprocess_run(
				args=callArgs,
				stdout=subprocess_PIPE,
				stderr=subprocess_STDOUT,
				check=True,
				encoding="utf-8"
			)
		except CalledProcessError as ex:
			print("CALLED PROCESS ERROR")
			print(ex.returncode)
			print(ex.output)
			exit(1)
		except Exception as ex:
			print("EXCEPTION")
			print(ex)
			exit(3)

		output = prog.stdout
		for line in output.split("\n"):
			print(line)

	def test_Fillout(self):
		print()

		callArgs = self.__getExecutable("fillout", "template.in", "template.out")
		print(callArgs)

		try:
			prog = subprocess_run(
				args=callArgs,
				stdout=subprocess_PIPE,
				stderr=subprocess_STDOUT,
				check=True,
				encoding="utf-8"
			)
		except CalledProcessError as ex:
			print("CALLED PROCESS ERROR")
			print(ex.returncode)
			print(ex.output)
			exit(1)
		except Exception as ex:
			print("EXCEPTION")
			print(ex)
			exit(3)

		output = prog.stdout
		for line in output.split("\n"):
			print(line)
