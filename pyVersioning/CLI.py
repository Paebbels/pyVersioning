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
from argparse import RawDescriptionHelpFormatter, Namespace
from collections import namedtuple
from pathlib      import Path
from textwrap     import dedent
from typing import NoReturn, Callable

from pyTooling.Attributes import Entity
from pyTooling.Decorators                     import export
from pyTooling.Attributes.ArgParse            import ArgParseHelperMixin, DefaultHandler, CommandHandler, CommandGroupAttribute
from pyTooling.Attributes.ArgParse.Argument   import StringArgument, PathArgument
from pyTooling.Attributes.ArgParse.ValuedFlag import LongValuedFlag
from pyTooling.TerminalUI                     import TerminalApplication, Severity

from pyVersioning                             import __version__, __author__, __email__, __copyright__, __license__
from pyVersioning                             import Versioning, Platforms, Project, SelfDescriptive
from pyVersioning.Configuration               import Configuration


@export
class ProjectAttributeGroup(CommandGroupAttribute):
	def __call__(self, func: Entity) -> Entity:
		self._AppendAttribute(func, LongValuedFlag("--project-name",    dest="ProjectName",    metaName="<Name>",    help="Name of the project."))
		self._AppendAttribute(func, LongValuedFlag("--project-variant", dest="ProjectVariant", metaName="<Variant>", help="Variant of the project."))
		self._AppendAttribute(func, LongValuedFlag("--project-version", dest="ProjectVersion", metaName="<Version>", help="Version of the project."))
		return func


@export
class CompilerAttributeGroup(CommandGroupAttribute):
	def __call__(self, func: Entity) -> Entity:
		self._AppendAttribute(func, LongValuedFlag("--compiler-name",    dest="CompilerName",    metaName="<Name>",    help="Used compiler."))
		self._AppendAttribute(func, LongValuedFlag("--compiler-version", dest="CompilerVersion", metaName="<Version>", help="Used compiler version."))
		self._AppendAttribute(func, LongValuedFlag("--compiler-config",  dest="CompilerConfig",  metaName="<Config>",  help="Used compiler configuration."))
		self._AppendAttribute(func, LongValuedFlag("--compiler-options", dest="CompilerOptions", metaName="<Options>", help="Used compiler options."))
		return func


ArgNames = namedtuple("ArgNames", ("Command", "Template", "Filename", "ProjectName", "ProjectVariant", "ProjectVersion", "CompilerName", "CompilerVersion", "CompilerConfig", "CompilerOptions"))


@export
class Application(TerminalApplication, ArgParseHelperMixin):
	HeadLine:     str = "Version file generator."

	__configFile: Path
	_config:      Configuration
	_versioning:  Versioning

	def __init__(self) -> None:
		super().__init__()

		self.HeadLine = "Version file generator."

		ArgParseHelperMixin.__init__(
			self,
			description=self.HeadLine,
			formatter_class=RawDescriptionHelpFormatter,
			add_help=False
		)

		self._LOG_MESSAGE_FORMAT__[Severity.Fatal] =   "{DARK_RED}[FATAL] {message}{NOCOLOR}"
		self._LOG_MESSAGE_FORMAT__[Severity.Error] =   "{RED}[ERROR] {message}{NOCOLOR}"
		self._LOG_MESSAGE_FORMAT__[Severity.Warning] = "{YELLOW}[WARNING] {message}{NOCOLOR}"
		self._LOG_MESSAGE_FORMAT__[Severity.Normal]=   "{GRAY}{message}{NOCOLOR}"

	def Initialize(self) -> None:
		if not self.__configFile.exists():
			self.WriteWarning(f"Configuration file '{self.__configFile}' does not exist.")
			self._config = Configuration()
		else:
			self._config = Configuration(self.__configFile)

		self._versioning = Versioning(self)
		self._versioning.LoadDataFromConfiguration(self._config)
		self._versioning.CollectData()

	def PrintHeadline(self) -> None:
		self.WriteNormal("{HEADLINE}{line}".format(line="=" * 80, **TerminalApplication.Foreground))
		self.WriteNormal("{HEADLINE}{headline: ^80s}".format(headline=self.HeadLine, **TerminalApplication.Foreground))
		self.WriteNormal("{HEADLINE}{line}".format(line="=" * 80, **TerminalApplication.Foreground))

	def Run(self, configFile: Path) -> NoReturn:
		self.__configFile = configFile

		super().Run(self)
		self.Exit()

	@DefaultHandler()
	def HandleDefault(self, args: Namespace) -> None:
		self.PrintHeadline()
		self.MainParser.print_help()

	@CommandHandler("help", help="Display help page(s) for the given command name.")
	@StringArgument(dest="Command", metaName="Command", optional=True, help="Print help page(s) for a command.")
	def HandleHelp(self, args: Namespace) -> None:
		self.PrintHeadline()
		self.WriteNormal(f"Author:    {__author__} ({__email__})")
		self.WriteNormal(f"Copyright: {__copyright__}")
		self.WriteNormal(f"License:   {__license__}")
		self.WriteNormal(f"Version:   {__version__}")
		self.WriteNormal("")

		if args.Command is None:
			self.MainParser.print_help()
		elif args.Command == "help":
			self.WriteError("This is a recursion ...")
		else:
			try:
				self.SubParsers[args.Command].print_help()
			except KeyError:
				self.WriteError(f"Command {args.Command} is unknown.")

	@CommandHandler("fillout", help="Read a template and replace tokens with version information.")
	@ProjectAttributeGroup("dummy")
	@CompilerAttributeGroup("flummy")
	@PathArgument(dest="Template", metaName="<Template file>", help="Template input filename.")
	@PathArgument(dest="Filename", metaName="<Output file>",   help="Output filename.")
	def HandleFillOut(self, args: Namespace) -> None:
		self.Configure(quiet=True)
		self.PrintHeadline()
		self.Initialize()

		templateFile = Path(args.Template)
		if not templateFile.exists():
			self.WriteError(f"Template file '{templateFile}' does not exist.")

		outputFile = Path(args.Filename)
		if not outputFile.parent.exists():
			self.WriteWarning(f"Directory for file '{outputFile}' does not exist. Directory will be created")
			try:
				outputFile.parent.mkdir()
			except:
				self.WriteError(f"Failed to create the directory '{outputFile.parent}' for the output file.")
		elif outputFile.exists():
			self.WriteWarning(f"Output file '{outputFile}' already exists. This file will be overwritten.")

		self.ExitOnPreviousErrors()

		self.UpdateProject(args)
		self.UpdateCompiler(args)

		self._versioning.WriteSourceFile(templateFile, outputFile)

	@CommandHandler("variables", help="Print all available variables.")
	@ProjectAttributeGroup("dummy")
	@CompilerAttributeGroup("flummy")
	def HandleVariables(self, args: Namespace) -> None:
		self.Configure(quiet=True)
		self.PrintHeadline()
		self.Initialize()

		self.UpdateProject(args)
		self.UpdateCompiler(args)

		def print(key, value, indent):
			key = ("  " * indent) + str(key)
			self.WriteNormal(f"{key:24}: {value!s}")
			if isinstance(value, SelfDescriptive):
				for k, v in value.KeyValuePairs():
					print(k, v, indent + 1)

		for key,value in self._versioning.variables.items():
			print(key, value, 0)

	@CommandHandler("json", help="Write all available variables as JSON.")
	@ProjectAttributeGroup("dummy")
	@CompilerAttributeGroup("flummy")
	@PathArgument(dest="Filename", metaName="<Output file>", optional=True, help="Output filename.")
	def HandleJSON(self, args: Namespace) -> None:
		self.Configure(quiet=True)
		self.Initialize()

		self.UpdateProject(args)
		self.UpdateCompiler(args)

		content = dedent("""\
		{{
		  "format": "1.1",
		  "version": {{
		    "name": "{version!s}",
		    "major": {version.Major},
		    "minor": {version.Minor},
		    "patch": {version.Patch},
		   "flags": {version.Flags}
		  }}
		}}
		""")
		output = content.format(**self._versioning.variables)
		self.WriteQuiet(output)

	@CommandHandler("yaml", help="Write all available variables as YAML.")
	@ProjectAttributeGroup("dummy")
	@CompilerAttributeGroup("flummy")
	@PathArgument(dest="Filename", metaName="<Output file>", optional=True, help="Output filename.")
	def HandleYAML(self, args: Namespace) -> None:
		self.Configure(quiet=True)
		self.Initialize()

		self.UpdateProject(args)
		self.UpdateCompiler(args)

		yamlEnvironment = "\n"
		# for key, value in self._versioning.variables["env"].as_dict().items():
		# 	yamlEnvironment += f"    {key}: {value}\n"

		yamlAppVeyor = "\n#   not found"
		yamlGitHub =   "\n#   not found"
		yamlGitLab =   "\n#   not found"
		yamlTravis =   "\n#   not found"
		if self._versioning.platform is Platforms.AppVeyor:
			yamlAppVeyor = "\n"
			for key, value in self._versioning.variables["appveyor"].as_dict().items():
				yamlAppVeyor += f"    {key}: {value}\n"
		elif self._versioning.platform is Platforms.GitHub:
			yamlGitHub = "\n"
			for key, value in self._versioning.variables["github"].as_dict().items():
				yamlGitHub += f"    {key}: {value}\n"
		elif self._versioning.platform is Platforms.GitLab:
			yamlGitLab = "\n"
			for key, value in self._versioning.variables["gitlab"].as_dict().items():
				yamlGitLab += f"    {key}: {value}\n"
		elif self._versioning.platform is Platforms.Travis:
			yamlTravis = "\n"
			for key, value in self._versioning.variables["travis"].as_dict().items():
				yamlTravis += f"    {key}: {value}\n"

		content = dedent("""\
		  format: "1.1"

		  version:
		    name: "{version!s}"
		    major: {version.Major}
		    minor: {version.Minor}
		    patch: {version.Patch}
		    flags: {version.Flags}

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
		self.WriteQuiet(output)

	def UpdateProject(self, args: Namespace) -> None:
		if "project" not in self._versioning.variables:
			self._versioning.variables["project"] = Project(args.ProjectName, args.ProjectVersion, args.ProjectVariant)
		elif args.ProjectName is not None:
			self._versioning.variables["project"]._name = args.ProjectName

		if args.ProjectVariant is not None:
			self._versioning.variables["project"]._variant = args.ProjectVariant

		if args.ProjectVersion is not None:
			self._versioning.variables["project"]._version = args.ProjectVersion

	def UpdateCompiler(self, args: Namespace) -> None:
		if args.CompilerName is not None:
			self._versioning.variables["build"]._compiler._name = args.CompilerName
		if args.CompilerVersion is not None:
			self._versioning.variables["build"]._compiler._version = args.CompilerVersion
		if args.CompilerConfig is not None:
			self._versioning.variables["build"]._compiler._configuration = args.CompilerConfig
		if args.CompilerOptions is not None:
			self._versioning.variables["build"]._compiler._options = args.CompilerOptions


def main() -> NoReturn:
	configFile = Path(".pyVersioning.yml")

	application = Application()
	application.CheckPythonVersion((3, 8, 0))
	application.Run(configFile)


if __name__ == "__main__":
	main()
