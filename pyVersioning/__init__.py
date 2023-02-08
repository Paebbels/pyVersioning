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
# Copyright 2020-2023 Patrick Lehmann - Bötzingen, Germany                                                             #
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
__copyright__ = "2020-2023, Patrick Lehmann"
__license__ =   "Apache License, Version 2.0"
__version__ =   "0.9.0"
__keywords__ =  ["Python3", "Template", "Versioning", "Git"]

from dataclasses  import dataclass, make_dataclass, field
from datetime     import date, time, datetime
from enum         import Enum, auto
from os           import environ
from pathlib      import Path
from subprocess   import run as subprocess_run, PIPE
from typing       import Union, Any, Dict

from pyTooling.Decorators import export
from pyTooling.Versioning       import SemVersion
from pyTooling.TerminalUI       import ILineTerminal

from pyVersioning.Utils         import SelfDescriptive
from pyVersioning.AppVeyor      import AppVeyor
from pyVersioning.CIService     import WorkStation
from pyVersioning.Configuration import Configuration
from pyVersioning.GitLab        import GitLab
from pyVersioning.GitHub        import GitHub
from pyVersioning.Travis        import Travis


@export
@dataclass
class Tool(SelfDescriptive):
	name    : str
	version : SemVersion

	_public = ["name", "version"]


@export
class Date(date, SelfDescriptive):
	_public = ["day", "month", "year"]


@export
class Time(time, SelfDescriptive):
	_public = ["hour", "minute", "second"]


@export
@dataclass
class Author(SelfDescriptive):
	name:  str
	email: str

	_public = ["name", "email"]


@export
@dataclass
class Commit(SelfDescriptive):
	hash:    str
	date:    date
	time:    time
	author:  Author
	comment: str
	oneline: str = field(init=False)

	_public = ["hash", "date", "time", "author", "comment", "oneline"]

	def __post_init__(self) -> None:
		"""Calculate `oneline` from `comment`."""

		if self.comment != "":
			self.oneline = self.comment.split("\n")[0]


@export
@dataclass
class Git(SelfDescriptive):
	commit:     Commit
	reference:  str = field(init=False)
	tag:        str = ""
	branch:     str = ""
	repository: str = ""

	_public = ["commit", "reference", "tag", "branch", "repository"]

	def __post_init__(self) -> None:
		"""Calculate `reference` from `tag` or `branch`."""

		if self.tag != "":
			self.reference = self.tag
		elif self.branch != "":
			self.reference = self.branch
		else:
			self.reference = "[Detached HEAD]"


@export
@dataclass
class Project(SelfDescriptive):
	name:     str
	variant:  str
	version:  SemVersion

	_public = ["name", "variant", "version"]

	def __init__(self, name: str, version: Union[str, SemVersion] = None, variant: str = None) -> None:
		"""Assign fields and convert version string to a `Version` object."""

		self.name    = name    if name    is not None else ""
		self.variant = variant if variant is not None else ""

		if isinstance(version, SemVersion):
			self.version = version
		elif isinstance(version, str):
			self.version = SemVersion(version)
		elif version is None:
			self.version = SemVersion(0, 0, 0)


@export
@dataclass
class Compiler(SelfDescriptive):
	name:           str
	version:        SemVersion
	configuration:  str
	options:        str

	_public = ["name", "version", "configuration", "options"]

	def __init__(self, name: str, version: Union[str, SemVersion] = "", configuration: str = "", options: str = "") -> None:
		"""Assign fields and convert version string to a `Version` object."""

		self.name          = name          if name          is not None else ""
		self.configuration = configuration if configuration is not None else ""
		self.options       = options       if options       is not None else ""

		if isinstance(version, SemVersion):
			self.version     = version
		elif isinstance(version, str):
			self.version     = SemVersion(version)
		elif version is None:
			self.version     = SemVersion(0, 0, 0)


@export
@dataclass
class Build(SelfDescriptive):
	date:     date
	time:     time
	compiler: Compiler

	_public = ["date", "time", "compiler"]


@export
class Platforms(Enum):
	Workstation = auto()
	AppVeyor =    auto()
	GitHub =      auto()
	GitLab =      auto()
	Travis =      auto()


@export
class GitShowCommand(Enum):
	CommitDateTime =       auto()
	CommitAuthorName =     auto()
	CommitAuthorEmail =    auto()
	CommitCommitterName =  auto()
	CommitCommitterEmail = auto()
	CommitHash =           auto()
	CommitComment =        auto()


@export
class Versioning(ILineTerminal):
	platform:  Platforms = Platforms.Workstation
	variables: Dict

	def __init__(self, terminal: ILineTerminal):
		super().__init__(terminal)

		self.variables = {}

		if "APPVEYOR" in environ:
			self.platform = Platforms.AppVeyor
		elif "GITHUB_ACTIONS" in environ:
			self.platform = Platforms.GitHub
		elif "GITLAB_CI" in environ:
			self.platform = Platforms.GitLab
		elif "TRAVIS" in environ:
			self.platform = Platforms.Travis
		else:
			self.platform = Platforms.Workstation

	def loadDataFromConfiguration(self, config: Configuration) -> None:
		"""Preload versioning information from configuration file."""

		self.variables["project"] = self.getProject(config.project)
		self.variables["build"]   = self.getBuild(config.build)
		self.variables["version"] = self.getVersion(config.project)

	def collectData(self) -> None:
		"""Collect versioning information from environment including CI services (if available)."""

		if self.platform is Platforms.AppVeyor:
			self.service                = AppVeyor()
			self.variables["appveyor"]  = self.service.getEnvironment()
		elif self.platform is Platforms.GitHub:
			self.service                = GitHub()
			self.variables["github"]    = self.service.getEnvironment()
		elif self.platform is Platforms.GitLab:
			self.service                = GitLab()
			self.variables["gitlab"]    = self.service.getEnvironment()
		elif self.platform is Platforms.Travis:
			self.service                = Travis()
			self.variables["travis"]    = self.service.getEnvironment()
		else:
			self.service                = WorkStation()

		self.variables["tool"]     = Tool("pyVersioning", SemVersion(0,7,1))
		self.variables["git"]      = self.getGitInformation()
		self.variables["env"]      = self.getEnvironment()
		self.variables["platform"] = self.service.getPlatform()

		self.calculateData()

	def calculateData(self) -> None:
		if self.variables["git"].tag != "":
			pass

	def getVersion(self, config: Configuration.Project) -> SemVersion:
		if config.version is not None:
			return config.version
		else:
			return SemVersion("0.0.0")

	def getGitInformation(self) -> Git:
		return Git(
			commit=self.getLastCommit(),
			tag=self.getGitTag(),
			branch=self.getGitLocalBranch(),
			repository=self.getGitRemoteURL()
		)

	def getLastCommit(self) -> Commit:
		dt = self.getCommitDate()

		return Commit(
			hash=self.getGitHash(),
			date=dt.date(),
			time=dt.time(),
			author=self.getCommitAuthor(),
			comment=self.getCommitComment()
		)

	def getGitHash(self) -> str:
		if self.platform is not Platforms.Workstation:
			return self.service.getGitHash()

		return self.execGitShow(GitShowCommand.CommitHash)

	def getCommitDate(self) -> datetime:
		if self.platform is not Platforms.Workstation:
			return self.service.getCommitDate()

		datetimeString = self.execGitShow(GitShowCommand.CommitDateTime)
		return datetime.fromtimestamp(int(datetimeString))

	def getCommitAuthor(self) -> Author:
		return Author(
			name=self.getCommitAuthorName(),
			email=self.getCommitAuthorEmail()
		)

	def getCommitAuthorName(self) -> str:
		return self.execGitShow(GitShowCommand.CommitAuthorName)

	def getCommitAuthorEmail(self) -> str:
		return self.execGitShow(GitShowCommand.CommitAuthorEmail)

	def getCommitCommitterName(self) -> str:
		return self.execGitShow(GitShowCommand.CommitCommitterName)

	def getCommitCommitterEmail(self) -> str:
		return self.execGitShow(GitShowCommand.CommitCommitterEmail)

	def getCommitComment(self) -> str:
		return self.execGitShow(GitShowCommand.CommitComment)

	def getGitLocalBranch(self) -> str:
		if self.platform is not Platforms.Workstation:
			return self.service.getGitBranch()

		try:
			command =   "git"
			arguments = ("branch", "--show-current")
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except:
			return ""
		if completed.returncode == 0:
			return completed.stdout.decode("utf-8").split("\n")[0]
		else:
			message = completed.stderr.decode("utf-8")
			self.WriteFatal(f"Message from '{command}': {message}")

	def getGitRemoteBranch(self, localBranch: str = None) -> str:
		if self.platform is not Platforms.Workstation:
			return self.service.getGitBranch()

		if localBranch is None:
			localBranch = self.getGitLocalBranch()

		try:
			command =   "git"
			arguments = ("config", f"branch.{localBranch}.merge")
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except:
			raise Exception()

		if completed.returncode == 0:
			return completed.stdout.decode("utf-8").split("\n")[0]
		else:
			message = completed.stderr.decode("utf-8")
			self.WriteFatal(f"Message from '{command}': {message}")
			raise Exception

	def getGitRemote(self, localBranch: str = None) -> str:
		if localBranch is None:
			localBranch = self.getGitLocalBranch()

		try:
			command =   "git"
			arguments=  ("config", f"branch.{localBranch}.remote")
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except:
			raise Exception

		if completed.returncode == 0:
			return completed.stdout.decode("utf-8").split("\n")[0]
		elif completed.returncode == 1:
			self.WriteWarning(f"Branch '{localBranch}' is not pushed to a remote.")
			return f"(local) {localBranch}"
		else:
			message = completed.stderr.decode("utf-8")
			self.WriteFatal(f"Message from '{command}': {message}")
			raise Exception

	def getGitTag(self) -> str:
		if self.platform is not Platforms.Workstation:
			return self.service.getGitTag()

		try:
			command =   "git"
			arguments = ("tag", "--points-at", "HEAD")
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except:
			raise Exception

		if completed.returncode == 0:
			return completed.stdout.decode("utf-8").split("\n")[0]
		else:
			message = completed.stderr.decode("utf-8")
			self.WriteFatal(f"Message from '{command}': {message}")
			raise Exception

	def getGitRemoteURL(self, remote: str = None) -> str:
		if self.platform is not Platforms.Workstation:
			return self.service.getGitRepository()

		if remote is None:
			remote = self.getGitRemote()
		try:
			command =   "git"
			arguments = ("config", f"remote.{remote}.url")
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except:
			raise Exception

		if completed.returncode == 0:
			return completed.stdout.decode("utf-8").split("\n")[0]
		else:
			message = completed.stderr.decode("utf-8")
			self.WriteFatal(f"Message from '{command}': {message}")
			raise Exception

	__GIT_SHOW_COMMAND_TO_FORMAT_LOOKUP = {
		GitShowCommand.CommitHash: "%H",
		GitShowCommand.CommitDateTime: "%ct",
		GitShowCommand.CommitAuthorName: "%an",
		GitShowCommand.CommitAuthorEmail: "%ae",
		GitShowCommand.CommitCommitterName: "%cn",
		GitShowCommand.CommitCommitterEmail: "%ce",
		GitShowCommand.CommitComment: "%B",
	}

	def execGitShow(self, command: GitShowCommand) -> str:
		format = f"--format='{self.__GIT_SHOW_COMMAND_TO_FORMAT_LOOKUP[command]}'"

		try:
			command =   "git"
			arguments = ("show", "-s", format) #, "HEAD")
			completed = subprocess_run((command, *arguments), stdout=PIPE, stderr=PIPE)
		except:
			return ""
		if completed.returncode == 0:
			comment = completed.stdout.decode("utf-8")
			return comment[1:-2]
		else:
			message = completed.stderr.decode("utf-8")
			self.WriteFatal(f"Message from '{command}': {message}")

	def getProject(self, config: Configuration.Project) -> Project:
		return Project(
			name=config.name,
			version=config.version,
			variant=config.variant
		)

	def getBuild(self, config: Configuration.Build) -> Build:
		dt = datetime.now()
		return Build(
			date=dt.date(),
			time=dt.time(),
			compiler=self.getCompiler(config.compiler)
		)

	def getCompiler(self, config: Configuration.Build.Compiler) -> Compiler:
		return Compiler(
			name=config.name,
			version=SemVersion(config.version),
			configuration=config.configuration,
			options=config.options
		)

	def getEnvironment(self) -> Any:
		env = {}
		for key, value in environ.items():
			if not key.isidentifier():
				self.WriteWarning(f"Skipping environment variable '{key}', because it's not a valid Python identifier.")
				continue
			key = key.replace("(", "_")
			key = key.replace(")", "_")
			key = key.replace(" ", "_")
			env[key] = value

		def func(s):
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

	def writeSourceFile(self, template: Path, filename: Path) -> None:
		content = template.read_text()

		# apply variables
		content = content.format(**self.variables)

		with filename.open("w") as file:
			file.write(content)
