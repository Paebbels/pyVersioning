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
"""Unit tests for pyVersioning application."""
from io                   import StringIO
from json                 import loads as json_loads
from pathlib              import Path
from re                   import compile as re_compile
from unittest             import TestCase
from unittest.mock        import patch

from ruamel.yaml          import YAML

from pyVersioning.CLI     import Application as pyV_Application


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unittest <testcase module>'")
	exit(1)


class Application(TestCase):
	@patch("sys.argv", ["pyVersioning.py", "json"])
	def test_JSON(self):
		print()

		configFile = Path("CIServices/.pyVersioning.yml")

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run(configFile)
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		out.seek(0)
		err.seek(0)

		# WORKAROUND: removing color codes
		ansiEscape = re_compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
		jsonContent = ansiEscape.sub("", out.read())
		print("-" * 40)
		print(jsonContent)
		print("-" * 40)
		json = json_loads(jsonContent)

		self.assertEqual("1.1", json["format"])

	@patch("sys.argv", ["pyVersioning.py", "yaml"])
	def test_YAML(self):
		print()

		configFile = Path("CIServices/.pyVersioning.yml")

		app = pyV_Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run(configFile)
		except SystemExit as ex:
			self.assertEqual(0, ex.code)

		out.seek(0)
		err.seek(0)

		# WORKAROUND: removing color codes
		ansiEscape = re_compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
		yamlContent = ansiEscape.sub("", out.read())
		yamlParser = YAML()
		yaml = yamlParser.load(yamlContent)

		self.assertEqual("1.1", yaml["format"])
