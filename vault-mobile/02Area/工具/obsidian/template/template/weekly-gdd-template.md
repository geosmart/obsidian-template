<%*
// GDD 周报生成模板
// 此模板根据指定周内的日记生成 GDD（好的、困难的、不同的）周报
// 添加了详细的中文注释和日志输出

// 配置常量
const DIARY_PATH = 'Diary';
const GDD_TAGS = { '#good': '👍', '#difficult': '💪', '#different': '🌟' };

// 日志输出函数
const log = (message) => {
    console.log(message);
}

log("🚀 开始生成GDD周报…");

// 从文件名获取年份和周数
const fileName = tp.file.title;
const match = fileName.match(/(\d+)-W(\d+)/);
if (!match) {
    log("❌ 错误：文件名格式应为 YYYY-WXX");
    new Notice('文件名格式应为 YYYY-WXX，如 2025-W12');
    return;
}

const year = match[1];
const weekNumber = parseInt(match[2]);
log(`📅 解析文件名：${fileName}，年份：${year}，周数：${weekNumber}`);

// 获取该周的开始和结束日期
const startDate = moment().year(year).isoWeek(weekNumber).startOf('isoWeek').format('YYYY-MM-DD');
const endDate = moment().year(year).isoWeek(weekNumber).endOf('isoWeek').format('YYYY-MM-DD');
log(`📆 周范围：${startDate} 至 ${endDate}`);

// 生成该周的日期数组
const dates = [];
let currentDate = moment(startDate);
while (currentDate <= moment(endDate)) {
    dates.push(currentDate.format('YYYY-MM-DD'));
    currentDate.add(1, 'days');
}
log(`📊 本周包含 ${dates.length} 天`);

// 初始化标签映射，用于存储备忘录
const tagMap = Object.keys(GDD_TAGS).reduce((acc, tag) => (acc[tag] = [], acc), {});
const tagRegex = new RegExp(`(${Object.keys(GDD_TAGS).join('|')})\\b`, 'g');
log(`🏷️ 初始化标签类别：${Object.keys(GDD_TAGS).join(', ')}`);

// 处理周内每一天的日记
let processedFiles = 0;
let totalMemos = 0;
for (const date of dates) {
    const filePath = `${DIARY_PATH}/${year}/${date}`;
    const file = app.vault.getAbstractFileByPath(`${filePath}.md`);
    
    if (file) {
        log(`📄 处理日记文件：${date}`);
        processedFiles++;
        const content = await app.vault.read(file);
        const memoSection = content.match(/## memos\n([\s\S]*?)(?=\n##|$)/);
        
        if (memoSection) {
            const memoLines = memoSection[1].split('\n')
                .filter(line => line.trim().startsWith('- ') || line.trim().startsWith('* '))
                .map(line => line.substring(2).trim());
            log(`📝 发现 ${memoLines.length} 条备忘录`);
            
            for (const memo of memoLines) {
                const tags = memo.match(tagRegex);
                if (tags) {
                    for (const tag of tags) {
                        const cleanText = memo.replace(tagRegex, '').replace(/\s{2,}/g, ' ').trim();
                        if (cleanText) {
                            tagMap[tag].push(`${date} ${cleanText}`);
                            totalMemos++;
                            log(`✅ 添加 ${tag} 标签备忘录: ${cleanText.substring(0, 20)}…`);
                        }
                    }
                }
            }
        } else {
            log(`⚠️ 未在 ${date} 找到 memos 部分`);
        }
    } else {
        log(`ℹ️ 未找到 ${date} 的日记文件`);
    }
}

// 渲染分类
for (const [tag, items] of Object.entries(tagMap)) {
    if (items.length > 0) {
        const header=tag.split("#")[1]
        tR += `### ${GDD_TAGS[tag]} ${header} · ${items.length}条\n\n`;
        for (const item of items) {
            tR += `* ${item}\n`;
        }
    }
}
new Notice(`✨ GDD周报生成完成！`, 3000);
%>