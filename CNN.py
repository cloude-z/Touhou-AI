import os.path
import torchvision.transforms as T

from train_eval import *
import data_load
import model

device = torch.device("cuda" if torch.cuda.is_available() else 'cpu')
print("Using device: {}".format(device))

# path of dataset
label_root = os.path.join(".", "Dataset", "raw_labels")
pic_root = os.path.join(".", "Dataset", "raw_screenshots")
sample_root = [os.path.join(pic_root, x)
    for x in os.listdir(pic_root)]

# load and wrap the data into dataloader
train_loader, cv_loader, test_loader = data_load.data_load(sample_root, label_root)

CNN_model = model.toho_CNN()
CNN_model = CNN_model.to(device)

epochs = 150
losses, cv_losses = PokeAIMaster(CNN_model, epochs, train_loader, cv_loader)

test = plt.imread(os.path.join(sample_root[0], "0834.jpg"))
test = T.ToTensor()(test)
o = CNN_model(torch.stack([test]).to(device))
o.detach().cpu().numpy()

torch.save(CNN_model.state_dict(), "CNN_param.pth")

