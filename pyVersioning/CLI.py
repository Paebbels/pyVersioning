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
from argparse    import RawDescriptionHelpFormatter, Namespace
from collections import namedtuple
from pathlib     import Path
from textwrap    import dedent
from typing      import NoReturn, Optional as Nullable

from pyTooling.Attributes                     import Entity
from pyTooling.Decorators                     import export
from pyTooling.Attributes.ArgParse            import ArgParseHelperMixin, DefaultHandler, CommandHandler, CommandGroupAttribute
from pyTooling.Attributes.ArgParse.Argument   import StringArgument, PathArgument
from pyTooling.Attributes.ArgParse.Flag       import FlagArgument
from pyTooling.Attributes.ArgParse.ValuedFlag import LongValuedFlag
from pyTooling.TerminalUI                     import TerminalApplication, Severity, Mode

from pyVersioning                             import __version__, __author__, __email__, __copyright__, __license__
from pyVersioning                             import Versioning, Platforms, Project, SelfDescriptive
from pyVersioning.Configuration               import Configuration


@export
class ProjectAttributeGroup(CommandGroupAttribute):
	"""
	This attribute group applies the following ArgParse attributes:

	* ``--project-name``
	* ``--project-variant``
	* ``--project-version``
	"""
	def __call__(self, func: Entity) -> Entity:
		self._AppendAttribute(func, LongValuedFlag("--project-name",    dest="ProjectName",    metaName="<Name>",    optional=True, help="Name of the project."))
		self._AppendAttribute(func, LongValuedFlag("--project-variant", dest="ProjectVariant", metaName="<Variant>", optional=True, help="Variant of the project."))
		self._AppendAttribute(func, LongValuedFlag("--project-version", dest="ProjectVersion", metaName="<Version>", optional=True, help="Version of the project."))
		return func


@export
class CompilerAttributeGroup(CommandGroupAttribute):
	"""
	This attribute group applies the following ArgParse attributes:

	* ``--compiler-name``
	* ``--compiler-version``
	* ``--compiler-config``
	* ``--compiler-options``
	"""
	def __call__(self, func: Entity) -> Entity:
		self._AppendAttribute(func, LongValuedFlag("--compiler-name",    dest="CompilerName",    metaName="<Name>",    optional=True, help="Used compiler."))
		self._AppendAttribute(func, LongValuedFlag("--compiler-version", dest="CompilerVersion", metaName="<Version>", optional=True, help="Used compiler version."))
		self._AppendAttribute(func, LongValuedFlag("--compiler-config",  dest="CompilerConfig",  metaName="<Config>",  optional=True, help="Used compiler configuration."))
		self._AppendAttribute(func, LongValuedFlag("--compiler-options", dest="CompilerOptions", metaName="<Options>", optional=True, help="Used compiler options."))
		return func


ArgNames = namedtuple("ArgNames", ("Command", "Template", "Filename", "ProjectName", "ProjectVariant", "ProjectVersion", "CompilerName", "CompilerVersion", "CompilerConfig", "CompilerOptions"))


@export
class Application(TerminalApplication, ArgParseHelperMixin):
	"""
	pyVersioning's command line interface application class.
	"""
	HeadLine:     str = "Version file generator."

	__configFile: Path
	_config:      Nullable[Configuration]
	_versioning:  Nullable[Versioning]

	def __init__(self) -> None:
		super().__init__(Mode.TextToStdOut_ErrorsToStdErr)

		self.HeadLine = "Version file generator."

		self.__configFile = Path(".pyVersioning.yml")
		self._config = None
		self._versioning = None

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

	def Initialize(self, configFile: Nullable[Path] = None) -> None:
		if configFile is None:
			if not self.__configFile.exists():
				self.WriteWarning(f"Configuration file '{self.__configFile}' does not exist.")
				self._config = Configuration()
			else:
				self.WriteVerbose(f"Reading configuration file '{self.__configFile}'")
				self._config = Configuration(self.__configFile)
		elif configFile.exists():
			self.WriteVerbose(f"Reading configuration file '{configFile}'")
			self._config = Configuration(configFile)
		else:
			self.WriteError(f"Configuration file '{configFile}' does not exist.")
			self._config = Configuration()

		self.WriteVerbose(f"Creating internal data model ...")
		self._versioning = Versioning(self)
		self.WriteDebug(f"  Loading information from configuration file ...")
		self._versioning.LoadDataFromConfiguration(self._config)
		self.WriteDebug(f"  Collecting information from environment ...")
		self._versioning.CollectData()

	def Run(self) -> NoReturn:
		super().Run()  # todo: enableAutoComplete ??
		self.Exit()

	def _PrintHeadline(self) -> None:
		"""Helper method to print the program headline."""
		self.WriteNormal("{HEADLINE}{line}".format(line="=" * 80, **TerminalApplication.Foreground))
		self.WriteNormal("{HEADLINE}{headline: ^80s}".format(headline=self.HeadLine, **TerminalApplication.Foreground))
		self.WriteNormal("{HEADLINE}{line}".format(line="=" * 80, **TerminalApplication.Foreground))

	def _PrintVersion(self) -> None:
		"""Helper method to print the version information."""
		self.WriteNormal(f"Author:    {__author__} ({__email__})")
		self.WriteNormal(f"Copyright: {__copyright__}")
		self.WriteNormal(f"License:   {__license__}")
		self.WriteNormal(f"Version:   {__version__}")

	@DefaultHandler()
	@FlagArgument(short="-v", long="--verbose", dest="Verbose", help="Print verbose messages.")
	@FlagArgument(short="-d", long="--debug", dest="Debug", help="Print debug messages.")
	@LongValuedFlag("--config-file", dest="ConfigFile", metaName="<pyVersioning.yaml>", optional=True, help="Path to pyVersioning.yaml .")
	def HandleDefault(self, args: Namespace) -> None:
		"""Handle program calls for no given command."""
		self.Configure(verbose=args.Verbose, debug=args.Debug)
		self._PrintHeadline()
		self._PrintVersion()
		self.WriteNormal("")
		self.MainParser.print_help(self._stdout)

	@CommandHandler("help", help="Display help page(s) for the given command name.")
	@StringArgument(dest="Command", metaName="Command", optional=True, help="Print help page(s) for a command.")
	def HandleHelp(self, args: Namespace) -> None:
		"""Handle program calls for command ``help``."""
		self.Configure(verbose=args.Verbose, debug=args.Debug)
		self._PrintHeadline()
		self._PrintVersion()
		self.WriteNormal("")

		if args.Command is None:
			self.MainParser.print_help(self._stdout)
		elif args.Command == "help":
			self.WriteError("This is a recursion ...")
		else:
			try:
				self.SubParsers[args.Command].print_help(self._stdout)
			except KeyError:
				self.WriteError(f"Command {args.Command} is unknown.")

	@CommandHandler("version", help="Display version information.", description="Display version information.")
	def HandleVersion(self, args: Namespace) -> None:
		"""Handle program calls for command ``version``."""
		self.Configure(verbose=args.Verbose, debug=args.Debug)
		self._PrintHeadline()
		self._PrintVersion()

	@CommandHandler("variables", help="Print all available variables.")
	@ProjectAttributeGroup("dummy")
	@CompilerAttributeGroup("flummy")
	def HandleVariables(self, args: Namespace) -> None:
		"""Handle program calls for command ``variables``."""
		self.Configure(verbose=args.Verbose, debug=args.Debug, quiet=True)
		self._PrintHeadline()
		self.Initialize(Path(args.ConfigFile) if args.ConfigFile is not None else None)

		self.UpdateProject(args)
		self.UpdateCompiler(args)

		def _print(key, value, indent):
			key = ("  " * indent) + str(key)
			self.WriteQuiet(f"{key:24}: {value!s}")
			if isinstance(value, SelfDescriptive):
				for k, v in value.KeyValuePairs():
					_print(k, v, indent + 1)

		for key,value in self._versioning.Variables.items():
			_print(key, value, 0)

	@CommandHandler("field", help="Return a single pyVersioning field.")
	@ProjectAttributeGroup("dummy")
	@CompilerAttributeGroup("flummy")
	@StringArgument(dest="Field", metaName="<Field name>", help="Field to return.")
	@PathArgument(dest="Filename", metaName="<Output file>", optional=True, help="Output filename.")
	def HandleField(self, args: Namespace) -> None:
		"""Handle program calls for command ``field``."""
		self.Configure(verbose=args.Verbose, debug=args.Debug)  #, quiet=args.Filename is None)
		self._PrintHeadline()
		self.Initialize(None if args.ConfigFile is None else Path(args.ConfigFile))

		query = f"{{{args.Field}}}"

		content = self.FillOutTemplate(query)

		self.WriteOutput(
			None if args.Filename is None else Path(args.Filename),
			content
		)

	@CommandHandler("fillout", help="Read a template and replace tokens with version information.")
	@ProjectAttributeGroup("dummy")
	@CompilerAttributeGroup("flummy")
	@PathArgument(dest="Template", metaName="<Template file>", help="Template input filename.")
	@PathArgument(dest="Filename", metaName="<Output file>",   optional=True, help="Output filename.")
	def HandleFillOut(self, args: Namespace) -> None:
		"""Handle program calls for command ``fillout``."""
		self.Configure(verbose=args.Verbose, debug=args.Debug, quiet=args.Filename is None)
		self._PrintHeadline()
		self.Initialize(None if args.ConfigFile is None else Path(args.ConfigFile))

		templateFile = Path(args.Template)
		if not templateFile.exists():
			self.WriteError(f"Template file '{templateFile}' does not exist.")

		template = templateFile.read_text(encoding="utf-8")

		self.UpdateProject(args)
		self.UpdateCompiler(args)

		content = self.FillOutTemplate(template)

		self.WriteOutput(
			None if args.Filename is None else Path(args.Filename),
			content
		)

	@CommandHandler("json", help="Write all available variables as JSON.")
	@ProjectAttributeGroup("dummy")
	@CompilerAttributeGroup("flummy")
	@PathArgument(dest="Filename", metaName="<Output file>", optional=True, help="Output filename.")
	def HandleJSON(self, args: Namespace) -> None:
		"""Handle program calls for command ``json``."""
		self.Configure(verbose=args.Verbose, debug=args.Debug, quiet=args.Filename is None)
		self.Initialize(Path(args.ConfigFile) if args.ConfigFile is not None else None)

		self.UpdateProject(args)
		self.UpdateCompiler(args)

		template = dedent("""\
		{{
		  "format": "1.1",
		  "version": {{
		    "name": "{version!s}",
		    "major": {version.Major},
		    "minor": {version.Minor},
		    "patch": {version.Patch},
		    "flags": {version.Flags.value}
		  }}
		}}
		""")

		content = self._versioning.FillOutTemplate(template)

		self.WriteOutput(
			None if args.Filename is None else Path(args.Filename),
			content
		)

	@CommandHandler("yaml", help="Write all available variables as YAML.")
	@ProjectAttributeGroup("dummy")
	@CompilerAttributeGroup("flummy")
	@PathArgument(dest="Filename", metaName="<Output file>", optional=True, help="Output filename.")
	def HandleYAML(self, args: Namespace) -> None:
		"""Handle program calls for command ``yaml``."""
		self.Configure(verbose=args.Verbose, debug=args.Debug, quiet=args.Filename is None)
		self.Initialize(Path(args.ConfigFile) if args.ConfigFile is not None else None)

		self.UpdateProject(args)
		self.UpdateCompiler(args)

		yamlEnvironment = "\n"
		# for key, value in self._versioning.variables["env"].as_dict().items():
		# 	yamlEnvironment += f"    {key}: {value}\n"

		yamlAppVeyor = "\n#   not found"
		yamlGitHub =   "\n#   not found"
		yamlGitLab =   "\n#   not found"
		yamlTravis =   "\n#   not found"
		if self._versioning.Platform is Platforms.AppVeyor:
			yamlAppVeyor = "\n"
			for key, value in self._versioning.Variables["appveyor"].as_dict().items():
				yamlAppVeyor += f"    {key}: {value}\n"
		elif self._versioning.Platform is Platforms.GitHub:
			yamlGitHub = "\n"
			for key, value in self._versioning.Variables["github"].as_dict().items():
				yamlGitHub += f"    {key}: {value}\n"
		elif self._versioning.Platform is Platforms.GitLab:
			yamlGitLab = "\n"
			for key, value in self._versioning.Variables["gitlab"].as_dict().items():
				yamlGitLab += f"    {key}: {value}\n"
		elif self._versioning.Platform is Platforms.Travis:
			yamlTravis = "\n"
			for key, value in self._versioning.Variables["travis"].as_dict().items():
				yamlTravis += f"    {key}: {value}\n"

		template = dedent("""\
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

		content = self.FillOutTemplate(
			template,
			yamlEnvironment=yamlEnvironment,
			yamlAppVeyor=yamlAppVeyor,
			yamlGitHub=yamlGitHub,
			yamlGitLab=yamlGitLab,
			yamlTravis=yamlTravis
		)

		self.WriteOutput(
			None if args.Filename is None else Path(args.Filename),
			content
		)

	def UpdateProject(self, args: Namespace) -> None:
		if "project" not in self._versioning.Variables:
			self._versioning.Variables["project"] = Project(args.ProjectName, args.ProjectVersion, args.ProjectVariant)
		elif args.ProjectName is not None:
			self._versioning.Variables["project"]._name = args.ProjectName

		if args.ProjectVariant is not None:
			self._versioning.Variables["project"]._variant = args.ProjectVariant

		if args.ProjectVersion is not None:
			self._versioning.Variables["project"]._version = args.ProjectVersion

	def UpdateCompiler(self, args: Namespace) -> None:
		if args.CompilerName is not None:
			self._versioning.Variables["build"]._compiler._name = args.CompilerName
		if args.CompilerVersion is not None:
			self._versioning.Variables["build"]._compiler._version = args.CompilerVersion
		if args.CompilerConfig is not None:
			self._versioning.Variables["build"]._compiler._configuration = args.CompilerConfig
		if args.CompilerOptions is not None:
			self._versioning.Variables["build"]._compiler._options = args.CompilerOptions

	def FillOutTemplate(self, template: str, **kwargs) -> str:
		self.WriteVerbose(f"Applying variables to template ...")
		return self._versioning.FillOutTemplate(template, **kwargs)

	def WriteOutput(self, outputFile: Nullable[Path], content: str):
		if outputFile is not None:
			self.WriteVerbose(f"Writing output to '{outputFile}' ...")
			if not outputFile.parent.exists():
				self.WriteWarning(f"Directory for file '{outputFile}' does not exist. Directory will be created")
				try:
					outputFile.parent.mkdir()
				except:
					self.WriteError(f"Failed to create the directory '{outputFile.parent}' for the output file.")
			elif outputFile.exists():
				self.WriteWarning(f"Output file '{outputFile}' already exists. This file will be overwritten.")

			self.ExitOnPreviousErrors()

			outputFile.write_text(content, encoding="utf-8")
		else:
			self.WriteToStdOut(content)


def main() -> NoReturn:
	"""Entrypoint for program execution."""
	application = Application()
	application.CheckPythonVersion((3, 8, 0))
	try:
		application.Run()
	# except ServiceException as ex:
	# 	application.PrintException(ex)
	except Exception as ex:
		application.PrintException(ex)


if __name__ == "__main__":
	main()
