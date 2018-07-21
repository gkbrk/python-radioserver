#!/usr/bin/env python3

# Copyright (C) 2018 Gokberk Yaltirakli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path
import hashlib
import subprocess

INPUT  = Path('/home/username/music/')
OUTPUT = Path('/home/username/radioserver/music/')

def hash_file(f):
    with open(f, 'rb') as f:
        sha1 = hashlib.sha1(f.read()).hexdigest()
        return sha1

def encode_mp3(f):
    name = hash_file(f) + '.mp3'
    out_name = OUTPUT / name

    subprocess.run(['ffmpeg', '-y', '-i', f, '-map', '0:a', '-codec:a', 'libmp3lame', '-qscale:a', '9', out_name])

if __name__ == '__main__':
    for music in INPUT.glob('*.*'):
        encode_mp3(music)
