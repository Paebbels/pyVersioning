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
from argparse     import RawDescriptionHelpFormatter
from dataclasses  import dataclass
from datetime     import datetime
from pathlib      import Path
from textwrap     import dedent
from typing       import Dict

from pyAttributes.ArgParseAttributes import ArgParseMixin, DefaultAttribute, CommandAttribute, ArgumentAttribute
from pyTerminalUI                    import LineTerminal


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
			self.flags = 0
		else:
			self.major = major
			self.minor = minor
			self.patch = patch
			self.flags = 0

	def __str__(self):
		return "v{0}.{1}.{2}".format(self.major, self.minor, self.patch)

	def __repr__(self):
		return "{0}.{1}.{2}".format(self.major, self.minor, self.patch)


class Versioning(LineTerminal, ArgParseMixin):
	HeadLine = "Version file generator."

	def __init__(self):
		super().__init__()

		ArgParseMixin.__init__(
			self,
	    description=dedent("Version file generator"),
	    formatter_class=RawDescriptionHelpFormatter,
	    add_help=False
	  )

	def PrintHeadline(self):
		self.WriteNormal("{HEADLINE}{line}".format(line="=" * 80, **LineTerminal.Foreground))
		self.WriteNormal("{HEADLINE}{headline: ^80s}".format(headline=self.HeadLine, **LineTerminal.Foreground))
		self.WriteNormal("{HEADLINE}{line}".format(line="=" * 80, **LineTerminal.Foreground))

	def Run(self):
		ArgParseMixin.Run(self)

	@DefaultAttribute()
	def HandleDefault(self, args):
		self.PrintHeadline()
		self.MainParser.print_help()

	@CommandAttribute("help", help="Display help page(s) for the given command name.")
	@ArgumentAttribute(metavar="Command", dest="Command", type=str, nargs="?", help="Print help page(s) for a command.")
	def HandleHelp(self, args):
		self.PrintHeadline()

		if (args.Command is None):
			self.MainParser.print_help()
		elif (args.Command == "help"):
			self.WriteError("This is a recursion ...")
		else:
			try:
				self.SubParsers[args.Command].print_help()
			except KeyError:
				self.WriteError("Command {0} is unknown.".format(args.Command))

	@CommandAttribute("fillout", help="Read a template and replace tokens with version information.")
	@ArgumentAttribute(metavar='<Template file>', dest="Template", type=str, help="Template input filename.")
	@ArgumentAttribute(metavar='<Output file>',   dest="Filename", type=str, help="Output filename.")
	def HandleFillOut(self, args):
		self.PrintHeadline()

		templateFile = Path(args.Template)
		if not templateFile.exists():
			self.WriteError("Template file '{file!s}' does not exist.".format(file=templateFile))

		outputFile = Path(args.Filename)
		if not outputFile.parent.exists():
			self.WriteWarning("Directoy for file '{file!s}' does not exist. Directory will be created".format(file=outputFile))
			try:
				outputFile.parent.mkdir()
			except:
				self.WriteError("Failed to create the directory '{dir}' for the output file.".format(dir=outputFile.parent))
		elif outputFile.exists():
			self.WriteWarning("Output file '{file!s}' already exists. This file will be overwritten.".format(file=outputFile))

		self.ExitOnPreviousErrors()

		variables = self.collectData()
		self.writeSourceFile(templateFile, outputFile, variables)

	@CommandAttribute("variables", help="Print all available variables.")
	def HandleVariables(self, args):
		self.PrintHeadline()

		variables = self.collectData()
		for key,value in variables.items():
			self.WriteNormal("{key:24}: {value}".format(key=key, value=value))

	@CommandAttribute("json", help="Write all available variables as JSON.")
	@ArgumentAttribute(metavar='<Output file>',   dest="Filename", type=str, nargs="?", help="Output filename.")
	def HandleJSON(self, args):
		self.PrintHeadline()

		variables = self.collectData()
		content = dedent("""\
		{{
			version: {{
				major: {version.major},
		    minor: {version.minor},
		    patch: {version.patch},
		    flags: {version.flags}
			}}
		}}
		""")
		output = content.format(**variables)
		self.WriteNormal(output)

	@CommandAttribute("yaml", help="Write all available variables as YAML.")
	@ArgumentAttribute(metavar='<Output file>',   dest="Filename", type=str, nargs="?", help="Output filename.")
	def HandleYAML(self, args):
		self.PrintHeadline()

		variables = self.collectData()
		content = dedent("""\
		  version:
		    major: {version.major}
		    minor: {version.minor}
		    patch: {version.patch}
		    flags: {version.flags}
		""")
		output = content.format(**variables)
		self.WriteNormal(output)

	def collectData(self) -> Dict[str, any]:
		variables = {}

		variables['tool_name'] =    "pyVersioning"
		variables['tool_version'] = "v0.2.4"

		version = self.getVersion()
		variables['version'] = version
		variables['version_flags'] = 0x00
		variables['version_major'] = version.major
		variables['version_minor'] = version.minor
		variables['version_patch'] = version.patch

		gitCommitDate = self.getCommitDate()
		variables['git_commit_hash'] =    self.getGitHash()
		variables['git_commit_date'] =    gitCommitDate
		variables['git_commit_year'] =    gitCommitDate.year
		variables['git_commit_month'] =   gitCommitDate.month
		variables['git_commit_day'] =     gitCommitDate.day
		variables['git_commit_hour'] =    gitCommitDate.hour
		variables['git_commit_minute'] =  gitCommitDate.minute
		variables['git_commit_second'] =  gitCommitDate.second

		variables['git_reference'] =      self.getGitReference()
		variables['git_repository'] =     self.getGitRepository()

		buildDate = datetime.now()
		variables['build_date_year'] =    buildDate.year
		variables['build_date_month'] =   buildDate.month
		variables['build_date_day'] =     buildDate.day
		variables['build_date_hour'] =    buildDate.hour
		variables['build_date_minute'] =  buildDate.minute
		variables['build_date_second'] =  buildDate.second

		variables['build_compiler'] =     self.getCompiler()

		return variables

	def getVersion(self) -> Version:
		return Version("0.0.0")

	def getGitHash(self):
		return "0123456789012345678901234567890123456789"

	def getCommitDate(self):
		return datetime.now()

	def getGitReference(self):
		return "undefined"

	def getGitRepository(self):
		return "undefined"

	def getCompiler(self):
		return "undefined"

	def writeSourceFile(self, template : Path, filename : Path, variables : Dict[str, any]):
		with template.open('r') as file:
			content = template.read_text()

		# apply variables
		content = content.format(**variables)

		with filename.open('w') as file:
			file.write(content)
