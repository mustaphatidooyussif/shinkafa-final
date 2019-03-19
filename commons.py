import io
import urllib.request as ur
import torch
import torch.nn as nn
from torchvision import models
from PIL import Image
import torchvision.transforms as transforms
import boto3

def get_model():
    url = 'https://s3.amazonaws.com/rice-classifier-frontend/checkpoint.pth'
    # checkpoint_path = 'models/checkpoint.pth'
    f = ur.urlopen(url)
    checkpoint_path = io.BytesIO(f.read())
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    model = checkpoint['model']
    model.classifier = checkpoint['classifier']
    model.load_state_dict(checkpoint['state_dict'])
    model.class_to_idx = checkpoint['class_to_idx']
    optimizer = checkpoint['optimizer']
    epochs = checkpoint['epochs']
    
    for param in model.parameters():
        param.requires_grad = False
        
    return model, checkpoint['class_to_idx']

def get_tensor(image_bytes):
	my_transforms = transforms.Compose([transforms.Resize(256),
        				    transforms.CenterCrop(224),
        				    transforms.ToTensor(),
        				    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                             					  std=[0.229, 0.224, 0.225])])
	image = Image.open(io.BytesIO(image_bytes))
	return my_transforms(image).unsqueeze(0)

  