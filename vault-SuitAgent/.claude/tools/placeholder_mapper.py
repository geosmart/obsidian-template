#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
占位符映射工具
将YAML字段映射为Word模板占位符

版本: v1.0
更新: 2025-11-14
作者: SuitAgent整合系统
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlaceholderMapper:
    """占位符映射器

    将SuitAgent案件YAML数据转换为委托文件生成系统识别的占位符格式
    """

    # 字段映射字典
    # 格式: {YAML字段名: 占位符名}
    FIELD_MAPPING = {
        # 委托人信息
        'client_name': 'client',
        'client_type': 'type',
        'client_code': 'code',
        'client_address': 'address',
        'legal_representative': 'representative',
        'representative_position': 'position',
        # 律师信息
        'lawyer_name': 'lawyer',
        'lawyer_contact': 'tel',
        # 案件信息
        'opposing_party': 'opposite',
        'case_cause': 'cause',
        'case_type': 'case_type',
        'client_vs_opponent': 'client_opponent',
        # 日期信息
        'year': 'year',
        'month': 'month',
        'day': 'day',
    }

    # 必填字段列表
    REQUIRED_FIELDS = {
        'client_name', 'client_type', 'client_code', 'client_address',
        'legal_representative', 'representative_position',
        'lawyer_name', 'lawyer_contact',
        'opposing_party', 'case_cause', 'case_type', 'client_vs_opponent',
        'year', 'month', 'day'
    }

    # 嵌套路径映射
    NESTED_PATH_MAPPING = {
        # 委托人信息路径
        ('委托人信息', 'client_name'): 'client',
        ('委托人信息', 'client_type'): 'type',
        ('委托人信息', 'client_code'): 'code',
        ('委托人信息', 'client_address'): 'address',
        ('委托人信息', 'legal_representative'): 'representative',
        ('委托人信息', 'representative_position'): 'position',
        # 律师信息路径
        ('律师信息', 'lawyer_name'): 'lawyer',
        ('律师信息', 'lawyer_contact'): 'tel',
        # 案件信息路径
        ('案件信息', 'opposing_party'): 'opposite',
        ('案件信息', 'case_cause'): 'cause',
        ('案件信息', 'case_type'): 'case_type',
        ('案件信息', 'client_vs_opponent'): 'client_opponent',
        # 日期信息路径
        ('日期信息', 'year'): 'year',
        ('日期信息', 'month'): 'month',
        ('日期信息', 'day'): 'day',
    }

    @classmethod
    def yaml_to_placeholders(cls, yaml_data: Dict[str, Any]) -> Dict[str, str]:
        """
        将YAML数据转换为占位符字典

        Args:
            yaml_data: 案件YAML数据

        Returns:
            dict: 占位符字典 {占位符: 值}

        Raises:
            KeyError: 当必填字段缺失时
            ValueError: 当字段值无效时
        """
        placeholders = {}

        # 提取委托人信息
        if '案件基本信息' in yaml_data and '委托人信息' in yaml_data['案件基本信息']:
            client_info = yaml_data['案件基本信息']['委托人信息']
            for field, placeholder in {
                'client_name': 'client',
                'client_type': 'type',
                'client_code': 'code',
                'client_address': 'address',
                'legal_representative': 'representative',
                'representative_position': 'position'
            }.items():
                if field in client_info:
                    placeholders[placeholder] = str(client_info[field])
                else:
                    logger.warning(f"委托人信息缺失: {field}")

        # 提取律师信息
        if '案件基本信息' in yaml_data and '律师信息' in yaml_data['案件基本信息']:
            lawyer_info = yaml_data['案件基本信息']['律师信息']
            for field, placeholder in {
                'lawyer_name': 'lawyer',
                'lawyer_contact': 'tel'
            }.items():
                if field in lawyer_info:
                    placeholders[placeholder] = str(lawyer_info[field])
                else:
                    logger.warning(f"律师信息缺失: {field}")

        # 提取案件信息
        if '案件基本信息' in yaml_data and '案件信息' in yaml_data['案件基本信息']:
            case_info = yaml_data['案件基本信息']['案件信息']
            for field, placeholder in {
                'opposing_party': 'opposite',
                'case_cause': 'cause',
                'case_type': 'case_type',
                'client_vs_opponent': 'client_opponent'
            }.items():
                if field in case_info:
                    placeholders[placeholder] = str(case_info[field])
                else:
                    logger.warning(f"案件信息缺失: {field}")

        # 提取日期信息
        if '日期信息' in yaml_data:
            date_info = yaml_data['日期信息']
            for field in ['year', 'month', 'day']:
                if field in date_info:
                    # 确保月份和日期是两位数格式
                    value = str(date_info[field])
                    if field in ['month', 'day'] and len(value) == 1:
                        value = f"0{value}"
                    placeholders[field] = value
                else:
                    logger.warning(f"日期信息缺失: {field}")

        return placeholders

    @classmethod
    def load_yaml_from_file(cls, yaml_file_path: str) -> Dict[str, Any]:
        """
        从文件加载YAML数据

        Args:
            yaml_file_path: YAML文件路径

        Returns:
            dict: YAML数据

        Raises:
            FileNotFoundError: 当文件不存在时
            yaml.YAMLError: 当YAML格式错误时
        """
        if not os.path.exists(yaml_file_path):
            raise FileNotFoundError(f"YAML文件不存在: {yaml_file_path}")

        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f"YAML解析错误: {e}")
            raise

    @classmethod
    def validate_required_fields(cls, placeholders: Dict[str, str]) -> List[str]:
        """
        验证必填字段是否完整

        Args:
            placeholders: 占位符字典（键为占位符名）

        Returns:
            list: 缺失的必填占位符列表（空列表表示验证通过）
        """
        # 将字段名转换为占位符名
        required_placeholders = {
            cls.FIELD_MAPPING[field] for field in cls.REQUIRED_FIELDS
        }

        missing_placeholders = []

        for placeholder in required_placeholders:
            if placeholder not in placeholders or not placeholders[placeholder]:
                missing_placeholders.append(placeholder)

        return missing_placeholders

    @classmethod
    def format_month_day(cls, value: str) -> str:
        """
        格式化月份和日期为两位数

        Args:
            value: 月份或日期值

        Returns:
            str: 格式化后的值
        """
        # 移除前导零并重新格式化
        int_value = int(value)
        return f"{int_value:02d}"

    @classmethod
    def print_mapping_table(cls):
        """打印字段映射表"""
        print("=" * 80)
        print("字段映射表")
        print("=" * 80)
        print(f"{'YAML字段':<40} {'占位符':<20} {'中文名称'}")
        print("-" * 80)

        mapping_info = {
            # 委托人信息
            'client_name': '委托人名称',
            'client_type': '委托人类型',
            'client_code': '代码',
            'client_address': '地址',
            'legal_representative': '法定代表人',
            'representative_position': '职位',
            # 律师信息
            'lawyer_name': '律师姓名',
            'lawyer_contact': '联系电话',
            # 案件信息
            'opposing_party': '对方当事人',
            'case_cause': '案由',
            'case_type': '案件类型',
            'client_vs_opponent': '当事人关系',
            # 日期信息
            'year': '年份',
            'month': '月份',
            'day': '日期',
        }

        for yaml_field, placeholder in cls.FIELD_MAPPING.items():
            chinese_name = mapping_info.get(yaml_field, '')
            print(f"{yaml_field:<40} {{{placeholder}}} {chinese_name}")

        print("=" * 80)


def main():
    """主函数 - 用于测试"""
    # 打印映射表
    PlaceholderMapper.print_mapping_table()

    # 测试数据
    test_yaml_data = {
        '案件基本信息': {
            '委托人信息': {
                'client_name': '张三有限公司',
                'client_type': '公司',
                'client_code': '912345678901234567',
                'client_address': '北京市朝阳区xxx街道',
                'legal_representative': '李四',
                'representative_position': '总经理'
            },
            '律师信息': {
                'lawyer_name': '王五',
                'lawyer_contact': '13800000000'
            },
            '案件信息': {
                'opposing_party': '北京某某公司',
                'case_cause': '买卖合同纠纷',
                'case_type': '民事案件',
                'client_vs_opponent': '张三有限公司诉北京某某公司'
            }
        },
        '日期信息': {
            'year': '2025',
            'month': '11',
            'day': '14'
        }
    }

    # 测试转换
    print("\n" + "=" * 80)
    print("测试数据转换")
    print("=" * 80)

    placeholders = PlaceholderMapper.yaml_to_placeholders(test_yaml_data)

    print("\n转换后的占位符:")
    for key, value in placeholders.items():
        print(f"  {{{key}}}: {value}")

    # 验证必填字段
    missing = PlaceholderMapper.validate_required_fields(placeholders)
    if missing:
        print(f"\n缺失的必填字段: {', '.join(missing)}")
    else:
        print("\n✓ 所有必填字段完整")


if __name__ == "__main__":
    main()
