from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # 导入Service


def 初始化_普通模式(浏览器路径, 驱动器路径, 启动参数=None):
    """
    初始化谷歌浏览器。

    参数：
        - 浏览器路径: Chrome 浏览器的可执行文件路径。
        - 驱动器路径: ChromeDriver 的路径。
        - 启动参数: 启动浏览器时的自定义参数（可选），列表形式，例如 ["--headless", "--incognito", "--disable-gpu"]。

    返回值：
        - 成功返回浏览器驱动器对象。
        - 失败返回 False。
    """
    try:
        chrome选项 = Options()

        # 设置浏览器的可执行文件路径
        chrome选项.binary_location = 浏览器路径

        # 添加自定义的启动参数
        if 启动参数:
            for 参数 in 启动参数:
                chrome选项.add_argument(参数)

        # 使用Service对象来设置驱动器路径
        服务 = Service(驱动器路径)

        # 启动浏览器
        驱动器对象 = webdriver.Chrome(service=服务, options=chrome选项)

        return 驱动器对象  # 成功返回浏览器对象
    except Exception:
        return False  # 失败返回 False