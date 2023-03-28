#include "mol.h"
/*********************************

CIS 2750 
Assignment 2
Elman Islam
Student ID : 1126272

Note: I have a 'FILE' environment variable which can be
set to a .c file to quickly run it (e.g. set 
"FILE = test1" to run the test1.c file)

Questions
Are we expected to test for invalid inputs?

*********************************/


void atomset( atom *atom, char element[3], double *x, double *y, double *z ) {

  strcpy(atom->element, element);
  atom->x = *x;
  atom->y = *y;
  atom->z = *z;

}

void atomget( atom *atom, char element[3], double *x, double *y, double *z ) {

  strcpy(element, atom->element);
  *x = atom->x;
  *y = atom->y;
  *z = atom->z;

}

void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom**atoms, unsigned char *epairs ) {
  bond->a1 = *a1;
  bond->a2 = *a2;
  bond->atoms = *atoms;
  bond->epairs = *epairs;
  compute_coords(bond);
}

void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom**atoms, unsigned char *epairs ) {

  *a1 = bond->a1;
  *a2 = bond->a2;
  *atoms = bond->atoms;
  *epairs = bond->epairs;
}

void compute_coords( bond *bond ) {


  bond->x1 = bond->atoms[bond->a1].x;
  bond->x2 = bond->atoms[bond->a2].x;

  bond->y1 = bond->atoms[bond->a1].y;
  bond->y2 = bond->atoms[bond->a2].y;

  bond->z = bond->atoms[bond->a1].z + bond->atoms[bond->a2].z;
  bond->z = bond->z / 2;
  
  bond->dx = (bond->x2 - bond->x1) ;
  bond->dy = (bond->y2 - bond->y1) ;

  bond->len = sqrt((bond->dx * bond->dx) + (bond->dy * bond->dy));

  bond->dx /= bond->len;
  bond->dy /= bond->len;



}


molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ) {

  // create a molecule pointer, allocate appropriate memory and initialize 'max' and 'no'
  molecule * tempMol = NULL;
  tempMol = malloc(sizeof( molecule));

  tempMol->atom_max = atom_max;
  tempMol->atom_no = 0;

  tempMol->atoms = malloc(sizeof(struct atom) * atom_max);
  tempMol->atom_ptrs = malloc(sizeof(struct atom) * atom_max);

  tempMol->bond_max = bond_max;
  tempMol->bond_no = 0;

  tempMol->bonds = malloc(sizeof(struct bond) * bond_max);
  tempMol->bond_ptrs = malloc(sizeof(struct bond) * bond_max);


  return tempMol;
}

molecule *molcopy( molecule *src ) {


  molecule * tempMol;

  tempMol = molmalloc(src->atom_max, src->bond_max);

  // loop through atoms array and append each one
  for (int i = 0; i < src->atom_no; i++)
    molappend_atom(tempMol, &(src->atoms[i]));

  // loop through bonds array and append each one
  for (int i = 0; i < src->bond_no; i++)
    molappend_bond(tempMol, &(src->bonds[i]));

  return tempMol;
}

void molfree( molecule *ptr ) {
  
  free(ptr->atom_ptrs);
  free(ptr->atoms);
  free(ptr->bond_ptrs);
  free(ptr->bonds);
  free(ptr);

}

void molappend_atom( molecule *molecule, atom *atom ) {

  int isMalloc = 0; // boolean variable for determining if a malloc has occurred
  if ((molecule->atom_max == 0) || (molecule->atom_no >= molecule->atom_max))
  {
    if (molecule->atom_max == 0)
      molecule->atom_max = 1;
    else // atom has reached maximum size, realloc to make it two times bigger
      molecule->atom_max = molecule->atom_max * 2;

    molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
    molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom) * molecule->atom_max);
    isMalloc = 1;
  }

  atomset( &(molecule->atoms[molecule->atom_no]), atom->element, &(atom->x), &(atom->y), &(atom->z) );

  if (isMalloc == 1) //if memory has been allocated or reallocated, set atom_ptr array to newly allocated atoms array
  {
    for (int i = 0; i <= molecule->atom_no; i++) // i <= molecules->atom_no instead of '<' because atom_no will be incremented
      molecule->atom_ptrs[i] = &(molecule->atoms[i]);

  } else
      molecule->atom_ptrs[molecule->atom_no] = &(molecule->atoms[molecule->atom_no]);

  molecule->atom_no++;

}

void molappend_bond( molecule *molecule, bond *bond ) {

  int isMalloc = 0; // boolean variable for determining if a malloc has occurred
  if ((molecule->bond_max == 0) || (molecule->bond_no >= molecule->bond_max))
  {
    if (molecule->bond_max == 0)
      molecule->bond_max = 1;
    else // bond has reached maximum size, realloc to make it two times bigger
      molecule->bond_max = molecule->bond_max * 2;

    molecule->bonds = realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
    molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond) * molecule->bond_max);
    isMalloc = 1;
  }

  bondset( &(molecule->bonds[molecule->bond_no]), &bond->a1, &bond->a2, &bond->atoms, &bond->epairs );

  if (isMalloc == 1) //if memory has been allocated or reallocated, set bond_ptr array to newly allocated bonds array
  {
    for (int i = 0; i <= molecule->bond_no; i++) // i <= molecules->bond_no instead of '<' because bond_no will be incremented
      molecule->bond_ptrs[i] = &(molecule->bonds[i]);

  } else
      molecule->bond_ptrs[molecule->bond_no] = &(molecule->bonds[molecule->bond_no]);

  molecule->bond_no++;

}

void molsort( molecule *molecule ) {

  // see helper functions at end of file for the compare functions
  qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom*), compareAtoms);
  qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond*), bond_comp);

}

// the matrices used for x, y, and z rotation were borrowed from the matrix rotation wikipedia page
void xrotation( xform_matrix xform_matrix, unsigned short deg ) {

  double rad = deg * (3.14159265358979323846 / 180.0); // convert the deg input to radians
  double temp_matrix[3][3] = { {1, 0, 0}, {0, cos(rad), -sin(rad)}, {0, sin(rad), cos(rad)} };

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      xform_matrix[i][j] = temp_matrix[i][j];
    }
  }
}

void yrotation( xform_matrix xform_matrix, unsigned short deg ) {

  double rad = deg * (3.14159265358979323846 / 180.0);
  double temp_matrix[3][3] = { {cos(rad), 0, sin(rad)}, {0, 1, 0}, {-sin(rad), 0, cos(rad)} };

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      xform_matrix[i][j] = temp_matrix[i][j];
    }
  }
}

void zrotation( xform_matrix xform_matrix, unsigned short deg ) {

  double rad = deg * (3.14159265358979323846 / 180.0);
  double temp_matrix[3][3] = { {cos(rad), -sin(rad), 0}, {sin(rad), cos(rad), 0}, {0, 0, 1} };

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      xform_matrix[i][j] = temp_matrix[i][j];
    }
  }
}

void mol_xform( molecule *molecule, xform_matrix matrix ) {

  for (int i = 0; i < molecule->atom_no; i++)
  {
    double x, y, z;
    x = molecule->atoms[i].x * matrix[0][0] + molecule->atoms[i].y * matrix[0][1] + molecule->atoms[i].z * matrix[0][2];
    y = molecule->atoms[i].x * matrix[1][0] + molecule->atoms[i].y * matrix[1][1] + molecule->atoms[i].z * matrix[1][2];
    z = molecule->atoms[i].x * matrix[2][0] + molecule->atoms[i].y * matrix[2][1] + molecule->atoms[i].z * matrix[2][2];  
    molecule->atoms[i].x = x;
    molecule->atoms[i].y = y;
    molecule->atoms[i].z = z;
  }

  for (int i = 0; i < molecule->bond_no; i++)
  {
    compute_coords(&molecule->bonds[i]);
  }
}

/* HELPER FUNCTIONS */

int compareAtoms(const void * a, const void * b) {

 
  struct atom **a_ptr, **b_ptr;

  a_ptr = (struct atom**) a;
  b_ptr = (struct atom**) b;
  
  return ((*a_ptr)->z - (*b_ptr)->z); 

}

int bond_comp(const void * a, const void * b) {


  struct bond **a_ptr, **b_ptr;
  a_ptr = (struct bond**) a;
  b_ptr = (struct bond**) b;

  double z1 = (*a_ptr)->z;
  double z2 = (*b_ptr)->z;

  return (z1 - z2); 
  
}

