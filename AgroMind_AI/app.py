"""Local web application: python app.py, then http://localhost:8000."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from model import KNN, load_rows, recommend
ROOT=Path(__file__).resolve().parent
MODEL=KNN(load_rows())

class Handler(BaseHTTPRequestHandler):
    def respond(self,status,data,kind='application/json'):
        body=json.dumps(data,allow_nan=False).encode() if kind=='application/json' else data
        self.send_response(status)
        self.send_header('Content-Type',kind+'; charset=utf-8')
        self.send_header('Content-Length',str(len(body)))
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path=urlsplit(self.path).path
        if path=='/api/health':
            return self.respond(200,{'status':'ok','samples':len(MODEL.rows),'crops':len(MODEL.profiles),'model':'weighted k-NN'})
        routes={'/':('static/index.html','text/html'),'/style.css':('static/style.css','text/css'),'/app.js':('static/app.js','text/javascript')}
        if path not in routes:
            return self.respond(404,{'error':'Not found'})
        file,kind=routes[path]
        self.respond(200,(ROOT/file).read_bytes(),kind)

    def do_POST(self):
        if urlsplit(self.path).path!='/api/recommend':
            return self.respond(404,{'error':'Not found'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=8192:
                return self.respond(413,{'error':'Request must contain 1–8192 bytes.'})
            data=json.loads(self.rfile.read(size))
            self.respond(200,recommend(MODEL,data))
        except (ValueError,UnicodeDecodeError) as exc:
            self.respond(400,{'error':str(exc)})

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=8000)
    args=parser.parse_args()
    print(f'AgroMind AI • Open http://localhost:{args.port} • Ctrl+C to stop',flush=True)
    try:
        ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
