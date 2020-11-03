'''
Important notes for when going through the text file 
Ignore fasta sequence if it does not have the mol:protein
Amino acid letter codes: U, Z, B, O, x are non standard amino acids or unknown?
'''

###IMPORTS###
from collections import Counter 
import collections 
import json 
import matplotlib.pyplot as plt
from counterProteinFullStatsAutomation import file_name, download_automation, time 
###IMPORTS###



#SEARCH OPTIONS: Name, length range, sequence part 
def extracting_search_data_to_json():
    protein_set = set([])
    protein_lengths_sum = 0
    residue_counter = Counter()
    standard_amino_acids = []
    standard_amino_acids = ["A", "R", "N", "D", "C", "E", "Q", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V"]
    other_total = 0
    #reading the file 
    f = open(file_name, 'r')
    fullDataBase = f.read().replace('\n', '|||').split("|||>")
    f.close()
    fullDataBase[0] = fullDataBase[0][1:]
    #search options stored 
    search_number, search_input = search_options()
    #iterating trhough all the proteins and extracting their data if search conditions met 
    for data_entry in fullDataBase:
        #data_entry only used for data if it is protein 
        if data_entry.split(" ")[1] == "mol:protein" and search_boolean_statement(search_number, search_input, data_entry):
            #protein ID printed 
            print(data_entry[0:4])
            #data from data_entry is extracted 
            protein_set.add(data_entry[0:4]) #proteins id added 
            protein_lengths_sum += int(data_entry.split(" ")[2].split(":")[1]) #proteins length 
            residue_counter += Counter(data_entry.split("|||")[1]) #counter object of seq 
    #summing then deleting non normal/unknown residues and putting their sum in counter 
    rc_del_copy = residue_counter.copy()
    for residue in rc_del_copy:
        if residue not in standard_amino_acids:
            other_total += rc_del_copy[residue]
            del residue_counter[residue]
    residue_counter["other"] = other_total
    #writing data to json file 
    number_proteins = len(protein_set)
    databaseStatistics = {"number proteins" : number_proteins, "length sum" : protein_lengths_sum, "residue counter values sum" : sum(residue_counter.values()), "residue counter" : residue_counter}
    with open('rcsbFullDatabaseStats.txt', 'w') as outfile:
        json.dump(databaseStatistics, outfile)
    

#extracting_search_data_to_json()

#uses the pdb_seqres.txt to make json file of the full rcsb database data 
def extracting_all_data_to_json():
    #variables
    protein_set = set([])
    protein_lengths_sum = 0
    residue_counter = Counter()
    standard_amino_acids = []
    standard_amino_acids = ["A", "R", "N", "D", "C", "E", "Q", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V"]
    other_total = 0
    #reading the file 
    f = open(file_name, 'r')
    fullDataBase = f.read().replace('\n', '|||').split("|||>")
    f.close()
    fullDataBase[0] = fullDataBase[0][1:]
    #going through all the data entries
    for data_entry in fullDataBase:
        #data_entry only used for data if it is protein 
        if data_entry.split(" ")[1] == "mol:protein":
            #protein ID printed 
            print(data_entry[0:4])
            #data from data_entry is extracted 
            protein_set.add(data_entry[0:4]) #proteins id added 
            protein_lengths_sum += int(data_entry.split(" ")[2].split(":")[1]) #proteins length 
            residue_counter += Counter(data_entry.split("|||")[1]) #counter object of seq 
    #summing then deleting non normal/unknown residues and putting their sum in counter 
    rc_del_copy = residue_counter.copy()
    for residue in rc_del_copy:
        if residue not in standard_amino_acids:
            other_total += rc_del_copy[residue]
            del residue_counter[residue]
    residue_counter["other"] = other_total
    #writing data to json file 
    number_proteins = len(protein_set)
    databaseStatistics = {"number proteins" : number_proteins, "length sum" : protein_lengths_sum, "residue counter values sum" : sum(residue_counter.values()), "residue counter" : residue_counter}
    with open('rcsbFullDatabaseStats.txt', 'w') as outfile:
        json.dump(databaseStatistics, outfile)

#graphs the percents of each residue and groups of residues (e.g. hydrophobic) of the full database
def full_stats_graph():
    #loading the json data 
    with open('rcsbFullDatabaseStats.txt') as json_file:
        statsDict = json.load(json_file)
    #variables 
    residue_amounts_counter = statsDict["residue counter"]
    total_residues = statsDict["length sum"]
    xlabels_residues_list = list(collections.OrderedDict(sorted(residue_amounts_counter.items())).keys())
    yValues = [x / total_residues * 100 for x in collections.OrderedDict(sorted(residue_amounts_counter.items())).values()]
    dict_percent_residues = dict(zip(xlabels_residues_list, yValues))
    dict_types_residues = {"Positively Charged" : 0, "Negatively Charged" : 0, "Polar Uncharged" : 0, "Hydrophobic" : 0, "Aromatic" : 0, "Other/Unkown" : 0}
    #making dict_types_residues 
    for residue in residue_amounts_counter:
        if residue.lower() in ["g", "a", "v", "l", "i", "p"]: 
            dict_types_residues["Hydrophobic"] += dict_percent_residues[residue]
        elif residue.lower() in ["k", "r", "h"]:
            dict_types_residues["Positively Charged"] += dict_percent_residues[residue]
        elif residue.lower() in ["d", "e"]:
            dict_types_residues["Negatively Charged"] += dict_percent_residues[residue]
        elif residue.lower() in ["s", "t", "c", "m", "n", "q"]:
            dict_types_residues["Polar Uncharged"] += dict_percent_residues[residue]
        elif residue.lower() in ["f", "y", "w"]:
            dict_types_residues["Aromatic"] += dict_percent_residues[residue]
        else:
            dict_types_residues["Other/Unkown"] += dict_percent_residues[residue]        
    #printing 
    print("-------------------Percent of Each Residue in Full Database-------------------")
    for x in range(len(xlabels_residues_list)):
        print("Residue: " + xlabels_residues_list[x].upper() + (" " * (max([len(y) for y in xlabels_residues_list]) - len(xlabels_residues_list[x]))) + " | " + str(round(yValues[x], 5)))
    print()
    print("----------------Percent of Groups of Residues in Full Database----------------")
    for x in range(len(dict_types_residues.keys())):
        print("Group: " + list(dict_types_residues.keys())[x] + (" " * (max([len(y) for y in dict_types_residues.keys()]) - len(list(dict_types_residues.keys())[x]))) + " | " + str(round(list(dict_types_residues.values())[x], 5)))
    print()
    #plotting
    #plot of each residue 
    plt.figure(1)
    plt.rcParams["figure.figsize"] = (13.5, 7.5)
    plt.bar(xlabels_residues_list, yValues)
    plt.xticks(rotation = 0, fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.xlabel("Residues", labelpad = 15, fontsize = 16)
    plt.ylabel("Percent", labelpad = 15, fontsize = 16)
    plt.title("Percent of Each Residue In The Full RCSB Database", fontsize = 18)
    #plot of residue groups 
    plt.figure(2)
    plt.rcParams["figure.figsize"] = (13, 7)
    plt.bar(dict_types_residues.keys(), dict_types_residues.values())
    plt.xticks(rotation = 0, fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.xlabel("Group of Residues", labelpad = 15, fontsize = 16)
    plt.ylabel("Percent", labelpad = 15, fontsize = 16)
    plt.title("Percent of Each Group of Residues In The Full RCSB Database", fontsize = 18)
    plt.show()


def search_options():
    print("Search Options: \n\t1. Molecule Name\n\t2. Molecule Length\n\t3. Sequence")
    search_type = int(input("Enter number of type of search: "))
    #molecule name searching 
    if search_type == 1:
        print("Name Options: \n\t1. Part of Name \n\t2. Exact Name\n\t3. Not in Name\n\t4. Not Equal to Name")
        name_type = int(input("Enter number of type of molecule name search: "))
        if name_type == 1:
            return 1, input("Enter part of molecule name: ")
        elif name_type == 2:
            return 2, input("Enter exact molecule Name: ")
        elif name_type == 3:
            return 3, input("Enter part of name thats not in targets: ")
        else:
            return 4, input("Enter name not equal to targets")
    #molecule length searching 
    elif search_type == 2:
        print("Length Options: \n\t1. Range\n\t2. Exact Number\n\t3. More than\n\t4. Less than\n\t5. not equal to\n\t6. Equal to number in list")
        length_type = int(input("Enter number of type of length search: "))
        if length_type == 1: 
            greater = int(input("Enter molecular length that target is greater than: "))
            less = int(input("Enter molecular length that target is less than: "))
            return 5, [greater, less]
        elif length_type == 2:
            return 6, int(input("Enter exact molecular length: ")) 
        elif length_type == 3:
            return 7, int(input("Enter molecular length that targets are greater than: "))
        elif length_type == 4:
            return 8, int(input("Enter molecular length that targets are less than: ")) 
        elif length_type == 5:
            return 9, int(input("Enter molecular length that targets are not equal to: ")) 
        else:
            molecular_lengths_equal_to = [int(x) for x in input("Enter list of molecular lengths that targets can be equal to (seperate by one space): ").split(" ")]
            return 10, molecular_lengths_equal_to
    #sequence searching 
    elif search_type == 3: 
        # sequence search inputs 
        search_sequence = input("Enter sequence to search for: ")
        print("Sequence Options: \n\t1. Part of sequence \n\t2. Exact Sequence \n\t3. Not in Sequence")
        sequence_type = int(input("Enter number of type of sequence search"))
        # part of sequence 
        if sequence_type == 1:
            part_sequence_search_options = int(input("Part of Sequence Options: \n\t1. Sequence Appears Certain amount of times \n\t2.", \
                "Sequence Appears less than specified times \n\t3. Sequence Appears greater than", \
                "specified times \n\t4. Sequence Appears between specified range of times"))
            if part_sequence_search_options == 1:
                return 11, [search_sequence, int(input("Enter number of times that sequence appears in targets: "))]
            elif part_sequence_search_options == 2:
                return 12, [search_sequence, int(input("Enter number of times that sequence appears less than in targets: "))]
            elif part_sequence_search_options == 3:
                return 13, [search_sequence, int(input("Enter number of times that sequence appears greater than in targets: "))]
            elif part_sequence_search_options == 4:
                greater_than = int(input("Enter number of times that sequence appears greater than in targets: "))
                less_than = int(input("Enter number of times that sequence appears less than in targets: "))
                return 14, [search_sequence, greater_than, less_than]
        # exact sequence 
        elif sequence_type == 2:
            return 15, [search_sequence, input("Enter exact sequence targets equal to: ")]
        # not in sequence 
        else:
            return 16, [search_sequence, input("Enter sequence not in targets: ")]

'''
>101m_A mol:protein length:154  MYOGLOBIN
MVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRVKHLKTEAEMKASEDLKKHGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQG
'''

def search_boolean_statement(search_number, search_input, data_entry):
    # part of molecule name searching 
    if search_number == 1: 
        return search_input in data_entry
    elif search_number == 2:
        return search_input == data_entry
    elif search_number == 3:
        return search_input not in data_entry
    elif search_number == 4:
        return search_input != data_entry 
    # molecule length searching 
    elif search_number == 5:
        return search_input[0] > data_entry and search_input < data_entry
    elif search_number == 6:
        return search_input == data_entry
    elif search_number == 7:
        return search_input > data_entry
    elif search_number == 8:
        return search_input < data_entry
    elif search_number == 9:
        return search_input != data_entry
    elif search_number == 10:
        return data_entry in search_input
    # molecule sequence searching, TBD these need to be revised 
    # have the sequences as first item in list in serach_input 
    elif search_number == 11:
        return search_input == data_entry
    elif search_number == 12:
        return search_input < data_entry
    elif search_number == 13:
        return search_input > data_entry
    elif search_number == 14:
        return data_entry.count(search_input[0]) > search_input[0] and data_entry.count(search_input[1]) <
    elif search_number == 15:
        data_entry.count(search_input)


#sequence searching 
    elif search_type == 3: 
        # sequence search inputs 
        search_sequence = input("Enter sequence to search for: ")
        print("Sequence Options: \n\t1. Part of sequence \n\t2. Exact Sequence \n\t3. Not in Sequence")
        sequence_type = int(input("Enter number of type of sequence search"))
        # part of sequence 
        if sequence_type == 1:
            part_sequence_search_options = int(input("Part of Sequence Options: \n\t1. Sequence Appears Certain amount of times \n\t2.", \
                "Sequence Appears less than specified times \n\t3. Sequence Appears greater than", \
                "specified times \n\t4. Sequence Appears between specified range of times"))
            if part_sequence_search_options == 1:
                return 11, [search_sequence, int(input("Enter number of times that sequence appears in targets: "))]
            elif part_sequence_search_options == 2:
                return 12, [search_sequence, int(input("Enter number of times that sequence appears less than in targets: "))]
            elif part_sequence_search_options == 3:
                return 13, [search_sequence, int(input("Enter number of times that sequence appears greater than in targets: "))]
            elif part_sequence_search_options == 4:
                greater_than = int(input("Enter number of times that sequence appears greater than in targets: "))
                less_than = int(input("Enter number of times that sequence appears less than in targets: "))
                return 14, [search_sequence, greater_than, less_than]
        # exact sequence 
        elif sequence_type == 2:
            return 15, [search_sequence, input("Enter exact sequence targets equal to: ")]
        # not in sequence 
        else:
            return 16, [search_sequence, input("Enter sequence not in targets: ")]


# NOT USED anymore, search_options and search_boolean_statement are meant to do this
def searched_database_options(fasta_part):
    print("Search Options: \n\t1. Molecule Name\n\t2. Molecule Length\n\t3. Sequence")
    search_type = int(input("Enter number of type of search: "))
    #molecule name searching 
    if search_type == 1:
        print("Name Options: \n\t1. Part of Name \n\t2. Exact Name\n\t3. Not in Name\n\t4. Not Equal to Name")
        name_type = int(input("Enter number of type of molecule name search: "))
        if name_type == 1:
            return input("Enter part of molecule name: ") in fasta_part
        elif name_type == 2:
            return input("Enter exact molecule Name: ") == fasta_part
        elif name_type == 3:
            return input("Enter part of name thats not in targets: ") not in fasta_part
        else:
            return input("Enter name not equal to targets") != fasta_part
    #molecule length searching 
    elif search_type == 2:
        print("Length Options: \n\t1. Range\n\t2. Exact Number\n\t3. More than\n\t4. Less than\n\t5. not equal to\n\t6. Equal to number in list")
        length_type = int(input("Enter number of type of length search: "))
        if length_type == 1: 
            greater = int(input("Enter molecular length that target is greater than: "))
            less = int(input("Enter molecular length that target is less than: "))
            return greater > fasta_part and less < fasta_part
        elif length_type == 2:
            return int(input("Enter exact molecular length: ")) == fasta_part
        elif length_type == 3:
            return int(input("Enter molecular length that targets are greater than: ")) > fasta_part
        elif length_type == 4:
            return int(input("Enter molecular length that targets are less than: ")) < fasta_part
        elif length_type == 5:
            return int(input("Enter molecular length that targets are not equal to: ")) != fasta_part
        else:
            molecular_lengths_equal_to = [int(x) for x in input("Enter list of molecular lengths that targets can be equal to (seperate by one space): ").split(" ")]
            return fasta_part in molecular_lengths_equal_to
    #sequence searching 
    elif search_type == 3: 
        search_sequence = input("Enter sequence to search for: ")
        print("Sequence Options: \n\t1. Part of sequence \n\t2. Exact Sequence \n\t3. Not in Sequence")
        sequence_type = int(input("Enter number of type of sequence search"))
        if sequence_type == 1:
            part_sequence_search_options = int(input("Part of Sequence Options: \n\t1. Sequence Appears Certain amount of times \n\t2.", \
                "Sequence Appears less than specified times \n\t3. Sequence Appears greater than", \
                "specified times \n\t4. Sequence Appears between specified range of times"))
            if part_sequence_search_options == 1:
                return int(input("Enter number of times that sequence appears in targets: ")) == fasta_part
            elif part_sequence_search_options == 2:
                return int(input("Enter number of times that sequence appears less than in targets: ")) < fasta_part
            elif part_sequence_search_options == 3:
                return int(input("Enter number of times that sequence appears greater than in targets: ")) > fasta_part
            elif part_sequence_search_options == 4:
                greater_than = int(input("Enter number of times that sequence appears greater than in targets: "))
                less_than = int(input("Enter number of times that sequence appears less than in targets: "))
                return fast_part < greater_than and fasta_part > less_than
            #TBD
            #do it so that they can do less than or equal to certain times, or equal to exact time 
            return fasta_part.count(input("Enter part of sequence in targets: ")) 
        elif sequence_type == 2:
            return input("Enter exact sequence targets equal to: ") in fasta_part
        else:
            return input("Enter sequence not in targets: ") not in fasta_part

#main function; runs downloading, assembling database and graphing 
def main():
    print("""Answer questions using "y" for yes and "n" for no""")
    #input on whether to download pdb_seqres.txt and assemble database
    download_assemble = input("Would you like to download the rcsb full protein database raw data and then assemble database of statistics: ")
    try: 
        if download_assemble[0].lower() == "y":
            download_automation() #downloads raw data 
            extracting_data_start = time.time() #start time 
            extracting_all_data_to_json() #assembles database statistics from raw data file 
            extracting_data_end = time.time() #end time 
            print("Time elapsed extracting data from", file_name, "and building database: ", round(extracting_data_end - extracting_data_start, 4), "Seconds")
    except ValueError:
        pass

    #input on whether to graph database stats
    graph_full_database = input("Would You like to graph the rcsb full database statistics: ") 
    try: 
        if graph_full_database[0].lower() == "y":
            full_stats_graph() #database stats graphed 
    except ValueError:
        pass 

    #input on whether to assemble a database from a search 
    assemble_searched_database = input("Would you like to assemble a database from a search: ")
    try: 
        if assemble_searched_database[0].lower() == "y":
            searched_database_options()
            
            #name_types = [Part of name, all of name]
            #length_types = [range, exact range, more than, less than, not equal to, equal to one in a list of multiple ]
            #sequence_types = [], this could be really interesting could do like MSA, but this could also
            #   be extremely computationally extensive 
    except ValueError:
        pass

    #input on whether to graph database assembled from search 
    graph_searched_database = input("Would you like to graph the database from the search: ")
    try: 
        if graph_searched_database[0].lower() == "y":
            pass
    except ValueError:
        pass

main()


