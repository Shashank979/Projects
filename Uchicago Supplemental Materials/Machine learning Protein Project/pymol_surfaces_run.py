import pymol
import os
import shutil
import random

# finish commenting out code, at the main function 

# will need to comment out this functino, current comments might be wrong 
def get_images_test(proteins, protein_mode, path_send):
    # grab all the protein files from the database 
    for protein in proteins:
        cmd.fetch(protein)


    # taking png's of all the proteins 
    for number, protein in enumerate(proteins): 
        # loading in protein 
        cmd.reinitialize()
        cmd.load(protein + ".cif")
        # settings for protein 
        cmd.color("green")  # colors protein green
        cmd.hide("all")   # hides the protein
        cmd.show(protein_mode)
        # resets protein orientation 
        cmd.orient()

        # setting tag
        if number > 8:
            tag = "globular"
        else:
            tag = "fibrous"

        # generating list of rotations 
        rand_rotations = set([])
        while len(rand_rotations) < 1:
            random_angle = random.randrange(0, 360, 90)
            # ensuring that there is only one rotation at 0 degrees 
            if random_angle == 0:
                random_axis = "startpos"
            else:
                random_axis = random.choice(["x", "y", "z"])
            rand_rotations.add((random_axis, random_angle))

        # taking png of each rotation 
        for rotation in rand_rotations:
            axis = rotation[0]
            angle = rotation[1]

            if axis == "startpos":
                cmd.png(tag + "_" + protein + "_" + axis + str(angle) + "_" + protein_mode, ray = 1)    # takes png of protien 
            else:
                # rotates on x,y or z axis by some amount of specified degrees 
                cmd.rotate(axis, angle)   # rotates protein  
                cmd.png(tag + "_" + protein + "_" + axis + str(angle) + "_" + protein_mode, ray = 1)    # takes png of protien 
                # setting protein back into original position
                cmd.rotate(axis, 360 - angle)   # rotates protein  

    # moving the file to the proper folder 
    globular_fibrous_path = '/Users/shashank/git/tutoring/MachineLearning/globular_fibrous'
    for file in os.listdir(globular_fibrous_path): 
        if file.endswith('.png'): 
            shutil.move(globular_fibrous_path + '/' + file, path_send)

# gets pictures for validation directory 
def get_images_val(tag, proteins, protein_mode, path_send):
    # grab all the protein files from the database 
    for protein in proteins:
        cmd.fetch(protein)

    # taking png's of all the proteins 
    for protein in proteins: 
        # loading in protein 
        cmd.reinitialize()
        cmd.load(protein + ".cif")
        # settings for protein 
        cmd.color("green")  # colors protein green
        cmd.hide("all")   # hides the protein
        cmd.show(protein_mode)
        # resets protein orientation 
        cmd.orient()

        # generating list of rotations 
        rand_rotations = set([])
        while len(rand_rotations) < 4:
            random_angle = random.randrange(0, 360, 90)
            # ensuring that there is only one rotation at 0 degrees 
            if random_angle == 0:
                random_axis = "startpos"
            else:
                random_axis = random.choice(["x", "y", "z"])
            rand_rotations.add((random_axis, random_angle))

        # taking png of each rotation 
        for rotation in rand_rotations:
            axis = rotation[0]
            angle = rotation[1]

            if axis == "startpos":
                cmd.png(tag + "_" + protein + "_" + axis + str(angle) + "_" + protein_mode, ray = 1)    # takes png of protien 
            else:
                # rotates on x,y or z axis by some amount of specified degrees 
                cmd.rotate(axis, angle)   # rotates protein  
                cmd.png(tag + "_" + protein + "_" + axis + str(angle) + "_" + protein_mode, ray = 1)    # takes png of protien 
                # setting protein back into original position
                cmd.rotate(axis, 360 - angle)   # rotates protein  

    # moving the file to the proper folder 
    globular_fibrous_path = '/Users/shashank/git/tutoring/MachineLearning/globular_fibrous'
    for file in os.listdir(globular_fibrous_path): 
        if file.endswith('.png'): 
            shutil.move(globular_fibrous_path + '/' + file, path_send)

# gets pictures for train directory 
def get_images(tag, proteins, protein_mode, path_send):
    # grab all the protein files from the database 
    for protein in proteins:
        cmd.fetch(protein)

    # taking png's of all the proteins 
    for protein in proteins:
        # loading in protein 
        cmd.reinitialize() 
        cmd.load(protein + ".cif")
        # settings for protein 
        cmd.color("green")
        cmd.hide("all")
        cmd.show(protein_mode)
        # resets protein orientation 
        cmd.orient()
        # takes png at start position 
        cmd.png(tag + "_" + protein + "_" + "startpos" + "_" + protein_mode, ray = 1)
        
        # how much to rotate by each time 
        rotation_value = 90
        # number of times to rotate 
        rotation_times = 360 / rotation_value
        # takes pngs for x rotations
        # ends up back at the start position 
        for num in range(rotation_times):
            cmd.rotate("x", rotation_value)
            if num != 3:
                cmd.png(tag + "_" + protein + "_" + "x" + str(num * 90 + 90) + "_" + protein_mode, ray = 1)
        # takes pngs for x rotations
        # ends up back at the start position 
        for num in range(rotation_times):
            cmd.rotate("y", rotation_value)
            if num != 3:
                cmd.png(tag + "_" + protein + "_" + "y" + str(num * 90 + 90) + "_" + protein_mode, ray = 1)
        # takes pngs for x rotations
        # ends up back at the start position 
        for num in range(rotation_times):
            cmd.rotate("z", rotation_value)
            if num != 3:
                cmd.png(tag + "_" + protein + "_" + "z" + str(num * 90 + 90) + "_" + protein_mode, ray = 1)


    # moving the file to the proper folder 
    globular_fibrous_path = '/Users/shashank/git/tutoring/MachineLearning/globular_fibrous'
    for file in os.listdir(globular_fibrous_path): 
        if file.endswith('.png'): 
            shutil.move(globular_fibrous_path + '/' + file, path_send)

# main function to set main variables and call the proper function 
def main():
    proteins =  ["1KU8", "5XAU", "1VDF", "4PLM", "1FBM", "1WZB", "3NTN", "4N23", "6UUI", "1CEM", "1MBO", "1RIE", "1SCR", "1DIV", "1JXU", "2BP2", "1HPI", "1XTG", "1CUK", "1AVU"]
    protein_mode = "surface"    
    # folder to put png's in
    path_send = '/Users/shashank/git/tutoring/MachineLearning/globular_fibrous/glob_fib_data1_test'   # path to send png's too

    # calling either function for val or function for train 
    get_images_test(proteins, protein_mode, path_send)

main()

# what to save : 
# color is set for now how about : 
# wire, licorice, ribbon, cartoon, spheres, surface
# for now try 3 different models : surface, spheres, wires 
# rotate works so how about do x = 90, 180, 270; y = 90, 180, 270; z = 90, 180, 270  and 0, 0, 0 so start pos
# so for first test we are going to do Surface and 12 images / protein
# Train : 120 images (10 proteins w/ 10 rotations)
# val : 24 images (6 proteins w/ 4 random rotations)