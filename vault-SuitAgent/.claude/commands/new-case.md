# /new-case - 创建新案件

## 功能说明
为新案件创建标准化的工作目录结构，自动复制案件模板并初始化管理文件。

## 使用方式

### 基本用法
```bash
/new-case [参数]
```

### 参数选项

#### 必需参数
- `--case-id TEXT` - 案件编号
  - 有案号格式：`[YYYY]省[城市]民初/行初/刑初[序号]号`
  - 无案号格式：`{原告姓名}诉{被告姓名}{案由}`

#### 可选参数
- `--client-name TEXT` - 委托人姓名/公司名
- `--case-type TEXT` - 案件类型（民事/刑事/行政）
- `--case-cause TEXT` - 案由
- `--opposite-party TEXT` - 对方当事人
- `--output-dir TEXT` - 输出目录（默认：output/）

### 使用示例

#### 1. 创建有案号的案件
```bash
/new-case \
  --case-id "[2025]京0105民初1234号" \
  --client-name "北京科技有限公司" \
  --case-type "民事" \
  --case-cause "合同纠纷" \
  --opposite-party "上海某某公司"
```

#### 2. 创建无案号的案件
```bash
/new-case \
  --case-id "张三诉李四合同纠纷案" \
  --client-name "张三" \
  --case-type "民事" \
  --case-cause "合同纠纷" \
  --opposite-party "李四"
```

#### 3. 最小必需参数
```bash
/new-case --case-id "[2025]京0105民初1234号"
```

## SubAgent 工作流

此Command会触发以下SubAgent工作流：

```
1. DocAnalyzer (文档分析器)
   ↓
2. Scheduler (日程规划者)
   ├─ 创建案件目录结构
   ├─ 复制case-templates模板
   ├─ 初始化[Y案件编号].yaml
   ├─ 初始化[Y案件编号].md
   └─ 创建工作记录模板
   ↓
3. Reporter (报告整合器)
```

## 输出内容

### 自动创建的目录结构（12目录架构）

> **重要**：目录结构定义来源于 [`.claude/rules/AgentMapping.md`](../rules/AgentMapping.md)
>
> - 完整的12层标准化架构定义
> - 命名格式：`{id} - {emoji} {name}`，横线前后必须有空格
> - Agent与目录的映射关系详见该文件
>
> **目录结构概览**：
>
> ```
> output/[案件编号]/
> ├── [案件编号]案件信息.md          # 案件管理看板（根目录）
> ├── 00 - 📅 日程管理/
> ├── 01 - 🤝 委托材料/
> ├── 02 - 📄 案件分析/
> ├── 03 - 🔍 法律研究/
> ├── 04 - 📤 客户提供/
> ├── 05 - 📎 证据材料/
> ├── 06 - 📝 法律文书/
> ├── 07 - 📥 对方提交/
> ├── 08 - 🏛️ 法院送达/
> ├── 09 - 🎯 庭审笔录/
> ├── 10 - 📊 综合报告/
> └── 11 - 📚 参考文件/
> ```
>
> **每个目录的详细说明和Agent映射**请参考 AgentMapping.md

## 技术实现

### 核心流程

1. **案件目录创建**
   - 复制自 `.claude/templates/case-templates/`
   - 包含完整的12层目录结构（00-11）
   - 支持按需选择模板类型（AI工作流/实务流程/混合模式）

2. **YAML管理文件生成**
   ```yaml
   案件基本信息:
     案件编号: "[案件编号]"
     案件性质: "民事/刑事/行政"
     当前状态: "初始阶段"
     案件阶段: "一审"

   当事人信息:
     委托人: "[委托人]"
     对方当事人: "[对方]"
     案由: "[案由]"

   工作进度:
     已完成工作: []
     正在进行: []
     待开始工作:
       - 案件分析
       - 证据整理
       - 法律研究
   ```

3. **MD工作记录生成**
   - 案件基本信息记录
   - 工作时间线模板
   - 每日工作记录格式

### 模板来源
- 位置：`.claude/templates/case-templates/`
- 包含：12个标准目录（00-11）+ 工作记录模板
- 每个目录包含详细的README.md说明文件
- 案件管理文件：[案件编号].yaml + [案件编号].md

### Agent目录映射

> **完整映射关系**：详见 [`.claude/rules/AgentMapping.md`](../rules/AgentMapping.md)
>
> 该文件定义了所有Agent与目录的映射关系，按四层架构组织：
> - 输入层：DocAnalyzer、EvidenceAnalyzer
> - 分析层：IssueIdentifier、Researcher、Strategist
> - 输出层：Writer、Reporter、Summarizer
> - 支持层：Scheduler、Reviewer

## 注意事项

1. **案件编号格式**：
   - 有案号：严格按照法院格式 `[YYYY]省[城市]民初/行初/刑初[序号]号`
   - 无案号：使用当事人信息 `{原告}诉{被告}{案由}`

2. **文件权限**：
   - 所有目录自动创建 `.gitkeep` 保持结构
   - YAML和MD文件自动生成并填充基础信息

3. **目录清理**：
   - 输出目录存在时会提示确认
   - 可使用 `--force` 参数强制覆盖

## 相关命令

- `/generate-trust-docs` - 生成委托材料
- `/evidence-review` - 证据质证
- `/generate-pleading` - 生成答辩状
