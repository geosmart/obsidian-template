<%*
/**
 * 将光标定位到 "## summary" 后面的第一行
 */

// 配置：标题符号和标题内容
const headingSymbol = "##"; // 标题符号（如：#，##）
const sectionHeading = "summary"; // 标题内容

// 获取当前活动编辑器
const editor = app.workspace.activeEditor?.editor;
if (!editor) {
  new Notice("未找到活动编辑器");
  return;
}

// 获取文件内容
const content = editor.getValue();
const headingPattern = `${headingSymbol} ${sectionHeading}`; // 完整标题（如： "# 今日小结"）

const startIndex = content.indexOf(headingPattern);
if (startIndex === -1) {
  new Notice(`⚠️ 未找到 ${headingPattern}`);
  return;
}

// 获取标题后面的第一行的开始位置
const rest = content.slice(startIndex + headingPattern.length);
const firstLineEndIndex = rest.indexOf("\n") + startIndex + headingPattern.length + 1; // 标题后的第一行结束位置

if (firstLineEndIndex === startIndex + headingPattern.length) {
  new Notice("没有找到标题后的第一行内容");
  return;
}

// 将光标定位到该位置
const insertPosition = editor.offsetToPos(firstLineEndIndex);
editor.setCursor(insertPosition);
new Notice(`光标定位到${headingPattern}的第一行`);
%>