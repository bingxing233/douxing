// backend/utils/document_parser.py
import PyPDF2
import docx
import pandas as pd
from typing import Union
import os

class DocumentParser:
    """支持多种格式的文档解析器"""
    
    @staticmethod
    def parse_document(file_path: str) -> str:
        """
        根据文件扩展名解析不同格式的文档
        支持PDF、DOCX、TXT、Excel等格式
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.pdf':
            return DocumentParser._parse_pdf(file_path)
        elif ext == '.docx':
            return DocumentParser._parse_docx(file_path)
        elif ext == '.txt':
            return DocumentParser._parse_txt(file_path)
        elif ext in ['.xlsx', '.xls']:
            return DocumentParser._parse_excel(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
    
    @staticmethod
    def _parse_pdf(file_path: str) -> str:
        """解析PDF文件"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            raise Exception(f"PDF解析失败: {str(e)}")
    
    @staticmethod
    def _parse_docx(file_path: str) -> str:
        """解析DOCX文件"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"DOCX解析失败: {str(e)}")
    
    @staticmethod
    def _parse_txt(file_path: str) -> str:
        """解析TXT文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"TXT解析失败: {str(e)}")
    
    @staticmethod
    def _parse_excel(file_path: str) -> str:
        """解析Excel文件"""
        try:
            df = pd.read_excel(file_path)
            return df.to_string()
        except Exception as e:
            raise Exception(f"Excel解析失败: {str(e)}")
    
    @staticmethod
    def extract_candidate_info(resume_text: str) -> dict:
        """
        从简历文本中提取候选人信息
        返回结构化数据
        """
        # 这里可以使用NLP技术或正则表达式提取信息
        # 简化实现，实际应更复杂
        return {
            "name": "候选人姓名",
            "email": "candidate@example.com",
            "phone": "13800138000",
            "education": "学历信息",
            "experience": "工作经验",
            "skills": ["技能1", "技能2", "技能3"]
        }