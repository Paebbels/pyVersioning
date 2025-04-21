#! /bin/bash

exampleName="$1"

cd "${exampleName}" || exit 1

case "${exampleName}" in
	C)
		pyVersioning fillout ../../templates/C/versioning.c.template versioning.c
		;;
	CXX)
		pyVersioning fillout ../../templates/CXX/versioning.cpp.template versioning.cpp
		;;
	*)
		printf "Unknown example '%s'\n" "${exampleName}"
		;;
esac
