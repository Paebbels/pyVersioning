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
"""Unit tests for pyVersioning application using mocking."""
from io                   import StringIO
from json                 import loads as json_loads
from re                   import compile as re_compile
from typing               import Tuple
from unittest             import TestCase
from unittest.mock        import patch

from ruamel.yaml          import YAML

from pyVersioning.CLI     import Application as pyV_Application


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unittest <testcase module>'")
	exit(1)


class Application(TestCase):
	@staticmethod
	def _PrintToStdOutAndStdErr(out: StringIO, err: StringIO, stdoutEnd: str = "") -> Tuple[str, str]:
		out.seek(0)
		err.seek(0)

		stdout = out.read()
		stderr = err.read()

		print("-- STDOUT " + "-" * 70)
		print(stdout, end=stdoutEnd)
		if len(stderr) > 0:
			print("-- STDERR " + "-" * 70)
			print(stderr, end="")
		print("-" * 80)

		return stdout, stderr

	@staticmethod
	def _RemoveColorCodes(content: str) -> str:
		# WORKAROUND: removing color codes
		ansiEscape = re_compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
		return ansiEscape.sub("", content)

	@patch("sys.argv", ["pyVersioning.py"])
	def test_NoCommand(self):
		print()

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		# self.assertEqual("1.1", json["format"])

	@patch("sys.argv", ["pyVersioning.py", "help"])
	def test_Help(self):
		print()

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		# self.assertEqual("1.1", json["format"])

	@patch("sys.argv", ["pyVersioning.py", "version"])
	def test_Version(self):
		print()

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		# self.assertEqual("1.1", json["format"])

	@patch("sys.argv", ["pyVersioning.py", "variables"])
	def test_Variables(self):
		print()

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		# self.assertEqual("1.1", json["format"])

	@patch("sys.argv", ["pyVersioning.py", "field", "version"])
	def test_Field_Version(self):
		print()

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err, "\n")

		# self.assertEqual("1.1", json["format"])

	@patch("sys.argv", ["pyVersioning.py", "field", "git.commit.hash"])
	def test_Field_GitCommitHash(self):
		print()

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err, "\n")

		# self.assertEqual("1.1", json["format"])

	@patch("sys.argv", ["pyVersioning.py", "fillout", "tests/template.in"])
	def test_Fillout(self):
		print()

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		# self.assertEqual("1.1", json["format"])

	@patch("sys.argv", ["pyVersioning.py", "--config-file=tests/unit/CIServices/.pyVersioning.yml", "json"])
	def test_JSON_WithoutError(self):
		print()

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)
		jsonContent = self._RemoveColorCodes(stdout)

		json = json_loads(jsonContent)

		self.assertEqual("1.1", json["format"])

	@patch("sys.argv", ["pyVersioning.py", "--config-file=CIServices/.pyVersioning.yml", "json"])
	def test_JSON_WithError(self):
		print()

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)
		jsonContent = self._RemoveColorCodes(stdout)

		json = json_loads(jsonContent)

		self.assertEqual("1.1", json["format"])

	@patch("sys.argv", ["pyVersioning.py", "--config-file=tests/unit/CIServices/.pyVersioning.yml", "yaml"])
	def test_YAML_WithoutError(self):
		print()

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)
		yamlContent = self._RemoveColorCodes(stdout)

		yamlParser = YAML()
		yaml = yamlParser.load(yamlContent)

		self.assertEqual("1.1", yaml["format"])

	@patch("sys.argv", ["pyVersioning.py", "--config-file=CIServices/.pyVersioning.yml", "yaml"])
	def test_YAML_WithError(self):
		print()

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)
		yamlContent = self._RemoveColorCodes(stdout)

		yamlParser = YAML()
		yaml = yamlParser.load(yamlContent)

		self.assertEqual("1.1", yaml["format"])
