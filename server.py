#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler

# headers
H_STA_MAC = 'X_ESP8266_STA_MAC'
H_AP_MAC = 'X_ESP8266_AP_MAC'
H_FREE_SPACE = 'X_ESP8266_FREE_SPACE'
H_SKETCH_SIZE = 'X_ESP8266_SKETCH_SIZE'
H_CHIP_SIZE = 'X_ESP8266_CHIP_SIZE'
H_SDK_VERSION  = 'X_ESP8266_SDK_VERSION'
H_VERSION = 'X_ESP8266_VERSION'

REQUIRED_HEADERS = [H_STA_MAC, H_AP_MAC, H_FREE_SPACE, H_SKETCH_SIZE, H_CHIP_SIZE, H_SDK_VERSION, H_VERSION]

class ESP8266UpdateHandler(BaseHTTPRequestHandler):


    def _validate_headers():
        for header in REQUIRED_HEADERS:
            if header not in self.headers:
                self.send_response('403', 'ESP8266 updater only - you are missing %s' % header)
                self.end_headers()
                return false
        return true

    def do_GET():
        if not self._validate_headers():
            return



