from os         import environ as os_environ, getcwd as os_getcwd
from subprocess import run as subprocess_run, PIPE as subprocess_PIPE, STDOUT as subprocess_STDOUT, CalledProcessError, TimeoutExpired

from unittest   import TestCase


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class GitLab(TestCase):
	def test_Variables(self):
		args = [
			"python",
			"../../pyVersioning/cli.py",
			"variables"
		]
		env = {k:v for k,v in os_environ.items()}
		env["GITLAB_CI"] =      "YES"
		env["CI_COMMIT_SHA"] =  "1234567890123456789012345678901234567890"

		try:
			prog = subprocess_run(
				args=args,
				stdout=subprocess_PIPE,
				stderr=subprocess_STDOUT,
				shell=True,
#				cwd="",
				env=env,
				check=True,
				encoding="utf-8"
			)
		except CalledProcessError as ex:
			print("CALLED PROCESS ERROR")
#			print(ex.returncode)
#			print(ex.output)
			exit(1)
		except TimeoutExpired as ex:
			print("TIMEOUT EXPIRED")
			exit(2)
		except Exception as ex:
			print("EXCEPTION")
			print(ex)
			exit(3)

		print(prog.stdout.encode("utf-8"))

