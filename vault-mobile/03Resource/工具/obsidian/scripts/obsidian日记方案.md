---
title: obsidian 日记方案
aliases: [obsidian 日记方案]
tags: []
created: 2024-04-01T13:52:25
updated: 2025-06-08T21:08:06
---

# obsidian 日记方案

obsidian 中，日记记录在#memos 标题下，包含二级目录##工作和##生活，如何按##工作和##生活聚合，比如支持按年/月/周聚合的日记 view

```dataview
table
  date(file.name) as 日期,
  file.name as 文件名,
  工作内容 as "工作",
  生活内容 as "生活"
from "Diary/2025/Diary"
where contains(file.name, "# memos") and date(file.name).weekyear = date(today()).weekyear and date(file.name).week = date(today()).week
sort file.day desc

let 工作内容 = match(file.content, "## 工作", "after")[0],
    生活内容 = match(file.content, "## 生活", "after")[0]
```

```dataview
table file.folder as 目录,date(split(file.name," ",2)[0]) as 日期
from "Diary/2024/Diary/04"
where 
date(split(file.name," ",2)[0]).weekyear=number(split(this.file.name,"W")[1])
sort file.day desc
```
