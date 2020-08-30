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
from dataclasses  import dataclass, make_dataclass, field
from datetime     import datetime
from pathlib      import Path
from os           import environ

from flags        import Flags
from pyTerminalUI import ILineTerminal

from pyVersioning.AppVeyor  import AppVeyor
from pyVersioning.CIService import WorkStation
from pyVersioning.GitLab    import GitLab
from pyVersioning.GitHub    import GitHub
from pyVersioning.Travis    import Travis


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


@dataclass
class Commit():
	hash : str
	date : datetime


@dataclass
class Git():
	commit      : Commit
	reference   : str = field(init=False)
	tag         : str = ""
	branch      : str = ""
	repository  : str = ""

	def __post_init__(self):
		if self.tag != "":
			self.reference = self.tag
		elif self.branch != "":
			self.reference = self.branch
		else:
			self.reference = "[Detached HEAD]"


@dataclass
class Project():
	name    : str
	variant : str


@dataclass
class Compiler():
	name          : str
	version       : Version
	configuration : str
	options       : str


@dataclass
class Build():
	date     : datetime
	compiler : Compiler


class Platforms(Flags):
	Workstation = 1
	AppVeyor = 2
	GitHub = 3
	GitLab = 4
	Travis = 5


class Versioning(ILineTerminal):
	platform  : int = Platforms.Workstation
	variables : dict

	def __init__(self, terminal):
		super().__init__(terminal)

		if 'APPVEYOR' in environ:
			self.platform = Platforms.AppVeyor
		elif 'GITHUB_ACTIONS' in environ:
			self.platform = Platforms.GitHub
		elif 'GITLAB_CI' in environ:
			self.platform = Platforms.GitLab
		elif 'TRAVIS' in environ:
			self.platform = Platforms.Travis
		else:
			self.platform = Platforms.Workstation

	def collectData(self):
		self.variables = {}

		if self.platform is Platforms.AppVeyor:
			self.service                = AppVeyor()
			self.variables['appveyor']  = self.service.getEnvironment()
		elif self.platform is Platforms.GitHub:
			self.service                = GitHub()
			self.variables['github']    = self.service.getEnvironment()
		elif self.platform is Platforms.GitLab:
			self.service                = GitLab()
			self.variables['gitlab']    = self.service.getEnvironment()
		elif self.platform is Platforms.Travis:
			self.service                = Travis()
			self.variables['travis']    = self.service.getEnvironment()
		else:
			self.service                = WorkStation()

		self.variables['tool']     = Tool("pyVersioning", Version(0,6,3)),
		self.variables['version']  = self.getVersion()
		self.variables['git']      = self.getGitInformation()
		self.variables['project']  = self.getProject()
		self.variables['build']    = self.getBuild()
		self.variables['env']      = self.getEnvironment()
		self.variables['platform'] = self.service.getPlatform()

	def getVersion(self) -> Version:
		return Version("0.0.0")

	def getGitInformation(self):
		return Git(
			commit=self.getLastCommit(),
			tag=self.getGitTag(),
			branch=self.getGitLocalBranch(),
			repository=self.getGitRemoteURL()
		)

	def getLastCommit(self):
		return Commit(
			hash=self.getGitHash(),
			date=self.getCommitDate()
		)

	def getGitHash(self):
		if self.platform is not Platforms.Workstation:
			return self.service.getGitHash()

		try:
			command =   "git rev-parse HEAD"
			completed = subprocess_run(command, stdout=PIPE, stderr=PIPE)
		except:
			return "0" * 40
		if completed.returncode == 0:
			return completed.stdout.decode('utf-8').split("\n")[0]
		else:
			message = completed.stderr.decode('utf-8')
			self.WriteFatal("Message from '{command}': {message}".format(command=command, message=message))

	def getCommitDate(self):
		try:
			command =   "git show -s --format=%ct HEAD"
			completed = subprocess_run(command, stdout=PIPE, stderr=PIPE)
		except:
			return None
		if completed.returncode == 0:
			ts = int(completed.stdout.decode('utf-8').split("\n")[0])
			return datetime.fromtimestamp(ts)
		else:
			message = completed.stderr.decode('utf-8')
			self.WriteFatal("Message from '{command}': {message}".format(command=command, message=message))

	def getGitLocalBranch(self):
		if self.platform is not Platforms.Workstation:
			return self.service.getGitBranch()

		try:
			command =   "git branch --show-current"
			completed = subprocess_run(command, stdout=PIPE, stderr=PIPE)
		except:
			return ""
		if completed.returncode == 0:
			return completed.stdout.decode('utf-8').split("\n")[0]
		else:
			message = completed.stderr.decode('utf-8')
			self.WriteFatal("Message from '{command}': {message}".format(command=command, message=message))

	def getGitRemoteBranch(self, localBranch : str = None):
		if localBranch is None:
			localBranch = self.getGitLocalBranch()

		try:
			command =   "git config branch.{localBranch}.merge".format(localBranch=localBranch)
			completed = subprocess_run(command, stdout=PIPE, stderr=PIPE)
		except:
			return ""
		if completed.returncode == 0:
			return completed.stdout.decode('utf-8').split("\n")[0]
		else:
			message = completed.stderr.decode('utf-8')
			self.WriteFatal("Message from '{command}': {message}".format(command=command, message=message))

	def getGitRemote(self, localBranch : str = None):
		if localBranch is None:
			localBranch = self.getGitLocalBranch()

		try:
			command =   "git config branch.{localBranch}.remote".format(localBranch=localBranch)
			completed = subprocess_run(command, stdout=PIPE, stderr=PIPE)
		except:
			return ""
		if completed.returncode == 0:
			return completed.stdout.decode('utf-8').split("\n")[0]
		else:
			message = completed.stderr.decode('utf-8')
			self.WriteFatal("Message from '{command}': {message}".format(command=command, message=message))

	def getGitTag(self):
		if self.platform is not Platforms.Workstation:
			return self.service.getGitTag()

		try:
			command =   "git tag --points-at HEAD"
			completed = subprocess_run(command, stdout=PIPE, stderr=PIPE)
		except:
			return ""
		if completed.returncode == 0:
			return completed.stdout.decode('utf-8').split("\n")[0]
		else:
			message = completed.stderr.decode('utf-8')
			self.WriteFatal("Message from '{command}': {message}".format(command=command, message=message))

	def getGitRemoteURL(self, remote : str = None):
		if remote is None:
			remote = self.getGitRemote()
		try:
			command =   "git config remote.{remote}.url".format(remote=remote)
			completed = subprocess_run(command, stdout=PIPE, stderr=PIPE)
		except:
			return ""
		if completed.returncode == 0:
			return completed.stdout.decode('utf-8').split("\n")[0]
		else:
			message = completed.stderr.decode('utf-8')
			self.WriteFatal("Message from '{command}': {message}".format(command=command, message=message))

	def getProject(self):
		return Project(
			name="not implemented",
			variant="not implemented"
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
			configuration="",
			options=""
		)

	def getEnvironment(self):
		env = {}
		for key, value in environ.items():
			if not key.isidentifier():
				self.WriteWarning("Skipping environment variable '{key}', because it's not a valid Python identifier.".format(key=key))
				continue
			key = key.replace("(", "_")
			key = key.replace(")", "_")
			key = key.replace(" ", "_")
			env[key] = value

		Environment = make_dataclass(
			"Environment",
			[(name, str) for name in env.keys()],
			namespace={
				'as_dict': lambda self: env
			}
		)

		return Environment(**env)

	def writeSourceFile(self, template : Path, filename : Path):
		with template.open('r') as file:
			content = template.read_text()

		# apply variables
		content = content.format(**self.variables)

		with filename.open('w') as file:
			file.write(content)
