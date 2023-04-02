from . import MolDisplay;
import sqlite3;

import os;


DEFAULT_ELEMENTS = {
  'H': ( 1, 'Hydrogen', 'FFFFFF', '050505', '020202', 25 ),
  'C': ( 6, 'Carbon', '808080', '010101', '000000', 40 ),
  'N': ( 7, 'Nitrogen', '0000FF', '000005', '000002', 40 ),
  'O': ( 8, 'Oxygen', 'FF0000', '050000', '020000', 40 )
}

class Database():

  def __init__(self, reset=False ):

    if (reset == True): #only remove the file if it exists in local directory
    
      if os.path.isfile("molecule.db") == True:
        os.remove("molecule.db");


    self.conn = sqlite3.connect( "molecule.db"); #make database connection to a file


  def create_tables(self):

    cur = self.conn.cursor();

    # Create Elements table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Elements(
        
          ELEMENT_NO INTEGER NOT NULL,
          ELEMENT_CODE VARCHAR(3) PRIMARY KEY NOT NULL,
          ELEMENT_NAME VARCHAR(32) NOT NULL,
          COLOUR1 CHAR(6) NOT NULL,
          COLOUR2 CHAR(6) NOT NULL,
          COLOUR3 CHAR(6) NOT NULL,
          RADIUS DECIMAL(3) NOT NULL
        )
    """)
    # Create Atoms table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Atoms (
        
          ATOM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          ELEMENT_CODE VARCHAR(3) NOT NULL,
          X DECIMAL(7,4) NOT NULL,
          Y DECIMAL(7,4) NOT NULL,
          Z DECIMAL(7,4) NOT NULL,
          FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements
        )
    """)

    # Create Bonds table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Bonds (
        
          BOND_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          A1 INTEGER NOT NULL,
          A2 INTEGER NOT NULL,
          EPAIRS INTEGER NOT NULL
        )
    """)

    # Create Molecules table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Molecules (
        
          MOLECULE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          NAME TEXT UNIQUE NOT NULL
        )
    """)

    # Create MoleculeAtom table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS MoleculeAtom (
        
          MOLECULE_ID INTEGER NOT NULL,
          ATOM_ID INTEGER  NOT NULL REFERENCES Atoms(ATOM_ID),
          PRIMARY KEY(MOLECULE_ID, ATOM_ID)
          FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
          FOREIGN KEY (ATOM_ID) REFERENCES Atoms
        )
    """)

    # Create MoleculeBond table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS MoleculeBond (
        
          MOLECULE_ID INTEGER NOT NULL,
          BOND_ID INTEGER NOT NULL,
          PRIMARY KEY(MOLECULE_ID, BOND_ID)
          FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
          FOREIGN KEY (BOND_ID) REFERENCES Bonds
        )
    """)



  def __setitem__( self, table, values ):

    # Create a string where the number of question marks is the length of 'values' - 1
    string ="";
    reg = "?, "
    for i in range (0, len(values) - 1):
      string += reg;
    
    # Insert into 'table' the 'values', where 'string' is a placeholder for each value
    self.conn.execute(f"INSERT INTO {table} VALUES({string}?)", values);


  def add_atom(self, molname, atom ):
    
    atom_data = (atom.element, atom.x, atom.y, atom.z);

    element_exists = self.conn.execute(f"SELECT ELEMENT_CODE FROM Elements WHERE Elements.ELEMENT_CODE='{atom.element}'").fetchone();

    if element_exists == None: # If the element does not exist, create default values for it
        if atom.element in DEFAULT_ELEMENTS.keys():
            t = DEFAULT_ELEMENTS.get(atom.element);
            self['Elements'] = (t[0], atom.element, t[1], t[2], t[3], t[4], t[5]);
          
        else:
            self['Elements'] =  (0, atom.element, 'Unnamed Element', 'FFFFFF', '969696', '000000', 40 );

    self.conn.execute("INSERT INTO Atoms(ELEMENT_CODE, X, Y, Z) VALUES(?, ?, ?, ?)", atom_data);
    id = self.conn.execute("SELECT last_insert_rowid()").fetchone(); # obtain the most recently created id from any table

    self.conn.execute("""
        INSERT INTO MoleculeAtom(MOLECULE_ID, ATOM_ID) VALUES (
        
          (SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?), ?)
    """, (molname, id[0] ));


  def add_bond(self, molname, bond ):
    
    bond_data = (bond.a1, bond.a2, bond.epairs);

    self.conn.execute("INSERT INTO Bonds(A1, A2, EPAIRS) VALUES(?, ?, ?)", bond_data);
    id = self.conn.execute("SELECT last_insert_rowid()").fetchone(); # obtain the most recently created id from any table

    self.conn.execute("""
        INSERT INTO MoleculeBond(MOLECULE_ID, BOND_ID) VALUES (
        
          (SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?), ?)
        
    """, (molname, id[0] ));


  def add_molecule(self, name, fp ):

    mol = MolDisplay.Molecule();
    mol.parse(fp);
   
    self.conn.execute("INSERT INTO Molecules(NAME) VALUES( ? )", (name,));

    # cycle through all atoms and bonds, and then add them

    for i in range (0, mol.atom_no):
      temp_atom = MolDisplay.Atom(mol.get_atom(i));
      self.add_atom(name, temp_atom.atom);

    for i in range (0, mol.bond_no):
      temp_bond = MolDisplay.Bond(mol.get_bond(i));
      self.add_bond(name, temp_bond.bond);

    self.conn.commit();
  

  def load_mol( self, name ):

    mol = MolDisplay.Molecule();

    # list containing arguments for Atoms

    atom_args = self.conn.execute(""" SELECT Atoms.ATOM_ID, Atoms.ELEMENT_CODE, Atoms.X, Atoms.Y, Atoms.Z
 
      FROM MoleculeAtom
      JOIN Atoms ON MoleculeAtom.ATOM_ID = Atoms.ATOM_ID
      JOIN Molecules ON MoleculeAtom.MOLECULE_ID = Molecules.MOLECULE_ID
      WHERE Molecules.NAME = ?
      ORDER BY Atoms.ATOM_ID ASC
      
    """, (name,)).fetchall(); 

    for i in atom_args:
      mol.append_atom(i[1], i[2], i[3], i[4]);

    bond_args = self.conn.execute(""" SELECT Bonds.BOND_ID, Bonds.A1, Bonds.A2, Bonds.EPAIRS
 
      FROM MoleculeBond
      JOIN Bonds ON MoleculeBond.BOND_ID = Bonds.BOND_ID
      JOIN Molecules ON MoleculeBond.MOLECULE_ID = Molecules.MOLECULE_ID
      WHERE Molecules.NAME = ?
      ORDER BY Bonds.BOND_ID ASC
      
    """, (name,)).fetchall(); 

    for i in bond_args:
      mol.append_bond(i[1], i[2], i[3]);

    return mol;


  def radius( self ):

    # extract each row from the Elements table and put the radius values in 'radius_dict'
    radius_data = self.conn.execute("SELECT ELEMENT_CODE, RADIUS FROM Elements").fetchall();
    radius_dict = {}; 

    for i in radius_data:
      radius_dict[i[0]] = i[1];
    
    return radius_dict;


  def element_name( self ):

    # extract each row from the Elements table and put the names in 'element_dict'
    element_data = self.conn.execute("SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements").fetchall();
    element_dict = {};
    for i in element_data:
      element_dict[i[0]] = i[1];
    
    return element_dict;


  def radial_gradients( self ):

    # template string for any element as a radial gradient
    radialGradientSVG = """
      <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
        <stop offset="0%%" stop-color="#%s"/>
        <stop offset="50%%" stop-color="#%s"/>
        <stop offset="100%%" stop-color="#%s"/>
      </radialGradient>""";

    gradient_str = ""; # main string to be returned

    colour_data = self.conn.execute("SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements").fetchall();
    for i in colour_data:
      gradient_str += radialGradientSVG % (str(i[0]),  str(i[1]),  str(i[2]),  str(i[3])); 

    return gradient_str;


  ## Helper function: resets radial gradients and update radius and element dicts
  def update_database( self ):

    MolDisplay.radius = self.radius();
    MolDisplay.element_name = self.element_name();
    MolDisplay.header = """<svg version="1.1" width="1000" height="1000"
 xmlns="http://www.w3.org/2000/svg">""";
    
    MolDisplay.header += self.radial_gradients();
