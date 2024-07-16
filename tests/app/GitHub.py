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
"""Unit tests for GitLab CI."""
from subprocess       import run as subprocess_run, PIPE as subprocess_PIPE, STDOUT as subprocess_STDOUT, CalledProcessError
from typing           import Any, Optional as Nullable

from unittest         import TestCase


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unittest <testcase module>'")
	exit(1)


class GitHubEnvironment(TestCase):
	@classmethod
	def _run(cls, command: Nullable[str] = None, *args: Any):
		callArgs = ["pyVersioning"]
		if command is not None:
			callArgs.append(command)
		if len(args) > 0:
			callArgs.extend(args)

		try:
			prog = subprocess_run(
				args=callArgs,
				stdout=subprocess_PIPE,
				stderr=subprocess_STDOUT,
				check=True,
				encoding="utf-8"
			)
		except CalledProcessError as ex:
			print("-- CALLED PROCESS ERROR " + "-" * 56)
			print(f"Return code: {ex.returncode}")
			print(ex.output)
			print("-" * 80)
			raise Exception(f"Error when executing the process: {ex}") from ex
		except Exception as ex:
			print("-- EXCEPTION " + "-" * 67)
			print(ex)
			raise Exception(f"Unknown error: {ex}") from ex

		stdout = prog.stdout
		stderr = prog.stderr

		print("-- STDOUT " + "-" * 70)
		for line in stdout.split("\n"):
			print(line)
		if stderr is not None:
			print("-- STDERR " + "-" * 70)
			for line in stderr.split("\n"):
				print(line)
		print("-" * 80)

		return stdout, stderr

	def test_NoCommand(self) -> None:
		print()

		stdout, stderr = self._run()

	def test_HelpCommand(self) -> None:
		print()

		stdout, stderr = self._run("help")

	def test_VariablesCommand(self) -> None:
		print()

		stdout, stderr = self._run("variables")

	def test_YAMLCommand(self) -> None:
		print()

		stdout, stderr = self._run("yaml")

	def test_JSONCommand(self) -> None:
		print()

		stdout, stderr = self._run("json")

	def test_Fillout(self) -> None:
		print()

		stdout, stderr = self._run("fillout", "tests/template.in", "tests/template.out")
