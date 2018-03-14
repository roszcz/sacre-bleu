import BaseHTTPServer

def new_address_string(self):
    host, port = self.client_address[:2]
    return '%s (no getfqdn)' % host #used to call: socket.getfqdn(host)

BaseHTTPServer.BaseHTTPRequestHandler.address_string = new_address_string
import SimpleXMLRPCServer
from utils.realcam import PhotoTaker

srv = SimpleXMLRPCServer.SimpleXMLRPCServer(("0.0.0.0",6969))

srv.register_instance(PhotoTaker())
srv.serve_forever()
