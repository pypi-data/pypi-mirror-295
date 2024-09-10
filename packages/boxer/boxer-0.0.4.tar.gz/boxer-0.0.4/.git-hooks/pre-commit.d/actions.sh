# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: CC0-1.0

set -e

if command -v forgejo-actions >/dev/null ; then
	forgejo-actions exec
else
    >&2 echo "Unable to find forgejo-actions binary"
fi
