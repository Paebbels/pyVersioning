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
/* @brief     C++ Structure definitions for pyVersioning                                                               *
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

#ifndef VERSIONING_H
#define VERSIONING_H

#include <cstdint>

// Check if <string_view> is available using __has_include.
#if defined(__has_include)
#if __has_include(<string_view>)
#include <string_view>
#define PYVERSIONING_HAS_STRING_VIEW
#endif // #if __has_include(<string_view>)
#endif // #if defined(__has_include)

namespace pyVersioning 
{

#ifdef PYVERSIONING_HAS_STRING_VIEW
using FixedString_t = std::string_view;
#elif __cplusplus >= 201103L
using FixedString_t = char const *;
#else
typedef char const * FixedString_t;
#endif

struct Date {
	uint8_t  day;
	uint8_t  month;
	uint16_t year;
};

struct Time {
	uint8_t hour;
	uint8_t minute;
	uint8_t second;
};

struct DateTime {
	Date date;
	Time time;
};

struct Version {
	uint8_t  flags;
	uint16_t major;
	uint16_t minor;
	uint16_t patch;
};

struct Commit {
	pyVersioning::FixedString_t hash;
	DateTime                   datetime;
};

struct Git {
	Commit                      commit;
	pyVersioning::FixedString_t reference;
	pyVersioning::FixedString_t repository;
};

struct Project {
	pyVersioning::FixedString_t name;
	pyVersioning::FixedString_t variant;
};

struct Compiler {
	pyVersioning::FixedString_t name;
	Version                     version;
	pyVersioning::FixedString_t configuration;
	pyVersioning::FixedString_t options;
};

struct Build {
	DateTime    datetime;
	Compiler    compiler;
};

struct VersioningInformation {
	Version    version;
	Git        git;
	Project    project;
	Build      build;
};

} // namespace pyVersioning 

extern const pyVersioning::VersioningInformation versioningInformation;

#endif /* VERSIONING_H */
