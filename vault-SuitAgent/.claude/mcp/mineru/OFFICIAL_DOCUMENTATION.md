# MinerU MCP 官方文档

*本文档基于 [MinerU MCP 官方 GitHub](https://github.com/opendatalab/MinerU/tree/dev/projects/mcp) 整理*

## 1. 项目介绍和功能特性

MinerU MCP-Server 基于 FastMCP 框架构建，作为 MinerU API 的接口，用于将文档转换为 Markdown 格式。

### 核心功能
- **文档提取**: 支持多种格式文档 (PDF、PPT、DOC、图片等)
- **批量处理**: 同时处理多个文档文件
- **OCR 支持**: 可选启用 OCR 功能处理扫描版文档
- **多语言支持**: 支持多种语言识别
- **自动化流程**: 自动处理与 MinerU API 的交互
- **本地解析**: 支持调用本地部署的 MinerU 模型

## 2. 安装要求和步骤

### 系统要求
- Python >= 3.10

### 安装方式

#### 使用 pip 安装 (推荐)
```bash
pip install mineru-mcp==1.0.0
```

#### 从源码安装
```bash
git clone https://github.com/opendatalab/MinerU.git
cd MinerU/projects/mcp
uv venv
source .venv/bin/activate
uv pip install -e .
```

#### 从 GitHub 直接安装
```bash
pip install --break-system-packages --user git+https://github.com/opendatalab/MinerU.git@dev#subdirectory=projects/mcp
```

## 3. 配置说明和示例

项目支持通过环境变量配置或 .env 文件。

### Claude Code 配置示例

#### 安装包运行方式
```json
{
  "mcpServers": {
    "mineru": {
      "command": "~/Library/Python/3.13/bin/mineru-mcp",
      "env": {
        "MINERU_API_BASE": "https://mineru.net",
        "MINERU_API_KEY": "your_api_key_here",
        "OUTPUT_DIR": "./output/mineru",
        "USE_LOCAL_API": "false"
      }
    }
  }
}
```

#### 使用本地 API 配置
```json
{
  "mcpServers": {
    "mineru": {
      "command": "~/Library/Python/3.13/bin/mineru-mcp",
      "env": {
        "MINERU_API_BASE": "https://mineru.net",
        "MINERU_API_KEY": "your_api_key_here",
        "OUTPUT_DIR": "./output/mineru",
        "USE_LOCAL_API": "true",
        "LOCAL_MINERU_API_BASE": "http://localhost:8080"
      }
    }
  }
}
```

## 4. 使用方法和 API 说明

### 可用工具
1. **parse_documents**: 统一接口，支持处理本地文件和 URL
2. **get_ocr_languages**: 获取 OCR 支持的语言列表

### parse_documents 参数说明

| 参数 | 类型 | 说明 | 默认值 | 适用模式 |
|------|------|------|--------|----------|
| file_sources | 字符串 | 文件路径或 URL，多个可用逗号或换行符分隔 | - | 全部 |
| enable_ocr | 布尔值 | 是否启用 OCR 功能 | false | 全部 |
| language | 字符串 | 文档语言，默认"ch"中文 | "ch" | 全部 |
| page_ranges | 字符串 | 指定页码范围 (远程 API) | None | 远程 API |

### 直接运行服务
```bash
# SSE 传输模式
mineru-mcp --transport sse

# Streamable HTTP 传输模式
mineru-mcp --transport streamable-http

# 标准 stdio 模式 (默认)
mineru-mcp
```

服务默认在 http://localhost:8001 启动：
- SSE 模式使用 /sse 路由
- Streamable HTTP 模式使用 /mcp 路由

## 5. 环境变量配置

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `MINERU_API_BASE` | MinerU 远程 API 的基础 URL | `https://mineru.net` |
| `MINERU_API_KEY` | MinerU API 密钥 | 必需 |
| `OUTPUT_DIR` | 转换后文件的保存路径 | `./downloads` |
| `USE_LOCAL_API` | 是否使用本地 API 进行解析 | `false` |
| `LOCAL_MINERU_API_BASE` | 本地 API 的基础 URL | `http://localhost:8080` |

## 6. 故障排除和常见问题

### API 密钥问题
- **问题**: 无法连接 MinerU API 或返回 401 错误
- **解决**: 检查 API 密钥是否正确设置，确保密钥有效且未过期

### 文件路径问题
- **问题**: 使用 parse_documents 工具处理本地文件时报错
- **解决**: 确保使用绝对路径或正确的相对路径

### MCP 服务调用超时
- **问题**: 处理大型文档时出现超时错误
- **解决方案**:
  - 处理较小的文件
  - 分批处理大型文档
  - 重启 MCP 客户端
  - 检查网络连接稳定性

### 优雅退出服务
- 服务运行时，可通过按 `Ctrl+C` 来优雅退出

## 7. Docker 部署

项目支持使用 Docker 进行部署，使你能在任何支持 Docker 的环境中快速启动 MinerU MCP 服务器。

### 使用 Docker Compose
```bash
cp .env.example .env
docker-compose up -d
```

### 手动构建 Docker 镜像
```bash
docker build -t mineru-mcp:latest .
docker run -p 8001:8001 --env-file .env mineru-mcp:latest
```

## 8. 使用示例

### 基本文档转换
在 Claude Code 中，您可以：
1. 直接上传 PDF、图片等文档文件
2. 请求："请将这个文档转换为 Markdown 格式"
3. 系统会自动调用 MinerU MCP 进行转换

### 批量处理
```
用户：请处理这些文档：document1.pdf, document2.docx, image1.jpg
系统：[自动调用 MinerU MCP 批量转换]
```

### 启用 OCR
```
用户：这个 PDF 是扫描件，请启用 OCR 进行文字识别
系统：[使用 OCR 功能处理扫描文档]
```

---

*文档版本: 基于 MinerU MCP dev 分支*
*最后更新: 2025-11-20*