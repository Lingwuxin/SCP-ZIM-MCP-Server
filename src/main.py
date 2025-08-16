from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from html_parser.html_processor import SCPHtmlProcessor
from handle_zim.readzim import ReadZIM
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


load_dotenv()
SCP_OFFLINE_ZIM_PATH = os.getenv("SCP_OFFLINE_ZIM_PATH")
if not SCP_OFFLINE_ZIM_PATH:
    raise ValueError("请设置环境变量 SCP_OFFLINE_ZIM_PATH 指向 SCP ZIM 文件的路径")
SCP_MD_OUTPUT_DIR = os.getenv("SCP_MD_OUTPUT_DIR")
if not SCP_MD_OUTPUT_DIR:
    raise ValueError("请设置环境变量 SCP_MD_OUTPUT_DIR 指向 Markdown 输出目录的路径")
if SCP_MD_OUTPUT_DIR and SCP_MD_OUTPUT_DIR[-1] == '/':
    SCP_MD_OUTPUT_DIR = SCP_MD_OUTPUT_DIR[:-1]

mcp = FastMCP("read-zim", port=8765, host="0.0.0.0")


@mcp.tool()
def make_md(scp_id) -> str:
    """
    make the scp markdown file how to use the SCP ZIM.
    scp_id: The ID of the SCP to generate the markdown for. like "scp-001","scp-8002"
    """
    zim_file_path = SCP_OFFLINE_ZIM_PATH
    zim = ReadZIM(zim_file_path)
    zim.read_zim()
    content = zim.get_content(scp_id)
    html_processor = SCPHtmlProcessor()
    img_source = ''
    if content:
        html_processor.process_html(content)
        img_source = html_processor.extract_image_sources()
    else:
        return "获取内容失败"
    if html_processor.page_content_div:
        # 在这里生成 Markdown 格式的内容
        md_content = f"# {html_processor.page_content_div}"
        if img_source:
            if SCP_MD_OUTPUT_DIR is not None:
                zim.get_img(img_source, save_dir=SCP_MD_OUTPUT_DIR+"/images")
            else:
                raise ValueError("SCP_MD_OUTPUT_DIR 环境变量未设置")
        with open(f"{SCP_MD_OUTPUT_DIR}/{scp_id}.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        return md_content
    return "获取内容失败"


@mcp.tool()
def read_md(scp_id) -> str:
    """
    read the scp markdown file how to use the SCP ZIM.
    scp_id: The ID of the SCP to read the markdown for. like "scp-001","scp-8002"
    """
    md_file_path = f"{SCP_MD_OUTPUT_DIR}/{scp_id}.md"
    if not os.path.exists(md_file_path):
        raise FileNotFoundError(f"Markdown file not found: {md_file_path}")
    with open(md_file_path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    mcp.run(transport='sse')


if __name__ == "__main__":
    main()
