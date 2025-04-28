<%*
/**
 * 选中指定的标题段落（包括标题本身）
 * 标题符号和标题内容都可以灵活配置
 */

// 配置：标题符号和标题内容
const headingSymbol = "##"; // 标题符号（如：##，###）
const sectionHeading = "memos"; // 标题内容（如：memos，reflection）

const editor = app.workspace.activeEditor?.editor;
if (!editor) {
  new Notice("未找到活动编辑器");
  return;
}

const content = editor.getValue();
const headingPattern = `${headingSymbol} ${sectionHeading}`; // 动态生成完整的标题（如： "## memos"）

const startIndex = content.indexOf(headingPattern);
if (startIndex === -1) {
  new Notice(`⚠️ 未找到 ${headingPattern}`);
  return;
}

// 提取从标题开始到下一个标题或文末
const rest = content.slice(startIndex);
const match = rest.match(new RegExp(`${headingPattern}\n([\\s\\S]*?)(?=\\n${headingSymbol} |\\n*$)`));

if (!match) {
  new Notice(`⚠️ 没有匹配到 ${headingPattern} 内容`);
  return;
}

// 包括标题本身选中
const sectionContent = headingPattern + "\n" + match[1];
const endIndex = startIndex + sectionContent.length;

editor.setSelection(
  editor.offsetToPos(startIndex),
  editor.offsetToPos(endIndex)
);
%>