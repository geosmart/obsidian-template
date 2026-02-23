#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健壮的PDF文本提取工具
支持多种提取方法和OCR识别

使用方法:
1. 作为独立工具调用:
   python3 .claude/tools/pdf_processor.py <PDF文件路径> [输出目录]

2. 在Agent中调用:
   from .claude.tools.pdf_processor import extract_pdf_text

作者: SuitAgent
版本: 1.0
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

from pypdf import PdfReader
from pdfplumber import open as pdfplumber_open
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import json
from datetime import datetime


class PDFProcessor:
    """PDF文本提取处理器"""

    def __init__(self, dpi=300, max_pages=None):
        self.dpi = dpi
        self.max_pages = max_pages
        self.stats = {
            'total_pages': 0,
            'text_pages': 0,
            'ocr_pages': 0,
            'failed_pages': 0,
            'processing_time': 0
        }

    def extract_with_pypdf(self, pdf_path):
        """方法1: 使用pypdf提取文本（适用于有文字层的PDF）"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text += page_text + "\n\n"
                    self.stats['text_pages'] += 1
            return text if text.strip() else None
        except Exception as e:
            print(f"⚠️ pypdf提取失败: {e}")
            return None

    def extract_with_pdfplumber(self, pdf_path):
        """方法2: 使用pdfplumber提取文本（更好的布局保留）"""
        try:
            text = ""
            with pdfplumber_open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    if self.max_pages and i >= self.max_pages:
                        break

                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text += f"\n--- 第 {i+1} 页 ---\n"
                        text += page_text + "\n\n"
                        self.stats['text_pages'] += 1
            return text if text.strip() else None
        except Exception as e:
            print(f"⚠️ pdfplumber提取失败: {e}")
            return None

    def preprocess_image(self, image):
        """图像预处理 - 提高OCR准确率"""
        # 转换为灰度图
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 增强对比度
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)

        # 轻微锐化
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.5)

        return image

    def extract_with_ocr(self, pdf_path):
        """方法3: 使用OCR提取文本（适用于扫描件）"""
        try:
            print("📄 检测为扫描PDF，开始OCR识别...")
            print(f"   分辨率: {self.dpi} DPI")

            # 转换PDF到图片
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                fmt='png',
                thread_count=2  # 控制内存使用
            )

            self.stats['total_pages'] = len(images)

            text = ""
            for i, image in enumerate(images):
                if self.max_pages and i >= self.max_pages:
                    break

                # 预处理图像
                image = self.preprocess_image(image)

                try:
                    # OCR识别
                    page_text = pytesseract.image_to_string(
                        image,
                        lang='chi_sim+eng',
                        config='--psm 6'  # 假设统一文本块
                    )

                    if page_text and page_text.strip():
                        text += f"\n--- 第 {i+1} 页 ---\n"
                        text += page_text + "\n\n"
                        self.stats['ocr_pages'] += 1
                        print(f"   第 {i+1} 页 OCR完成")
                    else:
                        self.stats['failed_pages'] += 1
                        print(f"   第 {i+1} 页 无识别内容")

                except Exception as e:
                    self.stats['failed_pages'] += 1
                    print(f"   ⚠️ 第 {i+1} 页 OCR失败: {e}")

            return text if text.strip() else None

        except Exception as e:
            print(f"❌ OCR提取失败: {e}")
            return None

    def process_pdf(self, pdf_path, output_dir=None):
        """
        处理PDF文件的主方法
        尝试多种提取方法，优先级：pypdf → pdfplumber → OCR
        """
        start_time = datetime.now()

        if not os.path.exists(pdf_path):
            print(f"❌ 文件不存在: {pdf_path}")
            return None, self.stats

        file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # MB
        print(f"📄 处理文件: {os.path.basename(pdf_path)}")
        print(f"   大小: {file_size:.2f} MB")

        extracted_text = None

        # 方法1: 尝试pypdf（快速）
        print("\n🔍 方法1: pypdf文本提取...")
        extracted_text = self.extract_with_pypdf(pdf_path)
        if extracted_text:
            print("✅ pypdf提取成功")
        else:
            # 方法2: 尝试pdfplumber（更好布局）
            print("\n🔍 方法2: pdfplumber文本提取...")
            extracted_text = self.extract_with_pdfplumber(pdf_path)
            if extracted_text:
                print("✅ pdfplumber提取成功")
            else:
                # 方法3: OCR（适用于扫描件）
                if file_size < 50:  # OCR内存限制
                    extracted_text = self.extract_with_ocr(pdf_path)
                    if extracted_text:
                        print("✅ OCR提取成功")
                else:
                    print("⚠️ 文件过大，跳过OCR")

        if not extracted_text:
            print("\n❌ 所有提取方法都失败了")
            self.stats['processing_time'] = (datetime.now() - start_time).total_seconds()
            return None, self.stats

        # 保存提取的文本
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

            # 保存Markdown
            md_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(pdf_path))[0]}.md")
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write("# PDF文本提取结果\n\n")
                f.write(extracted_text)
            print(f"\n✅ Markdown文件已保存: {md_path}")

            # 保存统计信息
            self.stats['processing_time'] = (datetime.now() - start_time).total_seconds()
            stats_path = os.path.join(output_dir, "提取统计.json")
            with open(stats_path, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
            print(f"✅ 统计信息已保存: {stats_path}")

        return extracted_text, self.stats

    def get_stats(self):
        """获取处理统计"""
        return self.stats


def extract_pdf_text(pdf_path, output_dir=None, dpi=300, max_pages=None):
    """
    独立的PDF文本提取函数

    参数:
        pdf_path: PDF文件路径
        output_dir: 输出目录（可选）
        dpi: OCR分辨率（默认300）
        max_pages: 最大页数限制（可选）

    返回:
        tuple: (提取的文本, 统计信息)
    """
    processor = PDFProcessor(dpi=dpi, max_pages=max_pages)
    return processor.process_pdf(pdf_path, output_dir)


def main():
    """命令行使用"""
    if len(sys.argv) < 2:
        print("用法: python3 .claude/tools/pdf_processor.py <PDF文件路径> [输出目录]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    text, stats = extract_pdf_text(pdf_path, output_dir)

    if text:
        print(f"\n✅ 文本提取完成！共提取 {len(text)} 字符")

        # 显示统计信息
        print("\n📊 处理统计:")
        print(f"   总页数: {stats['total_pages']}")
        print(f"   文本页: {stats['text_pages']}")
        print(f"   OCR页: {stats['ocr_pages']}")
        print(f"   失败页: {stats['failed_pages']}")
        print(f"   处理时间: {stats['processing_time']:.2f} 秒")
    else:
        print("\n❌ 文本提取失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
