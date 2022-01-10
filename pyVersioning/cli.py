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
# Copyright 2020-2021 Patrick Lehmann - Bötzingen, Germany
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
from typing       import NoReturn

from pyAttributes                    import Attribute
from pyAttributes.ArgParseAttributes import ArgParseMixin, CommandAttribute, ArgumentAttribute, DefaultAttribute
from pyTooling.TerminalUI            import LineTerminal, Severity

from pyVersioning                    import Versioning, Platforms, Project, SelfDescriptive
from pyVersioning.Configuration      import Configuration


class ProjectAttributeGroup(Attribute):
	def __call__(self, func):
		self._AppendAttribute(func, ArgumentAttribute("--project-name",    metavar='<Name>',    dest="ProjectName",    type=str, help="Name of the project."))
		self._AppendAttribute(func, ArgumentAttribute("--project-variant", metavar='<Variant>', dest="ProjectVariant", type=str, help="Variant of the project."))
		self._AppendAttribute(func, ArgumentAttribute("--project-version", metavar='<Version>', dest="ProjectVersion", type=str, help="Version of the project."))
		return func

class CompilerAttributeGroup(Attribute):
	def __call__(self, func):
		self._AppendAttribute(func, ArgumentAttribute("--compiler-name",    metavar='<Name>',    dest="CompilerName",    type=str, help="Used compiler."))
		self._AppendAttribute(func, ArgumentAttribute("--compiler-version", metavar='<Version>', dest="CompilerVersion", type=str, help="Used compiler version."))
		self._AppendAttribute(func, ArgumentAttribute("--compiler-config",  metavar='<Config>',  dest="CompilerConfig",  type=str, help="Used compiler configuration."))
		self._AppendAttribute(func, ArgumentAttribute("--compiler-options", metavar='<Options>', dest="CompilerOptions", type=str, help="Used compiler options."))
		return func


class Application(LineTerminal, ArgParseMixin):
	HeadLine:     str  = "Version file generator."
	__configFile: Path

	def __init__(self, configFile: Path) -> None:
		super().__init__()

		self.__configFile = configFile

		ArgParseMixin.__init__(
			self,
	    description=dedent("Version file generator"),
	    formatter_class=RawDescriptionHelpFormatter,
	    add_help=False
	  )

		self._LOG_MESSAGE_FORMAT__[Severity.Fatal]   = "{DARK_RED}[FATAL] {message}{NOCOLOR}"
		self._LOG_MESSAGE_FORMAT__[Severity.Error]   = "{RED}[ERROR] {message}{NOCOLOR}"
		self._LOG_MESSAGE_FORMAT__[Severity.Warning] = "{YELLOW}[WARNING] {message}{NOCOLOR}"
		self._LOG_MESSAGE_FORMAT__[Severity.Normal]  = "{GRAY}{message}{NOCOLOR}"

	def Initialize(self) -> None:
		if not self.__configFile.exists():
			self.WriteWarning("Configuration file '{file!s}' does not exist.".format(file=self.__configFile))
			self._config = Configuration()
		else:
			self._config = Configuration(self.__configFile)

		self._versioning = Versioning(self)
		self._versioning.loadDataFromConfiguration(self._config)
		self._versioning.collectData()

	def PrintHeadline(self) -> None:
		self.WriteNormal("{HEADLINE}{line}".format(line="=" * 80, **LineTerminal.Foreground))
		self.WriteNormal("{HEADLINE}{headline: ^80s}".format(headline=self.HeadLine, **LineTerminal.Foreground))
		self.WriteNormal("{HEADLINE}{line}".format(line="=" * 80, **LineTerminal.Foreground))

	def Run(self) -> NoReturn:
		ArgParseMixin.Run(self)
		self.exit()

	@DefaultAttribute()
	def HandleDefault(self, args) -> None:
		self.PrintHeadline()
		self.MainParser.print_help()

	@CommandAttribute("help", help="Display help page(s) for the given command name.")
	@ArgumentAttribute(metavar="Command", dest="Command", type=str, nargs="?", help="Print help page(s) for a command.")
	def HandleHelp(self, args) -> None:
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
	@ProjectAttributeGroup()
	@CompilerAttributeGroup()
	@ArgumentAttribute(metavar='<Template file>', dest="Template", type=str, help="Template input filename.")
	@ArgumentAttribute(metavar='<Output file>',   dest="Filename", type=str, help="Output filename.")
	def HandleFillOut(self, args) -> None:
		self.PrintHeadline()
		self.Initialize()

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

		self.UpdateProject(args)
		self.UpdateCompiler(args)

		self._versioning.writeSourceFile(templateFile, outputFile)

	@CommandAttribute("variables", help="Print all available variables.")
	@ProjectAttributeGroup()
	@CompilerAttributeGroup()
	def HandleVariables(self, args) -> None:
		self.PrintHeadline()
		self.Initialize()

		self.UpdateProject(args)
		self.UpdateCompiler(args)

		def print(key, value, indent):
			key = ("  " * indent) + str(key)
			self.WriteNormal("{key:24}: {value!s}".format(key=key, value=value))
			if isinstance(value, SelfDescriptive):
				for k,v in value.KeyValuePairs():
					print(k, v, indent + 1)

		for key,value in self._versioning.variables.items():
			print(key, value, 0)

	@CommandAttribute("json", help="Write all available variables as JSON.")
	@ProjectAttributeGroup()
	@CompilerAttributeGroup()
	@ArgumentAttribute(metavar='<Output file>',   dest="Filename", type=str, nargs="?", help="Output filename.")
	def HandleJSON(self, args) -> None:
		self.Initialize()

		self.UpdateProject(args)
		self.UpdateCompiler(args)

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
		output = content.format(**self._versioning.variables)
		self.WriteNormal(output)


	@CommandAttribute("yaml", help="Write all available variables as YAML.")
	@ProjectAttributeGroup()
	@CompilerAttributeGroup()
	@ArgumentAttribute(metavar='<Output file>',   dest="Filename", type=str, nargs="?", help="Output filename.")
	def HandleYAML(self, args) -> None:
		self.Initialize()

		self.UpdateProject(args)
		self.UpdateCompiler(args)

		yamlEnvironment = "\n"
		# for key, value in self._versioning.variables['env'].as_dict().items():
		# 	yamlEnvironment += f"    {key}: {value}\n".format(key=key, value=value)

		yamlAppVeyor  = "\n#   not found"
		yamlGitHub    = "\n#   not found"
		yamlGitLab    = "\n#   not found"
		yamlTravis    = "\n#   not found"
		if self._versioning.platform is Platforms.AppVeyor:
			yamlAppVeyor = "\n"
			for key, value in self._versioning.variables['appveyor'].as_dict().items():
				yamlAppVeyor += f"    {key}: {value}\n".format(key=key, value=value)
		elif self._versioning.platform is Platforms.GitHub:
			yamlGitHub = "\n"
			for key, value in self._versioning.variables['github'].as_dict().items():
				yamlGitHub += f"    {key}: {value}\n".format(key=key, value=value)
		elif self._versioning.platform is Platforms.GitLab:
			yamlGitLab = "\n"
			for key, value in self._versioning.variables['gitlab'].as_dict().items():
				yamlGitLab += f"    {key}: {value}\n".format(key=key, value=value)
		elif self._versioning.platform is Platforms.Travis:
			yamlTravis = "\n"
			for key, value in self._versioning.variables['travis'].as_dict().items():
				yamlTravis += f"    {key}: {value}\n".format(key=key, value=value)

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
		  appveyor: {yamlAppVeyor}
		  github: {yamlGitHub}
		  gitlab: {yamlGitLab}
		  travis: {yamlTravis}
		  env:{yamlEnvironment}
		""")
		output = content.format(**self._versioning.variables, yamlEnvironment=yamlEnvironment, yamlAppVeyor=yamlAppVeyor, yamlGitHub=yamlGitHub, yamlGitLab=yamlGitLab, yamlTravis=yamlTravis)
		self.WriteNormal(output)

	def UpdateProject(self, args) -> None:
		if 'project' not in self._versioning.variables:
			self._versioning.variables['project'] = Project(args.ProjectName, args.ProjectVersion, args.ProjectVariant)
		elif args.ProjectName is not None:
			self._versioning.variables['project'].name = args.ProjectName

		if args.ProjectVariant is not None:
			self._versioning.variables['project'].variant = args.ProjectVariant

		if args.ProjectVersion is not None:
			self._versioning.variables['project'].version = args.ProjectVersion

	def UpdateCompiler(self, args) -> None:
		if args.CompilerName is not None:
			self._versioning.variables['build'].compiler.name = args.CompilerName
		if args.CompilerVersion is not None:
			self._versioning.variables['build'].compiler.version = args.CompilerVersion
		if args.CompilerConfig is not None:
			self._versioning.variables['build'].compiler.configuration = args.CompilerConfig
		if args.CompilerOptions is not None:
			self._versioning.variables['build'].compiler.options = args.CompilerOptions


def main() -> NoReturn:
	configFile = Path(".pyVersioning.yml")

	Application.versionCheck((3,7,0))
	application = Application(configFile)
	application.Run()


if __name__ == '__main__':
	main()
