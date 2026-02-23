# /generate-trust-docs - 生成委托材料

## 功能说明
自动生成完整的委托材料包，包括委托合同、授权委托书、谈话笔录等5个核心文档。

## 使用方式

### 基本用法
```bash
/generate-trust-docs [参数]
```

### 参数选项

#### 必需参数
- `--client-name TEXT` - 委托人姓名/公司名
- `--client-type [company|person]` - 客户类型（公司或个人）
- `--lawyer-name TEXT` - 代理律师姓名
- `--case-type TEXT` - 案件类型（如：合同纠纷、侵权纠纷等）

#### 可选参数
- `--client-code TEXT` - 统一社会信用代码/身份证号
- `--client-address TEXT` - 地址
- `--client-representative TEXT` - 法定代表人/身份证号
- `--client-position TEXT` - 职务
- `--lawyer-tel TEXT` - 律师联系电话
- `--opposite-party TEXT` - 对方当事人
- `--case-cause TEXT` - 案由
- `--output-dir TEXT` - 输出目录（默认：output/[案件编号]/04_法律文书/）

#### 日期参数（可选）
- `--year TEXT` - 年（默认：当前年份）
- `--month TEXT` - 月（默认：当前月份）
- `--day TEXT` - 日（默认：当前日期）

### 使用示例

#### 1. 公司委托（完整参数）
```bash
/generate-trust-docs \
  --client-name "北京科技有限公司" \
  --client-type company \
  --client-code "91110000000000000X" \
  --client-address "北京市朝阳区xxx大厦1001室" \
  --client-representative "张三" \
  --client-position "总经理" \
  --lawyer-name "李四律师" \
  --lawyer-tel "13800000000" \
  --opposite-party "上海某某公司" \
  --case-cause "合同纠纷" \
  --case-type "合同纠纷"
```

#### 2. 个人委托（最小必需）
```bash
/generate-trust-docs \
  --client-name "张三" \
  --client-type person \
  --client-code "110101199001011234" \
  --lawyer-name "李四律师"
```

## SubAgent 工作流

此Command会触发以下SubAgent工作流：

```
1. DocAnalyzer (文档分析器)
   ↓
2. Writer (法律文书起草器)
   ├─ 读取YAML数据
   ├─ 字段映射转换 (placeholder_mapper.py)
   ├─ 模板选择 (根据client_type)
   ├─ Word文档生成 (DocxProcessor.py)
   └─ 输出5个文档
   ↓
3. Summarizer (摘要生成器)
   ↓
4. Reporter (报告整合器)
```

## 输出内容

### 自动生成的文档
```
output/[案件编号]/04_法律文书/
├── 002律师服务质量监督卡存根.docx
├── 003谈话笔录.docx
├── 004委托代理合同.docx
├── 005授权委托书(公司/个人).docx
├── 007法律文书送达地确认书.docx
└── 委托材料包/
    ├── 委托材料清单.md
    └── 完整委托材料报告.md
```

## 技术实现

### 核心组件

#### 1. placeholder_mapper.py
**位置**：`.claude/tools/placeholder_mapper.py`

**字段映射规则**：
```python
YAML字段 → Word占位符

client_name → {client}
client_type → {type}
client_code → {code}
client_address → {address}
client_representative → {representative}
client_position → {position}

lawyer_name → {lawyer}
lawyer_tel → {tel}

opposite_party → {opposite}
case_cause → {cause}
case_type → {case_type}

year → {year}
month → {month}
day → {day}
```

#### 2. DocxProcessor.py
**位置**：`.claude/tools/DocxProcessor.py`

**主要功能**：
- `Execute.p_replace()` - 段落级别替换
- `Execute.r_replace()` - 运行级别替换（保持格式）
- `DocxProcessor.process_directory()` - 批量处理

#### 3. docx_tools.py
**位置**：`.claude/tools/docx_tools.py`

**主要方法**：
```python
def batch_generate_trust_documents(yaml_data: dict, output_dir: str) -> list[str]:
    """批量生成所有委托文档"""
```

### 模板资源

**公司委托模板**：`.claude/templates/公司委托模板-剑桥颐华/` (9个文档)
**个人委托模板**：`.claude/templates/个人委托模板-剑桥颐华/` (8个文档)

## 注意事项

1. **格式保持**：Word文档格式完全保持（字体、颜色、对齐等）
2. **字段验证**：自动检查必填字段
3. **错误处理**：提供详细的错误提示和解决建议

## 相关命令

- `/new-case` - 创建新案件
- `/evidence-review` - 证据质证
- `/generate-pleading` - 生成答辩状
