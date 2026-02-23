# MCP实现指南

**版本**: 1.0
**状态**: 生效中
**最后更新**: 2025-11-20

## 🎯 问题解决方案总结

根据用户反馈的核心问题：**使用"OCR"、"识别"、"解析"等关键词时，Agent无法正确触发对应的MCP工具**，我们已经完成了完整的解决方案部署。

## ✅ 已完成的配置更新

### 1. 核心规范文档
- ✅ [`MCP_TRIGGER_PATTERNS.md`](./MCP_TRIGGER_PATTERNS.md) - 触发词识别规范
- ✅ [`RESPONSIVE_AGENT_MECHANISM.md`](./RESPONSIVE_AGENT_MECHANISM.md) - 响应式调用机制
- ✅ [`DOCUMENT_PROCESSING_STANDARDS.md`](./DOCUMENT_PROCESSING_STANDARDS.md) - 文档处理强制规范

### 2. 系统级配置
- ✅ [`CLAUDE.md`](../../CLAUDE.md) - 主系统MCP触发规范
- ✅ [`fallback.json`](../fallback.json) - 备用方案配置

### 3. Subagent配置更新
- ✅ **DocAnalyzer** - 已更新MCP触发规范
- ✅ **EvidenceAnalyzer** - 已更新MCP触发规范
- ✅ **Writer** - 已更新MCP触发规范
- ✅ **IssueIdentifier** - 已更新MCP触发规范
- ✅ **其他7个Agent** - 已批量更新配置

## 🔧 关键配置要点

### Subagent配置结构
每个Subagent现在都包含：

```yaml
---
name: AgentName
description: 职能描述，必须主动使用(MUST BE PROACTIVELY USED)mineru MCP进行PDF/图片OCR处理
tools: ["Read", "Bash", "Grep", "Write", "Edit", "Glob", "Skill"]
color: agent_color
---
```

### MCP触发词规范
每个Subagent都包含：

```markdown
## 🚨 MCP自动触发规范

**必须立即响应以下触发词**：
- ✅ "OCR" → 立即调用mineru.parse_documents()
- ✅ "识别" → 立即调用mineru.parse_documents()
- ✅ "解析" → 立即调用mineru.parse_documents()
- ✅ "提取文字" → 立即调用mineru.parse_documents()
- ✅ "文字识别" → 立即调用mineru.parse_documents()

**响应原则**：
- ❌ 不要询问用户："请问您希望我做什么？"
- ❌ 不要要求明确："请提供更具体的要求"
- ✅ 立即调用MCP工具
- ✅ 先处理，后分析
```

## 📋 实现机制说明

### 1. 立即响应流程
```mermaid
flowchart TD
    A[用户请求] --> B{包含触发词?}
    B -->|包含OCR/识别/解析| C[立即调用mineru.parse_documents()]
    B -->|不包含| D[常规Agent处理]
    C --> E[生成Markdown文件]
    E --> F[返回结果]
    D --> G[完成]
    F --> G
```

### 2. 强制执行关键词
使用官方推荐的强制执行关键词：
- `必须主动使用(MUST BE PROACTIVELY USED)`
- `MCP自动触发规范`
- `立即调用`

### 3. 工具权限配置
所有Subagent都已添加`"Skill"`工具，确保能够访问MCP工具。

## 🎯 测试验证

### 测试用例
以下场景现在应该能够正确触发MCP工具：

1. **直接OCR请求**：
   ```
   用户：我需要OCR这个身份证PDF
   期望：立即调用mineru.parse_documents()
   ```

2. **识别请求**：
   ```
   用户：请识别这个营业执照图片
   期望：立即调用mineru.parse_documents()
   ```

3. **解析请求**：
   ```
   用户：解析这个起诉状
   期望：立即调用mineru.parse_documents()
   ```

4. **Subagent调用**：
   ```
   用户：使用DocAnalyzer处理这个合同PDF
   期望：DocAgent检测到触发词，立即调用MCP
   ```

## 🚨 重要注意事项

### 禁止行为
- ❌ **不要询问用户**具体需求
- ❌ **不要绕过MCP**直接使用其他工具
- ❌ **不要先分析后处理**
- ❌ **不要编写Python脚本**调用MCP

### 必须行为
- ✅ **立即识别触发词**
- ✅ **直接调用MCP工具**
- ✅ **先处理，后分析**
- ✅ **只生成Markdown文件**

## 📊 配置验证清单

每个Subagent配置检查：
- [ ] description包含`MUST BE PROACTIVELY USED`
- [ ] tools包含`"Skill"`
- [ ] 包含MCP自动触发规范
- [ ] 包含响应原则说明
- [ ] 包含触发词列表

## 🔄 后续维护

### 新增Subagent
当新增Subagent时，必须：
1. 在description中添加MCP强制使用说明
2. 在tools中添加"Skill"工具
3. 添加MCP自动触发规范部分

### 配置更新
当MCP工具更新时：
1. 更新触发词列表
2. 更新调用函数名称
3. 更新相关文档

## 📞 技术支持

### 相关文档
- [MCP触发词识别规范](./MCP_TRIGGER_PATTERNS.md)
- [响应式Agent调用机制](./RESPONSIVE_AGENT_MECHANISM.md)
- [文档处理强制规范](./DOCUMENT_PROCESSING_STANDARDS.md)
- [MinerU MCP配置](../mcp/mineru/README.md)

### 配置文件位置
- 主配置：`../../CLAUDE.md`
- Subagent配置：`../../agents/*.md`
- 备用配置：`../fallback.json`
- 规范文档：`./standards/*.md`

---

**总结**：通过以上完整的配置更新，系统现在应该能够正确识别和响应用户的OCR、识别、解析等触发词，并立即调用对应的MCP工具进行处理。