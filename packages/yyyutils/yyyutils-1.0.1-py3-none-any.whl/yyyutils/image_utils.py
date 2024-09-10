"""
用于处理图像的工具类
"""
import cv2
import numpy as np


class ImageUtils:
    """
    用于处理图像的静态工具类
    """
    @staticmethod
    def resize_image(image, width=None, height=None, inter=cv2.INTER_AREA):
        """
        调整图像大小
        :param image: 输入图像
        :param width: 输出图像宽度
        :param height: 输出图像高度
        :param inter: 缩放插值方法
        :return: 调整后的图像
        """
        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        resized = cv2.resize(image, dim, interpolation=inter)
        return resized

    @staticmethod
    def rotate_image(image, angle, center=None, scale=1.0):
        """
        旋转图像
        :param image: 输入图像
        :param angle: 旋转角度
        :param center: 旋转中心
        :param scale: 缩放比例
        :return: 旋转后的图像
        """
        (h, w) = image.shape[:2]
        if center is None:
            center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(image, M, (w, h))
        return rotated

    @staticmethod
    def crop_image(image, x, y, w, h):
        """
        裁剪图像
        :param image: 输入图像
        :param x: 裁剪区域左上角x坐标
        :param y: 裁剪区域左上角y坐标
        :param w: 裁剪区域宽度
        :param h: 裁剪区域高度
        :return: 裁剪后的图像
        """
        cropped = image[y:y + h, x:x + w]
        return cropped

    @staticmethod
    def flip_image(image, flip_code):
        """
        翻转图像
        :param image: 输入图像
        :param flip_code: 翻转方向
        :return: 翻转后的图像
        """
        flipped = cv2.flip(image, flip_code)
        return flipped

    @staticmethod
    def add_padding(image, top, bottom, left, right, color=(0, 0, 0)):
        """
        添加边缘填充
        :param image: 输入图像
        :param top: 上边缘填充长度
        :param bottom: 下边缘填充长度
        :param left: 左边缘填充长度
        :param right: 右边缘填充长度
        :param color: 填充颜色
        :return: 填充后的图像
        """
        padded = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return padded

    @staticmethod
    def add_noise(image, mean=0, std=10):
        """
        添加噪声
        :param image: 输入图像
        :param mean: 均值
        :param std: 标准差
        :return: 加噪声后的图像
        """
        noisy = image.astype(np.int16) + np.random.normal(mean, std, image.shape)
        noisy = np.clip(noisy, 0, 255).astype(np.uint8)
        return noisy

    @staticmethod
    def add_salt_pepper_noise(image, amount=0.05):
        """
        添加椒盐噪声
        :param image: 输入图像
        :param amount: 噪声比例
        :return: 加噪声后的图像
        """
        output = image.copy()
        h, w = image.shape[:2]
        num_salt = np.ceil(amount * h * w * 0.5)
        num_pepper = np.ceil(amount * h * w * 0.5)
        for i in range(num_salt):
            x = np.random.randint(0, w)
            y = np.random.randint(0, h)
            output[y, x] = 255
        for i in range(num_pepper):
            x = np.random.randint(0, w)
            y = np.random.randint(0, h)
            output[y, x] = 0
        return output

    @staticmethod
    def add_gaussian_noise(image, mean=0, var=0.01):
        """
        添加高斯噪声
        :param image: 输入图像
        :param mean: 均值
        :param var: 方差
        :return: 加噪声后的图像
        """
        noise = np.random.normal(mean, var ** 0.5, image.shape)
        noisy = image + noise
        return noisy

    @staticmethod
    def add_speckle_noise(image, mean=0, var=0.01):
        """
        添加斑点噪声
        :param image: 输入图像
        :param mean: 均值
        :param var: 方差
        :return: 加噪声后的图像
        """
        noise = image.copy()
        h, w = image.shape[:2]
        noise = np.random.normal(mean, var ** 0.5, (h, w))
        noisy = image + image * noise
        return noisy

    @staticmethod
    def add_poisson_noise(image, mean=0):
        """
        添加泊松噪声
        :param image: 输入图像
        :param mean: 均值
        :return: 加噪声后的图像
        """
        noisy = np.random.poisson(image * mean) / mean
        return noisy

    @staticmethod
    def add_speckle_noise_with_mask(image, mask, mean=0, var=0.01):
        """
        添加斑点噪声
        :param image: 输入图像
        :param mask: 噪声掩码
        :param mean: 均值
        :param var: 方差
        :return: 加噪声后的图像
        """
        noise = np.random.normal(mean, var ** 0.5, image.shape)
        noisy = image + image * noise * mask
        return noisy

    @staticmethod
    def add_gaussian_blur(image, ksize=5):
        """
        添加高斯模糊
        :param image: 输入图像
        :param ksize: 高斯核大小
        :return: 加模糊后的图像
        """
        blurred = cv2.GaussianBlur(image, (ksize, ksize), 0)
        return blurred

    @staticmethod
    def add_median_blur(image, ksize=5):
        """
        添加中值模糊
        :param image: 输入图像
        :param ksize: 中值核大小
        :return: 加模糊后的图像
        """
        blurred = cv2.medianBlur(image, ksize)
        return blurred

    @staticmethod
    def add_bilateral_blur(image, d=9, sigmaColor=75, sigmaSpace=75):
        """
        添加双边模糊
        :param image: 输入图像
        :param d: 领域大小
        :param sigmaColor: 颜色空间标准差
        :param sigmaSpace: 坐标空间标准差
        :return: 加模糊后的图像
        """
        blurred = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)
        return blurred

    @staticmethod
    def add_gamma_correction(image, gamma=1.0):
        """
        添加伽马校正
        :param image: 输入图像
        :param gamma: 伽马值
        :return: 加校正后的图像
        """
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        gamma_corrected = cv2.LUT(image, table)
        return gamma_corrected

    @staticmethod
    def add_clahe(image, clipLimit=2.0, tileGridSize=(8, 8)):
        """
        添加CLAHE
        :param image: 输入图像
        :param clipLimit: 裁剪限值
        :param tileGridSize: 块大小
        :return: 加CLAHE后的图像
        """
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
        cl1 = clahe.apply(image)
        return cl1

    @staticmethod
    def add_histogram_equalization(image):
        """
        添加直方图均衡化
        :param image: 输入图像
        :return: 加均衡化后的图像
        """
        equalized = cv2.equalizeHist(image)
        return equalized

    @staticmethod
    def add_adaptive_equalization(image, kernel_size=3):
        """
        添加自适应均衡化
        :param image: 输入图像
        :param kernel_size: 卷积核大小
        :return: 加均衡化后的图像
        """
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl1 = clahe.apply(image)
        adapteq = cv2.adaptiveThreshold(cl1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, kernel_size, 2)
        return adapteq

    @staticmethod
    def add_image(image1, image2, alpha=0.5):
        """
        叠加图像
        :param image1: 输入图像1
        :param image2: 输入图像2
        :param alpha: 透明度
        :return: 叠加后的图像
        """
        if image1.shape != image2.shape:
            raise ValueError("Image shapes must match")
        blended = cv2.addWeighted(image1, alpha, image2, 1 - alpha, 0)
        return blended

    @staticmethod
    def subtract_image(image1, image2):
        """
        减去图像
        :param image1: 输入图像1
        :param image2: 输入图像2
        :return: 减去后的图像
        """
        if image1.shape != image2.shape:
            raise ValueError("Image shapes must match")
        subtracted = cv2.subtract(image1, image2)
        return subtracted

    @staticmethod
    # 二值化图像
    def binarize_image(image, threshold=127, max_value=255, type=cv2.THRESH_BINARY):
        """
        二值化图像
        :param image: 输入图像
        :param threshold: 阈值
        :param max_value: 最大值
        :param type: 阈值类型
        :return: 二值化后的图像
        """
        ret, binary = cv2.threshold(image, threshold, max_value, type)
        return binary

    @staticmethod
    # 反二值化图像
    def inverse_binarize_image(image, threshold=127, max_value=255, type=cv2.THRESH_BINARY):
        """
        反二值化图像
        :param image: 输入图像
        :param threshold: 阈值
        :param max_value: 最大值
        :param type: 阈值类型
        :return: 反二值化后的图像
        """
        ret, binary = cv2.threshold(image, threshold, max_value, type)
        inverse_binary = cv2.bitwise_not(binary)
        return inverse_binary

    @staticmethod
    # 图像形态学操作
    def morphology_operation(image, operation, kernel):
        """
        图像形态学操作
        :param image: 输入图像
        :param operation: 操作类型
        :param kernel: 卷积核
        :return: 操作后的图像
        """
        if operation == "erosion":
            result = cv2.erode(image, kernel)
        elif operation == "dilation":
            result = cv2.dilate(image, kernel)
        elif operation == "opening":
            result = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        elif operation == "closing":
            result = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        elif operation == "gradient":
            result = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
        elif operation == "top_hat":
            result = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
        elif operation == "black_hat":
            result = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
        else:
            raise ValueError("Invalid operation")
        return result

    @staticmethod
    # 图像梯度
    def gradient(image):
        """
        图像梯度
        :param image: 输入图像
        :return: 梯度图像
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0)
        grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        return grad

    @staticmethod
    # 图像梯度方向
    def gradient_direction(image):
        """
        图像梯度方向
        :param image: 输入图像
        :return: 梯度方向图像
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0)
        grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1)
        grad_dir = cv2.phase(grad_x, grad_y, angleInDegrees=True)
        return grad_dir


if __name__ == '__main__':
    # 识别验证码图片中的字母并输出
    import pytesseract
    from PIL import Image
    import os

    # 读取验证码图片
    img_path = r'D:\PycharmProjects Prefession\proj_git\py_choose_lessons-master\chooselessonassistance\cap.jpg'
    img = cv2.imread(img_path)

    # 灰度化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 二值化
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # 识别验证码
    result = pytesseract.image_to_string(Image.fromarray(binary))

    print(result)
