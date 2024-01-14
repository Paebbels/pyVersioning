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
__author__ =    "Patrick Lehmann"
__email__ =     "Paebbels@gmail.com"
__copyright__ = "2020-2024, Patrick Lehmann"
__license__ =   "Apache License, Version 2.0"
__version__ =   "0.13.0"
__keywords__ =  ["Python3", "Template", "Versioning", "Git"]

from dataclasses  import make_dataclass
from datetime     import date, time, datetime
from enum         import Enum, auto
from os           import environ
from pathlib      import Path
from subprocess   import run as subprocess_run, PIPE, CalledProcessError
from typing       import Union, Any, Dict, Tuple, ClassVar, Generator, Optional as Nullable

from pyTooling.Decorators       import export, readonly
from pyTooling.MetaClasses      import ExtendedType
from pyTooling.Versioning       import SemanticVersion
from pyTooling.TerminalUI       import ILineTerminal

from pyVersioning.Utils         import GitHelper, GitShowCommand
from pyVersioning.Configuration import Configuration


@export
class SelfDescriptive(metaclass=ExtendedType, slots=True, mixin=True):

	# TODO: could this be filled with a decorator?
	_public: ClassVar[Tuple[str, ...]]

	def Keys(self) -> Generator[str, None, None]:
		for element in self._public:
			yield element

	def KeyValuePairs(self) -> Generator[Tuple[str, Any], None, None]:
		for element in self._public:
			value = self.__getattribute__(element)
			yield (element, value)


@export
class Tool(SelfDescriptive):
	"""This data structure class describes the tool name and version of pyVersioning."""

	_name:    str
	_version: SemanticVersion

	_public:  ClassVar[Tuple[str, ...]] = ("name", "version")

	def __init__(self, name: str, version: SemanticVersion) -> None:
		self._name = name
		self._version = version

	@readonly
	def name(self) -> str:
		return self._name

	@readonly
	def version(self) -> SemanticVersion:
		return self._version

	def __str__(self) -> str:
		return f"{self._name} {self._version}"


@export
class Date(date, SelfDescriptive):
	_public: ClassVar[Tuple[str, ...]] = ("day", "month", "year")


@export
class Time(time, SelfDescriptive):
	_public: ClassVar[Tuple[str, ...]] = ("hour", "minute", "second")


@export
class Person(SelfDescriptive):
	"""This data structure class describes an author with name and email address."""

	_name:  str
	_email: str

	_public: ClassVar[Tuple[str, ...]] = ("name", "email")

	def __init__(self, name: str, email: str) -> None:
		self._name = name
		self._email = email

	@readonly
	def name(self) -> str:
		return self._name

	@readonly
	def email(self) -> str:
		return self._email

	def __str__(self) -> str:
		return f"{self._name} <{self._email}>"


@export
class Commit(SelfDescriptive):
	_hash:      str
	_date:      date
	_time:      time
	_author:    Person
	_committer: Person
	_comment:   str
	_oneline:   Union[str,  bool] = False

	_public: ClassVar[Tuple[str, ...]] = ("hash", "date", "time", "author", "committer", "comment", "oneline")

	def __init__(self, hash: str, date: date, time: time, author: Person, committer: Person, comment: str) -> None:
		self._hash = hash
		self._date = date
		self._time = time
		self._author = author
		self._committer = committer
		self._comment = comment

		if comment != "":
			self._oneline = comment.split("\n")[0]

	@readonly
	def hash(self) -> str:
		return self._hash

	@readonly
	def date(self) -> date:
		return self._date

	@readonly
	def time(self) -> time:
		return self._time

	@readonly
	def author(self) -> Person:
		return self._author

	@readonly
	def committer(self) -> Person:
		return self._committer

	@readonly
	def comment(self) -> str:
		return self._comment

	@readonly
	def oneline(self) -> Union[str,  bool]:
		return self._oneline


@export
class Git(SelfDescriptive):
	_commit:     Commit
	_reference:  str = ""
	_tag:        str = ""
	_branch:     str = ""
	_repository: str = ""

	_public: ClassVar[Tuple[str, ...]] = ("commit", "reference", "tag", "branch", "repository")

	def __init__(self, commit: Commit, repository: str, tag: str = "", branch: str = "") -> None:
		self._commit = commit
		self._tag = tag
		self._branch = branch
		self._repository = repository

		if tag != "":
			self._reference = tag
		elif branch != "":
			self._reference = branch
		else:
			self._reference = "[Detached HEAD]"

	@readonly
	def commit(self) -> Commit:
		return self._commit

	@readonly
	def reference(self) -> str:
		return self._reference

	@readonly
	def tag(self) -> str:
		return self._tag

	@readonly
	def branch(self) -> str:
		return self._branch

	@readonly
	def repository(self) -> str:
		return self._repository


@export
class Project(SelfDescriptive):
	_name:     str
	_variant:  str
	_version:  SemanticVersion

	_public: ClassVar[Tuple[str, ...]] = ("name", "variant", "version")

	def __init__(self, name: str, version: Union[str, SemanticVersion, None] = None, variant: Nullable[str] = None) -> None:
		"""Assign fields and convert version string to a `Version` object."""

		self._name    = name    if name    is not None else ""
		self._variant = variant if variant is not None else ""

		if isinstance(version, SemanticVersion):
			self._version = version
		elif isinstance(version, str):
			self._version = SemanticVersion(version)
		elif version is None:
			self._version = SemanticVersion("v0.0.0")

	@readonly
	def name(self) -> str:
		return self._name

	@readonly
	def variant(self) -> str:
		return self._variant

	@readonly
	def version(self) -> SemanticVersion:
		return self._version

	def __str__(self) -> str:
		return f"{self._name} - {self._variant} {self._version}"


@export
class Compiler(SelfDescriptive):
	_name:          str
	_version:       SemanticVersion
	_configuration: str
	_options:       str

	_public: ClassVar[Tuple[str, ...]] = ("name", "version", "configuration", "options")

	def __init__(self, name: str, version: Union[str, SemanticVersion] = "", configuration: str = "", options: str = "") -> None:
		"""Assign fields and convert version string to a `Version` object."""

		self._name          = name          if name          is not None else ""
		self._configuration = configuration if configuration is not None else ""
		self._options       = options       if options       is not None else ""

		if isinstance(version, SemanticVersion):
			self._version = version
		elif isinstance(version, str):
			self._version = SemanticVersion(version)
		elif version is None:
			self._version = SemanticVersion("v0.0.0")

	@readonly
	def name(self) -> str:
		return self._name

	@readonly
	def version(self) -> SemanticVersion:
		return self._version

	@readonly
	def configuration(self) -> str:
		return self._configuration

	@readonly
	def options(self) -> str:
		return self._options


@export
class Build(SelfDescriptive):
	_date:     date
	_time:     time
	_compiler: Compiler

	_public: ClassVar[Tuple[str, ...]] = ("date", "time", "compiler")

	def __init__(self, date: date, time: time, compiler: Compiler) -> None:
		self._date = date
		self._time = time
		self._compiler = compiler

	@readonly
	def date(self) -> date:
		return self._date

	@readonly
	def time(self) -> time:
		return self._time

	@readonly
	def compiler(self) -> Compiler:
		return self._compiler


@export
class Platforms(Enum):
	Workstation = auto()
	AppVeyor =    auto()
	GitHub =      auto()
	GitLab =      auto()
	Travis =      auto()


@export
class Platform(SelfDescriptive):
	""".. todo:: Platform needs documentation"""

	_ciService: str
	_public:  ClassVar[Tuple[str, ...]] = ('ci_service', )

	def __init__(self, ciService: str) -> None:
		self._ciService = ciService

	@readonly
	def ci_service(self) -> str:
		return self._ciService


@export
class BaseService(metaclass=ExtendedType):
	"""Base-class to collect platform and environment information from e.g. environment variables."""

	# @abstractmethod
	def GetPlatform(self) -> Platform:  # type: ignore[empty-body]
		""".. todo:: getPlatform needs documentation"""


@export
class Versioning(ILineTerminal, GitHelper):
	_variables: Dict[str, Any]
	_platform:  Platforms = Platforms.Workstation
	_service:   BaseService

	def __init__(self, terminal: ILineTerminal) -> None:
		super().__init__(terminal)

		self._variables = {}

		if "APPVEYOR" in environ:
			self._platform = Platforms.AppVeyor
		elif "GITHUB_ACTIONS" in environ:
			self._platform = Platforms.GitHub
		elif "GITLAB_CI" in environ:
			self._platform = Platforms.GitLab
		elif "TRAVIS" in environ:
			self._platform = Platforms.Travis
		else:
			self._platform = Platforms.Workstation

	@readonly
	def variables(self) -> Dict[str, Any]:
		return self._variables

	@readonly
	def platform(self) -> Platforms:
		return self._platform

	def LoadDataFromConfiguration(self, config: Configuration) -> None:
		"""Preload versioning information from configuration file."""

		self._variables["project"] = self.GetProject(config.project)
		self._variables["build"]   = self.GetBuild(config.build)
		self._variables["version"] = self.GetVersion(config.project)

	def CollectData(self) -> None:
		"""Collect versioning information from environment including CI services (if available)."""

		from pyVersioning.AppVeyor      import AppVeyor
		from pyVersioning.CIService     import WorkStation
		from pyVersioning.GitLab        import GitLab
		from pyVersioning.GitHub        import GitHub
		from pyVersioning.Travis        import Travis

		if self._platform is Platforms.AppVeyor:
			self._service                = AppVeyor()
			self._variables["appveyor"]  = self._service.GetEnvironment()
		elif self._platform is Platforms.GitHub:
			self._service                = GitHub()
			self._variables["github"]    = self._service.GetEnvironment()
		elif self._platform is Platforms.GitLab:
			self._service                = GitLab()
			self._variables["gitlab"]    = self._service.GetEnvironment()
		elif self._platform is Platforms.Travis:
			self._service                = Travis()
			self._variables["travis"]    = self._service.GetEnvironment()
		else:
			self._service                = WorkStation()

		self._variables["tool"]     = Tool("pyVersioning", SemanticVersion(__version__))
		self._variables["git"]      = self.GetGitInformation()
		self._variables["env"]      = self.GetEnvironment()
		self._variables["platform"] = self._service.GetPlatform()

		self.CalculateData()

	def CalculateData(self) -> None:
		if self._variables["git"].tag != "":
			pass

	def GetVersion(self, config: Configuration.Project) -> SemanticVersion:
		if config.version is not None:
			return config.version
		else:
			return SemanticVersion("0.0.0")

	def GetGitInformation(self) -> Git:
		return Git(
			commit=self.GetLastCommit(),
			tag=self.GetGitTag(),
			branch=self.GetGitLocalBranch(),
			repository=self.GetGitRemoteURL()
		)

	def GetLastCommit(self) -> Commit:
		dt = self.GetCommitDate()

		return Commit(
			hash=self.GetGitHash(),
			date=dt.date(),
			time=dt.time(),
			author=self.GetCommitAuthor(),
			committer=self.GetCommitCommitter(),
			comment=self.GetCommitComment()
		)

	def GetGitHash(self) -> str:
		if self._platform is not Platforms.Workstation:
			return self._service.GetGitHash()

		return self.ExecuteGitShow(GitShowCommand.CommitHash)

	def GetCommitDate(self) -> datetime:
		if self._platform is not Platforms.Workstation:
			return self._service.GetCommitDate()

		datetimeString = self.ExecuteGitShow(GitShowCommand.CommitDateTime)
		return datetime.fromtimestamp(int(datetimeString))

	def GetCommitAuthor(self) -> Person:
		return Person(
			name=self.GetCommitAuthorName(),
			email=self.GetCommitAuthorEmail()
		)

	def GetCommitAuthorName(self) -> str:
		return self.ExecuteGitShow(GitShowCommand.CommitAuthorName)

	def GetCommitAuthorEmail(self) -> str:
		return self.ExecuteGitShow(GitShowCommand.CommitAuthorEmail)

	def GetCommitCommitter(self) -> Person:
		return Person(
			name=self.GetCommitCommitterName(),
			email=self.GetCommitCommitterEmail()
		)

	def GetCommitCommitterName(self) -> str:
		return self.ExecuteGitShow(GitShowCommand.CommitCommitterName)

	def GetCommitCommitterEmail(self) -> str:
		return self.ExecuteGitShow(GitShowCommand.CommitCommitterEmail)

	def GetCommitComment(self) -> str:
		return self.ExecuteGitShow(GitShowCommand.CommitComment)

	def GetGitLocalBranch(self) -> str:
		if self._platform is not Platforms.Workstation:
			return self._service.GetGitBranch()

		command = "git"
		arguments = ("branch", "--show-current")
		try:
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except CalledProcessError:
			return ""

		if completed.returncode == 0:
			return completed.stdout.decode("utf-8").split("\n")[0]
		else:
			message = completed.stderr.decode("utf-8")
			self.WriteFatal(f"Message from '{command}': {message}")

	def GetGitRemoteBranch(self, localBranch: Nullable[str] = None) -> str:
		if self._platform is not Platforms.Workstation:
			return self._service.GetGitBranch()

		if localBranch is None:
			localBranch = self.GetGitLocalBranch()

		command = "git"
		arguments = ("config", f"branch.{localBranch}.merge")
		try:
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except CalledProcessError:
			raise Exception()  # XXX: needs error message

		if completed.returncode == 0:
			return completed.stdout.decode("utf-8").split("\n")[0]
		else:
			message = completed.stderr.decode("utf-8")
			self.WriteFatal(f"Message from '{command}': {message}")
			raise Exception()  # XXX: needs error message

	def GetGitRemote(self, localBranch: Nullable[str] = None) -> str:
		if localBranch is None:
			localBranch = self.GetGitLocalBranch()

		command = "git"
		arguments = ("config", f"branch.{localBranch}.remote")
		try:
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except CalledProcessError:
			raise Exception()  # XXX: needs error message

		if completed.returncode == 0:
			return completed.stdout.decode("utf-8").split("\n")[0]
		elif completed.returncode == 1:
			self.WriteWarning(f"Branch '{localBranch}' is not pushed to a remote.")
			return f"(local) {localBranch}"
		else:
			message = completed.stderr.decode("utf-8")
			self.WriteFatal(f"Message from '{command}': {message}")
			raise Exception()  # XXX: needs error message

	def GetGitTag(self) -> str:
		if self._platform is not Platforms.Workstation:
			return self._service.GetGitTag()

		command = "git"
		arguments = ("tag", "--points-at", "HEAD")
		try:
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except CalledProcessError:
			raise Exception()  # XXX: needs error message

		if completed.returncode == 0:
			return completed.stdout.decode("utf-8").split("\n")[0]
		else:
			message = completed.stderr.decode("utf-8")
			self.WriteFatal(f"Message from '{command}': {message}")
			raise Exception()  # XXX: needs error message

	def GetGitRemoteURL(self, remote: Nullable[str] = None) -> str:
		if self._platform is not Platforms.Workstation:
			return self._service.GetGitRepository()

		if remote is None:
			remote = self.GetGitRemote()

		command = "git"
		arguments = ("config", f"remote.{remote}.url")
		try:
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except CalledProcessError:
			raise Exception()  # XXX: needs error message

		if completed.returncode == 0:
			return completed.stdout.decode("utf-8").split("\n")[0]
		else:
			message = completed.stderr.decode("utf-8")
			self.WriteFatal(f"Message from '{command}': {message}")
			raise Exception()  # XXX: needs error message

	# 		self.WriteFatal(f"Message from '{command}': {message}")

	def GetProject(self, config: Configuration.Project) -> Project:
		return Project(
			name=config.name,
			version=config.version,
			variant=config.variant
		)

	def GetBuild(self, config: Configuration.Build) -> Build:
		dt = datetime.now()
		return Build(
			date=dt.date(),
			time=dt.time(),
			compiler=self.GetCompiler(config.compiler)
		)

	def GetCompiler(self, config: Configuration.Build.Compiler) -> Compiler:
		return Compiler(
			name=config.name,
			version=SemanticVersion(config.version),
			configuration=config.configuration,
			options=config.options
		)

	def GetEnvironment(self) -> Any:
		env = {}
		for key, value in environ.items():
			if not key.isidentifier():
				self.WriteWarning(f"Skipping environment variable '{key}', because it's not a valid Python identifier.")
				continue
			key = key.replace("(", "_")
			key = key.replace(")", "_")
			key = key.replace(" ", "_")
			env[key] = value

		def func(s) -> Generator[Tuple[str, Any], None, None]:
			for e in env.keys():
				yield (e, s.__getattribute__(e))

		Environment = make_dataclass(
			"Environment",
			[(name, str) for name in env.keys()],
#			bases=(SelfDescriptive,),
			namespace={
				"as_dict":       lambda self: env,
				"Keys":          lambda self: env.keys(),
				"KeyValuePairs": lambda self: func(self)
			},
			repr=True
		)

		return Environment(**env)

	def WriteSourceFile(self, template: Path, filename: Path) -> None:
		content = template.read_text()

		# apply variables
		content = content.format(**self._variables)

		with filename.open("w") as file:
			file.write(content)
