# 格式配置目录

> Last updated: 2025-11-13
> 本目录包含用于2word命令的格式配置文件

## 文件说明

### 预设格式

| 文件名 | 格式名称 | 适用场景 | 特点 |
|--------|----------|----------|------|
| `default.md` | default | 通用文档转换 | 标准Word格式，宋体+黑体 |
| `legal-standard.md` | legal-standard | 法律文书 | 符合法院要求，包含编号系统 |
| `simple.md` | simple | 内部文档 | 简洁快速，Times New Roman+Arial |

### 自定义格式

| 文件名 | 用途 | 说明 |
|--------|------|------|
| `custom-template.md` | 自定义模板 | 用于创建个人自定义格式的模板文件 |
| `my-custom.md` | 用户自定义 | 需要您手动创建，用于保存个人格式配置 |

## 使用方法

### 查看可用格式
```bash
ls .claude/memory/docxformats/
```

### 使用预设格式
```bash
/2word --format=default input.md output.docx
/2word --format=legal-standard input.md output.docx
/2word --format=simple input.md output.docx
```

### 创建自定义格式
1. 复制模板：
   ```bash
   cp .claude/memory/docxformats/custom-template.md .claude/memory/docxformats/my-format.md
   ```

2. 编辑配置文件：
   ```bash
   Read .claude/memory/docxformats/my-format.md
   Edit .claude/memory/docxformats/my-format.md
   ```

3. 使用自定义格式：
   ```bash
   /2word --format=my-format input.md output.docx
   ```

## 格式配置内容

每个格式配置包含以下部分：

- **字体设置**: 中英文字体选择
- **段落设置**: 行距、缩进、对齐方式
- **标题样式**: 各级标题的格式
- **页面设置**: 边距、页眉页脚、页码
- **列表样式**: 有序列表、无序列表样式
- **表格样式**: 表格边框、表头、内容格式
- **特殊元素**: 引用、代码块、链接样式
- **法律文书特有格式**: 编号系统、签名区域、法条引用等

## 最佳实践

1. **命名规范**: 使用英文和数字，避免特殊字符
2. **测试验证**: 修改格式后先测试简单文档
3. **备份重要格式**: 定期备份自定义格式配置
4. **团队共享**: 可以将好的格式配置分享给团队

## 格式优先级

1. 用户指定格式（`--format=xxx`）
2. 当前目录配置（如存在 `.2word-format.md`）
3. 默认格式（default）

## 注意事项

- 修改格式配置后，需要重启Claude Code才能生效
- 确保系统安装了格式配置中指定的中文字体
- 格式配置使用Markdown编写，便于阅读和修改
- 复杂格式可能需要多次测试和调整

## 获取帮助

查看格式配置详情：
```bash
Read .claude/memory/docxformats/格式名称.md
```

查看命令使用说明：
```bash
Read .claude/commands/2word.md
```
