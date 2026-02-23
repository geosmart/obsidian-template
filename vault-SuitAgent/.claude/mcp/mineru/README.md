# MinerU MCP 配置教程

MinerU 是一个强大的文档转换工具，可以将 PDF、图片等文档转换为 Markdown 格式。

## 🚀 一键安装

```bash
./install.sh
```

## ⚙️ 配置步骤

### 1. 获取 API 密钥
访问 [MinerU 官网](https://mineru.net) 注册账号并获取 API 密钥

### 2. 更新主配置文件
编辑 `.claude/mcp.json` 文件，将 `your_api_key_here` 替换为您的 API 密钥：

```json
{
  "mcpServers": {
    "mineru": {
      "command": "~/Library/Python/3.13/bin/mineru-mcp",
      "env": {
        "MINERU_API_KEY": "your_actual_api_key_here",
        "OUTPUT_DIR": "./",
        "OUTPUT_IN_SAME_DIR": "true",
        "KEEP_FILENAME": "true"
      }
    }
  }
}
```

**输出配置说明**：
- `OUTPUT_DIR`: `"./"` - 表示在原文件所在目录输出
- `OUTPUT_IN_SAME_DIR`: `"true"` - 强制在原文件同目录输出
- `KEEP_FILENAME`: `"true"` - 保持原文件名，只改扩展名为 `.md`

## 🔍 验证安装

```bash
~/Library/Python/3.13/bin/mineru-mcp --help
```

## 🚀 使用方法

### ⚠️ 重要：正确使用方式

**严禁使用Python脚本调用MCP**！MinerU已配置为MCP服务，必须通过Claude Code的MCP工具直接调用。

**正确使用方式**：
1. 在Claude Code对话中，直接使用mineru的MCP工具
2. **不要编写任何Python脚本来调用mineru**
3. **不要绕过MCP直接使用API**

### 📋 调用规范

在Claude Code中，mineru提供以下工具：
- `parse_documents` - 解析文档（主要工具）
- `get_ocr_languages` - 获取支持语言列表

**调用示例**：
```
用户：请解析这个身份证PDF文件
系统：直接调用 mineru.parse_documents() MCP工具
```

### 📁 输出文件规范

**严格要求**：
- ✅ **只生成一个同名Markdown文件**
- ❌ **不要生成JSON文件**
- ❌ **不要生成图片目录**
- ❌ **不要生成布局信息文件**
- ❌ **不要生成其他格式的文件**

**输出位置**：
- 输入文件：`张敏娟 身份证.pdf`
- 输出文件：`张敏娟 身份证.md`（同目录，同名，扩展名改为.md）

**Markdown文件内容**：
```markdown
# [文件名] 解析结果

## 关键信息提取
- 姓名: xxx
- 性别: xxx
- ...（结构化信息）
```

**重要**：
- ✅ **只包含结构化信息**
- ❌ **不要包含原始OCR文本**
- ❌ **不要包含技术说明**

### 🔧 MCP配置

当前系统已正确配置mineru MCP，路径：
- 配置文件：`.claude/mcp.json`
- 可执行文件：`~/Library/Python/3.13/bin/mineru-mcp`
- 工作模式：STDIO（标准MCP通信）

## 🆘 问题排查

- **命令未找到**: 确保路径正确 `~/Library/Python/3.13/bin/mineru-mcp`
- **API 密钥无效**: 检查密钥是否正确且有效
- **转换失败**: 确认文档格式支持

## 📚 更多文档

- **官方完整文档**: [OFFICIAL_DOCUMENTATION.md](OFFICIAL_DOCUMENTATION.md)
- **官方 GitHub**: [MinerU MCP 项目](https://github.com/opendatalab/MinerU/tree/dev/projects/mcp)

---

*MinerU MCP 配置教程*