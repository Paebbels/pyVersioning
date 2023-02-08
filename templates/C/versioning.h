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
/* @brief     C Structure definitions for pyVersioning                                                                 *
/*                                                                                                                     *
/* @copyright Copyright 2020-2023 Patrick Lehmann - Boetzingen, Germany                                                *
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
#include <stdint.h>

#ifndef VERSIONING_H
#define VERSIONING_H

typedef struct {
	uint8_t day;
	uint8_t month;
	uint16_t year;
} Date;

typedef struct {
	uint8_t hour;
	uint8_t minute;
	uint8_t second;
} Time;

typedef struct {
	Date date;
	Time time;
} DateTime;

typedef struct {
	uint8_t flags;
	uint16_t major;
	uint16_t minor;
	uint16_t patch;
} Version;

typedef struct {
	char       hash[41];    // hex-value as string (160-bit => 40 characters + \0)
	DateTime   datetime;
} Commit;

typedef struct {
	Commit      commit;
	const char* reference;
	const char* repository;
} Git;

typedef struct {
	const char* name;
	const char* variant;
} Project;

typedef struct {
	const char* name;
	Version     version;
	const char* configuration;
	const char* options;
} Compiler;

typedef struct {
	DateTime    datetime;
	Compiler    compiler;
} Build;

typedef struct {
	Version    version;
	Git        git;
	Project    project;
	Build      build;
} VersioningInformation;


extern const VersioningInformation versioningInformation;

#endif /* VERSIONING_H */
