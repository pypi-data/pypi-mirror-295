import torch
import colorama


def test(model, test_loader, read_model_path=None, debug=False, classes: list = None, debug_num=10):
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
            pred = torch.argmax(output, dim=1)
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
    print('Test Accuracy: {:.2f}%'.format(100 * test_acc / test_num))


if __name__ == '__main__':
    pass
