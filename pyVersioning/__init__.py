# EMACS settings: -*-  tab-width: 2; indent-tabs-mode: t -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
# =============================================================================
#            __     __            _             _
#  _ __  _   \ \   / /__ _ __ ___(_) ___  _ __ (_)_ __   __ _
# | '_ \| | | \ \ / / _ \ '__/ __| |/ _ \| '_ \| | '_ \ / _` |
# | |_) | |_| |\ V /  __/ |  \__ \ | (_) | | | | | | | | (_| |
# | .__/ \__, | \_/ \___|_|  |___/_|\___/|_| |_|_|_| |_|\__, |
# |_|    |___/                                          |___/
# =============================================================================
# Authors:            Patrick Lehmann
#
# Python package:     pyVersioning Implementation
#
# Description:
# ------------------------------------
#		TODO
#
# License:
# ============================================================================
# Copyright 2020-2020 Patrick Lehmann - Bötzingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============================================================================
#

from argparse import RawDescriptionHelpFormatter
from dataclasses import dataclass
from pathlib  import Path
from textwrap import dedent
from typing   import Dict

from pyAttributes.ArgParseAttributes import ArgParseMixin, DefaultAttribute, CommandAttribute, ArgumentAttribute


@dataclass
class Version():
	flags : int
	major : int
	minor : int
	patch : int

	def __init__(self, major, minor=-1, patch=-1):
		if isinstance(major, str):
			split = major.split(".")
			self.major = int(split[0])
			self.minor = int(split[1])
			self.patch = int(split[2])
		else:
			self.major = major
			self.minor = minor
			self.patch = patch

	def __str__(self):
		return "{0}.{1}.{2}".format(self.major, self.minor, self.patch)


class Versioning(ArgParseMixin):
	HeadLine = "Version file generator."

	def __init__(self):
		super().__init__(
	    description=dedent("Version file generator"),
	    formatter_class=RawDescriptionHelpFormatter,
	    add_help=False
	  )

	def PrintHeadline(self):
		print("{line}".format(line="=" * 80))
		print("{headline: ^80s}".format(headline=self.HeadLine))
		print("{line}".format(line="=" * 80))

	def Run(self):
		ArgParseMixin.Run(self)


	@DefaultAttribute()
	def HandleDefault(self, args):
		self.PrintHeadline()

	@CommandAttribute("help", help="Display help page(s) for the given command name.")
	@ArgumentAttribute(metavar="Command", dest="Command", type=str, nargs="?", help="Print help page(s) for a command.")
	def HandleHelp(self, args):
		self.PrintHeadline()

		if (args.Command is None):
			self.MainParser.print_help()
		elif (args.Command == "help"):
			print("This is a recursion ...")
		else:
			try:
				self.SubParsers[args.Command].print_help()
			except KeyError:
				print("Command {0} is unknown.".format(args.Command))

	@CommandAttribute("ansi-c", help="Create a version file for ANSI-C.")
	@ArgumentAttribute(metavar='<Filename>', dest="Filename", type=str, help="Output filename.")
	def HandleAnsiC(self, args):
		self.PrintHeadline()

		filename = Path(args.Filename)
		variables = self.collectData()
		self.writeCConstant(filename, variables)

	def collectData(self) -> Dict[str, any]:
		variables = {}

		version = self.getVersion()
		variables['flags'] = 0x00
		variables['major'] = version.major
		variables['minor'] = version.minor
		variables['patch'] = version.patch

		return variables

	def getVersion(self) -> Version:
		return Version("0.0.0")

	def writeCConstant(self, filename : Path, variables : Dict[str, any]):
		content = dedent("""\
			#include "version.h"

			const Version version = {
			.version = {
				.flags = 0x{flags:02X},
				.major = 0x{major:02X},
				.minor = 0x{minor:02X},
				.patch = 0x{patch:02X}
			};
			""").format(**variables)

		with filename.open('w') as file:
			file.write(content)


def main():
	versioning = Versioning()
	versioning.Run()


if __name__ == "__main__":
	main()
