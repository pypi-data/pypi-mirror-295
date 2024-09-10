from mytools.AllUtils.deep_learning_utils.CNN_utils.img_CNN_utils.data_partition import DataHandler
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import torch.utils.data as data


def train_val_test_dataloader(all_data_dir=None, split_test_rate=0.2, copy_flag=False, split_val_rate=0.2,
                              batch_size=32,
                              image_size=224, num_workers=2):
    """
    用于从分好类的图片文件夹中划分训练集和验证集，并返回对应的DataLoader
    """
    transforms_list = [transforms.Resize((image_size, image_size)), transforms.ToTensor()]
    if all_data_dir is not None:
        DataHandler.create_train_test_dir(all_data_dir, split_test_rate, copy_flag=copy_flag)
        mean, std = DataHandler.mean_std_normalize_images(all_data_dir)
        transforms_list.append(transforms.Normalize(mean, std))

    train_dataset = datasets.ImageFolder(root='./data/train', transform=transforms.Compose(transforms_list))
    test_dataset = datasets.ImageFolder(root='./data/test', transform=transforms.Compose(transforms_list))
    train_data, val_data = data.random_split(train_dataset,
                                             [round((1 - split_val_rate) * len(train_dataset)),
                                              round(split_val_rate * len(train_dataset))])
    train_loader = data.DataLoader(dataset=train_data, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = data.DataLoader(dataset=val_data, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    test_loader = data.DataLoader(dataset=test_dataset, shuffle=True)

    return train_loader, val_loader, test_loader
