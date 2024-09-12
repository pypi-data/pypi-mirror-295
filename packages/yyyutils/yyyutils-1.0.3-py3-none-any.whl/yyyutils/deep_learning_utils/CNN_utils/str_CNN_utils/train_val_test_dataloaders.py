from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
import torch


class DataUtils:
    _exchange_dim = (0, 2, 1)
    _pad = True

    def __init__(self):
        self.__collate_fn = DataUtils.__default_collate_fn  # default_collate_fn

    @staticmethod
    def __default_collate_fn(batch):
        """
        默认的collate_fn函数，默认交换了一个batch中第二和第三维度，最终返回[batch_size, feature_num, feature_dim]
        :param batch:
        :return:
        """
        # 假设 batch 是一个包含 (data, label) 元组的列表
        # 需要在返回的data数据中加上批次维度
        data = [item[0] for item in batch]
        labels = [item[1] for item in batch]
        if DataUtils._pad:
            data = pad_sequence(data, batch_first=True)
            # print(1, data.shape)
        else:
            # size_set = set([item.shape for item in data])
            # print(size_set)
            data = torch.stack(data, dim=0)
            # print(2, data.shape)
        if DataUtils._exchange_dim is not None:
            data = data.permute(DataUtils._exchange_dim)
            # print(3, data.shape)
        labels = torch.tensor(labels, dtype=torch.long)  # 确保labels是长整型
        return data, labels

    def train_val_test_dataloaders(self, data, train_size=0.8, val_size=0.1, test_size=0.1, batch_size=32, shuffle=True,
                                   collate_fn=None,
                                   num_workers=0):
        """
        构建训练集、验证集、测试集的DataLoader
        :param data: 输入元组，可以是 [reviews, labels] 或 reviews_and_labels
        :param train_size:
        :param val_size:
        :param test_size:
        :param batch_size:
        :param shuffle:
        :param num_workers:
        :return:
        """
        if collate_fn is not None:
            self.__collate_fn = collate_fn
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
        # print(type(train_data[0][0]))
        # for data, target in train_data:
        #     print(data.shape, target)
        # print(val_data)
        # print(val_data[0][0].shape)

        # 构建数据加载器
        train_loader = DataLoader(train_data, batch_size=batch_size, num_workers=num_workers,
                                  collate_fn=self.__collate_fn, shuffle=shuffle)
        val_loader = DataLoader(val_data, batch_size=batch_size, num_workers=num_workers,
                                collate_fn=self.__collate_fn, shuffle=shuffle)
        test_loader = DataLoader(test_data, num_workers=num_workers, collate_fn=self.__collate_fn)
        # for i, (data, target) in enumerate(val_loader):
        #     print(data.shape, target)
        # for i, (data, target) in enumerate(test_loader):
        #     print(data, target)
        return train_loader, val_loader, test_loader
