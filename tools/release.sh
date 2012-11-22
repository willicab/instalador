#!/bin/sh -e
#
# ====================================================================
# PACKAGE: canaima-semilla
# FILE: tools/release.sh
# DESCRIPTION:  Makes a new stable release of Canaima Semilla.
# USAGE: ./tools/release.sh
# COPYRIGHT:
# (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCE: GPL3
# ====================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

ROOTDIR="$( pwd )"
ROOTNAME="$( basename ${ROOTDIR} )"
PROJDIR="$( dirname ${ROOTDIR} )"
VERSION="${ROOTDIR}/VERSION"
CHANGELOG="${ROOTDIR}/ChangeLog"
CHANGES="$( tempfile )"
DEVERSION="$( tempfile )"
NEWCHANGES="$( tempfile )"
DATE=$( date +%D )

ERROR() {
	printf "\033[1;31m${1}\033[0m\n"
}

WARNING() {
	printf "\033[1;33m${1}\033[0m\n"
}

SUCCESS() {
	printf "\033[1;32m${1}\033[0m\n"
}

cd ${ROOTDIR}
if [ "$( git branch 2> /dev/null | sed -e '/^[^*]/d;s/\* //' )" != "development" ]; then
	ERROR "[MAIN] You are not on \"development\" branch."
	git checkout development
fi
if [ -n "$( git diff --exit-code 2> /dev/null )" ]; then
	ERROR "[MAIN] You have uncommitted code on \"development\" branch."
	exit 1
fi

git log > ${CHANGES}
cp ${VERSION} ${DEVERSION}
git checkout release
git clean -fd
git reset --hard

OLDCOMMIT="$( cat ${VERSION} | grep "COMMIT" | sed 's/COMMIT=//g;s/"//g' )"
OLDCOMMITLINE="$( cat ${CHANGES}  | grep -n "${OLDCOMMIT}" | awk -F: '{print $1}' )"
NEWVERSION="$( cat ${DEVERSION} | grep "VERSION" | sed 's/VERSION=//g;s/"//g;s/+.*//g' )"

echo "STABLE RELEASE v${NEWVERSION} (${DATE})" > ${NEWCHANGES}
cat ${CHANGES} | sed -n 1,${OLDCOMMITLINE}p | sed 's/commit.*//g;s/Author:.*//g;s/Date:.*//g;s/Merge.*//g;/^$/d;' >> ${NEWCHANGES}
sed -i 's/New stable release.*//g;s/    //g;/^$/d;' ${NEWCHANGES}
sed -i 's/New development snapshot.*//g;s/    //g;/^$/d;' ${NEWCHANGES}
sed -i 's/Signed-off-by:.*//g;s/    //g;/^$/d;' ${NEWCHANGES}
echo "" >> ${NEWCHANGES}
cat ${CHANGELOG} >> ${NEWCHANGES}

WARNING "Merging development into release ..."
git merge -q -s recursive -X theirs --squash development

mv ${NEWCHANGES} ${CHANGELOG}
rm ${CHANGES} ${DEVERSION}

LASTCOMMIT="$( git rev-parse HEAD )"

echo "VERSION=\"${NEWVERSION}\"" > ${VERSION}
echo "COMMIT=\"${LASTCOMMIT}\"" >> ${VERSION}
echo "RELDATE=\"${DATE}\"" >> ${VERSION}

WARNING "Committing changes ..."
git add .
git commit -q -a -m "New stable release ${NEWVERSION}"
git tag ${NEWVERSION} -m "New stable release ${NEWVERSION}"

git checkout development

SUCCESS "Stable Release Created"
