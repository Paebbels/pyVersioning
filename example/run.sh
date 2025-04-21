#! /bin/bash

exampleName="$1"

cd "${exampleName}" || exit 1

case "${exampleName}" in
	C)
		./example
		;;
	CXX)
		./example
		;;
	*)
		printf "Unknown example '%s'\n" "${exampleName}"
		;;
esac
