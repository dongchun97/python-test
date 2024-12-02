from torch.utils.data import Dataset
from PIL import Image
import os 

class MyData(Dataset):
    def __init__(self) -> None:
        super().__init__()


    def __getitem__(self, index) -> Any:
        return super().__getitem__(index) 