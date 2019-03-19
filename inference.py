import json
import torch
from torch import nn, optim
from torch.optim import lr_scheduler
from torch.autograd import Variable

from PIL import Image
import numpy as np
import torchvision
import torch
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler
import torch.nn as nn

from commons import get_model, get_tensor

with open('class_to_idx.json') as f:
	class_to_idx = json.load(f)

idx_to_class = {v:k for k, v in class_to_idx.items()}

model = get_model()

def get_rice_name(image_bytes):
	tensor = get_tensor(image_bytes)
	outputs = model.forward(tensor)
	_, prediction = outputs.max(1)
	category = prediction.item()
	rice_name = idx_to_class[category]
	return category, rice_name
