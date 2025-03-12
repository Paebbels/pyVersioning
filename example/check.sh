#! /bin/bash

exampleName="$1"

cd ${exampleName} || exit 1

case "${exampleName}" in
	C)
		./example
		./example | grep version
		;;
	CXX)
		./example
		./example | grep version
		;;
	*)
		printf "Unknown example '%s'\n" "${exampleName}"
		;;
esac
