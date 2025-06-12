---
title: 查询包含标签的行记录
aliases: [查询包含标签的行记录]
tags: []
created: 2024-11-28T17:46:24
updated: 2025-06-08T21:08:40
---

# 查询包含标签的行记录

```js
// 整个代码是先筛选符合标签的笔记，再筛选笔记中的行内容是否具有标签，然后将文件名和行显示在表中。 
// 参考用//注释开关指定查询范围
//tag1限定笔记文件，tag2限定行内容

const tag = "#问答"
// 获取指定文件夹中的所有md文件,支持二级目录
const files = app.vault.getMarkdownFiles().filter(file => file.path.includes("Diary/打卡"))
// 预设标签1，从而限定笔记文件
// 将指定文件夹中,带有标签1的文件筛选出来
const taggedFiles = new Set(files.reduce((acc, file) => {
    const tags = app.metadataCache.getFileCache(file).tags
    if (tags) {
      let filtered = tags.filter(t => t.tag === tag)
      if (filtered) {
        return [...acc, file]
      }
    }
    return acc
}, []))

//创建一个包含文件名和包含所需标记的行的数组
let arr = files.map(async(file) => {
  // 读取限定后的文件，并将其所有内容作为字符串获取
  const content = await app.vault.cachedRead(file)
  //将所有内容转换为行的数组，并提取包含标签“#tag2”的行 
  let lines = await content.split("\n").filter(line => line.includes(tag)) 
    // 删除行中的标记和前置空格,以便于在表中显示。其中“-”是为了删除行中的“-”，“#tag2”是为了删除行中的“#DEF”，“  ”是为了删除行中的空格。
  for(var i=0; i < lines.length; i++) { 
    lines[i] = lines[i].replace(/- /g, '');
    lines[i] = lines[i].replace(/  /g, '');
    lines[i] = lines[i].replace(tag, '');
  }
  //删除被上步骤替换后形成的空行
  console.log(lines)
  // 返回包含标记的行的文件名和行的数组 
  return ["[["+file.name.split(".")[0]+"]]", lines]
})

//解析promises并构建表 
Promise.all(arr).then(values => {
console.log(values)
// 过滤掉没有“#tag2”的行
const exists = values.filter(value => value[1][0])
//构建表，显示文件名和行 
dv.table(["File", "Lines"], exists)
})
```
