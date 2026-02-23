#!/usr/bin/env python3
"""
SuitAgent 路径引用更新工具

用途：自动更新项目中所有配置文件路径的引用
使用：python .claude/tools/update_paths.py
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# ==================== 配置 ====================

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 路径替换映射
PATH_REPLACEMENTS = {
    # 旧的配置文件路径 → 新的规则文件路径
    '.claude/config/agent-mappings.yaml': '.claude/rules/AgentMapping.md',
    '.claude/config/case-directories.yaml': '.claude/rules/AgentMapping.md',

    # 旧的工作流文件名 → 新的文件名
    '.claude/rules/workflows.md': '.claude/rules/WorkflowSystem.md',
    '.claude/rules/scenarios.md': '.claude/rules/AgentMapping.md',
}

# 需要扫描的目录
SCAN_DIRECTORIES = [
    '.claude/agents/',
    '.claude/commands/',
]

# 文件扩展名
FILE_EXTENSIONS = ['.md']

# ==================== 工具函数 ====================

def find_files_to_update() -> List[Path]:
    """查找需要更新的文件"""
    files = []
    for directory in SCAN_DIRECTORIES:
        dir_path = PROJECT_ROOT / directory
        if not dir_path.exists():
            continue

        for ext in FILE_EXTENSIONS:
            files.extend(dir_path.rglob(f'*{ext}'))

    # 也检查主文档
    main_doc = PROJECT_ROOT / 'CLAUDE.md'
    if main_doc.exists():
        files.append(main_doc)

    return sorted(files)

def update_file_paths(file_path: Path) -> Tuple[int, List[str]]:
    """更新单个文件中的路径引用

    Returns:
        (替换数量, 替换详情列表)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    replacements = []

    # 执行所有替换
    for old_path, new_path in PATH_REPLACEMENTS.items():
        # 匹配各种格式的引用
        # 1. 标准链接格式：[text](path)
        pattern_link = rf'\[{ old_path.replace('/', r'\/') }\]'
        if re.search(pattern_link, content):
            content = re.sub(pattern_link, f'[{new_path}]', content)
            replacements.append(f'  {old_path} → {new_path} (链接格式)')

        # 2. 直接文本引用
        if old_path in content:
            content = content.replace(old_path, new_path)
            replacements.append(f'  {old_path} → {new_path}')

    # 如果有变化，写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return len(replacements), replacements

    return 0, []

def verify_paths() -> bool:
    """验证所有目标路径是否存在"""
    all_valid = True
    for old_path, new_path in PATH_REPLACEMENTS.items():
        target = PROJECT_ROOT / new_path
        if not target.exists():
            print(f"⚠️  警告：目标路径不存在: {new_path}")
            all_valid = False
    return all_valid

def scan_old_references() -> List[Tuple[Path, str]]:
    """扫描是否还有旧的路径引用"""
    files_with_old_refs = []
    files = find_files_to_update()

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for old_path in PATH_REPLACEMENTS.keys():
            if old_path in content:
                files_with_old_refs.append((file_path, old_path))

    return files_with_old_refs

# ==================== 主函数 ====================

def main():
    """主函数"""
    print("=" * 60)
    print("SuitAgent 路径引用更新工具")
    print("=" * 60)
    print()

    # 1. 验证目标路径
    print("🔍 验证目标路径...")
    if not verify_paths():
        print("⚠️  警告：部分目标路径不存在，请确认！")
        print()
    else:
        print("✅ 所有目标路径验证通过")
        print()

    # 2. 查找需要更新的文件
    print("🔍 扫描需要更新的文件...")
    files = find_files_to_update()
    print(f"找到 {len(files)} 个文件需要检查")
    print()

    # 3. 执行更新
    print("🔄 执行路径更新...")
    print()

    total_files = 0
    total_replacements = 0
    update_details = []

    for file_path in files:
        rel_path = file_path.relative_to(PROJECT_ROOT)
        count, replacements = update_file_paths(file_path)

        if count > 0:
            total_files += 1
            total_replacements += count
            update_details.append((rel_path, count, replacements))

    # 4. 输出更新报告
    if total_files == 0:
        print("✅ 所有文件都是最新的，无需更新")
    else:
        print("=" * 60)
        print("更新报告")
        print("=" * 60)
        print()
        print(f"📊 统计信息:")
        print(f"  - 扫描文件: {len(files)} 个")
        print(f"  - 更新文件: {total_files} 个")
        print(f"  - 替换引用: {total_replacements} 处")
        print()

        print("📝 更新详情:")
        for file_path, count, replacements in update_details:
            print(f"✅ {file_path} ({count} 处)")
            for detail in replacements:
                print(f"{detail}")
            print()

    # 5. 扫描遗留的旧引用
    print()
    print("🔍 检查遗留的旧引用...")
    old_refs = scan_old_references()
    if old_refs:
        print(f"⚠️  发现 {len(old_refs)} 处旧引用未更新:")
        for file_path, old_path in old_refs:
            print(f"  - {file_path.relative_to(PROJECT_ROOT)}: {old_path}")
    else:
        print("✅ 没有发现遗留的旧引用")

    print()
    print("=" * 60)
    if total_files > 0:
        print("✅ 路径引用更新完成！")
    else:
        print("✅ 路径引用检查完成，所有文件已是最新！")
    print("=" * 60)

if __name__ == '__main__':
    main()
