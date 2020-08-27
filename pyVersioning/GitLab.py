from dataclasses  import make_dataclass
from os           import environ


class GitLab:
	def getEnvironment(self):
		env = environ
		filteredEnv = {key:value for (key,value) in environ if key.startswith(("CI_", "GITLAB_")) and not key.endswith("_TOKEN")}

		# manually add some variables
		for key in ['CI']:
			try:
				filteredEnv[key] = env[key]
			except:
				pass

		# manually delete some variables
		for key in ['CI_JOB_TOKEN']:
			try:
				del filteredEnv[key]
			except:
				pass

		Environment = make_dataclass(
			"Environment",
			[(name, str) for name in env.keys()],
			namespace={
				'as_dict': lambda self: env
			}
		)

		return Environment(**env)
