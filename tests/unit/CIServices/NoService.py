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
# Copyright 2020-2026 Patrick Lehmann - Bötzingen, Germany                                                             #
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
from typing import Any, Dict

from pyTooling.Platform import CurrentPlatform, Platforms
from pytest             import mark
from ruamel.yaml        import YAML
from ruamel.yaml.reader import ReaderError

from . import TestCase


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unittest <testcase module>'")
	exit(1)


class LocalEnvironment(TestCase):
	@classmethod
	def _getServiceEnvironment(cls, **kwargs: Any) -> Dict[str, str]:
		env: Dict[str, str] = {k: v for k, v in os_environ.items()}

		# Remove GitHub variables
		if "GITHUB_ACTIONS" in env:
			env = {k: v for k, v in env.items() if not k.startswith("GITHUB_")}

		# Remove GitLab variables
		if "GITLAB_CI" in env:
			env = {k: v for k, v in env.items() if not k.startswith("CI_")}

		env.update(kwargs)

		return env

	@mark.skipif(Platforms.OS_Windows in CurrentPlatform._platform, reason="Skipped, if current platform is on Windows.")
	def test_NoArguments(self) -> None:
		print()

		stdout, stderr = self._run()

	@mark.skipif(Platforms.OS_Windows in CurrentPlatform._platform, reason="Skipped, if current platform is on Windows.")
	def test_Help(self) -> None:
		print()

		stdout, stderr = self._run("help")

	@mark.skipif(Platforms.OS_Windows in CurrentPlatform._platform, reason="Skipped, if current platform is on Windows.")
	def test_Variables(self) -> None:
		print()

		stdout, stderr = self._run("variables")

	@mark.skipif(Platforms.OS_Windows in CurrentPlatform._platform, reason="Skipped, if current platform is on Windows.")
	def test_Field_Version(self) -> None:
		print()

		stdout, stderr = self._run("field", "-d", "version")

	@mark.skipif(Platforms.OS_Windows in CurrentPlatform._platform, reason="Skipped, if current platform is on Windows.")
	def test_Field_GitCommitHash(self) -> None:
		print()

		stdout, stderr = self._run("field", "git.commit.hash")

	@mark.skipif(Platforms.OS_Windows in CurrentPlatform._platform, reason="Skipped, if current platform is on Windows.")
	def test_Fillout_WithoutOutputFile(self) -> None:
		print()

		stdout, stderr = self._run("fillout", "tests/template.in")

	@mark.skipif(Platforms.OS_Windows in CurrentPlatform._platform, reason="Skipped, if current platform is on Windows.")
	def test_Fillout_WithOutputFile(self) -> None:
		print()

		stdout, stderr = self._run("fillout", "tests/template.in", "tests/template.out")

	@mark.skip
	def test_Json_WithoutOutputFile(self) -> None:
		print()

		stdout, stderr = self._run("json")

		try:
			# WORKAROUND: removing color codes
			ansiEscape = re_compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
			jsonContent = ansiEscape.sub("", stdout)
			json = loads(jsonContent)
		except JSONDecodeError as ex:
			print( "JSON: JSONDecodeError")
			print(f"  {ex}")
			self.fail("Internal JSON error: JSONDecodeError")

	@mark.skip
	def test_Json_WithOutputFile(self) -> None:
		print()

		outputFile = Path("tests/template.json")
		stdout, stderr = self._run("-d", "json", outputFile.as_posix())

		try:
			json = loads(outputFile.read_text())
		except JSONDecodeError as ex:
			print( "JSON: JSONDecodeError")
			print(f"  {ex}")
			self.fail("Internal JSON error: JSONDecodeError")
		except FileNotFoundError as ex:
			print( "OS: FileNotFoundError")
			print(f"  {ex}")
			print(f"  cwd: {Path.cwd()}")
			print( "  tests/")
			for item in (Path.cwd() / 'tests').glob("*.*"):
				print(f"    {item}")
			self.fail("Unittest error: FileNotFoundError")

	@mark.skipif(Platforms.OS_Windows in CurrentPlatform._platform, reason="Skipped, if current platform is on Windows.")
	def test_Yaml_WithoutOutputFile(self) -> None:
		print()

		stdout, stderr = self._run("yaml")

		yaml = YAML()
		try:
			# WORKAROUND: removing color codes
			ansiEscape = re_compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
			yamlContent = ansiEscape.sub("", stdout)
			yaml.load(yamlContent)
		except ReaderError as ex:
			print( "YAML: ReaderError")
			print(f"  {ex}")
			self.fail("Internal YAML error: ReaderError")

	@mark.skip
	def test_Yaml_WithOutputFile(self) -> None:
		print()

		outputFile = Path("tests/template.yaml")

		stdout, stderr = self._run("-d", "yaml", outputFile.as_posix())

		yaml = YAML()
		try:
			yaml.load(outputFile.read_text())
		except ReaderError as ex:
			print( "YAML: ReaderError")
			print(f"  {ex}")
			self.fail("Internal YAML error: ReaderError")
		except FileNotFoundError as ex:
			print( "OS: FileNotFoundError")
			print(f"  {ex}")
			print(f"  cwd: {Path.cwd()}")
			print( "  tests/")
			for item in (Path.cwd() / 'tests').glob("*.*"):
				print(f"    {item}")
			self.fail("Unittest error: FileNotFoundError")
