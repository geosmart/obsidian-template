# SuitAgent 路径管理解决方案

## 问题背景

在架构不稳定期，文件路径经常变化，导致需要手动更新多个文件中的路径引用，容易遗漏和不一致。

## 解决方案：混合方案

采用 **"配置文件 + 自动更新工具"** 的混合方案，兼顾灵活性和自动化。

---

## 📁 核心文件

### 1. 配置文件
**位置**: `.claude/config/paths.yaml`

定义所有路径映射关系，作为单一真实来源。

```yaml
# 路径映射配置
rules:
  agent_mapping: .claude/rules/AgentMapping.md
  workflow_system: .claude/rules/WorkflowSystem.md

agent_directories:
  DocAnalyzer:
    primary: "02 - 📄 案件分析"
    secondary: [...]
```

### 2. 更新工具
**位置**: `.claude/tools/update_paths.py`

自动扫描并更新所有文件中的路径引用。

### 3. Command 定义
**位置**: `.claude/commands/update-paths.md`

定义 `/update-paths` 命令的使用方法。

---

## 🚀 使用方法

### 方式 1：直接运行 Python 脚本（推荐）

```bash
# 在项目根目录运行
python3 .claude/tools/update_paths.py
```

**优点**：
- ✅ 快速直接
- ✅ 无需额外配置
- ✅ 可集成到 Git hooks

### 方式 2：使用 Command（通过 AI）

```
/update-paths
```

**优点**：
- ✅ 自然语言交互
- ✅ AI 可以智能处理特殊情况
- ✅ 适合不熟悉命令行的用户

---

## 📋 工作流程

### 场景 1：文件结构调整后

```bash
# 1. 修改配置文件
vim .claude/config/paths.yaml

# 2. 运行更新工具
python3 .claude/tools/update_paths.py

# 3. 检查更新报告
# 工具会显示哪些文件被更新

# 4. 验证更新
git diff  # 查看变更
```

### 场景 2：定期维护

```bash
# 每次重构后运行一次
python3 .claude/tools/update_paths.py
```

### 场景 3：Git Hook 自动化

在 `.git/hooks/pre-commit` 中添加：

```bash
#!/bin/bash
# 提交前自动检查路径引用
python3 .claude/tools/update_paths.py
```

---

## 📊 工具输出示例

```bash
============================================================
SuitAgent 路径引用更新工具
============================================================

🔍 验证目标路径...
✅ 所有目标路径验证通过

🔍 扫描需要更新的文件...
找到 17 个文件需要检查

🔄 执行路径更新...

============================================================
更新报告
============================================================

📊 统计信息:
  - 扫描文件: 17 个
  - 更新文件: 3 个
  - 替换引用: 8 处

📝 更新详情:
✅ .claude/agents/DocAnalyzer.md (2 处)
  .claude/config/agent-mappings.yaml → .claude/rules/AgentMapping.md

✅ .claude/commands/new-case.md (4 处)
  .claude/config/case-directories.yaml → .claude/rules/AgentMapping.md

✅ CLAUDE.md (2 处)
  .claude/rules/workflows.md → .claude/rules/WorkflowSystem.md

🔍 检查遗留的旧引用...
✅ 没有发现遗留的旧引用

============================================================
✅ 路径引用更新完成！
============================================================
```

---

## 🎯 最佳实践

### 1. 配置文件维护

**何时更新**：
- 文件结构调整时
- 新增 Agent 时
- 修改目录命名时

**更新步骤**：
1. 修改 `paths.yaml`
2. 运行 `update_paths.py`
3. 提交变更

### 2. 路径引用规范

**推荐写法**：
```markdown
详见 [`.claude/rules/AgentMapping.md`](.claude/rules/AgentMapping.md)
```

**不推荐**：
```markdown
详见 AgentMapping.md
../config/agent-mappings.yaml
```

### 3. 版本控制

**纳入 Git 的文件**：
- ✅ `.claude/config/paths.yaml` - 配置文件
- ✅ `.claude/tools/update_paths.py` - 更新工具
- ✅ `.claude/commands/update-paths.md` - 命令定义

**不需要纳入**：
- ❌ 临时更新报告
- ❌ 备份文件

---

## 🔧 高级用法

### 1. 自定义替换规则

编辑 `update_paths.py` 中的 `PATH_REPLACEMENTS`：

```python
PATH_REPLACEMENTS = {
    '旧路径': '新路径',
    # 添加你的替换规则
}
```

### 2. 扩展扫描目录

编辑 `SCAN_DIRECTORIES`：

```python
SCAN_DIRECTORIES = [
    '.claude/agents/',
    '.claude/commands/',
    '.claude/memory/',  # 添加新目录
]
```

### 3. 集成到 CI/CD

在 GitHub Actions 中添加：

```yaml
- name: Update Path References
  run: python3 .claude/tools/update_paths.py
```

---

## 📈 未来改进方向

### 短期（1-2周）
- ✅ 基础自动更新工具
- ✅ 配置文件定义
- ✅ 使用文档

### 中期（1-2月）
- 🔄 Git Hook 集成
- 🔄 VS Code 插件支持
- 🔄 交互式更新界面

### 长期（3-6月）
- 🔄 真正的引用解析机制
- 🔄 Markdown 预处理器
- 🔄 IDE 实时提示

---

## ❓ 常见问题

### Q: 为什么不直接用配置文件 + 动态引用？

**A**: Markdown 不支持原生引用，需要额外的预处理层。当前阶段（架构不稳定期）简单工具更实用。

### Q: 工具会误删内容吗？

**A**: 不会。工具只替换精确匹配的路径字符串，不会修改其他内容。建议先用 Git 提交当前状态，以便回滚。

### Q: 如何确认更新成功？

**A**:
1. 查看工具的更新报告
2. 运行 `git diff` 查看变更
3. 运行工具后，会自动检查是否还有旧引用

### Q: 可以支持 JSON/YAML 文件吗？

**A**: 可以！修改 `FILE_EXTENSIONS` 配置即可：
```python
FILE_EXTENSIONS = ['.md', '.json', '.yaml', '.yml']
```

---

## 📝 总结

这个混合方案的核心优势：

1. **简单实用** - 配置文件 + 自动工具，无需复杂架构
2. **自动化** - 一键更新所有引用，减少人工错误
3. **可扩展** - 易于添加新规则和新目录
4. **渐进式** - 可逐步演进到更复杂的方案

**适用场景**：当前架构不稳定期，适合快速迭代。

**长期方案**：架构稳定后，可以考虑实现真正的引用解析机制。
