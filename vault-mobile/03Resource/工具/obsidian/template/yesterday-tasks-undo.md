<%*
const taskRegex = /[-|\*] \[ \] .*?#task.*?($|\n)/g; // 匹配未完成的 #task 任务
// 工具函数：动态生成日记文件路径
function getDailyNotePath(dateStr) {
  const [year, month, day] = dateStr.split("-");
  return `Diary/${year}/${year}-${month}-${day}.md`; // 格式：Diary/2024/2024-05-20.md
}

// 步骤1：读取文件内容
async function readFileContent(filePath) {
  try {
    const targetFile = tp.file.find_tfile(filePath);
    return await app.vault.read(targetFile);
  } catch (error) {
    console.log(`读取文件 ${filePath} 内容失败:`, error);
    return "";
  }
}

// 步骤2：提取未完成的 #task 任务
function extractUnfinishedTasks(content) {
  return content.match(taskRegex) || [];
}

// 步骤3：将任务追加到今日文件中
async function appendTasksToTodayFile(todayFilePath, tasks) {
  if (tasks.length === 0) return; // 如果没有任务，直接返回

  // 检查今日文件是否存在，不存在则创建
  const fileExists = await tp.file.exists(todayFilePath);
  if (!fileExists) {
    await app.vault.create(todayFilePath);
  }

  // 获取文件对象并追加任务
  const file = app.vault.getAbstractFileByPath(todayFilePath);
  if (file) {
    const currentContent = await app.vault.read(file);
    const newContent = currentContent + tasks.join(""); // 在文件末尾追加任务
    await app.vault.modify(file, newContent);
    console.log("✅ 未完成任务已追加到今日文件中。");
  } else {
    console.log("❌ 今日文件未找到！");
  }
}

// 步骤4：从昨日文件中删除未完成任务
async function removeTasksFromYesterdayFile(yesterdayFilePath, tasks) {
  if (tasks.length === 0) return; // 如果没有任务，直接返回

  try {
    const targetFile = tp.file.find_tfile(yesterdayFilePath);
    let yesterdayContent = await app.vault.read(targetFile);

    // 使用正则替换删除未完成任务
    const updatedContent = yesterdayContent.replace(taskRegex, "");
    await app.vault.modify(targetFile, updatedContent);
    console.log("✅ 未完成任务已从昨日文件中删除。");
  } catch (error) {
    console.log("❌ 删除未完成任务时出错:", error);
  }
}

// 主函数：执行任务迁移逻辑
async function migrateUnfinishedTasks() {
  // 获取昨日和今日的文件路径
  const todayDate = tp.date.now("yyyy-MM-DD");
  const yesterdayDate = tp.date.yesterday("yyyy-MM-DD");
  const yesterdayFilePath = getDailyNotePath(yesterdayDate);
  const todayFilePath = getDailyNotePath(todayDate);
  console.log(`昨天文件：${yesterdayFilePath}`);
  // 读取昨日文件内容
  const yesterdayContent = await readFileContent(yesterdayFilePath);

  // 提取未完成的 #task 任务
  const unfinishedTasks = extractUnfinishedTasks(yesterdayContent);
  console.log(`昨天未完成：${unfinishedTasks}`);
  // 将任务追加到今日文件中
  await appendTasksToTodayFile(todayFilePath, unfinishedTasks);

  // 从昨日文件中删除未完成任务
  await removeTasksFromYesterdayFile(yesterdayFilePath, unfinishedTasks);
}

// 执行主函数
await migrateUnfinishedTasks();
%>