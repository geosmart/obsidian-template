# 2word - Markdown转Word工具

将Markdown文档转换为Word格式（docx），支持自定义格式配置。

## 代码来源

本转换工具基于用户提供的 `md2word.py` 代码，该代码是经过测试的完整实现，包含：
- 完整的Markdown到Word转换功能
- 支持表格、代码块、引用、图片、Mermaid图表等多种元素
- 自动引号转换（英文引号→中文引号）
- 法律文书专用格式优化
- PDF嵌入优化

## 使用方法

### 基础转换
```bash
/2word input.md output.docx
```

### 指定格式转换
```bash
/2word --format=格式名称 input.md output.docx
```

### 使用预设格式
```bash
/2word --format=legal-standard input.md output.docx  # 法律文书标准格式
/2word --format=simple input.md output.docx          # 简化格式
/2word --format=default input.md output.docx         # 默认格式
```

### 自定义格式
```bash
/2word --format=my-custom input.md output.docx  # 使用自定义格式
```

## 支持的格式

### 1. default (默认格式)
- **适用场景**: 通用文档转换
- **特点**: 基于md2word.py，完整功能，标准Word格式
- **字体**: 仿宋_GB2312（中文正文）、Times New Roman（英文）
- **标题**: 仿宋_GB2312，小三号（15pt）加粗，居中
- **行距**: 1.5倍行距
- **页边距**: 上下2.54cm，左右3.18cm

### 2. legal-standard (法律文书标准格式)
- **适用场景**: 起诉状、答辩状、代理词等正式法律文书
- **特点**: 符合法院要求的正式格式，基于md2word.py
- **字体**: 仿宋_GB2312（中文）、Times New Roman（英文）
- **标题**: 小三号（15pt）加粗居中，二级标题小四号（12pt）加粗
- **页边距**: 上下2.54cm，左右3.18cm
- **特色功能**: 自动引号转换、法条引用格式、签名区域

### 3. simple (简化格式)
- **适用场景**: 工作记录、笔记、内部报告
- **特点**: 简洁易读，快速转换
- **字体**: Times New Roman（正文）、Arial（标题）
- **行距**: 1.15倍行距

### 4. 自定义格式
- **创建位置**: `.claude/memory/docxformats/my-custom.md`
- **使用方法**: 参考 `.claude/memory/docxformats/custom-template.md`
- **功能**: 完全自定义字体、段落、页面等所有格式

## 格式配置说明

### 配置文件位置
所有格式配置存储在 `.claude/memory/docxformats/` 目录中：
```
.claude/memory/docxformats/
├── default.md              # 默认格式
├── legal-standard.md       # 法律文书标准格式
├── simple.md              # 简化格式
├── custom-template.md     # 自定义模板
└── my-custom.md           # 您的自定义格式（需要您创建）
```

### 自定义格式创建步骤

#### 步骤1: 复制模板
```bash
cp .claude/memory/docxformats/custom-template.md .claude/memory/docxformats/my-format.md
```

#### 步骤2: 修改配置
编辑 `my-format.md`，根据您的喜好调整：
- 字体设置
- 段落间距
- 页面布局
- 颜色方案
- 列表样式
- 表格样式

#### 步骤3: 使用自定义格式
```bash
/2word --format=my-format input.md output.docx
```

### 格式配置内容

每个格式配置文件包含：
- **字体设置**: 中文字体、英文字体
- **段落设置**: 行距、缩进、对齐方式
- **标题设置**: 各级标题的字体、大小、样式
- **页面设置**: 纸张大小、页边距、页眉页脚
- **列表设置**: 有序列表、无序列表样式
- **表格设置**: 边框、表头、内容样式
- **特殊元素**: 引用、代码块、链接样式

## 使用示例

### 转换法律文书
```bash
# 使用法律文书标准格式
/2word --format=legal-standard 起诉状.md 起诉状.docx
/2word --format=legal-standard 答辩状.md 答辩状.docx

# 简化法律文书（快速草稿）
/2word --format=simple 起诉状草稿.md 起诉状草稿.docx
```

### 转换工作文档
```bash
# 使用默认格式
/2word 案件分析报告.md 案件分析报告.docx

# 使用简化格式（快速笔记）
/2word --format=simple 工作记录.md 工作记录.docx
```

### 转换自定义格式
```bash
# 首先创建自定义格式配置文件
# 然后使用该格式
/2word --format=my-style 研究报告.md 研究报告.docx
```

## 功能特性

### 支持的Markdown元素
- ✅ 标题（H1-H6）
- ✅ 段落和换行
- ✅ 粗体和斜体文本
- ✅ 有序和无序列表
- ✅ 表格
- ✅ 链接和图片
- ✅ 引用块
- ✅ 代码块和行内代码
- ✅ 水平分割线
- ✅ 脚注

### 转换特性
- ✅ 智能格式识别
- ✅ 自动编号（法律文书格式）
- ✅ 超链接保持
- ✅ 图片嵌入
- ✅ 表格优化
- ✅ 法条引用格式
- ✅ 案例引用格式

### 中文支持
- ✅ 完整的中文字体支持
- ✅ 中文编号系统（一、二、三...）
- ✅ 中文标点符号
- ✅ 法条引用格式
- ✅ 案件编号格式

## 高级用法

### 批量转换
虽然命令本身不支持批量转换，但可以结合shell命令：
```bash
for file in *.md; do
    /2word --format=legal-standard "$file" "${file%.md}.docx"
done
```

### 格式优先级
1. 用户指定格式（`--format=xxx`）
2. 当前目录配置（如存在 `.2word-format.md`）
3. 默认格式（default）

### 错误处理
- 如果指定格式不存在，自动回退到默认格式
- 如果输入文件不存在，显示错误信息
- 如果输出目录不存在，自动创建

## 格式配置示例

### 自定义法律事务所格式
在您的自定义格式文件中，可以设置：
- 事务所Logo和页眉
- 专用字体和颜色
- 法律条文专用格式
- 签名区域样式
- 附件格式

### 简化笔记格式
可以设置：
- 更大的字体（便于阅读）
- 更紧凑的行距
- 去除装饰性元素
- 快速列表样式

## 注意事项

1. **格式文件修改**: 修改格式配置后，需要重启Claude Code才能生效
2. **字体依赖**: 部分字体可能需要在系统中安装
3. **兼容性**: 转换后的Word文档兼容Microsoft Word 2010及以上版本
4. **备份**: 重要的自定义格式建议定期备份
5. **共享**: 可以在团队中共享格式配置，提升一致性

## 故障排除

### 常见问题

**Q: 转换后的格式不正确**
A: 检查格式配置文件是否正确，是否选择了正确的格式

**Q: 中文字体显示异常**
A: 确保系统安装了对应的中文字体，或使用默认字体

**Q: 自定义格式不生效**
A: 检查格式文件名是否正确（不含空格和特殊字符），格式配置是否符合规范

**Q: 表格格式错乱**
A: 检查Markdown表格语法是否正确，尝试简化表格结构

### 获取帮助
查看所有可用格式：
```bash
ls .claude/memory/docxformats/
```

查看格式配置详情：
```bash
Read .claude/memory/docxformats/格式名称.md
```
