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
# Copyright 2020-2025 Patrick Lehmann - Bötzingen, Germany                                                             #
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
from datetime import datetime
from os       import environ as os_environ
from typing   import Any, Dict

from .        import TestCase


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unittest <testcase module>'")
	exit(1)


class GitLabEnvironment(TestCase):
	@classmethod
	def _getServiceEnvironment(cls, **kwargs: Any) -> Dict[str, str]:
		env: Dict[str, str] = {k: v for k, v in os_environ.items()}

		if len(kwargs) == 0:
			env["GITLAB_CI"] =          "YES"
			env["CI_COMMIT_SHA"] =      "1234567890123456789012345678901234567890"
			env["CI_COMMIT_BRANCH"] =   "dev"
			env["CI_COMMIT_TIMESTAMP"] = datetime.now().astimezone().isoformat()
			env["CI_REPOSITORY_URL"] =  "gitlab.com/path/to/repo.git"
		else:
			env.update(kwargs)

		return env

	def test_Variables(self) -> None:
		print()

		stdout, stderr = self._run("variables")

	def test_Fillout(self) -> None:
		print()

		stdout, stderr = self._run("-d", "--config-file=tests/unit/CIServices/.pyVersioning.yml", "fillout", "tests/template.in", "tests/template.out")
