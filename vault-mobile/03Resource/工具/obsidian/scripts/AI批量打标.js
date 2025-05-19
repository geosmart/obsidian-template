module.exports = async (params) => {
  // 增加取消标志
  let isCancelled = false;

  // 获取 QuickAdd 参数，如果未提供则使用默认值
  let config = {
    recursive: false,        // 是否递归处理子文件夹
    delayBetweenFiles: 300,  // 文件间处理延迟(ms)
    commandDelay: 2000,      // 命令执行后延迟(ms)
    showProgressBar: true    // 是否显示进度条
  };

  // 命令ID常量
  const exmemoCommand = "exmemo-tools:adjust-meta";
  const linterCommand = "obsidian-linter:lint-file";

  // 检查插件命令是否存在
  if (!app.commands.editorCommands[exmemoCommand]) {
    new Notice("❌ 未检测到插件命令：ExMemo Tools", 3000);
    throw new Error("ExMemo Tools 插件未安装或命令 ID 不正确");
  }
  if (!app.commands.editorCommands[linterCommand]) {
    new Notice("❌ 未检测到插件命令：Linter", 3000);
    throw new Error("Linter 插件未安装或命令 ID 不正确");
  }

  // 获取所有文件夹
  const folders = app.vault.getAllLoadedFiles()
    .filter(file => file.children) 
    .map(folder => folder.path);
  
  // 添加vault根目录
  folders.unshift("/");
  
  // 使用suggester让用户选择文件夹
  const folderPath = await params.quickAddApi.suggester(
    folders, 
    folders,
    "选择一个文件夹"
  );
  
  if (!folderPath) {
    console.log("用户取消了选择");
    return;
  }

  console.log(`用户选择了${folderPath}`);

  // 获取需要处理的文件列表
  const files = getMarkdownFiles(folderPath, config.recursive);

  if (files.length === 0) {
    new Notice(`📂 文件夹「${folderPath}」中没有 Markdown 文件。`, 3000);
    return;
  }

  const userConfirm = await params.quickAddApi.yesNoPrompt(
    `AI批量提取标签/标题/摘要-操作确认`,
    `确定要处理「${folderPath}」${config.recursive ? "及其子文件夹" : ""}中的 ${files.length} 个 Markdown 文件吗？`
  );

  if (!userConfirm) {
    console.log("用户取消了操作");
    return;
  }

  // 实用工具函数
  const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
  
  // 初始化进度变量
  let successCount = 0;
  let errorCount = 0;
  let progressBar;

  // 创建进度条
  if (config.showProgressBar) {
    progressBar = createProgressBar(files.length);
  }

  try {
    // 处理每个文件
    for (const [i, file] of files.entries()) {
      // 检查是否被取消
      if (isCancelled) {
        new Notice("🛑 操作已被用户取消", 3000);
        break;
      }

      try {
        // 更新进度条
        if (config.showProgressBar && !isCancelled) {
          updateProgressBar(progressBar, i, files.length, file.name);
        }

        // 打开文件
        const leaf = app.workspace.getLeaf(true);
        await leaf.openFile(file);
        await sleep(config.delayBetweenFiles);

        // 再次检查是否被取消
        if (isCancelled) break;

        // 执行 ExMemo 命令
        await app.commands.executeCommandById(exmemoCommand);
        await sleep(config.commandDelay);

        // 再次检查是否被取消
        if (isCancelled) break;

        // 执行 Linter 命令
        await app.commands.executeCommandById(linterCommand);
        await sleep(config.delayBetweenFiles);

        // 关闭当前叶子
        leaf.detach();

        successCount++;
        new Notice(`✅ 已处理 [${successCount}/${files.length}]: ${file.name}`, 1000);
      } catch (e) {
        // 如果是用户取消导致的错误，直接终止
        if (e.message === "USER_CANCELLED") {
          break;
        }
        
        errorCount++;
        console.error(`❌ 处理失败：${file.path}`, e);
        new Notice(`❌ 出错跳过：${file.name}`, 1500);
      }
    }
  } finally {
    // 完成后关闭进度条
    if (config.showProgressBar && progressBar) {
      progressBar.hide();
      document.body.removeChild(progressBar.containerEl);
    }

    // 关闭所有处理中打开的markdown标签页
    app.workspace.detachLeavesOfType("markdown");
  }

  // 完成统计 (只有在非取消状态下才显示完成消息)
  if (!isCancelled) {
    new Notice(`🎉 处理完成！成功：${successCount}，失败：${errorCount}，总计：${files.length}`, 5000);
  }

  /**
   * 根据路径获取所有 Markdown 文件
   * @param {string} folderPath - 文件夹路径
   * @param {boolean} recursive - 是否递归子文件夹
   * @returns {TFile[]} Markdown 文件列表
   */
  function getMarkdownFiles(folderPath, recursive) {
    return app.vault.getFiles().filter(file => {
      // 确保是 Markdown 文件
      if (!file.path.endsWith(".md")) return false;
      
      // 检查文件是否在目标文件夹中
      if (folderPath === "/") {
        return recursive || !file.path.includes("/");
      } else {
        const isInFolder = file.path.startsWith(folderPath + "/");
        
        if (!recursive) {
          // 非递归模式：文件必须直接位于指定文件夹中
          const relativePath = file.path.substring(folderPath.length + 1);
          return isInFolder && !relativePath.includes("/");
        }
        
        return isInFolder; // 递归模式：返回所有子文件夹中的文件
      }
    });
  }

  /**
   * 创建进度条
   * @param {number} total - 总文件数
   * @returns {Object} 进度条对象
   */
  function createProgressBar(total) {
    // 创建容器
    const containerEl = document.createElement("div");
    containerEl.style.position = "fixed";
    containerEl.style.top = "10px";
    containerEl.style.left = "50%";
    containerEl.style.transform = "translateX(-50%)";
    containerEl.style.zIndex = "1000";
    containerEl.style.backgroundColor = "var(--background-primary)";
    containerEl.style.padding = "10px 15px";
    containerEl.style.borderRadius = "8px";
    containerEl.style.boxShadow = "0 2px 8px var(--background-modifier-box-shadow)";
    containerEl.style.width = "300px";
    containerEl.style.maxWidth = "80vw";
    containerEl.style.display = "flex";
    containerEl.style.flexDirection = "column";
    containerEl.style.gap = "5px";
    document.body.appendChild(containerEl);

    // 标题
    const titleEl = document.createElement("div");
    titleEl.style.fontWeight = "bold";
    titleEl.style.marginBottom = "5px";
    titleEl.style.display = "flex";
    titleEl.style.justifyContent = "space-between";
    titleEl.textContent = "AI批量处理";
    containerEl.appendChild(titleEl);

    // 进度计数
    const counterEl = document.createElement("div");
    counterEl.style.fontSize = "0.9em";
    counterEl.style.marginBottom = "5px";
    containerEl.appendChild(counterEl);

    // 当前文件名
    const fileNameEl = document.createElement("div");
    fileNameEl.style.fontSize = "0.8em";
    fileNameEl.style.whiteSpace = "nowrap";
    fileNameEl.style.overflow = "hidden";
    fileNameEl.style.textOverflow = "ellipsis";
    fileNameEl.style.color = "var(--text-muted)";
    containerEl.appendChild(fileNameEl);

    // 进度条背景
    const progressBgEl = document.createElement("div");
    progressBgEl.style.width = "100%";
    progressBgEl.style.backgroundColor = "var(--background-modifier-border)";
    progressBgEl.style.height = "6px";
    progressBgEl.style.borderRadius = "3px";
    progressBgEl.style.overflow = "hidden";
    containerEl.appendChild(progressBgEl);

    // 进度条前景
    const progressEl = document.createElement("div");
    progressEl.style.width = "0%";
    progressEl.style.backgroundColor = "var(--interactive-accent)";
    progressEl.style.height = "100%";
    progressEl.style.borderRadius = "3px";
    progressEl.style.transition = "width 0.3s ease";
    progressBgEl.appendChild(progressEl);

    // 取消按钮 - 改进版
    const cancelBtn = document.createElement("button");
    cancelBtn.style.marginTop = "8px";
    cancelBtn.style.padding = "4px 8px";
    cancelBtn.style.border = "none";
    cancelBtn.style.borderRadius = "4px";
    cancelBtn.style.backgroundColor = "var(--background-modifier-error)";
    cancelBtn.style.color = "white";
    cancelBtn.style.cursor = "pointer";
    cancelBtn.style.fontSize = "0.8em";
    cancelBtn.textContent = "取消操作";
    cancelBtn.onclick = () => {
      // 设置取消标志
      isCancelled = true;
      
      // 更新UI显示
      titleEl.textContent = "正在取消...";
      cancelBtn.disabled = true;
      cancelBtn.style.backgroundColor = "var(--background-modifier-border)";
      cancelBtn.textContent = "正在停止...";
      
      // 通知用户
      new Notice("🛑 正在取消批处理操作...", 2000);
    };
    containerEl.appendChild(cancelBtn);

    return {
      containerEl,
      titleEl,
      counterEl,
      fileNameEl,
      progressEl,
      update: (current, total, fileName) => {
        const percent = Math.round((current / total) * 100);
        counterEl.textContent = `进度：${current}/${total} (${percent}%)`;
        fileNameEl.textContent = `正在处理：${fileName}`;
        progressEl.style.width = `${percent}%`;
      },
      hide: () => {
        containerEl.style.display = "none";
      }
    };
  }

  /**
   * 更新进度条
   * @param {Object} progressBar - 进度条对象
   * @param {number} current - 当前处理的索引
   * @param {number} total - 总文件数
   * @param {string} fileName - 当前处理的文件名
   */
  function updateProgressBar(progressBar, current, total, fileName) {
    if (!progressBar) return;
    progressBar.update(current + 1, total, fileName);
  }
};