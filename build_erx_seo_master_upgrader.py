# -*- coding: utf-8 -*-
"""
Builds:
1. D:\\GIT\\SEO Tool\\pm_assets\\sitemap-erx-master.txt
   Complete, canonical 161-URL sitemap for https://erx.vn/ (Homepage + 21 Category/Menu Hubs + 119 Blog Articles 712* + 20 Workshop Pages 831*).
2. D:\\GIT\\SEO Tool\\pm_assets\\erx_seo_master_upgrader.js
   Comprehensive SEO upgrader for https://erx.vn/administrator:
   - Updates MENU.META_TITLE, MENU.META_DESC, MENU.META_KEY across all Category/Menu pages (skipping Menu 578 'Trang chủ' to preserve '/' routing, and standardizing Menu 1477 title to 'Mẫu file quản lý Excel').
   - Updates TITLE, META_TITLE, META_DESC, and META_KEY for all 42 short-title blog articles (<45 chars) and 7 short/generic meta-description blog articles.
   - Updates Workshop items (831*) in backend + injects synchronous <head> SEO Meta, Canonical, OpenGraph, and valid PascalCase Schema.org JSON-LD (Organization, WebSite, BreadcrumbList, TechArticle, EducationEvent, FAQPage) in META.SCRIPT_HEADER, followed by restoring SYS.MENU_DEFAULT=578 & SYS.MENU_HOME=578.
"""
import json
from pathlib import Path

OUT_DIR = Path(r"D:\GIT\SEO Tool\pm_assets")
LIVE_ARTICLES_JSON = OUT_DIR / "live_119_articles_seo.json"
OUT_SITEMAP = OUT_DIR / "sitemap-erx-master.txt"
OUT_JS = OUT_DIR / "erx_seo_master_upgrader.js"

with open(LIVE_ARTICLES_JSON, "r", encoding="utf-8") as f:
    live_data = json.load(f)

article_urls = [x["url"] for x in live_data["valid"]]

# 1. Canonical Category & Menu Hub SEO Metadata Map (keyed by URL path / alias)
MENU_SEO_MAP = {
    "kien-thuc": {
        "meta_title": "Chia sẻ kiến thức Excel, Power BI, Python & Chuỗi cung ứng | ERX",
        "meta_desc": "Kho tàng bài viết chuyên sâu về Excel 365, VBA, SQL, Power BI DAX, Python, Quản trị Dự án PMBOK 8 và Quản lý Chuỗi cung ứng (Supply Chain) thực chiến tại ERX.",
        "meta_key": "chia sẻ kiến thức erx, học excel nâng cao, power bi dax, quản lý chuỗi cung ứng, supply chain management, project management pmbok 8"
    },
    "hoi-thao": {
        "meta_title": "Hội thảo thực chiến Excel 365, Power BI & Chuỗi cung ứng | ERX",
        "meta_desc": "Chuỗi hội thảo trực tuyến (Workshop Online) miễn phí hàng tuần của ERX Việt Nam: Giải bài toán thực chiến về Excel 365, Power Query, Power BI và Supply Chain.",
        "meta_key": "hội thảo excel, workshop power bi, hội thảo chuỗi cung ứng, sự kiện erx việt nam, đào tạo phân tích dữ liệu"
    },
    "dao-tao-doanh-nghiep": {
        "meta_title": "Đào tạo doanh nghiệp (In-house Training) Data & Supply Chain | ERX",
        "meta_desc": "Chương trình đào tạo doanh nghiệp (Corporate In-house Training) thiết kế riêng theo bài toán thực tế về Phân tích dữ liệu (Excel, Power BI, SQL, Python) & Chuỗi cung ứng.",
        "meta_key": "đào tạo doanh nghiệp, inhouse training excel power bi, đào tạo chuỗi cung ứng cho doanh nghiệp, tư vấn đào tạo erx"
    },
    "phan-mem": {
        "meta_title": "Phần mềm & Công cụ tối ưu hóa Chuỗi cung ứng, Quản trị dự án | ERX",
        "meta_desc": "Hệ sinh thái phần mềm và Add-in thực chiến từ ERX Việt Nam: ERX Smart Tool, AI Project Gantt Planner (PMBOK 8), công cụ tối ưu hóa tuyến đường vận tải và kho vận.",
        "meta_key": "phần mềm chuỗi cung ứng, addin excel erx smart tool, phần mềm quản lý dự án pmbok 8, tối ưu hóa tuyến đường"
    },
    "tuyen-dung": {
        "meta_title": "Hợp tác Giảng viên & Tuyển dụng Nhân sự Chuỗi cung ứng | ERX",
        "meta_desc": "Cơ hội hợp tác trở thành Giảng viên chuyên gia tại ERX Việt Nam và thông tin tuyển dụng các vị trí Quản lý Chuỗi cung ứng, Mua hàng (Procurement), Logistics uy tín.",
        "meta_key": "hợp tác việc làm erx, tuyển dụng supply chain, tuyển dụng mua hàng logistics, tuyển giảng viên phân tích dữ liệu"
    },
    "lien-he": {
        "meta_title": "Liên hệ tư vấn Khóa học & Giải pháp Đào tạo Doanh nghiệp | ERX",
        "meta_desc": "Liên hệ Trung tâm Đào tạo Thực chiến ERX Việt Nam (Hotline/Zalo: 0879.490.845 - Email: info@erx.vn) để được tư vấn lộ trình học Phân tích dữ liệu & Chuỗi cung ứng.",
        "meta_key": "liên hệ erx việt nam, trung tâm đào tạo erx, tư vấn khóa học supply chain data analysis"
    },
    "gioi-thieu": {
        "meta_title": "Giới thiệu về ERX Việt Nam - Đào tạo Phân tích Dữ liệu & SCM",
        "meta_desc": "ERX Việt Nam là trung tâm đào tạo thực chiến hàng đầu về Phân tích dữ liệu (Excel, SQL, VBA, Power BI, Python) và Quản trị Chuỗi cung ứng (Supply Chain Management).",
        "meta_key": "giới thiệu erx việt nam, về erx, trung tâm đào tạo phân tích dữ liệu và chuỗi cung ứng"
    },
    "mau-file-quan-ly-excel": {
        "new_nav_title": "Mẫu file quản lý Excel",
        "meta_title": "Mẫu file quản lý Excel miễn phí cho Kho vận, Mua hàng & Dự án | ERX",
        "meta_desc": "Tải miễn phí bộ sưu tập mẫu file quản lý bằng Excel chuyên nghiệp: Quản lý tồn kho, kế hoạch mua hàng, lịch thanh toán, nhân sự và tự động hóa báo cáo doanh nghiệp.",
        "meta_key": "mẫu file quản lý excel, file excel quản lý kho, mẫu báo cáo excel đẹp, tải file excel miễn phí erx"
    },
    "excel": {
        "meta_title": "Kiến thức Microsoft Excel thực chiến từ Cơ bản đến Chuyên sâu | ERX",
        "meta_desc": "Tổng hợp kiến thức Microsoft Excel toàn diện: Hệ thống hàm Excel 365 mảng động, lập trình tự động hóa VBA, truy vấn SQL trong Excel và thiết kế Dashboard quản trị.",
        "meta_key": "học excel thực chiến, thủ thuật excel nâng cao, excel cho chuỗi cung ứng, đào tạo excel erx"
    },
    "excel-functions": {
        "meta_title": "Tra cứu các Hàm Excel thông dụng & Nâng cao kèm Ví dụ thực tế | ERX",
        "meta_desc": "Cẩm nang tra cứu cú pháp và bài tập thực hành các hàm trong Excel (VLOOKUP, INDEX MATCH, SUMIFS, COUNTIFS, SUBTOTAL, XLOOKUP, FILTER, LAMBDA) dễ hiểu nhất.",
        "meta_key": "các hàm trong excel, excel functions, hàm lọc dữ liệu excel, hàm tìm kiếm trong excel, công thức excel nâng cao"
    },
    "excel-function": {
        "meta_title": "Tổng hợp Hàm Excel thực chiến trong Phân tích Dữ liệu | ERX Việt Nam",
        "meta_desc": "Hướng dẫn chi tiết cách kết hợp các hàm tính toán, dò tìm và xử lý chuỗi văn bản trong Microsoft Excel phục vụ lập báo cáo quản trị và vận hành doanh nghiệp.",
        "meta_key": "hàm excel thực chiến, công thức excel văn phòng, hướng dẫn hàm excel erx"
    },
    "cac-ham-excel-365": {
        "meta_title": "Các hàm Excel 365 mới nhất: FILTER, XLOOKUP, LAMBDA, VSTACK | ERX",
        "meta_desc": "Làm chủ trọn bộ các hàm mảng động (Dynamic Array Functions) mới nhất trên Microsoft Excel 365: FILTER, TOCOL, TOROW, VSTACK, HSTACK, TEXTSPLIT, CHOOSECOLS và LAMBDA.",
        "meta_key": "các hàm excel 365, hàm mảng động excel, hàm filter trong excel, hàm lambda excel 365, hàm vstack textsplit"
    },
    "excel-365": {
        "meta_title": "Hướng dẫn các Hàm Mảng Động trên Microsoft Excel 365 | ERX Việt Nam",
        "meta_desc": "Khám phá sức mạnh đột phá của các hàm mảng động trong phiên bản Microsoft Excel 365 giúp tự động hóa hoàn toàn bảng tính mà không cần viết code phức tạp.",
        "meta_key": "excel 365 nâng cao, hàm mới trong office 365, tự động hóa báo cáo excel 365"
    },
    "excel-vba": {
        "meta_title": "Lập trình Excel VBA thực chiến: Tự động hóa Báo cáo chỉ 1 Click | ERX",
        "meta_desc": "Hướng dẫn lập trình VBA trong Excel từ cơ bản đến nâng cao: Thao tác đối tượng Workbook/Range, viết hàm UDF, kết nối ADODB SQL và tự động hóa báo cáo doanh nghiệp.",
        "meta_key": "lập trình excel vba, tự động hóa báo cáo bằng vba, học vba excel cho người mới, code vba excel thực chiến"
    },
    "sql": {
        "meta_title": "SQL trong Excel: Truy vấn & Tổng hợp Dữ liệu lớn Siêu tốc | ERX",
        "meta_desc": "Phương pháp sử dụng ngôn ngữ truy vấn SQL (SELECT, JOIN, GROUP BY, UNION, PIVOT) ngay trong Microsoft Excel qua ADODB giúp tổng hợp hàng trăm nghìn dòng trong 1 giây.",
        "meta_key": "sql trong excel, sql in excel, adodb connection excel vba, truy vấn sql trên file excel, gộp dữ liệu nhiều file excel"
    },
    "dashboard-automated-report": {
        "meta_title": "Thiết kế Dashboard & Báo cáo Tự động (Automated Report) trên Excel",
        "meta_desc": "Hướng dẫn kỹ thuật vẽ biểu đồ động (Dynamic Chart), Highlight Top N, nhãn dữ liệu thông minh và thiết kế hệ thống Dashboard báo cáo quản trị tự động trên Excel.",
        "meta_key": "thiết kế dashboard excel, báo cáo tự động trong excel, vẽ biểu đồ động excel, automated report erx"
    },
    "power-bi": {
        "meta_title": "Tài liệu học Power BI & Ngôn ngữ DAX thực chiến từ A-Z | ERX Việt Nam",
        "meta_desc": "Chuyên mục hướng dẫn Microsoft Power BI chuyên sâu: Xây dựng Data Model chuẩn Star Schema, viết hàm DAX nâng cao (CALCULATE, ALL, ALLSELECTED), Pareto và Dashboard.",
        "meta_key": "học power bi, hàm dax trong power bi, phân tích dữ liệu power bi, thiết kế dashboard power bi, data modeling"
    },
    "supply-chain-management": {
        "meta_title": "Quản trị Chuỗi cung ứng (Supply Chain Management) Thực chiến | ERX",
        "meta_desc": "Kiến thức chuyên sâu về Quản trị Chuỗi cung ứng (SCM) hiện đại: Chiến lược tìm nguồn cung ứng, hoạch định vật tư, vận hành kho bãi, Logistics và phân tích dữ liệu SCM.",
        "meta_key": "quản trị chuỗi cung ứng, supply chain management là gì, kiến thức chuỗi cung ứng thực chiến, phân tích dữ liệu chuỗi cung ứng"
    },
    "procurement-management": {
        "meta_title": "Quản trị Mua hàng (Procurement Management) & Strategic Sourcing | ERX",
        "meta_desc": "Cẩm nang Quản trị Mua sắm (Procurement) B2B: Tìm nguồn cung ứng chiến lược (Strategic Sourcing), phân tích chi phí TCO, 8 phương pháp tính Saving và đàm phán nhà cung cấp.",
        "meta_key": "quản trị mua hàng, procurement management, strategic sourcing là gì, phân tích tco, cắt giảm chi phí mua hàng"
    },
    "planning-management": {
        "meta_title": "Hoạch định Chuỗi cung ứng & Nhu cầu Vật tư (Planning / MRP) | ERX",
        "meta_desc": "Phương pháp Hoạch định Chuỗi cung ứng (Supply Chain Planning): Dự báo nhu cầu (Demand Forecasting), lập kế hoạch nguyên vật liệu (MRP) và tối ưu hóa mức tồn kho an toàn.",
        "meta_key": "planning management, hoạch định chuỗi cung ứng, tính toán mrp bằng python excel, quản lý kế hoạch sản xuất"
    },
    "inventory-management": {
        "meta_title": "Quản trị Kho hàng (Warehouse & Inventory Management) Thực chiến | ERX",
        "meta_desc": "Giải pháp tối ưu hóa vận hành kho hàng hiện đại: Thiết kế Layout kho theo phân tích ABC đa chiều, tối ưu lộ trình lấy hàng (Order Picking Routing) và kiểm soát tồn kho.",
        "meta_key": "warehouse management, inventory management, quản lý kho hàng, phân tích abc trong kho, tối ưu lộ trình lấy hàng"
    },
    "logistics-management": {
        "meta_title": "Quản trị Vận hành Logistics, Xuất nhập khẩu & Tối ưu Tuyến đường | ERX",
        "meta_desc": "Kiến thức thực chiến về Quản trị Logistics: Nghiệp vụ xuất nhập khẩu, tra cứu HS Code, bài toán tối ưu hóa tuyến đường vận tải (Route Optimization) và tính cước vận chuyển.",
        "meta_key": "quản trị logistics, logistics management, tối ưu hóa tuyến đường vận tải, tra cứu hs code, vận hành logistics thực chiến"
    },
    "python-for-supply-chain": {
        "meta_title": "Ứng dụng Python trong Chuỗi cung ứng & Phân tích Dữ liệu (Pandas) | ERX",
        "meta_desc": "Hướng dẫn lập trình Python cho chuyên viên Supply Chain & Data Analyst: Làm chủ Google Colab, Jupyter Notebook, thư viện Pandas DataFrame và bài toán tự động hóa MRP.",
        "meta_key": "python for supply chain, ứng dụng python trong chuỗi cung ứng, học thư viện pandas python, phân tích dữ liệu bằng python"
    },
    "project-management": {
        "meta_title": "Quản trị Dự án Chuẩn PMBOK 8: WBS, Đường găng CPM, EVM & AI Gantt | ERX",
        "meta_desc": "Trọn bộ cẩm nang Quản trị Dự án thực chiến theo chuẩn PMBOK Guide 8th Edition: Project Charter, Ma trận RACI, WBS, Đường găng CPM, 9 chỉ số EVM và định lượng rủi ro EMV.",
        "meta_key": "quản trị dự án pmbok 8, project management erx, cấu trúc wbs, đường găng cpm, earned value management evm, ai gantt planner"
    },
    "tro-thanh-giang-vien-cung-erx": {
        "meta_title": "Hợp tác trở thành Giảng viên Chuyên gia cùng ERX Việt Nam",
        "meta_desc": "Tham gia đội ngũ Giảng viên Chuyên gia tại ERX Việt Nam để lan tỏa kiến thức thực chiến về Phân tích Dữ liệu (Excel, Power BI, Python) và Quản trị Chuỗi cung ứng.",
        "meta_key": "tuyển giảng viên erx, hợp tác giảng dạy phân tích dữ liệu, giảng viên supply chain"
    },
    "thong-tin-tuyen-sinh": {
        "meta_title": "Thông tin Tuyển sinh các Khóa học Phân tích Dữ liệu & SCM | ERX",
        "meta_desc": "Lịch khai giảng và thông tin tuyển sinh các khóa đào tạo thực chiến về Excel, VBA, SQL, Power BI, Python và Quản trị Chuỗi cung ứng tại ERX Việt Nam.",
        "meta_key": "thông tin tuyển sinh erx, lịch khai giảng khóa học excel power bi, khóa học supply chain"
    },
    "tin-quan-trong": {
        "meta_title": "Tin tức Quan trọng & Hoạt động Đào tạo tại ERX Việt Nam",
        "meta_desc": "Cập nhật những thông báo, sự kiện, hội thảo chuyên đề và tin tức hoạt động đào tạo mới nhất từ Trung tâm Đào tạo Thực chiến ERX Việt Nam.",
        "meta_key": "tin tức erx việt nam, sự kiện đào tạo erx, thông báo khóa học erx"
    },
    "cuoc-thi-supply-chain-data-analysis-challenge": {
        "meta_title": "Cuộc thi Supply Chain Data Analysis Challenge | ERX Việt Nam",
        "meta_desc": "Sân chơi học thuật và thực chiến phân tích dữ liệu chuỗi cung ứng (Supply Chain Data Analysis Challenge) dành cho cộng đồng Supply Chain và Data Analyst tại Việt Nam.",
        "meta_key": "supply chain data analysis challenge, cuộc thi phân tích dữ liệu chuỗi cung ứng erx"
    },
    "cau-chuyen-thanh-cong": {
        "meta_title": "Câu chuyện Thành công & Dự án Ứng dụng Thực tế của Học viên ERX",
        "meta_desc": "Khám phá các dự án tự động hóa báo cáo và tối ưu hóa vận hành chuỗi cung ứng do chính học viên ERX Việt Nam triển khai thành công tại doanh nghiệp.",
        "meta_key": "câu chuyện thành công học viên erx, ứng dụng python excel vào công việc thực tế"
    },
    "su-kien": {
        "meta_title": "Sự kiện & Hội thảo Chuyên đề Phân tích Dữ liệu, Chuỗi cung ứng | ERX",
        "meta_desc": "Tổng hợp các sự kiện, buổi chia sẻ chuyên đề và hội thảo trực tuyến về ứng dụng công nghệ dữ liệu trong quản trị doanh nghiệp tại ERX Việt Nam.",
        "meta_key": "sự kiện erx, hội thảo phân tích dữ liệu, webinar chuỗi cung ứng"
    }
}

# 2. All 42 Short-Title Blog Articles (<45 chars) + 7 Meta-Description Upgrades
ARTICLE_SEO_UPGRADES = {
    "7123869202": {
        "title": "Giới thiệu Add-ins ERX Smart Tool: Công cụ tăng tốc xử lý Excel thực chiến",
        "meta_title": "Giới thiệu Add-ins ERX Smart Tool: Công cụ tăng tốc xử lý Excel"
    },
    "7123909199": {
        "title": "Phân tích Pareto (Quy tắc 80/20) trong Power BI bằng hàm DAX thực chiến",
        "meta_title": "Phân tích Pareto (Quy tắc 80/20) trong Power BI bằng công thức DAX"
    },
    "7123374265": {
        "title": "Phân biệt Calculated Columns và Measures trong ngôn ngữ DAX Power BI",
        "meta_title": "Phân biệt Calculated Columns và Measures trong DAX Power BI chi tiết"
    },
    "7123407300": {
        "title": "Cách tạo bảng lịch (Date Table) tự động trong Power BI bằng DAX & M",
        "meta_title": "Cách tạo Date Table (Calendar) tự động trong Power BI bằng DAX & M"
    },
    "7122939679": {
        "title": "Chiến lược đàm phán mua hàng hiệu quả với những nhà cung cấp lớn",
        "meta_title": "Cách đàm phán với những nhà cung cấp lớn trong Quản trị Mua hàng"
    },
    "7122399614": {
        "title": "Câu lệnh SQL SELECT trong Excel: Cú pháp truy vấn dữ liệu từ cơ bản đến nâng cao",
        "meta_title": "Câu lệnh SQL SELECT trong Excel: Cú pháp & Ví dụ truy vấn dữ liệu"
    },
    "7122169949": {
        "title": "SQL trong Excel: Giải pháp truy vấn và tổng hợp dữ liệu lớn siêu tốc",
        "meta_title": "SQL trong Excel: Cách truy vấn & tổng hợp dữ liệu lớn bằng ADODB"
    },
    "7122144092": {
        "title": "Strategic Sourcing là gì? Quy trình 7 bước tìm nguồn cung ứng chiến lược",
        "meta_title": "Strategic Sourcing là gì? Quy trình tìm nguồn cung ứng chiến lược",
        "meta_desc": "Tìm nguồn cung ứng chiến lược (Strategic Sourcing) là gì? Phân tích quy trình 7 bước kết nối phân tích chi tiêu (Spend Analysis), đàm phán nhà cung cấp và tối ưu TCO."
    },
    "7122305017": {
        "title": "Tối ưu hóa tuyến đường vận tải (Route Optimization) trong Logistics",
        "meta_title": "Tối ưu hóa tuyến đường (Route Optimization) giảm chi phí Logistics"
    },
    "7123893660": {
        "title": "DAX là gì? Tổng quan ngôn ngữ DAX trong Power BI cho người mới bắt đầu",
        "meta_title": "DAX là gì? Hướng dẫn ngôn ngữ DAX trong Power BI cho người mới"
    },
    "7123816032": {
        "title": "Cách viết và ứng dụng hàm LAMBDA để tạo hàm tùy chỉnh trong Excel 365",
        "meta_title": "Cách viết và sử dụng hàm LAMBDA trong Excel 365 kèm ví dụ thực tế"
    },
    "7123716407": {
        "title": "Tổng hợp các tính năng mới tuyệt vời nhất trên Microsoft Excel 365",
        "meta_title": "Các tính năng mới tuyệt vời nhất trong Microsoft Excel 365 nên biết"
    },
    "7123694822": {
        "title": "Hàm FILTER trong Excel 365: Cú pháp và 6 ví dụ lọc dữ liệu tự động",
        "meta_title": "Hàm FILTER trong Excel 365: Cú pháp & Cách lọc dữ liệu nhiều điều kiện"
    },
    "7123554595": {
        "title": "Hàm COUNTIFS trong Excel: Cú pháp và những lưu ý quan trọng cần biết",
        "meta_title": "Hàm COUNTIFS trong Excel: Cú pháp đếm nhiều điều kiện & Lưu ý đặc biệt"
    },
    "7122733141": {
        "title": "Cách sử dụng tính năng Paste Special Skip Blanks trong Microsoft Excel",
        "meta_title": "Cách sử dụng tính năng Skip Blanks trong Excel để dán bỏ qua ô trống"
    },
    "7122722851": {
        "title": "Hướng dẫn tạo danh sách tùy chỉnh (Custom List) để sắp xếp nhanh trong Excel",
        "meta_title": "Hướng dẫn tạo Custom List trong Excel để điền và sắp xếp dữ liệu nhanh",
        "meta_desc": "Hướng dẫn chi tiết cách tạo và quản lý danh sách tùy chỉnh (Custom List) trong Microsoft Excel, giúp tự động điền nhanh danh mục phòng ban và sắp xếp dữ liệu chuẩn xác."
    },
    "7122684703": {
        "title": "Trọn bộ bí kíp sử dụng hàm VLOOKUP trong Excel từ cơ bản đến nâng cao",
        "meta_title": "Bí kíp sử dụng hàm VLOOKUP trong Excel từ cơ bản đến nâng cao"
    },
    "7123563926": {
        "title": "Lộ trình 11 bước làm chủ Microsoft Excel từ cơ bản đến chuyên gia",
        "meta_title": "11 bước để làm chủ Microsoft Excel (Master Excel) cho người đi làm"
    },
    "7123388955": {
        "title": "Cách dùng lệnh PIVOT, UNION và UNION ALL khi truy vấn SQL trong Excel",
        "meta_title": "Câu lệnh PIVOT, UNION và UNION ALL trong SQL Excel VBA kèm ví dụ"
    },
    "7123183520": {
        "title": "Câu lệnh INSERT, UPDATE và DELETE khi thao tác dữ liệu SQL trong Excel",
        "meta_title": "Hướng dẫn câu lệnh INSERT, UPDATE, DELETE trong SQL Excel (ADODB)"
    },
    "7123179255": {
        "title": "Kỹ thuật dùng hàm IIF, Subquery và xác định dòng cuối (LastRow) trong SQL Excel",
        "meta_title": "Cách dùng hàm IIF, Subquery và tìm dòng cuối LastRow trong SQL Excel"
    },
    "7122913368": {
        "title": "Lập trình VBA thao tác với đối tượng Workbook trong Excel (Phần 2)",
        "meta_title": "Thao tác với đối tượng Workbook trong Excel VBA (Phần 2): Lưu & Đóng file"
    },
    "7122847956": {
        "title": "7 bước cơ bản thiết lập kết nối ADODB và câu lệnh SELECT trong SQL Excel",
        "meta_title": "7 bước cơ bản thiết lập kết nối ADODB & Câu lệnh SELECT trong SQL Excel"
    },
    "7122834639": {
        "title": "Hướng dẫn thiết lập môi trường lập trình VBA căn bản trong Microsoft Excel",
        "meta_title": "Thiết lập VBA căn bản trong Excel: Bật Developer, Macro & Cửa sổ VBE"
    },
    "7122706843": {
        "title": "Hướng dẫn tạo báo cáo tổng hợp siêu tốc bằng kết hợp SQL và VBA trong Excel",
        "meta_title": "Tạo báo cáo tự động siêu tốc bằng ngôn ngữ SQL và VBA trong Excel",
        "meta_desc": "Nâng cấp kỹ năng tự động hóa báo cáo trên Excel bằng sự kết hợp giữa ngôn ngữ truy vấn SQL (ADODB) và lập trình VBA: trích xuất liên file và tổng hợp dữ liệu trong 1 giây."
    },
    "7121866391": {
        "title": "Lập trình VBA trong Excel: Lộ trình tự động hóa báo cáo trong tầm tay",
        "meta_title": "Lập trình VBA trong Excel: Hướng dẫn viết code Macro tự động hóa báo cáo"
    },
    "7121832835": {
        "title": "Tổng quan về lập trình VBA và các tính năng tự động hóa trong Excel",
        "meta_title": "VBA trong Excel là gì? Các tính năng hỗ trợ tự động hóa bảng tính"
    },
    "7123117353": {
        "title": "Câu lệnh JOIN trong SQL Excel (INNER, LEFT, RIGHT JOIN) thay thế VLOOKUP",
        "meta_title": "Câu lệnh JOIN trong SQL Excel: Cách kết nối nhiều bảng dữ liệu siêu tốc"
    },
    "7123107285": {
        "title": "Một số thao tác kỹ thuật cơ bản khi viết câu lệnh truy vấn SQL trong Excel",
        "meta_title": "Một số thao tác cơ bản trong SQL Excel: Cắt chuỗi, nối dòng & Truyền biến"
    },
    "7122985392": {
        "title": "Cách sử dụng ký tự đại diện (Wildcard) và các toán tử lọc trong SQL Excel",
        "meta_title": "Ký tự đại diện Wildcard (%, _) & Toán tử LIKE, BETWEEN, IN trong SQL Excel"
    },
    "7122975038": {
        "title": "Cách dùng mệnh đề WHERE, GROUP BY, HAVING và ORDER BY trong SQL Excel",
        "meta_title": "Hướng dẫn mệnh đề WHERE, GROUP BY, HAVING, ORDER BY trong SQL Excel"
    },
    "7122926210": {
        "title": "Nghệ thuật thay đổi cách thuyết phục người khác trong môi trường doanh nghiệp",
        "meta_title": "Thay đổi cách bạn thuyết phục người khác: 5 rào cản tâm lý cần tháo gỡ"
    },
    "7122438204": {
        "title": "Hướng dẫn sử dụng thư viện Pandas trong Python để khám phá dữ liệu (EDA)",
        "meta_title": "Sử dụng thư viện Pandas trong Python để khám phá & phân tích dữ liệu"
    },
    "7122425785": {
        "title": "Giới thiệu phần mềm tối ưu hóa tuyến đường vận tải (Route Optimization) trên Excel",
        "meta_title": "Giới thiệu phần mềm tối ưu hóa tuyến đường (Route Optimization) ERX"
    },
    "7122518308": {
        "title": "Giới thiệu Google Colab: Môi trường lập trình Python miễn phí trên đám mây",
        "meta_title": "Google Colab là gì? Hướng dẫn sử dụng Google Colab lập trình Python từ A-Z"
    },
    "7123986505": {
        "title": "Tuyển dụng Procurement Specialist - Direct Material (Raw Materials & Energy)",
        "meta_title": "Tuyển dụng Chuyên viên Mua hàng (Procurement Specialist - Direct Material)",
        "meta_desc": "Thông tin tuyển dụng vị trí Chuyên viên Mua hàng Nguyên vật liệu trực tiếp (Procurement Specialist - Direct Material): mô tả công việc, yêu cầu năng lực và chế độ đãi ngộ."
    },
    "7123976602": {
        "title": "Tuyển dụng Lead Logistics - Process Specialist (Chuyên gia Quy trình Logistics)",
        "meta_title": "Tuyển dụng Lead Logistics - Process Specialist | Cơ hội nghề nghiệp SCM",
        "meta_desc": "Cơ hội nghề nghiệp vị trí Lead Logistics - Process Specialist: Chịu trách nhiệm chuẩn hóa quy trình vận hành Logistics, tối ưu chi phí vận tải và phát triển hệ thống."
    },
    "7123968182": {
        "title": "Tuyển dụng Trưởng phòng Chuỗi cung ứng (Supply Chain Manager)",
        "meta_title": "Tuyển dụng Supply Chain Manager (Trưởng phòng Quản lý Chuỗi cung ứng)",
        "meta_desc": "Thông tin tuyển dụng vị trí Trưởng phòng Chuỗi cung ứng (Supply Chain Manager): Điều hành chiến lược kế hoạch, mua hàng, kho vận và tối ưu hiệu suất chuỗi cung ứng."
    },
    "7123946893": {
        "title": "Tuyển dụng vị trí Trợ lý Kinh doanh (Sales Admin) ngành Thiết bị Công nghiệp",
        "meta_title": "Tuyển dụng Trợ lý Kinh doanh (Sales Admin) - Cơ hội việc làm tại ERX"
    },
    "7123956328": {
        "title": "Tuyển dụng Deputy Purchasing and Logistics Team Leader ( Mua hàng & Logistics)",
        "meta_title": "Tuyển dụng Deputy Purchasing & Logistics Team Leader | Việc làm SCM",
        "meta_desc": "Tuyển dụng vị trí Phó nhóm Mua hàng Quốc tế & Logistics (Deputy Purchasing and Logistics Team Leader): Quản lý thu mua nhập khẩu, đàm phán nhà cung cấp và điều phối xuất nhập khẩu."
    },
    "7122675302": {
        "title": "Làm thế nào để vẽ và thiết kế biểu đồ cột (Column Chart) chuyên nghiệp trong Excel?",
        "meta_title": "Cách vẽ biểu đồ cột (Column Chart) chuyên nghiệp trong Microsoft Excel"
    },
    "7122807028": {
        "title": "Làm quen với Jupyter Notebook: Công cụ lập trình Python phân tích dữ liệu",
        "meta_title": "Hướng dẫn sử dụng Jupyter Notebook cho người mới học Python & Data"
    },
    "7122812051": {
        "title": "Làm quen với thư viện Pandas và cấu trúc dữ liệu DataFrame trong Python",
        "meta_title": "Làm quen với thư viện Pandas và DataFrame trong Python từ cơ bản"
    },
    "7123094250": {
        "title": "Phân tích hành vi của người mua hàng công nghiệp (Industrial Buying Behavior)",
        "meta_title": "Hành vi của người mua hàng công nghiệp trong Quản trị Mua sắm B2B"
    }
}

# 3. All 20 Workshop Pages (831*) SEO Metadata & URLs
WORKSHOP_SEO_MAP = {
    "8315644": {
        "url": "https://erx.vn/tai-sao-and-or-khong-spill-4-giai-phap-thay-the-trong-excel-moi-8315644.html",
        "h1": "“Tại sao hàm AND/OR không Spill? 4 giải pháp thay thế trong Excel 365”",
        "meta_title": "Tại sao hàm AND/OR không Spill? 4 giải pháp mảng động trong Excel 365 | ERX",
        "meta_desc": "Hội thảo thực chiến ERX: Giải thích nguyên nhân hàm AND/OR không trả về mảng động (Spill) khi kết hợp với FILTER/IF và 4 giải pháp thay thế bằng toán tử *, +, BYROW."
    },
    "8318776": {
        "url": "https://erx.vn/groupby-trong-excel-tong-hop-du-lieu-theo-thang-fiscal-year-chuan-xac-8318776.html",
        "h1": "“Hàm GROUPBY trong Excel – Tổng hợp dữ liệu theo tháng & Fiscal Year chuẩn xác”",
        "meta_title": "Hàm GROUPBY trong Excel 365: Tổng hợp dữ liệu theo Tháng & Fiscal Year | ERX",
        "meta_desc": "Workshop thực chiến cách ứng dụng hàm GROUPBY mới trong Excel 365 để gom nhóm, tính tổng doanh thu theo tháng và năm tài chính (Fiscal Year) thay thế PivotTable."
    },
    "8313513": {
        "url": "https://erx.vn/xlookup-vs-filter-dung-ham-nao-trong-tinh-huong-nao-8313513.html",
        "h1": "“XLOOKUP vs FILTER – Dùng hàm nào trong tình huống nào?”",
        "meta_title": "So sánh hàm XLOOKUP và FILTER trong Excel 365: Khi nào dùng hàm nào? | ERX",
        "meta_desc": "Phân tích chuyên sâu sự khác biệt giữa hàm XLOOKUP và hàm FILTER trong Excel 365: Cách chọn đúng hàm khi dò tìm 1 kết quả, nhiều kết quả và tối ưu tốc độ bảng tính."
    },
    "8312031": {
        "url": "https://erx.vn/filter-with-wildcards-3-cach-tim-kiem-nang-cao-trong-excel-8312031.html",
        "h1": "“Hàm FILTER với Wildcards – 3 cách tìm kiếm nâng cao trong Excel”",
        "meta_title": "Hàm FILTER kết hợp Wildcard trong Excel: 3 cách lọc tìm kiếm gần đúng | ERX",
        "meta_desc": "Hướng dẫn 3 kỹ thuật khắc phục nhược điểm hàm FILTER không hỗ trợ trực tiếp ký tự đại diện (*, ?) bằng tổ hợp SEARCH + ISNUMBER, REGEXTEST và XMATCH trong Excel 365."
    },
    "8313066": {
        "url": "https://erx.vn/tu-bo-xlookup-lam-chu-data-model-power-pivot-buoc-khoi-dau-de-tien-toi-8313066.html",
        "h1": "“Từ bỏ XLOOKUP – Làm chủ Data Model & Power Pivot: Bước khởi đầu tiến tới Power BI”",
        "meta_title": "Làm chủ Data Model & Power Pivot trong Excel: Bước đệm tiến tới Power BI | ERX",
        "meta_desc": "Tại sao nên chuyển từ nối bảng bằng VLOOKUP/XLOOKUP sang xây dựng mô hình quan hệ dữ liệu (Data Model & Power Pivot) để xử lý hàng triệu dòng mượt mà trên Excel?"
    },
    "8314296": {
        "url": "https://erx.vn/su-dung-ham-hyperlink-trong-excel-tao-bao-cao-thong-minh-va-dieu-huong-8314296.html",
        "h1": "🚀 “Sử dụng hàm HYPERLINK trong Excel – Tạo báo cáo thông minh và điều hướng chuyên nghiệp”",
        "meta_title": "Hàm HYPERLINK trong Excel: Cách tạo Menu điều hướng báo cáo thông minh | ERX",
        "meta_desc": "Hướng dẫn ứng dụng hàm HYPERLINK kết hợp CELL, ADDRESS, XMATCH để tạo mục lục điều hướng động giữa các Sheet, mở nhanh thư mục chứng từ và thiết kế Dashboard chuyên nghiệp."
    },
    "8318087": {
        "url": "https://erx.vn/giai-ma-ham-match-trong-excel-true-1-0-khac-nhau-nhu-the-nao-8318087.html",
        "h1": "🚀 “Giải mã hàm MATCH trong Excel – Tham số 1, 0, -1 khác nhau như thế nào?”",
        "meta_title": "Giải mã hàm MATCH trong Excel: Phân biệt tham số 1, 0 và -1 chi tiết | ERX",
        "meta_desc": "Hiểu tận gốc cơ chế tìm kiếm nhị phân (Binary Search) và tuyến tính của hàm MATCH / XMATCH trong Excel với các kiểu khớp 0 (chính xác), 1 (nhỏ hơn) và -1 (lớn hơn)."
    },
    "8316838": {
        "url": "https://erx.vn/tai-sao-nen-chuyen-tu-vlookup-sang-index-match-tim-kiem-du-lieu-chuyen-8316838.html",
        "h1": "🚀 “Tại sao nên chuyển từ VLOOKUP sang INDEX MATCH – Tìm kiếm dữ liệu chuyên nghiệp trong Excel”",
        "meta_title": "Tại sao nên chuyển từ VLOOKUP sang INDEX MATCH trong Excel? | Hội thảo ERX",
        "meta_desc": "So sánh hiệu năng và tính linh hoạt giữa VLOOKUP và cặp hàm INDEX + MATCH: Cách dò tìm ngược từ phải sang trái, chống gãy công thức khi chèn cột và dò tìm đa chiều."
    },
    "8318928": {
        "url": "https://erx.vn/power-query-chuan-hoa-du-lieu-cham-cong-bang-power-query-noi-khong-8318928.html",
        "h1": "🚀 “Power Query – Chuẩn hóa dữ liệu chấm công bằng Power Query: Nói không với dữ liệu lỗi”",
        "meta_title": "Chuẩn hóa dữ liệu chấm công tự động bằng Power Query trong Excel | ERX",
        "meta_desc": "Hướng dẫn thực chiến dùng Power Query trong Excel để làm sạch, xoay bảng (Unpivot) và tự động tổng hợp bảng chấm công phức tạp từ máy chấm công chỉ với 1 nút Refresh."
    },
    "8313099": {
        "url": "https://erx.vn/power-query-trong-excel-lam-sach-tong-hop-du-lieu-chuyen-nghiep-8313099.html",
        "h1": "🚀 “Power Query trong Excel – Làm sạch & tổng hợp dữ liệu chuyên nghiệp”",
        "meta_title": "Power Query trong Excel: Hướng dẫn làm sạch & gộp dữ liệu tự động | ERX",
        "meta_desc": "Làm chủ quy trình ETL (Extract - Transform - Load) bằng công cụ Power Query có sẵn trong Excel để gộp hàng chục file báo cáo và chuẩn hóa dữ liệu không cần VBA."
    },
    "8313087": {
        "url": "https://erx.vn/thuc-hanh-giai-de-excel-kiem-tra-trinh-do-cua-ban-8313087.html",
        "h1": "🚀 “Thực hành giải đề Excel – Kiểm tra trình độ của bạn”",
        "meta_title": "Thực hành giải đề thi tuyển dụng Excel thực chiến cho Data & Supply Chain | ERX",
        "meta_desc": "Trực tiếp giải các bài test Excel tuyển dụng thực tế tại các tập đoàn lớn cho vị trí Supply Chain, Mua hàng, Kế toán và Data Analyst cùng chuyên gia ERX Việt Nam."
    },
    "8317247": {
        "url": "https://erx.vn/lam-chu-table-trong-excel-tham-chieu-ham-va-ung-dung-bao-cao-tren-8317247.html",
        "h1": "🚀 “Làm chủ Table trong Excel – Tham chiếu, hàm và ứng dụng báo cáo trên Excel 365”",
        "meta_title": "Làm chủ Excel Table (Ctrl+T): Tham chiếu có cấu trúc & Báo cáo tự động | ERX",
        "meta_desc": "Khám phá sức mạnh của Excel Table (Structured References): Cách viết công thức tự động co giãn theo dòng dữ liệu mới và kết hợp mượt mà với hàm mảng động Excel 365."
    },
    "8312267": {
        "url": "https://erx.vn/sumproduct-than-chuong-phan-2-giai-ma-co-che-ma-tran-hieu-tan-goc-co-8312267.html",
        "h1": "“Làm chủ hàm SUMPRODUCT – Phần 2: Giải mã cơ chế mảng & ma trận”",
        "meta_title": "Làm chủ hàm SUMPRODUCT (Phần 2): Giải mã cơ chế tính toán Ma trận | ERX",
        "meta_desc": "Hiểu sâu bản chất toán học của mảng 1 chiều, mảng 2 chiều (Ma trận dòng × cột) và toán tử dấu gạch ngang kép (--) bên trong hàm SUMPRODUCT nâng cao."
    },
    "8313732": {
        "url": "https://erx.vn/sumproduct-than-chuong-phan-01-ung-dung-thuc-chien-trong-bao-cao-va-xu-8313732.html",
        "h1": "“Làm chủ hàm SUMPRODUCT – Phần 1: Ứng dụng thực chiến trong báo cáo và xử lý dữ liệu”",
        "meta_title": "Làm chủ hàm SUMPRODUCT (Phần 1): Ứng dụng tính tổng đa điều kiện | ERX",
        "meta_desc": "Hướng dẫn thực hành hàm SUMPRODUCT trong Excel để tính tổng có điều kiện phức tạp (AND/OR), tính trung bình gia quyền và xử lý dữ liệu mảng không cần Ctrl+Shift+Enter."
    },
    "8318279": {
        "url": "https://erx.vn/ung-dung-check-box-trong-excel-365-check-box-conditional-formatting-8318279.html",
        "h1": "“Ứng dụng Check Box trong Excel 365 – Kết hợp Conditional Formatting & hàm FILTER”",
        "meta_title": "Cách tạo và ứng dụng Check Box mới trong Excel 365 kèm hàm FILTER | ERX",
        "meta_desc": "Hướng dẫn sử dụng tính năng Cell Checkbox mới trên Excel 365 kết hợp với Conditional Formatting và hàm FILTER để làm bảng theo dõi tiến độ công việc tương tác."
    },
    "8315591": {
        "url": "https://erx.vn/tu-dong-hoa-tong-hop-du-lieu-google-sheets-excel-power-bi-google-8315591.html",
        "h1": "“Tự động hóa tổng hợp dữ liệu Google Sheets sang Excel & Power BI”",
        "meta_title": "Cách kết nối và tự động đồng bộ dữ liệu Google Sheets sang Excel & Power BI",
        "meta_desc": "Giải pháp xây dựng luồng đồng bộ dữ liệu tự động từ nhiều file Google Sheets về Microsoft Excel và Power BI bằng Google Drive Desktop, Apps Script và Power Query."
    },
    "8316071": {
        "url": "https://erx.vn/lam-chu-xu-ly-merge-cells-trong-excel-365-conditional-formatting-custom-8316071.html",
        "h1": "“Làm chủ xử lý Merge Cells trong Excel 365 – Conditional Formatting, Custom Format & AGGREGATE”",
        "meta_title": "Cách xử lý ô gộp (Merge Cells) trong Excel 365 không làm hỏng dữ liệu | ERX",
        "meta_desc": "Giải pháp thay thế thao tác Merge & Center gây lỗi lọc dữ liệu bằng Center Across Selection, Conditional Formatting giả lập gộp ô và cách điền đầy dữ liệu sau khi bỏ gộp."
    },
    "8315449": {
        "url": "https://erx.vn/lam-chu-dynamic-named-range-trong-excel-365-index-offset-trimrange-8315449.html",
        "h1": "“Làm chủ Dynamic Named Range trong Excel 365 – INDEX, OFFSET, TRIMRANGE & các giải pháp khác”",
        "meta_title": "Cách tạo vùng tên động (Dynamic Named Range) bằng INDEX, OFFSET & TRIMRANGE",
        "meta_desc": "So sánh 4 phương pháp tạo dải ô động (Dynamic Named Range) trong Excel 365: Toán tử tràn (#), hàm mới TRIMRANGE / dấu chấm (.:.), hàm INDEX và hàm OFFSET."
    },
    "8317559": {
        "url": "https://erx.vn/lam-chu-pareto-chart-trong-excel-pivot-table-running-total-8317559.html",
        "h1": "“Làm chủ biểu đồ Pareto Chart trong Excel – PivotTable, % Running Total & Highlight Visual”",
        "meta_title": "Cách vẽ biểu đồ Pareto 80/20 trong Excel bằng PivotTable & Highlight động",
        "meta_desc": "Hướng dẫn từng bước thiết kế biểu đồ Pareto (Quy tắc 80/20) chuyên nghiệp trên Excel kết hợp đường lũy kế % Running Total và tự động tô màu nhóm nguyên nhân cốt lõi."
    },
    "8318738": {
        "url": "https://erx.vn/lam-chu-search-box-trong-excel-filter-conditional-formatting-activex-8318738.html",
        "h1": "“Làm chủ Search Box trong Excel – Kết hợp FILTER, Conditional Formatting & ActiveX TextBox”",
        "meta_title": "Cách tạo ô tìm kiếm tức thời (Search Box) trong Excel bằng FILTER & TextBox",
        "meta_desc": "Hướng dẫn tạo thanh tìm kiếm dữ liệu theo thời gian thực (Instant Search Box) ngay khi gõ phím trong Excel bằng ActiveX TextBox kết hợp hàm FILTER và Conditional Formatting."
    }
}

# 4. Build Master Sitemap (161 Canonical URLs)
canonical_hub_urls = [
    "https://erx.vn/",
    "https://erx.vn/kien-thuc.html",
    "https://erx.vn/hoi-thao.html",
    "https://erx.vn/dao-tao-doanh-nghiep.html",
    "https://erx.vn/phan-mem.html",
    "https://erx.vn/tuyen-dung.html",
    "https://erx.vn/lien-he.html",
    "https://erx.vn/gioi-thieu.html",
    "https://erx.vn/mau-file-quan-ly-excel.html",
    "https://erx.vn/excel.html",
    "https://erx.vn/excel-functions.html",
    "https://erx.vn/cac-ham-excel-365.html",
    "https://erx.vn/excel-vba.html",
    "https://erx.vn/sql.html",
    "https://erx.vn/dashboard-automated-report.html",
    "https://erx.vn/power-bi.html",
    "https://erx.vn/supply-chain-management.html",
    "https://erx.vn/procurement-management.html",
    "https://erx.vn/planning-management.html",
    "https://erx.vn/inventory-management.html",
    "https://erx.vn/logistics-management.html",
    "https://erx.vn/python-for-supply-chain.html",
    "https://erx.vn/project-management.html",
]

workshop_urls = [v["url"] for v in WORKSHOP_SEO_MAP.values()]

all_sitemap_urls = []
for u in canonical_hub_urls + article_urls + workshop_urls:
    if u not in all_sitemap_urls:
        all_sitemap_urls.append(u)

OUT_SITEMAP.write_text("\n".join(all_sitemap_urls) + "\n", encoding="utf-8")
print(f"Wrote {OUT_SITEMAP} with {len(all_sitemap_urls)} canonical URLs")

# 5. Build Synchronous Head SEO & Valid Schema.org JSON-LD Upgrade Script for META.SCRIPT_HEADER
HEAD_SEO_AND_SCHEMA_SCRIPT = f"""
<script id="erx-seo-schema-upgrader">
(function() {{
  var menuSeo = {json.dumps(MENU_SEO_MAP, ensure_ascii=False)};
  var workshopSeo = {json.dumps(WORKSHOP_SEO_MAP, ensure_ascii=False)};
  var path = window.location.pathname || '/';
  var cleanSlug = path.replace(/^\\/+/, '').replace(/\\.html$/i, '');

  function setMetaTag(attrName, attrVal, content) {{
    if (!content) return;
    var sel = 'meta[' + attrName + '="' + attrVal + '"]';
    var el = document.querySelector(sel);
    if (!el) {{
      el = document.createElement('meta');
      el.setAttribute(attrName, attrVal);
      document.head.appendChild(el);
    }}
    el.setAttribute('content', content);
  }}

  // 1. Check if current page is a Workshop detail page (-831*.html)
  var wm = path.match(/-(\\d{{7}})\\.html$/);
  var wid = wm ? wm[1] : null;
  if (wid && workshopSeo[wid]) {{
    var w = workshopSeo[wid];
    document.title = w.meta_title;
    setMetaTag('name', 'description', w.meta_desc);
    setMetaTag('property', 'og:title', w.meta_title);
    setMetaTag('property', 'og:description', w.meta_desc);
  }} else if (menuSeo[cleanSlug]) {{
    var m = menuSeo[cleanSlug];
    if (!document.title || document.title.length < 35) {{
      document.title = m.meta_title;
    }}
    var curDescEl = document.querySelector('meta[name="description"]');
    var curDesc = curDescEl ? (curDescEl.getAttribute('content') || '').trim() : '';
    if (!curDesc || curDesc.length < 50) {{
      setMetaTag('name', 'description', m.meta_desc);
      setMetaTag('property', 'og:description', m.meta_desc);
    }}
    setMetaTag('property', 'og:title', document.title);
  }}

  // 2. Replace broken lowercase JSON-LD (@type: "article" / "website") with valid Schema.org Graph
  function injectValidSchema() {{
    var oldScripts = document.querySelectorAll('script[type="application/ld+json"]');
    for (var i = 0; i < oldScripts.length; i++) {{
      var txt = oldScripts[i].textContent || '';
      if (txt.indexOf('"@type":"article"') !== -1 || txt.indexOf('"@type": "article"') !== -1 || txt.indexOf('"@type":"website"') !== -1 || txt.indexOf('"@type": "website"') !== -1) {{
        oldScripts[i].parentNode.removeChild(oldScripts[i]);
      }}
    }}
    if (document.getElementById('erx-valid-jsonld')) return;

    var canonicalUrl = 'https://erx.vn' + (path === '/index.html' ? '/' : path);
    var pageTitle = document.title || 'ERX - Trung tâm đào tạo thực chiến phân tích dữ liệu & quản lý chuỗi cung ứng';
    var descEl = document.querySelector('meta[name="description"]');
    var pageDesc = descEl ? (descEl.getAttribute('content') || '') : pageTitle;
    var ogImgEl = document.querySelector('meta[property="og:image"]');
    var pageImg = ogImgEl && ogImgEl.getAttribute('content') ? ogImgEl.getAttribute('content') : 'https://erx.vn/Images/Share/logo-erx.png';
    if (pageImg.indexOf('http') !== 0) pageImg = 'https://erx.vn' + (pageImg.charAt(0) === '/' ? '' : '/') + pageImg;

    var graph = [
      {{
        "@type": "EducationalOrganization",
        "@id": "https://erx.vn/#organization",
        "name": "ERX Việt Nam",
        "alternateName": "Trung tâm Đào tạo Thực chiến Phân tích Dữ liệu & Quản lý Chuỗi cung ứng ERX",
        "url": "https://erx.vn/",
        "logo": "https://erx.vn/Images/Share/logo-erx.png",
        "telephone": "+84-879-490-845",
        "email": "info@erx.vn",
        "sameAs": [
          "https://community.erx.vn/",
          "https://project-management.erx.vn/",
          "https://khoahoc.erx.vn/"
        ]
      }},
      {{
        "@type": "WebSite",
        "@id": "https://erx.vn/#website",
        "url": "https://erx.vn/",
        "name": "ERX Việt Nam",
        "publisher": {{ "@id": "https://erx.vn/#organization" }},
        "inLanguage": "vi-VN"
      }}
    ];

    // BreadcrumbList from .breadcrumb if present
    var bcLinks = document.querySelectorAll('ul.breadcrumb li a');
    if (bcLinks && bcLinks.length > 0) {{
      var itemList = [];
      for (var b = 0; b < bcLinks.length; b++) {{
        var bName = (bcLinks[b].textContent || '').trim();
        var bHref = bcLinks[b].getAttribute('href') || '/';
        if (bHref === '#' || bHref === '/#.html') bHref = 'https://erx.vn/';
        else if (bHref.indexOf('http') !== 0) bHref = 'https://erx.vn' + (bHref.charAt(0) === '/' ? '' : '/') + bHref;
        if (bName) {{
          itemList.push({{
            "@type": "ListItem",
            "position": itemList.length + 1,
            "name": bName,
            "item": bHref
          }});
        }}
      }}
      if (itemList.length > 0) {{
        graph.push({{
          "@type": "BreadcrumbList",
          "@id": canonicalUrl + "#breadcrumb",
          "itemListElement": itemList
        }});
      }}
    }}

    // TechArticle for Blog Articles (-712*.html) or EducationEvent for Workshops (-831*.html)
    if (/-(712\\d+)\\.html$/.test(path)) {{
      var h1El = document.querySelector('.ct-article-detail h1, h1');
      var headline = h1El ? (h1El.textContent || '').trim() : pageTitle;
      graph.push({{
        "@type": "TechArticle",
        "@id": canonicalUrl + "#article",
        "mainEntityOfPage": canonicalUrl,
        "headline": headline,
        "description": pageDesc,
        "image": pageImg,
        "inLanguage": "vi-VN",
        "author": {{ "@id": "https://erx.vn/#organization" }},
        "publisher": {{ "@id": "https://erx.vn/#organization" }}
      }});
    }} else if (wid && workshopSeo[wid]) {{
      graph.push({{
        "@type": "EducationEvent",
        "@id": canonicalUrl + "#event",
        "name": workshopSeo[wid].h1.replace(/^[🚀“"\\s]+|[”"\\s]+$/g, ''),
        "description": workshopSeo[wid].meta_desc,
        "url": canonicalUrl,
        "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
        "eventStatus": "https://schema.org/EventScheduled",
        "isAccessibleForFree": true,
        "organizer": {{ "@id": "https://erx.vn/#organization" }}
      }});
    }}

    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.id = 'erx-valid-jsonld';
    s.textContent = JSON.stringify({{ "@context": "https://schema.org", "@graph": graph }});
    document.head.appendChild(s);
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', injectValidSchema);
  }} else {{
    injectValidSchema();
  }}
}})();
</script>
""".strip()

sitemap_b64 = __import__("base64").b64encode(OUT_SITEMAP.read_bytes()).decode("ascii")

js_code = f"""// ERX Master SEO Upgrader (Menus, Articles, Workshops, Schema.org & Sitemap)
window.ERX_MENU_SEO_MAP = {json.dumps(MENU_SEO_MAP, ensure_ascii=False)};
window.ERX_ARTICLE_SEO_UPGRADES = {json.dumps(ARTICLE_SEO_UPGRADES, ensure_ascii=False)};
window.ERX_WORKSHOP_SEO_MAP = {json.dumps(WORKSHOP_SEO_MAP, ensure_ascii=False)};
window.ERX_HEAD_SEO_SCHEMA_SCRIPT = {json.dumps(HEAD_SEO_AND_SCHEMA_SCRIPT, ensure_ascii=False)};
window.ERX_MASTER_SITEMAP_B64 = {json.dumps(sitemap_b64)};

window.erxSerializeForm = function(form) {{
  const fd = new URLSearchParams();
  for (const el of form.elements) {{
    if (!el.name) continue;
    const tag = el.tagName.toLowerCase();
    const type = (el.type || "").toLowerCase();
    if (type === "checkbox" || type === "radio") {{
      if (el.checked) fd.append(el.name, el.value || "on");
    }} else if (tag === "select" && el.multiple) {{
      for (const opt of el.options) {{
        if (opt.selected) fd.append(el.name, opt.value);
      }}
    }} else if (type !== "submit" && type !== "button" && type !== "image" && type !== "file") {{
      fd.set(el.name, el.value || "");
    }}
  }}
  return fd;
}};

// 1. Update all Category & Menu Hub SEO Metadata (Skipping Menu 578 'Trang chủ')
window.erxUpgradeAllMenusSeo = async function() {{
  const results = {{ updated: [], skipped: [], errors: [] }};
  const menuTypes = ["main-menu-blog", "menu-hidden"];
  const discoveredIds = new Set();

  for (const mt of menuTypes) {{
    const listUrl = `/administrator/menu/list?from=1&divid=200&sTypeMenu=${{mt}}&nPageSize=200`;
    const resp = await fetch(listUrl, {{ credentials: "include" }});
    const html = await resp.text();
    const matches = html.matchAll(/nId=(\\d+)/gi);
    for (const m of matches) {{
      if (m[1] !== "0") discoveredIds.add({{ id: m[1], sTypeMenu: mt }});
    }}
  }}

  const seenId = new Set();
  for (const item of discoveredIds) {{
    const mid = item.id;
    if (seenId.has(mid)) continue;
    seenId.add(mid);

    // CRITICAL: Never touch Menu 578 (Trang chủ) so '/' alias is never altered
    if (String(mid) === "578") {{
      results.skipped.push({{ mid, reason: "Homepage Menu 578 protected" }});
      continue;
    }}

    try {{
      const editUrl = `/administrator/menu/editex.aspx?from=1&divid=200&sTypeMenu=${{item.sTypeMenu}}&nId=${{mid}}`;
      const resp = await fetch(editUrl, {{ credentials: "include" }});
      const html = await resp.text();
      const doc = new DOMParser().parseFromString(html, "text/html");
      const form = doc.querySelector("form");
      if (!form) continue;

      const fd = window.erxSerializeForm(form);
      const alias = (fd.get("LIST_TITLEBYLANGUAGE[0].ALIAS") || "").trim().replace(/^\\/+/, "").replace(/\\.html$/i, "");
      const seo = window.ERX_MENU_SEO_MAP[alias];
      if (!seo) {{
        results.skipped.push({{ mid, alias, reason: "No map entry" }});
        continue;
      }}

      if (seo.new_nav_title) {{
        fd.set("LIST_TITLEBYLANGUAGE[0].TITLE", seo.new_nav_title);
      }}
      // Populate all possible Meta Title / Meta Desc / Meta Key fields on the menu form
      for (const k of Array.from(fd.keys())) {{
        const up = k.toUpperCase();
        if (up.includes("META_TITLE") || up.includes("PAGETITLE") || up.includes("PAGE_TITLE")) {{
          fd.set(k, seo.meta_title);
        }} else if (up.includes("META_DESC")) {{
          fd.set(k, seo.meta_desc);
        }} else if (up.includes("META_KEY")) {{
          fd.set(k, seo.meta_key);
        }}
      }}
      fd.set("MENU.META_TITLE", seo.meta_title);
      fd.set("MENU.META_DESC", seo.meta_desc);
      fd.set("MENU.META_KEY", seo.meta_key);
      if (fd.has("LIST_TITLEBYLANGUAGE[0].META_TITLE")) fd.set("LIST_TITLEBYLANGUAGE[0].META_TITLE", seo.meta_title);
      if (fd.has("LIST_TITLEBYLANGUAGE[0].META_DESC")) fd.set("LIST_TITLEBYLANGUAGE[0].META_DESC", seo.meta_desc);
      if (fd.has("LIST_TITLEBYLANGUAGE[0].META_KEY")) fd.set("LIST_TITLEBYLANGUAGE[0].META_KEY", seo.meta_key);

      fd.set("btnSubmit", "save");
      const postResp = await fetch(editUrl, {{
        method: "POST",
        credentials: "include",
        headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
        body: fd.toString()
      }});
      results.updated.push({{ mid, alias, ok: postResp.ok, status: postResp.status }});
    }} catch (e) {{
      results.errors.push({{ mid, err: String(e) }});
    }}
  }}
  return results;
}};

// 2. Update all 42 Short-Title Blog Articles & 7 Short/Generic Meta-Description Blog Articles
window.erxUpgradeArticlesSeo = async function() {{
  const entries = Object.entries(window.ERX_ARTICLE_SEO_UPGRADES);
  const results = {{ updated: 0, sampleKeys: null, errors: [] }};
  const batchSize = 5;

  for (let i = 0; i < entries.length; i += batchSize) {{
    const batch = entries.slice(i, i + batchSize);
    await Promise.all(batch.map(async ([nid, seo]) => {{
      try {{
        const editUrl = `/administrator/content/edit.aspx?nContentId=${{nid}}&divid=300&from=31`;
        const resp = await fetch(editUrl, {{ credentials: "include" }});
        const html = await resp.text();
        const doc = new DOMParser().parseFromString(html, "text/html");
        const form = doc.querySelector("form");
        if (!form) {{
          results.errors.push({{ nid, err: "No form" }});
          return;
        }}

        const fd = window.erxSerializeForm(form);
        if (!results.sampleKeys) {{
          results.sampleKeys = Array.from(fd.keys()).filter(k => k.toUpperCase().includes("TITLE") || k.toUpperCase().includes("META") || k.toUpperCase().includes("DESC"));
        }}

        if (seo.title) {{
          fd.set("CONTENTS[0].TITLE", seo.title);
        }}
        const targetMetaTitle = seo.meta_title || seo.title;
        if (targetMetaTitle) {{
          for (const k of Array.from(fd.keys())) {{
            if (k.toUpperCase().includes("META_TITLE") || k.toUpperCase().includes("PAGETITLE") || k.toUpperCase().includes("PAGE_TITLE")) {{
              fd.set(k, targetMetaTitle);
            }}
          }}
          fd.set("CONTENTS[0].META_TITLE", targetMetaTitle);
          fd.set("CONTENT.META_TITLE", targetMetaTitle);
        }}

        if (seo.meta_desc) {{
          for (const k of Array.from(fd.keys())) {{
            if (k.toUpperCase().includes("META_DESC") || k.toUpperCase().includes("METADESC")) {{
              fd.set(k, seo.meta_desc);
            }}
          }}
          fd.set("CONTENTS[0].META_DESC", seo.meta_desc);
          fd.set("CONTENT.META_DESC", seo.meta_desc);
        }}

        fd.set("btnSubmit", "save_and_close");
        const postResp = await fetch(editUrl, {{
          method: "POST",
          credentials: "include",
          headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
          body: fd.toString()
        }});
        if (postResp.ok) results.updated++;
        else results.errors.push({{ nid, status: postResp.status }});
      }} catch (e) {{
        results.errors.push({{ nid, err: String(e) }});
      }}
    }}));
  }}
  return results;
}};

// 3. Upload Master Sitemap (sitemap-erx-master.txt) via CKFinder Files
window.erxUploadMasterSitemap = async function() {{
  const byteChars = atob(window.ERX_MASTER_SITEMAP_B64);
  const byteNumbers = new Array(byteChars.length);
  for (let i = 0; i < byteChars.length; i++) byteNumbers[i] = byteChars.charCodeAt(i);
  const blob = new Blob([new Uint8Array(byteNumbers)], {{ type: "text/plain" }});
  const fd = new FormData();
  fd.append("upload", blob, "sitemap-erx-master.txt");
  const resp = await fetch("/ckfinder/core/connector/aspx/connector.aspx?command=QuickUpload&type=Files&currentFolder=%2F", {{
    method: "POST",
    credentials: "include",
    body: fd
  }});
  const txt = await resp.text();
  return {{ ok: resp.ok, url: "https://erx.vn/Media/files/sitemap-erx-master.txt", respPreview: txt.slice(0, 200) }};
}};

// 4. Update META.SCRIPT_HEADER with Head SEO & Valid Schema.org Graph + Restore SYS.MENU_DEFAULT=578
window.erxUpgradeHeaderAndRestoreHome = async function() {{
  const siteUrl = "/administrator/globalconfiguration/site?from=3&divid=100";
  const resp = await fetch(siteUrl, {{ credentials: "include" }});
  const html = await resp.text();
  const doc = new DOMParser().parseFromString(html, "text/html");
  const form = doc.querySelector("form");
  if (!form) return {{ ok: false, err: "No site form" }};

  const fd = window.erxSerializeForm(form);
  let sh = fd.get("META.SCRIPT_HEADER") || "";
  sh = sh.replace(/<script id="erx-seo-schema-upgrader">[\\s\\S]*?<\\/script>/g, "");
  sh += "\\n" + window.ERX_HEAD_SEO_SCHEMA_SCRIPT;
  fd.set("META.SCRIPT_HEADER", sh);
  fd.set("btnSubmit", "save");

  const saveSite = await fetch(siteUrl, {{
    method: "POST",
    credentials: "include",
    headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
    body: fd.toString()
  }});

  // Immediately re-save SYS.MENU_DEFAULT = 578 & SYS.MENU_HOME = 578 so homepage routing never resets
  const sysUrl = "/administrator/globalconfiguration/sytem?from=102&divid0=100&divid=100";
  const sysResp = await fetch(sysUrl, {{ credentials: "include" }});
  const sysHtml = await sysResp.text();
  const sysDoc = new DOMParser().parseFromString(sysHtml, "text/html");
  const sysForm = sysDoc.querySelector("form");
  let sysOk = false;
  if (sysForm) {{
    const sysFd = window.erxSerializeForm(sysForm);
    sysFd.set("SYS.MENU_DEFAULT", "578");
    sysFd.set("SYS.MENU_HOME", "578");
    sysFd.set("btnSubmit", "save");
    const saveSys = await fetch(sysUrl, {{
      method: "POST",
      credentials: "include",
      headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
      body: sysFd.toString()
    }});
    sysOk = saveSys.ok;
  }}

  return {{ siteOk: saveSite.ok, sysHomeRestored: sysOk }};
}};

window.erxRunAllSeoUpgrades = async function() {{
  const menus = await window.erxUpgradeAllMenusSeo();
  const articles = await window.erxUpgradeArticlesSeo();
  const sitemap = await window.erxUploadMasterSitemap();
  const header = await window.erxUpgradeHeaderAndRestoreHome();
  return {{ menus, articles, sitemap, header }};
}};
""".strip()

OUT_JS.write_text(js_code, encoding="utf-8")
print(f"Wrote {OUT_JS} ({OUT_JS.stat().st_size:,} bytes)")
