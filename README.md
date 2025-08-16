# SCP-ZIM-MCP-Server

一个基于 MCP (Model Context Protocol) 的 SCP 基金会文档处理服务器，用于从 ZIM 文件中提取 SCP 文档并转换为 Markdown 格式。

## 概述

该项目提供了一个 MCP 服务器，能够：
- 从 SCP 基金会的 ZIM 离线文档中提取特定 SCP 项目内容
- 处理 HTML 内容并转换为 Markdown 格式
- 提取和保存图片资源
- 为 AI 助手和知识管理工具提供标准化的 SCP 文档访问接口

## 功能特性

- **ZIM 文件读取**: 支持读取 SCP 基金会离线计划提供的 ZIM 格式文档
- **HTML 处理**: 自动处理和清理 HTML 内容，提取核心文档内容
- **Markdown 转换**: 将 SCP 文档转换为结构化的 Markdown 格式
- **图片提取**: 自动提取并保存文档中的图片资源
- **MCP 协议支持**: 通过 MCP 协议为 AI 助手提供工具接口

## 项目结构

```
SCP-ZIM-MCP-Server/
├── src/
│   ├── main.py                 # MCP 服务器主程序
│   ├── handle_zim/
│   │   └── readzim.py         # ZIM 文件读取处理
│   └── html_parser/
│       └── html_processor.py   # HTML 内容处理
├── .env.example               # 环境变量示例
├── .env                       # 环境变量配置
├── pyproject.toml            # 项目依赖配置
├── README.md                 # 项目文档
└── LICENSE                   # 许可证
```

## 安装与配置

### 环境要求

- Python 3.8+
- SCP 基金会 ZIM 文件（可从 [SCP基金会离线计划](https://scp-wiki-cn.wikidot.com/offline) 获取）
### 安装依赖

使用 [uv](https://github.com/astral-sh/uv) 启动项目：

```bash
uv run src/main.py
```

### 环境配置

1. 复制环境变量示例文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，设置必要的环境变量：

```env
# SCP ZIM 文件路径
SCP_OFFLINE_ZIM_PATH=/path/to/scp-wiki_zh_all_2024-10.zim

# Markdown 输出目录
SCP_MD_OUTPUT_DIR=/path/to/output/directory
```

## 使用方法

### 启动 MCP 服务器

```bash
python src/main.py
```

服务器将在 `http://0.0.0.0:8765` 上启动，使用 SSE (Server-Sent Events) 传输协议。

### MCP 工具

服务器提供以下 MCP 工具：

#### `make_md(scp_id)`

从 ZIM 文件中提取指定 SCP 项目的内容并生成 Markdown 文件。

**参数：**
- `scp_id` (str): SCP 项目 ID，如 "scp-001", "scp-173", "scp-8002"

**返回：**
- 生成的 Markdown 内容

**示例：**
```python
# 提取 SCP-173 的文档
content = make_md("scp-173")
```

#### `read_md(scp_id)`

读取已生成的 SCP Markdown 文件。

**参数：**
- `scp_id` (str): SCP 项目 ID，如 "scp-001", "scp-173", "scp-8002"

**返回：**
- Markdown 文件的完整内容

**示例：**
```python
# 读取 SCP-173 的 Markdown 文档
content = read_md("scp-173")
```

### 工作流程

1. **提取文档**: 使用 `make_md()` 工具从 ZIM 文件中提取 SCP 文档
2. **生成 Markdown**: 自动处理 HTML 内容并转换为 Markdown 格式
3. **保存资源**: 提取并保存文档中的图片到指定目录
4. **读取文档**: 使用 `read_md()` 工具读取生成的 Markdown 文件

## 核心组件

### ReadZIM 类

负责 ZIM 文件的读取和内容提取：

```python
zim = ReadZIM(zim_file_path)
zim.read_zim()
content = zim.get_content(scp_id)
```

### SCPHtmlProcessor 类

处理从 ZIM 文件中提取的 HTML 内容：

```python
html_processor = SCPHtmlProcessor()
html_processor.process_html(content)
img_sources = html_processor.extract_image_sources()
```

## 配置选项

| 环境变量 | 描述 | 示例值 |
|---------|------|--------|
| `SCP_OFFLINE_ZIM_PATH` | SCP ZIM 文件的完整路径 | `/data/scp-wiki_zh_all_2024-10.zim` |
| `SCP_MD_OUTPUT_DIR` | Markdown 文件输出目录 | `/output/scp-docs` |

## 相关项目

- [SCP-Obsidian](https://github.com/Lingwuxin/SCP-Obsidian): 使用此 MCP 服务器构建 SCP 基金会 Obsidian 知识图谱的工具

## 许可证

本项目采用 [LICENSE](LICENSE) 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进此项目。

## 支持

如果您遇到问题或有建议，请在 GitHub 上创建 Issue。