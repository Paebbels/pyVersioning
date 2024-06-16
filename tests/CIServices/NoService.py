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
from json               import loads, JSONDecodeError
from os                 import environ as os_environ
from pathlib            import Path
from re                 import compile as re_compile
from typing             import Any

from ruamel.yaml        import YAML
from ruamel.yaml.reader import ReaderError

from . import TestCase


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unittest <testcase module>'")
	exit(1)


class LocalEnvironment(TestCase):
	@classmethod
	def _getServiceEnvironment(cls, **kwargs: Any):
		env = {k: v for k, v in os_environ.items()}

		if len(kwargs) == 0:
			env["GITLAB_CI"] =          "YES"
			env["CI_COMMIT_SHA"] =      "1234567890123456789012345678901234567890"
			env["CI_COMMIT_BRANCH"] =   "dev"
			env["CI_REPOSITORY_URL"] =  "gitlab.com/path/to/repo.git"
		else:
			for k, v in kwargs.items():
				env[k] = v

		return env

	def test_NoArguments(self):
		print()

		stdout, stderr = self._run()

	def test_Help(self) -> None:
		print()

		stdout, stderr = self._run("help")

	def test_Variables(self) -> None:
		print()

		stdout, stderr = self._run("variables")

	def test_Fillout_WithoutOutputFile(self) -> None:
		print()

		stdout, stderr = self._run("fillout", "tests/template.in")

	def test_Fillout_WithOutputFile(self) -> None:
		print()

		stdout, stderr = self._run("fillout", "tests/template.in", "tests/template.out")


	def test_Json_WithoutOutputFile(self) -> None:
		print()

		stdout, stderr = self._run("json")

		try:
			# WORKAROUND: removing color codes
			ansiEscape = re_compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
			jsonContent = ansiEscape.sub("", stdout)
			json = loads(jsonContent)
		except JSONDecodeError as ex:
			print("=" * 80)
			print(ex)
			print("=" * 80)
			self.fail("Internal JSON error: JSONDecodeError")

	def test_Json_WithOutputFile(self) -> None:
		print()

		outputFile = Path("tests/template.json")
		stdout, stderr = self._run("json", outputFile.as_posix())

		try:
			json = loads(outputFile.read_text())
		except JSONDecodeError as ex:
			print("=" * 80)
			print(ex)
			print("=" * 80)
			self.fail("Internal JSON error: JSONDecodeError")

	def test_Yaml_WithoutOutputFile(self) -> None:
		print()

		yaml = YAML()

		stdout, stderr = self._run("yaml")

		try:
			# WORKAROUND: removing color codes
			ansiEscape = re_compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
			yamlContent = ansiEscape.sub("", stdout)
			yaml.load(yamlContent)
		except ReaderError as ex:
			print("=" * 80)
			print(ex)
			print("=" * 80)
			self.fail("Internal YAML error: ReaderError")

	def test_Yaml_WithOutputFile(self) -> None:
		print()

		outputFile = Path("tests/template.yaml")

		stdout, stderr = self._run("yaml", outputFile.as_posix())

		yaml = YAML()
		try:
			yaml.load(outputFile.read_text())
		except ReaderError as ex:
			print("=" * 80)
			print(ex)
			print("=" * 80)
			self.fail("Internal YAML error: ReaderError")
