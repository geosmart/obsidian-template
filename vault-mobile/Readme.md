---
title: Readme
aliases: [轻松做好周总结：PDCA 循环 + Obsidian 自动化工作流]
tags: []
created: 2025-03-23T09:10:01
updated: 2025-06-12T11:30:50
draft: true
---

# Readme
![极客工具|417x128](files/xtool-logo.png)

[极客工具-构建个人知识库-系列](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzA4Nzg2NTY2Mw==&action=getalbum&album_id=3880988817024614400&subscene=159&subscene=&scenenote=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2FVyDepofPltPfEFn7nzXHKw%3Fpoc_token%3DHDqOJmijINYRJRbY358yBW_HxONeInwbK3sfqUtn&nolastread=1#wechat_redirect)

## Obsidian 模板
模板围绕以 PARA 方法论

1. 日记
	1. 待办管理
	2. 移动端闪念笔记
	3. 问答式日记模板
	4. AI 总结日记
2. 周总结
	1. 自动汇总日记
	2. PDCA 方法论
3. 月总结
	1. 自动汇总周总结
	2. OKR 实践月计划

![home.png](files/home.png)

## Obsidian 插件

### 系统配置
* 插件安装：[pkmer](https://pkmer.cn/products/plugin/pluginMarket/)
* 状态栏管理： [statusbar-organizer](obsidian://show-plugin?id=statusbar-organizer)

### GTD 待办管理
* 待办管理：[[obsidian-tasks]]
* 待办管理 - 排序：[completed-tasks](obsidian://show-plugin?id=completed-tasks)，更新待办状态时，将未完成时的任务移动到列表前面
* 待办管理 - 时间线视图：[tasks-calendar-wrapper](obsidian://show-plugin?id=tasks-calendar-wrapper)
* 待办管理 - 昨天未完成的 todo 移动到今天：[obsidian-rollover-daily-todos](obsidian://show-plugin?id=obsidian-rollover-daily-todos)
* 任务清单 - 全选打钩/取消全选：[obsidian-checklist-reset](obsidian://show-plugin?id=obsidian-checklist-reset)

### 日记
* 快速笔记：[QuickAdd](obsidian://show-plugin?id=quickadd)：自动化，AI 助理
* 周期笔记：[periodic-notes](obsidian://show-plugin?id=periodic-notes)，按周/季/月/年，按模板总结

### 知识同步
* 实时同步：[[obsidian-livesync]]，基于 couchdb 服务
* 实时同步：[[Resilio]]
* 数据备份：[[obsidian-git]]，基于 git 服务
	* 自建 git 服务端： gogos
	* android 客户端： https://github.com/ViscousPot/GitSync
* 微信阅读：[obsidian-weread-plugin](obsidian://show-plugin?id=obsidian-weread-plugin)，按书同步笔记和高亮
* 知识导出：[obsidian-enhancing-export](obsidian://show-plugin?id=obsidian-enhancing-export)：基于 pandoc 导出各种格式
* 数据导入：[obsidian-importer](obsidian://show-plugin?id=obsidian-importer)：外部笔记导入，第一次知识迁移时候能用到

### 编辑增强
* 自动格式化：[linter](obsidian://show-plugin?id=obsidian-linter)
* 嵌入笔记编辑：[outliner.md](https://outliner.md/)
* 笔记模板：[[obsidian-templater]]
* 图表脚本：[mermaid](obsidian://show-plugin?id=mehrmaid)，封装了主流图表库 [mermaid](https://mermaid.js.org/)，支持 20 多种图表类型，特别适合让大模型自动生成
* 图表视图: [obsidian-chartsview-plugin](obsidian://show-plugin?id=obsidian-chartsview-plugin)，可交互式制作图表，提供各类图表模板
* 输入智能补全：[[various-complements]]
* REST 接口：[[obsidian-local-rest-api]]
* office 文档编辑：[obsidian-univer](https://github.com/dream-num/obsidian-univer)，支持编辑 docx 文档和 xlsx 表格

### 搜索增强
* 搜索增强：[omnisearch](obsidian://show-plugin?id=omnisearch)
* 主页：[homepage](obsidian://show-plugin?id=homepage)
* 文件夹笔记：[folder-notes](obsidian://show-plugin?id=folder-notes)
* 文件夹显示文件数：[file-explorer-note-count](obsidian://show-plugin?id=file-explorer-note-count)
* 文件路径复制：[show-file-path](obsidian://show-plugin?id=obsidian-show-file-path)
* 最近编辑的文件：[recent-files-obsidian](obsidian://show-plugin?id=recent-files-obsidian)
* 最近编辑的光标位置：[remember-cursor-position](obsidian://show-plugin?id=remember-cursor-position)
* 笔记大纲：[obsidian-quiet-outline](obsidian://show-plugin?id=obsidian-quiet-outline)
* 彩色标签：[[colored-tags]]
* 文件路径复制：[obsidian-show-file-path](obsidian://show-plugin?id=obsidian-show-file-path),在 obsidian 中一键复制图片的绝对路径；
* 内置浏览器：webviewer，官方插件

### AI 增强
* AI 总结/提示词管理：[quickadd](obsidian://show-plugin?id=quickadd)，启用 AI Assistant
* AI 对话/RAG 问答：[copilot](obsidian://show-plugin?id=copilot)，支持本地笔记的 rag 搜索
* AI 对话：[chatgpt-md](obsidian://show-plugin?id=chatgpt-md)，覆盖广，支持 ollama,chatgpt,openRouter，基本能使用所有大模型
* 本地大模型服务：[ai-providers](obsidian://show-plugin?id=ai-providers),可对接本地的 LmStudio
* 本地 AI 助手：[local-gpt](obsidian://show-plugin?id=local-gpt)，支持提示词管理，右键
* AI-IDE：[[smart-composer]]

### 视图管理

#### 日历视图 - 待办
1. [Obsidian-Tasks-Calendar](github.com/702573N/Obsidian-Tasks-Calendar)：支持日/周/月 3 个视图，简洁只读；
2. [FullCalendar](obsidian://show-plugin?id=obsidian-full-calendar): 支持日/周/月/列表 4 个视图，存储模式支持 2 种本地 (full note,diary note)3 种远程（如 icloud），交互做的是真好。
3. [BigCalendar](obsidian://show-plugin?id=big-calendar)：支持日周月 3 个视图，可按时间创建任务

> FullCalendar 每个事项都创建一个文件，用了一年我笔记数量爆炸，没办法我换成 tasks calendar wrapper 用时间线来管理，当天的 task 都记在一个笔记

#### 日历视图 - 笔记
显示其他非 task 类的，比如日记，笔记
1. [oz-calendar](obsidian://show-plugin?id=oz-calendar)，支持月视图，通过读取笔记的 created 字段显示在日历中，
2. [chronology](obsidian://show-plugin?id=chronology): 支持月视图，比 oz-calendar 多个热力图，

#### 笔记视图
* 脑图：[obsidian-mindmap-nextgen](https://github.com/james-tindal/obsidian-mindmap-nextgen)，按 markdown 大纲展示为树形脑图
* 数据视图：[[obsidian-dataview]]，类似 mysql
* PPT 演示文稿：[marp](obsidian://show-plugin?id=marp-slides)
* 卡片视图：[notes-explorer](obsidian://show-plugin?id=notes-explorer)，前身是 CardsView
* 完全魔改的：make.md，改得和 notion 很像，太花了，我用不习惯

### 附件管理
1. 远程图床：[image-upload-toolkit](obsidian://show-plugin?id=image-upload-toolkit):，本地图片上传到远程图床，如 OSS,COS,Qiniu
2. 图片编辑/粘贴：[image-converter](obsidian://show-plugin?id=image-converter)，，支持粘贴时按规则自动重命名，图片缩放，裁剪，压缩，右键重命名

## 商业化模板
* LifeHQ: https://lifehq.practicalpkm.com/
* LifeOS：https://github.com/quanru/obsidian-example-LifeOS

## 插件资源
1. obsidian 年度插件 -2024 https://obsidian.md/blog/2024-goty-winners/
2. obsidian 年度插件 -2000 到 2023 分析
3. obsdian 插件 trending： https://www.obsidianstats.com/trending
4. obsdian 插件下载排行： https://www.obsidianstats.com/most-downloaded
