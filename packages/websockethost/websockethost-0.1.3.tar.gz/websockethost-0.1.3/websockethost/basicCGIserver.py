import http.server as server
import socketserver

def startCGIserver(port: int, host: str):
    adress = (host, port)

    handler = server.CGIHTTPRequestHandler
    httpR = socketserver.TCPServer(adress, handler)

    print('Serveur démmaré CTRL + C pour arrété le serveur...')
    try:
        httpR.serve_forever()
    except KeyboardInterrupt:
        print('Serveur CGI arréter...')
