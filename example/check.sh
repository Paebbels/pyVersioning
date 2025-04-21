#! /bin/bash

exampleName="$1"

cd "${exampleName}" || exit 1

check() {
	printf "$1"
	./example | grep -E "$2" > /dev/null
	if [[ $? -eq 0 ]]; then
		printf "[OK]\n"
	else
		printf "[MISMATCH]\n"
	fi
}

case "${exampleName}" in
	C)
		check "Check for version string ... " "^Version:\s+v2\.1\.6"
		check "Check Git SHA ...            " "${GITHUB_SHA}"
		check "Check Git repository ...     " "${GITHUB_REPOSITORY}"
		;;
	CXX)
		check "Check for version string ... " "^Version:\s+v2\.1\.6"
		check "Check Git SHA ...            " "${GITHUB_SHA}"
		check "Check Git repository ...     " "${GITHUB_REPOSITORY}"
		;;
	*)
		printf "Unknown example '%s'\n" "${exampleName}"
		;;
esac
