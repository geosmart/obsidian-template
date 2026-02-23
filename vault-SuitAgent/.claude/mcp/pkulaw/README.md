# 北大法宝 MCP (pkulaw-mcp) 智能法律服务平台

## 概述

北大法宝MCP是一个基于Model Context Protocol (MCP)的法律研究工具，提供法律法规检索、判例查询、法条解读等智能法律服务。

## 安装指南

### 方式一：pip安装（推荐）

```bash
pip install pkulaw-mcp
```

### 方式二：源码安装

```bash
git clone https://github.com/pkulaw/mcp.git
cd mcp
pip install -e .
```

## 配置说明

### 环境变量配置

在 `.claude/mcp.json` 中配置以下参数：

```json
{
  "mcpServers": {
    "pkulaw": {
      "command": "pkulaw-mcp",
      "args": [],
      "env": {
        "PKULAW_API_KEY": "your_api_key_here",
        "PKULAW_BASE_URL": "https://api.pkulaw.com/v1"
      }
    }
  }
}
```

### API密钥获取

1. 访问 [北大法宝开放平台](https://www.pkulaw.com/)
2. 注册账号并登录
3. 进入开发者中心
4. 创建应用并获取API密钥

## API参考

### 1. 法律法规检索 (search_laws)

检索相关法律法规条文。

**参数：**
- `keyword`: 检索关键词
- `category`: 法律法规分类（可选）
- `level`: 法律效力级别（可选：法律、行政法规、部门规章、地方性法规）
- `date_from`: 开始日期（可选）
- `date_to`: 结束日期（可选）
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）

**返回值：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "list": [
      {
        "law_id": "12345",
        "title": "中华人民共和国合同法",
        "category": "法律",
        "effective_date": "1999-10-01",
        "content": "..."
      }
    ]
  }
}
```

### 2. 判例检索 (search_cases)

检索相关判例。

**参数：**
- `keyword`: 检索关键词
- `case_type`: 案例类型（可选：民事、刑事、行政）
- `court_level`: 法院级别（可选）
- `region`: 地区（可选）
- `date_from`: 开始日期（可选）
- `date_to`: 结束日期（可选）
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）

**返回值：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 50,
    "list": [
      {
        "case_id": "67890",
        "title": "房屋租赁合同纠纷案",
        "case_number": "(2025)京01民终1234号",
        "court": "北京市第一中级人民法院",
        "judge_date": "2025-01-15",
        "summary": "...",
        "content": "..."
      }
    ]
  }
}
```

### 3. 法条解读 (interpret_article)

对特定法条进行详细解读。

**参数：**
- `law_id`: 法律法规ID
- `article`: 条款编号
- `context`: 法条内容（可选）

**返回值：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "law_title": "中华人民共和国民法典",
    "article": "第七百零五条",
    "content": "...",
    "interpretation": {
      "meaning": "条款含义解释",
      "application": "适用场景",
      "notes": "注意事项"
    }
  }
}
```

### 4. 案例分析 (analyze_case)

对案例进行深度分析。

**参数：**
- `case_id`: 案例ID
- `analysis_type`: 分析类型（可选：争议焦点、法律适用、判决分析）

**返回值：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "case_summary": "案件概要",
    "dispute_focus": [
      "争议焦点1",
      "争议焦点2"
    ],
    "law_application": [
      {
        "law": "中华人民共和国民法典",
        "articles": ["第123条", "第456条"],
        "application": "适用说明"
      }
    ],
    "judgment_analysis": "判决分析"
  }
}
```

### 5. 法律咨询 (legal_consultation)

提供法律问题咨询。

**参数：**
- `question`: 法律问题
- `category`: 问题类型（可选：民事、刑事、行政、劳动等）

**返回值：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "question": "用户提问",
    "answer": "专业回答",
    "related_laws": [
      {
        "law_title": "相关法律",
        "articles": ["条款列表"]
      }
    ],
    "related_cases": [
      {
        "case_title": "相关案例",
        "case_id": "案例ID"
      }
    ]
  }
}
```

## 使用示例

### Python示例

```python
import asyncio
from pkulaw_mcp import PkulawClient

async def main():
    client = PkulawClient(api_key="your_api_key")

    # 检索法律法规
    laws = await client.search_laws(
        keyword="房屋租赁",
        category="法律",
        page_size=10
    )

    print(f"找到 {laws['total']} 条相关法律法规")

    # 检索判例
    cases = await client.search_cases(
        keyword="房屋租赁合同纠纷",
        case_type="民事",
        page_size=10
    )

    print(f"找到 {cases['total']} 个相关案例")

    # 法条解读
    interpretation = await client.interpret_article(
        law_id="12345",
        article="第五百条"
    )

    print(f"法条解读: {interpretation['interpretation']['meaning']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript示例

```javascript
const { PkulawClient } = require('pkulaw-mcp');

async function main() {
  const client = new PkulawClient({
    apiKey: 'your_api_key'
  });

  // 检索法律法规
  const laws = await client.searchLaws({
    keyword: '房屋租赁',
    category: '法律',
    pageSize: 10
  });

  console.log(`找到 ${laws.total} 条相关法律法规`);

  // 检索判例
  const cases = await client.searchCases({
    keyword: '房屋租赁合同纠纷',
    caseType: '民事',
    pageSize: 10
  });

  console.log(`找到 ${cases.total} 个相关案例`);
}

main();
```

## 错误代码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | API密钥无效 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |

## 常见问题

### Q: 如何获取API密钥？

A: 访问北大法宝开放平台，注册账号后进入开发者中心创建应用即可获取API密钥。

### Q: API调用频率限制是多少？

A: 免费版API限制为每分钟100次请求，付费版可联系客服调整。

### Q: 如何处理返回数据中的HTML标签？

A: 返回数据已自动处理HTML标签，如需原始HTML可设置`raw_html=true`参数。

### Q: 判例数据包含哪些内容？

A: 包含案例标题、案号、审理法院、审理日期、案件摘要、判决正文等完整信息。

### Q: 支持检索哪些类型的法律法规？

A: 支持法律、行政法规、部门规章、地方性法规、司法解释等各类规范性文件。

## 技术支持

- 文档地址：https://mcp.pkulaw.com/docs
- GitHub仓库：https://github.com/pkulaw/mcp
- 技术支持邮箱：support@pkulaw.com
- 用户交流群：QQ群号 123456789

## 更新日志

### v1.0.0 (2024-12-01)
- 初始版本发布
- 支持法律法规检索
- 支持判例查询
- 支持法条解读

### v1.1.0 (2025-01-15)
- 新增案例分析功能
- 新增法律咨询功能
- 优化检索算法
- 提升响应速度

### v1.2.0 (2025-03-01)
- 新增多语言支持
- 增强错误处理
- 提供更多查询参数
- 支持自定义排序

## 许可证

MIT License

## 版权信息

Copyright © 2025 北大法宝 (pkulaw.com). All rights reserved.
