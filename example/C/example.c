/***********************************************************************************************************************
 *            __     __            _             _                                                                     *
 *  _ __  _   \ \   / /__ _ __ ___(_) ___  _ __ (_)_ __   __ _                                                         *
 * | '_ \| | | \ \ / / _ \ '__/ __| |/ _ \| '_ \| | '_ \ / _` |                                                        *
 * | |_) | |_| |\ V /  __/ |  \__ \ | (_) | | | | | | | | (_| |                                                        *
 * | .__/ \__, | \_/ \___|_|  |___/_|\___/|_| |_|_|_| |_|\__, |                                                        *
 * |_|    |___/                                          |___/                                                         *
 ***********************************************************************************************************************
 * @author    Patrick Lehmann                                                                                          *
 *                                                                                                                     *
 * @brief     Code example in C                                                                                        *
 *                                                                                                                     *
 * @copyright Copyright 2020-2025 Patrick Lehmann - Boetzingen, Germany                                                *
 *                                                                                                                     *
 * Licensed under the Apache License, Version 2.0 (the "License");                                                     *
 * you may not use this file except in compliance with the License.                                                    *
 * You may obtain a copy of the License at                                                                             *
 *                                                                                                                     *
 *   http://www.apache.org/licenses/LICENSE-2.0                                                                        *
 *                                                                                                                     *
 * Unless required by applicable law or agreed to in writing, software                                                 *
 * distributed under the License is distributed on an "AS IS" BASIS,                                                   *
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                            *
 * See the License for the specific language governing permissions and                                                 *
 * limitations under the License.                                                                                      *
 *                                                                                                                     *
 * SPDX-License-Identifier: Apache-2.0                                                                                 *
 **********************************************************************************************************************/

#include <stdio.h>
#include <stdlib.h>

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

int main(void) {
	printf(
		"========================================\n"
		"pyVersioning Example C\n"
		"========================================\n"
	);

	printVersion();

	return EXIT_SUCCESS;
}
