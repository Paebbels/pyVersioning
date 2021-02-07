from os         import environ as os_environ, getcwd as os_getcwd
from subprocess import run as subprocess_run, PIPE as subprocess_PIPE, STDOUT as subprocess_STDOUT, CalledProcessError, TimeoutExpired

from unittest import TestCase, skip


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class GitLabEnvironment(TestCase):
	@staticmethod
	def __getExecutable(command: str, *args):
		callArgs = [
			"python",
			"../../pyVersioning/cli.py",
			command
		]
		if len(args) > 0:
			callArgs.extend(args)

		return callArgs

	@staticmethod
	def __getServiceEnvironment(**kwargs):
		env = {k: v for k, v in os_environ.items()}

		if len(kwargs) == 0:
			env["GITLAB_CI"] =          "YES"
			env["CI_COMMIT_SHA"] =      "1234567890123456789012345678901234567890"
			env["CI_COMMIT_BRANCH"] =   "dev"
			env["CI_REPOSITORY_URL"] =  "gitlab.com/path/to/repo.git"
		else:
			for k,v in kwargs.items():
				env[k] = v

		return env

	#@skip("under development")
	def test_Variables(self):
		try:
			prog = subprocess_run(
				args=self.__getExecutable("variables"),
				stdout=subprocess_PIPE,
				stderr=subprocess_STDOUT,
				shell=True,
				env=self.__getServiceEnvironment(),
				check=True,
				encoding="utf-8"
			)
		except CalledProcessError as ex:
			print("CALLED PROCESS ERROR")
			print(ex.returncode)
			print(ex.output)
			exit(1)
		except TimeoutExpired as ex:
			print("TIMEOUT EXPIRED")
			exit(2)
		except Exception as ex:
			print("EXCEPTION")
			print(ex)
			exit(3)

		output = prog.stdout
		print()
		for line in output.split("\n"):
			print(line)

	#@skip("under development")
	def test_Fillout(self):
		try:
			prog = subprocess_run(
				args=self.__getExecutable("fillout", "template.in", "template.out"),
				stdout=subprocess_PIPE,
				stderr=subprocess_STDOUT,
				shell=True,
				env=self.__getServiceEnvironment(),
				check=True,
				encoding="utf-8"
			)
		except CalledProcessError as ex:
			print("CALLED PROCESS ERROR")
			print(ex.returncode)
			print(ex.output)
			exit(1)
		except TimeoutExpired as ex:
			print("TIMEOUT EXPIRED")
			exit(2)
		except Exception as ex:
			print("EXCEPTION")
			print(ex)
			exit(3)

		output = prog.stdout
		print()
		for line in output.split("\n"):
			print(line)


