import torch
import copy
import os
import pandas as pd
import time
import torch.nn as nn
import matplotlib.pyplot as plt
import keyboard
import numpy as np
import colorama
from yyyutils.decorator_utils import DecoratorUtils
from typing import Callable


class TrainTestUtils():
    """
    用于训练和测试模型的工具类，可以自定义预测标签的函数和求loss的函数
    """
    def __init__(self):
        self.predict_label_func = TrainTestUtils.__default_predict_label
        self.loss_func = TrainTestUtils.__default_loss_func

    @staticmethod
    def __default_predict_label(output):
        return torch.argmax(output, dim=1)

    @staticmethod
    def __default_loss_func(output, target):
        return nn.CrossEntropyLoss()(output, target)

    @DecoratorUtils.validate_input
    def train(self, model, train_loader, test_loader, epoches: int, lr: float, predict_label_func: Callable = None,
              loss_func: Callable = None,
              read_model_path: str = None,
              batch_debug: bool = False, stop_by_esc: bool = False):
        """
        :param model:
        :param train_loader:
        :param test_loader:
        :param epoches:
        :param lr:
        :param predict_label_func: 预测标签的函数，默认使用torch.argmax(output, dim=1)
        :param loss_func: 求出loss的函数，默认使用nn.CrossEntropyLoss()(output, target)
        :param read_model_path:
        :param batch_debug:
        :param stop_by_esc:
        :return:
        """
        if predict_label_func is not None:
            self.predict_label_func = predict_label_func
        if loss_func is not None:
            self.loss_func = loss_func
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = model.to(device)
        colorama.init()
        if read_model_path is not None:
            model.load_state_dict(torch.load(read_model_path))

        optimizer = torch.optim.Adam(model.parameters(), lr=lr)

        best_model_wts = copy.deepcopy(model.state_dict())

        best_acc = 0.0

        train_loss_list = []
        test_loss_list = []
        train_acc_list = []
        test_acc_list = []
        token = False
        since = time.time()
        for epoch in range(epoches):
            print('-' * 30)
            print('Epoch {}/{}'.format(epoch + 1, epoches))
            train_loss = 0.0
            train_correct = 0
            test_loss = 0.0
            test_correct = 0
            train_num = 0
            test_num = 0
            for i, (bx, by) in enumerate(train_loader):
                batch_since = time.time()
                bx = bx.to(device)
                by = by.to(device)

                model.train()
                output = model(bx)
                pre_label = self.predict_label_func(output)
                # print(by)
                # print(pre_label)
                loss = self.loss_func(output, by)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                train_loss += loss.item() * bx.size(0)
                train_correct += torch.sum(pre_label == by).item()
                # print(train_correct)
                train_num += bx.size(0)
                if stop_by_esc:
                    if keyboard.is_pressed('esc'):
                        if epoch == 0:
                            raise KeyboardInterrupt('第一次迭代未完成！！！')
                        token = True
                        print("\nEsc键被按下，退出训练并保存模型")
                        break
                if batch_debug:
                    print('\r\ttrain Batch Debug: {} [{}/{} bt]\t{:.2f}s'.format(
                        colorama.Fore.GREEN + str(
                            round((i + 1) / len(train_loader) * 100)) + '%' + colorama.Style.RESET_ALL,
                        i + 1, len(train_loader), (time.time() - batch_since) * (len(train_loader) - i - 1)), end='')
            if token:
                break
            # print()
            # print()
            for i, (bx, by) in enumerate(test_loader):
                batch_since = time.time()
                bx = bx.to(device)
                by = by.to(device)

                model.eval()
                output = model(bx)
                pre_label = self.predict_label_func(output)
                loss = self.loss_func(output, by)

                test_loss += loss.item() * bx.size(0)
                test_correct += torch.sum(pre_label == by).item()
                test_num += bx.size(0)
                batch_time_used = time.time() - batch_since
                if batch_debug:
                    print('\r\ttest Batch Debug: {} [{}/{} bt]\t{:.2f}s'.format(
                        colorama.Fore.GREEN + str(
                            round((i + 1) / len(test_loader) * 100)) + '%' + colorama.Style.RESET_ALL,
                        i + 1, len(test_loader), batch_time_used * (len(test_loader) - i - 1)), end='')
            if not token:
                train_loss_list.append(train_loss / train_num)
                test_loss_list.append(test_loss / test_num)
                train_acc_list.append(float(train_correct) / train_num)
                test_acc_list.append(float(test_correct) / test_num)
                print()
                print('Train Loss: {:.4f} Acc: {:.4f} '.format(train_loss_list[-1], train_acc_list[-1]))
                print('Test Loss: {:.4f} Acc: {:.4f} '.format(test_loss_list[-1], test_acc_list[-1]))

                if test_acc_list[-1] > best_acc:
                    best_acc = test_acc_list[-1]
                    best_model_wts = copy.deepcopy(model.state_dict())

                time_used = time.time() - since
                print('All time used: {}h {}m {:.2f}s'.format(int(time_used // 3600), int((time_used % 3600) // 60),
                                                              time_used % 60))
        if token:
            num = epoch
        else:
            num = epoch + 1
        train_process = pd.DataFrame(
            {'epoch': range(1, num + 1), 'train_loss': train_loss_list, 'train_acc': train_acc_list,
             'test_loss': test_loss_list, 'test_acc': test_acc_list})

        return best_model_wts, train_process

    def save_best_model(self, best_model_wts, path):
        torch.save(best_model_wts, path)

    def plot_train_process(self, train_process):
        """
        plot train process
        """
        plot_name = os.path.basename(os.getcwd())

        plt.figure(figsize=(12, 4))
        plt.subplot(1, 2, 1)
        plt.plot(np.array(train_process['epoch']), np.array(train_process['train_loss']), 'ro-', label='train_loss')
        plt.plot(np.array(train_process['epoch']), np.array(train_process['test_loss']), 'bo-', label='eval_loss')
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.legend()
        plt.title(plot_name)

        plt.subplot(1, 2, 2)
        plt.plot(np.array(train_process['epoch']), np.array(train_process['train_acc']), 'ro-', label='train_acc')
        plt.plot(np.array(train_process['epoch']), np.array(train_process['test_acc']), 'bo-', label='eval_acc')
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.legend()
        plt.title(plot_name)
        plt.show()

    def test(self, model, test_loader, read_model_path=None, debug=False, classes: list = None, debug_num=10):
        colorama.init()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if read_model_path is not None:
            model.load_state_dict(torch.load(read_model_path))
        model.to(device)
        model.eval()
        test_acc = 0
        test_num = 0
        error_num = 0
        with torch.no_grad():
            for i, (dx, dy) in enumerate(test_loader):
                dx, dy = dx.to(device), dy.to(device)
                output = model(dx)
                pred = self.predict_label_func(output)
                test_acc += torch.sum(pred == dy).item()
                test_num += dx.size(0)
                if debug and i < debug_num:
                    if classes is None:
                        if pred.item() != dy.item():
                            error_num += 1
                            print(
                                colorama.Fore.RED + f"真实值: {pred.item()} ------- 预测值: {dy.item()}" + colorama.Style.RESET_ALL)
                        else:
                            print(f"真实值: {dy.item()} ------- 预测值: {pred.item()}")
                    else:
                        if pred.item() != dy.item():
                            error_num += 1
                            print(
                                colorama.Fore.RED + f"真实值: {classes[dy.item()]} ------- 预测值: {classes[pred.item()]}" + colorama.Style.RESET_ALL)
                        else:
                            print(f"真实值: {classes[dy.item()]} ------- 预测值: {classes[pred.item()]}")
                    if i == debug_num - 1:
                        print()
                        print(f"检测数量: {debug_num}，错误数量: {error_num}")
        print('Test Total Accuracy: {:.2f}%'.format(100 * test_acc / test_num))


if __name__ == '__main__':
    pass
