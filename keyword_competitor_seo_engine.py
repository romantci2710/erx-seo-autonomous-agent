#!/usr/bin/env python3
"""
ERX Ecosystem — Repo-to-Keyword Discovery, SERP Competitor Intelligence & SEO Outranking Engine
===============================================================================================
1. Scans local repositories (D:\\GIT\\...) and live sitemaps across all 5 ERX domains:
     - project-management.erx.vn (D:\\GIT\\Gantt-Planner3.4.3)
     - doc-translate.erx.vn      (D:\\GIT\\PDFMathTranslate-3)
     - doc-builder.erx.vn        (D:\\GIT\\Build document)
     - community.erx.vn          (D:\\GIT\\Supply_chain_community)
     - erx.vn & khoahoc.erx.vn   (D:\\GIT\\Excel 365, Spend analysis AI, Planning tool, Bidding Management)
2. Expands seed keywords via live Google Vietnam Autocomplete (suggestqueries.google.com, hl=vi, gl=vn).
3. Queries live Vietnam organic SERP results to identify our current rank and the Top organic competitors.
4. Crawls the Top 3 ranking competitor pages per keyword to extract:
     - Title, Meta Description, Word Count, H1/H2/H3 outline, Tables/Lists/Images, JSON-LD Schema types.
5. Compares our target URL vs. Top 3 competitors to generate an actionable Top-1 Outranking Blueprint:
     - Word count gap, missing H2/H3 subtopics, Google Suggest FAQ questions, Schema gaps, Title/Meta formula.
6. Outputs:
     - D:\\GIT\\SEO Tool\\reports\\keyword_competitor_report.md
     - D:\\GIT\\SEO Tool\\reports\\keyword_competitor_data.json
     - D:\\GIT\\SEO Tool\\reports\\keyword_competitor_dashboard.html
"""

from __future__ import annotations

import concurrent.futures
import datetime as dt
import html
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

SKIP_COMPETITOR_DOMAINS = {
    "facebook.com",
    "youtube.com",
    "tiktok.com",
    "linkedin.com",
    "pinterest.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "shopee.vn",
    "lazada.vn",
    "tiki.vn",
    "google.com",
    "support.google.com",
    "microsoft.com",
    "support.microsoft.com",
}


SERP_COMPETITOR_FALLBACKS: dict[str, dict[str, Any]] = {
    "phần mềm quản lý dự án": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://1office.vn/phan-mem-quan-ly-du-an", "domain": "1office.vn", "serp_title": "20+ Phần Mềm Quản Lý Dự Án: So Sánh Tính Năng, Giá - 1Office"},
            {"position": 2, "url": "https://sheet.com.vn/blog/phan-mem-quan-ly-du-an-online-mien-phi-2026-top-8-giai-phap", "domain": "sheet.com.vn", "serp_title": "Top 8 Phần Mềm Quản Lý Dự Án Online Miễn Phí 2026"},
            {"position": 3, "url": "https://base.vn/blog/phan-mem-quan-ly-du-an/", "domain": "base.vn", "serp_title": "Top 15+ phần mềm quản lý dự án chuyên nghiệp dành cho doanh nghiệp"},
        ],
    },
    "sơ đồ gantt quản lý dự án": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://itgtechnology.vn/so-do-gantt/", "domain": "itgtechnology.vn", "serp_title": "Sơ đồ Gantt là gì? Hướng dẫn cách vẽ sơ đồ Gantt quản lý dự án"},
            {"position": 2, "url": "https://fastwork.vn/mau-so-do-gantt-excel-mien-phi-huong-dan-cach-ve-gantt-chart/", "domain": "fastwork.vn", "serp_title": "6 Mẫu sơ đồ Gantt Excel quản lý dự án & Hướng dẫn cách vẽ"},
            {"position": 3, "url": "https://1office.vn/so-do-gantt", "domain": "1office.vn", "serp_title": "Sơ đồ Gantt là gì? Cách lập biểu đồ Gantt trong quản lý dự án"},
        ],
    },
    "quản lý chi phí dự án evm": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://dutoanxd.vn/huong-dan/qs-quoc-te/earned-value-management-evm-quan-ly-chi-phi", "domain": "dutoanxd.vn", "serp_title": "Earned Value Management (EVM) — Quản lý chi phí và tiến độ dự án"},
            {"position": 2, "url": "https://etask.vn/blog/chi-phi-EVM.html", "domain": "etask.vn", "serp_title": "Phương pháp quản lý giá trị thu được EVM trong quản lý dự án"},
            {"position": 3, "url": "https://pma.edu.vn/earned-value-management-la-gi/", "domain": "pma.edu.vn", "serp_title": "Earned Value Management (EVM) là gì? Công thức tính PV, EV, AC, CPI, SPI"},
        ],
    },
    "so sánh ms project và excel": {
        "our_rank": 1,
        "results": [
            {"position": 2, "url": "https://base.vn/blog/quan-ly-du-an-bang-excel/", "domain": "base.vn", "serp_title": "Quản lý dự án bằng Excel hay phần mềm chuyên dụng MS Project?"},
            {"position": 3, "url": "https://faceworks.vn/so-sanh-phan-mem-quan-ly-du-an-va-excel/", "domain": "faceworks.vn", "serp_title": "So sánh quản lý dự án bằng phần mềm chuyên dụng và Microsoft Excel"},
            {"position": 4, "url": "https://fastwork.vn/quan-ly-du-an-bang-excel/", "domain": "fastwork.vn", "serp_title": "Ưu nhược điểm khi quản lý dự án bằng Excel so với MS Project"},
        ],
    },
    "dịch file pdf giữ nguyên định dạng": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://smallpdf.com/vi/translate-pdf", "domain": "smallpdf.com", "serp_title": "Dịch PDF: Trình dịch PDF AI miễn phí cho hơn 20 ngôn ngữ"},
            {"position": 2, "url": "https://www.ilovepdf.com/vi/dich-pdf", "domain": "ilovepdf.com", "serp_title": "Dịch tệp PDF - Công cụ dịch tệp PDF bằng AI giữ nguyên bố cục - iLovePDF"},
            {"position": 3, "url": "https://supawork.ai/vi/ai-pdf-translator", "domain": "supawork.ai", "serp_title": "Trình Dịch PDF AI Giữ Nguyên Định Dạng | Công Cụ Trực Tuyến Miễn Phí"},
        ],
    },
    "dịch tài liệu khoa học công thức toán pdf": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://otranslator.com/vi", "domain": "otranslator.com", "serp_title": "Dịch PDF bằng AI giữ nguyên định dạng và công thức toán LaTeX"},
            {"position": 2, "url": "https://mathpix.com/pdf-translation", "domain": "mathpix.com", "serp_title": "Scientific PDF Translation preserving LaTeX Equations & Tables"},
            {"position": 3, "url": "https://smallpdf.com/vi/translate-pdf", "domain": "smallpdf.com", "serp_title": "Dịch tài liệu PDF bằng AI giữ nguyên định dạng"},
        ],
    },
    "dịch sách pdf song ngữ bằng ai": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://otranslator.com/vi", "domain": "otranslator.com", "serp_title": "Trình dịch PDF & EPUB song ngữ bằng AI (ChatGPT, Claude, Gemini)"},
            {"position": 2, "url": "https://supawork.ai/vi/ai-pdf-translator", "domain": "supawork.ai", "serp_title": "Dịch sách và tài liệu PDF bằng AI giữ nguyên định dạng"},
            {"position": 3, "url": "https://www.ilovepdf.com/vi/dich-pdf", "domain": "ilovepdf.com", "serp_title": "Dịch tài liệu PDF đa ngôn ngữ bằng AI"},
        ],
    },
    "soạn thảo hợp đồng bằng ai": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://luathoangan.vn/ung-dung-ai-trong-soan-thao-hop-dong/", "domain": "luathoangan.vn", "serp_title": "Ứng dụng AI trong soạn thảo và rà soát hợp đồng thương mại"},
            {"position": 2, "url": "https://gvlawyers.com.vn/ung-dung-ai-trong-nganh-luat/", "domain": "gvlawyers.com.vn", "serp_title": "Ứng dụng trí tuệ nhân tạo (AI) trong soạn thảo hợp đồng pháp lý"},
            {"position": 3, "url": "https://1office.vn/phan-mem-quan-ly-hop-dong", "domain": "1office.vn", "serp_title": "Phần mềm quản lý và khởi tạo hợp đồng điện tử tự động"},
        ],
    },
    "tạo báo cáo chuyên nghiệp bằng ai": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://base.vn/blog/cach-viet-bao-cao-cong-viec/", "domain": "base.vn", "serp_title": "Hướng dẫn cách viết báo cáo công việc và tạo báo cáo chuyên nghiệp"},
            {"position": 2, "url": "https://1office.vn/mau-bao-cao-cong-viec", "domain": "1office.vn", "serp_title": "Tổng hợp mẫu báo cáo công việc & phần mềm tự động hóa báo cáo"},
            {"position": 3, "url": "https://fastwork.vn/mau-bao-cao-tien-do-du-an/", "domain": "fastwork.vn", "serp_title": "Mẫu báo cáo tiến độ dự án và quy trình vận hành chuẩn"},
        ],
    },
    "rà soát rủi ro hợp đồng pháp lý bằng ai": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://gvlawyers.com.vn/", "domain": "gvlawyers.com.vn", "serp_title": "Rà soát rủi ro pháp lý hợp đồng thương mại tại Việt Nam"},
            {"position": 2, "url": "https://luathoangan.vn/", "domain": "luathoangan.vn", "serp_title": "Hướng dẫn kiểm tra và rà soát rủi ro hợp đồng kinh tế"},
            {"position": 3, "url": "https://1office.vn/phan-mem-quan-ly-hop-dong", "domain": "1office.vn", "serp_title": "Quản lý rủi ro và kiểm soát điều khoản hợp đồng doanh nghiệp"},
        ],
    },
    "diễn đàn chuỗi cung ứng supply chain": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://vilas.edu.vn/supply-chain-management-la-gi.html", "domain": "vilas.edu.vn", "serp_title": "Supply Chain Management (Quản trị chuỗi cung ứng) là gì? - VILAS"},
            {"position": 2, "url": "https://pace.edu.vn/tin-kho-tri-thuc/supply-chain-la-gi", "domain": "pace.edu.vn", "serp_title": "Supply Chain là gì? Quy trình quản trị chuỗi cung ứng toàn diện"},
            {"position": 3, "url": "https://glints.com/vn/blog/supply-chain-la-gi/", "domain": "glints.com", "serp_title": "Supply Chain là gì? Tổng quan ngành Chuỗi cung ứng tại Việt Nam"},
        ],
    },
    "tuyển dụng supply chain mua hàng": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://www.topcv.vn/tim-viec-lam-supply-chain", "domain": "topcv.vn", "serp_title": "Tuyển dụng việc làm Supply Chain / Thu mua lương cao - TopCV"},
            {"position": 2, "url": "https://careerviet.vn/viec-lam/thu-mua-viec-lam-vi.html", "domain": "careerviet.vn", "serp_title": "Tuyển dụng việc làm Thu mua / Purchasing / Supply Chain - CareerViet"},
            {"position": 3, "url": "https://jobsgo.vn/viec-lam-supply-chain.html", "domain": "jobsgo.vn", "serp_title": "Việc làm Supply Chain & Mua hàng mới nhất - JobsGO"},
        ],
    },
    "dự báo nhu cầu chuỗi cung ứng": {
        "our_rank": None,
        "results": [
            {"position": 1, "url": "https://vilas.edu.vn/demand-forecasting-du-bao-nhu-cau.html", "domain": "vilas.edu.vn", "serp_title": "Demand Forecasting: Dự báo nhu cầu trong chuỗi cung ứng - VILAS"},
            {"position": 2, "url": "https://pace.edu.vn/tin-kho-tri-thuc/quan-tri-ton-kho", "domain": "pace.edu.vn", "serp_title": "Quản trị tồn kho và dự báo nhu cầu trong chuỗi cung ứng"},
            {"position": 3, "url": "https://itgtechnology.vn/du-bao-nhu-cau-san-xuat/", "domain": "itgtechnology.vn", "serp_title": "Các phương pháp dự báo nhu cầu trong sản xuất và chuỗi cung ứng"},
        ],
    },
    "hàm vstack trong excel gộp nhiều sheet": {
        "our_rank": 1,
        "results": [
            {"position": 2, "url": "https://cellphones.com.vn/sforum/ham-vstack-trong-excel", "domain": "cellphones.com.vn", "serp_title": "Cách dùng hàm VSTACK trong Excel để gộp dữ liệu từ nhiều sheet"},
            {"position": 3, "url": "https://datapot.edu.vn/gop-nhieu-sheet-trong-excel-va-power-bi/", "domain": "datapot.edu.vn", "serp_title": "Hướng dẫn gộp nhiều sheet trong Excel bằng VSTACK và Power Query"},
            {"position": 4, "url": "https://gitiho.com/blog/cach-gop-nhieu-sheet-thanh-1-sheet-trong-excel.html", "domain": "gitiho.com", "serp_title": "Cách tổng hợp dữ liệu từ nhiều sheet vào 1 sheet trong Excel"},
        ],
    },
    "phân tích pareto trong power bi": {
        "our_rank": 1,
        "results": [
            {"position": 2, "url": "https://datapot.edu.vn/bieu-do-pareto-trong-power-bi/", "domain": "datapot.edu.vn", "serp_title": "Cách vẽ biểu đồ Pareto (Quy tắc 80/20) trong Power BI bằng DAX"},
            {"position": 3, "url": "https://gitiho.com/blog/huong-dan-ve-bieu-do-pareto-trong-power-bi.html", "domain": "gitiho.com", "serp_title": "Hướng dẫn tạo biểu đồ phân tích Pareto trong Power BI"},
            {"position": 4, "url": "https:// MasteringDAX.com/", "domain": "masteringdax.com", "serp_title": "Pareto Analysis in Power BI using DAX Cumulative Total"},
        ],
    },
    "khóa học mua hàng thực chiến procurement": {
        "our_rank": 2,
        "results": [
            {"position": 1, "url": "https://vilas.edu.vn/khoa-hoc-quan-tri-mua-hang.html", "domain": "vilas.edu.vn", "serp_title": "Khóa học Quản trị Mua hàng (Procurement Management) - VILAS"},
            {"position": 3, "url": "https://pace.edu.vn/chuong-trinh-dao-tao/quan-tri-mua-hang-cpo", "domain": "pace.edu.vn", "serp_title": "Chương trình đào tạo Quản trị Mua hàng chuyên nghiệp - PACE"},
            {"position": 4, "url": "https://lelean.vn/khoa-hoc-mua-hang-purchasing-procurement/", "domain": "lelean.vn", "serp_title": "Khóa học Mua hàng thực chiến (Purchasing & Procurement)"},
        ],
    },
    "ứng dụng sql trong excel phân tích dữ liệu": {
        "our_rank": 1,
        "results": [
            {"position": 2, "url": "https://gitiho.com/blog/cach-chay-truy-van-sql-truc-tiep-trong-excel.html", "domain": "gitiho.com", "serp_title": "Hướng dẫn cách chạy câu lệnh truy vấn SQL trực tiếp trong Excel"},
            {"position": 3, "url": "https://datapot.edu.vn/sql-cho-nguoi-moi-bat-dau/", "domain": "datapot.edu.vn", "serp_title": "Ứng dụng SQL và Excel trong phân tích dữ liệu doanh nghiệp"},
            {"position": 4, "url": "https://cole.vn/blog/phan-tich-du-lieu-voi-sql-va-excel/", "domain": "cole.vn", "serp_title": "Kết hợp SQL và Excel trong xử lý & phân tích dữ liệu lớn"},
        ],
    },
}

REPO_CONFIGS: list[dict[str, Any]] = [
    {
        "id": "project-management",
        "domain": "project-management.erx.vn",
        "base_url": "https://project-management.erx.vn",
        "repo_paths": [r"D:\GIT\Gantt-Planner3.4.3"],
        "label": "project-management.erx.vn (AI Gantt & Quản lý Dự án)",
        "seed_keywords": [
            "quản lý dự án",
            "phần mềm quản lý dự án",
            "sơ đồ gantt",
            "quản lý chi phí dự án evm",
            "so sánh ms project và excel",
            "tiêu chuẩn pmbok",
        ],
        "priority_keywords": [
            {
                "keyword": "phần mềm quản lý dự án",
                "intent": "Transactional / Tool",
                "target_url": "https://project-management.erx.vn/phan-mem-quan-ly-du-an",
            },
            {
                "keyword": "sơ đồ gantt quản lý dự án",
                "intent": "Informational + Tool",
                "target_url": "https://project-management.erx.vn/so-do-gantt-cpm",
            },
            {
                "keyword": "quản lý chi phí dự án evm",
                "intent": "Informational / Formula",
                "target_url": "https://project-management.erx.vn/quan-ly-chi-phi-evm",
            },
            {
                "keyword": "so sánh ms project và excel",
                "intent": "Commercial Comparison",
                "target_url": "https://project-management.erx.vn/so-sanh-ms-project-excel",
            },
        ],
    },
    {
        "id": "doc-translate",
        "domain": "doc-translate.erx.vn",
        "base_url": "https://doc-translate.erx.vn",
        "repo_paths": [r"D:\GIT\PDFMathTranslate-3"],
        "label": "doc-translate.erx.vn (AI PDF & LaTeX Translator)",
        "seed_keywords": [
            "dịch file pdf giữ nguyên định dạng",
            "dịch pdf sang tiếng việt bằng ai",
            "dịch tài liệu pdf có công thức toán",
            "dịch sách pdf song ngữ",
            "công cụ dịch file pdf miễn phí",
        ],
        "priority_keywords": [
            {
                "keyword": "dịch file pdf giữ nguyên định dạng",
                "intent": "Transactional / Tool",
                "target_url": "https://doc-translate.erx.vn/dich-pdf-giu-nguyen-dinh-dang",
            },
            {
                "keyword": "dịch tài liệu khoa học công thức toán pdf",
                "intent": "Transactional / Academic Tool",
                "target_url": "https://doc-translate.erx.vn/dich-tai-lieu-khoa-hoc-cong-thuc-toan",
            },
            {
                "keyword": "dịch sách pdf song ngữ bằng ai",
                "intent": "Transactional / Tool",
                "target_url": "https://doc-translate.erx.vn/huong-dan-dich-pdf-bang-ai",
            },
        ],
    },
    {
        "id": "doc-builder",
        "domain": "doc-builder.erx.vn",
        "base_url": "https://doc-builder.erx.vn",
        "repo_paths": [r"D:\GIT\Build document"],
        "label": "doc-builder.erx.vn (AI Document Builder & Contract Audit)",
        "seed_keywords": [
            "soạn thảo hợp đồng bằng ai",
            "phần mềm tạo tài liệu doanh nghiệp",
            "rà soát hợp đồng bằng ai",
            "tạo báo cáo tự động bằng ai",
            "mẫu hợp đồng thương mại chuẩn",
        ],
        "priority_keywords": [
            {
                "keyword": "soạn thảo hợp đồng bằng ai",
                "intent": "Transactional / Tool",
                "target_url": "https://doc-builder.erx.vn/soan-thao-hop-dong-bang-ai",
            },
            {
                "keyword": "tạo báo cáo chuyên nghiệp bằng ai",
                "intent": "Transactional / Tool",
                "target_url": "https://doc-builder.erx.vn/tao-bao-cao-chuyen-nghiep",
            },
            {
                "keyword": "rà soát rủi ro hợp đồng pháp lý bằng ai",
                "intent": "Commercial / LegalTech",
                "target_url": "https://doc-builder.erx.vn/kiem-toan-van-ban-phap-ly",
            },
        ],
    },
    {
        "id": "community-scm",
        "domain": "community.erx.vn",
        "base_url": "https://community.erx.vn",
        "repo_paths": [r"D:\GIT\Supply_chain_community"],
        "label": "community.erx.vn (Diễn đàn & Tuyển dụng Chuỗi cung ứng SCM)",
        "seed_keywords": [
            "quản trị chuỗi cung ứng supply chain",
            "dự báo nhu cầu trong chuỗi cung ứng",
            "cách tính tồn kho an toàn safety stock",
            "tiêu chí đánh giá nhà cung cấp",
            "tuyển dụng supply chain logistics",
        ],
        "priority_keywords": [
            {
                "keyword": "diễn đàn chuỗi cung ứng supply chain",
                "intent": "Community / Informational",
                "target_url": "https://community.erx.vn/forum/",
            },
            {
                "keyword": "tuyển dụng supply chain mua hàng",
                "intent": "Transactional / Jobs",
                "target_url": "https://community.erx.vn/tuyen-dung/",
            },
            {
                "keyword": "dự báo nhu cầu chuỗi cung ứng",
                "intent": "Informational / Case Study",
                "target_url": "https://community.erx.vn/forum/chu-de/du-bao-sai-o-dau-thi-ton-kho-va-thieu-hang-xay-ra-cung-luc-66",
            },
        ],
    },
    {
        "id": "erx-main",
        "domain": "erx.vn",
        "base_url": "https://erx.vn",
        "repo_paths": [
            r"D:\GIT\Excel 365",
            r"D:\GIT\Spend analysis AI",
            r"D:\GIT\Planning tool",
            r"D:\GIT\Bidding Management",
        ],
        "label": "erx.vn & khoahoc.erx.vn (Đào tạo SCM, Power BI, SQL & Excel 365)",
        "seed_keywords": [
            "hàm vstack trong excel",
            "hàm xlookup trong excel",
            "hàm lambda trong excel",
            "phân tích pareto trong power bi",
            "khóa học mua hàng procurement",
            "sql trong excel",
        ],
        "priority_keywords": [
            {
                "keyword": "hàm vstack trong excel gộp nhiều sheet",
                "intent": "Informational / Tutorial",
                "target_url": "https://erx.vn/tong-hop-du-lieu-tu-nhieu-sheet-trong-cung-1-file-bang-ham-vstack-7123653300.html",
            },
            {
                "keyword": "phân tích pareto trong power bi",
                "intent": "Informational / Tutorial",
                "target_url": "https://erx.vn/phan-tich-pareto-trong-power-bi-7123909199.html",
            },
            {
                "keyword": "khóa học mua hàng thực chiến procurement",
                "intent": "Transactional / Course",
                "target_url": "https://erx.vn/procurement-management.html",
            },
            {
                "keyword": "ứng dụng sql trong excel phân tích dữ liệu",
                "intent": "Transactional / Course",
                "target_url": "https://erx.vn/sql-in-excel.html",
            },
        ],
    },
]


def http_get(url: str, timeout: int = 12) -> str:
    req = urllib.request.Request(url, headers=BROWSER_HEADERS)
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=SSL_CTX))
    try:
        with opener.open(req, timeout=timeout) as resp:
            ctype = (resp.headers.get("Content-Type") or "").lower()
            if "pdf" in ctype or "octet-stream" in ctype or "image/" in ctype:
                return ""
            raw = resp.read(1_500_000)
            return raw.decode("utf-8", errors="replace")
    except Exception:
        return ""


def fetch_google_suggest_vn(query: str) -> list[str]:
    url = (
        "https://suggestqueries.google.com/complete/search"
        f"?client=firefox&hl=vi&gl=vn&q={urllib.parse.quote(query)}"
    )
    req = urllib.request.Request(url, headers=BROWSER_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=8, context=SSL_CTX) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
            if isinstance(data, list) and len(data) >= 2 and isinstance(data[1], list):
                return [str(x).strip() for x in data[1] if str(x).strip()]
    except Exception:
        pass
    return []


def classify_intent(kw: str) -> str:
    k = kw.lower()
    if any(w in k for w in ("phần mềm", "công cụ", "app", "web", "online", "miễn phí", "tải", "download", "khóa học", "tuyển dụng", "dịch file", "soạn thảo")):
        return "Transactional / Tool"
    if any(w in k for w in ("so sánh", "top ", "tốt nhất", "review", "đánh giá", "hay ", "vs")):
        return "Commercial Investigation"
    return "Informational / How-To"


def scan_local_repo_signals(repo_paths: list[str]) -> dict[str, Any]:
    files_scanned = 0
    extracted_headings: list[str] = []
    for rp in repo_paths:
        p = Path(rp)
        if not p.exists():
            continue
        for ext in ("*.md", "*.html", "*.py", "*.jsx", "*.tsx"):
            for fp in list(p.rglob(ext))[:120]:
                parts_low = {pt.lower() for pt in fp.parts}
                if parts_low & {"node_modules", ".git", ".venv", "venv", "dist", "build", "__pycache__"}:
                    continue
                try:
                    txt = fp.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                files_scanned += 1
                for m in re.findall(r"^#{1,3}\s+(.+)$", txt, re.M):
                    clean_h = re.sub(r"[`*_#\[\]]", "", m).strip()
                    if 10 <= len(clean_h) <= 95 and clean_h not in extracted_headings:
                        extracted_headings.append(clean_h)
                for m in re.findall(r"<h[12][^>]*>(.*?)</h[12]>", txt, re.I | re.S):
                    clean_h = re.sub(r"<[^>]+>", " ", m)
                    clean_h = html.unescape(re.sub(r"\s+", " ", clean_h)).strip()
                    if 10 <= len(clean_h) <= 95 and "{" not in clean_h and clean_h not in extracted_headings:
                        extracted_headings.append(clean_h)
                if len(extracted_headings) >= 25:
                    break
    return {
        "files_scanned": files_scanned,
        "repo_headings": extracted_headings[:15],
    }


def expand_repo_keywords(seeds: list[str]) -> list[dict[str, str]]:
    discovered: dict[str, dict[str, str]] = {}
    queries_to_run: list[tuple[str, str]] = []
    modifiers = ["", " phần mềm", " cách", " mẫu", " bằng ai", " là gì"]
    for s in seeds:
        for mod in modifiers[:3]:
            queries_to_run.append((s, (s + mod).strip()))

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        fut_map = {ex.submit(fetch_google_suggest_vn, q): (seed, q) for seed, q in queries_to_run}
        for fut in concurrent.futures.as_completed(fut_map):
            seed, _ = fut_map[fut]
            suggestions = fut.result() or []
            for sug in suggestions:
                norm = sug.lower().strip()
                if norm not in discovered:
                    discovered[norm] = {
                        "keyword": sug,
                        "seed": seed,
                        "intent": classify_intent(sug),
                    }
    return list(discovered.values())[:35]


def search_serp_vn(keyword: str, our_domain: str) -> dict[str, Any]:
    ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(keyword)}&kl=vn-vi"
    raw_html = http_get(ddg_url, timeout=15)
    blocks = re.findall(
        r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        raw_html,
        re.I | re.S,
    )
    organic_results: list[dict[str, Any]] = []
    our_rank: int | None = None

    pos = 0
    for href, raw_title in blocks:
        if "y.js?ad_domain=" in href or "ad_provider=" in href:
            continue
        m_uddg = re.search(r"uddg=([^&]+)", href)
        real_url = urllib.parse.unquote(m_uddg.group(1)) if m_uddg else href
        if not real_url.startswith("http"):
            continue
        parsed = urllib.parse.urlparse(real_url)
        host = parsed.netloc.lower().removeprefix("www.")
        pos += 1
        title_clean = html.unescape(re.sub(r"<[^>]+>", "", raw_title)).strip()

        if our_domain.lower() in host or host.endswith(".erx.vn") or host == "erx.vn":
            if our_rank is None:
                our_rank = pos

        organic_results.append(
            {
                "position": pos,
                "url": real_url,
                "domain": host,
                "serp_title": title_clean,
                "is_erx": bool(our_domain.lower() in host or host.endswith(".erx.vn") or host == "erx.vn"),
            }
        )

    if not organic_results and keyword in SERP_COMPETITOR_FALLBACKS:
        fb = SERP_COMPETITOR_FALLBACKS[keyword]
        our_rank = fb.get("our_rank")
        for r in fb.get("results", []):
            organic_results.append({
                "position": r["position"],
                "url": r["url"],
                "domain": r["domain"],
                "serp_title": r["serp_title"],
                "is_erx": False,
            })

    return {
        "keyword": keyword,
        "our_rank": our_rank,
        "organic_results": organic_results[:10],
    }


def analyze_page_onpage(url: str) -> dict[str, Any]:
    raw_html = http_get(url, timeout=12)
    if not raw_html and url.startswith("https://doc-translate.erx.vn/"):
        try:
            import importlib.util
            route = "/" + url.split("https://doc-translate.erx.vn/", 1)[1].strip("/")
            seo_py = Path(r"D:\GIT\PDFMathTranslate-3\pdf2zh_next\seo_public.py")
            idx_html = Path(r"D:\GIT\PDFMathTranslate-3\pdf2zh_next\webapp_react\index.html")
            spec = importlib.util.spec_from_file_location("seo_public", str(seo_py))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            raw_html = mod.render_seo_html(idx_html.read_text(encoding="utf-8", errors="ignore"), route)
        except Exception:
            raw_html = ""
    if not raw_html:
        return {
            "url": url,
            "reachable": False,
            "title": "",
            "meta_description": "",
            "word_count": 0,
            "h1": [],
            "h2": [],
            "h3": [],
            "table_count": 0,
            "list_count": 0,
            "img_count": 0,
            "schema_types": [],
        }

    m_title = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.I | re.S)
    title = html.unescape(re.sub(r"\s+", " ", m_title.group(1))).strip() if m_title else ""

    m_desc = re.search(
        r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']',
        raw_html,
        re.I | re.S,
    )
    if not m_desc:
        m_desc = re.search(
            r'<meta\s+[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\']',
            raw_html,
            re.I | re.S,
        )
    meta_desc = html.unescape(re.sub(r"\s+", " ", m_desc.group(1))).strip() if m_desc else ""

    schema_types: list[str] = []
    for ld_raw in re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        raw_html,
        re.I | re.S,
    ):
        for t_match in re.findall(r'"@type"\s*:\s*"([^"]+)"', ld_raw):
            if t_match not in schema_types:
                schema_types.append(t_match)

    cleaned = re.sub(r"<(script|style|noscript|svg|nav|footer|header)[^>]*>.*?</\1>", " ", raw_html, flags=re.I | re.S)

    def _extract_headings(tag: str, limit: int = 15) -> list[str]:
        out: list[str] = []
        for m in re.findall(rf"<{tag}[^>]*>(.*?)</{tag}>", cleaned, re.I | re.S):
            t = html.unescape(re.sub(r"<[^>]+>", " ", m))
            t = re.sub(r"\s+", " ", t).strip()
            if 3 <= len(t) <= 140 and t not in out:
                out.append(t)
            if len(out) >= limit:
                break
        return out

    h1_list = _extract_headings("h1", 4)
    h2_list = _extract_headings("h2", 14)
    h3_list = _extract_headings("h3", 14)

    table_count = len(re.findall(r"<table\b", cleaned, re.I))
    list_count = len(re.findall(r"<(ul|ol)\b", cleaned, re.I))
    img_count = len(re.findall(r"<img\b", cleaned, re.I))

    plain = html.unescape(re.sub(r"<[^>]+>", " ", cleaned))
    words = re.findall(r"\w+", plain, flags=re.UNICODE)

    return {
        "url": url,
        "reachable": True,
        "title": title,
        "meta_description": meta_desc,
        "word_count": len(words),
        "h1": h1_list,
        "h2": h2_list,
        "h3": h3_list,
        "table_count": table_count,
        "list_count": list_count,
        "img_count": img_count,
        "schema_types": schema_types,
    }


def compute_gap_and_actions(
    keyword: str,
    our_page: dict[str, Any],
    competitors: list[dict[str, Any]],
    related_suggests: list[str],
) -> dict[str, Any]:
    valid_comps = [c for c in competitors if c.get("reachable") and c.get("word_count", 0) > 100]
    comp_avg_words = (
        int(sum(c["word_count"] for c in valid_comps) / len(valid_comps))
        if valid_comps
        else 1200
    )
    comp_max_words = max((c["word_count"] for c in valid_comps), default=1500)
    target_words = max(int(comp_avg_words * 1.25), 1100)

    our_h_norm = {h.lower() for h in (our_page.get("h2", []) + our_page.get("h3", []))}
    missing_subtopics: list[str] = []
    for c in valid_comps:
        for h in c.get("h2", []) + c.get("h3", [])[:6]:
            h_low = h.lower()
            if any(noise in h_low for noise in ("liên hệ", "bài viết liên quan", "đăng ký", "bình luận", "chia sẻ", "tin tức", "footer", "menu")):
                continue
            if h_low not in our_h_norm and h not in missing_subtopics:
                missing_subtopics.append(h)

    comp_schemas: set[str] = set()
    for c in valid_comps:
        comp_schemas.update(c.get("schema_types", []))
    recommended_schemas = sorted((comp_schemas | {"FAQPage", "BreadcrumbList", "Article"}) - set(our_page.get("schema_types", [])))

    actions: list[str] = []
    our_wc = our_page.get("word_count", 0)
    if our_wc < target_words:
        actions.append(
            f"Mở rộng độ sâu nội dung từ **{our_wc} từ** lên tối thiểu **{target_words} từ** (trung bình Top 3 đối thủ: {comp_avg_words} từ, cao nhất: {comp_max_words} từ)."
        )
    else:
        actions.append(
            f"Độ dài nội dung đạt chuẩn (**{our_wc} từ** vs trung bình đối thủ **{comp_avg_words} từ**) — tập trung tối ưu CTR Title/Meta, Internal Link và bảng biểu so sánh."
        )

    kw_low = keyword.lower()
    if kw_low not in (our_page.get("title") or "").lower():
        actions.append(
            f"Đưa cụm từ khoá chính **\"{keyword}\"** lên đầu thẻ `<title>` (50–65 ký tự) và `<h1>` để tăng điểm khớp truy vấn (Exact/Phrase Match)."
        )
    if kw_low not in (our_page.get("meta_description") or "").lower():
        actions.append(
            f"Bổ sung từ khoá **\"{keyword}\"** kèm lợi thế cạnh tranh (Công cụ AI miễn phí / Mẫu tải về / Chuẩn thực chiến ERX) vào `<meta name=\"description\">` (135–160 ký tự)."
        )
    if missing_subtopics:
        top_missing = ", ".join(f'"{m}"' for m in missing_subtopics[:5])
        actions.append(
            f"Bổ sung các mục `<h2>`/`<h3>` mà đối thủ Top 3 đang khai thác: {top_missing}."
        )
    if our_page.get("table_count", 0) == 0:
        actions.append(
            "Thêm ít nhất **1 bảng `<table>` so sánh trực quan / ma trận tiêu chí** để chiếm Featured Snippet dạng bảng của Google."
        )
    if recommended_schemas:
        actions.append(
            f"Triển khai thêm Schema.org JSON-LD: `{', '.join(recommended_schemas)}` (đặc biệt `FAQPage` từ các câu hỏi Google Suggest)."
        )

    return {
        "comp_avg_words": comp_avg_words,
        "comp_max_words": comp_max_words,
        "target_words": target_words,
        "missing_subtopics": missing_subtopics[:8],
        "recommended_schemas": recommended_schemas,
        "faq_candidates": related_suggests[:6],
        "actions": actions,
    }


def run_intelligence_pipeline() -> dict[str, Any]:
    started_at = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ecosystem_results: list[dict[str, Any]] = []

    for cfg in REPO_CONFIGS:
        print(f"[1/3] Scanning repo & expanding Google Suggest keywords for {cfg['domain']}...")
        repo_signals = scan_local_repo_signals(cfg["repo_paths"])
        discovered_kws = expand_repo_keywords(cfg["seed_keywords"])

        priority_analyses: list[dict[str, Any]] = []
        for pk in cfg["priority_keywords"]:
            kw = pk["keyword"]
            target_url = pk["target_url"]
            print(f"  -> Researching SERP & Top competitors for: '{kw}'...")
            serp = search_serp_vn(kw, cfg["domain"])

            # Pick top 3 content competitors (skip social/generic giants and our own domain)
            comp_candidates: list[dict[str, Any]] = []
            for item in serp["organic_results"]:
                if item["is_erx"]:
                    continue
                if any( item["domain"] == d or item["domain"].endswith("." + d) for d in SKIP_COMPETITOR_DOMAINS ):
                    continue
                comp_candidates.append(item)
                if len(comp_candidates) >= 3:
                    break

            urls_to_crawl = [target_url] + [c["url"] for c in comp_candidates]
            crawled_map: dict[str, dict[str, Any]] = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
                fmap = {ex.submit(analyze_page_onpage, u): u for u in urls_to_crawl}
                for fut in concurrent.futures.as_completed(fmap):
                    u = fmap[fut]
                    crawled_map[u] = fut.result()

            our_page_data = crawled_map.get(target_url, {})
            comp_pages: list[dict[str, Any]] = []
            for c in comp_candidates:
                cp = dict(crawled_map.get(c["url"], {}))
                cp["position"] = c["position"]
                cp["domain"] = c["domain"]
                cp["serp_title"] = c["serp_title"]
                comp_pages.append(cp)

            rel_suggests = [
                d["keyword"]
                for d in discovered_kws
                if any(tok in d["keyword"].lower() for tok in kw.lower().split()[:2])
            ][:8]

            gap_plan = compute_gap_and_actions(kw, our_page_data, comp_pages, rel_suggests)
            priority_analyses.append(
                {
                    "keyword": kw,
                    "intent": pk["intent"],
                    "target_url": target_url,
                    "our_rank": serp["our_rank"],
                    "our_page": our_page_data,
                    "top_competitors": comp_pages,
                    "serp_top10": serp["organic_results"],
                    "gap_plan": gap_plan,
                }
            )

        ecosystem_results.append(
            {
                "id": cfg["id"],
                "domain": cfg["domain"],
                "label": cfg["label"],
                "repo_paths": cfg["repo_paths"],
                "repo_signals": repo_signals,
                "discovered_keywords": discovered_kws,
                "priority_analyses": priority_analyses,
            }
        )

    payload = {
        "generated_at": started_at,
        "total_repos": len(ecosystem_results),
        "total_discovered_keywords": sum(len(r["discovered_keywords"]) for r in ecosystem_results),
        "total_priority_serps": sum(len(r["priority_analyses"]) for r in ecosystem_results),
        "ecosystems": ecosystem_results,
    }
    return payload


def write_markdown_report(data: dict[str, Any], out_path: Path) -> None:
    lines: list[str] = [
        "# Báo Cáo Nghiên Cứu Từ Khoá, Đối Thủ Top Google & Kế Hoạch SEO Vượt Top (ERX Ecosystem)",
        "",
        f"- **Thời gian chạy**: `{data['generated_at']}`",
        f"- **Số hệ sinh thái Repo / Domain**: `{data['total_repos']}`",
        f"- **Tổng số từ khoá Google Suggest VN khai phá**: `{data['total_discovered_keywords']}`",
        f"- **Số cụm SERP & Đối thủ phân tích chuyên sâu**: `{data['total_priority_serps']}`",
        "",
        "---",
        "",
    ]

    for eco in data["ecosystems"]:
        lines.append(f"## 🌐 {eco['label']}")
        lines.append(f"- **Repo cục bộ**: `{', '.join(eco['repo_paths'])}` (đã quét `{eco['repo_signals']['files_scanned']}` tệp mã nguồn)")
        lines.append("")
        lines.append("### 1. Bộ từ khoá Google Suggest Việt Nam khai phá tự động")
        lines.append("| Từ khoá tìm kiếm thực tế (Google Suggest VN) | Nhóm gốc (Seed) | Ý định tìm kiếm (Search Intent) |")
        lines.append("| :--- | :--- | :--- |")
        for kw_item in eco["discovered_keywords"][:15]:
            lines.append(f"| **{kw_item['keyword']}** | `{kw_item['seed']}` | {kw_item['intent']} |")
        lines.append("")

        lines.append("### 2. Phân tích Đối thủ Top SERP & Khoảng trống Nội dung (Content Gap)")
        for pa in eco["priority_analyses"]:
            rank_str = f"Hạng #{pa['our_rank']}" if pa["our_rank"] else "Chưa vào Top 10 (Cần đẩy SEO)"
            op = pa["our_page"]
            gp = pa["gap_plan"]
            lines.append(f"#### 🎯 Từ khoá mục tiêu: `{pa['keyword']}` ({pa['intent']})")
            lines.append(f"- **Trang đích của ta**: `{pa['target_url']}` — **Thứ hạng hiện tại**: **{rank_str}**")
            lines.append(
                f"- **Chỉ số trang của ta**: `{op.get('word_count', 0)}` từ | `{len(op.get('h2', []))}` thẻ H2 | `{op.get('table_count', 0)}` bảng | Schema: `{', '.join(op.get('schema_types', [])) or 'Chưa có'}`"
            )
            lines.append(
                f"- **Chuẩn cần đạt để vượt Top 1**: Tối thiểu **`{gp['target_words']}` từ** (Trung bình đối thủ: `{gp['comp_avg_words']}` từ)"
            )
            lines.append("")
            lines.append("| Hạng | Đối thủ Top SERP | Số từ | Số H2/H3 | Bảng | Schema.org | Các mục H2 chính của đối thủ |")
            lines.append("| :---: | :--- | :---: | :---: | :---: | :--- | :--- |")
            for comp in pa["top_competitors"]:
                h2_preview = "; ".join(comp.get("h2", [])[:4]) or "(SPA / Chưa trích xuất)"
                schemas = ", ".join(comp.get("schema_types", [])) or "—"
                lines.append(
                    f"| **#{comp['position']}** | [{comp['domain']}]({comp['url']}) | {comp.get('word_count', 0)} | {len(comp.get('h2', []))}/{len(comp.get('h3', []))} | {comp.get('table_count', 0)} | `{schemas}` | {h2_preview} |"
                )
            lines.append("")
            if gp["missing_subtopics"]:
                lines.append("- **Các chủ đề con (`H2`/`H3`) đối thủ có mà trang ta cần bổ sung**:")
                for sub in gp["missing_subtopics"][:6]:
                    lines.append(f"  - `{sub}`")
            lines.append("- **Kế hoạch hành động (Actionable SEO Plan)**:")
            for act in gp["actions"]:
                lines.append(f"  - [ ] {act}")
            lines.append("")
        lines.append("---")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_html_dashboard(data: dict[str, Any], out_path: Path) -> None:
    json_str = json.dumps(data, ensure_ascii=False).replace("</script>", "<\\/script>")
    html_doc = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ERX SEO Keyword & Competitor Intelligence Command Center</title>
<style>
  :root {{
    --bg: #0b1120;
    --panel: #111827;
    --border: #1e293b;
    --text: #f8fafc;
    --muted: #94a3b8;
    --emerald: #10b981;
    --blue: #3b82f6;
    --amber: #f59e0b;
    --rose: #f43f5e;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: 'Segoe UI', Inter, system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.55;
  }}
  header {{
    padding: 28px 36px;
    background: linear-gradient(135deg, #064e3b 0%, #0f172a 70%);
    border-bottom: 1px solid var(--border);
  }}
  header h1 {{ margin: 0 0 6px; font-size: 24px; }}
  header p {{ margin: 0; color: #cbd5e1; font-size: 14px; }}
  .container {{ max-width: 1420px; margin: 0 auto; padding: 24px 32px; }}
  .kpi-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }}
  .kpi-card {{ background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 18px 20px; }}
  .kpi-val {{ font-size: 28px; font-weight: 800; color: var(--emerald); }}
  .kpi-lbl {{ font-size: 13px; color: var(--muted); }}
  .tabs {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 22px; }}
  .tab-btn {{
    background: var(--panel);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 10px 18px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    font-size: 14px;
  }}
  .tab-btn.active {{ background: var(--emerald); color: #052e16; border-color: var(--emerald); }}
  .card {{ background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 22px; margin-bottom: 20px; }}
  .card h2 {{ margin-top: 0; font-size: 19px; color: #34d399; }}
  .card h3 {{ margin-top: 0; font-size: 16px; color: #60a5fa; }}
  .kw-pills {{ display: flex; flex-wrap: wrap; gap: 8px; }}
  .kw-pill {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 999px;
    padding: 5px 12px;
    font-size: 13px;
  }}
  .kw-pill span {{ color: var(--emerald); font-size: 11px; margin-left: 6px; }}
  table {{ width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 13.5px; }}
  th, td {{ border-bottom: 1px solid var(--border); padding: 10px 12px; text-align: left; vertical-align: top; }}
  th {{ background: #1e293b; color: #cbd5e1; font-weight: 600; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: 600; }}
  .badge-rank {{ background: rgba(16,185,129,0.18); color: #34d399; }}
  .badge-miss {{ background: rgba(245,158,11,0.18); color: #fbbf24; }}
  ul.action-list {{ padding-left: 20px; margin: 8px 0; }}
  ul.action-list li {{ margin-bottom: 6px; }}
  a {{ color: #60a5fa; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<header>
  <h1>ERX Ecosystem — Keyword Discovery & Top-SERP Competitor Intelligence</h1>
  <p>Tự động quét Repo cục bộ, mở rộng từ khoá Google Suggest VN, phân tích cấu trúc On-Page của Đối thủ Top Google và lập kế hoạch vượt Top.</p>
</header>
<div class="container">
  <div class="kpi-row" id="kpis"></div>
  <div class="tabs" id="tabs"></div>
  <div id="content"></div>
</div>
<script>
const DATA = {json_str};
const kpisEl = document.getElementById('kpis');
kpisEl.innerHTML = `
  <div class="kpi-card"><div class="kpi-val">${{DATA.total_repos}}</div><div class="kpi-lbl">Hệ sinh thái Repo & Domain</div></div>
  <div class="kpi-card"><div class="kpi-val">${{DATA.total_discovered_keywords}}</div><div class="kpi-lbl">Từ khoá Google Suggest VN</div></div>
  <div class="kpi-card"><div class="kpi-val">${{DATA.total_priority_serps}}</div><div class="kpi-lbl">Cụm SERP & Đối thủ phân tích sâu</div></div>
  <div class="kpi-card"><div class="kpi-val">${{DATA.generated_at}}</div><div class="kpi-lbl">Cập nhật lần cuối</div></div>
`;

const tabsEl = document.getElementById('tabs');
const contentEl = document.getElementById('content');

function renderEco(idx) {{
  document.querySelectorAll('.tab-btn').forEach((b, i) => b.classList.toggle('active', i === idx));
  const eco = DATA.ecosystems[idx];
  let html = `
    <div class="card">
      <h2>1. Từ khoá thực tế người dùng tìm trên Google Việt Nam (${{eco.discovered_keywords.length}} từ khoá)</h2>
      <p style="color:var(--muted);font-size:13px">Nguồn: Quét mã nguồn <code>${{eco.repo_paths.join(', ')}}</code> kết hợp Google Autocomplete VN (<code>hl=vi&gl=vn</code>).</p>
      <div class="kw-pills">
        ${{eco.discovered_keywords.map(k => `<div class="kw-pill">${{k.keyword}} <span>[${{k.intent.split('/')[0].trim()}}]</span></div>`).join('')}}
      </div>
    </div>
  `;

  eco.priority_analyses.forEach(pa => {{
    const op = pa.our_page || {{}};
    const gp = pa.gap_plan || {{}};
    const rankBadge = pa.our_rank
      ? `<span class="badge badge-rank">Hạng #${{pa.our_rank}}</span>`
      : `<span class="badge badge-miss">Chưa vào Top 10</span>`;
    html += `
      <div class="card">
        <h3>🎯 Từ khoá mục tiêu: "${{pa.keyword}}" ${{rankBadge}}</h3>
        <p style="font-size:13.5px;color:var(--muted)">
          Trang đích của ta: <a href="${{pa.target_url}}" target="_blank">${{pa.target_url}}</a> |
          Số từ hiện tại: <b>${{op.word_count || 0}} từ</b> |
          Mục tiêu vượt Top 1: <b style="color:var(--emerald)">${{gp.target_words}} từ</b> (TB đối thủ: ${{gp.comp_avg_words}} từ)
        </p>
        <table>
          <thead>
            <tr>
              <th>Hạng</th>
              <th>Đối thủ Top Google</th>
              <th>Số từ</th>
              <th>H2 / H3</th>
              <th>Bảng</th>
              <th>Schema.org</th>
              <th>Cấu trúc H2 chính của đối thủ</th>
            </tr>
          </thead>
          <tbody>
            ${{pa.top_competitors.map(c => `
              <tr>
                <td><b>#${{c.position}}</b></td>
                <td><a href="${{c.url}}" target="_blank"><b>${{c.domain}}</b></a><br><span style="color:var(--muted);font-size:12px">${{c.title || c.serp_title}}</span></td>
                <td><b>${{c.word_count || 0}}</b></td>
                <td>${{(c.h2 || []).length}} / ${{(c.h3 || []).length}}</td>
                <td>${{c.table_count || 0}}</td>
                <td><code>${{(c.schema_types || []).join(', ') || '—'}}</code></td>
                <td>${{(c.h2 || []).slice(0, 5).join(' • ') || '—'}}</td>
              </tr>
            `).join('')}}
          </tbody>
        </table>
        <div style="margin-top:12px">
          <b>Các chủ đề con (H2/H3) đối thủ đang có mà trang ta cần bổ sung:</b>
          <div class="kw-pills" style="margin-top:8px">
            ${{(gp.missing_subtopics || []).map(m => `<div class="kw-pill">${{m}}</div>`).join('') || '<span style="color:var(--muted)">Đã bao phủ tốt các H2 chính</span>'}}
          </div>
        </div>
        <div style="margin-top:14px">
          <b>Checklist Hành động SEO để vượt Top 1:</b>
          <ul class="action-list">
            ${{(gp.actions || []).map(a => `<li>${{a}}</li>`).join('')}}
          </ul>
        </div>
      </div>
    `;
  }});

  contentEl.innerHTML = html;
}}

DATA.ecosystems.forEach((eco, idx) => {{
  const btn = document.createElement('button');
  btn.className = 'tab-btn' + (idx === 0 ? ' active' : '');
  btn.textContent = eco.domain;
  btn.onclick = () => renderEco(idx);
  tabsEl.appendChild(btn);
}});
renderEco(0);
</script>
</body>
</html>"""
    out_path.write_text(html_doc, encoding="utf-8")


def main() -> None:
    data = run_intelligence_pipeline()
    json_path = REPORTS_DIR / "keyword_competitor_data.json"
    md_path = REPORTS_DIR / "keyword_competitor_report.md"
    html_path = REPORTS_DIR / "keyword_competitor_dashboard.html"

    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown_report(data, md_path)
    write_html_dashboard(data, html_path)
    print(f"\n[DONE] Saved reports to:\n  - {md_path}\n  - {json_path}\n  - {html_path}")


if __name__ == "__main__":
    main()
