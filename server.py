import sys;
import os;
from http.server import HTTPServer, BaseHTTPRequestHandler;
from src import MolDisplay;
from src import molecule;
from src import molsql;
import cgi;
import json;

## GLOBAL CONSTANT VARIABLES ##

PORT = 8000; # main port host server on; default port is 8000
PATH = os.path.realpath(__file__); # path to current file
DIR = os.path.dirname(PATH); # name of current directory
HTML = DIR + "/templates";



class MyHandler( BaseHTTPRequestHandler ):

  db = molsql.Database(reset=True); # Create a database attribute for the server
  db.create_tables(); # also set up tables

  pages = [ '/index.html', '/add-molecule.html', '/add-element.html', '/remove-element.html', '/view-molecule.html', '/display.html'];
  # all web pages
  
  def do_GET(self):
    if self.path == "/":
      fp = open(HTML + "/index.html");
      main_page = fp.read();

      self.send_response( 200 ); # OK
      self.send_header( "Content-type", "text/html" );
      self.send_header( "Content-length", len(main_page) );
      self.end_headers();

      self.wfile.write( bytes( main_page, "utf-8" ) );

    elif self.path in self.pages:   # make sure it's a valid file

            fp = open(HTML + self.path); 

            # load the specified file
            web_page = fp.read();
            fp.close();

            if self.path == '/remove-element.html':
              
              table = self.db.conn.execute( "SELECT * FROM Elements;" ).fetchall() ;
              html_content = ""
              for entry in table:
                html_content += f"<tr name={entry[1]} class='element-entry'>"
                for i in entry:
                    if len(str(i)) == 6 and i != entry[2]:
                      html_content += f"<td style='font-weight: 900; color:#{i}'>#{i}</td>"
                    else:
                      html_content += f"<td>{i}</td>"

                html_content += "</tr>"
              web_page = web_page.replace("</table>", html_content + "</table>");
  
            elif self.path == '/view-molecule.html':

              table = self.db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() ;
              html_content = ""
              for entry in table:
                tempMol = self.db.load_mol(entry[1]);
                self.db.update_database();

                html_content += f"<tr name={entry[1]} class='molecule-entry'>"

                for i in entry:
                   html_content += f"<td>{i}</td>"

                html_content += f"<td>{tempMol.atom_no}</td><td>{tempMol.bond_no}</td>"
                html_content += "</tr>"
              web_page = web_page.replace("</table>", html_content + "</table>");

           # elif self.path == '/display.html':
            
             # web_page = web_page.replace("<svg></svg>", );


            # create and send headers
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(web_page) );
            self.end_headers();

            self.wfile.write( bytes( web_page, "utf-8" ) );

            # send the contents

    elif self.path == '/script.js':


        # Open and read the contents of script.js
        with open(HTML + '/script.js', 'rb') as f:
            js_content = f.read()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/javascript')
        self.end_headers()
        # Write the JavaScript content to the response body
        self.wfile.write(js_content)


    elif self.path == '/style.css':


        # Open and read the contents of style.css
        with open(HTML + '/style.css', 'rb') as f:
            css_content = f.read()

        # Write the CSS content to the response body
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()    
        self.wfile.write(css_content)

    else:
      self.send_response( 404 );
      self.end_headers();
      self.wfile.write( bytes( "404: not found", "utf-8" ) );
  


  def do_POST(self):

      if self.path == '/upload-element':

        alert_element_success = '''
        <script>
          $(document).ready(function(){
            alert('Sucessfully submitted element');
          });
        </script>
        '''

        # this is specific to 'multipart/form-data' encoding used by POST
        content_type = self.headers.get('Content-Type')
        content_length = int(self.headers['Content-Length']);
      
        boundary = content_type.split('; ')[1].split('=')[1].encode()
              
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': content_type}
        )

        form_data = {}
        for field in form.keys():
                field_item = form[field]
                if field_item.filename:
                    # This is a file field
                    file_data = field_item.file.read()
                    form_data[field] = {'filename': field_item.filename, 'data': file_data}
                else:
                    # This is a regular field
                    form_data[field] = field_item.value

        id = form_data.get('input-id')
        symbol = form_data.get('input-symbol')
        element = form_data.get('input-element')
        colour1 = form_data.get('input-color-1')
        colour2 = form_data.get('input-color-2')
        colour3 = form_data.get('input-color-3') 
        radius = form_data.get('input-radius')       

        temp_dict = self.db.element_name()
        if (temp_dict): # if the dictionary is not empty
            if symbol in temp_dict: # if the element already exists 
                self.db.conn.execute(f" DELETE FROM Elements WHERE ELEMENT_CODE='{symbol}';") # delete the element
                alert_element_success = alert_element_success.replace("submitted", "updated"); # change message to "updated"
          
        colour1 = str(colour1).replace('#', '').upper();
        colour2 = str(colour2).replace('#', '').upper();
        colour3 = str(colour3).replace('#', '').upper();

        self.db['Elements'] = ( id, symbol, element, colour1, colour2, colour3, radius); # add or update the element

        fp = open(HTML  + '/index.html'); 
        web_page = fp.read();
        fp.close();

        alert_element_success = alert_element_success.replace('element', 'element ' + str(element))
        
        web_page = web_page.replace(
            '<body>',
            '<body>' + alert_element_success 
        )

        # create and send headers
        self.send_response( 200 );  # OK
        self.send_header( "Content-type", "text/html" );
        self.send_header( "Content-length", len(web_page) );

        self.end_headers();
        self.wfile.write( bytes( web_page, "utf-8" ) );         


      elif self.path == '/delete-element':
            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            deleteElement = str(repr( body.decode('utf-8') ))

            self.db.conn.execute(f" DELETE FROM Elements WHERE ELEMENT_CODE={deleteElement};")



      elif self.path == '/upload-sdf':
            # Get the content type and length
            content_type = self.headers['Content-Type']
            content_length = int(self.headers['Content-Length'])

            # Parse the form data
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
               
            file_field = form_data['file']
            molecule_name = form_data.getvalue('input-element');

            file_name = file_field.filename
            file_data = file_field.file.read()

            web_fp = open(HTML  + '/add-molecule.html'); 
            web_page = web_fp.read();
            web_fp.close();

            # check if the molecule name already exists
            molecule_exists = self.db.conn.execute(f" SELECT NAME FROM Molecules WHERE Molecules.NAME='{molecule_name}'").fetchone();

            alert_message = ""
            if molecule_exists != None: # The molecule already exists

                alert_message =  "<script>alert('The molecule already exists')</script>"          
                alert_message = alert_message.replace('molecule', 'molecule ' + str(molecule_name))

            else: # The molecule is new; add it to the table
                alert_message = "<script>alert('Successfully uploaded the sdf file')</script>"
                fp = open(DIR + '/temp_output_file.txt', 'wb')
                fp.write(file_data)
                fp.close();

                fp = open(DIR + "/temp_output_file.txt");

                isValid = self.db.add_molecule(molecule_name, fp); # check if the sdf is valid
                if (isValid == False): # send error message if it is invalid
                  alert_message =  "<script>alert('The uploaded file is an invalid SDF')</script>"          

                else: # otherwise it will be added to the database; update the database
                  self.db.update_database();

                os.remove(DIR + "/temp_output_file.txt") # Delete the temporary file after obtaining information

            web_page = web_page.replace('</body>', alert_message + '</body>')
            # Send a response
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(web_page) );

            self.end_headers();
            self.wfile.write( bytes( web_page, "utf-8" ) );     


      elif self.path == '/display-molecule':
          content_length = int(self.headers['Content-Length']);
          body = self.rfile.read(content_length);

          molecule_name = str(repr( body.decode('utf-8') ))

          molecule_name = molecule_name.strip("\'");

          web_fp = open(HTML  + '/display.html'); 
          web_page = web_fp.read();
          web_fp.close();

          mol = self.db.load_mol(molecule_name);
          self.db.update_database();

          web_page = web_page.replace('id="molecule-name">', f'name="{molecule_name}" id="molecule-name">' + molecule_name);
          web_page = web_page.replace("<svg></svg>", mol.svg());
          alert_message =  "<script>alert('The molecule already exists')</script>"       
          web_page = web_page.replace("</body>", alert_message + "</body>");
   
          self.send_response( 200 );  # OK
          self.send_header( "Content-type", "text/html" );
          self.send_header( "Content-length", len(web_page) );

          self.end_headers();
          self.wfile.write( bytes( web_page, "utf-8" ) );     


      elif self.path == '/display-rotate':
          content_length = int(self.headers['Content-Length']);
          body = self.rfile.read(content_length);

          string_data = str(repr( body.decode('utf-8') )).replace("\'", "");
          rotation_data = string_data.split('&');

          molecule_name = rotation_data[0].split('=');
          molecule_name = molecule_name[1];
          degrees = rotation_data[1].split('=');
          degrees = int(degrees[1]);
          dimension =  rotation_data[2].split('=');
          dimension = dimension[1];

          tempMol = self.db.load_mol(molecule_name);
          self.db.update_database();

          mx = molecule.mx_wrapper(0,0,0);

          if (dimension == 'X'):
            mx = molecule.mx_wrapper(degrees,0,0);
          elif (dimension == 'Y'):
            mx = molecule.mx_wrapper(0,degrees,0);
          elif (dimension == 'Z'):
            mx = molecule.mx_wrapper(0,0,degrees);



          tempMol.xform( mx.xform_matrix );


          new_svg = tempMol.svg();

          self.send_response( 200 );  # OK
          self.send_header( "Content-type", "text/html" );
          self.send_header( "Content-length", len(new_svg) );

          self.end_headers();
          self.wfile.write( bytes( new_svg, "utf-8" ) );     


if __name__ == '__main__':
    
    local_port = PORT;

    if len(sys.argv) > 1:
        local_port = int(sys.argv[1])

    server_address = ('localhost', local_port);

    httpd = HTTPServer(server_address, MyHandler)
    print(f'Server running on http://localhost:{local_port}')
    httpd.serve_forever()