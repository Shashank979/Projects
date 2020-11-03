### IMPORTS ###  
from __future__ import print_function, division

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import time
import os
import copy
from PIL import Image
from pathlib import Path
from torch.autograd import Variable
from torchvision.transforms import ToTensor

import torchvision.transforms.functional as TF

# TBD L dataloaders issue, figure it out they are nto working,
#          when I put in the transforms its working so its an issue iwth image_datasets probably
#------------------------------
# commenting code (right now in pymol_surfaces_run.py) 
#------------------------------
# show what it guessed for each image in every run, then figure out where to go. 
# for doing this I am printing input label and then the guess label for val and 
# shuffling and then running and seeing what its accuracy is 

# needs accuracy  of > 80, for now dont crop it, just do things like rotation 
# current: 
#           1. Save and Be able to load a trained model
#                       this seems to be working, try to save the model with a ton of epochs
#           2. Make the folder of the test files 

# Will I need transforms?!?!?!

"""
data_transforms = {
    'train': transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}



# directory 
data_dir = 'glob_fib_data1'
# dictionary of images in train and val
image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
                  for x in ['train', 'val']}

# loads the data set 
#dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=1, shuffle = True 
#                    , num_workers=1)
#              for x in ['train', 'val']}
# no shuffle (for regular use the other dataloaders)
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=1, shuffle = True, num_workers=1) for x in ['train', 'val']}



# size of dataset_sizes 
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
class_names = image_datasets['train'].classes

# setting device as cpu or gpu 
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
"""


# using try, catch to catch the local variable or the image where its messing up

# train model function 
def train_model(model, criterion, optimizer, scheduler, num_epochs=25):
    try:
        # the current time 
        since = time.time()

        #   state_dict gives Python dictionary object that maps each layer to 
        # its parameter tensor
        best_model_wts = copy.deepcopy(model.state_dict())
        # best accuracy value 
        best_acc = 0.0

        # iterates 
        for epoch in range(num_epochs):
            # prints the epoch 
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)

            # Each epoch has a training and validation phase
            for phase in ['train', 'val']:
                print("-------------------", phase, "-----------------")
                # models put into correct modes 
                if phase == 'train':
                    model.train()  # Set model to training mode
                else:
                    model.eval()   # Set model to evaluate mode

                # running_loss is total loss of all images in each respective phase 
                running_loss = 0.0   
                # running_corrects is total number of correct guesses in each respective phase 
                running_corrects = 0   

                # len(dataloaders[train]) is 43? and len(dataloaders['val']) is 10. What are these? 
                # Iterate over data.
                # dataloaders is all the images, phase is train or validation 
                # inputs  = images data, labels = wether it is dog or cat (type is tensor)
                for inputs, labels in dataloaders[phase]:
                    #if phase == 'val':
                    #    print("label on the data: ", labels)
                    # zeros the parameter gradients, so can restart. So we are resetting parameters from image to image
                    # gradient only needed during training 
                    # scheduler.step() needs to be called with optimzer.zero_grad()
                    optimizer.zero_grad()
                    
                    # gradient only enabled in train but it still does the inside code in both phases 
                    # enables gradient thus it can change parameters and learn from image 
                    with torch.set_grad_enabled(phase == 'train'):
                        # images plugged into model and outputs is returned which is the chance it is dog and chance it is cat?
                        outputs = model(inputs) 
                        # underscore ignores values. Preds is indices of the largest value in each row. Indices would give whether dog or cat 
                        _, preds = torch.max(outputs, 1)  
                        '''
                        ex. 
                           preds = [0, 0, 0, 1]
                           outputs:  tensor([[ 0.2449,  0.9274], 
                                             [ 0.0640,  0.5708],
                                             [ 0.2913,  0.6338],
                                             [ 2.5553, -1.2961]], grad_fn=<AddmmBackward>)
                        '''
                        #if phase == 'val':
                        #    print("output guess: ", preds)
                        # measures the performance of the model whose output is a probability between 0 and 1.  
                        # A perfect model would have a log loss of 0. 
                        loss = criterion(outputs, labels)

                        # backward + optimize only if in training phase
                        # saving and updating parameters essentialy 
                        if phase == 'train':
                            # calculates the gradients and then saves them 
                            loss.backward()
                            # updates the parameters 
                            optimizer.step()
                        
                    # input.size(0) is usually 4 as most of the batches have 4 images in them 
                    # losses of current iteration images added too running_loss
                    running_loss += loss.item() * inputs.size(0)
                    # the number of correct guesses by model are added to running_corrects 
                    running_corrects += torch.sum(preds == labels.data)
               
                # dont fully understand 
                if phase == 'train':
                    # changes the learning rate 
                    scheduler.step()


                # getting loss 
                # this is bascically (total_loss_of_images / number of all_images) for respective phase 
                epoch_loss = running_loss / dataset_sizes[phase]
                # getting accuracy 
                # this is basically (number of images_correct / number of all_images) for respective phase 
                epoch_acc = running_corrects.double() / dataset_sizes[phase]

                print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                    phase, epoch_loss, epoch_acc))

                # save the model 
                # saves best model and accuracy 
                if phase == 'val' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    # state_dict() is a python dict mapping from layer to their parameters
                    # used to save and load models 
                    best_model_wts = copy.deepcopy(model.state_dict())

            print()

        # gives the time passed 
        time_elapsed = time.time() - since  # time that has passed
        print('Training complete in {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60))
        # gives the best accuracy 
        print('Best val Acc: {:4f}'.format(best_acc))

        # load scalar state 
        model.load_state_dict(best_model_wts)
        # best model returned 
    except Exception as e: 
        print(locals())
        print(e)
        exit()

    return model

def make_model():
    # running train model 
    model_ft = torch.hub.load('pytorch/vision:v0.6.0', 'resnet18', pretrained=False)

    num_ftrs = model_ft.fc.in_features
    # Here the size of each output sample is set to 2.
    # Alternatively, it can be generalized to nn.Linear(num_ftrs, len(class_names)).
    model_ft.fc = nn.Linear(num_ftrs, 2)

    model_ft = model_ft.to(device)

    criterion = nn.CrossEntropyLoss()

    # Observe that all parameters are being optimized
    optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)

    # Decay LR by a factor of 0.1 every 7 epochs
    # learning rate is the amount that weights are adjusted in training. 
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)


    # MODEL
    model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler, num_epochs=5)

def save_model(model_to_save):
    # saving model 
    path_model = "/Users/shashank/git/tutoring/MachineLearning/globular_fibrous/glob_fib_data1_model.pt"
    torch.save(model_ft, path_model)
    

# some function that i found online that allows a test folder to be put into model 
def test_model(path_model):
    #aka : device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model1 = torch.load(path_model)
    model1.eval()
    # iterate through the images 
    directory = '/Users/shashank/git/tutoring/MachineLearning/globular_fibrous/glob_fib_data1_test'
    for filename in os.listdir(directory):
        print(directory + "/" + filename)
        image = Image.open(directory + "/" + filename)
        
        to_pil = transforms.ToPILImage()
        image = to_pil(image)
        index = predict_image(image)
        
        #still not working 
        # could maybe do dataloder for each file but seems overkill :(
        
        """#-----------------new code
        #https://discuss.pytorch.org/t/how-to-read-just-one-pic/17434 is where found first few lines of this code 
        # getting some error 
        image = TF.to_tensor(image)
        # is the unsqueeze step right 
        image.unsqueeze_(0)

        # would doing the transformations fix the error?
        #transforms.ToTensor()
        #transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        print(image)
        """#-----------------new code   


        output = model1(image)
        prediction = int(torch.max(output.data, 1)[1].numpy())
        if prediction == 0:
            print("Guess: Fibrous")
        elif prediction == 1:
            print("Guess: Globular")
        else:
            print("*Error*   prediction = ", prediction)

#imsize = 256
#loader = transforms.Compose([transforms.Scale(imsize), transforms.ToTensor()])
def image_loader(image_name):
    """load image, returns cuda tensor"""
    image = Image.open(image_name)
    image = ToTensor()(image).unsqueeze(0)
    #image = image.view()

    #image = loader(image)#.float()
    image = Variable(image, requires_grad=True)
    #image = image.unsqueeze(0)  #this is for VGG, may not be needed for ResNet
    
    return image



test_transforms = transforms.Compose([transforms.Resize(224),
                                      transforms.ToTensor(),
                                     ])
def predict_image(image):
    image_tensor = test_transforms(image).float()
    image_tensor = image_tensor.unsqueeze_(0)
    image1 = Variable(image_tensor)
    image1 = image1.to(device)
    output = model(image1)
    index = output.data.cpu().numpy().argmax()
    return index

test_model("/Users/shashank/git/tutoring/MachineLearning/globular_fibrous/glob_fib_data1_model.pt")




