---
draft: true
title: weekly
tags: []
created: 2025-03-09T18:01:49
updated: 2025-04-26T10:36:01
---

# weekly
<%*
// 生成标题和日期
const curFile = tp.file.title;
const isWeeklyFile = curFile.match(/(\d+)-W(\d+)/);
if (isWeeklyFile) {
    const [_, targetYear, targetWeek] = isWeeklyFile;

    // 计算周的开始和结束日期
    const startDate = moment().isoWeekYear(targetYear).isoWeek(targetWeek).startOf('isoWeek').format("YYYY-MM-DD");
    const endDate = moment().isoWeekYear(targetYear).isoWeek(targetWeek).endOf('isoWeek').format("YYYY-MM-DD");

    // 格式化周数显示
    const weekDisplay = `W${targetWeek.padStart(2, '0')}`;

    // 输出内容
    tR += `# ${targetYear}-${weekDisplay} 周报\n\n`;
    tR += `📅 时间范围: ${startDate} 至 ${endDate}`;
} else {
    tR += "⚠️ 文件名格式错误，请使用 'YYYY-Wxx' 格式。";
}
%>

## Plan
### 本周最重要的 3 件事
1. 项目：推进完成「XX 项目」设计/开发/上线
2. 学习：每天投入 1 小时，整理个人知识库，极客工具输出。
3. 习惯：每日 xx 前睡觉，保证 xx 小时睡眠，记录打卡。

### 周末安排
* 户外运动：爬山，乒乓
* 极客工具输出
* 亲密关系
* 亲子游戏

### GDD 总结

> * 列举具体数据支持的亮点成果
> * 分析困难事件的根本原因
> * 对比本周与上周的差异化

### Task 总结
#### 关键成果（KR）

> * 量化的指标突破

##### 工作成果

##### 输入：阅读

##### 输出：极客工具

#### 阻塞情况

> * 标注延期任务的关键影响因素
> * 明确技术/资源/沟通类卡点
> * 说明已尝试的解决方案
> * 标注需要外部介入的任务

```dataviewjs  
const quickAddChoice  = "周总结-汇总";
// 获取 QuickAdd 插件 API
const quickAdd = app.plugins.plugins["quickadd"];
if (!quickAdd) {
  new Notice("❌ 未检测到 QuickAdd 插件，请先启用它");
}
const btn = dv.el("button", quickAddChoice);
// 创建按钮并绑定点击事件
btn.addEventListener("click", async () => {
  try {
    await quickAdd.api.executeChoice(quickAddChoice);
  } catch (err) {
    new Notice(`❌ 运行失败：${err.message}`);
  }
});
```

## Memos
### GDD 明细

> 自动汇总的数据：good,difficult,different

## Task
### Task 明细

> 自动汇总的数据：按标签分组的 task 执行情况
