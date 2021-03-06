import time
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

from LeNet import Net

def train(net=None, model_name='mnist_lenet', gpu_train=False):
    # check if net was passed in
    if net == None:
        net = Net()

    # Create the transformation to prepare the image
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(
                (0.1307,),  # mean
                (0.3081,)   # std
            )
        ]
    )

    #save training dataset to ./data, downloads and trasforms images
    trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    #load train set, with 4 samples per minibatch, randomize images and use 2 threads
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=4, shuffle=True, num_workers=2)

    # enable GPU training
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    if gpu_train == True:
        net.to(device)  # send network to device
        print('Training on %s\n' % device)

    #print the neural network
    print(net)

    criterion = nn.CrossEntropyLoss() # creating a mean squared error object (try other loss functions)
    # set up optimizer for SGD and pass network parameters and learning rate
    optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.5)

    start_time = time.time()

    for epoch in range(2):  # iterate over dataset multiple times

        running_loss = 0.0  # running total of the cost function for output
        # iterate through the training set
        for i, data in enumerate(trainloader, 0):
            # get the input and the label
            if gpu_train == True:
                inputs, labels = data[0].to(device), data[1].to(device)
            else:
                inputs, labels = data

            optimizer.zero_grad()  # zeros the gradient buffers

            output = net(inputs)   # propogate input through the neural network
            loss = criterion(output, labels) # Puts output and target into criterion object, MSE
            loss.backward()  # calculate the gradient of each parameter based on the MSE loss function
            optimizer.step()  # Does the update
            #print statistics of training
            running_loss += loss.item()
            if i % 200 == 199:
                print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, (running_loss / 200)))
                running_loss = 0.0

    duration = time.time() - start_time
    print('--~~ Finished Training ~~--\nTrained in %.2f seconds' % duration)

    print('Saving Model')
    torch.save(net.state_dict(), './models/' + model_name + '.pth')

    #print('Print weights\n')
    #weights = list(net.conv1.parameters())
    #print(weights) 

    


if (__name__ == '__main__'):
    train()
