###IMPORTS###
from counterProtein import plot_residue_group_percents, plot_each_residue_percents, plot_each_atom_percents
###IMPORTS###


#main function runs user input
def main():
    #menu keeps going until user quits menu 
    while True:
        #variables 
        option = 0
        #printing options and input for option
        print("""\n------------------------------------------
Options: 1. Percent of Residue Groups
         2. Percent of Each Residue 
         3. Percent of Each Atom
         4. Quit Menu\n""")
        #ensuring valid option 
        while option not in range(1, 5):
            try: 
                option = int(input("User: "))
            except ValueError:
                print("Invalid option")
        #residue groups 
        if option == 1:
            plot_residue_group_percents()
        #each residue 
        elif option == 2:
            plot_each_residue_percents()
        #each atom 
        elif option == 3:
            plot_each_atom_percents()
        #quit 
        elif option == 4:
            break

main()

#1fn3