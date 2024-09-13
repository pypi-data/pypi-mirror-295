import albumentations as A
import numpy as np 
import imgaug.augmenters as iaa

def randAugmenter():
    augmentors = [
        A.ElasticTransform(alpha=250.0,always_apply=True),
        A.RandomRotate90(),
                A.Flip(),
                A.Transpose(),
                A.OpticalDistortion(p=1.0, distort_limit=1.0),
                A.OneOf([
                    A.GaussNoise(),
                ], p=0.2),
                A.OneOf([
                    A.MotionBlur(p=.2),
                    A.MedianBlur(blur_limit=3, p=0.1),
                    A.Blur(blur_limit=3, p=0.1),
                ], p=0.2),
                A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=45, p=0.2),
                A.OneOf([
                    A.OpticalDistortion(p=0.3),
                    A.GridDistortion(p=.1),
                    A.PiecewiseAffine(p=0.3),
                ], p=0.2),
                A.OneOf([
                    A.CLAHE(clip_limit=2),
                    A.Sharpen(),
                    A.Emboss(),
                    A.RandomBrightnessContrast(),            
                ], p=0.3),
                A.HueSaturationValue(p=0.3)]

    aug_ind = np.random.choice(np.arange(1,len(augmentors)), 3, replace=False)
    aug = A.Compose([augmentors[0],
                    augmentors[aug_ind[0]],
                    augmentors[aug_ind[1]],
                    augmentors[aug_ind[2]]])
        # aug = A.Compose([self.augmentors[0], A.GridDistortion(p=1.0), self.augmentors[3], self.augmentors[1], self.augmentors[7]])
    return aug