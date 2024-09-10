import torch
from torch.utils.data import DataLoader, Dataset
from torch.nn.utils.rnn import pad_sequence
import numpy as np

def __collate_fn(batch):
    # 假设 batch 是一个包含 (data, label) 元组的列表
    # 需要在返回的data数据中加上批次维度
    data = [item[0] for item in batch]
    labels = [item[1] for item in batch]
    data_padded = pad_sequence(data, batch_first=True)
    data_permuted = data_padded.permute(0, 2, 1)
    labels = torch.tensor(labels, dtype=torch.long)  # 确保labels是长整型
    return data_permuted, labels


def train_val_test_dataloaders(data, train_size=0.8, val_size=0.1, test_size=0.1, batch_size=32, num_workers=0):
    """
    此函数里面不能再打乱数据集了，因为一旦打乱，一个批次中的数据序列长短会差异很大，后续会填充特别多的padding（因为经典CNN模型的输入要求是每个批次定长）
    故CNN用于文本分类时，数据集只能在获得词向量表示之前进行打乱。而且其实bert模型本事就对数据进行了填充，是否对模型效果有很大影响，还有待研究。
    :param data: 输入元组，可以是 [reviews, labels] 或 reviews_and_labels
    """
    # 确保数据集划分的比例总和为1
    assert train_size + val_size + test_size == 1.0, "The sum of train_size, val_size, and test_size must be 1.0"

    if len(data) == 2:
        data = list(zip(data[0], data[1]))
    elif len(data) == 1:
        data = data[0]
    else:
        raise ValueError("Invalid number of arguments. Expected 1 or 2 arguments.")

    data_size = len(data)
    train_end_index = int(train_size * data_size)
    val_end_index = int((train_size + val_size) * data_size)
    train_data = data[:train_end_index]
    val_data = data[train_end_index:val_end_index]
    test_data = data[val_end_index:]

    # 构建数据加载器
    train_loader = DataLoader(train_data, batch_size=batch_size, num_workers=num_workers,
                              collate_fn=__collate_fn)
    val_loader = DataLoader(val_data, batch_size=batch_size, num_workers=num_workers,
                            collate_fn=__collate_fn)
    test_loader = DataLoader(test_data, num_workers=num_workers, collate_fn=__collate_fn)

    return train_loader, val_loader, test_loader


def shuffle_texts_and_labels(texts, labels) -> (list, list):
    if len(texts) != len(labels):
        raise ValueError("The number of texts and labels must be equal.")

    texts = np.array(texts)
    labels = np.array(labels)

    random_indices = np.random.permutation(len(texts))
    shuffled_texts = list(texts[random_indices])
    shuffled_labels = list(labels[random_indices])

    return shuffled_texts, shuffled_labels
