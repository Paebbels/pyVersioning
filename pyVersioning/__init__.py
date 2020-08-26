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
from subprocess   import run as subprocess_run, PIPE
from argparse     import RawDescriptionHelpFormatter
from dataclasses  import dataclass
from datetime     import datetime
from pathlib      import Path
from textwrap     import dedent
from typing       import Dict

from pyAttributes.ArgParseAttributes import ArgParseMixin, DefaultAttribute, CommandAttribute, ArgumentAttribute
from pyTerminalUI import LineTerminal, Severity


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


@dataclass
class Tool():
	name    : str
	version : Version

	def __init__(self, name : str, version : Version):
		self.name    = name
		self.version = version


@dataclass
class Commit():
	hash : str
	date : datetime

	def __init__(self, hash : str, date : datetime):
		self.hash = hash
		self.date = date


@dataclass
class Git():
	commit      : Commit
	reference   : str
	tag         : str
	branch      : str
	repository  : str

	def __init__(self, commit : Commit, tag : str, branch : str, repository : str):
		self.commit     = commit
		self.tag        = tag
		self.branch     = branch
		self.repository = repository

		if tag != "":
			self.reference = tag
		elif branch != "":
			self.reference = branch
		else:
			self.reference = "[Detached HEAD]"


@dataclass
class Project():
	name : str

	def __init__(self, name : str):
		self.name = name


@dataclass
class Compiler():
	name    : str
	version : Version
	options : str

	def __init__(self, name : str, version : Version, options : str):
		self.name    = name
		self.version = version
		self.options = options


@dataclass
class Build():
	date     : datetime
	compiler : Compiler

	def __init__(self, date : datetime, compiler : Compiler):
		self.date     = date
		self.compiler = compiler


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

		self._LOG_MESSAGE_FORMAT__[Severity.Fatal] = "{DARK_RED}[FATAL] {message}{NOCOLOR}"
		self._LOG_MESSAGE_FORMAT__[Severity.Error] = "{RED}[ERROR] {message}{NOCOLOR}",

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
			self.WriteWarning("Directory for file '{file!s}' does not exist. Directory will be created".format(file=outputFile))
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
		variables = self.collectData()
		content = dedent("""\
		  version: {version!s}
		    major: {version.major}
		    minor: {version.minor}
		    patch: {version.patch}
		    flags: {version.flags}
		  git:
		    commit:
		      hash: {git.commit.hash}
		      date: {git.commit.date}
		    reference: {git.reference}
		    branch: {git.branch}
		    tag: {git.tag}
		    repository: {git.repository}
		  project:
		    name: {project.name}
		  build:
		    date: {build.date}
		    compiler:
		      name: {build.compiler.name}
		      version: {build.compiler.version}
		      options: {build.compiler.options}
		""")
		output = content.format(**variables)
		self.WriteNormal(output)

	def collectData(self) -> Dict[str, any]:
		variables = {}

		variables['tool'] =     Tool("pyVersioning", Version(0,2,6)),
		variables['version'] =  self.getVersion()
		variables['git'] =      self.getGitInformation()
		variables['project'] =  self.getProject()
		variables['build'] =    self.getBuild()

		return variables

	def getVersion(self) -> Version:
		return Version("0.0.0")

	def getGitInformation(self):
		return Git(
			commit=self.getLastCommit(),
			tag=self.getGitTag(),
			branch=self.getGitBranch(),
			repository=self.getGitRepository()
		)

	def getLastCommit(self):
		return Commit(
			hash=self.getGitHash(),
			date=self.getCommitDate()
		)

	def getGitHash(self):
		try:
			completed = subprocess_run("git rev-parse HEAD", stdout=PIPE, stderr=PIPE)
		except:
			return "0" * 40
		if completed.returncode == 0:
			return completed.stdout.decode('utf-8')[0:40]
		else:
			message = completed.stderr.decode('utf-8')
			self.WriteFatal("Message from 'git': {message}".format(message=message))

	def getCommitDate(self):
		try:
			completed = subprocess_run("git show -s --format=%ct HEAD", stdout=PIPE, stderr=PIPE)
		except:
			return None
		if completed.returncode == 0:
			ts = int(completed.stdout.decode('utf-8'))
			return datetime.fromtimestamp(ts)
		else:
			message = completed.stderr.decode('utf-8')
			self.WriteFatal("Message from 'git': {message}".format(message=message))

	def getGitBranch(self):
		try:
			completed = subprocess_run("git branch --show-current", stdout=PIPE, stderr=PIPE)
		except:
			return ""
		if completed.returncode == 0:
			return completed.stdout.decode('utf-8')
		else:
			message = completed.stderr.decode('utf-8')
			self.WriteFatal("Message from 'git': {message}".format(message=message))

	def getGitTag(self):
		return "not implemented"

	def getGitRepository(self):
		return "not implemented"

	def getProject(self):
		return Project(
			"not implemented"
		)

	def getBuild(self):
		return Build(
			date=datetime.now(),
			compiler=self.getCompiler()
		)

	def getCompiler(self):
		return Compiler(
			name="not implemeneted",
			version=Version(0,0,0),
			options=""
		)

	def writeSourceFile(self, template : Path, filename : Path, variables : Dict[str, any]):
		with template.open('r') as file:
			content = template.read_text()

		# apply variables
		content = content.format(**variables)

		with filename.open('w') as file:
			file.write(content)
