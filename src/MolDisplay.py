from .molecule import molecule;
radius = {};
element_name = {};
header = """<svg version="1.1" width="1000" height="1000"
 xmlns="http://www.w3.org/2000/svg">""";
footer = """</svg>""";

offsetx = 500;
offsety = 500;


class Atom:
  def __init__(self, c_atom):
    self.atom = c_atom;
    self.z = c_atom.z;
  
  def __str__(self):
    return self.atom.element + " " + str(self.atom.x) + " " + str(self.atom.y) + " " + str(self.z);
  
  def svg(self):
    # calculate the center of the circle's x and y coordinates (cx and cy)
    cx = self.atom.x * 100 + offsetx; 
    cy = self.atom.y * 100 + offsety;

    r = radius[self.atom.element];
    fill = element_name[self.atom.element];
    return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (cx, cy, r, fill);

class Bond:

  def __init__(self, c_bond):
    self.bond = c_bond;
    self.z = c_bond.z;
  
  def __str__(self):
  
    return str(self.bond.a1) + " " + str(self.bond.a2) + " " + str(self.bond.epairs) + " " + str(self.bond.x1) + \
    " " + str(self.bond.y1) + " " + str(self.bond.x2) + " " + str(self.bond.y2) + " " + str(self.bond.len) + \
     " " + str(self.bond.dx) + " " + str(self.bond.dy) + " " + str(self.z); 
  
  def svg(self):
    
    #let 'T' represent a double array of 4 coordinates that will be the rectangle's corners
    T = [[self.bond.x1, self.bond.y1],  [self.bond.x1, self.bond.y1],  
         [self.bond.x2, self.bond.y2], [self.bond.x2, self.bond.y2]]
    
    for i in range(4):
      if i % 2 == 0:
        # if it is the first or third point, calculate the lower perpendicular
        # corner by adding the dx and dy values multiplied by 10
        T[i][0] = T[i][0] * 100 + offsetx - self.bond.dy * 10
        T[i][1] = T[i][1] * 100 + offsety - self.bond.dx * 10
      else:
        # if it is the second or fourth point, calculate the upper perpendicular
        # corner by subtracting the dx and dy values multiplied by 10
        T[i][0] = T[i][0] * 100 + offsetx + self.bond.dy * 10
        T[i][1] = T[i][1] * 100 + offsety + self.bond.dx * 10   
        
    return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' \
      % (T[0][0], T[1][1], T[1][0], T[0][1], T[3][0], T[2][1], T[2][0], T[3][1]); 

class Molecule(molecule):

  def __str__(self):
    str = "";
    for i in range(self.atom_no):
      a1 = Atom(self.get_atom(i));
      str += " " + (a1.__str__());

  def svg(self):
    svg_string = header + "\n";
  
    atom_count = 0;
    bond_count = 0;
  
    count = 0;
    if self.atom_no > self.bond_no:
      max = self.bond_no;

    else:
      max = self.atom_no;
  
    while atom_count or bond_count < max:
      count +=1;
      a1 = Atom(self.get_atom(atom_count));
      b1 = Bond(self.get_bond(bond_count));

      if a1.z < b1.z:
        svg_string += a1.svg();
        atom_count += 1;

      else: #b1.z <a1.z
        svg_string += b1.svg();
        bond_count += 1;
      
      if count == self.atom_no or count == self.bond_no:
        break;


    for i in range (atom_count, self.atom_no):
      a1 = Atom(self.get_atom(i));
      svg_string += a1.svg();


    for i in range (bond_count, self.bond_no):
      b1 = Bond(self.get_bond(i));
      svg_string += b1.svg();
  

    svg_string += footer;
    return svg_string;


  def parse(self, file_obj, content_length = 0):

    count = 3; # indicates the current line. Set at 3 to start on 4th line of the sdf file
    num_atoms = 0;
    num_bonds = 0;

    if content_length > 0:
      rfile_str = file_obj.read(content_length) 
      rfile_str = rfile_str.decode("utf-8").split("\r\n")[4:]  # Skip an extra 4 lines to ignore headers
      rfile_str = '\n'.join(rfile_str)
 
    else:
      rfile_str = file_obj.read();
 

    lines = rfile_str.split('\n'); 

    numbers = (lines[count].strip()).split(); #read the 4th line and find each number i-0we
    num_atoms = int(numbers[0]);
    num_bonds = int(numbers[1]);

    for i in range(num_atoms):
      count += 1;
      numbers = (lines[count].strip()).split();
      self.append_atom(str(numbers[3]), float(numbers[0]), float(numbers[1]), float(numbers[2]));
  
    for i in range(num_bonds):
      count += 1;

      numbers = (lines[count].strip()).split();
      self.append_bond(int(numbers[0]) - 1, int(numbers[1]) - 1, int(numbers[2]));


    file_obj.close()
    


