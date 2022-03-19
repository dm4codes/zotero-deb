#!/usr/bin/env python3

import sys
from util import run

baseurl = 'https://zotero.retorque.re/file/apt-package-archive'
url = sys.argv[1]

with open('README.md') as f:
  lines = f.readlines()
  readme = ''
  replace = False
  for line in lines:
    replace = replace or line.startswith('----')
    if replace:
      line = line.replace(baseurl, url)
    readme += line
with open('index.md', 'w') as f:
  f.write(readme)
run('pandoc index.md -s --css pandoc.css -o index.html')

with open('install.sh', 'w') as f:
  f.write(f"""
# https://wiki.debian.org/DebianRepository/UseThirdParty

case `uname -m` in
  "i386" | "i686" | "x86_64")
    ;;
  *)
    echo "Zotero is only available for architectures i686 and x86_64"
    exit
    ;;
esac

export GNUPGHOME="/dev/null"

KEYNAME=zotero-archive-keyring.gpg
GPGKEY=https://raw.githubusercontent.com/retorquere/zotero-deb/master/$KEYNAME
KEYRING=/usr/share/keyrings/$KEYNAME
if [ -x "$(command -v curl)" ]; then
  sudo curl -L $GPGKEY -o $KEYRING
elif [ -x "$(command -v wget)" ]; then
  sudo wget -O $KEYRING $GPGKEY
else
  echo "Error: need wget or curl installed." >&2
  exit 1
fi

sudo chmod 644 $KEYRING
# old key with too broad reach
sudo rm -f /etc/apt/trusted.gpg.d/zotero.gpg

cat << EOF | sudo tee /etc/apt/sources.list.d/zotero.list
deb [signed-by=$KEYRING by-hash=force] {url} ./
EOF

sudo apt-get clean
""")
