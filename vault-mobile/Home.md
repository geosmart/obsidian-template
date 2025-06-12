---
title: Home
tags: []
created: 2025-04-28T12:00:44
updated: 2025-06-12T11:37:27
draft: true
---

# Home
# 待办
## 今日待办

```tasks
# 查询当天任务
happens in  today
# 显示控制
hide backlink
hide start date
hide scheduled date
hide created date
hide due date
# 按标签分组
group by function task.tags.join(" ")
# 按日期排序
sort by path
```

## 本周待办

```tasks
# 查询本周任务
happens after today
happens before end of this week
not done
# 显示控制
hide backlink
hide start date
hide scheduled date
hide created date
hide due date
# 按标签分组
group by function task.tags.join(" ")
# 按日期排序
sort by path
```

## 30 天内待办

```tasks
# 查询本月任务
happens after yesterday
happens before in 30 days
not done
# 按标签分组
group by function task.tags.join(" ")
# 按日期排序
sort by path
```

## 未完成任务

^9af7c3

```tasks
# 显示控制
hide due date
hide scheduled date
hide recurrence rule

# 查询本周任务
filter by function task.file.path.includes('Diary/2025')
filter by function task.status.name !== 'Done'
filter by function task.status.name !== 'Cancelled'
# 按标签分组
group by function task.tags.join(" ")
# 按日期排序
sort by path
```

## 待安排

```tasks
# 显示控制
hide due date
hide scheduled date
hide recurrence rule

# 查询本周任务
filter by function task.file.path.includes('Diary/Inbox.md')
filter by function task.status.name !== 'Done'
# 按标签分组
group by function task.tags.join(" ")
# 按日期排序
sort by path
```
