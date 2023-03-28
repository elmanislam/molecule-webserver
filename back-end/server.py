import sys;
from http.server import HTTPServer, BaseHTTPRequestHandler;
import MolDisplay 
from urllib.parse import urlparse
home_page = """
<html>
  <head>
    <title> File Upload </title>
  </head>
  <body>
    <h1> File Upload </h1>
    <form action="molecule" enctype="multipart/form-data" method="post">
      <p>
        <input type="file" id="sdf_file" name="filename"/>
      </p>
      <p>
        <input type="submit" value="Upload"/>
      </p>
    </form>
  </body>
</html>
""";




class MyHandler( BaseHTTPRequestHandler ):
  def do_GET(self):
    if self.path == "/":
      self.send_response( 200 ); # OK
      self.send_header( "Content-type", "text/html" );
      self.send_header( "Content-length", len(home_page) );
      self.end_headers();

      self.wfile.write( bytes( home_page, "utf-8" ) );

    else:
      self.send_response( 404 );
      self.end_headers();
      self.wfile.write( bytes( "404: not found", "utf-8" ) );

  def do_POST(self):

    parsed_path = urlparse(self.path)

    if self.path == "/molecule":
      content_length = int(self.headers['Content-Length'])

      molecule = MolDisplay.Molecule()
  
      molecule.parse(self.rfile, content_length);
      molecule.sort()
      rfile = molecule.svg()
      self.send_response(200)
      self.send_header('Content-type', 'image/svg+xml')
      self.end_headers()
      self.wfile.write(rfile.encode('utf-8'))

      # self.send_header( "Content-length", content_length );



    else:
      self.send_response( 404 );
      self.end_headers();
      self.wfile.write( bytes( "404: not found", "utf-8" ) );


httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler ); 
httpd.serve_forever();