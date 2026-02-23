#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SuitAgent工具包装函数
为DocxProcessor和PlaceholderMapper提供简化的调用接口

版本: v1.0
更新: 2025-11-14
作者: SuitAgent整合系统
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from .DocxProcessor import DocxProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_trust_document(
    case_id: str,
    template_name: str,
    yaml_path: str,
    output_dir: str,
    client_type: str = "company",
    template_dir: Optional[str] = None
) -> str:
    """
    生成单个委托文件

    Args:
        case_id: 案件编号（用于日志和文件命名）
        template_name: 模板文件名（不含路径）
        yaml_path: YAML文件路径
        output_dir: 输出目录
        client_type: 委托类型（company=公司，person=个人）
        template_dir: 模板目录（自动根据client_type选择）

    Returns:
        str: 输出文件路径

    Raises:
        FileNotFoundError: 当模板文件或YAML文件不存在时
        Exception: 当生成失败时
    """
    # 自动选择模板目录
    if template_dir is None:
        if client_type == "company":
            template_dir = ".claude/templates/公司委托模板"
        elif client_type == "person":
            template_dir = ".claude/templates/个人委托模板"
        else:
            raise ValueError(f"不支持的委托类型: {client_type}")

    # 构建完整路径
    template_path = os.path.join(template_dir, template_name)
    case_output_dir = os.path.join(output_dir, case_id, "04_法律文书", "委托文件")
    output_filename = f"[{case_id}]_{template_name}"
    output_path = os.path.join(case_output_dir, output_filename)

    logger.info(f"开始生成委托文件: {template_name}")

    # 处理文档
    success = DocxProcessor.process_from_yaml(
        template_path, output_path, yaml_path
    )

    if success:
        logger.info(f"✓ 生成成功: {output_path}")
        return output_path
    else:
        raise Exception(f"生成失败: {output_filename}")


def batch_generate_trust_documents(
    case_id: str,
    yaml_path: str,
    output_dir: str,
    templates: List[str],
    client_type: str = "company",
    template_dir: Optional[str] = None
) -> List[str]:
    """
    批量生成委托文件

    Args:
        case_id: 案件编号
        yaml_path: YAML文件路径
        output_dir: 输出目录
        templates: 模板文件名列表
                 例如: ['委托合同.docx', '授权委托书.docx', '谈话笔录.docx']
        client_type: 委托类型（company=公司，person=个人）
        template_dir: 模板目录（自动根据client_type选择）

    Returns:
        List[str]: 成功生成的文件路径列表

    Raises:
        Exception: 当所有模板都生成失败时
    """
    # 自动选择模板目录
    if template_dir is None:
        if client_type == "company":
            template_dir = ".claude/templates/公司委托模板"
        elif client_type == "person":
            template_dir = ".claude/templates/个人委托模板"
        else:
            raise ValueError(f"不支持的委托类型: {client_type}")
    results = []
    failures = []

    logger.info(f"开始批量生成委托文件: {case_id}")
    logger.info(f"模板列表: {', '.join(templates)}")

    for template in templates:
        try:
            result = generate_trust_document(
                case_id, template, yaml_path, output_dir, template_dir
            )
            results.append(result)
        except Exception as e:
            logger.error(f"模板 {template} 生成失败: {e}")
            failures.append(template)

    # 统计结果
    logger.info(f"批量生成完成: {len(results)}/{len(templates)} 成功")

    if failures:
        logger.warning(f"失败模板: {', '.join(failures)}")

    if not results:
        raise Exception("所有模板生成失败")

    return results


def create_case_yaml_template(
    case_id: str,
    output_path: str
) -> str:
    """
    创建案件YAML模板文件

    Args:
        case_id: 案件编号
        output_path: 输出文件路径

    Returns:
        str: 输出文件路径
    """
    template_content = f"""# 案件基本信息
案件编号: "{case_id}"

案件基本信息:
  委托人信息:
    client_name: ""              # 委托人名称
    client_type: ""              # 委托人类型（公司/自然人）
    client_code: ""              # 统一社会信用代码/身份证号
    client_address: ""           # 住所地/地址
    legal_representative: ""     # 法定代表人
    representative_position: ""  # 法定代表人职位

  律师信息:
    lawyer_name: ""              # 律师姓名
    lawyer_contact: ""           # 联系电话

  案件信息:
    opposing_party: ""           # 对方当事人
    case_cause: ""               # 案由
    case_type: ""                # 案件类型
    client_vs_opponent: ""       # 委托人与对方关系

日期信息:
  year: ""                       # 年份
  month: ""                      # 月份（两位数）
  day: ""                        # 日期（两位数）

案件状态:
  当前状态: "委托确定"            # 当前案件状态
  阶段: "一审"                    # 诉讼阶段
  风险等级: "中"                  # 风险等级

工作进度:
  已完成工作: []
  正在进行: []
  待开始工作: []
"""

    # 确保目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template_content)

    logger.info(f"✓ 创建YAML模板: {output_path}")
    return output_path


def validate_yaml_file(yaml_path: str) -> Tuple[bool, List[str]]:
    """
    验证YAML文件的完整性

    Args:
        yaml_path: YAML文件路径

    Returns:
        Tuple[bool, List[str]]: (是否完整, 缺失字段列表)
    """
    try:
        from .placeholder_mapper import PlaceholderMapper

        # 加载YAML文件
        yaml_data = PlaceholderMapper.load_yaml_from_file(yaml_path)

        # 转换为占位符
        placeholders = PlaceholderMapper.yaml_to_placeholders(yaml_data)

        # 验证必填字段
        missing = PlaceholderMapper.validate_required_fields(placeholders)

        is_complete = len(missing) == 0

        return is_complete, missing

    except Exception as e:
        logger.error(f"验证YAML文件失败: {e}")
        return False, [str(e)]


def get_template_list(template_dir: str = ".claude/templates/公司委托模板") -> List[str]:
    """
    获取可用模板列表

    Args:
        template_dir: 模板目录

    Returns:
        List[str]: 模板文件名列表
    """
    if not os.path.exists(template_dir):
        logger.warning(f"模板目录不存在: {template_dir}")
        return []

    files = os.listdir(template_dir)
    templates = [f for f in files if f.endswith(('.docx', '.doc'))]

    logger.info(f"找到 {len(templates)} 个模板")
    return templates


def print_template_usage():
    """打印模板使用说明"""
    print("=" * 80)
    print("委托文件生成工具使用说明")
    print("=" * 80)
    print("\n1. 准备模板文件")
    print("   将Word模板文件放入 templates/trust/ 目录")
    print("   模板中需要替换的位置使用占位符，如: {client}, {lawyer}")
    print("\n2. 创建案件YAML文件")
    print("   使用 create_case_yaml_template() 函数创建模板")
    print("   填写完整的案件信息")
    print("\n3. 生成委托文件")
    print("   使用 generate_trust_document() 生成单个文件")
    print("   或使用 batch_generate_trust_documents() 批量生成")
    print("\n4. 验证文件")
    print("   使用 validate_yaml_file() 验证YAML完整性")
    print("=" * 80)


def main():
    """主函数 - 用于测试"""
    print_template_usage()

    # 测试模板列表（公司）
    print("\n公司委托模板:")
    templates = get_template_list(".claude/templates/公司委托模板")
    for template in templates[:5]:  # 只显示前5个
        print(f"  - {template}")
    if len(templates) > 5:
        print(f"  ... 还有 {len(templates) - 5} 个文件")

    # 测试模板列表（个人）
    print("\n个人委托模板:")
    templates = get_template_list(".claude/templates/个人委托模板")
    for template in templates[:5]:  # 只显示前5个
        print(f"  - {template}")
    if len(templates) > 5:
        print(f"  ... 还有 {len(templates) - 5} 个文件")

    # 测试YAML验证
    print("\nYAML验证测试:")
    test_yaml_path = "tests/test_case.yaml"
    if os.path.exists(test_yaml_path):
        is_complete, missing = validate_yaml_file(test_yaml_path)
        if is_complete:
            print("  ✓ YAML文件完整")
        else:
            print(f"  ✗ 缺失字段: {', '.join(missing)}")
    else:
        print("  (未找到测试YAML文件)")


if __name__ == "__main__":
    main()
