#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler
import re
import os.path

# headers
H_STA_MAC = 'X_ESP8266_STA_MAC'
H_AP_MAC = 'X_ESP8266_AP_MAC'
H_FREE_SPACE = 'X_ESP8266_FREE_SPACE'
H_SKETCH_SIZE = 'X_ESP8266_SKETCH_SIZE'
H_CHIP_SIZE = 'X_ESP8266_CHIP_SIZE'
H_SDK_VERSION  = 'X_ESP8266_SDK_VERSION'
H_VERSION = 'X_ESP8266_VERSION'

REQUIRED_HEADERS = [H_STA_MAC, H_AP_MAC, H_FREE_SPACE, H_SKETCH_SIZE, H_CHIP_SIZE, H_SDK_VERSION, H_VERSION]


class ESP8266ImageDirectory(object):

    def __init__(self, directory):
        self.directory = directory

    def get_path(node_name, version):
        raise NotImplementedError

# package-level instance - not sure i can override the ctor in ESP8266UpdateHandler
image_dir = ESP8266ImageDirectory('/foo/var/')

class ESP8266UpdateHandler(BaseHTTPRequestHandler):

    @classmethod
    def _validate_headers(cls):
        for header in REQUIRED_HEADERS:
            if header not in self.headers:
                self.send_response('403', 'ESP8266 updater only - you are missing %s' % header)
                self.end_headers()
                return false
        return true

    def client_current_version(self):
        return self.headers[H_VERSION]

    def do_GET(self):
        if not self._validate_headers():
            return
        path_re = re.compile(ur'/(P<node_name)\w\.bin')
        path_match = path_re.match(self.path)
        if not path_match:
            self.send_response('404')
            return
        node_name = path_match.group('node_name')
        (bin_path, md5sum) = image_dir.get_path(node_name, self.client_current_version)
        if not bin_path:
            # no update found!
            self.send_response(304)
            return
        self.send_response(200)
        self.send_header('Content-Type', 'application/octet-stream')
        self.send_header('Content-Disposition', 'attachment; filename=%s' % os.path.basename(bin_path))
        self.send_header('X-MD5', md5sum)
        self.send_header('Content-Length', os.path.getsize(bin_path))
        self.end_headers()
        with open(bin_path) as bin_fh:
            self.wfile.write(bin_fh.read())
        return
