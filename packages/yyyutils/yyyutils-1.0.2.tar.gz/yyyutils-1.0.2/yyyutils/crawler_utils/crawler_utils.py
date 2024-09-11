import openpyxl
import os
import json
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl.styles import Alignment
from yyyutils.data_structure_utils import DictUtils
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyperclip
import asyncio
import re
import subprocess
import ast
from pyppeteer import launch


class CrawlerUtils:
    """
    用于爬虫的静态工具类
    """
    def __init__(self):
        pass

    @staticmethod
    def set_excel_wrap_text(path: str, sheet_name: str = 'Sheet1', column_width: int = 50,
                            horizontal_alignment: str = 'center', vertical_alignment: str = 'center'):
        if not os.path.exists(path):
            raise FileNotFoundError("File not found")
        if not path.endswith('.xlsx'):
            raise ValueError("File is not an Excel file")
        # 打开 Excel 文件
        workbook = openpyxl.load_workbook(path)

        # 选择要操作的表格
        sheet = workbook[sheet_name]
        for column in sheet.columns:
            sheet.column_dimensions[column[0].column_letter].width = column_width
        # 遍历每行每列，并设置单元格的格式
        for row in sheet.iter_rows():
            for cell in row:
                # 设置单元格的文本换行
                cell.alignment = Alignment(wrapText=True, horizontal=horizontal_alignment, vertical=vertical_alignment)

        # 保存更改
        workbook.save(path)

    @staticmethod
    def extract_args(url):
        res = list(map(list, re.findall(r'[?,&]?(.*?=.*?)(&|$)', url)))
        res[0][0] = res[0][0].split('?')[1]
        args = [i[0] for i in res]
        if args:
            return args
        else:
            print("No args found in URL")
            return None

    @staticmethod
    def charset_finder(soup: BeautifulSoup) -> str:
        """
        找到网页的编码格式
        :param soup:
        :return:
        """
        try:
            charset = soup.find('meta', attrs={'http-equiv': 'Content-Type'})['content'].split('=')[1]
        except:
            charset = soup.find('meta', attrs={'charset': True})['charset']
        if not charset:
            print("Charset not found, using default (UTF-8)")
            charset = 'UTF-8'
        return charset

    """
    def data_formatter(data_text: str):
        data = data_text.split('\n')
        data = [d.lstrip() for d in data if d]
        data = [d.rstrip(',') for d in data if d]
        if data[0][-1] == ':':
            for i in range(len(data)):
                if data[i] and data[i][-1] == ':' and data[i + 1][-1] == ':':
                    raise ValueError("Invalid data format")
            data = {data[i][:-1]: data[i + 1] for i in range(0, len(data), 2) if data[i]}
        else:
            for d in data:
                if d and d[-1] == ':':
                    raise ValueError("Invalid data format")
            data = [i.split(': ') for i in data]
            data = {i[0]: i[1] for i in data if len(i) == 2}
        return data
    
    
    
    def value_comparer(text1: str, text2: str) -> list:
        text1 = data_formatter(text1)
        text2 = data_formatter(text2)
        if len(text1) != len(text2):
            raise ValueError("The two texts have different lengths")
        diff = []
        for key, value in text1.items():
            if text2[key] != value:
                diff.append(key)
        return diff
    
    
    def key_comparer(text1: str, text2: str) -> bool:
        text1 = data_formatter(text1)
        text2 = data_formatter(text2)
        if len(text1) != len(text2):
            print("The two texts have different lengths")
            return False
        diff_keys = []
        for key in text1.keys():
            if key not in text2.keys():
                diff_keys.append(key)
        if diff_keys:
            print("The two texts have have same length but different keys")
            print(f"Keys {diff_keys} not found in text2")
            return False
        return True
    """

    @staticmethod
    def json_to_dataframes(json_data: dict, headers: list = None, all_floors=False):
        df_list = []
        value_lists = []
        for header in headers:
            # print(header)
            value_list = DictUtils.dict_data_extractor(json_data, header)  # 包含了所有层的数据
            # print(value_list)
            floors_set = set([i[1] for i in value_list])
            if len(floors_set) > 1:
                if all_floors:
                    value_list = [i[0] for i in value_list]
                    try:
                        df_list.append(pd.DataFrame(value_list, columns=[header]))
                    except:
                        print(
                            f"数据格式错误，即将返回 {header} 当前层的数据列表，请检查数据格式后自行调用 pd.DataFrame() 函数")
                        value_lists.append(value_list)
                    continue
                choose_floor = input(f"现在有多层数据含有{header}，请从以下数据选择需要的层数：{floors_set} --> ")
                if choose_floor == 'all':
                    """返回该key的所有层数的数据 -> list"""
                    value_list = [i[0] for i in value_list]
                    try:
                        df_list.append(pd.DataFrame(value_list, columns=[header]))
                    except:
                        print(
                            f"数据格式错误，即将返回 {header} 当前层的数据列表，请检查数据格式后自行调用 pd.DataFrame() 函数")
                        value_lists.append(value_list)
                    continue
                if int(choose_floor) not in floors_set:
                    raise ValueError("Invalid floor number")
                value_list = [i[0] for i in value_list if i[1] == int(choose_floor)]
            else:
                value_list = [i[0] for i in value_list]
            try:
                df_list.append(pd.DataFrame(value_list, columns=[header]))
            except:
                print(
                    f"数据格式错误，即将返回 {header} 当前层的错误数据列表，请检查数据格式后自行调用 pd.DataFrame() 函数")
                value_lists.append(value_list)
        if value_lists:
            return value_lists
        df_list = pd.concat(df_list, axis=1)
        return df_list

    @staticmethod
    def extract_non_empty_from_excel(file_path):
        # 从 Excel 文件中加载数据
        df = pd.read_excel(file_path)

        result_list = []

        # 遍历每一列，提取不为空的内容到结果列表
        for col in df.columns:
            col_data = df[col].dropna().tolist()
            result_list += col_data

        return result_list

    @staticmethod
    def get_cookies_headers_by_cURL_auto(url, databag_name, driver_path="D:/msedgedriver.exe"):
        options = Options()
        service = Service(driver_path)
        options.use_chromium = True
        driver = webdriver.Edge(service=service, options=options)

        # 访问目标网页
        driver.get(url)

        # 等待页面加载完成
        time.sleep(8)

        # 打开开发者工具（F12 或 Ctrl+Shift+I）
        # 创建ActionChains对象
        actions = ActionChains(driver)

        # 模拟按下F12键
        actions.send_keys(Keys.F12).perform()
        # 等待开发者工具加载完成
        time.sleep(8)

        # 切换到Network标签页
        webdriver.ActionChains(driver).send_keys(Keys.F1).perform()  # 打开命令菜单
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys('Network').perform()  # 输入Network并选择
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()  # 确认选择

        # 刷新页面以捕获网络请求
        driver.refresh()

        # 等待网络请求捕获完成
        time.sleep(5)

        # 执行JavaScript代码，模拟右键点击并复制为cURL
        driver.execute_script("""
            // 定位到网络面板
            var networkPanel = document.querySelector('div[aria-label="Network"]');

            // 寻找具有特定名称的请求
            var targetRequestName = arguments[0]; // 从Selenium传入的请求名称
            var requests = networkPanel.querySelectorAll('.request-list-item .request-name');
            var targetRequest = null;
            for (var i = 0; i < requests.length; i++) {
                if (requests[i].textContent.includes(targetRequestName)) {
                    targetRequest = requests[i].closest('.request-list-item');
                    break;
                }
            }

            // 如果找到了请求
            if (targetRequest) {
                // 获取请求元素的尺寸和位置
                var rect = targetRequest.getBoundingClientRect();
                var x = rect.left + rect.width / 2;
                var y = rect.top + rect.height / 2;

                // 创建并触发右键点击事件
                var event = new MouseEvent('contextmenu', {
                    view: window,
                    bubbles: true,
                    cancelable: true,
                    clientX: x,
                    clientY: y
                });
                targetRequest.dispatchEvent(event);

                // 等待并点击复制为cURL菜单项
                setTimeout(() => {
                    var copyAsCurl = document.querySelector('div[aria-label="Copy as cURL"]');
                    if (copyAsCurl) {
                        copyAsCurl.click();
                    }
                }, 1000);
            }
        """, databag_name)  #

        # 等待复制操作完成
        time.sleep(2)

        # 从剪贴板中获取cURL命令（需要使用pyperclip库）
        curl_command = pyperclip.paste()
        print(curl_command)

        # 关闭浏览器
        driver.quit()

    @staticmethod
    async def __main(base_url, databag_name, wait_time):
        """

        :param base_url: 是哪个网址
        :param databag_name: 是这个网址的哪个数据包
        :return:
        """
        browser = await launch({
            'executablePath': 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
            'headless': True,
            'dumpio': True
        })
        page = await browser.newPage()
        await page.goto(base_url)

        # 监听网络请求
        requests = []
        page.on('request', lambda req: requests.append(req))

        # 等待一些时间以便捕获请求
        await asyncio.sleep(wait_time)  # 根据需要调整等待时间

        # 获取 cookies
        cookies = await page.cookies()
        cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

        # 检查请求并找到特定名称的数据包
        for req in requests:
            if databag_name in req.url:  # 根据你的条件过滤请求
                url = req.url
                method = req.method
                headers = req.headers
                postData = req.postData  # 直接访问属性，而不是调用方法

                # 构造 cURL 命令
                curl_command = f"curl -X {method} '{url}'"
                for header, value in headers.items():
                    curl_command += f" \\\n  -H '{header}: {value}'"
                if cookie_str:
                    curl_command += f" \\\n  -H 'Cookie: {cookie_str}'"
                if postData:
                    curl_command += f" \\\n  -d '{postData}'"

                # print(curl_command)
                break

        await browser.close()
        return curl_command

    @staticmethod
    def __call_node_script(curl_command):
        node_script_path = 'D:/Python/Python38/Lib/site-packages/mytools/crawler_utils/curl_convert.js'  # 替换为实际路径
        # 将 curl_command 作为单个字符串参数传递
        result = subprocess.run(['node', node_script_path, curl_command],
                                capture_output=True,
                                text=True,
                                encoding='utf-8')  # 使用 utf-8 编码

        if result.returncode == 0:
            code = result.stdout
            # 使用正则表达式匹配字典
            cookies_pattern = r"cookies\s*=\s*({.*?})"
            headers_pattern = r"headers\s*=\s*({.*?})"
            params_pattern = r"params\s*=\s*({.*?})"

            # 搜索代码字符串以找到匹配的字典
            cookies_match = re.search(cookies_pattern, code, re.DOTALL)
            headers_match = re.search(headers_pattern, code, re.DOTALL)
            params_match = re.search(params_pattern, code, re.DOTALL)

            # 使用 ast.literal_eval 安全地评估字符串中的字典
            cookies_dict = ast.literal_eval(cookies_match.group(1)) if cookies_match else {}
            headers_dict = ast.literal_eval(headers_match.group(1)) if headers_match else {}
            params_dict = ast.literal_eval(params_match.group(1)) if params_match else {}

            # 打印提取出的字典
            # print("Cookies 字典:", cookies_dict)
            # print("Headers 字典:", headers_dict)
            # print("Params 字典:", params_dict)
            return code, cookies_dict, headers_dict, params_dict
        else:
            print("Error:", result.stderr)

    @staticmethod
    def get_databag_code_cookies_headers_params(request_url, databag_name, wait_time=5, need_save=False):
        curl_command = asyncio.run(CrawlerUtils.__main(request_url, databag_name, wait_time))
        python_code, cookies_dict, headers_dict, params_dict = CrawlerUtils.__call_node_script(curl_command)
        if need_save:
            with open('dictionaries.json', 'w', encoding='utf-8') as f:
                json.dump({'cookies': cookies_dict, 'headers': headers_dict, 'params': params_dict}, f,
                          ensure_ascii=False, indent=4)
        return python_code, cookies_dict, headers_dict, params_dict

    @staticmethod
    def read_json_file(file_path) -> dict:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data


if __name__ == '__main__':
    # options = Options()
    # service = Service("D:/msedgedriver.exe")
    # options.use_chromium = True
    # driver = webdriver.Edge(service=service, options=options)
    # driver.get('https://s.weibo.com/weibo?q=%E6%95%8F%E6%84%9F%E8%AF%8D')
    # time.sleep(2)
    code, cookies_dict, headers_dict, params_dict = CrawlerUtils.get_databag_code_cookies_headers_params(
        'https://s.weibo.com/weibo?q=%E6%95%8F%E6%84%9F%E8%AF%8D',
        'weibo?q=%E6%95%8F%E6%84%9F%E8%AF%8D', wait_time=2)
    print(cookies_dict)
    print(headers_dict)
    print(params_dict)
