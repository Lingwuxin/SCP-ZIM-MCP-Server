"""
HTML 内容处理器
使用 BeautifulSoup 处理 SCP Wiki 的 HTML 内容，提取正文部分
"""

from bs4 import BeautifulSoup, Tag
import re
import os
from typing import Optional, Dict, List, Union


class SCPHtmlProcessor:
    """SCP HTML 内容处理器"""

    def __init__(self):
        """
        初始化处理器

        Args:
            html_file_path: HTML 文件路径
        """
        self.soup: Optional[BeautifulSoup] = None
        self.page_content_div: Optional[Tag] = None

    def process_html(self, html_content: str) -> None:
        self.soup = BeautifulSoup(html_content, 'html.parser')
        # 移除不需要的元素
        self._remove_unwanted_elements()
        # 提取正文部分
        found_div = self.soup.find('div', id='page-content')
        self.page_content_div = found_div if isinstance(
            found_div, Tag) or found_div is None else None

    def _remove_unwanted_elements(self):
        """移除不需要的HTML元素"""
        if not self.soup:
            return

        # 要移除的元素选择器列表
        unwanted_selectors = [
            # 脚本和样式
            'script',
            'style',

            # 导航和菜单
            'nav',
            '.top-bar',
            '.mobile-top-bar',
            '.side-block',

            # 页脚和授权信息
            '.footer',
            '.licensebox',
            '#licensebox',
            '.footnotes-footer',
            '.footer-wikiwalk-nav'
            # 其他不需要的元素
            '#skrollr-body',
            'iframe',

            # 可折叠块（通常包含不重要信息）
            '.collapsible-block',

            # 图片块（如果不需要图片描述）
            # '.scp-image-block',
        ]

        for selector in unwanted_selectors:
            elements = self.soup.select(selector)
            for element in elements:
                element.decompose()  # 完全移除元素

    def extract_image_sources(self) -> str:
        if not self.page_content_div:
            return ''
        print(f"extract_image_sources:当前为测试版本，提取一个图片的src，待优化")
        image_source = ''

        # 查找所有img标签
        img_tags = []
        if isinstance(self.page_content_div, Tag):
            img_tags = self.page_content_div.find_all('img')

        for img in img_tags:
            if isinstance(img, Tag):  # 确保是Tag对象
                src = img.get('src')
                if src and isinstance(src, str):  # 确保src是字符串
                    # 去除相对路径前缀 "../"
                    if src.startswith('../'):
                        src = src[3:]  # 移除 "../"
                    elif src.startswith('./'):
                        src = src[2:]  # 移除 "./"

                    image_source = src
                # 只拿第一个
                # 从soup中删除这个img
                img.decompose()
                break

        return image_source


if __name__ == "__main__":
    processor = SCPHtmlProcessor()
    processor.process_html(
        "<html><body><div id='page-content'>Hello, SCP!</div></body></html>")
    print(processor.page_content_div)
