#!/bin/sh -e
#
# ====================================================================
# PACKAGE: canaima-semilla
# FILE: tools/snapshot.sh
# DESCRIPTION:  Makes a new development snapshot of Canaima Semilla.
# USAGE: ./tools/snapshot.sh
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
VERSION="${ROOTDIR}/VERSION"
CHANGELOG="${ROOTDIR}/ChangeLog"
CHANGES="$( tempfile )"
NEWCHANGES="$( tempfile )"
DATE="$( date +%D )"
SNAPSHOT="dev$( date +%Y%m%d%H%M%S )"

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

if [ "$( git status -s )" = "" ]; then
	ERROR "Nothing to commit, aborting."
	exit 1
fi

WARNING "Committing changes ..."
git add .
git commit -a

if [ ${?} -eq 1 ]; then
	ERROR "Empty commit message, aborting."
	exit 1
fi

git log > ${CHANGES}

OLDVERSION="$( cat ${VERSION} | grep "VERSION" | sed 's/VERSION=//g;s/"//g' )"
OLDCOMMIT="$( cat ${VERSION} | grep "COMMIT" | sed 's/COMMIT=//g;s/"//g' )"
OLDCOMMITLINE="$( cat ${CHANGES}  | grep -n "${OLDCOMMIT}" | awk -F: '{print $1}' )"

read -p "Enter new version (last version was ${OLDVERSION}): " REPLY
NEWVERSION="${REPLY}"

echo "DEVELOPMENT RELEASE v${NEWVERSION}+${SNAPSHOT} (${DATE})" > ${NEWCHANGES}
cat ${CHANGES} | sed -n 1,${OLDCOMMITLINE}p | sed 's/commit.*//g;s/Author:.*//g;s/Date:.*//g;s/Merge.*//g;/^$/d;' >> ${NEWCHANGES}
sed -i 's/New development snapshot.*//g;s/    //g;/^$/d;' ${NEWCHANGES}
sed -i 's/Signed-off-by:.*//g;s/    //g;/^$/d;' ${NEWCHANGES}
echo "" >> ${NEWCHANGES}
cat ${CHANGELOG} >> ${NEWCHANGES}
mv ${NEWCHANGES} ${CHANGELOG}
rm ${CHANGES}

LASTCOMMIT="$( git rev-parse HEAD )"

echo "VERSION=\"${NEWVERSION}+${SNAPSHOT}\"" > ${VERSION}
echo "COMMIT=\"${LASTCOMMIT}\"" >> ${VERSION}
echo "RELDATE=\"${DATE}\"" >> ${VERSION}

WARNING "Commiting changes ..."
git add .
git commit -q -a -m "New development snapshot ${NEWVERSION}+${SNAPSHOT}"
git tag ${NEWVERSION}+${SNAPSHOT} -m "New development snapshot ${NEWVERSION}+${SNAPSHOT}"

WARNING "Creating tarball ..."
tar -czf ../canaima-instalador_${NEWVERSION}+${SNAPSHOT}.orig.tar.gz *

SUCCESS "Snapshot Created"
