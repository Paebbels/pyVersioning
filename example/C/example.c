#include <stdio.h>

#include "versioning.h"

void printVersion(void) {
	printf("Project:  %s - %s\n",
		versioningInformation.project.name,
		versioningInformation.project.variant
	);
	printf("Version:  v%d.%d.%d\n",
		versioningInformation.version.major,
		versioningInformation.version.minor,
		versioningInformation.version.patch
	);
	printf("Git:      %s - %02d.%02d.%02d-%02d:%02d:%02d\n",
		versioningInformation.git.reference,
		versioningInformation.git.commit.datetime.date.day,
		versioningInformation.git.commit.datetime.date.month,
		versioningInformation.git.commit.datetime.date.year,
		versioningInformation.git.commit.datetime.time.hour,
		versioningInformation.git.commit.datetime.time.minute,
		versioningInformation.git.commit.datetime.time.second
	);
	printf("          %s\n", versioningInformation.git.commit.hash);
	printf("          %s\n", versioningInformation.git.repository);
	printf("Build on: %02d.%02d.%02d-%02d:%02d:%02d\n",
		versioningInformation.build.datetime.date.day,
		versioningInformation.build.datetime.date.month,
		versioningInformation.build.datetime.date.year,
		versioningInformation.build.datetime.time.hour,
		versioningInformation.build.datetime.time.minute,
		versioningInformation.build.datetime.time.second
	);
	printf("Compiler: %s (%d.%d.%d)\n",
		versioningInformation.build.compiler.name,
		versioningInformation.build.compiler.version.major,
		versioningInformation.build.compiler.version.minor,
		versioningInformation.build.compiler.version.patch
	);
}

int main(char** argv, int argc) {
	printf(
		"========================================\n"
		"pyVersioning Example\n"
		"========================================\n"
	);

	printVersion();

	return 0;
}
