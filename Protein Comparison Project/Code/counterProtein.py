###IMPORTS### 
from prody import *
import matplotlib.pyplot as plt
import pandas as pd
import collections
from collections import Counter 
###IMPORTS### 


###TBD### 
# TBD!!! remember that there are certain non normal residues and you need to account for this 
#
# Test all objectives and verify they correct
# See if there are any other things you can do with pdb data and any other things to do for counterProtein project  
# WORK on graphing the secondary structure percentage of proteins 
#       For this Im workingo on the fucntion 
###TBD### 


# globals 
standard_amino_acids = ["ala", "cys", "asp", "glu", "phe", "gly", "his", "ile", "lys", "leu", "met", "asn", "pro", "gln", "arg", "ser", "thr", "val", "trp", "tyr"]
standard_amino_acids.sort()



###RESIDUE GROUPS### 
# returns list of percent of each residue group in protein 
def count_residue_groups_protein(protein_id):
    # categories are: Positively charged, negatively charged, hydrophobic, polar uncharged, aromatic 
    # variables
    structure = parsePDB(protein_id)
    hv = structure.getHierView()
    list_amino_acids = []
    # different category lists
    pos_charged = []
    neg_charged = []
    polar_uncharged = []
    hydrophobic = []
    aromatic = []
    # iterating through
    for x in hv:
        for y in x:
            # only appends to list if not HOH and len of it is greater than 1, so this way DNA/RNA excluded 
            if str(y).count("HOH") == 0 and len(str(y).split(" ")[0]) >= 3:
                list_amino_acids.append(str(y).split(" ")[0].lower())
    # getting different categories 
    for x in list_amino_acids:
        # positively charged
        if x == "lys" or x == "arg" or x == "his":
            pos_charged.append(x)
        # negatively charged 
        elif x == "asp" or x == "glu":
            neg_charged.append(x)
        # polar uncharged
        elif x == "ser" or x == "thr" or x == "cys" or x == "met" or x == "asn" or x == "gln":
            polar_uncharged.append(x)
        # hydrophobic
        elif x == "gly" or x == "ala" or x == "val" or x == "leu" or x == "ile" or x == "pro":
            hydrophobic.append(x)
        # aromatic 
        elif x == "phe" or x == "tyr" or x == "trp":
            aromatic.append(x)
        # else is not residue 
        else:
            # printing of other objects in list 
            print("Not an Amino Acid Object in " + protein_id + " : ", x.upper())
    # num of residues and percent of residues per category lists 
    num_residues_per_category = [len(pos_charged), len(neg_charged), len(polar_uncharged), len(hydrophobic), len(aromatic)]
    percent_residues_per_category = [x / sum(num_residues_per_category) * 100 for x in num_residues_per_category]
    return percent_residues_per_category

# plots the percent of each residue group of 1 - 4 proteins 
def plot_residue_group_percents():
    print("1 - 4 proteins can be entered")
    # variables and input 
    dict_proteins_residues = {}
    xlabels_list = ["Positively Charged", "Negatively Charged", "Polar Uncharged", "Hydrophobic", "Aromatic"]
    proteins_inp = input("Enter protein(s) (seperate by comma): ")
    list_proteins = proteins_inp.split(", ")
    # making sure 4 or less proteins entered
    list_proteins = list_proteins[0:4]

    # plotting
    plt.rcParams["figure.figsize"] = (13, 7)
    # iterating for every protein
    for index, protein in enumerate(list_proteins):
        dict_proteins_residues[protein] = count_residue_groups_protein(protein)
    df = pd.DataFrame(dict_proteins_residues, index = xlabels_list)
    bar = df.plot(kind = 'bar')
    # labels and graph components 
    plt.xticks(rotation = 0, fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.xlabel("Residue Type", labelpad = 15, fontsize = 16)
    plt.ylabel("Percent of Residues", labelpad = 15, fontsize = 16)
    plt.title("Percent of Types of Residues In " + ", ".join(list_proteins), fontsize = 18)
    plt.legend()
    plt.show()


###INDIVIDUAL RESIDUES### 
# returns list of percent of each residue in protein 
def count_each_residue_protein(protein_id):
    # variables 
    structure = parsePDB(protein_id)
    hv = structure.getHierView()
    list_amino_acids = []
    # iterating through
    for x in hv:
        for y in x:
            y = str(y).lower()[0:3]
            # only appends to list if it is normal amino acid 
            if y in standard_amino_acids:
                list_amino_acids.append(str(y).split(" ")[0].upper())
    # making list to return
    collections_amino_acids = collections.OrderedDict(Counter(list_amino_acids).items())
    for x in standard_amino_acids:
        if x.upper() not in collections_amino_acids.keys():
            collections_amino_acids[x.upper()] = 0
    # sorts the collection
    collections_amino_acids = collections.OrderedDict(sorted(collections_amino_acids.items()))
    # returns a list of all the different counted values for each amino acid in order 
    return [x / sum(list(collections_amino_acids.values())) * 100 for x in list(collections_amino_acids.values())]

# plots the percent of each residue of 1 - 2 proteins 
def plot_each_residue_percents():
    print("1 - 2 proteins can be entered")
    # variables and input 
    dict_proteins_residues = {}
    xlabels_list = [x.upper() for x in standard_amino_acids]
    proteins_inp = input("Enter protein(s) (separate by comma): ")
    list_proteins = proteins_inp.split(", ")
    # making sure 2 or less proteins entered
    list_proteins = list_proteins[0:2]
    # plotting
    plt.rcParams["figure.figsize"] = (13, 7)
    for index, protein in enumerate(list_proteins):
        dict_proteins_residues[protein] = count_each_residue_protein(protein)
    df = pd.DataFrame(dict_proteins_residues, index = xlabels_list)
    bar = df.plot(kind = 'bar')
    # labels and graph components 
    plt.xticks(rotation = 0, fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.xlabel("Residues", labelpad = 15, fontsize = 16)
    plt.ylabel("Percent of Residues", labelpad = 15, fontsize = 16)
    plt.title("Percent of Each Residues In " + ", ".join(list_proteins), fontsize = 18)
    plt.legend()
    plt.show()


###ATOMS### 
# returns dictionary of percentage of each atom in protein 
# uses .getElements() (method to be used on residue group to get the elements in each residue
def count_each_atom_protein(protein_id):
    # variables 
    structure = parsePDB(protein_id)
    hv = structure.getHierView()
    atoms_list = []
    # iterating through the structure and adding the atoms to list of atoms
    for chain in hv:
        for residue in chain:
            # only counts atoms if residue is not water
            if str(residue).lower()[0:3] != "hoh":
                # gets all elements in residue 
                atoms_in_residue = residue.getElements()
                # appends all the atoms in residue to atoms_list
                for atom in atoms_in_residue:
                    atoms_list.append(atom.lower())
    # returns the collections of percents of each atom 
    collections_atoms = collections.OrderedDict(Counter(atoms_list).items())
    num_atoms = sum(collections_atoms.values())
    # turns collections_atoms into dict of percents of each atom 
    for key, value in collections_atoms.items():
        collections_atoms[key] = value / num_atoms * 100
    return collections_atoms

# plots the percent of each atom of 1-5 proteins 
def plot_each_atom_percents():
    print("1 - 5 proteins can be entered")
    # variables and input 
    dict_proteins_atoms = {}
    proteins_inp = input("Enter protein(s) (separate by comma): ")
    list_proteins = proteins_inp.split(", ")
    # making sure 5 or less proteins entered
    list_proteins = list_proteins[0:5]

    # plotting
    plt.rcParams["figure.figsize"] = (13, 7)
    for index, protein in enumerate(list_proteins):
        dict_proteins_atoms[protein] = count_each_atom_protein(protein)

    # making set of all the different types of atom seen among the proteins 
    all_different_atoms = set([])
    for dict_protein in dict_proteins_atoms.values():
        for atom in dict_protein:
            all_different_atoms.add(atom)
    # adds all atoms to different protein dicts
    for atom in all_different_atoms:
        for protein in dict_proteins_atoms:
            if atom not in dict_proteins_atoms[protein]:
                dict_proteins_atoms[protein][atom] = 0
    # sorts all protein dictionaries and then turns them into list of values and prints atoms with percents less than certain amount 
    for protein in dict_proteins_atoms:
        small_percent_present = False
        # iterating through each proteins dictionary 
        for atom, percent in dict_proteins_atoms[protein].items():
            if percent < 4 and percent != 0:
                # correct upper and lower casing for atoms and correct connector_str
                if len(atom) == 2:
                    atom = atom[0].upper() + atom[1].lower()
                    connector_str = ": "
                else:
                    connector_str = " : "
                    atom = atom.upper()
                # printing 
                # printing protein name only once 
                if not small_percent_present:
                    small_percent_present = True
                    print("------" + protein.upper() + "------") 
                print(atom + connector_str + str(round(percent, 3)))
        # sorting dict and tunring it into list of values 
        dict_proteins_atoms[protein] = list(collections.OrderedDict(sorted(dict_proteins_atoms[protein].items())).values())
    # xlabels list and dataframe -> plot 
    xlabels_list = list(all_different_atoms)
    xlabels_list.sort()
    # correct upper and lower casing for atoms in xlabels_list 
    xlabels_list = [x[0].upper() + x[1].lower() if len(x) == 2 else x.upper() for x in xlabels_list]
    df = pd.DataFrame(dict_proteins_atoms, index = xlabels_list)
    bar = df.plot(kind = 'bar')
    # labels and graph components 
    plt.xticks(rotation = 0, fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.xlabel("Atoms", labelpad = 15, fontsize = 16)
    plt.ylabel("Percent of Atoms", labelpad = 15, fontsize = 16)
    plt.title("Percent of Each Atom In " + ", ".join([x.upper() for x in list_proteins]), fontsize = 18)
    plt.legend()
    plt.show()


###SECONDARY STRUCTURE###
def count_secondary_structure_protein(protein_id):
    # also there might be some kind of secondary structure file which I can use
    # https://www.rcsb.org/pages/help/ssHelp
    #file = fetchPDB(protein_id)
    #file = parsePDBHeader(protein_id)
    # TBD : understand the ss file, maybe the data is in, for the atom group there does not seem to be the data
    # maybe i use something instead of parsePDB 

    structure = parsePDB(protein_id)
    print(structure)
    hv = structure.getHierView()
    for x in hv:
        print(x)
        for y in x:
            print(y)
            for label in y.getDataLabels():
                print(label, "   ------   ", y.getData(label))
            break
            #print(y.getSecids())
        break

    




# enzymes to test: Transferases, Hydrolases, Lyases, Oxidoreductases, Isomerases, Ligases 
# Transferases: []
# Hydrolases: []
# Lyases: []
# Oxidoreductases: []
# Isomerases: {}
# Ligases: {4NV7 : N-acetyltransferase, 3O8M : Hexokinase, 1ZIO : Phosphotransferase}


def testing():
    count_secondary_structure_protein("5vw1")

#testing()
