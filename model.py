import torch
from torch import nn

class toho_CNN(nn.Module):
    def __init__(self):
        super(toho_CNN, self).__init__()
        # input size of image 3*200*150
        self.model = self.build_nn()
        self.optimizer = self.build_optimizer(self.model)
        self.criterion = nn.BCELoss()
    
    def build_optimizer(self, model=None):
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-4, weight_decay=6e-4) # 6e-4 step 150;
        return optimizer

    def build_nn(self):
        convs = nn.Sequential(
            nn.Conv2d(3, 96, 11, stride=4),
            nn.ReLU(),
            nn.MaxPool2d(3, stride=2),
            nn.Conv2d(96, 256, 5, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(3, stride=2),
            nn.Conv2d(256, 384, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(384, 256, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(3, stride=2)
        )
        linear = nn.Sequential(
            nn.Flatten(),
            nn.Linear(3840, 3840),
            nn.ReLU(),
            nn.Linear(3840, 1280), # 648
            nn.ReLU(),
            nn.Linear(1280, 5)
        )
        sigmoid = nn.Sigmoid()
        return nn.Sequential(convs, linear, sigmoid)

    def forward(self, x):
        x = self.model(x)
        return x