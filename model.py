import torch
from torch import nn

class toho_CNN(nn.Module):
    def __init__(self, ):
        super().__init__()
        # input size of image 3*200*150
        self.model = self.build_nn()
        self.optimizer = self.build_optimizer(self.model)
        self.criterion = nn.BCELoss()
    
    def build_optimizer(self, model=None):
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-5)
        return optimizer

    def build_nn(self):
        convs = nn.Sequential(
            nn.Conv2d(3, 96, 11, stride=4),
            nn.ReLU(),
            nn.MaxPool2d(3, stride=2),
            nn.Conv2d(96, 256, 5, padding="same"),
            nn.ReLU(),
            nn.MaxPool2d(3, stride=2),
            nn.Conv2d(256, 384, 3, padding="same"),
            nn.ReLU(),
            nn.Conv2d(384, 256, 3, padding="same"),
            nn.ReLU(),
            nn.MaxPool2d(3, stride=2)
        )
        linear = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256*5*3, 1280),
            nn.ReLU(),
            nn.Linear(1280, 320),
            nn.ReLU(),
            nn.Linear(320, 5),
            nn.ReLU()
        )
        sigmoid = nn.Sigmoid()
        return nn.Sequential(convs, linear, sigmoid)

    def forward(self, x):
        x = self.model(x)
        return x