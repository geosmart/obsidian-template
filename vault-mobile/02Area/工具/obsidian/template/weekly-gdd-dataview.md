```dataviewjs
// 配置常量
const DIARY_PATH = 'Diary';
const GDD_TAGS = { '#good': '👍', '#difficult': '💪', '#different': '🌟' };

// 解析周报元数据
const parseWeekMeta = fileName => {
    const [year, week] = fileName.match(/(\d+)-W(\d+)/).slice(1);
    return { year, weekNumber: parseInt(week) };
};

// 获取周日期范围
const getWeekRange = (year, weekNumber) => ({
    start: moment().year(year).isoWeek(weekNumber).startOf('isoWeek'),
    end: moment().year(year).isoWeek(weekNumber).endOf('isoWeek')
});

// 获取周日记文件
const getWeeklyNotes = (diaryPath, year, { start, end }) => 
    dv.pages(`"${diaryPath}/${year}"`)
        .where(p => moment(p.file.name, "YYYY-MM-DD").isBetween(start, end, null, '[]'))
        .sort(page => page.file.cday, 'asc');

// 提取分类Memo
const extractTagMemos = (dailyNotes, tags) => {
    const tagMap = Object.keys(tags).reduce((acc, tag) => (acc[tag] = [], acc), {});
    const tagRegex = new RegExp(`(${Object.keys(tags).join('|')})\\b`, 'g');
    
    dailyNotes.forEach(page => 
        page.file.lists?.forEach(list => {
            if (list.section?.subpath !== 'memos') return;
            
            const cleanText = list.text
                .replace(tagRegex, '')
                .replace(/\s{2,}/g, ' ')
                .trim();
            
            if (!cleanText) return;
            
            list.text.match(tagRegex)?.forEach(tag => 
                tagMap[tag]?.push(`${page.file.name} ${cleanText}`)
            );
        })
    );
    return tagMap;
};

// 渲染分类列表
const renderCategories = (tagMap, emojiMap) => {
    dv.header(3, "📊 本周GDD统计");
    Object.entries(tagMap).forEach(([tag, items]) => {
        if (!items.length) return;
        dv.header(3, `${emojiMap[tag]} ${tag} · ${items.length}条`);
        dv.list(items);
    });
};

// 主流程
const { year, weekNumber } = parseWeekMeta(dv.current().file.name);
const weekRange = getWeekRange(year, weekNumber);
const dailyNotes = getWeeklyNotes(DIARY_PATH, year, weekRange);
const tagMap = extractTagMemos(dailyNotes, GDD_TAGS);

renderCategories(tagMap, GDD_TAGS);
```