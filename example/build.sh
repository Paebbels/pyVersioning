#! /bin/bash

exampleName="$1"

cd "${exampleName}" || exit 1

case "${exampleName}" in
	C)
		gcc \
			-Wall \
			-Wextra \
			-Wundef \
			-Wpointer-arith \
			-Wcast-align \
			-Wstrict-prototypes \
			-Wstrict-overflow=5 \
			-Wwrite-strings \
			-Waggregate-return \
			-Wcast-qual \
			-Wswitch-enum \
			-Wconversion \
			-Wunreachable-code \
			-o example \
			example.c versioning.c
		;;
	CXX)
		g++ \
			-Wall \
			-Wextra \
			-Wundef \
			-Wpointer-arith \
			-Wcast-align \
			-Wstrict-overflow=5 \
			-Wwrite-strings \
			-Wcast-qual \
			-Wswitch-enum \
			-Wconversion \
			-Wunreachable-code \
			-o example \
			example.cpp versioning.cpp
		;;
	*)
		printf "Unknown example '%s'\n" "${exampleName}"
		;;
esac
