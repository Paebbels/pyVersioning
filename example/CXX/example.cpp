/***********************************************************************************************************************
/*            __     __            _             _                                                                     *
/*  _ __  _   \ \   / /__ _ __ ___(_) ___  _ __ (_)_ __   __ _                                                         *
/* | '_ \| | | \ \ / / _ \ '__/ __| |/ _ \| '_ \| | '_ \ / _` |                                                        *
/* | |_) | |_| |\ V /  __/ |  \__ \ | (_) | | | | | | | | (_| |                                                        *
/* | .__/ \__, | \_/ \___|_|  |___/_|\___/|_| |_|_|_| |_|\__, |                                                        *
/* |_|    |___/                                          |___/                                                         *
/***********************************************************************************************************************
/* @author    Patrick Lehmann                                                                                          *
/*                                                                                                                     *
/* @brief     Code example in C++                                                                                      *
/*                                                                                                                     *
/* @copyright Copyright 2020-2024 Patrick Lehmann - Boetzingen, Germany                                                *
/*                                                                                                                     *
/* Licensed under the Apache License, Version 2.0 (the "License");                                                     *
/* you may not use this file except in compliance with the License.                                                    *
/* You may obtain a copy of the License at                                                                             *
/*                                                                                                                     *
/*   http://www.apache.org/licenses/LICENSE-2.0                                                                        *
/*                                                                                                                     *
/* Unless required by applicable law or agreed to in writing, software                                                 *
/* distributed under the License is distributed on an "AS IS" BASIS,                                                   *
/* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                            *
/* See the License for the specific language governing permissions and                                                 *
/* limitations under the License.                                                                                      *
/*                                                                                                                     *
/* SPDX-License-Identifier: Apache-2.0                                                                                 *
/**********************************************************************************************************************/
#include <iostream>
#include <iomanip>
#include <cstdlib>

#include "versioning.hpp"

void printVersion()
{
	using namespace pyVersioning;
	
	std::cout << "Project:  "
			  << versioningInformation.project.name
			  << " - "
			  << versioningInformation.project.variant
			  << "\n";

	std::cout << "Version:  v"
			  << std::to_string(versioningInformation.version.major)
			  << "."
			  << std::to_string(versioningInformation.version.minor)
			  << "."
			  << std::to_string(versioningInformation.version.patch)
			  << "\n";

	std::cout << "Git:      "
			  << versioningInformation.git.reference
			  << " - "
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.git.commit.datetime.date.day)
			  << "."
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.git.commit.datetime.date.month)
			  << "."
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.git.commit.datetime.date.year)
			  << "-"
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.git.commit.datetime.time.hour)
			  << ":"
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.git.commit.datetime.time.minute)
			  << ":"
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.git.commit.datetime.time.second)
			  << "\n";

	std::cout << "          " << versioningInformation.git.commit.hash << "\n";
	std::cout << "          " << versioningInformation.git.repository << "\n";
	std::cout << "Build on: "
			  << versioningInformation.git.reference
			  << " - "
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.build.datetime.date.day)
			  << "."
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.build.datetime.date.month)
			  << "."
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.build.datetime.date.year)
			  << "-"
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.build.datetime.time.hour)
			  << ":"
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.build.datetime.time.minute)
			  << ":"
			  << std::setw(2) << std::setfill('0') << std::to_string(versioningInformation.build.datetime.time.second)
			  << "\n";

	std::cout << "Compiler: "
			  << versioningInformation.build.compiler.name
			  << " ("
			  << std::to_string(versioningInformation.build.compiler.version.major)
			  << "."
			  << std::to_string(versioningInformation.build.compiler.version.minor)
			  << "."
			  << std::to_string(versioningInformation.build.compiler.version.patch)
			  << ")" << std::endl;
}

int main()
{
	std::cout << "========================================\n"
			  << "pyVersioning Example C++\n"
			  << "========================================"
			  << std::endl;

	printVersion();

	return EXIT_SUCCESS;
}
