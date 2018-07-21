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

import socketserver
import time
import glob
import random
import mp3

class RadioHandler(socketserver.StreamRequestHandler):
    def handle(self):
        station = self.rfile.readline().split(b' ')[1]
        print('Connection from {}'.format(self.client_address[0]))
        print('They want to play {}'.format(station))

        self.wfile.write(b'HTTP/1.1 200 OK\r\nContent-Type: audio/mpeg\r\n\r\n')

        while True:
            music_files = list(glob.glob('music/*.mp3'))
            f = random.choice(music_files)
            with open(f, 'rb') as music_file:
                seconds = 0
                for i, (head, fram) in enumerate(mp3.frames(music_file)):
                    self.wfile.write(fram)
                    seconds += mp3.time(head)
                    t = mp3.time(head) * 0.95
                    time.sleep(t)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
                
if __name__ == '__main__':
    HOST, PORT = "0.0.0.0", 1234

    ThreadedTCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), RadioHandler)
    server.serve_forever()
