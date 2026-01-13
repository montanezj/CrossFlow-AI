import torch
import torch.nn as nn
import torch.nn.functional as F

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # Layer 1: Takes sensor data -> Hidden thinking layer
        self.linear1 = nn.Linear(input_size, hidden_size)
        # Layer 2: Hidden -> Output actions
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # Activation Function: ReLU (Rectified Linear Unit)
        # It helps the AI learn non-linear patterns (like "stop ONLY if close")
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        """Helper to save the brain to a file"""
        import os
        model_folder_path = './models'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)