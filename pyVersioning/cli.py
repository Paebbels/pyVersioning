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
from pathlib      import Path
from textwrap     import dedent

from pyAttributes.ArgParseAttributes import ArgParseMixin, CommandAttribute, ArgumentAttribute, DefaultAttribute
from pyTerminalUI import LineTerminal, Severity

from pyVersioning import Versioning, Platforms


class Application(Versioning, LineTerminal, ArgParseMixin):
	HeadLine = "Version file generator."

	def __init__(self):
		super().__init__()
		LineTerminal.__init__(self)
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

		self.collectData()
		self.writeSourceFile(templateFile, outputFile)

	@CommandAttribute("variables", help="Print all available variables.")
	def HandleVariables(self, args):
		self.PrintHeadline()

		self.collectData()
		for key,value in self.variables.items():
			self.WriteNormal("{key:24}: {value}".format(key=key, value=value))

	@CommandAttribute("json", help="Write all available variables as JSON.")
	@ArgumentAttribute(metavar='<Output file>',   dest="Filename", type=str, nargs="?", help="Output filename.")
	def HandleJSON(self, args):
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
		output = content.format(**self.variables)
		self.WriteNormal(output)


	@CommandAttribute("yaml", help="Write all available variables as YAML.")
	@ArgumentAttribute(metavar='<Output file>',   dest="Filename", type=str, nargs="?", help="Output filename.")
	def HandleYAML(self, args):
		env = "\n"
		for key, value in self.variables['env'].as_dict().items():
			env += f"    {key}: {value}\n".format(key=key, value=value)

		appVeyor  = "\n#   not found"
		github    = "\n#   not found"
		gitlab    = "\n#   not found"
		travis    = "\n#   not found"
		if self.platform is Platforms.AppVeyor:
			appVeyor = "\n"
			for key, value in self.variables['appveyor'].as_dict().items():
				env += f"    {key}: {value}\n".format(key=key, value=value)
		elif self.platform is Platforms.GitHub:
			github = "\n"
			for key, value in self.variables['github'].as_dict().items():
				env += f"    {key}: {value}\n".format(key=key, value=value)
		elif self.platform is Platforms.GitLab:
			gitlab = "\n"
			for key, value in self.variables['gitlab'].as_dict().items():
				env += f"    {key}: {value}\n".format(key=key, value=value)
		elif self.platform is Platforms.Travis:
			travis = "\n"
			for key, value in self.variables['travis'].as_dict().items():
				env += f"    {key}: {value}\n".format(key=key, value=value)

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
		    variant: {project.variant}

		  build:
		    date: {build.date}
		    compiler:
		      name: {build.compiler.name}
		      version: {build.compiler.version}
		      configuration: {build.compiler.configuration}
		      options: {build.compiler.options}

		  platform:
		    ci-service: {platform.ci_service}
		  appveyor: {appveyor}
		  github: {github}
		  gitlab: {gitlab}
		  travis: {travis}
		  env:{environment}
		""")
		output = content.format(**self.variables, environment=env, appveyor=appVeyor, github=github, gitlab=gitlab, travis=travis)
		self.WriteNormal(output)


def main():
	Application.versionCheck((3,7,0))
	application = Application()
	application.Run()
	application.exit()


if __name__ == '__main__':
	main()
