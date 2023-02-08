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
"""Unit tests for project information."""
from unittest     import TestCase

from pyTooling.Versioning import SemVersion

from pyVersioning import Project


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class ProjectTests(TestCase):
	def test_ProjectName(self):
		name = "Project 1"
		variant = ""

		project = Project(name)

		self.assertEqual(project.name, name)
		self.assertEqual(project.variant, variant)
		self.assertEqual(project.version, SemVersion("0.0.0"))

	def test_ProjectName_VariantName(self):
		name = "Project 1"
		variant = "Variant 1"

		project = Project(name, variant=variant)

		self.assertEqual(project.name, name)
		self.assertEqual(project.variant, variant)
		self.assertEqual(project.version, SemVersion("0.0.0"))

	def test_ProjectName_VersionAsString(self):
		name = "Project 1"
		variant = ""
		version = "0.1.2"

		project = Project(name, version)

		self.assertEqual(project.name, name)
		self.assertEqual(project.variant, variant)
		self.assertEqual(project.version, SemVersion(version))

	def test_ProjectName_VersionAsVersion(self):
		name = "Project 1"
		variant = ""
		version = SemVersion("1.3.2")

		project = Project(name, version)

		self.assertEqual(project.name, name)
		self.assertEqual(project.variant, variant)
		self.assertIs(project.version, version)
