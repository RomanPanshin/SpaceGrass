import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from SpaceGrass import main
from DB_controller import insert_data_into_database

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        if parsed_url.path == '/':
            self.send_response(302)
            self.send_header('Location', '/data/?Fly_Dist=30&SP_ForClient=120')
            self.end_headers()
            return
        
        elif parsed_url.path == '/data/':
            self.send_response(200)

            if 'Fly_Dist' in query_params and 'SP_ForClient' in query_params:
                Fly_Dist = int(query_params['Fly_Dist'][0])
                sp_for_client = int(query_params['SP_ForClient'][0])
                with open('index.html', 'r') as f:
                    html = f.read()
                AllFuel, All_Oxi, All_cost, day = main(int(Fly_Dist), int(sp_for_client))
                
                html = html.replace('{fly-dist}', str(Fly_Dist))
                html = html.replace('{sp-for-client}', str(sp_for_client))
                html = html.replace('{AllFuel}', str(AllFuel))
                html = html.replace('{All_Oxi}', str(All_Oxi))
                html = html.replace('{All_cost}', str(All_cost))
                html = html.replace('{day_grow_var+day_no_grow_var}', str(day))
                
                
                #Расскоментить если у вас есть БД
                #insert_data_into_database(AllFuel, All_Oxi, All_cost, day, Fly_Dist, sp_for_client)
                
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(html, 'utf-8'))
            else:
                self.send_error(400, 'Invalid query parameters')
        
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()

