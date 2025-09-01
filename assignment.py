import urllib.request ## I have used to get DATA from API
import json           ## I have used this to parse JSON objects. Both of them are internal libraries
import http.server    ## This have been used to handle WEB requests
import socketserver   ## This is the server used to make Connection
url = "https://api.time.com/graphql"
query='''query FeaturesData {
    featuresData {
        features {
            redirect_URL
            title
            
        }
    }
}
'''
store={'query':query}
data=json.dumps(store).encode('utf-8')
headers={'Content-Type':'application/json'}

req=urllib.request.Request(url,data=data,headers=headers,method="POST")

with urllib.request.urlopen(req) as response:
    body=response.read()
    text=body.decode('utf-8')
    info=json.loads(text)

data_1=info['data']['featuresData']['features']
data_1=data_1[:6]
for index,i in enumerate(data_1):
    i['link']=i.pop('redirect_URL')
    i['link']='https://time.com/'+i.get('link')
   

final_data=json.dumps(data_1,indent=4)
PORT = 8000


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getTimeStories':
    
            self.send_response(200)
            
            
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            
            self.wfile.write(final_data.encode('utf-8'))
        else:
            self.send_error(404, "Not Found")


with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Server started at localhost:8000")
    print("Serving JSON on http://localhost:8000/getTimeStories")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")
    
