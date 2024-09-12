class atom:
    '''
    Representative  of an atom isth xyz coordinates

    Class variables
    ---------------

    atom_type (str): the atom type in the format of the atomic symbol
    
    x_val (float): cartesian x coordinate
    
    y_val (float): cartesian y coordinate
    
    z_val (float): cartesian z coordinate
    
    '''
    def __init__(self,atom_type : str, x_val : float, y_val : float, z_val : float) -> None:

        self.atom_type = atom_type
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val
        pass

    def change_atom_type(self,new_atom_type:str)-> None:
        self.atom_type = new_atom_type
        pass
    
    @classmethod
    def from_line(cls,line:str):
        '''formats a given line for the class

        Parameters
        ----------

        line (str): the line which contains atom parameters

        Returns
        -------

        The atom type
        '''
        line_list = line.strip(" \n").split()
        return cls(line_list[0],float(line_list[1]),float(line_list[2]),float(line_list[3]))


    def get_line(self) -> str:
        '''outputs the atom as a string

        Returns
        -------

        a formatted string of this atom following the format atom_type  x   y   z
        '''
        return f'{self.atom_type:5} { self.x_val:13} {self.y_val:13} {self.z_val:13}\n'

class molecule:
    def __init__(self,atom_list = None) -> None:
        self.atom_list = atom_list
        pass

    @classmethod
    def from_orca_xyz(cls,xyz_file:str):
        temp_atom_list = []
        with open(xyz_file,"r") as file:
            for line in file.readlines()[2:]:
                temp_atom_list.append(atom.from_line(line))
        return cls(temp_atom_list)

    def add_atom_from_line(self,line):
        self.atom_list.append(atom.from_line(line))

    def get_string(self):
        string_version = ""
        for i in self.atom_list:
            string_version = string_version + i.get_line()
        return string_version

class orca_file:
    '''an object to build orca input files.

    Class variables
    ---------------

    file_name (str): the name\path of the input file

    input_line (str): the input line associated with the orca input file

    charge (int): the charge of the system in the orca input file

    multiplicity (int): the spin multiplicity of the system in the orca input file

    atom_list (list[atom]): a lits of all of the atoms associated with the orca input line
    '''

    def __init__(self,file_name ="",input_line = "!",charge = 0,multiplicity = 1, atom_list = None) -> None:
        
        self.file_name = file_name
        self.input_line = input_line
        self.charge = charge
        self.multiplicity = multiplicity
        self.atom_list = atom_list
        pass
    
    def get_atom_list(current_index : int, file_list) -> int:
        ''' helper method to from_file that pulls the atom information from an already existing Orca Input File

        Parameters
        ----------
        
        current_index (int): the current index in a file that already exists

        file_list (list[str]): the orca input file in the format of a list where each line is a str in the list

        Returns
        -------

        atom_list (list[atom]): a list if atom objects from the input file
        current_index (int): the index where the atom list ends
        '''
        line = file_list[current_index]
        # A list for the atoms to be appended to.
        atom_list = molecule()
        # The Last line of the atom list is an astrsk so we continue this loop until we find that
        while "*" not in line:
            # Appending an atom object to the end lsit based on the current line.
            atom_list.add_atom_from_line(line)
            # Itterating to the next line in the list
            current_index = current_index+1
            line = file_list[current_index]
        return  atom_list , current_index

    @classmethod
    def from_file(cls,file_name:str):
        ''' factory method  to make an orca object from a Orca Input File

        Parameters
        ----------
        
        file_name (str): the name/path to a orca input file

        Returns
        -------

        an orca class object


        '''
        future_input_line = "!"
        # Gives the future file the same name as the inputed one.
        future_file_name = file_name
        # Tells if the charge and multiplicity have been found in the file yet.
        charge_mult_hit = False

        # Opens and formats the file into a list where each line in a string in a list file_list
        with open(file_name) as file:
            file_list = file.readlines()

        current_index = 0
        for index, line in enumerate(file_list):
            if index <= current_index:
                current_index = current_index + 1
            if "xyz" in line:
                # Recognizes the charge, mulitplicity, and xyz atom coordinate section
                current_index = current_index - 1
                future_charge = line.split()[2]
                future_multiplicity = line.split()[3]
                future_atom_list , current_index = cls.get_atom_list(current_index,file_list)
                current_index = current_index + 1
                charge_mult_hit = True
            if line[0] == "!":
                # recognizes the input lines by a  line starting with '!'
                future_input_line = future_input_line + line.strip("! \n")
                current_index = current_index + 1
        return cls(file_name=future_file_name , input_line=future_input_line , charge=future_charge , multiplicity=future_multiplicity , atom_list=future_atom_list )
    
    def make_file(self,comment = "") -> None:
        ''' writes the input file

        Parameters
        ----------

        comment (str): an optional comment at the begining of a file

        Returns
        -------

        None

        uses a formatted string to write a file from the orca object
        '''

        # Turns the atom list in to a string.
        atom_list_string = self.atom_list.get_string()
        
        file_string = f'''#{comment}
{self.input_line}

%maxcore 16384

%pal
   nprocs 1
end

* xyz {self.charge} {self.multiplicity}
{atom_list_string[:-1]}
*



'''
        
        with open(self.file_name,"w") as new_file:
            new_file.write(file_string)