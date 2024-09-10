import torch

class ExtendedTorchModule(torch.nn.Module):
  def __init__(self,model):
    super().__init__()
    self.model = model

  def train(self,dataloader_train, criterion, optimizer, epoch_count = 10):
    for epoch in range(epoch_count):  # loop over the dataset multiple times

      running_loss = 0.0
      for i, data in enumerate(dataloader_train, 0):
          # get the inputs; data is a list of [inputs, labels]
          inputs, labels = data
          
          # zero the parameter gradients
          optimizer.zero_grad()

          # forward + backward + optimize
          outputs = self(inputs)
          loss = criterion(outputs, labels)
          loss.backward()
          optimizer.step()

          # print statistics
          running_loss += loss.item()
          if i % 5000 == 4999:    # print every 2000 mini-batches
              print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 5000:.3f}')
              running_loss = 0.0
    print('Finished Training')
    
  def forward(self, x):
    x = x.to(torch.float32)
    # for f in self.module_list:
    #     x = f(x)
    # return x
    return self.model(x)
    
  def compute_outputs(self, dataloader_test):
    output_arr = []
    with torch.no_grad():
      for data in dataloader_test:
          inputs, labels = data
          # calculate outputs by running inputs through the network
          outputs = self(inputs)
          output_arr.append(outputs.numpy())

    # <ipython-input-44-114ac3037693>:54: UserWarning: Creating a tensor from a list of numpy.ndarrays is extremely slow. Please consider converting the list to a single numpy.ndarray with numpy.array() before converting to a tensor. (Triggered internally at ../torch/csrc/utils/tensor_new.cpp:245.)
    t = torch.tensor(output_arr) 
    return torch.squeeze(t) 

  # def compute_accuracy(self, dataloader_test):
  #   correct = 0
  #   total = 0
  #   # since we're not training, we don't need to calculate the gradients for our outputs
  #   with torch.no_grad():
  #       for data in dataloader_test:
  #           inputs, labels = data
  #           # calculate outputs by running inputs through the network
  #           outputs = self(inputs)
  #           # the class with the highest energy is what we choose as prediction
  #           _, predicted = torch.max(outputs.data, 1)
  #           total += labels.size(0)
  #           correct += (predicted == labels).sum().item()

  #   print(f'Accuracy of the network: {100 * correct // total} %')