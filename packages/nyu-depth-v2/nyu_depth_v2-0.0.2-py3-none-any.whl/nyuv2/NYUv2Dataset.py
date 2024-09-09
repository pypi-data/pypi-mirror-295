import h5py
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from torchvision.datasets.utils import download_url
from einops import rearrange
from pathlib import Path
from tqdm import tqdm
import random

class NYUv2Dataset(Dataset):
    """
    NYUv2Dataset class wrapping PyTorch Dataset class.

    Args:
        root_dir (str): The first number.
        save (bool): If true, then the images, depths, images containing the transformed images and depths.
        transform_image (torchvision.transforms.Compose): The transforms for the images.
        transform_depth (torchvision.transforms.Compose): The transforms for the depths.
    """
    def __init__(self,
                 root_dir : str,
                 save : bool = False,
                 transform_image : transforms.Compose = None,
                 transform_depth : transforms.Compose = None):

        super().__init__()
        self.root_dir : Path = Path(root_dir)
        self.filename : str = "nyu_depth_v2_labeled.mat"
        self.file : h5py.File = None
        self.save : bool = save

        self.images : list = []
        self.depths : list = []

        self.transform_depth = transform_depth
        self.transform_image = transform_image

        self.root_dir.mkdir(parents=True, exist_ok=True)
        self.download()
        self.load_data()
        self.save_data()

    def download(self):
        url : str = "http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v2/nyu_depth_v2_labeled.mat"

        if not (self.root_dir / self.filename).exists():
            print("downloading...")
            download_url(url, self.root_dir, self.filename)

    def load_data(self):
        print("loading data...")

        mat_file : Path = self.root_dir / self.filename
        self.file = h5py.File(mat_file, 'r')
        
        images : h5py._hl.dataset.Dataset = self.file["images"]
        depths : h5py._hl.dataset.Dataset = self.file["depths"]

        for i in tqdm(range(len(images))):
            image : np.ndarray = images[i]
            depth : np.ndarray = depths[i]
            image = rearrange(images[i], "c w h -> h w c")
            depth = rearrange(depths[i], "w h -> h w 1")

            image_transform : np.ndarray = image
            depth_transform : np.ndarray = depth

            seed = random.randint(0,2**32)
            if self.transform_image is not None:
                reset_seed(seed)
                image_transform = self.transform_image(image)

            if self.transform_depth is not None:
                reset_seed(seed)
                depth_transform = self.transform_depth(depth)

            self.images.append(image_transform)
            self.depths.append(depth_transform)

    def save_data(self):
        images_save_dir : Path = self.root_dir / "images"
        depths_save_dir : Path = self.root_dir / "depths"
        transform_save_dir : Path = self.root_dir / "transform"
        MAX_RANGE : int = 10 # max depth is 10 meter.

        if self.save:
            images_save_dir.mkdir(parents=True, exist_ok=True)
            depths_save_dir.mkdir(parents=True, exist_ok=True)
            transform_save_dir.mkdir(parents=True, exist_ok=True)

            images : h5py._hl.dataset.Dataset = self.file["images"]
            depths : h5py._hl.dataset.Dataset = self.file["depths"]
            
            for i in range(len(images)):
                image : np.ndarray = images[i]
                depth : np.ndarray = depths[i]

                image = rearrange(images[i], "c w h -> h w c")
                depth = rearrange(depths[i], "w h -> h w 1")

                image = np.array(image)
                depth = np.array(depth / MAX_RANGE * 65535).astype(np.uint16)
                
                cv2.imwrite(images_save_dir / f"{i}.png", image)
                cv2.imwrite(depths_save_dir / f"{i}.png", depth)

    def __len__(self):
        assert len(self.images) == len(self.depths)
        return len(self.images)
    
    def __getitem__(self, idx):
        image = self.images[idx]
        depth = self.depths[idx]

        return image, depth

def reset_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
