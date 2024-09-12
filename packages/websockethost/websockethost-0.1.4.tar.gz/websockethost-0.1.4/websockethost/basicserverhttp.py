import http.server as server
import socketserver
import threading 

def start_server_http(port: int, host: str):
    adress = (host, port)

    handler = server.SimpleHTTPRequestHandler
    httpR = socketserver.TCPServer(adress, handler)
    
    try:        
        print('Server lancer CTRL + C pour arreté le serveur...')
        httpR.serve_forever()
    except KeyboardInterrupt:
        print('Serveur arrété...')