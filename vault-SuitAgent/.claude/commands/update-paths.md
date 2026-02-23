# /update-paths - 更新路径引用

## 功能说明

自动更新项目中所有配置文件路径的引用，确保路径一致性。

## 使用方式

```bash
/update-paths
```

## 工作原理

1. 读取 `.claude/config/paths.yaml` 配置文件
2. 扫描所有 Agent 配置文件和 Command 配置文件
3. 自动替换旧的路径引用为新的路径引用
4. 生成更新报告

## 支持的路径替换

### 旧路径 → 新路径映射

| 旧路径 | 新路径 |
|--------|--------|
| `.claude/rules/AgentMapping.md` | `.claude/rules/AgentMapping.md` |
| `.claude/rules/AgentMapping.md` | `.claude/rules/AgentMapping.md` |
| `.claude/rules/WorkflowSystem.md` | `.claude/rules/WorkflowSystem.md` |
| `.claude/rules/AgentMapping.md` | `.claude/rules/AgentMapping.md` |

## 更新的文件类型

- ✅ Agent 配置文件：`.claude/agents/*.md`
- ✅ Command 配置文件：`.claude/commands/*.md`
- ✅ 主文档：`CLAUDE.md`

## SubAgent 工作流

```
1. Reader Agent
   ├─ 读取 paths.yaml 配置
   ├─ 解析路径映射规则
   └─ 识别需要更新的文件
   ↓
2. Updater Agent
   ├─ 扫描所有配置文件
   ├─ 执行路径替换
   └─ 生成更新报告
   ↓
3. Verifier Agent
   ├─ 验证所有路径存在
   ├─ 检查引用一致性
   └─ 输出验证结果
```

## 输出内容

### 更新报告示例

```markdown
# 路径引用更新报告

## 更新统计
- 扫描文件：15 个
- 更新文件：12 个
- 替换引用：24 处

## 更新详情

### Agent 配置文件 (10)
- ✅ DocAnalyzer.md - 3 处替换
- ✅ Scheduler.md - 2 处替换
- ✅ EvidenceAnalyzer.md - 2 处替换
- ✅ IssueIdentifier.md - 2 处替换
- ✅ Researcher.md - 2 处替换
- ✅ Writer.md - 3 处替换
- ✅ Strategist.md - 2 处替换
- ✅ Summarizer.md - 2 处替换
- ✅ Reporter.md - 2 处替换
- ✅ Reviewer.md - 2 处替换

### Command 配置文件 (2)
- ✅ new-case.md - 4 处替换
- ✅ evidence-review.md - 2 处替换

### 主文档 (1)
- ✅ CLAUDE.md - 3 处替换

## 验证结果
- ✅ 所有引用路径有效
- ✅ 没有遗漏的旧引用
- ✅ 引用格式一致
```

## 使用场景

### 场景 1：文件结构调整后
```bash
# 1. 修改 paths.yaml 中的路径配置
vim .claude/config/paths.yaml

# 2. 运行更新命令
/update-paths

# 3. 检查更新报告
# 所有相关文件自动更新
```

### 场景 2：日常维护
```bash
# 定期运行，确保路径一致性
/update-paths
```

## 技术实现

### 替换规则

```python
# 路径替换映射
replacements = {
    '.claude/rules/AgentMapping.md': '.claude/rules/AgentMapping.md',
    '.claude/rules/AgentMapping.md': '.claude/rules/AgentMapping.md',
}
```

### 文件扫描

```bash
# 查找需要更新的文件
find .claude/agents/ -name "*.md"
find .claude/commands/ -name "*.md"
```

### 替换执行

```bash
# 使用 sed 批量替换
sed -i 's|旧路径|新路径|g' file.md
```

## 注意事项

1. **备份建议**：重要更新前先提交 Git
2. **路径格式**：使用相对路径，确保跨平台兼容
3. **测试验证**：更新后验证所有引用正确
4. **版本控制**：paths.yaml 纳入版本控制

## 相关命令

- `/new-case` - 创建新案件（使用路径配置）
- `/evidence-review` - 证据质证（使用路径配置）
