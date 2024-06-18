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
from subprocess         import run as subprocess_run, PIPE as subprocess_PIPE, STDOUT as subprocess_STDOUT, CalledProcessError
from typing             import Any, Optional as Nullable, Tuple, List, Dict
from unittest           import TestCase as ut_TestCase

from pyTooling.Platform import CurrentPlatform


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unittest <testcase module>'")
	exit(1)


class TestCase(ut_TestCase):
	@classmethod
	def _getServiceEnvironment(cls, **kwargs: Any) -> Dict[str, str]:
		raise NotImplementedError()

	@classmethod
	def _getExecutable(cls, command: Nullable[str] = None, *args: Any) -> List[str]:
		if CurrentPlatform.IsNativeWindows:
			callArgs = ["py", f"-{CurrentPlatform.PythonVersion.Major}.{CurrentPlatform.PythonVersion.Minor}"]
		else:
			callArgs = [f"python{CurrentPlatform.PythonVersion.Major}.{CurrentPlatform.PythonVersion.Minor}"]

		callArgs.append("pyVersioning/CLI.py")
		if command is not None:
			callArgs.append(command)

		if len(args) > 0:
			callArgs.extend(args)

		return callArgs

	@classmethod
	def _run(self, command: Nullable[str] = None, *args: Any) -> Tuple[str, str]:
		try:
			prog = subprocess_run(
				args=self._getExecutable(command, *args),
				stdout=subprocess_PIPE,
				stderr=subprocess_STDOUT,
				shell=True,
				env=self._getServiceEnvironment(),
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
