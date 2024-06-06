# import os
# import cv2
# import pandas as pd
# from torch.utils.data import Dataset
# import albumentations as A
# from albumentations.pytorch import ToTensorV2

# class ISICDataset(Dataset):
#     def __init__(self, csv, imgs_path, labels_path, transform=None, training=True):
#         '''
#         csv -> file csv
#         imgs_path -> percorso delle immagini
#         labels_path -> percorso delle etichette
#         transform -> funzione usata per il set di addestramento per trasformare le immagini
#         '''
#         self.transform = transform
#         self.training = training
#         self.df = pd.read_csv(csv)
#         self.imgs_path = [os.path.join(imgs_path, i) for i in self.df['image_name']]
#         self.labels_path = [os.path.join(labels_path, i.replace('.jpg', '_segmentation.png')) for i in self.df['image_name']]

#     def __getitem__(self, index):
#         img = cv2.imread(self.imgs_path[index])[:, :, ::-1]  # Leggi l'immagine in formato BGR e converti in RGB
#         label = cv2.imread(self.labels_path[index], cv2.IMREAD_GRAYSCALE)  # Leggi l'etichetta in scala di grigi
        
#         if self.transform:
#             data = self.transform(image=img, mask=label)
#             img = data['image']
#             label = data['mask'] / 255  # Normalizza l'etichetta nell'intervallo [0, 1]
            
#         return img, label

#     def __len__(self):
#         return len(self.df)

# # Definisci le trasformazioni
# def get_transforms(training=True):
#     if training:
#         transform = A.Compose([
#             A.Resize(width=512, height=512),
#             A.RandomRotate90(),
#             A.Flip(p=0.5),
#             A.ShiftScaleRotate(shift_limit=0, scale_limit=(-0.2, 0.1), rotate_limit=40, p=0.5),
#             A.RandomBrightnessContrast(brightness_limit=0.5, contrast_limit=0.1, p=0.5),
#             A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=100, val_shift_limit=80),
#             A.GaussNoise(),
#             A.OneOf([
#                 A.ElasticTransform(),
#                 A.GridDistortion(),
#                 A.OpticalDistortion(distort_limit=0.5, shift_limit=0)
#             ]),
#             A.Normalize(
#                 mean=[0.485, 0.456, 0.406],
#                 std=[0.229, 0.224, 0.225],
#                 max_pixel_value=255.0,
#                 p=1.0
#             ),
#             ToTensorV2()
#         ])
#     else:
#         transform = A.Compose([
#             A.Resize(width=512, height=512),
#             A.Normalize(
#                 mean=[0.485, 0.456, 0.406],
#                 std=[0.229, 0.224, 0.225],
#                 max_pixel_value=255.0,
#                 p=1.0
#             ),
#             ToTensorV2()
#         ])
#     return transform

from torch.utils.data import Dataset
import torchvision.transforms as transforms

from PIL import Image

import numpy as np
import random
import torch
import os 


class ISICDataset(Dataset):

    def init(self,
                 img_dir,
                 annotation_filepath,
                 transform=False):

        self.img_dir = img_dir
        self.transform = transform
        self.filepaths = []
        self.labels = []
        self.classes = []
        self.melanome=[]
        self.seborrheic_keratosis=[]

        # just pick the classes
        with open(annotation_filepath, 'r') as f:
            for line in f.readlines():
                self.classes = line.strip().split(",")[1:]

        # useless?
        self.classes_to_idx = {cls_name:idx for idx,cls_name in enumerate(self.classes)}

        # now pick all the classes
        with open(annotation_filepath, 'r') as f:
            for line in f.readlines()[1:]:
                line_array = line.strip().split(",")
                filename = line_array[0]
                class_array = np.array(line_array[1:])
                
                # Check if there are elements equal to '1.0' in the class_array
                indices = np.where(class_array == '1.0')[0]
                # If there are, take the index of the first occurrence
                if len(indices) > 0:
                    #!!!! 0 -> Melanoma, 1 -> seborrheic_keratosis
                    #print("Filename: ",filename)
                    class_id = indices[0]
                    #print("class_id: ",class_id)
                    self.filepaths.append(os.path.join(img_dir, f'{filename}.jpg'))
                    self.labels.append(int(class_id))
                    if class_id == 0:
                        self.melanome.append(filename)
                    else:
                        self.seborrheic_keratosis.append(filename)


    def len(self):
        return len(self.filepaths)


    def getitem(self, idx):

        img = Image.open(self.filepaths[idx]).convert('RGB')
        label = np.array(self.labels[idx])

        if self.transform:
            img = self.transform(img)

        return idx, img, label
    
    def getlabels(self):
        return self.labels