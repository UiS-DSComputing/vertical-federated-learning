from torch import nn, optim
import torch.nn.functional as F


class ImageClient(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = ImageNet()
        self.output = None
        self.grad_from_label = None

    def forward(self, inputs):
        self.output = self.model(inputs)
        output = self.output.detach().requires_grad_()
        return output

    def client_backward(self, grad_from_label):
        self.grad_from_label = grad_from_label
        self.output.backward(grad_from_label)

    def train(self):
        self.model.train()

    def eval(self):
        self.model.eval()

    def get_optimizer(self):
        return optim.SGD(self.model.parameters(), lr=0.01, momentum=0.9)


class ImageNet(nn.Module):
    def __init__(self):
        super(ImageNet, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 200)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return x
