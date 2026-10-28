# -*- coding: utf-8 -*-
"""
Compiles D:\\GIT\\SEO Tool\\pm_assets\\erx_legacy_upgrader.js
which upgrades all 107 legacy blog articles (712*) on https://erx.vn/administrator:
1. Populates / standardizes INTROTEXT_1 (220-350 chars) and META_DESCRIPTION for all 107 articles.
2. Upgrades META.SCRIPT_HEADER with .erx-code-block, .erx-code-header, .erx-code-pre, and .erx-inline-code styles + runtime DOM sanitizer.
3. Transforms FULLTEXT_1 across all 107 legacy articles:
   - Strips 1.1 MB of raw JupyterLab <style> bloat in 7122438204 and 7122491878.
   - Promotes bold numbered/step pseudo-headings into semantic <h2> and <h3> tags.
   - Converts standalone Excel formulas (=SUM, =SCAN, =FILTER, =TRIM, etc.), SQL queries, VBA blockquotes/code, DAX measures, and Python snippets into styled .erx-code-block cards.
   - Wraps inline function names and keywords in <code class="erx-inline-code">.
   - Appends curated deep-dive technical sections (syntax tables, advanced formula cards, error troubleshooting) to thin/incomplete articles, and replaces the placeholder 'test' body of 7122169949.
"""
import json
import re
from pathlib import Path

AUDIT_PATH = Path(r"D:\GIT\SEO Tool\pm_assets\sitemap_articles_audit.json")
OUT_JS_PATH = Path(r"D:\GIT\SEO Tool\pm_assets\erx_legacy_upgrader.js")

with open(AUDIT_PATH, "r", encoding="utf-8") as f:
    audit_data = json.load(f)

pm_ids = {
    "7124047589", "7124054453", "7124068075", "7124079199",
    "7124088613", "7124095185", "7124108707", "7124156882"
}

legacy_items = {}
for d in audit_data:
    nid = d.get("nid", "")
    if nid.startswith("712") and nid not in pm_ids and int(nid) < 7124040000:
        legacy_items[nid] = d

# Curated 220-350 char INTROTEXT_1 for all legacy articles needing intro fixes or standardization
CURATED_INTROS = {
    "7121823513": "Khám phá 7 sự cố sai lệch bảng tính Excel kinh điển từng khiến các tập đoàn tài chính như JPMorgan Chase, Fidelity và Barclays thiệt hại hàng tỷ USD, cùng giải pháp kiểm soát toàn vẹn dữ liệu doanh nghiệp.",
    "7121832835": "Tổng hợp các tính năng cốt lõi của lập trình VBA (Visual Basic for Applications) trong Excel: từ ghi Macro tự động, xây dựng hàm tùy chỉnh UDF đến tự động hóa quy trình báo cáo doanh nghiệp chỉ với 1 cú nhấp chuột.",
    "7121866391": "Hướng dẫn lộ trình làm chủ lập trình VBA trong Excel dành cho người đi làm: cách tư duy hướng đối tượng (Workbook, Worksheet, Range), viết câu lệnh Macro sạch và tự động hóa các tác vụ xử lý dữ liệu lặp lại hàng ngày.",
    "7122096748": "Hướng dẫn chi tiết cách tích hợp Google Maps Distance Matrix API vào Excel VBA để tự động tính chính xác quãng đường (km) và thời gian vận chuyển giữa hàng trăm điểm giao nhận trong quản trị Logistics.",
    "7122103947": "Giải pháp tra cứu siêu tốc khoảng cách (km) giữa 2 địa điểm bất kỳ bằng Ma trận vuông (Distance Matrix) trong Excel, giúp bộ phận Logistics và Mua hàng lập dự toán cước vận tải mà không phụ thuộc vào API trả phí.",
    "7122114672": "Tổng quan thực chiến về Quản trị Vận hành Logistics (Logistics Operations): quy trình xuất nhập khẩu, quản lý vận tải nội địa, tối ưu hóa chi phí kho bãi và kiểm soát chứng từ chuỗi cung ứng tại doanh nghiệp.",
    "7122144092": "Tìm nguồn cung ứng chiến lược (Strategic Sourcing) là gì? Phân tích quy trình 7 bước kết nối phân tích chi tiêu (Spend Analysis), nghiên cứu thị trường, đàm phán nhà cung cấp và tối ưu tổng chi phí sở hữu (TCO).",
    "7122169949": "Hướng dẫn toàn diện cách sử dụng ngôn ngữ truy vấn SQL ngay trong Microsoft Excel thông qua kết nối ADODB: giải pháp tổng hợp hàng trăm nghìn dòng dữ liệu từ nhiều file Excel và tự động hóa báo cáo chỉ với 1 cú click.",
    "7122293947": "Cẩm nang toàn diện về mã HS Code (Harmonized System Codes) trong xuất nhập khẩu: cấu trúc phân loại 6-8 chữ số của WCO, quy tắc áp mã chuẩn xác và cách tính thuế nhập khẩu ưu đãi cho doanh nghiệp Logistics.",
    "7122305017": "Bài toán Tối ưu hóa Tuyến đường (Vehicle Routing Problem - VRP) trong Logistics: nguyên lý giải thuật tìm đường đi ngắn nhất giúp doanh nghiệp phân phối cắt giảm 15–25% chi phí nhiên liệu và thời gian giao hàng.",
    "7122332290": "Thủ thuật lập trình Excel VBA thực chiến: Hướng dẫn cú pháp và cách ứng dụng hàm IsNumeric() kết hợp vòng lặp để kiểm tra, xác thực kiểu dữ liệu số (Numeric) trên bảng tính trước khi tính toán tự động.",
    "7122399614": "Hướng dẫn cú pháp và cách viết câu lệnh SQL SELECT ngay trong Excel VBA (ADODB): kỹ thuật truy vấn cột chỉ định, đặt bí danh (Alias), loại bỏ dòng trùng lặp với DISTINCT và lấy Top N dòng dữ liệu siêu tốc.",
    "7122417941": "Quy trình 8 bước chuẩn mực để thiết lập kết nối ADODB.Connection và thực thi câu lệnh truy vấn SQL trực tiếp trong Excel VBA, giúp trích xuất và làm sạch hàng trăm nghìn dòng dữ liệu chỉ trong vài giây.",
    "7122425785": "Giới thiệu công cụ Tối ưu hóa Tuyến đường (Route Optimization) trên nền tảng Excel do ERX phát triển: tự động giải bài toán định tuyến giao hàng đa điểm, giảm thiểu quãng đường di chuyển và chi phí vận tải.",
    "7122438204": "Hướng dẫn thực hành thư viện Pandas trong Python để khám phá dữ liệu (Exploratory Data Analysis - EDA): cách đọc file Excel/CSV, kiểm tra cấu trúc DataFrame, lọc dữ liệu đa điều kiện và thống kê mô tả.",
    "7122466307": "Tối ưu hóa lộ trình lấy hàng trong kho (Warehouse Order Picking Routing): phân tích các chiến lược S-Shape, Return, Midpoint, Largest Gap và ứng dụng thuật toán giảm thiểu thời gian di chuyển nhân sự kho.",
    "7122477609": "Tổng hợp 7 nền tảng và website học lập trình phân tích dữ liệu (Excel VBA, SQL, Python, R, Power BI) uy tín nhất thế giới giúp chuyên viên Supply Chain và Data Analyst nâng cấp kỹ năng tự động hóa báo cáo.",
    "7122491878": "Làm chủ hàm GroupBy trong thư viện Python Pandas theo cơ chế Split-Apply-Combine: hướng dẫn cách gom nhóm dữ liệu bán hàng, tính tổng doanh thu, trung bình, đếm số đơn và tạo bảng tổng hợp đa chiều siêu tốc.",
    "7122518308": "Hướng dẫn sử dụng Google Colab từ A-Z cho người mới bắt đầu học Python và Phân tích dữ liệu: môi trường Jupyter Notebook miễn phí trên đám mây của Google, không cần cài đặt cấu hình máy tính phức tạp.",
    "7122529576": "Làm chủ cấu trúc rẽ nhánh điều kiện (if - elif - else) và vòng lặp (for, while) trong ngôn ngữ lập trình Python kèm ví dụ minh họa trực quan về tự động hóa xử lý dữ liệu chuỗi cung ứng và tài chính.",
    "7122657559": "Phân biệt rõ vai trò và sức mạnh của bộ ba công cụ Business Intelligence từ Microsoft: Power Query (ETL & làm sạch dữ liệu), Power Pivot (Data Modeling & DAX) và Power BI (Trực quan hóa Dashboard quản trị).",
    "7122675302": "Hướng dẫn kỹ thuật thiết kế biểu đồ cột (Column Chart) chuyên nghiệp trong Excel: 5 nguyên tắc trình bày dữ liệu trực quan, cách tùy chỉnh trục tọa độ, nhãn dữ liệu (Data Labels) và màu sắc chuẩn báo cáo quản trị.",
    "7122684703": "Trọn bộ bí kíp làm chủ hàm VLOOKUP trong Excel từ cơ bản đến nâng cao: cú pháp dò tìm chính xác vs tương đối, cách kết hợp hàm MATCH/CHOOSE để dò tìm đa chiều và khắc phục triệt để lỗi #N/A.",
    "7122694446": "Hướng dẫn bộ 3 hàm tách chuỗi văn bản thế hệ mới trong Excel 365 gồm TEXTSPLIT, TEXTBEFORE và TEXTAFTER: giải pháp thay thế hoàn hảo cho tổ hợp LEFT/MID/RIGHT/FIND phức tạp chỉ bằng 1 công thức mảng động.",
    "7122706843": "Nâng cấp kỹ năng tự động hóa báo cáo trên Excel bằng sự kết hợp giữa ngôn ngữ truy vấn SQL (ADODB) và lập trình VBA: trích xuất dữ liệu liên file, tổng hợp đa điều kiện và xuất báo cáo động chỉ trong 1 giây.",
    "7122712685": "Hướng dẫn từng bước cách ứng dụng ngôn ngữ SQL ngay trên nền tảng Microsoft Excel để truy vấn, gom nhóm và tạo báo cáo tổng hợp dữ liệu lớn siêu tốc mà không làm nặng file hay treo bảng tính.",
    "7122722851": "Hướng dẫn tạo và quản lý danh sách tùy chỉnh (Custom List) trong Microsoft Excel, giúp tự động điền nhanh danh mục phòng ban, mã kho, chi nhánh và sắp xếp dữ liệu (Custom Sort) theo đúng thứ tự ưu tiên nghiệp vụ.",
    "7122733141": "Khám phá tính năng Paste Special – Skip Blanks trong Microsoft Excel: giải pháp cập nhật và hợp nhất dữ liệu giữa hai cột nhanh chóng mà không làm các ô trống (Blank Cells) ghi đè mất dữ liệu gốc quan trọng.",
    "7122807028": "Hướng dẫn cài đặt và sử dụng Jupyter Notebook (qua Anaconda) cho người mới bắt đầu phân tích dữ liệu với Python: làm chủ hệ thống phím tắt, Markdown trình bày báo cáo và thực thi từng khối lệnh trực quan.",
    "7122812051": "Làm quen với thư viện Pandas và cấu trúc dữ liệu DataFrame trong Python: hướng dẫn cách khởi tạo bảng dữ liệu 2 chiều, truy xuất dòng/cột bằng loc/iloc, xử lý giá trị khuyết thiếu (NaN) và xuất báo cáo Excel.",
    "7122834639": "Bài mở đầu chuỗi thực hành SQL & VBA trong Excel: hướng dẫn chi tiết cách bật thanh công cụ Developer, cấu hình bảo mật Macro, làm quen cửa sổ lập trình VBE (Alt + F11) và chuẩn bị dữ liệu chuẩn Database.",
    "7122847956": "Phân tích chi tiết cấu trúc 8 bước thiết lập kết nối ADODB trong Excel VBA và cách viết câu lệnh truy vấn SELECT cơ bản để trích xuất dữ liệu từ Sheet Excel hoặc Access Database sang bảng báo cáo.",
    "7122905369": "Hướng dẫn lập trình VBA thao tác với đối tượng Workbook trong Excel (Phần 1): cách tham chiếu Workbooks theo tên hoặc chỉ số, kiểm tra đường dẫn và tự động mở/đóng nhiều file dữ liệu bằng câu lệnh Workbooks.Open.",
    "7122913368": "Hướng dẫn lập trình VBA thao tác với đối tượng Workbook trong Excel (Phần 2): phân biệt các định dạng lưu trữ (.xlsx, .xlsm, .xlsb, .xls) và tự động hóa quy trình tạo mới, lưu trữ (Save/SaveAs) file báo cáo.",
    "7122926210": "Nghệ thuật thuyết phục dựa trên khoa học hành vi trong môi trường doanh nghiệp: cách tháo gỡ 5 rào cản tâm lý (Quán tính, Sự không chắc chắn, Phản kháng) để bảo vệ đề xuất dự án và chiến lược chuỗi cung ứng.",
    "7122939679": "Chiến lược đàm phán mua hàng khi đối mặt với các nhà cung cấp độc quyền hoặc nắm quyền lực chi phối thị trường: 6 đòn bẩy chiến thuật từ bài học Harvard Business Review giúp bộ phận Procurement xoay chuyển thế cờ.",
    "7122975038": "Làm chủ bộ tứ mệnh đề cốt lõi trong SQL gồm WHERE (lọc dữ liệu gốc), GROUP BY (gom nhóm thống kê), HAVING (lọc sau gom nhóm) và ORDER BY (sắp xếp thứ tự) khi truy vấn dữ liệu báo cáo trên Excel VBA.",
    "7122985392": "Hướng dẫn sử dụng ký tự đại diện (Wildcard: %, _, []) kết hợp toán tử LIKE, BETWEEN, IN và NOT trong SQL Excel (ADODB) để lọc dữ liệu văn bản gần đúng và truy vấn mã vật tư, khách hàng linh hoạt.",
    "7123094250": "Nghiên cứu chuyên sâu về Hành vi Mua hàng Công nghiệp (Industrial Buying Behavior): phân tích động lực kinh tế, ma trận rủi ro, cấu trúc trung tâm mua sắm (Buying Center) và quy trình ra quyết định B2B.",
    "7123107285": "Tổng hợp các thao tác kỹ thuật quan trọng khi viết câu lệnh SQL trong Excel VBA: cách nối chuỗi câu truy vấn dài trên nhiều dòng bằng ký tự gạch dưới (_), truyền biến động từ ô Excel và xử lý ngày tháng/chuỗi.",
    "7123117353": "Hướng dẫn toàn diện về câu lệnh JOIN trong SQL Excel (INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN): giải pháp kết nối dữ liệu từ nhiều bảng và nhiều file Excel thay thế hoàn hảo cho hàm VLOOKUP chậm chạp.",
    "7123166602": "Hướng dẫn 3 cách gỡ chặn (Unblock) triệt để lỗi bảo mật 'Microsoft has blocked macros from running because the source of this file is untrusted' trên Office 365 và Excel 2021 khi tải file chứa code VBA từ Internet.",
    "7123179255": "Nâng cao kỹ năng truy vấn SQL trong Excel VBA với 3 kỹ thuật thực chiến: hàm điều kiện IIF() thay thế IF lồng nhau, truy vấn con (Subquery) xử lý logic đa tầng và cách xác định dòng cuối động (LastRow).",
    "7123183520": "Hướng dẫn nhóm câu lệnh thao tác dữ liệu (DML) gồm INSERT INTO (chèn thêm dòng/bảng mới), UPDATE SET (cập nhật hàng loạt theo điều kiện) và DELETE (xóa dữ liệu) trực tiếp trên file Excel bằng SQL VBA.",
    "7123199704": "Cẩm nang toàn diện về thư viện ADO (ActiveX Data Objects) trong Excel VBA: kiến trúc Connection – Command – Recordset, chuỗi kết nối ConnectionString chuẩn cho Excel/Access/SQL Server và tối ưu tốc độ truy vấn.",
    "7123203445": "Phân tích Hành vi Mua hàng Công nghiệp (Phần 1): Khám phá các yếu tố kinh tế vĩ mô, áp lực tối ưu chi phí – chất lượng – tiến độ giao hàng và cách hệ thống KPI định hình quyết định của giám đốc thu mua.",
    "7123214977": "Phân tích Hành vi Mua hàng Công nghiệp (Phần 2):Hệ thống thước đo hiệu suất mua sắm (Purchasing Metrics), sự giằng co giữa rủi ro đứt gãy nguồn cung và mục tiêu tiết giảm giá vốn của bộ phận Procurement.",
    "7123229334": "Ứng dụng ngôn ngữ SQL trong Excel để xây dựng hệ thống Báo cáo Nhân sự (HR Analytics) siêu tốc: tự động đối chiếu ngân sách lương kế hoạch (Planning) và chi phí thực tế (Actual) từ nhiều phòng ban.",
    "7123298087": "Phân tích Hành vi Mua hàng Công nghiệp (Phần 3): Vai trò và mức độ ảnh hưởng của các phòng ban chức năng (R&D, Kỹ thuật, Sản xuất, Tài chính) qua từng giai đoạn trong quy trình mua sắm doanh nghiệp.",
    "7123307629": "Phân tích Hành vi Mua hàng Công nghiệp (Phần 4 - Cuối): So sánh mô hình tổ chức mua hàng Tập trung (Centralized) vs Phân quyền (Decentralized) và cách thiết kế cơ cấu Thu mua hỗn hợp cho tập đoàn đa ngành.",
    "7123319953": "8 phương pháp cắt giảm chi phí mua hàng (Cost Reduction & Cost Avoidance) thực chiến trong Quản trị Mua sắm (Phần 1): cách đo lường lợi ích tài chính từ đàm phán giá, chiết khấu sản lượng và tối ưu điều khoản thanh toán.",
    "7123329099": "Các phương pháp tính toán lợi ích cắt giảm chi phí mua hàng (Phần 2): tối ưu hóa thông số kỹ thuật (Value Engineering), chuẩn hóa vật tư, hợp nhất nhà cung cấp và cải tiến quy trình vận hành chuỗi cung ứng.",
    "7123331425": "Case Study ứng dụng lập trình Python vào bài toán Hoạch định Nhu cầu Nguyên vật liệu (MRP): tự động rà soát BOM, đối chiếu tồn kho thực tế và xác định chính xác thời điểm thiếu hụt vật tư sản xuất.",
    "7123346478": "Khám phá khung chương trình đào tạo Cử nhân Quản trị Mua hàng & Logistics (Procurement & Logistics) chuẩn quốc tế tại Phần Lan (Phần 1): mục tiêu năng lực, cấu trúc học phần nhà máy tương lai và quản lý vận tải.",
    "7123352633": "Khám phá chương trình đào tạo Procurement & Logistics chuẩn quốc tế tại Phần Lan (Phần 2): chi tiết các học phần Quản trị Intralogistics, Tự động hóa kho hàng, Mua sắm chiến lược và Phân tích dữ liệu chuỗi cung ứng.",
    "7123374265": "Phân biệt chuyên sâu giữa Calculated Columns (Cột tính toán) và Measures (Thước đo động) trong ngôn ngữ DAX Power BI: nguyên lý Row Context vs Filter Context, mức tiêu thụ bộ nhớ RAM (VertiPaq) và quy tắc chọn đúng.",
    "7123388955": "Hướng dẫn kỹ thuật gộp dữ liệu đa bảng theo chiều dọc bằng toán tử UNION / UNION ALL và xoay bảng tổng hợp chéo (Cross-tab) bằng câu lệnh TRANSFORM ... PIVOT trong SQL Excel VBA.",
    "7123397941": "Tổng quan chương trình đào tạo đại học ngành Procurement & Logistics quốc tế (Phần 3): phát triển kỹ năng giao tiếp thương lượng đa văn hóa, quản trị dự án chuỗi cung ứng và ứng dụng hệ thống ERP/SAP thực chiến.",
    "7123407300": "Hướng dẫn 2 phương pháp chuẩn mực tạo bảng lịch (Date Table / Calendar Dimension) tự động trong Power BI bằng hàm DAX (CALENDAR, CALENDARAUTO) và ngôn ngữ M trong Power Query phục vụ phân tích Time Intelligence.",
    "7123413948": "Ứng dụng mô hình Phân tích Tổng chi phí sở hữu (Total Cost of Ownership - TCO) trong kỷ nguyên Công nghiệp 4.0: phương pháp đánh giá toàn diện chi phí mua sắm, vận hành, bảo trì và rủi ro thiết bị công nghiệp.",
    "7123424362": "Phân tích tác động địa chính trị từ cuộc xung đột Nga – Ukraine và xu hướng tái cấu trúc chuỗi cung ứng toàn cầu: sự chuyển dịch từ Just-In-Time (JIT) sang chiến lược Đa dạng hóa nguồn cung (China+1, Nearshoring).",
    "7123516261": "Phân tích ưu nhược điểm giữa xử lý báo cáo bằng công thức Excel thuần túy và truy vấn SQL ngay trên Excel: khi nào doanh nghiệp nên nâng cấp lên SQL VBA để giải quyết triệt để tình trạng treo file dữ liệu lớn?",
    "7123526928": "Chiến lược Tìm nguồn cung ứng (Strategic Sourcing) trong bối cảnh thị trường cạnh tranh siêu giảm giá: cách các tập đoàn bán lẻ tái cấu trúc danh mục nhà cung cấp để cắt giảm giá vốn hàng bán (COGS) bền vững.",
    "7123543392": "Giải quyết bài toán xác định Lịch thanh toán (Payment Schedule) tự động trong doanh nghiệp bằng 2 phương pháp: tổ hợp hàm mảng Excel nâng cao và thuật toán vòng lặp VBA tốc độ cao.",
    "7123554595": "Giải mã cơ chế hoạt động ngầm của hàm COUNTIFS trong Excel khi đếm các chuỗi số dài trên 15 ký tự (mã vận đơn, số tài khoản, CCCD) và cách khắc phục triệt để lỗi đếm sai do giới hạn độ chính xác 15 chữ số.",
    "7123563926": "Lộ trình 11 bước làm chủ Microsoft Excel từ cơ bản đến chuyên gia phân tích dữ liệu: từ điều hướng giao diện, phím tắt tốc độ, hàm dò tìm/thống kê, PivotTable đến biểu đồ động và tự động hóa quy trình.",
    "7123572446": "Thủ thuật Power BI DAX thực chiến: Hướng dẫn cách viết Measure kiểm tra dữ liệu phát sinh để đồng bộ hóa Slicer (Sync Slicers), giúp ẩn tự động các mục rỗng không có doanh thu trong kỳ báo cáo.",
    "7123607639": "Phân biệt chuyên sâu hai hàm quản lý ngữ cảnh lọc quan trọng nhất trong Power BI DAX là ALL() và ALLSELECTED(): hiểu rõ Internal Filter vs External Filter để tính tỷ trọng phần trăm (% of Total) chính xác tuyệt đối.",
    "7123612988": "Hướng dẫn chi tiết cách tải, cài đặt và kích hoạt Add-in Đổi số thành chữ tiếng Việt (VNĐ / USD) tự động trong Microsoft Excel, giúp kế toán và mua hàng lập báo giá, hợp đồng, phiếu thu chi nhanh chóng.",
    "7123622137": "Hướng dẫn kỹ thuật tính tổng dữ liệu tự động bỏ qua cả dòng ẩn (Hidden Rows) lẫn cột ẩn (Hidden Columns) trong Excel bằng sự kết hợp giữa hàm SUBTOTAL(109,...), AGGREGATE và hàm tự tạo VBA (UDF).",
    "7123638572": "Hướng dẫn kỹ thuật vẽ Biểu đồ Cột động tự động tô màu nổi bật (Highlight) Top N giá trị lớn nhất hoặc nhỏ nhất trong Excel kết hợp hàm LARGE, IF và thanh trượt Form Control chuyên nghiệp.",
    "7123642222": "Tổng hợp 6 phương pháp đánh số thứ tự tự động trong Excel: từ hàm ROW, SUBTOTAL(103,...), AGGREGATE giữ nguyên thứ tự khi lọc dữ liệu (Filter) đến hàm mảng động SEQUENCE trong Excel 365.",
    "7123653300": "Hướng dẫn kỹ thuật sử dụng công thức mảng 3D (3D Reference) kết hợp hàm VSTACK và FILTER trong Excel 365 để tự động gộp và làm sạch dữ liệu từ hàng chục Sheet báo cáo về 1 Sheet Tổng hợp duy nhất.",
    "7123662758": "Hướng dẫn kỹ thuật tạo nhãn dữ liệu thông minh (Dynamic Data Labels) trên biểu đồ Excel: tự động hiển thị mũi tên tăng/giảm (▲/▼), phần trăm biến động và cảnh báo vượt ngưỡng KPI trực quan.",
    "7123673148": "Hướng dẫn cách viết công thức tính tổng doanh thu lũy kế động trong vòng N tháng bất kỳ trên Excel bằng tổ hợp hàm SUM, OFFSET, INDEX và SEQUENCE, giúp lập báo cáo Rolling Forecast linh hoạt.",
    "7123687467": "Hướng dẫn chi tiết cách kết hợp hai hàm mảng động nâng cao SCAN và LAMBDA trong Excel 365 để tính lũy kế doanh thu (Sales To Date) và lũy kế đầu năm (Sales YTD) chỉ bằng 1 công thức tràn mảng tự động.",
    "7123694822": "Làm chủ hàm FILTER trong Excel 365 từ cơ bản đến nâng cao: cú pháp lọc dữ liệu động theo 1 điều kiện, kết hợp toán tử nhân (*) cho điều kiện VÀ (AND), toán tử cộng (+) cho điều kiện HOẶC (OR) và xử lý lỗi #CALC!.",
    "7123702834": "Hướng dẫn cách xử lý triệt để lỗi khoảng trắng cứng (Non-breaking space – mã ASCII 160) tải về từ Web/ERP mà hàm TRIM thông thường không xóa được, bằng công thức kết hợp TRIM, SUBSTITUTE và CHAR(160).",
    "7123716407": "Khám phá những tính năng mới đột phá nhất trên Microsoft Excel 365: trích xuất bảng dữ liệu trực tiếp từ hình ảnh (Data from Picture), gợi ý công thức bằng AI, thanh tìm kiếm thông minh và hệ sinh thái hàm mảng động.",
    "7123727669": "Hướng dẫn toàn diện về hàm TEXTSPLIT trong Excel 365: cách phân tách chuỗi văn bản phức tạp thành nhiều cột và nhiều dòng cùng lúc theo một hoặc nhiều ký tự phân cách (Delimiters) mà không cần dùng Text to Columns.",
    "7123734453": "Làm chủ hàm TEXTBEFORE trong Excel 365: cú pháp và ví dụ thực tế cách trích xuất nhanh phần văn bản đứng trước ký tự phân cách thứ N (từ trái sang phải hoặc từ phải sang trái) mà không cần dùng hàm LEFT và FIND.",
    "7123747108": "Làm chủ hàm TEXTAFTER trong Excel 365: hướng dẫn chi tiết cách trích xuất phần văn bản nằm sau ký tự hoặc từ khóa phân cách bất kỳ, xử lý chuỗi nhiều dấu phân cách và bẫy lỗi khi không tìm thấy ký tự.",
    "7123752471": "Hướng dẫn sử dụng hàm mảng động CHOOSECOLS trong Excel 365 để trích xuất, sắp xếp lại thứ tự hoặc lấy các cột bất kỳ từ bên phải bảng dữ liệu (với tham số âm) phục vụ báo cáo tự động.",
    "7123772334": "Hướng dẫn chi tiết hàm CHOOSEROWS trong Excel 365: cách trích xuất các dòng chỉ định, lấy N dòng cuối bảng bằng chỉ số âm, lọc các dòng chẵn/lẻ tự động kết hợp hàm SEQUENCE và đảo ngược thứ tự bảng dữ liệu.",
    "7123785419": "Hướng dẫn sử dụng hàm DROP trong Excel 365 để tự động loại bỏ N dòng hoặc N cột không cần thiết ở đầu hoặc cuối bảng dữ liệu mảng động, giúp làm sạch vùng dữ liệu báo cáo nhanh chóng.",
    "7123795336": "Làm chủ hàm TAKE trong Excel 365: cách trích xuất nhanh N dòng hoặc N cột liền kề từ đầu hoặc cuối bảng dữ liệu, kết hợp hàm SORT và FILTER để tạo báo cáo Top N sản phẩm/khách hàng tự động.",
    "7123806948": "Hướng dẫn sử dụng hàm EXPAND trong Excel 365 để mở rộng kích thước mảng dữ liệu hai chiều tới số dòng và số cột chỉ định, giúp đồng bộ kích thước các bảng trước khi gộp bằng VSTACK/HSTACK.",
    "7123816032": "Cẩm nang toàn diện về hàm LAMBDA trong Excel 365: cách tự định nghĩa hàm tùy chỉnh (Custom Function) ngay bằng công thức bảng tính mà không cần viết VBA, kèm quy trình kiểm thử và đặt tên trong Name Manager.",
    "7123826123": "Hướng dẫn sử dụng hàm TOCOL trong Excel 365 để chuyển đổi bảng dữ liệu nhiều dòng nhiều cột (2D Range) thành một cột duy nhất, tự động bỏ qua ô trống và các ô lỗi chỉ bằng 1 tham số.",
    "7123837426": "Hướng dẫn chi tiết hàm TOROW trong Excel 365: cách chuyển đổi một vùng dữ liệu đa chiều thành một hàng ngang duy nhất (quét theo hàng hoặc theo cột), kết hợp loại bỏ ô trống và giá trị lỗi tự động.",
    "7123848940": "Hướng dẫn cách hợp nhất nhiều bảng dữ liệu theo chiều dọc và chiều ngang trong Excel 365 bằng bộ đôi hàm mảng động VSTACK và HSTACK, kèm kỹ thuật xử lý lỗi #N/A khi các bảng khác kích thước.",
    "7123852851": "Làm chủ hai hàm định hình lại mảng dữ liệu WRAPROWS và WRAPCOLS trong Excel 365: cách chuyển đổi danh sách 1 chiều (1 cột hoặc 1 hàng) thành bảng dữ liệu 2 chiều có số cột/dòng cố định.",
    "7123869202": "Giới thiệu bộ công cụ Add-in ERX Smart Tool dành cho Microsoft Excel: giải pháp tự động hóa đối chiếu dữ liệu, chuẩn hóa danh mục vật tư MRO, tách gộp file báo cáo và tăng tốc công việc cho chuyên viên Supply Chain.",
    "7123873942": "Hướng dẫn viết công thức DAX trong Power BI để so sánh biến động doanh thu giữa 2 mốc thời gian bất kỳ do người dùng tùy chọn trên 2 Slicer độc lập (Disconnected Date Tables) phục vụ Dashboard quản trị.",
    "7123889385": "Kỹ thuật mô hình hóa dữ liệu trong Power BI: cách sử dụng bảng phân nhóm động (Disconnected Segmentation Table) kết hợp hàm DAX thay thế cho các câu lệnh IF/SWITCH lồng nhau phức tạp.",
    "7123893660": "Ngôn ngữ DAX (Data Analysis Expressions) trong Power BI, Excel Power Pivot và SSAS là gì? Giải thích toàn diện về cú pháp, các nhóm hàm cốt lõi, ngữ cảnh tính toán (Evaluation Context) và lộ trình học DAX hiệu quả.",
    "7123909199": "Hướng dẫn từng bước cách xây dựng Biểu đồ Phân tích Pareto (Quy tắc 80/20) trong Power BI bằng công thức DAX (RANKX, CALCULATE, ALLSELECTED, TOPN), giúp nhận diện 20% sản phẩm/khách hàng mang lại 80% doanh thu.",
    "7123912837": "Hướng dẫn nâng cao tính toàn vẹn dữ liệu trên Excel 365 thông qua việc đóng gói công thức phức tạp thành Hàm tùy chỉnh (Custom Function) bằng hàm LAMBDA và Name Manager cho toàn bộ Workbook.",
    "7123946893": "Thông tin tuyển dụng vị trí Trợ lý Kinh doanh (Sales Admin / Business Assistant) tại Công ty Thiết bị Công nghiệp & Tự động hóa Song Nguyên: mô tả công việc quản lý đơn hàng, báo giá, hợp đồng và chế độ đãi ngộ.",
    "7123956328": "Cơ hội nghề nghiệp vị trí Phó phòng Mua hàng & Logistics (Deputy Purchasing and Logistics Team Leader): phụ trách hoạt động mua hàng quốc tế, đàm phán nhà cung cấp chiến lược và tối ưu hóa vận hành xuất nhập khẩu.",
    "7123968182": "Cơ hội nghề nghiệp vị trí Trưởng phòng Chuỗi Cung Ứng (Supply Chain Manager): điều hành toàn diện quy trình xử lý đơn hàng, hoạch định nhu cầu (Demand Planning), thu mua, kho vận và tối ưu hiệu suất tồn kho.",
    "7123976602": "Thông tin tuyển dụng vị trí Chuyên viên Chính Quy trình Logistics (Lead Logistics Process Specialist): quản lý quy trình đặt chỗ xuất nhập khẩu (Booking), kiểm soát SLA, hải quan và tối ưu hóa vận hành chuỗi cung ứng.",
    "7123986505": "Thông tin tuyển dụng vị trí Chuyên viên Mua hàng Nguyên vật liệu trực tiếp & Năng lượng (Procurement Specialist – Direct Material): quản lý tìm nguồn cung ứng (Sourcing), đấu thầu, đàm phán hợp đồng và phát triển nhà cung cấp.",
    "7123995135": "Phân biệt chính xác các cặp thuật ngữ dễ gây nhầm lẫn nhất trong Quản trị Mua hàng & Chuỗi cung ứng: Procurement vs Purchasing, Supplier vs Vendor, Direct vs Indirect Spend, Cost Reduction vs Cost Avoidance.",
    "7124009517": "Bài học thực chiến về Chuẩn hóa Dữ liệu Danh mục Vật tư (MRO Master Data) trong Mua hàng và Chuỗi cung ứng: cách ứng dụng thuật toán tương đồng ngôn ngữ để xử lý hàng nghìn mã vật tư trùng lặp và sai lệch quy cách.",
    "7124011913": "Giải pháp thiết kế Layout kho hàng theo phương pháp Phân tích ABC đa chiều: tối ưu hóa vị trí lưu trữ hàng hóa theo tần suất xuất nhập, giảm 30–40% quãng đường lấy hàng (Picking) và nâng cao hiệu suất vận hành kho.",
    "7124024944": "Case Study Harvard Business School về Pactum AI tại Walmart & Maersk: Cách Trí tuệ Nhân tạo Tự hành (Autonomous AI Negotiation) đàm phán hợp đồng đồng thời với hàng chục nghìn nhà cung cấp và tạo giá trị đôi bên cùng có lợi."
}

# Full replacement HTML for 7122169949 (which currently has only 'test' in FULLTEXT_1)
REPLACEMENT_7122169949 = """
<h2>1. Tại sao nên ứng dụng ngôn ngữ SQL ngay trong Microsoft Excel?</h2>
<p>Khi quy mô dữ liệu doanh nghiệp vượt ngưỡng <strong>50.000 – 500.000 dòng</strong> hoặc phân tán trên hàng chục file Excel theo từng tháng/chi nhánh, các công thức dò tìm và tổng hợp truyền thống như <code class="erx-inline-code">VLOOKUP</code>, <code class="erx-inline-code">SUMIFS</code>, <code class="erx-inline-code">COUNTIFS</code> hay <code class="erx-inline-code">INDEX/MATCH</code> thường khiến bảng tính bị treo cứng (<em>Not Responding</em>) và tốn nhiều phút để tính toán lại (Recalculate).</p>
<p>Giải pháp đột phá được các chuyên gia Phân tích Dữ liệu tại <strong>ERX Việt Nam</strong> triển khai là <strong>kết hợp ngôn ngữ truy vấn SQL (Structured Query Language) trực tiếp bên trong Excel thông qua thư viện ADODB (ActiveX Data Objects)</strong>. Phương pháp này biến mỗi Sheet hoặc mỗi file Excel đóng (Closed Workbook) thành một bảng cơ sở dữ liệu (Database Table) thực thụ:</p>
<ul>
  <li><strong>Tốc độ xử lý siêu tốc:</strong> Tổng hợp, lọc đa điều kiện và nối (<code class="erx-inline-code">JOIN</code>) 200.000 dòng dữ liệu từ 12 file Excel chỉ trong <strong>1 – 2 giây</strong>.</li>
  <li><strong>Không làm phình dung lượng file báo cáo:</strong> Không cần lưu hàng triệu công thức trên ô tính; file báo cáo chỉ nhận kết quả cuối cùng từ bộ nhớ đệm <code class="erx-inline-code">ADODB.Recordset</code>.</li>
  <li><strong>Truy vấn trực tiếp từ các file Excel đang đóng:</strong> Không cần mở từng file nguồn, giúp tự động hóa hoàn toàn báo cáo quản trị chỉ bằng <strong>1 cú nhấp chuột (1-Click Reporting)</strong>.</li>
</ul>

<h2>2. So sánh hiệu năng: Công thức Excel truyền thống vs. SQL trong Excel (ADODB)</h2>
<div class="table-responsive">
  <table>
    <thead>
      <tr>
        <th>Tiêu chí đánh giá</th>
        <th>Công thức Excel thuần (<code class="erx-inline-code">VLOOKUP</code> / <code class="erx-inline-code">SUMIFS</code>)</th>
        <th>Truy vấn SQL trong Excel (<code class="erx-inline-code">ADODB</code>)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Tốc độ với 100.000+ dòng</strong></td>
        <td>Chậm (30 giây – vài phút), dễ treo máy khi lọc hoặc chèn dòng.</td>
        <td><strong>Siêu tốc (0.5 – 2 giây)</strong> nhờ cơ chế xử lý tập hợp (Set-based Engine).</td>
      </tr>
      <tr>
        <td><strong>Lấy dữ liệu từ nhiều file đóng</strong></td>
        <td>Rất khó, công thức liên kết ngoài dễ bị lỗi <code class="erx-inline-code">#REF!</code> hoặc <code class="erx-inline-code">#VALUE!</code>.</td>
        <td>Truy vấn trực tiếp qua đường dẫn file mà <strong>không cần mở file nguồn</strong>.</td>
      </tr>
      <tr>
        <td><strong>Nối nhiều bảng (Multi-Table Join)</strong></td>
        <td>Phải tạo nhiều cột phụ trung gian làm nặng bảng tính.</td>
        <td>Nối trực tiếp 3–5 bảng bằng <code class="erx-inline-code">LEFT JOIN</code>, <code class="erx-inline-code">INNER JOIN</code>, <code class="erx-inline-code">UNION ALL</code>.</td>
      </tr>
      <tr>
        <td><strong>Tính bảo mật &amp; Toàn vẹn công thức</strong></td>
        <td>Người dùng dễ vô tình xóa hoặc sửa nhầm công thức trên ô.</td>
        <td>Toàn bộ logic nằm an toàn trong câu lệnh SQL, trả về giá trị thuần.</td>
      </tr>
    </tbody>
  </table>
</div>

<h2>3. Cấu trúc 8 bước chuẩn thiết lập câu lệnh SQL trong Excel VBA</h2>
<p>Để thực thi một câu truy vấn SQL ngay trong Excel (mà không cần cài đặt thêm SQL Server hay phần mềm bên ngoài), chúng ta sử dụng trình điều khiển <strong>Microsoft ACE OLEDB 12.0</strong> có sẵn trong bộ Microsoft Office theo khung mẫu chuẩn 8 bước dưới đây:</p>
<div class="erx-code-block">
  <div class="erx-code-header"><span>MÃ NGUỒN VBA + SQL</span><span>Excel ADODB Standard Template</span></div>
  <pre class="erx-code-pre">Sub Chay_Bao_Cao_SQL_Sieu_Toc()
    ' Bước 1 &amp; 2: Khai báo và khởi tạo đối tượng Connection &amp; Recordset
    Dim cn As Object, rs As Object
    Set cn = CreateObject("ADODB.Connection")
    Set rs = CreateObject("ADODB.Recordset")

    ' Bước 3 &amp; 4: Thiết lập đường dẫn và mở kết nối tới File Excel nguồn
    Dim filePath As String
    filePath = ThisWorkbook.FullName
    cn.Open "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=" &amp; filePath &amp; _
            ";Extended Properties=""Excel 12.0 Xml;HDR=YES;IMEX=1"";"

    ' Bước 5: Viết câu lệnh truy vấn SQL (Lọc, Gom nhóm &amp; Sắp xếp)
    Dim strSQL As String
    strSQL = "SELECT KhuVuc, NhomHang, COUNT(MaDon) AS SoDon, SUM(DoanhThu) AS TongDoanhThu " &amp; _
             "FROM [Data_BanHang$] " &amp; _
             "WHERE Nam = 2026 AND DoanhThu &gt; 0 " &amp; _
             "GROUP BY KhuVuc, NhomHang " &amp; _
             "ORDER BY SUM(DoanhThu) DESC"

    ' Bước 6: Thực thi truy vấn đưa dữ liệu vào túi chứa Recordset
    rs.Open strSQL, cn

    ' Bước 7: Xóa dữ liệu cũ và đổ kết quả ra Sheet Báo cáo
    With Sheet_BaoCao
        .Range("A5:D10000").ClearContents
        .Range("A5").CopyFromRecordset rs
    End With

    ' Bước 8: Đóng kết nối và giải phóng bộ nhớ
    rs.Close: cn.Close
    Set rs = Nothing: Set cn = Nothing
End Sub</pre>
</div>

<h2>4. 5 Câu lệnh SQL quan trọng nhất cho Chuyên viên Phân tích Dữ liệu &amp; Supply Chain</h2>
<ul>
  <li><strong><code class="erx-inline-code">SELECT ... FROM [SheetName$]</code>:</strong> Lựa chọn các cột dữ liệu cần lấy và tạo cột tính toán mới bằng bí danh <code class="erx-inline-code">AS</code>.</li>
  <li><strong><code class="erx-inline-code">WHERE</code> kết hợp <code class="erx-inline-code">BETWEEN / LIKE / IN</code>:</strong> Lọc dữ liệu theo khoảng ngày, mã kho, nhóm nhà cung cấp hoặc từ khóa tìm kiếm gần đúng.</li>
  <li><strong><code class="erx-inline-code">GROUP BY</code> &amp; <code class="erx-inline-code">HAVING</code>:</strong> Gom nhóm thống kê (<code class="erx-inline-code">SUM</code>, <code class="erx-inline-code">COUNT</code>, <code class="erx-inline-code">AVG</code>, <code class="erx-inline-code">MIN</code>, <code class="erx-inline-code">MAX</code>) thay thế hoàn hảo cho PivotTable và lọc các nhóm sau tổng hợp.</li>
  <li><strong><code class="erx-inline-code">LEFT JOIN</code> &amp; <code class="erx-inline-code">INNER JOIN</code>:</strong> Kết nối bảng Giao dịch (Fact Table) với các bảng Danh mục Vật tư, Khách hàng, Nhà cung cấp (Dimension Tables) mà không cần dùng <code class="erx-inline-code">VLOOKUP</code>.</li>
  <li><strong><code class="erx-inline-code">UNION ALL</code> &amp; <code class="erx-inline-code">TRANSFORM ... PIVOT</code>:</strong> Gộp dữ liệu từ 12 Sheet tháng thành 1 bảng duy nhất và xoay bảng chéo tự động.</li>
</ul>
<div class="erx-callout-box" style="background:#ECFDF5;border-left:4px solid #059669;padding:16px 20px;border-radius:8px;margin-top:20px;">
  <strong>Lộ trình thực hành tiếp theo tại ERX:</strong> Bạn hãy xem chi tiết từng bài hướng dẫn chuyên sâu trong chuyên mục <a href="/excel-sql.html"><strong>Excel SQL</strong></a> từ <a href="/8-buoc-co-ban-de-de-thiet-lap-mot-cau-lenh-sql-trong-excel-7122417941.html">8 bước thiết lập câu lệnh SQL</a>, <a href="/whrere-group-by-having-order-by-7122975038.html">WHERE – GROUP BY – HAVING</a> đến <a href="/join-statement-7123117353.html">Kỹ thuật nối bảng bằng JOIN Statement</a>.
</div>
""".strip()

# Topic-specific rich appendices for thin/short articles (clean_len < 3600)
CURATED_APPENDICES = {
    "7123687467": """
<div class="erx-deepdive-box">
  <h2>Tổng hợp Cú pháp &amp; So sánh Hiệu năng: Hàm SCAN + LAMBDA vs. Công thức Truyền thống</h2>
  <p>Khi triển khai bài toán tính lũy kế <strong>Sales To Date (Running Total)</strong> và <strong>Sales YTD (Year-To-Date)</strong> trên các bảng dữ liệu lớn trong Excel 365, việc nắm vững cấu trúc tham số của <code class="erx-inline-code">SCAN</code> và <code class="erx-inline-code">LAMBDA</code> giúp bạn thay thế hoàn toàn các công thức tham chiếu tuyệt đối mở rộng (<code class="erx-inline-code">$B$2:B2</code>) vốn làm chậm bảng tính:</p>
  <div class="erx-code-block">
    <div class="erx-code-header"><span>CÔNG THỨC EXCEL 365 CHUẨN</span><span>Dynamic Array — Sales To Date &amp; Sales YTD</span></div>
    <pre class="erx-code-pre">' 1. Công thức mảng động tính Lũy kế Doanh thu (Sales To Date):
=SCAN(0, B2:B25, LAMBDA(accumulator, current_val, accumulator + current_val))

' 2. Công thức mảng động tính Lũy kế Đầu năm (Sales YTD - tự động Reset khi sang năm mới):
=SCAN(0, B2:B25, LAMBDA(a, b, IF(MONTH(OFFSET(b, 0, -1)) = 1, b, a + b)))

' 3. Phiên bản tối ưu không dùng OFFSET (tránh hàm Volatile bằng SEQUENCE):
=LET(
    dates, A2:A25,
    sales, B2:B25,
    SCAN(0, SEQUENCE(ROWS(sales)), LAMBDA(acc, idx,
        IF(idx = 1, INDEX(sales, 1),
           IF(YEAR(INDEX(dates, idx)) &lt;&gt; YEAR(INDEX(dates, idx - 1)),
              INDEX(sales, idx),
              acc + INDEX(sales, idx)
           )
        )
    ))
)</pre>
  </div>
  <h3>Lưu ý kỹ thuật khi áp dụng trong Báo cáo Tài chính &amp; Supply Chain</h3>
  <ul>
    <li><strong>Tránh lỗi <code class="erx-inline-code">#SPILL!</code>:</strong> Vì <code class="erx-inline-code">SCAN</code> trả về một mảng động tràn xuống toàn bộ cột, bạn chỉ nhập công thức tại ô đầu tiên (ví dụ <code class="erx-inline-code">C2</code>) và đảm bảo các ô bên dưới (<code class="erx-inline-code">C3:C25</code>) hoàn toàn trống.</li>
    <li><strong>Xử lý ô chứa văn bản hoặc rỗng:</strong> Nếu cột doanh thu có thể chứa chuỗi hoặc lỗi, hãy bọc <code class="erx-inline-code">N(b)</code> hoặc <code class="erx-inline-code">IFERROR(b, 0)</code> bên trong <code class="erx-inline-code">LAMBDA</code> để không làm đứt gãy chuỗi cộng dồn.</li>
  </ul>
</div>
""".strip(),

    "7123702834": """
<div class="erx-deepdive-box">
  <h2>Bảng Phân biệt Khoảng trắng ASCII 32 vs. ASCII 160 &amp; Công thức Làm sạch Toàn diện</h2>
  <p>Trong thực tế làm việc với dữ liệu xuất ra từ hệ thống ERP (SAP, Oracle), CRM hoặc copy từ trang Web, lỗi phổ biến nhất khiến hàm <code class="erx-inline-code">VLOOKUP</code> / <code class="erx-inline-code">XLOOKUP</code> trả về <code class="erx-inline-code">#N/A</code> dù nhìn bằng mắt thường hai mã giống hệt nhau chính là ký tự <strong>Non-breaking space (<code class="erx-inline-code">CHAR(160)</code>)</strong>:</p>
  <div class="table-responsive">
    <table>
      <thead>
        <tr>
          <th>Loại ký tự ẩn</th>
          <th>Mã ASCII / Unicode</th>
          <th>Hàm <code class="erx-inline-code">TRIM()</code> xóa được?</th>
          <th>Giải pháp xử lý triệt để</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Khoảng trắng chuẩn (Standard Space)</strong></td>
          <td><code class="erx-inline-code">CHAR(32)</code></td>
          <td>Có (xóa đầu, cuối và khoảng trắng kép)</td>
          <td><code class="erx-inline-code">=TRIM(A2)</code></td>
        </tr>
        <tr>
          <td><strong>Khoảng trắng cứng (Non-breaking Space)</strong></td>
          <td><code class="erx-inline-code">CHAR(160)</code></td>
          <td><strong>Không</strong></td>
          <td><code class="erx-inline-code">=TRIM(SUBSTITUTE(A2, CHAR(160), " "))</code></td>
        </tr>
        <tr>
          <td><strong>Ký tự xuống dòng / Tab ẩn</strong></td>
          <td><code class="erx-inline-code">CHAR(9)</code>, <code class="erx-inline-code">CHAR(10)</code>, <code class="erx-inline-code">CHAR(13)</code></td>
          <td><strong>Không</strong></td>
          <td>Kết hợp thêm hàm <code class="erx-inline-code">CLEAN()</code></td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="erx-code-block">
    <div class="erx-code-header"><span>CÔNG THỨC EXCEL CHUẨN HÓA CHUỖI</span><span>All-in-One Data Cleaning Formula</span></div>
    <pre class="erx-code-pre">' Công thức chuẩn hóa toàn diện (Xóa đồng thời CHAR(160), ký tự xuống dòng CHAR(10) và khoảng trắng thừa):
=TRIM(CLEAN(SUBSTITUTE(A2, CHAR(160), " ")))

' Kiểm tra mã ASCII của ký tự cuối cùng trong ô A2 để phát hiện nhanh CHAR(160):
=CODE(RIGHT(A2, 1))</pre>
  </div>
</div>
""".strip(),

    "7123694822": """
<div class="erx-deepdive-box">
  <h2>Tổng hợp Các Mẫu Công thức Hàm FILTER Thực chiến (Đa điều kiện AND / OR &amp; Top N)</h2>
  <p>Để khai thác tối đa sức mạnh của hàm <code class="erx-inline-code">FILTER</code> trong Excel 365, bạn hãy lưu lại 4 mẫu công thức kết hợp điều kiện nâng cao thường xuyên sử dụng nhất trong báo cáo quản trị:</p>
  <div class="erx-code-block">
    <div class="erx-code-header"><span>CÔNG THỨC EXCEL 365</span><span>Advanced FILTER Patterns</span></div>
    <pre class="erx-code-pre">' 1. Lọc kết hợp nhiều điều kiện VÀ (AND) — Dùng dấu nhân (*):
=FILTER(A2:D100, (B2:B100 = "Miền Nam") * (D2:D100 &gt;= 50000000), "Không có dữ liệu thỏa mãn")

' 2. Lọc kết hợp nhiều điều kiện HOẶC (OR) — Dùng dấu cộng (+):
=FILTER(A2:D100, (B2:B100 = "Hà Nội") + (B2:B100 = "TP.HCM"), "Không tìm thấy")

' 3. Lọc theo từ khóa chứa chuỗi con (Tìm kiếm gần đúng kết hợp ISNUMBER + SEARCH):
=FILTER(A2:D100, ISNUMBER(SEARCH(G1, A2:A100)), "Không khớp từ khóa")

' 4. Lọc dữ liệu đồng thời sắp xếp giảm dần theo cột Doanh thu (Cột số 4):
=SORT(FILTER(A2:D100, C2:C100 &gt; 100, ""), 4, -1)</pre>
  </div>
</div>
""".strip(),

    "7123673148": """
<div class="erx-deepdive-box">
  <h2>So sánh 3 Phương pháp Tính Tổng Doanh thu Động trong N Tháng (Rolling N Months)</h2>
  <p>Bên cạnh phương pháp sử dụng <code class="erx-inline-code">OFFSET</code> kết hợp <code class="erx-inline-code">MATCH</code>, trên các phiên bản Excel hiện đại bạn có thể áp dụng hàm <code class="erx-inline-code">INDEX</code> (Non-volatile — không làm chậm file) hoặc <code class="erx-inline-code">TAKE</code> trong Excel 365:</p>
  <div class="erx-code-block">
    <div class="erx-code-header"><span>CÔNG THỨC EXCEL</span><span>Dynamic N-Month Rolling Revenue</span></div>
    <pre class="erx-code-pre">' Cách 1: Dùng SUM + OFFSET (Linh hoạt trên mọi phiên bản Excel):
=SUM(OFFSET(B1, 1, 0, E2, 1))

' Cách 2: Dùng SUM + INDEX (Tối ưu hiệu năng, không phải hàm Volatile):
=SUM(B2:INDEX(B2:B13, E2))

' Cách 3: Dùng SUM + TAKE trên Excel 365 (Ngắn gọn và hiện đại nhất):
=SUM(TAKE(B2:B13, E2))</pre>
  </div>
</div>
""".strip(),
}

# Generic category-aware deep-dive generator for any other legacy article with clean_len < 3400
def build_generic_appendix(nid: str, item: dict) -> str:
    if nid in CURATED_APPENDICES:
        return CURATED_APPENDICES[nid]
    url = item["url"]
    slug = url.split("/")[-1]
    clean_len = len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", item["ft_html"])))
    # Only append to articles whose clean text is < 3800 chars (including txtr wrapper)
    if clean_len > 3800:
        return ""

    # Determine topic domain from slug / text
    if any(k in slug for k in ["sql", "join", "where", "whrere", "wildcard", "union", "iif", "insert-update", "ado-"]):
        return """
<div class="erx-deepdive-box">
  <h2>Mẹo Tối ưu Truy vấn SQL trong Excel VBA &amp; Xử lý Lỗi Thường gặp</h2>
  <p>Khi triển khai câu lệnh truy vấn SQL thông qua kết nối <code class="erx-inline-code">ADODB.Connection</code> trên nền tảng Microsoft Excel, bạn cần lưu ý 3 quy tắc vàng sau để đảm bảo tốc độ và độ chính xác tuyệt đối:</p>
  <div class="erx-code-block">
    <div class="erx-code-header"><span>CHUỖI KẾT NỐI &amp; CÚ PHÁP CHUẨN</span><span>Microsoft ACE OLEDB 12.0</span></div>
    <pre class="erx-code-pre">' Chuỗi kết nối chuẩn hỗ trợ cả cột trộn kiểu dữ liệu Số và Văn bản (IMEX=1):
cn.Open "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=" &amp; filePath &amp; _
        ";Extended Properties=""Excel 12.0 Xml;HDR=YES;IMEX=1"";"

' Quy tắc bọc tên Sheet và tên Cột có khoảng trắng hoặc tiếng Việt:
strSQL = "SELECT [Mã Hàng], [Tên Sản Phẩm], SUM([Thành Tiền]) AS TongTien " &amp; _
         "FROM [Data_BanHang$A1:G50000] " &amp; _
         "WHERE [Thành Tiền] IS NOT NULL " &amp; _
         "GROUP BY [Mã Hàng], [Tên Sản Phẩm]"</pre>
  </div>
  <ul>
    <li><strong>Luôn thêm tham số <code class="erx-inline-code">IMEX=1</code>:</strong> Giúp trình điều khiển OLEDB không tự ý biến các mã hàng vừa có số vừa có chữ thành giá trị <code class="erx-inline-code">Null</code>.</li>
    <li><strong>Giới hạn vùng dữ liệu khi Sheet có định dạng thừa:</strong> Thay vì gọi <code class="erx-inline-code">[Sheet1$]</code>, bạn có thể chỉ định rõ <code class="erx-inline-code">[Sheet1$A1:Z50000]</code> để bỏ qua các dòng rác cuối bảng.</li>
    <li><strong>Đóng kết nối sau khi <code class="erx-inline-code">CopyFromRecordset</code>:</strong> Luôn gọi <code class="erx-inline-code">rs.Close</code> và <code class="erx-inline-code">cn.Close</code> để giải phóng bộ nhớ RAM và tránh khóa file nguồn.</li>
  </ul>
</div>
""".strip()

    if any(k in slug for k in ["vba", "isnumeric", "workbook", "unblock", "addin", "payment_schedule"]):
        return """
<div class="erx-deepdive-box">
  <h2>Khung Mẫu Tối ưu Tốc độ Thực thi Code VBA trên Bảng tính Lớn</h2>
  <p>Khi áp dụng các đoạn mã VBA trên bảng tính doanh nghiệp có hàng chục nghìn dòng dữ liệu, bạn hãy bọc code trong khung mẫu tối ưu hiệu năng dưới đây để tăng tốc độ chạy Macro lên gấp <strong>10 – 50 lần</strong>:</p>
  <div class="erx-code-block">
    <div class="erx-code-header"><span>MÃ NGUỒN VBA CHUẨN</span><span>High-Performance Macro Wrapper</span></div>
    <pre class="erx-code-pre">Sub ERX_Optimized_Macro_Template()
    On Error GoTo CleanExit
    ' Tắt cập nhật màn hình và tính toán tự động để tăng tốc tối đa
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False

    ' --- Đặt nội dung xử lý VBA của bạn tại đây ---

CleanExit:
    ' Khôi phục trạng thái chuẩn của Excel sau khi hoàn tất
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Application.EnableEvents = True
End Sub</pre>
  </div>
</div>
""".strip()

    if any(k in slug for k in ["power-bi", "powerbi", "dax", "slicer", "datetable", "pareto"]):
        return """
<div class="erx-deepdive-box">
  <h2>Nguyên tắc Tối ưu Mô hình Dữ liệu (Star Schema) &amp; Viết Hàm DAX Chuẩn trong Power BI</h2>
  <p>Để các công thức DAX và bộ lọc Slicer trên Dashboard Power BI luôn phản hồi tức thì khi dữ liệu lên tới hàng triệu dòng, bạn hãy tuân thủ các nguyên tắc thực hành tốt nhất (Best Practices) sau:</p>
  <div class="erx-code-block">
    <div class="erx-code-header"><span>BIỂU THỨC DAX MẪU</span><span>DAX Best Practices — VAR / RETURN &amp; DIVIDE</span></div>
    <pre class="erx-code-pre">Doanh Thu Ky Truoc &amp; % Tang Truong = 
VAR _CurrentSales = [Total Sales]
VAR _PrevSales = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
RETURN
    DIVIDE(_CurrentSales - _PrevSales, _PrevSales, 0)</pre>
  </div>
  <ul>
    <li><strong>Sử dụng biến <code class="erx-inline-code">VAR ... RETURN</code>:</strong> Giúp công thức DAX chỉ tính toán biểu thức trung gian một lần duy nhất, vừa tăng tốc độ vừa dễ kiểm tra lỗi.</li>
    <li><strong>Ưu tiên Measure thay vì Calculated Column:</strong> Chỉ tạo cột tính toán khi bạn bắt buộc phải dùng cột đó làm tiêu chí lọc trên Slicer hoặc trục biểu đồ.</li>
  </ul>
</div>
""".strip()

    if any(k in slug for k in ["python", "pandas", "jupyter", "colab", "mrp"]):
        return """
<div class="erx-deepdive-box">
  <h2>Mẫu Quy trình Chuẩn: Đọc, Xử lý và Xuất Báo cáo Excel Tự động bằng Python Pandas</h2>
  <p>Bạn có thể kết hợp trực tiếp các kỹ thuật Python và thư viện <code class="erx-inline-code">pandas</code> trong bài viết vào quy trình tự động hóa báo cáo Excel hàng ngày theo khung code chuẩn sau:</p>
  <div class="erx-code-block">
    <div class="erx-code-header"><span>MÃ NGUỒN PYTHON</span><span>Pandas Excel Automation Pipeline</span></div>
    <pre class="erx-code-pre">import pandas as pd

# 1. Đọc dữ liệu từ file Excel và chuẩn hóa tên cột
df = pd.read_excel("Data_Nguon.xlsx", sheet_name="Sheet1")
df.columns = df.columns.str.strip()

# 2. Lọc dữ liệu hợp lệ và gom nhóm tổng hợp
summary = (
    df.dropna(subset=["DoanhThu"])
      .groupby("NhomHang", as_index=False)
      .agg(SoDon=("MaDon", "count"), TongDoanhThu=("DoanhThu", "sum"))
      .sort_values(by="TongDoanhThu", ascending=False)
)

# 3. Xuất kết quả ra file Excel báo cáo mới
summary.to_excel("Bao_Cao_Tong_Hop.xlsx", index=False)</pre>
  </div>
</div>
""".strip()

    if any(k in slug for k in ["excel", "textsplit", "textbefore", "textafter", "custom-list", "skip-blanks", "hidden-row", "danh-so-thu-tu", "vstack", "bieu-do", "do-thi"]):
        return """
<div class="erx-deepdive-box">
  <h2>Tổng hợp Công thức &amp; Phím tắt Tối ưu Hiệu suất Làm việc trên Microsoft Excel</h2>
  <p>Để áp dụng kỹ thuật trên một cách nhanh chóng và chuyên nghiệp nhất trong báo cáo thực tế tại doanh nghiệp, bạn hãy kết hợp chuyển đổi vùng dữ liệu nguồn sang định dạng <strong>Excel Table (<code class="erx-inline-code">Ctrl + T</code>)</strong>:</p>
  <div class="erx-code-block">
    <div class="erx-code-header"><span>CÔNG THỨC EXCEL THỰC CHIẾN</span><span>Dynamic Array &amp; Structured Reference</span></div>
    <pre class="erx-code-pre">' Kết hợp hàm mảng động lọc dữ liệu sạch, loại bỏ dòng trống và sắp xếp tự động:
=LET(
    data, FILTER(Table1, Table1[DoanhThu] &gt; 0, ""),
    SORT(data, 1, 1)
)</pre>
  </div>
  <ul>
    <li><strong>Tự động co giãn phạm vi:</strong> Khi dữ liệu gốc được đặt trong <code class="erx-inline-code">Excel Table (Ctrl + T)</code>, mọi công thức tham chiếu sẽ tự động cập nhật ngay khi bạn thêm dòng mới vào cuối bảng.</li>
    <li><strong>Bẫy lỗi chuyên nghiệp:</strong> Luôn truyền tham số <code class="erx-inline-code">[if_empty]</code> hoặc bọc ngoài bằng <code class="erx-inline-code">IFERROR(..., "")</code> để bảng báo cáo luôn sạch đẹp khi in ấn.</li>
  </ul>
</div>
""".strip()

    return ""

appendices_map = {}
for nid, item in legacy_items.items():
    app = build_generic_appendix(nid, item)
    if app:
        appendices_map[nid] = app

print(f"Prepared {len(CURATED_INTROS)} curated intros and {len(appendices_map)} deep-dive appendices.")

# Now build the browser JS bundle erx_legacy_upgrader.js
js_code = f"""// ERX Site-Wide Legacy Article Content & Code/Formula Formatter
window.ERX_LEGACY_INTROS = {json.dumps(CURATED_INTROS, ensure_ascii=False)};
window.ERX_LEGACY_APPENDICES = {json.dumps(appendices_map, ensure_ascii=False)};
window.ERX_REPLACEMENT_7122169949 = {json.dumps(REPLACEMENT_7122169949, ensure_ascii=False)};
window.ERX_ALL_LEGACY_IDS = {json.dumps(sorted(list(legacy_items.keys()), key=lambda x: int(x)))};

window.erxTransformArticleHtml = function(nid, rawHtml) {{
  if (nid === "7122169949") {{
    return window.ERX_REPLACEMENT_7122169949;
  }}
  if (!rawHtml) return rawHtml;

  // 1. Strip raw <style> blocks (especially 580KB JupyterLab CSS in 7122438204 & 7122491878)
  let cleaned = rawHtml.replace(/<style[^>]*>[\\s\\S]*?<\\/style>/gi, "");

  // Parse into a detached DOM container
  const container = document.createElement("div");
  container.innerHTML = cleaned;

  // Remove any previously injected erx-deepdive-box so re-runs are idempotent
  container.querySelectorAll(".erx-deepdive-box").forEach(el => el.remove());

  // 1b. Convert JupyterLab code cells (.jp-InputArea-editor / .highlight / pre) into .erx-code-block
  container.querySelectorAll(".jp-Cell-inputWrapper, .jp-InputArea").forEach(cell => {{
    const codeEl = cell.querySelector(".CodeMirror-code, pre");
    if (codeEl) {{
      let lines = [];
      const lineEls = codeEl.querySelectorAll(".CodeMirror-line, pre");
      if (lineEls.length > 0) {{
        lineEls.forEach(l => lines.push(l.textContent.replace(/\\u200b/g, "")));
      }} else {{
        lines.push(codeEl.textContent.replace(/\\u200b/g, ""));
      }}
      const codeTxt = lines.join("\\n").trim();
      if (codeTxt) {{
        const block = document.createElement("div");
        block.className = "erx-code-block";
        block.innerHTML = '<div class="erx-code-header"><span>MÃ NGUỒN PYTHON</span><span>Jupyter Notebook / Pandas</span></div><pre class="erx-code-pre"></pre>';
        block.querySelector("pre").textContent = codeTxt;
        cell.replaceWith(block);
      }}
    }}
  }});

  // 2. Convert <blockquote> containing VBA / SQL code into .erx-code-block
  container.querySelectorAll("blockquote").forEach(bq => {{
    if (bq.closest(".erx-code-block")) return;
    const txt = (bq.innerText || bq.textContent || "").replace(/\\u00a0/g, " ").trim();
    if (!txt) return;
    const isCode = /^(Dim |Set |Sub |Function |Private |Public |ActiveWorkbook|Workbooks|ThisWorkbook|Sheet\\d|Range\\(|Cells\\(|cn\\.|rs\\.|rst\\.|Duy\\.|SELECT |INSERT |UPDATE |DELETE |TRANSFORM |duong_dan|If |For |Do |With |=)/im.test(txt)
      || /(CreateObject\\(|ADODB\\.|CopyFromRecordset|ClearContents|\\.Open |\\.SaveAs |\\.Close|SELECT .* FROM )/i.test(txt);
    if (isCode) {{
      const rawLines = txt.split(/\\r?\\n/).map(s => s.trim()).filter(Boolean);
      const codeLines = [];
      const noteLines = [];
      let inNotes = false;
      for (const line of rawLines) {{
        if (/^(Lưu ý|Chú thích|Trong đó|Giải thích)\\s*:/i.test(line) || inNotes) {{
          inNotes = true;
          noteLines.push(line);
        }} else {{
          codeLines.push(line);
        }}
      }}
      if (codeLines.length > 0) {{
        const isSqlOnly = /^(SELECT |INSERT |UPDATE |DELETE |TRANSFORM )/i.test(codeLines[0]) && !/^(Dim |Set |rst\\.|rs\\.|cn\\.)/i.test(codeLines[0]);
        const badge = isSqlOnly ? "TRUY VẤN SQL" : "MÃ NGUỒN VBA / SQL";
        const subBadge = isSqlOnly ? "Excel SQL Query" : "Excel VBA / ADODB";
        const wrapper = document.createElement("div");
        const block = document.createElement("div");
        block.className = "erx-code-block";
        block.innerHTML = `<div class="erx-code-header"><span>${{badge}}</span><span>${{subBadge}}</span></div><pre class="erx-code-pre"></pre>`;
        block.querySelector("pre").textContent = codeLines.join("\\n");
        wrapper.appendChild(block);
        if (noteLines.length > 0) {{
          const noteP = document.createElement("p");
          noteP.style.cssText = "font-size:14.5px;color:#475569;background:#F1F5F9;padding:10px 14px;border-radius:8px;margin-top:-10px;margin-bottom:16px;";
          noteP.textContent = noteLines.join(" | ");
          wrapper.appendChild(noteP);
        }}
        bq.replaceWith(...wrapper.childNodes);
      }}
    }}
  }});

  // 3. Inspect standalone <p> and leaf <div> elements for Headings vs Formulas/Code
  const candidates = Array.from(container.querySelectorAll("p, div"));
  for (const el of candidates) {{
    if (!container.contains(el)) continue;
    if (el.closest(".erx-code-block, .erx-deepdive-box, table, thead, tbody, tr, td, th, ul, ol, blockquote")) continue;
    if (el.querySelector("img, iframe, table, ul, ol, p, div, blockquote, pre, h1, h2, h3, h4")) continue;

    const rawText = (el.innerText || el.textContent || "").replace(/\\u00a0/g, " ").trim();
    if (!rawText) {{
      // Remove empty spacer divs/paragraphs if they only had &nbsp;
      if (el.tagName === "DIV" && !el.children.length) el.remove();
      continue;
    }}

    // Check if this is a standalone Formula or Code snippet
    const isExcelFormula = /^=\\s*[A-Za-z_][A-Za-z0-9_.]*\\s*\\(/.test(rawText)
      || /^=\\s*\\$?[A-Z]{1,3}\\$?\\d+/.test(rawText)
      || /^(SCAN|LAMBDA|FILTER|CHOOSEROWS|CHOOSECOLS|TEXTSPLIT|TEXTBEFORE|TEXTAFTER|TOCOL|TOROW|VSTACK|HSTACK|WRAPROWS|WRAPCOLS|TAKE|DROP|EXPAND|VLOOKUP|XLOOKUP|INDEX|MATCH|OFFSET|SUBTOTAL|AGGREGATE|SUMIFS|COUNTIFS)\\s*\\([^)]+\\)$/i.test(rawText);

    const isSqlQuery = /^(SELECT\\s+.+\\s+FROM\\s+|INSERT\\s+INTO\\s+|UPDATE\\s+.+\\s+SET\\s+|DELETE\\s+FROM\\s+|TRANSFORM\\s+.+\\s+SELECT\\s+)/is.test(rawText) && rawText.length < 600;

    const isVbaSnippet = /^(Sub\\s+\\w+|Function\\s+\\w+|Dim\\s+\\w+\\s+As\\s+|Set\\s+\\w+\\s*=\\s*CreateObject|Workbooks\\.Open|ActiveWorkbook\\.|ThisWorkbook\\.|Application\\.)/i.test(rawText) && rawText.length < 600;

    const isDaxFormula = /^([A-Za-z0-9_À-ỹ ]+\\s*=\\s*(CALCULATE|SUMX|FILTER|ALL|ALLSELECTED|RANKX|DIVIDE|CALENDAR|CALENDARAUTO|VAR\\s+|IF\\s*\\(|SWITCH\\s*\\())/i.test(rawText) && rawText.length < 500;

    const isPythonSnippet = /^(import\\s+pandas|from\\s+pandas|df\\s*=\\s*pd\\.|df\\.(head|tail|info|describe|groupby|loc|iloc|dropna|fillna)|pip\\s+install\\s+|conda\\s+install\\s+)/i.test(rawText) && rawText.length < 400;

    if (isExcelFormula || isSqlQuery || isVbaSnippet || isDaxFormula || isPythonSnippet) {{
      let badge = "CÔNG THỨC EXCEL";
      let sub = "Excel Formula";
      if (isSqlQuery) {{ badge = "TRUY VẤN SQL"; sub = "SQL Statement"; }}
      else if (isVbaSnippet) {{ badge = "MÃ NGUỒN VBA"; sub = "Excel VBA"; }}
      else if (isDaxFormula) {{ badge = "BIỂU THỨC DAX"; sub = "Power BI DAX"; }}
      else if (isPythonSnippet) {{ badge = "MÃ NGUỒN PYTHON"; sub = "Python / Pandas"; }}

      const block = document.createElement("div");
      block.className = "erx-code-block";
      block.innerHTML = `<div class="erx-code-header"><span>${{badge}}</span><span>${{sub}}</span></div><pre class="erx-code-pre"></pre>`;
      block.querySelector("pre").textContent = rawText;
      el.replaceWith(block);
      continue;
    }}

    // Check if this is a pseudo-heading that should be promoted to <h2> or <h3>
    const hasLargeFont = /font-size\\s*:\\s*(2[0-9]|1[89])px/i.test(el.getAttribute("style") || "")
      || !!el.querySelector('[style*="font-size:24px"], [style*="font-size: 24px"], [style*="font-size:22px"], [style*="font-size: 22px"], [style*="font-size:20px"], [style*="font-size: 20px"], [style*="font-size:18px"], [style*="font-size: 18px"]');
    const isAllBold = (el.children.length === 1 && (el.firstElementChild.tagName === "STRONG" || el.firstElementChild.tagName === "B") && el.firstElementChild.textContent.trim() === rawText);

    if (rawText.length >= 4 && rawText.length <= 115) {{
      const isMainSectionPattern = /^((Phần|Bước|Phương pháp|Cách)\\s*\\d+|[IVX]+\\.|[A-Z]\\.|\\d+\\.\\s+\\S|Giới thiệu|Cách sử dụng|Các ví dụ|Một số lưu ý|Kết luận)/i.test(rawText);
      const isSubSectionPattern = /^(\\d+\\.\\d+\\.?\\s+\\S|[a-e]\\.\\s+\\S|Ví dụ\\s*\\d+)/i.test(rawText);
      if (isSubSectionPattern && (isAllBold || hasLargeFont)) {{
        const h3 = document.createElement("h3");
        h3.textContent = rawText;
        el.replaceWith(h3);
        continue;
      }}
      if ((isMainSectionPattern && (isAllBold || hasLargeFont || rawText.length <= 85)) || (hasLargeFont && rawText.length <= 95)) {{
        const h2 = document.createElement("h2");
        h2.textContent = rawText;
        el.replaceWith(h2);
        continue;
      }}
      if (isAllBold && rawText.length <= 75 && !/[.,;!]$/.test(rawText) && !rawText.startsWith("-") && !rawText.startsWith("•")) {{
        const h3 = document.createElement("h3");
        h3.textContent = rawText;
        el.replaceWith(h3);
        continue;
      }}
    }}

    // Inject structural <h2> headings into flat articles that lack headings
    const headingTriggers = [
      {{ match: /^Để tính được Sales To Date ta sẽ sử dụng/i, h2: "1. Cách tính lũy kế Sales To Date bằng hàm SCAN và LAMBDA" }},
      {{ match: /^Tuy nhiên nếu bạn muốn tính bài toán Sales YTD/i, h2: "2. Cách tính lũy kế đầu năm (Sales YTD) bằng hàm SCAN + OFFSET" }},
      {{ match: /^Ngoài ra nếu bạn sử dụng các phiên bản Office cũ/i, h2: "3. Công thức thay thế (SUM & SUMIFS) trên các phiên bản Excel cũ" }},
      {{ match: /^Hàm TRIM trong Excel loại bỏ khoảng trống/i, h2: "1. Sử dụng hàm TRIM để xóa khoảng trắng thừa tiêu chuẩn (ASCII 32)" }},
      {{ match: /^Tuy nhiên trong Excel không phải lúc nào dùng hàm TRIM/i, h2: "2. Nguyên nhân hàm TRIM không xóa được khoảng trắng mã ASCII 160" }},
      {{ match: /^Để làm điều đó thì ta cần sử dụng hàm SUBSTITUTE/i, h2: "3. Giải pháp kết hợp hàm TRIM, SUBSTITUTE và CHAR(160)" }},
      {{ match: /^Để tính ngày bắt đầu thì bạn sẽ sử dụng hàm EOMONTH/i, h2: "1. Xác định ngày bắt đầu kỳ N tháng bằng hàm EOMONTH" }},
      {{ match: /^Ở đây bạn có thể sử dụng 2 công thức để viết được kết quả/i, h2: "2. Công thức tính tổng doanh thu N tháng bằng INDEX/MATCH và XLOOKUP" }}
    ];
    for (const trig of headingTriggers) {{
      if (trig.match.test(rawText) && (!el.previousElementSibling || el.previousElementSibling.tagName !== "H2")) {{
        const h2 = document.createElement("h2");
        h2.textContent = trig.h2;
        el.parentNode.insertBefore(h2, el);
        break;
      }}
    }}
  }}

  // 4. Highlight inline function names and technical tokens in <p> and <li>
  const inlineRegex = /\\b(VLOOKUP|XLOOKUP|HLOOKUP|INDEX|MATCH|OFFSET|SUMIFS|COUNTIFS|AVERAGEIFS|SUBTOTAL|AGGREGATE|FILTER|SORT|SORTBY|UNIQUE|SEQUENCE|RANDARRAY|SCAN|REDUCE|LAMBDA|BYROW|BYCOL|MAKEARRAY|ISOMITTED|LET|VSTACK|HSTACK|TOCOL|TOROW|WRAPROWS|WRAPCOLS|TAKE|DROP|CHOOSEROWS|CHOOSECOLS|EXPAND|TEXTSPLIT|TEXTBEFORE|TEXTAFTER|SUBSTITUTE|TRIM|CLEAN|EOMONTH|EDATE|WORKDAY|NETWORKDAYS|ISNUMERIC|ADODB\\.Connection|ADODB\\.Recordset|CopyFromRecordset|ClearContents|CALCULATE|ALLSELECTED|SAMEPERIODLASTYEAR|CALENDARAUTO|RANKX|DIVIDE|DataFrame|groupby|read_excel|CHAR\\(160\\)|CHAR\\(32\\)|CHAR\\(10\\)|#N\\/A|#VALUE!|#REF!|#CALC!|#SPILL!|#NAME\\?)\\b/g;

  container.querySelectorAll("p, li").forEach(el => {{
    if (el.closest(".erx-code-block, .erx-deepdive-box, h1, h2, h3, h4, a, code, pre")) return;
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    const textNodes = [];
    while (walker.nextNode()) {{
      const n = walker.currentNode;
      if (n.parentElement && !n.parentElement.closest("code, pre, a, .erx-code-block")) {{
        if (inlineRegex.test(n.nodeValue)) {{
          textNodes.push(n);
        }}
        inlineRegex.lastIndex = 0;
      }}
    }}
    for (const tn of textNodes) {{
      const frag = document.createDocumentFragment();
      let lastIdx = 0;
      const str = tn.nodeValue;
      inlineRegex.lastIndex = 0;
      let m;
      while ((m = inlineRegex.exec(str)) !== null) {{
        if (m.index > lastIdx) {{
          frag.appendChild(document.createTextNode(str.slice(lastIdx, m.index)));
        }}
        const codeTag = document.createElement("code");
        codeTag.className = "erx-inline-code";
        codeTag.textContent = m[0];
        frag.appendChild(codeTag);
        lastIdx = m.index + m[0].length;
      }}
      if (lastIdx < str.length) {{
        frag.appendChild(document.createTextNode(str.slice(lastIdx)));
      }}
      tn.replaceWith(frag);
    }}
  }});

  // 5. Append curated deep-dive section if applicable
  const appendixHtml = window.ERX_LEGACY_APPENDICES[nid];
  if (appendixHtml) {{
    const temp = document.createElement("div");
    temp.innerHTML = appendixHtml;
    while (temp.firstChild) {{
      container.appendChild(temp.firstChild);
    }}
  }}

  return container.innerHTML;
}};

window.erxRunFullLegacyUpgrade = async function(batchSize = 5) {{
  const ids = window.ERX_ALL_LEGACY_IDS;
  const results = {{ total: ids.length, updated: 0, errors: [] }};

  for (let i = 0; i < ids.length; i += batchSize) {{
    const batch = ids.slice(i, i + batchSize);
    await Promise.all(batch.map(async (nid) => {{
      try {{
        const editUrl = `/administrator/content/edit.aspx?nContentId=${{nid}}&divid=300&from=31`;
        const resp = await fetch(editUrl, {{ credentials: "include" }});
        const html = await resp.text();
        const doc = new DOMParser().parseFromString(html, "text/html");
        const form = doc.querySelector("form");
        if (!form) {{
          results.errors.push({{ nid, err: "No form found" }});
          return;
        }}

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

        // 1. Set Curated INTROTEXT
        const curatedIntro = window.ERX_LEGACY_INTROS[nid];
        const currentIntro = (fd.get("CONTENTS[0].INTROTEXT") || "").trim();
        const plainIntro = currentIntro.replace(/<[^>]+>/g, " ").replace(/\\s+/g, " ").trim();
        if (curatedIntro) {{
          fd.set("CONTENTS[0].INTROTEXT", curatedIntro);
        }} else if (plainIntro.length > 420) {{
          fd.set("CONTENTS[0].INTROTEXT", plainIntro.slice(0, 340) + "...");
        }}

        // Also ensure META_DESC is populated cleanly
        const curMetaDesc = (fd.get("CONTENTS[0].META_DESC") || "").trim();
        if ((!curMetaDesc || curMetaDesc.length < 70 || curMetaDesc.length > 320) && (curatedIntro || plainIntro)) {{
          const srcDesc = curatedIntro || plainIntro;
          fd.set("CONTENTS[0].META_DESC", srcDesc.length > 160 ? srcDesc.slice(0, 157) + "..." : srcDesc);
        }}

        // 2. Transform FULLTEXT
        const rawFull = fd.get("CONTENTS[0].FULLTEXT") || "";
        const upgradedFull = window.erxTransformArticleHtml(nid, rawFull);
        fd.set("CONTENTS[0].FULLTEXT", upgradedFull);
        fd.set("btnSubmit", "save_and_close");

        const postResp = await fetch(editUrl, {{
          method: "POST",
          credentials: "include",
          headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
          body: fd.toString()
        }});

        if (postResp.ok) {{
          results.updated++;
        }} else {{
          results.errors.push({{ nid, status: postResp.status }});
        }}
      }} catch (e) {{
        results.errors.push({{ nid, err: String(e) }});
      }}
    }}));
    console.log(`[ERX Upgrader] Progress: ${{Math.min(i + batchSize, ids.length)}} / ${{ids.length}} (Updated: ${{results.updated}})`);
  }}
  return results;
}};

window.erxUpgradeHeaderScript = async function() {{
  const appUrl = "/administrator/system/applicationex.aspx";
  const resp = await fetch(appUrl, {{ credentials: "include" }});
  const html = await resp.text();
  const doc = new DOMParser().parseFromString(html, "text/html");
  const form = doc.querySelector("form");
  if (!form) return {{ ok: false, err: "No applicationex form" }};

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

  let sh = fd.get("META.SCRIPT_HEADER") || "";
  const extraCss = `
/* ERX Dedicated Formula & Code Block Styling */
.div-full-content .erx-code-block,
.course-detail-container .erx-code-block {{
  background: #F8FAFC !important;
  border: 1px solid #CBD5E1 !important;
  border-left: 4px solid #059669 !important;
  border-radius: 10px !important;
  margin: 18px 0 22px 0 !important;
  overflow: hidden !important;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04) !important;
}}
.div-full-content .erx-code-header,
.course-detail-container .erx-code-header {{
  background: #F1F5F9 !important;
  border-bottom: 1px solid #E2E8F0 !important;
  padding: 6px 14px !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  font-size: 11.5px !important;
  font-weight: 700 !important;
  letter-spacing: 0.05em !important;
  text-transform: uppercase !important;
  color: #047857 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
}}
.div-full-content .erx-code-body,
.course-detail-container .erx-code-body,
.div-full-content pre.erx-code-pre,
.course-detail-container pre.erx-code-pre {{
  margin: 0 !important;
  padding: 14px 16px !important;
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace !important;
  font-size: 14.5px !important;
  line-height: 1.65 !important;
  color: #0F172A !important;
  background: #F8FAFC !important;
  overflow-x: auto !important;
  white-space: pre-wrap !important;
  word-break: break-word !important;
  font-weight: 600 !important;
}}
.div-full-content code.erx-inline-code,
.course-detail-container code.erx-inline-code,
.div-full-content p code,
.div-full-content li code,
.div-full-content td code {{
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace !important;
  font-size: 0.9em !important;
  background: #F1F5F9 !important;
  color: #0F766E !important;
  border: 1px solid #CBD5E1 !important;
  border-radius: 5px !important;
  padding: 2px 6px !important;
  font-weight: 600 !important;
}}
.div-full-content .erx-deepdive-box {{
  background: #F8FAFC !important;
  border: 1px solid #E2E8F0 !important;
  border-top: 3px solid #059669 !important;
  border-radius: 12px !important;
  padding: 20px 24px !important;
  margin: 26px 0 !important;
}}
`;

  if (!sh.includes("/* ERX Dedicated Formula & Code Block Styling */")) {{
    if (sh.includes("</style>")) {{
      sh = sh.replace("</style>", extraCss + "\\n</style>");
    }} else {{
      sh += `<style id="erx-code-block-styles">${{extraCss}}</style>`;
    }}
  }}

  fd.set("META.SCRIPT_HEADER", sh);
  fd.set("btnSubmit", "update");

  const postResp = await fetch(appUrl, {{
    method: "POST",
    credentials: "include",
    headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
    body: fd.toString()
  }});
  return {{ ok: postResp.ok, status: postResp.status }};
}};
""";

OUT_JS_PATH.write_text(js_code, encoding="utf-8")
print(f"Wrote {OUT_JS_PATH} ({OUT_JS_PATH.stat().st_size:,} bytes)")
