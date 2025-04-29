⚠️ 文件名格式错误，请使用 'YYYY-Wxx' 格式。
## Plan
### 本周最重要的3件事
1. 项目：推进完成「XX项目」设计/开发/上线
2. 学习：每天投入1小时，整理个人知识库，极客工具输出。
3. 习惯：每日xx前睡觉，保证xx小时睡眠，记录打卡。

### 周末安排
* 户外运动：爬山，乒乓
* 极客工具输出
* 亲密关系
* 亲子游戏

### GDD 总结
>- 列举具体数据支持的亮点成果
>- 分析困难事件的根本原因
>- 对比本周与上周的差异化

### Task 总结
#### 关键成果（KR）
> - 量化的指标突破
##### 工作成果

##### 输入：阅读

##### 输出：极客工具


#### 阻塞情况
> - 标注延期任务的关键影响因素
> - 明确技术/资源/沟通类卡点
> - 说明已尝试的解决方案
> - 标注需要外部介入的任务


```dataviewjs
// GDD 明细生成脚本
const GDD_CONFIG = { 
  diaryPath: "Diary",   //日记目录
  gddHeader: "## memos",  // gdd所属目录
  buttonText: "生成本周memos明细",       // 按钮文字
  resetButtonText: "重置本周memos明细",  // 重置按钮文字
  sectionHeader: "### GDD 明细",  // 目标段落标题
  successNotice: "✨ GDD周报生成完成", // 成功提示
  resetSuccessNotice: "✨ GDD周报重置完成", // 重置成功提示
  errorNotice: "文件名需符合 YYYY-WXX 格式", // 错误提示
  gddTags: {                     // 标签配置
    '#good': { emoji: '👍', title: 'Good' },
    '#difficult': { emoji: '💪', title: 'Difficult' },
    '#different': { emoji: '🌟', title: 'Different' }
  }
}
// Task 明细生成脚本
const TASK_CONFIG = {
  diaryPath: "Diary",
  sectionHeader: "### Task 明细", // 要替换的目标段落标题
  taskTag: "#task",            // 要过滤掉的任务标签
  buttonText: "生成本周tasks执行明细", // 按钮显示文本
  resetButtonText: "重置本周tasks执行明细", // 重置按钮文字
  successNotice: "✨ 执行明细已更新！", // 成功通知文本
  resetSuccessNotice: "✨ 执行明细已重置！", // 重置成功提示
  errorNotice: "当前文件名不符合周报格式 (YYYY-WXX)", // 错误通知文本
  subheadingLevel: "####"      // 子标题级别
};
// 重置某个部分的内容
async function resetSection(sectionHeader, successNotice) {
  // 获取当前文件
  const file = app.vault.getFileByPath(dv.current().file.path);
  const content = await app.vault.read(file);
  
  // 提取当前标题的级别（有多少个#）
  const headerLevel = sectionHeader.match(/^(#+)/)[0].length;
  
  // 找到这个标题在文本中的位置
  const headerRegex = new RegExp(`^${escapeRegExp(sectionHeader)}\\s*$`, 'm');
  const headerMatch = content.match(headerRegex);
  
  if (!headerMatch) {
    new Notice(`未找到 ${sectionHeader} 部分`, 3000);
    return false;
  }
  
  // 找到标题的起始位置
  const headerStartPos = headerMatch.index;
  
  // 从标题开始的位置往后查找
  const contentAfterHeader = content.substring(headerStartPos);
  
  // 寻找下一个同级别或更高级别的标题
  // 精确匹配同级别或更高级别的标题（即 #, ##, … 直到当前标题级别）
  // 注意：此处需要确保匹配的是行首的标题，避免匹配内容中的标签或文本
  const nextHeaderRegex = new RegExp(`\\n^#{1,${headerLevel}}\\s`, 'm');
  const nextHeaderMatch = contentAfterHeader.match(nextHeaderRegex);
  
  let endPos;
  if (nextHeaderMatch) {
    // 如果找到下一个标题，截取到那里
    endPos = headerStartPos + nextHeaderMatch.index;
  } else {
    // 如果没找到，截取到文档结尾
    endPos = content.length;
  }
  
  // 构建新内容：保留标题后直接添加换行符
  const beforeSection = content.substring(0, headerStartPos + headerMatch[0].length);
  const afterSection = content.substring(endPos);
  const newContent = beforeSection + '\n' + afterSection;
  
  // 写入更新后的内容
  await app.vault.modify(file, newContent);
  new Notice(successNotice, 3000);
  return true;
}

// 主处理函数
async function generateGDD() {
  // 获取当前周报信息
  const currentFile = dv.current().file.name;
  const weekMatch = currentFile.match(/(\d+)-W(\d+)/);
  
  if (!weekMatch) {
    new Notice(GDD_CONFIG.errorNotice);
    return;
  }

  // 计算周范围
  const [_, year, week] = weekMatch;
  const startDate = moment().year(year).isoWeek(week).startOf('isoWeek');
  const endDate = moment().year(year).isoWeek(week).endOf('isoWeek');

  // 构建查询路径
  const allDiaries = dv.pages(`"${GDD_CONFIG.diaryPath}/${year}"`);
  console.log(`allDiaries.values.length:${allDiaries.values.length}`)
  
  // 过滤本周日记
  const weeklyDiaries = allDiaries.where(p => {
    const noteDate = moment(p.file.name, "yyyy-MM-DD");
    return noteDate.isBetween(startDate, endDate, null, '[]');
  });
  console.log(`weeklyDiaries:${weeklyDiaries.values.length}`)
  
  // 初始化标签存储
  const tagStore = Object.keys(GDD_CONFIG.gddTags).reduce((acc, tag) => {
    acc[tag] = [];
    return acc;
  }, {});

  // 处理每个日记文件
  for (const diary of weeklyDiaries) {
    try {
      const content = await dv.io.load(diary.file.path);
      const memosSection = content.match(/## memos\n([\s\S]*?)(?=\n##|$)/);
      
      if (!memosSection) continue;
      
      console.log(`memosSection:\n${memosSection}`)
      const memoLines = memosSection[1].split('\n')
                .filter(line => line.trim().startsWith('- ') || line.trim().startsWith('* '))
                .map(line => line.substring(2).trim());
        
      memoLines.forEach(memoLine => {
        console.log(`memoLine:\n${memoLine}`)
        const memoText = memoLine.replace(/^- /, '').trim();
        const memoDate = diary.file.name;
        
        // 捕获所有匹配的标签
        Object.keys(GDD_CONFIG.gddTags).forEach(tag => {
          if (memoText.includes(tag)) {
            const cleanText = memoText
              .replace(new RegExp(tag, 'g'), '')
              .replace(/\s{2,}/g, ' ')
              .trim();
            if (cleanText) {
              tagStore[tag].push(`${memoDate} ${cleanText}`);
            }
          }
        });
      });
    } catch (error) {
      console.error(`处理文件 ${diary.file.path} 时出错:`, error);
    }
  }

  // 构建Markdown内容
  let mdContent = "";
  for (const [tag, config] of Object.entries(GDD_CONFIG.gddTags)) {
    const items = tagStore[tag];
    if (items.length === 0) continue;
    
    mdContent += `#### ${config.emoji} ${config.title} · ${items.length}条\n\n`;
    items.forEach(item => mdContent += `* ${item}\n`);
    mdContent += "\n";
  }

  // 更新文档内容
  const file = app.vault.getFileByPath(dv.current().file.path);
  const originalContent = await app.vault.read(file);
  
  // 使用改进后的章节替换逻辑
  let newContent = await replaceSection(originalContent, GDD_CONFIG.sectionHeader, mdContent);

  // 写入更新
  await app.vault.modify(file, newContent);
  new Notice(GDD_CONFIG.successNotice, 3000);
}

async function generateTasks() {
  // 获取当前文件名并解析年份和周数
  const currentFileName = dv.current().file.name;
  const weekMatch = currentFileName.match(/(\d+)-W(\d+)/);
  
  if (!weekMatch) {
    new Notice(TASK_CONFIG.errorNotice);
    return;
  }
  
  const [_, targetYear, targetWeek] = weekMatch;
  
  // 计算周的开始和结束日期
  const weekStart = moment().isoWeekYear(parseInt(targetYear)).isoWeek(parseInt(targetWeek)).startOf('isoWeek').format("YYYY-MM-DD");
  const weekEnd = moment().isoWeekYear(parseInt(targetYear)).isoWeek(parseInt(targetWeek)).endOf('isoWeek').format("YYYY-MM-DD");
  
  console.log(`时间范围: ${weekStart} 至 ${weekEnd}`);
  
  // 查询在这个周范围内的任务，并为每个任务添加日期信息
  let tasksWithDates = [];
  const diaryYearPath=`"${TASK_CONFIG.diaryPath}/${targetYear}"`
  const pages = dv.pages(diaryYearPath).where(p => {
    // 检查文件是否有日期属性
    if (!p.file.day) return false;
    
    // 将日期转换为字符串格式进行比较
    const fileDateStr = p.file.day.toString();
    // 移除时间部分，只保留日期 (YYYY-MM-DD)
    const dateOnly = fileDateStr.split("T")[0];
    
    return dateOnly >= weekStart && dateOnly <= weekEnd;
  });
  
  // 为每个任务添加日期信息
  for (const page of pages) {
    for (const task of page.file.tasks) {
      tasksWithDates.push({
        task: task,
        date: page.file.day
      });
    }
  }
  
  // 按日期排序（升序）
  tasksWithDates.sort((a, b) => {
    return a.date - b.date;
  });
  
  // 按标签分组
  const tasksByTag = {};
  for (const item of tasksWithDates) {
    const task = item.task;
    // 过滤掉指定的任务标签，只保留其他标签
    const filteredTags = task.tags.filter(tag => tag !== TASK_CONFIG.taskTag);
    // 如果没有其他标签则归类为"无标签"
    const tags = filteredTags.length > 0 ? filteredTags.join(" ") : "无标签";
    
    if (!tasksByTag[tags]) {
      tasksByTag[tags] = [];
    }
    tasksByTag[tags].push(task);
  }
  
  // 准备 Markdown 内容
  let markdownContent = "";
  for (const tag in tasksByTag) {
    let taskSize=tasksByTag[tag].length
    // 标题中去掉 # 符号
    // const cleanTag = tag.replace(/#/g, '');
    markdownContent += `${TASK_CONFIG.subheadingLevel} ${tag} · ${taskSize}项\n\n`;
    
    for (const task of tasksByTag[tag]) {
      const status = task.completed ? "x" : " ";
      
      // 清理任务文本，移除所有标签
      let cleanText = task.text;
      task.tags.forEach(tag => {
        cleanText = cleanText.replace(tag, '');
      });
      // 移除多余空格
      cleanText = cleanText.trim();
      
      markdownContent += `* [${status}] ${cleanText} (${task.link})\n`;
    }
    markdownContent += "\n";
  }
  
  // 获取当前文件内容
  const file = app.vault.getFileByPath(dv.current().file.path);
  const fileContent = await app.vault.read(file);

  // 使用改进的章节替换逻辑
  const updatedContent = await replaceSection(fileContent, TASK_CONFIG.sectionHeader, markdownContent);
  
  // 保存更新后的内容
  await app.vault.modify(file, updatedContent);
  
  // 通知用户
  new Notice(TASK_CONFIG.successNotice, 3000);
}

// 共用的章节替换逻辑函数（改进版）
async function replaceSection(content, sectionHeader, newContent) {
  // 提取标题级别
  const headerLevel = sectionHeader.match(/^(#+)/)[0].length;
  
  // 找到标题在文本中的位置
  const headerRegex = new RegExp(`^${escapeRegExp(sectionHeader)}\\s*$`, 'm');
  const headerMatch = content.match(headerRegex);
  
  if (!headerMatch) {
    // 如果没有找到标题，在文档末尾添加
    return `${content}\n\n${sectionHeader}\n\n${newContent}\n`;
  }
  
  // 找到标题的起始位置
  const headerStartPos = headerMatch.index;
  
  // 获取标题后的内容
  const contentAfterHeader = content.substring(headerStartPos);
  
  // 寻找下一个同级别或更高级别的标题
  const nextHeaderRegex = new RegExp(`\\n^#{1,${headerLevel}}\\s`, 'm');
  const nextHeaderMatch = contentAfterHeader.match(nextHeaderRegex);
  
  // 确定截止位置
  let endPos;
  if (nextHeaderMatch) {
    endPos = headerStartPos + nextHeaderMatch.index;
  } else {
    endPos = content.length;
  }
  
  // 构建新内容
  const beforeSection = content.substring(0, headerStartPos + headerMatch[0].length);
  const afterSection = content.substring(endPos);
  
  // 组合最终内容
  return `${beforeSection}\n\n${newContent}\n${afterSection}`;
}

// 辅助函数：转义正则表达式中的特殊字符
function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// 创建 GDD 生成按钮
const gddBtn = this.container.createEl('button', {
  text: GDD_CONFIG.buttonText,
  cls: 'gdd-generate-btn'
});
gddBtn.style.marginRight = '1em';
gddBtn.style.marginBottom = '1em';
gddBtn.addEventListener('click', async () => {
  gddBtn.textContent = '生成中…';
  gddBtn.disabled = true;
  try {
    await generateGDD();
  } catch (error) {
    console.error('生成失败:', error);
    new Notice('❌ GDD生成失败，请查看控制台', 5000);
  } finally {
    gddBtn.textContent = GDD_CONFIG.buttonText;
    gddBtn.disabled = false;
  }
});

// 创建 GDD 重置按钮
const gddResetBtn = this.container.createEl('button', {
  text: GDD_CONFIG.resetButtonText,
  cls: 'gdd-reset-btn'
});
gddResetBtn.style.marginBottom = '1em';
gddResetBtn.addEventListener('click', async () => {
  gddResetBtn.textContent = '重置中…';
  gddResetBtn.disabled = true;
  try {
    await resetSection(GDD_CONFIG.sectionHeader, GDD_CONFIG.resetSuccessNotice);
  } catch (error) {
    console.error('重置失败:', error);
    new Notice('❌ GDD重置失败，请查看控制台', 5000);
  } finally {
    gddResetBtn.textContent = GDD_CONFIG.resetButtonText;
    gddResetBtn.disabled = false;
  }
});

// 初始渲染 GDD 占位提示
dv.el('div', '点击按钮生成本周GDD明细', {
  cls: 'gdd-placeholder',
  attr: { style: 'color: #666; margin-bottom: 1em;' }
});

// 创建 Task 生成按钮
const taskBtn = this.container.createEl('button', {
  text: TASK_CONFIG.buttonText,
  cls: 'task-generate-btn'
});
taskBtn.style.marginRight = '1em';
taskBtn.style.marginBottom = '1em';
taskBtn.addEventListener('click', async () => {
  taskBtn.textContent = '生成中…';
  taskBtn.disabled = true;
  try {
    await generateTasks();
  } catch (error) {
    console.error('生成失败:', error);
    new Notice('❌ Task生成失败，请查看控制台', 5000);
  } finally {
    taskBtn.textContent = TASK_CONFIG.buttonText;
    taskBtn.disabled = false;
  }
});

// 创建 Task 重置按钮
const taskResetBtn = this.container.createEl('button', {
  text: TASK_CONFIG.resetButtonText,
  cls: 'task-reset-btn'
});
taskResetBtn.style.marginBottom = '1em';
taskResetBtn.addEventListener('click', async () => {
  taskResetBtn.textContent = '重置中…';
  taskResetBtn.disabled = true;
  try {
    await resetSection(TASK_CONFIG.sectionHeader, TASK_CONFIG.resetSuccessNotice);
  } catch (error) {
    console.error('重置失败:', error);
    new Notice('❌ Task重置失败，请查看控制台', 5000);
  } finally {
    taskResetBtn.textContent = TASK_CONFIG.resetButtonText;
    taskResetBtn.disabled = false;
  }
});

// 初始渲染 Task 占位提示
dv.el('div', '点击按钮生成本周Task执行明细', {
  cls: 'task-placeholder',
  attr: { style: 'color: #666; margin-bottom: 1em;' }
});
```
## Memos
### GDD 明细
> 自动汇总的数据：good,difficult,different
## Task
### Task 明细
> 自动汇总的数据：按标签分组的task执行情况