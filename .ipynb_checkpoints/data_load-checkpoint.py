import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import torch
import torchvision.transforms as T
from torch.utils.data import random_split
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

import os
import os.path

if "__name__" == "__main__":
    # Path of dataset
    label_root = os.path.join(".", "Dataset", "raw_labels")
    pic_root = os.path.join(".", "Dataset", "raw_screenshots")
    sample_root = [os.path.join(pic_root, x)
        for x in os.listdir(pic_root)]

class LoadMyDataset(Dataset):
    """
    Load the dataset and do the specified transformations on it.
    """
    def __init__(self, sample_root, label_root, transforms=None, target_transforms=None):
        self.sample_root = sample_root # sample 目录列表
        self.label_root = label_root
        self.dataset = self.LoadData(self.sample_root, self.label_root) # 要能读取很多数据
        self.transforms = transforms
        self.target_transforms = target_transforms

    def __len__(self):
        return len(self.dataset[1])
    
    def __getitem__(self, index):
        if torch.is_tensor(index):
            index = index.tolist()
        
        sample = self.dataset[0][index]
        if self.transforms:
            sample = self.transforms(sample)

        label = self.dataset[1][index]
        if self.target_transforms:
            label = self.target_transforms(label)

        return sample, label

    def LoadData(self, sample_root, label_root):
        print("\n" + "="*10 + "load the data" + "="*10)
        
        # load the labels from .csv files and concatenate them in 2D tensor
        labels = pd.DataFrame()
        # flag = 0
        for i in sorted(os.listdir(label_root)):
            filename = os.path.join(label_root, i)
            temp = pd.read_csv(filename, header=None)
            # print("\rtemp:", temp.shape, end="")
            labels = pd.concat([labels, temp], axis=0)
            
            # ===================ONLY FOR DEBUG===================
            # flag += 1
            # if flag == 1:
            #     break
        
        labels = torch.FloatTensor(labels.values)
        print(f"labels matrix: {labels.shape}\n")

        # load the screenshot from each folder and concatenate them in 4D tensor, 
        # where the 1st dim refers to batch
        samples = []
        # flag = 0
        for i in sample_root:
            for j in sorted(os.listdir(i)):
                filename = os.path.join(i, j)
                temp = plt.imread(filename)
                temp = T.ToTensor()(temp)
                samples.append(temp)
                print(f"\r{j} done!", end="")
            
            # ===================ONLY FOR DEBUG===================
            # flag += 1
            # if flag == 1:
            #     break
        
        samples = torch.stack(samples)
        print(f"\n\nsamples matrix: {samples.shape}")
        print("="*35 + "\n\n")

        samples, labels = data_preprocessing(samples, labels)
        print("="*10 + "after processing" + "="*10)
        print(f"labels matrix:{labels.shape}\n\nsamples matrix:{samples.shape}")
        print("="*35)
        return (samples, labels)

def data_preprocessing(samples, labels): # 预处理数据，将0向量数据删除
    samples_temp = []
    labels_temp = []
    for i in range(labels.shape[0]):
        if labels[i].tolist() != [0, 0, 0, 0, 0]:
            samples_temp.append(samples[i])
            labels_temp.append(labels[i])
    
    samples = torch.stack(samples_temp)
    labels = torch.stack(labels_temp)

    return samples, labels

def data_load(sample_root, label_root):
    data = LoadMyDataset(sample_root, label_root, transforms=None)
    batch_size = 512

    train_nums = round(len(data)*0.8)
    cv_nums = round((len(data) - train_nums)*0.6)
    test_nums = len(data) - train_nums - cv_nums

    train_data, cv_data, test_data = random_split(data, [train_nums, cv_nums, test_nums])

    train_loader = DataLoader(
        train_data,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True,
        drop_last=True
    )
    cv_loader = DataLoader(
        cv_data,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True,
        drop_last=True
    )
    test_loader = DataLoader(
        test_data,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True,
        drop_last=True
    )
    return train_loader, cv_loader, test_loader