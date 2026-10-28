# -*- coding: utf-8 -*-
"""
Builds the 8 Cluster Articles (PM-02, PM-03, PM-05, PM-06, PM-07, PM-10, PM-11, PM-12)
with clean semantic HTML (no duplicate intro box, no duplicate hero diagram in body,
light-tone minimalist diagrams, and uniform editorial typography).
"""
import os
import json

ASSET_DIR = r"D:\GIT\SEO Tool\pm_assets"

# Exact live URLs of the 4 published Pillar Articles
URL_PM01 = "https://erx.vn/quan-tri-du-an-theo-chuan-pmbok-8-tong-quan-nguyen-tac-va-quy-trinh-7124047589.html"
URL_PM04 = "https://erx.vn/cau-truc-phan-ra-cong-viec-wbs-va-tu-dien-wbs-trong-quan-ly-du-an-7124054453.html"
URL_PM08 = "https://erx.vn/earned-value-management-evm-cach-tinh-pv-ev-ac-spi-cpi-eac-trong-du-an-7124068075.html"
URL_PM09 = "https://erx.vn/dinh-luong-rui-ro-du-an-bang-emv-expected-monetary-value-va-contingency-reserve-7124079199.html"

def figure_html(img_src, alt_text, caption_text):
    return f"""
<figure class="erx-figure" style="margin: 26px 0; text-align: center; background: #f8fafc; padding: 14px; border-radius: 12px; border: 1px solid #e2e8f0;">
  <img src="{img_src}" alt="{alt_text}" width="1200" height="675" loading="lazy" decoding="async" style="max-width: 100%; height: auto; border-radius: 8px; display: block; margin: 0 auto; border: 1px solid #e2e8f0;" />
  <figcaption style="margin-top: 10px; font-size: 14.5px; color: #475569; font-style: italic;">{caption_text}</figcaption>
</figure>
"""

CTA_BOX_HTML = """
<div class="erx-cta-box" style="margin: 28px 0; padding: 22px 26px; background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 5px solid #10b981; border-radius: 12px;">
  <h3 style="margin-top: 0; color: #065f46;">🚀 Thực hành Trực tiếp trên Nền tảng ERX AI Project Gantt Planner</h3>
  <p>
    Thay vì quản lý rời rạc trên hàng chục file Excel và Word dễ lệch số liệu, bạn có thể lập tiến độ <strong>WBS đa cấp</strong>, tính <strong>Đường găng (CPM)</strong>, theo dõi <strong>9 chỉ số EVM</strong>, định lượng rủi ro tự động <strong>EMV = P% × Impact($)</strong> và đồng bộ <strong>13 hồ sơ chuẩn PMBOK® 8</strong> ngay trên trình duyệt.
  </p>
  <p style="margin-bottom: 0;">
    👉 <a href="https://project-management.erx.vn/" target="_blank" rel="noopener" style="display: inline-block; background: #10b981; color: #ffffff !important; font-weight: 700; padding: 10px 20px; border-radius: 8px; text-decoration: none;">Mở Nền tảng project-management.erx.vn Ngay →</a>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="https://erx.vn/project-management.html" style="color: #059669; font-weight: 600; text-decoration: underline;">Xem trọn bộ Chuyên mục Project Management</a>
  </p>
</div>
"""

# ==============================================================================
# PM-02: PROJECT CHARTER & BUSINESS CASE
# ==============================================================================
pm02_html = f"""
<h2>1. Project Charter (Điều lệ Dự án) là gì trong chuẩn PMBOK® Guide – 8th Edition?</h2>
<p>
  Trong tiêu chuẩn <a href="{URL_PM01}"><strong>PMBOK® Guide – 8th Edition (PMBOK 8)</strong></a>, <strong>Project Charter (Điều lệ Dự án)</strong> là văn bản pháp lý nội bộ quan trọng nhất thuộc nhóm quy trình <em>Khởi tạo (Initiating Process Group)</em> và miền hiệu suất <em>Quản trị (Governance Performance Domain)</em>. Đây là tài liệu do Nhà tài trợ dự án (<em>Project Sponsor</em>) hoặc Ban Giám đốc ký ban hành nhằm:
</p>
<ul>
  <li><strong>Chính thức công nhận sự tồn tại của dự án:</strong> Cho phép dự án chuyển từ giai đoạn ý tưởng sang giai đoạn sử dụng nguồn lực và ngân sách của doanh nghiệp.</li>
  <li><strong>Trao quyền chính thức cho Giám đốc Dự án (Project Manager - PM):</strong> Xác định rõ quyền hạn của PM trong việc điều động nhân sự liên phòng ban, phê duyệt chi tiêu trong hạn mức và kiểm soát thay đổi.</li>
  <li><strong>Gắn kết mục tiêu dự án với chiến lược kinh doanh:</strong> Kết nối trực tiếp giữa bài toán đầu tư (<em>Business Case</em>) và kế hoạch hiện thực hóa lợi ích (<em>Benefits Management Plan</em>).</li>
</ul>

<h2>2. Phân biệt Ba Hồ sơ Khởi tạo: Business Case, Project Charter và Benefits Management Plan</h2>
<p>
  Một sai lầm phổ biến tại nhiều doanh nghiệp là gộp chung lý do đầu tư và kế hoạch triển khai vào một file trình ký sơ sài. Trên nền tảng <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>project-management.erx.vn</strong></a>, 3 hồ sơ số <code>(01) Project Charter</code>, <code>(02) Business Case</code> và <code>(03) Benefits Plan</code> được tách bạch rõ ràng nhưng đồng bộ dữ liệu thời gian thực với nhau:
</p>

{figure_html("/Media/images/pm02_2_business_case_vs_benefits_light.jpg", "Chu trình quản trị giá trị đầu tư dự án chuẩn PMBOK 8: Business Case, Project Charter và Benefits Management Plan", "Hình 1: Chu trình liên kết xuyên suốt giữa Business Case (Tại sao đầu tư), Project Charter (Ai thực thi) và Benefits Plan (Đo lường lợi ích) trên project-management.erx.vn.")}

<table>
  <thead>
    <tr>
      <th>Tiêu chí So sánh</th>
      <th>(02) Business Case (Bài toán Đầu tư)</th>
      <th>(01) Project Charter (Điều lệ Dự án)</th>
      <th>(03) Benefits Plan (Kế hoạch Lợi ích)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Câu hỏi Cốt lõi</strong></td>
      <td><em>"Tại sao doanh nghiệp nên bỏ tiền làm dự án này?"</em></td>
      <td><em>"Dự án làm gì, trong bao lâu, ngân sách bao nhiêu và ai chỉ huy?"</em></td>
      <td><em>"Khi nào thu được lợi ích và đo lường ROI bằng chỉ số nào?"</em></td>
    </tr>
    <tr>
      <td><strong>Người Chịu trách nhiệm</strong></td>
      <td>Project Sponsor &amp; Khối Tài chính / Chiến lược.</td>
      <td>Sponsor ký ban hành; Project Manager (PM) trực tiếp soạn thảo &amp; vận hành.</td>
      <td>Project Manager phối hợp cùng Trưởng bộ phận thụ hưởng (Business Owner).</td>
    </tr>
    <tr>
      <td><strong>Ví dụ Dự án <code>P2P-FOUNDATION-2026</code></strong></td>
      <td>Quy trình duyệt PR/PO thủ công mất 9 ngày, gây đứt gãy nguyên vật liệu. Đầu tư <code>$52,708</code> để hoàn vốn sau 4,5 tháng.</td>
      <td>Triển khai 20 bước WBS trong <strong>28 ngày</strong> với 7 phòng ban; <code>BAC = $49,448</code> + <code>EMV = $3,260</code>.</td>
      <td>Giảm <strong>45% Lead-time PR→PO</strong>; đạt <strong>100% đối soát 3-Way Match</strong> không sai lệch hóa đơn.</td>
    </tr>
  </tbody>
</table>

<h2>3. Cấu trúc 6 Thành phần Bắt buộc của một Bản Project Charter Chuẩn PMBOK® 8</h2>
<p>
  Khi mở tab <strong>Project Charter &amp; PMBOK Docs</strong> trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">ERX AI Project Gantt Planner</a>, một bản Điều lệ Dự án đạt chuẩn quốc tế luôn bao gồm 6 khối thông tin định lượng sau:
</p>
<ol>
  <li><strong>Mục tiêu Dự án &amp; Tiêu chí Thành công (Objectives &amp; Success Criteria):</strong> Phải định lượng theo chuẩn SMART (ví dụ: rút ngắn chu kỳ duyệt đơn mua hàng từ 9 ngày xuống dưới 5 ngày, tỷ lệ tuân thủ SLA nhà cung cấp đạt ≥ 95%).</li>
  <li><strong>Phạm vi Cấp cao &amp; Ranh giới Dự án (High-Level Scope &amp; Boundaries):</strong> Liệt kê rõ những gì nằm trong phạm vi (<em>In-Scope</em>: chuẩn hóa PR, RFQ, PO, GRN, 3-Way Matching, Supplier Scorecard) và những gì nằm ngoài phạm vi (<em>Out-of-Scope</em>: không thay đổi hệ thống kế toán thuế lõi) để chặn đứng <em>Scope Creep</em> ngay từ ngày đầu.</li>
  <li><strong>Lộ trình Cột mốc Tóm tắt (Summary Milestone Schedule):</strong> Tự động trích xuất các Task có <code>Duration = 0 ngày</code> từ bảng <a href="{URL_PM04}">Cấu trúc Phân rã Công việc (WBS)</a> (như <em>M1: Phê duyệt Charter</em>, <em>M2: Chốt danh sách NCC</em>, <em>M3: Go-Live hệ thống P2P</em>).</li>
  <li><strong>Ngân sách Phê duyệt Tự động (Approved Budget Synchronization):</strong> Thay vì gõ tay một con số ước chừng, nền tảng tự động cộng tổng chi phí cơ sở <a href="{URL_PM08}"><code>BAC = $49,448</code></a> với quỹ dự phòng rủi ro <a href="{URL_PM09}"><code>EMV = $3,260</code></a> để hiển thị chính xác <strong>Approved Budget = $52,708</strong>.</li>
  <li><strong>Giả định &amp; Ràng buộc Trọng yếu (Key Assumptions &amp; Constraints):</strong> Liên kết trực tiếp với hồ sơ số <code>(09) Assumption &amp; Constraint Log</code>.</li>
  <li><strong>Danh sách Bên liên quan Chính &amp; Thẩm quyền của PM:</strong> Xác định rõ Sponsor ký duyệt, quyền hạn của PM đối với ngân sách dự phòng và cơ chế leo thang xử lý sự cố (<em>Escalation Path</em>).</li>
</ol>

{CTA_BOX_HTML}

<h2>4. Bài viết Liên quan trong Hệ sinh thái Quản trị Dự án PMBOK® 8</h2>
<ul>
  <li>📘 <strong>Trụ cột 1 (Tổng quan PMBOK 8):</strong> <a href="{URL_PM01}">Quản trị Dự án theo chuẩn PMBOK 8: Tổng quan 6 Nguyên tắc, 7 Miền hiệu suất &amp; 5 Nhóm quy trình thực chiến</a>.</li>
  <li>🌳 <strong>Trụ cột 2 (Phân rã WBS):</strong> <a href="{URL_PM04}">Cấu trúc Phân rã Công việc (WBS) &amp; Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8</a>.</li>
  <li>📊 <strong>Trụ cột 3 (Kiểm soát Ngân sách EVM):</strong> <a href="{URL_PM08}">Quản lý Giá trị Thu được (Earned Value Management - EVM): Cách tính BAC, PV, EV, AC, SPI, CPI &amp; Dự báo EAC</a>.</li>
  <li>🛡️ <strong>Trụ cột 4 (Định lượng Rủi ro EMV):</strong> <a href="{URL_PM09}">Định lượng Rủi ro Dự án bằng EMV (Expected Monetary Value) &amp; Cách tính Quỹ Dự phòng (Contingency Reserve)</a>.</li>
</ul>

<h2>5. Câu hỏi Thường gặp (FAQ) về Project Charter &amp; Business Case</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: Ai là người ký ban hành Project Charter?</h3>
  <p>
    Mặc dù Giám đốc Dự án (PM) thường là người trực tiếp chấp bút soạn thảo <em>Project Charter</em>, nhưng người ký ban hành bắt buộc phải là <strong>Project Sponsor (Nhà tài trợ dự án)</strong> hoặc lãnh đạo có thẩm quyền cấp ngân sách cao hơn PM, nhằm trao quyền hợp pháp cho PM điều phối các phòng ban.
  </p>
  <h3>Câu hỏi 2: Project Charter có được phép sửa đổi trong quá trình chạy dự án không?</h3>
  <p>
    Project Charter là văn bản định hướng cấp cao nên rất ít khi thay đổi. Tuy nhiên, nếu có biến động lớn về phạm vi, ngân sách cơ sở (<code>BAC</code>) hoặc quỹ rủi ro (<code>EMV</code>) được Sponsor phê duyệt qua quy trình kiểm soát thay đổi, hệ thống <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a> sẽ tự động đồng bộ lại số liệu <em>Approved Budget</em> và danh sách <em>Milestones</em> trên Charter.
  </p>
  <h3>Câu hỏi 3: Làm sao để tạo nhanh Project Charter cho dự án mới trong 1 phút?</h3>
  <p style="margin-bottom: 0;">
    Bạn chỉ cần mở <code>project-management.erx.vn</code>, nhập mô tả mục tiêu dự án vào trợ lý <strong>AI Project Co-Pilot</strong>, hệ thống sẽ tự động sinh trọn bộ <em>Project Charter</em>, <em>Business Case</em>, <em>Benefits Plan</em> cùng bảng WBS 20 bước chuẩn PMBOK 8.
  </p>
</div>
"""

# ==============================================================================
# PM-03: RACI MATRIX & STAKEHOLDER REGISTER
# ==============================================================================
pm03_html = f"""
<h2>1. Tại sao Dự án Đa phòng ban Thường Thất bại vì "Cha chung không ai khóc"?</h2>
<p>
  Trong các dự án chuyển đổi số Chuỗi cung ứng (Supply Chain), Mua hàng (Procurement) hay triển khai ERP, công việc không bao giờ nằm gọn trong một phòng ban duy nhất. Lấy ví dụ dự án chuẩn hóa quy trình <strong>Procure-to-Pay (<code>P2P-FOUNDATION-2026</code>)</strong> trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a> có sự tham gia của <strong>7 đơn vị</strong>: Ban dự án (PMO), Phòng Mua hàng (Procurement), Tài chính – Kế toán (Finance/AP), Kho vận (Warehouse), Kiểm soát Chất lượng (QA/QC), Công nghệ Thông tin (IT/ERP) và Nhà cung cấp (Suppliers).
</p>
<p>
  Nếu chỉ giao việc chung chung kiểu <em>"Phòng Mua hàng phối hợp với Phòng Tài chính lập quy trình duyệt PO"</em>, khi trễ hạn cả hai bên sẽ đổ lỗi cho nhau. Để giải quyết triệt để bài toán này, miền hiệu suất <strong>Stakeholders (Bên liên quan)</strong> trong <a href="{URL_PM01}"><strong>PMBOK® Guide – 8th Edition</strong></a> yêu cầu kết hợp chặt chẽ 3 công cụ: <strong>(04) Stakeholder Register</strong>, <strong>(05) RACI Matrix</strong> và <strong>(06) Communication Plan</strong>.
</p>

<h2>2. Phân tích Bên liên quan bằng Lưới Quyền lực – Mức độ Quan tâm (Power / Interest Grid)</h2>
<p>
  Trước khi phân công công việc, Giám đốc Dự án cần lập <strong>Sổ đăng ký Bên liên quan (Stakeholder Register)</strong> và chấm điểm từng cá nhân/bộ phận theo 2 trục định lượng từ <code>1</code> đến <code>5</code>: <strong>Quyền lực (Power/Authority)</strong> và <strong>Mức độ Quan tâm (Interest/Impact)</strong>:
</p>

{figure_html("/Media/images/pm03_2_stakeholder_power_interest_grid_light.jpg", "Ma trận phân tích bên liên quan Power Interest Grid chuẩn PMBOK 8 trong dự án chuỗi cung ứng", "Hình 1: Lưới Power / Interest 4 góc phần tư giúp xác định chiến lược tương tác chính xác cho từng nhóm Stakeholder trên project-management.erx.vn.")}

<ul>
  <li><strong>Góc 1 — Quyền lực Cao &amp; Quan tâm Cao (Manage Closely - Quản lý sát sao):</strong> Bao gồm <em>Project Sponsor</em> và <em>Giám đốc Mua hàng (CPO)</em>. Đây là những người quyết định ngân sách và nghiệm thu dự án, cần được mời họp tại mọi cổng phê duyệt (Stage Gate) và nhận cảnh báo tiến độ tức thời.</li>
  <li><strong>Góc 2 — Quyền lực Cao &amp; Quan tâm Thấp (Keep Satisfied - Giữ hài lòng):</strong> Bao gồm <em>Giám đốc Tài chính (CFO)</em> hoặc <em>Ban Pháp chế</em>. Họ không cần nhận thông báo về từng bước lập trình nhỏ, nhưng phải được đảm bảo các chốt chặn kiểm soát ngân sách (<a href="{URL_PM08}"><code>CPI ≥ 1.0</code></a>) và mẫu hợp đồng khung không bị vi phạm.</li>
  <li><strong>Góc 3 — Quyền lực Thấp &amp; Quan tâm Cao (Keep Informed - Thông tin đầy đủ):</strong> Bao gồm đội ngũ trực tiếp vận hành như <em>Chuyên viên Mua hàng (Buyer)</em>, <em>Thủ kho nhận hàng (GRN)</em>, <em>Kế toán thanh toán (AP)</em>. Cần lấy ý kiến của họ khi thiết kế biểu mẫu và tổ chức đào tạo SOP kỹ lưỡng.</li>
  <li><strong>Góc 4 — Quyền lực Thấp &amp; Quan tâm Thấp (Monitor - Theo dõi định kỳ):</strong> Các phòng ban ít phát sinh mua sắm, chỉ cần gửi bản tin tổng hợp khi dự án Go-Live.</li>
</ul>

<h2>3. Giải mã Ma trận Phân quyền RACI &amp; 3 Quy tắc Kiểm toán Bắt buộc</h2>
<p>
  Sau khi nhận diện đầy đủ các bên liên quan, mọi gói công việc trong <a href="{URL_PM04}"><strong>Cấu trúc Phân rã Công việc (WBS)</strong></a> đều phải được ánh xạ vào <strong>Ma trận RACI</strong> với 4 chữ cái định danh:
</p>
<ul>
  <li><strong>R — Responsible (Người trực tiếp thực thi):</strong> Cá nhân hoặc bộ phận trực tiếp bỏ giờ công thực hiện gói công việc. Một việc có thể có một hoặc nhiều chữ <code>R</code> cùng phối hợp.</li>
  <li><strong>A — Accountable (Người chịu trách nhiệm giải trình cuối cùng):</strong> Người có quyền phê duyệt nghiệm thu kết quả của chữ <code>R</code> và chịu trách nhiệm trước Ban Giám đốc nếu gói công việc thất bại.</li>
  <li><strong>C — Consulted (Người được tham vấn — Giao tiếp 2 chiều):</strong> Chuyên gia cung cấp dữ liệu đầu vào hoặc ý kiến phản biện trước khi thực thi.</li>
  <li><strong>I — Informed (Người được thông báo — Giao tiếp 1 chiều):</strong> Người cần được cập nhật kết quả sau khi công việc hoàn thành để chuẩn bị cho bước tiếp theo.</li>
</ul>

<table>
  <thead>
    <tr>
      <th>Mã WBS &amp; Gói Công việc (Dự án P2P)</th>
      <th>PMO</th>
      <th>Mua hàng</th>
      <th>Tài chính</th>
      <th>Kho &amp; QA</th>
      <th>CNTT (IT)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1.1</strong> Phê duyệt Project Charter &amp; Ngân sách</td>
      <td><strong>A</strong></td>
      <td><strong>R</strong></td>
      <td><strong>C</strong></td>
      <td>I</td>
      <td>I</td>
    </tr>
    <tr>
      <td><strong>1.3</strong> Thiết lập Quy tắc Kiểm tra Ngân sách PR</td>
      <td>I</td>
      <td><strong>C</strong></td>
      <td><strong>A</strong></td>
      <td>I</td>
      <td><strong>R</strong></td>
    </tr>
    <tr>
      <td><strong>2.2</strong> Xây dựng Ma trận Chấm điểm Nhà cung cấp</td>
      <td>I</td>
      <td><strong>A / R</strong></td>
      <td><strong>C</strong></td>
      <td><strong>C</strong></td>
      <td>I</td>
    </tr>
    <tr>
      <td><strong>4.3</strong> Cấu hình Chốt chặn Đối soát 3 bên (3-Way Match)</td>
      <td>I</td>
      <td><strong>C</strong></td>
      <td><strong>A</strong></td>
      <td><strong>C</strong></td>
      <td><strong>R</strong></td>
    </tr>
  </tbody>
</table>

<p>
  Đặc biệt, công cụ kiểm toán RACI trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a> tự động quét từng dòng WBS theo <strong>3 Quy tắc Vàng chuẩn PMBOK 8</strong>:
</p>
<ol>
  <li><strong>Quy tắc Duy nhất 1 chữ A:</strong> Mỗi gói công việc bắt buộc phải có <strong>đúng 1 chữ A duy nhất</strong>. Nếu không có chữ A, công việc bị vô chủ; nếu có từ 2 chữ A trở lên, sẽ xảy ra đùn đẩy hoặc xung đột quyền phán quyết.</li>
  <li><strong>Quy tắc Tối thiểu 1 chữ R:</strong> Mọi gói công việc phải có ít nhất một người trực tiếp làm (có thể một người vừa là <code>A</code> vừa là <code>R</code> cho các việc gọn nhẹ).</li>
  <li><strong>Tránh lạm dụng chữ C:</strong> Nếu một dòng có quá nhiều chữ <code>C</code>, thời gian chờ xin ý kiến các phòng ban sẽ làm đình trệ tiến độ Đường găng. Hãy chuyển những người không thực sự cần phản biện sang chữ <code>I</code>.</li>
</ol>

{CTA_BOX_HTML}

<h2>4. Bài viết Liên quan trong Hệ sinh thái Quản trị Dự án PMBOK® 8</h2>
<ul>
  <li>📘 <strong>Tổng quan PMBOK 8:</strong> <a href="{URL_PM01}">Quản trị Dự án theo chuẩn PMBOK 8: Tổng quan 6 Nguyên tắc, 7 Miền hiệu suất &amp; 5 Nhóm quy trình thực chiến</a>.</li>
  <li>🌳 <strong>Xây dựng WBS &amp; Từ điển WBS:</strong> <a href="{URL_PM04}">Cấu trúc Phân rã Công việc (WBS) &amp; Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8</a>.</li>
  <li>🤝 <strong>Quản trị Mua hàng &amp; Nhà cung cấp:</strong> Khám phá chuyên mục <a href="https://erx.vn/procurement-management.html">Procurement Management</a>.</li>
</ul>

<h2>5. Câu hỏi Thường gặp (FAQ) về Ma trận RACI &amp; Stakeholder Register</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: Một người có thể vừa là A (Accountable) vừa là R (Responsible) trong cùng 1 Task không?</h3>
  <p>
    Hoàn toàn được phép. Trong các gói công việc chuyên môn do chính Trưởng bộ phận trực tiếp thực hiện và tự phê duyệt đầu ra, ô giao điểm của người đó trên Ma trận RACI sẽ được gán là <code>A/R</code>.
  </p>
  <h3>Câu hỏi 2: Sự khác biệt lớn nhất giữa chữ C (Consulted) và chữ I (Informed) là gì?</h3>
  <p>
    Chữ <strong>C (Consulted)</strong> là giao tiếp <strong>2 chiều trước khi chốt quyết định</strong> (bạn phải hỏi ý kiến họ và chờ họ phản hồi), còn chữ <strong>I (Informed)</strong> là giao tiếp <strong>1 chiều sau khi đã có kết quả</strong> (chỉ thông báo để họ nắm thông tin, không cần chờ họ duyệt).
  </p>
  <h3>Câu hỏi 3: Ma trận RACI trên project-management.erx.vn liên kết thế nào với Communication Plan?</h3>
  <p style="margin-bottom: 0;">
    Trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, các bên được gán vai trò <code>A</code> và <code>I</code> trong Ma trận RACI sẽ tự động được liên kết với <strong>(06) Communication Plan</strong> và hệ thống cảnh báo <strong>Executive Diff qua Telegram</strong> mỗi khi gói công việc được cập nhật.
  </p>
</div>
"""

# ==============================================================================
# PM-05: 4 PDM DEPENDENCIES (FS, SS, FF, SF) & FAST-TRACKING
# ==============================================================================
pm05_html = f"""
<h2>1. Phương pháp Biểu đồ Tiền nhiệm (Precedence Diagramming Method - PDM) là gì?</h2>
<p>
  Sau khi đã chia nhỏ dự án thành các gói công việc trong <a href="{URL_PM04}"><strong>Cấu trúc Phân rã Công việc (WBS)</strong></a>, bước quyết định để tạo nên một lịch trình sống động là thiết lập mạng logic phụ thuộc giữa các công việc theo <strong>Phương pháp Biểu đồ Tiền nhiệm (PDM)</strong> thuộc miền hiệu suất <em>Tiến độ (Schedule Performance Domain)</em> của <a href="{URL_PM01}"><strong>PMBOK® 8</strong></a>.
</p>
<p>
  Nếu bạn chỉ gõ ngày bắt đầu và ngày kết thúc cố định cho từng dòng (giống như kẻ bảng trên Excel), lịch trình của bạn sẽ "chết cứng" ngay khi một công việc bị trễ. Ngược lại, khi sử dụng động cơ PDM chuẩn <strong>Microsoft Project 2016 Parity</strong> trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>project-management.erx.vn</strong></a>, mọi công việc được kết nối bằng <strong>4 loại quan hệ phụ thuộc (FS, SS, FF, SF)</strong> kết hợp cùng độ trễ <strong>Lag (+)</strong> và độ sớm <strong>Lead (-)</strong>.
</p>

<h2>2. Giải mã Chi tiết 4 Mối quan hệ Phụ thuộc (FS, SS, FF, SF) Kèm Ví dụ Thực tế</h2>
<p>
  Giả sử chúng ta có công việc đứng trước là <strong>Task A (Predecessor - Tiền nhiệm)</strong> và công việc đứng sau là <strong>Task B (Successor - Kế nhiệm)</strong>:
</p>

<table>
  <thead>
    <tr>
      <th>Mã Quan hệ</th>
      <th>Tên đầy đủ &amp; Quy tắc Logic</th>
      <th>Công thức Tính Ngày trên Gantt</th>
      <th>Tình huống Thực chiến trong Dự án Chuỗi Cung Ứng (P2P)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong><code>FS</code></strong></td>
      <td><strong>Finish-to-Start</strong><br><em>(Kết thúc – Bắt đầu)</em></td>
      <td>Task A phải hoàn thành 100% thì Task B mới được phép bắt đầu.</td>
      <td><strong>Bước 2.4</strong> (Phê duyệt kết quả chọn Nhà cung cấp) hoàn tất → mới bắt đầu <strong>Bước 3.1</strong> (Soạn thảo Hợp đồng mua bán).</td>
    </tr>
    <tr>
      <td><strong><code>SS</code></strong></td>
      <td><strong>Start-to-Start</strong><br><em>(Bắt đầu – Bắt đầu)</em></td>
      <td>Task A bắt đầu thì Task B cũng được phép bắt đầu song song.</td>
      <td><strong>Bước 1.2</strong> (Chuẩn hóa biểu mẫu PR) bắt đầu được 1 ngày → <strong>Bước 1.3</strong> (Thiết lập quy tắc kiểm tra ngân sách) chạy gối đầu ngay (<code>2SS+1d</code>).</td>
    </tr>
    <tr>
      <td><strong><code>FF</code></strong></td>
      <td><strong>Finish-to-Finish</strong><br><em>(Kết thúc – Kết thúc)</em></td>
      <td>Task A phải hoàn thành thì Task B mới được chốt hoàn thành.</td>
      <td><strong>Bước 4.1</strong> (Nhập kho hàng hóa GRN) phải hoàn tất lô cuối cùng → <strong>Bước 4.2</strong> (Kiểm định chất lượng QA/QC) mới được đóng biên bản nghiệm thu (<code>FF</code>).</td>
    </tr>
    <tr>
      <td><strong><code>SF</code></strong></td>
      <td><strong>Start-to-Finish</strong><br><em>(Bắt đầu – Kết thúc)</em></td>
      <td>Task A (mới) phải bắt đầu vận hành thì Task B (cũ) mới được kết thúc.</td>
      <td>Hệ thống cổng mua hàng điện tử ERP mới chính thức <strong>Go-Live (Bắt đầu)</strong> → Quy trình duyệt giấy thủ công cũ mới được <strong>Ngừng hẳn (Kết thúc)</strong>.</td>
    </tr>
  </tbody>
</table>

<h2>3. Cách Sử dụng Độ trễ (Lag +) và Độ sớm (Lead -) theo 3 Đơn vị Chuẩn MS Project</h2>
<p>
  Trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, cú pháp nhập cột <code>Predecessors</code> hỗ trợ đầy đủ 3 định dạng thời gian chờ/gối đầu chuẩn quốc tế:
</p>
<ul>
  <li><strong>Ngày làm việc (Working Days — <code>d</code>):</strong> Ví dụ <code>5FS+2d</code> nghĩa là sau khi Task 5 kết thúc, phải chờ thêm 2 ngày làm việc (trừ Thứ Bảy, Chủ Nhật và ngày lễ) thì Task hiện tại mới bắt đầu.</li>
  <li><strong>Ngày lịch liên tục (Elapsed Days — <code>ed</code>):</strong> Ví dụ <code>8FS+7ed</code> dùng cho các quá trình vật lý hoặc thời hạn niêm yết thầu liên tục 7 ngày đêm (kể cả cuối tuần).</li>
  <li><strong>Phần trăm thời lượng (Percentage — <code>%</code>):</strong> Ví dụ <code>3FS-25%</code> (Lead 25%) nghĩa là khi Task 3 đã làm được 75% khối lượng (còn 25% cuối), Task kế tiếp được phép bắt đầu gối đầu ngay.</li>
</ul>

<h2>4. Kỹ thuật Nén Tiến độ Dự án: So sánh Fast-Tracking và Crashing</h2>
<p>
  Khi tổng thời gian tính ra vượt quá hạn chót của Ban Giám đốc (ví dụ lịch tuần tự ban đầu mất 34 ngày trong khi yêu cầu là <strong>28 ngày</strong>), chuẩn PMBOK 8 cung cấp 2 kỹ thuật nén tiến độ (<em>Schedule Compression</em>):
</p>

{figure_html("/Media/images/pm05_2_fast_tracking_vs_crashing_light.jpg", "So sánh kỹ thuật rút ngắn tiến độ dự án Fast-Tracking và Crashing chuẩn PMBOK 8", "Hình 1: So sánh trực quan giữa Fast-Tracking (gối đầu công việc bằng SS/FF không tốn thêm chi phí) và Crashing (bổ sung nguồn lực làm tăng chi phí trực tiếp).")}

<ol>
  <li><strong>Fast-Tracking (Làm gối đầu song song):</strong> Chuyển các mối quan hệ tuần tự <code>FS</code> trên Đường găng sang quan hệ gối đầu <code>SS+Lag</code> hoặc <code>FF</code>. Đây là kỹ thuật ưu tiên số 1 vì <strong>không làm tăng ngân sách cơ sở (<code>BAC</code>)</strong>, nhưng đòi hỏi sự phối hợp chặt chẽ giữa các phòng ban để tránh rủi ro làm lại (<em>Rework</em>).</li>
  <li><strong>Crashing (Tăng cường nguồn lực vào Đường găng):</strong> Bổ sung thêm nhân sự hoặc làm thêm giờ cho các gói công việc nằm trên Đường găng. Kỹ thuật này giúp giảm trực tiếp <code>Duration</code> của Task nhưng sẽ làm tăng chi phí và cần được kiểm soát qua chỉ số <a href="{URL_PM08}"><strong>CPI trong EVM</strong></a>.</li>
</ol>

{CTA_BOX_HTML}

<h2>5. Bài viết Liên quan trong Hệ sinh thái Quản trị Dự án PMBOK® 8</h2>
<ul>
  <li>🌳 <strong>Trụ cột 2 (Thiết kế WBS):</strong> <a href="{URL_PM04}">Cấu trúc Phân rã Công việc (WBS) &amp; Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8</a>.</li>
  <li>📘 <strong>Trụ cột 1 (Tổng quan PMBOK 8):</strong> <a href="{URL_PM01}">Quản trị Dự án theo chuẩn PMBOK 8: Tổng quan 6 Nguyên tắc, 7 Miền hiệu suất &amp; 5 Nhóm quy trình thực chiến</a>.</li>
  <li>📊 <strong>Trụ cột 3 (Kiểm soát Tiến độ &amp; Chi phí EVM):</strong> <a href="{URL_PM08}">Quản lý Giá trị Thu được (Earned Value Management - EVM): Cách tính BAC, PV, EV, AC, SPI, CPI &amp; Dự báo EAC</a>.</li>
</ul>

<h2>6. Câu hỏi Thường gặp (FAQ) về Quan hệ Phụ thuộc FS, SS, FF, SF</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: Giữa FS với độ sớm Lead (ví dụ 3FS-2d) và SS với độ trễ Lag (ví dụ 3SS+1d), nên dùng cách nào?</h3>
  <p>
    Theo khuyến nghị thực hành tốt nhất của PMI và chuẩn lập lịch trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, bạn nên ưu tiên dùng <strong><code>SS + Lag dương</code> (ví dụ <code>3SS+1d</code>)</strong> thay vì <code>FS - Lead âm</code>, vì điều kiện kích hoạt dựa trên sự kiện <em>"Task 3 đã bắt đầu được 1 ngày"</em> luôn rõ ràng và dễ kiểm soát hơn trong thực tế.
  </p>
  <h3>Câu hỏi 2: Có nên gắn Predecessor cho các dòng Summary Task (Giai đoạn cha) không?</h3>
  <p>
    Tuyệt đối không nên. Trong chuẩn PMBOK 8, các mối quan hệ phụ thuộc <code>FS/SS/FF/SF</code> chỉ nên gắn trực tiếp giữa các <strong>Work Packages (Gói công việc lá)</strong> và <strong>Milestones</strong> để tránh tạo ra vòng lặp logic (<em>Circular Dependency</em>) và giúp Đường găng hiển thị chính xác.
  </p>
  <h3>Câu hỏi 3: Hệ thống project-management.erx.vn có chặn lỗi vòng lặp phụ thuộc (A phụ thuộc B, B phụ thuộc A) không?</h3>
  <p style="margin-bottom: 0;">
    Có. Động cơ kiểm toán đồ thị có hướng (DAG Validator) của <code>project-management.erx.vn</code> tự động phát hiện và chặn ngay lập tức mọi liên kết vòng lặp (Circular Reference) trước khi tính toán lại lịch trình.
  </p>
</div>
"""

# ==============================================================================
# PM-06: CRITICAL PATH METHOD (CPM), FREE SLACK & TOTAL SLACK
# ==============================================================================
pm06_html = f"""
<h2>1. Đường găng Dự án (Critical Path Method - CPM) là gì?</h2>
<p>
  Trong một dự án gồm hàng chục đến hàng trăm gói công việc đan xen nhau, không phải mọi sự chậm trễ đều có hậu quả giống nhau. Có những công việc bị trễ 3 ngày nhưng ngày bàn giao cuối cùng của dự án vẫn không hề suy chuyển; ngược lại, có những công việc chỉ cần trễ <strong>nửa ngày</strong> là toàn bộ lễ Go-Live của dự án bị đẩy lùi ngay lập tức.
</p>
<p>
  <strong>Phương pháp Đường găng (Critical Path Method - CPM)</strong> trong miền hiệu suất <em>Schedule</em> của <a href="{URL_PM01}"><strong>PMBOK® 8</strong></a> chính là thuật toán toán học xác định:
</p>
<ul>
  <li><strong>Đường găng (Critical Path):</strong> Là chuỗi các công việc phụ thuộc <strong>dài nhất</strong> xuyên suốt mạng dự án, quyết định trực tiếp tổng thời gian ngắn nhất có thể để hoàn thành dự án.</li>
  <li><strong>Công việc Găng (Critical Task):</strong> Các gói công việc nằm trên Đường găng có <strong>Độ dự trữ toàn phần bằng không (<code>Total Slack = 0</code>)</strong>. Trên giao diện Gantt của <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>project-management.erx.vn</strong></a>, các thanh công việc găng và mũi tên nối giữa chúng được tự động tô màu đỏ nổi bật.</li>
</ul>

<h2>2. Công thức Tính Toán Lượt đi (Forward Pass) và Lượt về (Backward Pass) trong CPM</h2>
<p>
  Mỗi khi bạn thay đổi thời lượng (<code>Duration</code>) hoặc mối quan hệ phụ thuộc (<code>FS/SS/FF/SF</code>) của bất kỳ dòng nào trong <a href="{URL_PM04}">bảng WBS</a>, động cơ CPM của <code>project-management.erx.vn</code> lập tức chạy 2 lượt tính toán chỉ trong vài mili-giây:
</p>
<ol>
  <li><strong>Lượt đi (Forward Pass — Tính từ ngày khởi công sang phải):</strong> Tìm ngày bắt đầu sớm nhất (<code>ES - Early Start</code>) và ngày kết thúc sớm nhất (<code>EF - Early Finish</code>) của mọi công việc:
    <br><code>ES = Max(EF của tất cả các Task tiền nhiệm)</code>
    <br><code>EF = ES + Duration</code>
  </li>
  <li><strong>Lượt về (Backward Pass — Tính ngược từ ngày kết thúc dự án về trái):</strong> Tìm ngày kết thúc muộn nhất cho phép (<code>LF - Late Finish</code>) và ngày bắt đầu muộn nhất cho phép (<code>LS - Late Start</code>) mà không làm trễ dự án:
    <br><code>LF = Min(LS của tất cả các Task kế nhiệm)</code>
    <br><code>LS = LF - Duration</code>
  </li>
</ol>

<h2>3. Phân biệt Sống còn giữa Free Slack (Độ dự trữ Tự do) và Total Slack (Độ dự trữ Toàn phần)</h2>
<p>
  Từ kết quả của Lượt đi và Lượt về, chuẩn PMBOK 8 tách bạch 2 chỉ số dự trữ thời gian (<em>Float / Slack</em>) mà mọi Giám đốc Dự án cần nắm vững:
</p>

{figure_html("/Media/images/pm06_2_free_slack_vs_total_slack_light.jpg", "Phân biệt Free Slack và Total Slack trong phương pháp đường găng CPM chuẩn PMBOK 8", "Hình 1: Sự khác biệt cốt lõi giữa Free Slack (không làm trễ Task kế tiếp ngay sau nó) và Total Slack (không làm trễ ngày kết thúc toàn dự án).")}

<table>
  <thead>
    <tr>
      <th>Tiêu chí</th>
      <th>Free Slack (Độ dự trữ Tự do)</th>
      <th>Total Slack (Độ dự trữ Toàn phần)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Định nghĩa</strong></td>
      <td>Khoảng thời gian một Task có thể bị trễ mà <strong>không làm trễ ngày bắt đầu sớm nhất (<code>ES</code>) của bất kỳ Task kế tiếp nào</strong> ngay sau nó.</td>
      <td>Khoảng thời gian một Task có thể bị trễ mà <strong>không làm trễ ngày kết thúc chung (<code>Finish Date</code>) của toàn bộ dự án</strong>.</td>
    </tr>
    <tr>
      <td><strong>Công thức Tính</strong></td>
      <td><code>Free Slack = Min(ES của Task kế tiếp) - EF của Task hiện tại</code></td>
      <td><code>Total Slack = LS - ES = LF - EF</code></td>
    </tr>
    <tr>
      <td><strong>Quyền Sử dụng trong Điều hành</strong></td>
      <td><strong>Thuộc quyền chủ động của Trưởng nhóm / PM:</strong> Dùng để giãn lịch nhân sự bị quá tải (<em>Resource Leveling</em>) mà không ảnh hưởng đến phòng ban nhận bàn giao tiếp theo.</td>
      <td><strong>Tài sản dự phòng của toàn dự án:</strong> Nếu một Task tiêu hết <code>Total Slack</code> của một nhánh, tất cả các Task phía sau trên nhánh đó sẽ biến thành Task Găng (<code>Slack = 0</code>)!</td>
    </tr>
  </tbody>
</table>

<h2>4. Hiện tượng Đường găng Dịch chuyển (Shifting Critical Path) &amp; Negative Float</h2>
<p>
  Đường găng không phải là một đường cố định từ đầu đến cuối dự án. Trong quá trình thực thi:
</p>
<ul>
  <li><strong>Gần Găng (Near-Critical Path):</strong> Những nhánh công việc có <code>Total Slack = 1–2 ngày</code> cần được theo dõi sát sao không kém Đường găng chính, vì chỉ cần một sự cố nhỏ ở nhà cung cấp là nhánh đó sẽ vượt lên thành Đường găng mới.</li>
  <li><strong>Độ dự trữ Âm (Negative Float / Slack &lt; 0):</strong> Khi bạn đặt ràng buộc cứng như <em>Must Finish On (MFO)</em> hoặc khi tiến độ thực tế bị trễ vượt quá ngày kết thúc mục tiêu, <code>Total Slack</code> sẽ mang giá trị âm (ví dụ <code>-3d</code>), báo hiệu bạn bắt buộc phải áp dụng <em>Fast-Tracking</em> hoặc <em>Crashing</em> ngay lập tức để bù lại 3 ngày bị hụt.</li>
</ul>

{CTA_BOX_HTML}

<h2>5. Bài viết Liên quan trong Hệ sinh thái Quản trị Dự án PMBOK® 8</h2>
<ul>
  <li>🌳 <strong>Trụ cột 2 (Cấu trúc WBS):</strong> <a href="{URL_PM04}">Cấu trúc Phân rã Công việc (WBS) &amp; Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8</a>.</li>
  <li>📊 <strong>Trụ cột 3 (Đo lường Tiến độ SPI &amp; Chi phí CPI):</strong> <a href="{URL_PM08}">Quản lý Giá trị Thu được (Earned Value Management - EVM): Cách tính BAC, PV, EV, AC, SPI, CPI &amp; Dự báo EAC</a>.</li>
  <li>🛡️ <strong>Trụ cột 4 (Dự phòng Rủi ro EMV):</strong> <a href="{URL_PM09}">Định lượng Rủi ro Dự án bằng EMV (Expected Monetary Value) &amp; Cách tính Quỹ Dự phòng (Contingency Reserve)</a>.</li>
</ul>

<h2>6. Câu hỏi Thường gặp (FAQ) về Phương pháp Đường găng (CPM)</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: Một dự án có thể có nhiều hơn 1 Đường găng cùng lúc không?</h3>
  <p>
    Có. Nếu dự án có hai hoặc nhiều nhánh công việc song song cùng có tổng thời lượng dài nhất bằng nhau (cùng có <code>Total Slack = 0</code>), dự án sẽ có <strong>nhiều Đường găng song song</strong>. Khi đó, rủi ro trễ hạn của dự án tăng lên gấp đôi và cần được ưu tiên giám sát.
  </p>
  <h3>Câu hỏi 2: Free Slack có bao giờ lớn hơn Total Slack không?</h3>
  <p>
    Không bao giờ. Về mặt toán học, luôn luôn có <code>0 ≤ Free Slack ≤ Total Slack</code>. Khi <code>Total Slack = 0</code> (công việc nằm trên Đường găng), <code>Free Slack</code> của công việc đó cũng bắt buộc bằng <code>0</code>.
  </p>
  <h3>Câu hỏi 3: Làm sao bật hiển thị Đường găng màu đỏ trên project-management.erx.vn?</h3>
  <p style="margin-bottom: 0;">
    Trên thanh công cụ của <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, tính năng <strong>Critical Path Highlight</strong> được bật mặc định: mọi Task có <code>Total Slack ≤ 0</code> và đường dây liên kết giữa chúng được tô đỏ tức thời ngay khi bạn chỉnh sửa lịch trình.
  </p>
</div>
"""

# ==============================================================================
# PM-07: EXCEL GANTT VS MS PROJECT VS ERX AI GANTT PLANNER
# ==============================================================================
pm07_html = f"""
<h2>1. Thực trạng: Tại sao 70% Dự án Dùng Excel Vẽ Biểu đồ Gantt Bị Trượt Tiến độ?</h2>
<p>
  Microsoft Excel là công cụ tuyệt vời để phân tích bảng tính và xử lý dữ liệu (bạn có thể xem thêm các kỹ thuật nâng cao tại chuyên mục <a href="https://erx.vn/excel-functions.html">Excel Functions</a> của ERX). Tuy nhiên, khi một dự án vượt quá 15 đầu việc và có từ 3 phòng ban trở lên cùng tham gia, việc <strong>tô màu các ô Excel hoặc dùng Conditional Formatting để giả lập biểu đồ Gantt</strong> sẽ nhanh chóng bộc lộ <strong>6 điểm gãy chí mạng</strong>:
</p>
<ol>
  <li><strong>Không có Động cơ Lập lịch Mạng (No Network Scheduling Engine):</strong> Excel không hiểu khái niệm lịch làm việc (trừ Thứ Bảy, Chủ Nhật, nghỉ lễ Tết) kết hợp với 4 mối quan hệ phụ thuộc <code>FS, SS, FF, SF</code> và độ trễ <code>Lag/Lead</code>. Khi một công việc ở tuần thứ 2 bị trễ 3 ngày, người quản lý phải ngồi sửa tay lại ngày tháng của hàng chục dòng bên dưới.</li>
  <li><strong>Mù mờ về Đường găng (Critical Path Blindness):</strong> Bảng Excel không thể tự chạy thuật toán Lượt đi (<code>ES/EF</code>) và Lượt về (<code>LS/LF</code>) để chỉ ra đâu là chuỗi công việc găng (<code>Total Slack = 0</code>) đang quyết định ngày kết thúc dự án.</li>
  <li><strong>Không thể Cân bằng Nguồn lực (No Resource Leveling):</strong> Khi một kỹ sư hoặc chuyên viên mua hàng bị giao 3 việc trùng nhau trong cùng một tuần (quá tải <code>300%</code>), file Excel hoàn toàn im lặng cho đến khi nhân sự đó không kịp bàn giao.</li>
  <li><strong>Không có Hệ thống Baseline để Tính 9 Chỉ số EVM:</strong> Excel không có cơ chế chụp ảnh 11 mốc <code>Baseline</code> độc lập để so sánh tiến độ kế hoạch (<code>PV</code>) với giá trị thu được (<code>EV</code>) và chi phí thực tế (<code>AC</code>) theo chuẩn <a href="{URL_PM08}"><strong>Earned Value Management (EVM)</strong></a>.</li>
  <li><strong>Rời rạc giữa Tiến độ, Rủi ro EMV và 13 Hồ sơ PMBOK:</strong> Ngân sách trên bảng tiến độ Excel không tự động đồng bộ với bảng đánh giá rủi ro <a href="{URL_PM09}"><code>EMV = P% × Impact($)</code></a> và bản <em>Project Charter</em> trên Word.</li>
  <li><strong>Hỗn loạn Phiên bản khi Cộng tác (Version Chaos):</strong> Việc gửi file <code>Ke_hoach_v1_final_updated.xlsx</code> qua email/Zalo khiến Ban Giám đốc không bao giờ biết đâu là số liệu mới nhất và ai vừa sửa lùi ngày hoàn thành.</li>
</ol>

<h2>2. Bảng So sánh Toàn diện: Excel vs. MS Project Desktop vs. ERX AI Project Gantt Planner</h2>
<p>
  Để khắc phục sự cồng kềnh và chi phí bản quyền đắt đỏ của phần mềm cài đặt truyền thống nhưng vẫn giữ nguyên <strong>100% sức mạnh tính toán chuẩn quốc tế</strong>, nền tảng <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>project-management.erx.vn</strong></a> được xây dựng theo kiến trúc <strong>Microsoft Project 2016 Parity trên Đám mây kết hợp AI</strong>:
</p>

{figure_html("/Media/images/pm07_2_msp_parity_architecture_light.jpg", "Kiến trúc chuẩn Microsoft Project 2016 Parity kết hợp Cloud PMO và AI trên project-management.erx.vn", "Hình 1: 4 trụ cột kiến trúc của ERX AI Project Gantt Planner kết hợp độ chính xác của MS Project 2016 với cộng tác đám mây và AI.")}

<table>
  <thead>
    <tr>
      <th>Tính năng Quản trị Dự án</th>
      <th>Bảng tính Excel Thủ công</th>
      <th>MS Project Desktop (.mpp)</th>
      <th>ERX AI Gantt Planner (<code>project-management.erx.vn</code>)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Động cơ WBS, PDM (<code>FS/SS/FF/SF</code>) &amp; CPM</strong></td>
      <td>❌ Không có (phải gõ tay hoặc công thức dễ gãy)</td>
      <td>✅ Đầy đủ chuẩn công nghiệp</td>
      <td>✅ <strong>Chuẩn MS Project 2016 Parity</strong> (tự động tính <code>ES/EF/LS/LF</code> &amp; tô đỏ Đường găng)</td>
    </tr>
    <tr>
      <td><strong>Quản trị Nguồn lực &amp; Resource Leveling</strong></td>
      <td>❌ Không có</td>
      <td>✅ Có (3 Task Types, 9 Contours, Leveling)</td>
      <td>✅ <strong>Đầy đủ 3 Task Types, 9 Work Contours, Rate Tables A–E &amp; Auto Leveling</strong></td>
    </tr>
    <tr>
      <td><strong>Quản lý 11 Baselines &amp; 9 Chỉ số EVM</strong></td>
      <td>❌ Phải tự dựng bảng phụ phức tạp</td>
      <td>✅ Có 11 Baselines &amp; EVM</td>
      <td>✅ <strong>11 Baselines + Dashboard 9 chỉ số EVM &amp; Đồ thị S-Curve trực quan</strong></td>
    </tr>
    <tr>
      <td><strong>Tích hợp 13 Hồ sơ PMBOK® 8 &amp; Quỹ Rủi ro EMV</strong></td>
      <td>❌ Tách rời trên nhiều file Word/Excel</td>
      <td>❌ Không tích hợp sẵn 13 hồ sơ PMBOK</td>
      <td>✅ <strong>Tích hợp sẵn 13 Hồ sơ PMBOK 8 &amp; Tự động cộng <code>BAC + EMV = Approved Budget</code></strong></td>
    </tr>
    <tr>
      <td><strong>Cộng tác Đám mây &amp; Cảnh báo Điều hành</strong></td>
      <td>⚠️ Dễ ghi đè dữ liệu của nhau</td>
      <td>❌ File <code>.mpp</code> cục bộ khó chia sẻ</td>
      <td>✅ <strong>Cloud Check-out/Check-in + Báo cáo <code>Executive Diff</code> tự động qua Telegram</strong></td>
    </tr>
    <tr>
      <td><strong>Trợ lý AI Co-Pilot &amp; Giao thức MCP</strong></td>
      <td>❌ Không có</td>
      <td>❌ Không có</td>
      <td>✅ <strong>AI Co-Pilot khởi tạo dự án tự động &amp; MCP Server cho AI Agent</strong></td>
    </tr>
  </tbody>
</table>

<h2>3. Chuyển đổi Mượt mà: Nhập/Xuất Hai chiều giữa Excel (<code>.xlsx</code>) và AI Gantt Planner</h2>
<p>
  Hiểu rõ thói quen làm việc với dữ liệu bảng của các chuyên gia Chuỗi cung ứng và PMO, <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a> không bắt bạn từ bỏ Excel mà biến Excel thành kênh trao đổi dữ liệu hai chiều:
</p>
<ul>
  <li><strong>Import từ Excel / JSON trong 3 giây:</strong> Nếu bạn đã có danh sách đầu việc trên Excel, bạn có thể nạp thẳng vào hệ thống để động cơ CPM lập tức dựng cây <a href="{URL_PM04}">WBS đa cấp</a>, tính Đường găng và phát hiện xung đột nguồn lực.</li>
  <li><strong>Export Báo cáo Chuẩn Quốc tế:</strong> Xuất toàn bộ bảng tiến độ, bảng phân tích EVM và 13 hồ sơ PMBOK 8 ra file <code>.xlsx</code> nhiều sheet hoặc bản in PDF điều hành chỉ với 1 cú nhấp chuột.</li>
</ul>

{CTA_BOX_HTML}

<h2>4. Bài viết Liên quan trong Hệ sinh thái Quản trị Dự án &amp; Phân tích Dữ liệu</h2>
<ul>
  <li>📘 <strong>Tổng quan PMBOK 8:</strong> <a href="{URL_PM01}">Quản trị Dự án theo chuẩn PMBOK 8: Tổng quan 6 Nguyên tắc, 7 Miền hiệu suất &amp; 5 Nhóm quy trình thực chiến</a>.</li>
  <li>🌳 <strong>Xây dựng WBS chuẩn PMBOK 8:</strong> <a href="{URL_PM04}">Cấu trúc Phân rã Công việc (WBS) &amp; Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8</a>.</li>
  <li>📊 <strong>Kiểm soát Chi phí EVM:</strong> <a href="{URL_PM08}">Quản lý Giá trị Thu được (Earned Value Management - EVM): Cách tính BAC, PV, EV, AC, SPI, CPI &amp; Dự báo EAC</a>.</li>
  <li>📈 <strong>Tự động hóa Báo cáo Doanh nghiệp:</strong> Xem thêm tại <a href="https://erx.vn/dashboard-automated-report.html">Dashboard &amp; Automated Report</a>.</li>
</ul>

<h2>5. Câu hỏi Thường gặp (FAQ) khi Chuyển từ Excel sang Phần mềm Quản lý Dự án</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: Khi nào thì một bảng checklist trên Excel là đủ, và khi nào bắt buộc phải dùng Gantt CPM?</h3>
  <p>
    Nếu công việc chỉ có dưới 10 đầu mục độc lập do 1 cá nhân tự làm trong vài ngày, một bảng checklist đơn giản là đủ. Nhưng ngay khi dự án có <strong>các công việc phụ thuộc lẫn nhau giữa nhiều bộ phận</strong>, có ngân sách cần kiểm soát và có cam kết ngày Go-Live với Ban Giám đốc, bạn bắt buộc phải dùng động cơ Gantt CPM như <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>.
  </p>
  <h3>Câu hỏi 2: Đội ngũ chưa từng dùng Microsoft Project có mất nhiều thời gian làm quen với project-management.erx.vn không?</h3>
  <p>
    Không. Giao diện của <code>project-management.erx.vn</code> hỗ trợ thao tác phím tắt và chỉnh sửa trực tiếp trên lưới (Inline Grid Editing) thân thuộc như Excel, đồng thời tích hợp sẵn học liệu tương tác <strong>Học viện Đào tạo P2P</strong> và <strong>AI Co-Pilot</strong> hướng dẫn từng bước.
  </p>
  <h3>Câu hỏi 3: Tôi có cần cài đặt phần mềm lên máy tính để sử dụng không?</h3>
  <p style="margin-bottom: 0;">
    Hoàn toàn không. <code>project-management.erx.vn</code> hoạt động 100% trên trình duyệt web với kho lưu trữ đám mây bảo mật, cho phép bạn và đội ngũ truy cập mọi lúc từ bất kỳ thiết bị nào.
  </p>
</div>
"""

# ==============================================================================
# PM-10: RESOURCE LEVELING, 3 TASK TYPES & WORK CONTOURS
# ==============================================================================
pm10_html = f"""
<h2>1. Phương trình Tam giác Nguồn lực: <code>Work = Duration × Units</code></h2>
<p>
  Một trong những nguyên nhân lớn nhất khiến kế hoạch dự án trên giấy tờ khác xa thực tế là sự nhầm lẫn giữa <strong>Thời lượng (Duration)</strong> và <strong>Khối lượng Giờ công (Work / Effort)</strong>. Trong miền hiệu suất <em>Resources (Nguồn lực)</em> của <a href="{URL_PM01}"><strong>PMBOK® Guide – 8th Edition</strong></a> và động cơ chuẩn Microsoft Project 2016 trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>project-management.erx.vn</strong></a>, mọi gói công việc đều vận hành theo phương trình toán học cốt lõi:
</p>
<p style="background: #eff6ff; padding: 14px 18px; border-left: 4px solid #2563eb; border-radius: 8px; font-weight: 700; color: #1e3a8a;">
  <code>Work (Tổng giờ công) = Duration (Số ngày làm việc × 8 giờ/ngày) × Assignment Units (Tỷ lệ phân bổ nhân sự %)</code>
</p>
<p>
  Ví dụ: Gói công việc <em>"Cấu hình tích hợp cổng PO tự động"</em> kéo dài <code>Duration = 5 ngày</code> (tương đương 40 giờ lịch làm việc). Nếu giao cho 1 kỹ sư CNTT làm toàn thời gian (<code>Units = 100%</code>), tổng khối lượng công việc là <code>Work = 40 giờ công</code>. Nếu giao cho 2 kỹ sư cùng làm toàn thời gian (<code>Units = 200%</code>), tổng giờ công là <code>Work = 80 giờ công</code>.
</p>

<h2>2. Phân biệt 3 Kiểu Công việc (Task Types): Fixed Units, Fixed Duration và Fixed Work</h2>
<p>
  Khi bạn thay đổi một trong ba biến số (<code>Work</code>, <code>Duration</code>, <code>Units</code>), biến số nào sẽ được giữ cố định và biến số nào sẽ tự động tính lại? Câu trả lời nằm ở thiết lập <strong>Task Type</strong> của từng dòng <a href="{URL_PM04}">WBS</a>:
</p>

<table>
  <thead>
    <tr>
      <th>Kiểu Task (Task Type)</th>
      <th>Biến số Giữ cố định</th>
      <th>Khi Tăng Nhân sự (<code>Units ↑</code>)</th>
      <th>Khi Tăng Giờ công (<code>Work ↑</code>)</th>
      <th>Tình huống Áp dụng Thực tế</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Fixed Units</strong><br><em>(Mặc định — Phổ biến nhất)</em></td>
      <td>Giữ cố định <strong>Tỷ lệ nhân sự (<code>Units %</code>)</strong></td>
      <td><code>Duration</code> tự động giảm xuống (nếu bật <em>Effort Driven</em>)</td>
      <td><code>Duration</code> tự động kéo dài thêm</td>
      <td>Các công việc chuyên môn thông thường do một số lượng nhân sự cố định phụ trách.</td>
    </tr>
    <tr>
      <td><strong>2. Fixed Duration</strong><br><em>(Cố định Thời gian)</em></td>
      <td>Giữ cố định <strong>Số ngày (<code>Duration</code>)</strong></td>
      <td>Tổng giờ công (<code>Work</code>) tự động tăng lên</td>
      <td>Tỷ lệ phân bổ (<code>Units %</code>) tự động tăng lên</td>
      <td>Chạy thử nghiệm UAT trong 5 ngày cố định, hội thảo nghiệm thu, hoặc thời gian chờ đấu thầu.</td>
    </tr>
    <tr>
      <td><strong>3. Fixed Work</strong><br><em>(Cố định Khối lượng)</em></td>
      <td>Giữ cố định <strong>Tổng giờ công (<code>Work</code>)</strong></td>
      <td><code>Duration</code> giảm tỷ lệ nghịch ngay lập tức</td>
      <td>Khi sửa <code>Duration</code>, hệ thống tự tính lại <code>Units %</code></td>
      <td>Các gói công việc đã chốt cứng định mức giờ công (ví dụ 80 man-hours kiểm toán dữ liệu).</td>
    </tr>
  </tbody>
</table>

<h2>3. Đường cong Phân bổ Công việc (9 Work Contours) &amp; Bảng Đơn giá <code>Rate Tables A–E</code></h2>
<p>
  Trong thực tế, nhân sự không phải lúc nào cũng làm việc đều đặn 8 giờ/ngày từ đầu đến cuối một gói công việc. Nền tảng <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a> hỗ trợ đầy đủ:
</p>
<ul>
  <li><strong>9 Dạng Đường cong Phân bổ (Work Contours):</strong> Từ phân bổ đều (<em>Flat</em>), dồn tải về cuối giai đoạn (<em>Back-Loaded</em> — thường gặp khi chuẩn bị Go-Live), dồn tải đầu giai đoạn (<em>Front-Loaded</em>), đến hình quả chuông (<em>Bell / Turtle Curve</em>). Sự lựa chọn Work Contour tác động trực tiếp đến hình dáng đường ngân sách kế hoạch (<a href="{URL_PM08}"><code>PV</code> trên đồ thị S-Curve của EVM</a>).</li>
  <li><strong>5 Bảng Đơn giá Chi phí (Cost Rate Tables A–E):</strong> Cho phép áp dụng mức lương/đơn giá khác nhau cho cùng một nhân sự hoặc nhà thầu tùy theo tính chất công việc (ví dụ: Bảng A cho giờ hành chính chuẩn, Bảng B cho giờ tư vấn chuyên gia cao cấp), kết hợp với <code>Cost Per Use</code> để tính toán chính xác tuyệt đối ngân sách cơ sở <code>BAC</code>.</li>
</ul>

<h2>4. Cân bằng Nguồn lực Tự động (Resource Leveling): Xử lý Triệt để Quá tải Nhân sự</h2>
<p>
  Khi một nhân sự bị phân công vào nhiều gói công việc diễn ra song song vượt quá công suất tối đa (<code>Max Units = 100%</code>), hệ thống sẽ đánh dấu cảnh báo đỏ <strong>Over-allocated Resource</strong>. Thay vì phải dò tìm thủ công, thuật toán <strong>Resource Leveling</strong> trên <code>project-management.erx.vn</code> sẽ tự động giải quyết theo thứ tự ưu tiên:
</p>

{figure_html("/Media/images/pm10_2_resource_leveling_before_after_light.jpg", "Cân bằng nguồn lực tự động Resource Leveling xử lý quá tải nhân sự chuẩn PMBOK 8", "Hình 1: Cơ chế Resource Leveling tự động dời các công việc không găng vào vùng Free Slack để triệt tiêu đỉnh quá tải 200% mà không làm trễ ngày kết thúc dự án.")}

<ol>
  <li><strong>Bảo vệ Đường găng (Preserve Critical Path):</strong> Giữ nguyên lịch trình của các công việc nằm trên Đường găng (<code>Total Slack = 0</code>).</li>
  <li><strong>Tận dụng Độ dự trữ Tự do (Level within Available Slack):</strong> Tự động dịch chuyển ngày bắt đầu của các công việc không găng nằm trong phạm vi <code>Free Slack</code> và <code>Total Slack</code> cho đến khi tổng tải của nhân sự trong mọi ngày đều <code>≤ 100%</code>.</li>
</ol>

{CTA_BOX_HTML}

<h2>5. Bài viết Liên quan trong Hệ sinh thái Quản trị Dự án PMBOK® 8</h2>
<ul>
  <li>📘 <strong>Tổng quan PMBOK 8:</strong> <a href="{URL_PM01}">Quản trị Dự án theo chuẩn PMBOK 8: Tổng quan 6 Nguyên tắc, 7 Miền hiệu suất &amp; 5 Nhóm quy trình thực chiến</a>.</li>
  <li>🌳 <strong>Xây dựng WBS &amp; Gói công việc:</strong> <a href="{URL_PM04}">Cấu trúc Phân rã Công việc (WBS) &amp; Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8</a>.</li>
  <li>📊 <strong>Kiểm soát Chi phí EVM:</strong> <a href="{URL_PM08}">Quản lý Giá trị Thu được (Earned Value Management - EVM): Cách tính BAC, PV, EV, AC, SPI, CPI &amp; Dự báo EAC</a>.</li>
</ul>

<h2>6. Câu hỏi Thường gặp (FAQ) về Resource Leveling &amp; Phương trình Nguồn lực</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: Khi nào Resource Leveling làm kéo dài ngày kết thúc của toàn dự án?</h3>
  <p>
    Khi một nhân sự chủ chốt bị phân công làm <strong>hai công việc đều nằm trên Đường găng (<code>Slack = 0</code>) diễn ra cùng một thời điểm</strong>. Khi đó, vì không còn khoảng đệm <code>Slack</code> nào để dịch chuyển, nếu không bổ sung thêm người hỗ trợ, thuật toán Leveling buộc phải xếp hai việc nối tiếp nhau và làm lùi ngày kết thúc dự án.
  </p>
  <h3>Câu hỏi 2: Tùy chọn "Effort Driven" khác gì với "Fixed Work"?</h3>
  <p>
    <code>Fixed Work</code> khóa chặt tổng giờ công trong mọi trường hợp; trong khi <code>Fixed Units + Effort Driven</code> chỉ giữ nguyên tổng giờ công khi bạn <em>thêm hoặc bớt người</em> vào Task, nhưng vẫn cho phép bạn gõ sửa trực tiếp cột <code>Duration</code> để tăng/giảm khối lượng <code>Work</code> khi cần.
  </p>
  <h3>Câu hỏi 3: Làm sao kiểm tra nhanh ai đang bị quá tải trên project-management.erx.vn?</h3>
  <p style="margin-bottom: 0;">
    Bạn chỉ cần mở bảng <strong>Resource Sheet / Resource Usage</strong> trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, hệ thống sẽ tô đỏ tức thời các nhân sự có đỉnh phân bổ vượt quá <code>Max Units</code> và cho phép bấm <strong>Level Resources</strong> chỉ với 1 cú nhấp chuột.
  </p>
</div>
"""

# ==============================================================================
# PM-11: CASE STUDY P2P 20 STEPS (PROCURE-TO-PAY)
# ==============================================================================
pm11_html = f"""
<h2>1. Tổng quan Case Study: Dự án Chuẩn hóa Quy trình Mua hàng đến Thanh toán (<code>P2P-FOUNDATION-2026</code>)</h2>
<p>
  Để giúp các Giám đốc Chuỗi cung ứng (Supply Chain Directors), Trưởng phòng Mua hàng (Procurement Managers) và chuyên viên PMO thấy rõ cách áp dụng <a href="{URL_PM01}"><strong>chuẩn PMBOK® Guide – 8th Edition</strong></a> vào thực tiễn doanh nghiệp Việt Nam, đội ngũ chuyên gia ERX đã xây dựng dự án mẫu hoàn chỉnh mang mã hiệu <strong><code>P2P-FOUNDATION-2026</code></strong> tích hợp sẵn ngay trong Học viện Đào tạo của <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>project-management.erx.vn</strong></a>.
</p>
<ul>
  <li><strong>Bối cảnh &amp; Nỗi đau Doanh nghiệp:</strong> Quy trình mua sắm từ khi phát sinh Yêu cầu mua hàng (<em>Purchase Requisition - PR</em>) đến khi phát hành Đơn hàng (<em>Purchase Order - PO</em>), nhận hàng nhập kho (<em>Goods Receipt Note - GRN</em>) và thanh toán hóa đơn (<em>AP Invoice</em>) đang bị phân mảnh qua giấy tờ và email, mất trung bình <strong>9 ngày làm việc/đơn</strong> và thường xuyên xảy ra chênh lệch số lượng/đơn giá.</li>
  <li><strong>Thông số Chuẩn của Dự án:</strong> Tổng thời lượng <strong>28 ngày làm việc</strong>, chia làm <strong>5 Giai đoạn (Phases)</strong> và <strong>20 Bước WBS</strong>, huy động <strong>7 đơn vị/phòng ban</strong>.</li>
  <li><strong>Cấu trúc Ngân sách Chuẩn PMBOK 8:</strong> Ngân sách cơ sở cuốn chiếu từ 20 gói công việc là <a href="{URL_PM08}"><strong><code>BAC = $49,448</code></strong></a>, cộng với Quỹ dự phòng của 8 rủi ro trọng yếu <a href="{URL_PM09}"><strong><code>EMV = +$3,260</code></strong></a>, tạo thành <strong>Ngân sách Phê duyệt (Approved Budget) = <code>$52,708</code></strong>.</li>
</ul>

<h2>2. Bóc tách Chi tiết 5 Giai đoạn &amp; 20 Bước WBS của Dự án Chuỗi Cung Ứng P2P</h2>
<p>
  Toàn bộ <a href="{URL_PM04}">Cấu trúc Phân rã Công việc (WBS)</a> của dự án được thiết kế tuân thủ nghiêm ngặt <strong>Quy tắc 100%</strong>, kết hợp thông minh các mối quan hệ <code>FS</code>, <code>SS+1d</code> (Fast-Tracking) và <code>FF</code>:
</p>

<table>
  <thead>
    <tr>
      <th>Giai đoạn (Phase)</th>
      <th>Các Bước WBS Trọng tâm (20 Bước)</th>
      <th>Đầu ra Nghiệm thu (Deliverables) &amp; Phòng ban Chịu trách nhiệm (A/R)</th>
      <th>Ngân sách Giai đoạn</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Phase 1: Khởi tạo &amp; Quản trị Nhu cầu (PR)</strong><br><em>(Ngày 1 – Ngày 5)</em></td>
      <td><code>1.1</code> Lập Project Charter &amp; Ma trận RACI<br><code>1.2</code> Chuẩn hóa Biểu mẫu PR &amp; Danh mục Mã vật tư<br><code>1.3</code> Thiết lập Quy tắc Kiểm tra Ngân sách (<code>SS+1d</code>)<br><code>1.4</code> Cấu hình Luồng Phê duyệt PR Đa cấp (DOA)</td>
      <td>Bản Charter được duyệt; Bộ mã vật tư chuẩn; Ma trận hạn mức phê duyệt tự động (PMO, Mua hàng, Tài chính).</td>
      <td><strong><code>$8,400</code></strong></td>
    </tr>
    <tr>
      <td><strong>Phase 2: Đấu thầu (RFQ) &amp; Lựa chọn NCC</strong><br><em>(Ngày 6 – Ngày 11)</em></td>
      <td><code>2.1</code> Chuẩn hóa Hồ sơ Mời báo giá (RFQ Template)<br><code>2.2</code> Xây dựng Ma trận Chấm điểm Kỹ thuật &amp; Thương mại<br><code>2.3</code> Đàm phán Tổng chi phí Sở hữu (TCO) &amp; SLA<br><code>2.4</code> Phê duyệt Danh sách Nhà cung cấp Đạt chuẩn (AVL)</td>
      <td>Bảng so sánh báo giá tự động; Khung chấm điểm TCO; Danh bạ nhà cung cấp được duyệt (Mua hàng, QA, Tài chính).</td>
      <td><strong><code>$11,200</code></strong></td>
    </tr>
    <tr>
      <td><strong>Phase 3: Hợp đồng &amp; Phát hành Đơn hàng (PO)</strong><br><em>(Ngày 12 – Ngày 16)</em></td>
      <td><code>3.1</code> Chuẩn hóa Hợp đồng Khung &amp; Điều khoản Phạt trễ<br><code>3.2</code> Cấu hình Chuyển đổi Tự động từ PR sang PO<br><code>3.3</code> Cổng Xác nhận Đơn hàng từ Nhà cung cấp (PO Ack)<br><code>3.4</code> Thiết lập Thông báo Giao hàng Trước (ASN)</td>
      <td>Mẫu hợp đồng chuẩn pháp lý; Luồng tự động sinh PO không cần nhập liệu lại (Mua hàng, CNTT, Nhà cung cấp).</td>
      <td><strong><code>$9,848</code></strong></td>
    </tr>
    <tr>
      <td><strong>Phase 4: Nhận hàng, QA &amp; Đối soát 3-Way Match</strong><br><em>(Ngày 17 – Ngày 23)</em></td>
      <td><code>4.1</code> Quy trình Tiếp nhận Hàng hóa &amp; Lập phiếu GRN<br><code>4.2</code> Kiểm định Chất lượng Đầu vào (IQC / QA Gate - <code>FF</code>)<br><code>4.3</code> Cấu hình Đối soát Tự động 3 bên (3-Way Matching)<br><code>4.4</code> Quy trình Giải ngân &amp; Lịch Thanh toán (Payment Run)</td>
      <td>Chốt chặn kiểm soát tự động <code>PO ↔ GRN ↔ Invoice</code> trước khi giải ngân (Kho vận, QA, Kế toán AP, CNTT).</td>
      <td><strong><code>$12,600</code></strong></td>
    </tr>
    <tr>
      <td><strong>Phase 5: Supplier Scorecard &amp; Bàn giao Go-Live</strong><br><em>(Ngày 24 – Ngày 28)</em></td>
      <td><code>5.1</code> Xây dựng Dashboard KPI Mua hàng &amp; Công nợ<br><code>5.2</code> Thiết lập Thẻ điểm Nhà cung cấp (OTIF &amp; Quality)<br><code>5.3</code> Đào tạo SOP cho 7 Phòng ban &amp; Chạy UAT<br><code>5.4</code> Nghiệm thu Đóng Dự án &amp; Bàn giao Vận hành</td>
      <td>Dashboard theo dõi OTIF thời gian thực; 100% nhân sự vượt qua bài kiểm tra SOP; Biên bản nghiệm thu (Toàn bộ 7 đơn vị).</td>
      <td><strong><code>$7,400</code></strong></td>
    </tr>
  </tbody>
</table>

<h2>3. Điểm Nhấn Kiểm soát Chất lượng: Chốt chặn Đối soát Ba bên (3-Way Matching)</h2>
<p>
  Tại <strong>Bước 4.3</strong> trên Đường găng của dự án, nguyên tắc <em>"Nhúng chất lượng vào quy trình và giao phẩm" (Embed Quality)</em> của PMBOK 8 được hiện thực hóa thông qua cơ chế <strong>Đối soát Ba bên Tự động (3-Way Matching)</strong>:
</p>

{figure_html("/Media/images/pm11_2_three_way_matching_control_light.jpg", "Cơ chế đối soát ba bên 3-Way Matching PO GRN Invoice trong dự án chuỗi cung ứng P2P chuẩn PMBOK 8", "Hình 1: Chốt chặn kiểm soát chất lượng và tài chính 3-Way Matching (PO ↔ GRN ↔ Invoice) ở Bước 4.3 của dự án P2P-FOUNDATION-2026.")}

<p>
  Hệ thống đối chiếu tự động 3 chứng từ độc lập: <strong>Đơn đặt hàng (PO)</strong> của Phòng Mua hàng, <strong>Phiếu nhập kho đạt chuẩn (GRN + QA Pass)</strong> của Bộ phận Kho/QC, và <strong>Hóa đơn (Invoice)</strong> của Nhà cung cấp gửi cho Kế toán AP. Chỉ khi cả 3 chứng từ khớp 100% về mã hàng, số lượng thực nhận và đơn giá hợp đồng, lệnh thanh toán ở Bước 4.4 mới được kích hoạt.
</p>

{CTA_BOX_HTML}

<h2>4. Bài viết Liên quan trong Hệ sinh thái Quản trị Dự án &amp; Chuỗi Cung Ứng</h2>
<ul>
  <li>📘 <strong>Tổng quan PMBOK 8:</strong> <a href="{URL_PM01}">Quản trị Dự án theo chuẩn PMBOK 8: Tổng quan 6 Nguyên tắc, 7 Miền hiệu suất &amp; 5 Nhóm quy trình thực chiến</a>.</li>
  <li>🌳 <strong>Xây dựng WBS &amp; Từ điển WBS:</strong> <a href="{URL_PM04}">Cấu trúc Phân rã Công việc (WBS) &amp; Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8</a>.</li>
  <li>📊 <strong>Kiểm soát Ngân sách bằng EVM:</strong> <a href="{URL_PM08}">Quản lý Giá trị Thu được (Earned Value Management - EVM): Cách tính BAC, PV, EV, AC, SPI, CPI &amp; Dự báo EAC</a>.</li>
  <li>🛡️ <strong>Định lượng 8 Rủi ro Dự án P2P bằng EMV:</strong> <a href="{URL_PM09}">Định lượng Rủi ro Dự án bằng EMV (Expected Monetary Value) &amp; Cách tính Quỹ Dự phòng (Contingency Reserve)</a>.</li>
  <li>📦 <strong>Kiến thức Chuyên sâu về Mua hàng:</strong> Xem thêm tại <a href="https://erx.vn/procurement-management.html">Procurement Management</a> và <a href="https://community.erx.vn/" target="_blank" rel="noopener">Cộng đồng Chuỗi cung ứng SCM (community.erx.vn)</a>.</li>
</ul>

<h2>5. Câu hỏi Thường gặp (FAQ) về Case Study Dự án P2P</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: Làm sao để mở và tương tác trực tiếp với dữ liệu dự án mẫu P2P-FOUNDATION-2026?</h3>
  <p>
    Bạn chỉ cần truy cập <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, dự án mẫu <strong>P2P-FOUNDATION-2026</strong> cùng 2 trang học liệu chuyên sâu (<a href="https://project-management.erx.vn/training/p2p-project-management-foundation.html" target="_blank" rel="noopener">Nền tảng Quản trị Dự án P2P</a> và <a href="https://project-management.erx.vn/training/p2p-project-story-case-study.html" target="_blank" rel="noopener">Câu chuyện Thực chiến P2P</a>) đã được tích hợp sẵn để bạn trải nghiệm ngay lập tức.
  </p>
  <h3>Câu hỏi 2: Tôi có thể dùng mẫu WBS 20 bước này để tùy biến cho dự án triển khai ERP hoặc WMS của công ty mình không?</h3>
  <p>
    Hoàn toàn được. Bạn có thể nhân bản (Clone) dự án <code>P2P-FOUNDATION-2026</code> trên đám mây hoặc nhờ <strong>AI Project Co-Pilot</strong> điều chỉnh lại tên các gói công việc, đơn giá nhân sự và danh mục rủi ro cho khớp với doanh nghiệp của bạn.
  </p>
  <h3>Câu hỏi 3: Vì sao ngân sách phê duyệt của dự án là $52,708 thay vì $49,448?</h3>
  <p style="margin-bottom: 0;">
    <code>$49,448</code> là chi phí cơ sở (<code>BAC</code>) tính từ giờ công của 20 gói công việc, còn <code>$3,260</code> là quỹ dự phòng rủi ro (<code>Contingency Reserve</code>) được định lượng bằng công thức <code>EMV = P% × Impact($)</code> từ 8 rủi ro thực tế của dự án P2P, tổng cộng tạo thành ngân sách phê duyệt <code>$52,708</code>.
  </p>
</div>
"""

# ==============================================================================
# PM-12: AI AGENT, MCP PROTOCOL & REAL-TIME TELEGRAM EXECUTIVE DIFF
# ==============================================================================
pm12_html = f"""
<h2>1. Kỷ nguyên Quản trị Dự án AI-Native trong Chuẩn PMBOK® Guide – 8th Edition</h2>
<p>
  Một trong những điểm mới quan trọng nhất của <a href="{URL_PM01}"><strong>PMBOK® Guide – 8th Edition (PMBOK 8)</strong></a> là việc chính thức đưa <strong>Trí tuệ Nhân tạo (AI), Tự động hóa Dữ liệu và Quản trị Thời gian thực</strong> vào trọng tâm vận hành của Văn phòng Quản lý Dự án (PMO). Thay vì dành 80% thời gian mỗi tuần để gom số liệu thủ công, vẽ lại biểu đồ và viết báo cáo trạng thái, Giám đốc Dự án hiện đại sử dụng AI để tự động hóa các tác vụ tính toán định lượng và tập trung vào việc ra quyết định chiến lược.
</p>
<p>
  Nền tảng <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>ERX AI Project Gantt Planner (project-management.erx.vn)</strong></a> tiên phong hiện thực hóa tầm nhìn này thông qua 3 công nghệ cốt lõi: <strong>Trợ lý AI Project Co-Pilot</strong>, <strong>Giao thức Model Context Protocol (MCP Server)</strong> và <strong>Hệ thống Cảnh báo Chênh lệch Điều hành (Executive Diff) qua Telegram / OpenClaw</strong>.
</p>

<h2>2. AI Project Co-Pilot &amp; Giao thức MCP (Model Context Protocol): Khi AI Hiểu Sâu Cấu trúc WBS, CPM và EVM</h2>
<p>
  Khác với các công cụ chat AI thông thường chỉ sinh ra văn bản rời rạc, <strong>AI Co-Pilot</strong> và <strong>MCP Server</strong> trên <code>project-management.erx.vn</code> làm việc trực tiếp trên cấu trúc dữ liệu đồ thị của dự án:
</p>
<ul>
  <li><strong>Khởi tạo Dự án Toàn diện từ Prompt (Zero-to-Baseline in 60s):</strong> Chỉ từ một đoạn mô tả mục tiêu kinh doanh, AI tự động thiết kế cây <a href="{URL_PM04}">WBS đa cấp</a>, gắn mối quan hệ phụ thuộc <code>FS/SS/FF/SF</code>, phân bổ nhân sự, định lượng rủi ro <a href="{URL_PM09}"><code>EMV = P% × Impact($)</code></a> và điền đầy đủ <strong>13 hồ sơ chuẩn PMBOK® 8</strong>.</li>
  <li><strong>Kết nối AI Agent qua Chuẩn MCP (Model Context Protocol):</strong> Hệ thống cung cấp bộ công cụ MCP chuyên dụng (<code>list_cloud_projects</code>, <code>get_cloud_project_summary</code>, <code>query_cloud_tasks</code>, <code>update_cloud_task_progress</code>, <code>manage_cloud_lock</code>), cho phép các trợ lý AI doanh nghiệp truy vấn trực tiếp: <em>"Những gói công việc nào đang nằm trên Đường găng và có nguy cơ trễ hạn trong tuần này?"</em></li>
</ul>

<h2>3. Quản trị Kho Dự án Đám mây (Cloud Check-out / Check-in) &amp; Chống Xung đột Phiên bản</h2>
<p>
  Để đảm bảo nguyên tắc <em>Lãnh đạo có trách nhiệm giải trình (Accountable Leadership)</em> và tính toàn vẹn dữ liệu khi nhiều phòng ban cùng cập nhật tiến độ, kho dự án đám mây của <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a> vận hành theo cơ chế khóa phiên bản 엄ngặt:
</p>
<ol>
  <li><strong>Check-out (Khóa chỉnh sửa có kiểm soát):</strong> Khi PM hoặc Trưởng nhóm cần cập nhật phần trăm hoàn thành (<code>% Complete</code>) hay chi phí thực tế (<code>Actual Cost</code>), họ thực hiện <code>Check-out</code> để khóa phiên bản, ngăn chặn việc hai người cùng sửa đè lên dữ liệu của nhau.</li>
  <li><strong>Check-in (Lưu phiên bản mới &amp; Ghi nhật ký Audit Log):</strong> Khi hoàn tất cập nhật và bấm <code>Check-in</code>, hệ thống tự động tăng số phiên bản (Revision), lưu vết người chỉnh sửa và kích hoạt động cơ so sánh chênh lệch tự động.</li>
</ol>

<h2>4. Báo cáo Chênh lệch Điều hành (Executive Diff) Bắn Tự động qua Telegram / OpenClaw</h2>
<p>
  Tại các tập đoàn lớn, Ban Giám đốc và Project Sponsor không có thời gian mở file dự án 100 dòng mỗi ngày để dò xem dòng nào vừa thay đổi. Ngay tại thời điểm một thành viên thực hiện <strong>Cloud Check-in</strong>, động cơ <strong>Executive Diff Engine</strong> của <code>project-management.erx.vn</code> sẽ tự động so sánh phiên bản mới (<code>Version N</code>) với phiên bản liền trước (<code>Version N-1</code>) và bắn bản tin tóm tắt điều hành trực tiếp vào nhóm <strong>Telegram / OpenClaw</strong> của Ban Giám đốc:
</p>

{figure_html("/Media/images/pm12_2_executive_diff_telegram_alert_light.jpg", "Báo cáo chênh lệch điều hành Executive Diff tự động qua Telegram trên project-management.erx.vn", "Hình 1: Cấu trúc bản tin Executive Diff tự động gửi qua Telegram giúp Ban Giám đốc nắm bắt ngay biến động Finish Date, SPI/CPI, Đường găng và Rủi ro EMV.")}

<table>
  <thead>
    <tr>
      <th>Hạng mục Cảnh báo trong <code>Executive Diff</code></th>
      <th>Nội dung So sánh Tự động (<code>Version N-1 → Version N</code>)</th>
      <th>Giá trị Quản trị cho Ban Giám đốc &amp; PMO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Biến động Ngày Kết thúc &amp; Tiến độ (Schedule Delta)</strong></td>
      <td>So sánh <code>Finish Date</code> của dự án và chỉ số <a href="{URL_PM08}"><code>SPI (Schedule Performance Index)</code></a>.</td>
      <td>Phát hiện ngay lập tức nếu một cập nhật vừa làm ngày Go-Live bị đẩy lùi (ví dụ <code>+2 ngày</code>) để xử lý kịp thời.</td>
    </tr>
    <tr>
      <td><strong>2. Biến động Ngân sách &amp; Dự báo EAC (Finance Delta)</strong></td>
      <td>So sánh <code>Actual Cost (AC)</code>, chỉ số hiệu suất chi phí <code>CPI</code> và dự báo ngân sách khi hoàn thành <code>EAC</code> so với <code>Approved Budget ($52,708)</code>.</td>
      <td>Cảnh báo sớm nguy cơ vượt tổng mức đầu tư trước khi chi phí thực tế vượt quá quỹ dự phòng.</td>
    </tr>
    <tr>
      <td><strong>3. Sự Dịch chuyển Đường găng (Critical Path Shift)</strong></td>
      <td>Liệt kê các gói công việc mới bị rơi vào Đường găng (<code>Total Slack</code> giảm về <code>0</code>) hoặc các mốc <em>Milestone</em> bị trễ.</td>
      <td>Giúp PM biết chính xác cần tập trung hỗ trợ bộ phận nào trong cuộc họp giao ban sáng hôm sau.</td>
    </tr>
    <tr>
      <td><strong>4. Biến động Phơi nhiễm Rủi ro (Risk EMV Delta)</strong></td>
      <td>Cập nhật sự thay đổi của tổng quỹ dự phòng <a href="{URL_PM09}"><code>EMV ($)</code></a> và các rủi ro cấp độ Đỏ (High/Critical) mới phát sinh.</td>
      <td>Đảm bảo hạn mức dự phòng luôn đủ sức chống đỡ các rủi ro đang hoạt động.</td>
    </tr>
  </tbody>
</table>

{CTA_BOX_HTML}

<h2>5. Bài viết Liên quan trong Hệ sinh thái Quản trị Dự án PMBOK® 8</h2>
<ul>
  <li>📘 <strong>Trụ cột 1 (Tổng quan PMBOK 8):</strong> <a href="{URL_PM01}">Quản trị Dự án theo chuẩn PMBOK 8: Tổng quan 6 Nguyên tắc, 7 Miền hiệu suất &amp; 5 Nhóm quy trình thực chiến</a>.</li>
  <li>🌳 <strong>Trụ cột 2 (Cấu trúc WBS &amp; Từ điển WBS):</strong> <a href="{URL_PM04}">Cấu trúc Phân rã Công việc (WBS) &amp; Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8</a>.</li>
  <li>📊 <strong>Trụ cột 3 (Kiểm soát Ngân sách EVM):</strong> <a href="{URL_PM08}">Quản lý Giá trị Thu được (Earned Value Management - EVM): Cách tính BAC, PV, EV, AC, SPI, CPI &amp; Dự báo EAC</a>.</li>
  <li>🛡️ <strong>Trụ cột 4 (Định lượng Rủi ro EMV):</strong> <a href="{URL_PM09}">Định lượng Rủi ro Dự án bằng EMV (Expected Monetary Value) &amp; Cách tính Quỹ Dự phòng (Contingency Reserve)</a>.</li>
</ul>

<h2>6. Câu hỏi Thường gặp (FAQ) về AI Co-Pilot, MCP &amp; Cảnh báo Telegram</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: AI Project Co-Pilot có tự ý thay đổi tiến độ hoặc ngân sách khi chưa được PM cho phép không?</h3>
  <p>
    Không. Tuân thủ nguyên tắc <em>Accountable Leadership</em> của PMBOK 8, mọi đề xuất của AI Co-Pilot đều đi qua bước <strong>Xem trước và Phê duyệt của con người (Human-in-the-loop)</strong>, và mọi thay đổi khi lưu lên đám mây đều được ghi nhận đầy đủ trong báo cáo <em>Executive Diff</em>.
  </p>
  <h3>Câu hỏi 2: Làm thế nào để kết nối thông báo Executive Diff của dự án vào nhóm Telegram của công ty?</h3>
  <p>
    Trong phần cấu hình <strong>Cloud Webhook &amp; Notification</strong> trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, bạn chỉ cần nhập Chat ID / Webhook của nhóm Telegram hoặc cổng OpenClaw; từ đó mỗi lần có thành viên <code>Check-in</code> phiên bản mới, bản tin <em>Executive Diff</em> sẽ được gửi tự động trong chưa đầy 2 giây.
  </p>
  <h3>Câu hỏi 3: Tôi có thể trải nghiệm toàn bộ 12 chủ đề PMBOK 8 này ở đâu?</h3>
  <p style="margin-bottom: 0;">
    Bạn có thể đọc trọn bộ 12 bài cẩm nang chuyên sâu tại chuyên mục <a href="https://erx.vn/project-management.html"><strong>Project Management trên ERX.VN</strong></a> và thực hành trực tiếp ngay trên nền tảng <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>https://project-management.erx.vn/</strong></a>!
  </p>
</div>
"""

cluster_articles = [
    {
        "code": "PM-02",
        "title": "Project Charter là gì? Cách lập Điều lệ Dự án & Business Case chuẩn PMBOK 8",
        "alias": "project-charter-la-gi-cach-lap-dieu-le-du-an-va-business-case-chuan-pmbok-8",
        "meta_desc": "Hướng dẫn lập Project Charter (Điều lệ Dự án), phân biệt Business Case và Benefits Management Plan chuẩn PMBOK 8 kèm mẫu thực tế trên project-management.erx.vn.",
        "meta_key": "project charter là gì, điều lệ dự án, cách lập project charter, mẫu project charter pmbok 8, business case là gì, quản trị dự án erx",
        "introtext": "<p>Project Charter (Điều lệ Dự án) là văn bản pháp lý nội bộ chính thức khai sinh dự án và trao quyền cho Giám đốc Dự án trong chuẩn PMBOK® 8. Bài viết phân tích cấu trúc 6 thành phần cốt lõi của Project Charter, cách liên kết xuyên suốt giữa Business Case – Project Charter – Benefits Plan và tự động đồng bộ ngân sách Approved Budget = BAC + EMV trên project-management.erx.vn.</p>",
        "hero_file": "pm02_1_project_charter_structure_light.jpg",
        "inline_file": "pm02_2_business_case_vs_benefits_light.jpg",
        "fulltext": pm02_html.strip()
    },
    {
        "code": "PM-03",
        "title": "Ma trận RACI & Quản lý Bên liên quan (Stakeholder Register) chuẩn PMBOK 8",
        "alias": "ma-tran-raci-va-quan-ly-ben-lien-quan-stakeholder-register-chuan-pmbok-8",
        "meta_desc": "Cách lập Ma trận phân quyền RACI (Responsible, Accountable, Consulted, Informed) và phân tích Stakeholder Power/Interest Grid chuẩn PMBOK 8 cho dự án đa phòng ban.",
        "meta_key": "ma trận raci, raci là gì, cách lập ma trận raci, stakeholder register, power interest grid, quản lý bên liên quan pmbok 8",
        "introtext": "<p>Làm sao chấm dứt tình trạng đùn đẩy trách nhiệm trong các dự án liên phòng ban? Khám phá cách kết hợp Lưới Quyền lực – Mức độ quan tâm (Power/Interest Grid) với Ma trận phân quyền RACI và 3 quy tắc kiểm toán tự động (duy nhất 1 chữ A cho mỗi gói công việc) theo chuẩn PMBOK® 8 trên project-management.erx.vn.</p>",
        "hero_file": "pm03_1_raci_matrix_rules_light.jpg",
        "inline_file": "pm03_2_stakeholder_power_interest_grid_light.jpg",
        "fulltext": pm03_html.strip()
    },
    {
        "code": "PM-05",
        "title": "4 Mối quan hệ Phụ thuộc (FS, SS, FF, SF), Lag/Lead & Kỹ thuật Fast-Tracking chuẩn PMBOK 8",
        "alias": "4-moi-quan-he-phu-thuoc-fs-ss-ff-sf-va-ky-thuat-fast-tracking-chuan-pmbok-8",
        "meta_desc": "Giải mã 4 mối quan hệ phụ thuộc công việc PDM (FS, SS, FF, SF), cách tính độ trễ Lag/Lead và so sánh kỹ thuật rút ngắn tiến độ Fast-Tracking vs Crashing chuẩn PMBOK 8.",
        "meta_key": "fs ss ff sf trong quản lý dự án, quan hệ phụ thuộc công việc, lag và lead, fast tracking và crashing, lập tiến độ dự án pmbok 8",
        "introtext": "<p>Nắm vững 4 mối quan hệ phụ thuộc trong Phương pháp Biểu đồ Tiền nhiệm (PDM: Finish-to-Start, Start-to-Start, Finish-to-Finish, Start-to-Finish) cùng độ trễ Lag/Lead là chìa khóa để xây dựng lịch trình dự án tự động. Cùng phân tích các ví dụ thực chiến trong chuỗi cung ứng và cách nén tiến độ từ 34 ngày xuống 28 ngày bằng kỹ thuật Fast-Tracking.</p>",
        "hero_file": "pm05_1_pdm_4_dependencies_light.jpg",
        "inline_file": "pm05_2_fast_tracking_vs_crashing_light.jpg",
        "fulltext": pm05_html.strip()
    },
    {
        "code": "PM-06",
        "title": "Phương pháp Đường găng (Critical Path Method - CPM), Free Slack & Total Slack trong Quản lý Dự án",
        "alias": "phuong-phap-duong-gang-cpm-critical-path-free-slack-va-total-slack-trong-du-an",
        "meta_desc": "Hướng dẫn tính Đường găng dự án (Critical Path Method - CPM) qua Lượt đi (ES/EF), Lượt về (LS/LF) và phân biệt Free Slack với Total Slack chuẩn PMBOK 8.",
        "meta_key": "đường găng dự án, critical path method, cpm là gì, cách tính đường găng, free slack và total slack, es ef ls lf trong quản lý dự án",
        "introtext": "<p>Phương pháp Đường găng (Critical Path Method - CPM) giúp Giám đốc Dự án xác định chính xác chuỗi công việc dài nhất quyết định ngày kết thúc dự án (Total Slack = 0). Bài viết giải thích chi tiết thuật toán Lượt đi (ES/EF), Lượt về (LS/LF) và cách phân biệt Free Slack với Total Slack để điều phối nhân sự không làm vỡ hạn chót.</p>",
        "hero_file": "pm06_1_cpm_forward_backward_pass_light.jpg",
        "inline_file": "pm06_2_free_slack_vs_total_slack_light.jpg",
        "fulltext": pm06_html.strip()
    },
    {
        "code": "PM-07",
        "title": "Tại sao Quản lý Dự án bằng Excel dễ Vỡ tiến độ? So sánh Excel, MS Project & AI Gantt Planner",
        "alias": "tai-sao-quan-ly-du-an-bang-excel-de-vo-tien-do-so-sanh-ms-project-va-ai-gantt",
        "meta_desc": "Phân tích 6 điểm gãy khi vẽ biểu đồ Gantt bằng Excel thủ công và bảng so sánh chi tiết giữa Excel, Microsoft Project và nền tảng ERX AI Project Gantt Planner.",
        "meta_key": "vẽ biểu đồ gantt trong excel, quản lý dự án bằng excel, so sánh excel và ms project, phần mềm quản lý dự án online, ai gantt planner",
        "introtext": "<p>Tô màu ô Excel để vẽ biểu đồ Gantt rất dễ thực hiện ở ngày đầu tiên nhưng lại trở thành cơn ác mộng khi dự án phát sinh thay đổi. Cùng phân tích 6 điểm gãy kỹ thuật của Excel khi quản lý dự án đa phòng ban và cách chuyển đổi sang nền tảng đám mây chuẩn Microsoft Project 2016 Parity trên project-management.erx.vn.</p>",
        "hero_file": "pm07_1_excel_vs_ai_gantt_comparison_light.jpg",
        "inline_file": "pm07_2_msp_parity_architecture_light.jpg",
        "fulltext": pm07_html.strip()
    },
    {
        "code": "PM-10",
        "title": "Cân bằng Nguồn lực (Resource Leveling) & Phương trình Work = Duration × Units chuẩn PMBOK 8",
        "alias": "can-bang-nguon-luc-resource-leveling-va-phuong-trinh-work-duration-units-pmbok-8",
        "meta_desc": "Giải mã phương trình Work = Duration × Units, phân biệt 3 kiểu Task (Fixed Units, Fixed Duration, Fixed Work), 9 Work Contours và kỹ thuật Resource Leveling chống quá tải.",
        "meta_key": "resource leveling là gì, cân bằng nguồn lực dự án, work duration units, fixed units fixed duration fixed work, quản lý nguồn lực pmbok 8",
        "introtext": "<p>Hiểu rõ phương trình tam giác Work = Duration × Units và 3 kiểu công việc (Fixed Units, Fixed Duration, Fixed Work) là điều kiện tiên quyết để tính đúng giờ công và ngân sách dự án. Bài viết hướng dẫn cách ứng dụng 9 đường cong Work Contours và thuật toán Resource Leveling để xử lý triệt để tình trạng quá tải nhân sự (Over-allocation).</p>",
        "hero_file": "pm10_1_work_duration_units_triangle_light.jpg",
        "inline_file": "pm10_2_resource_leveling_before_after_light.jpg",
        "fulltext": pm10_html.strip()
    },
    {
        "code": "PM-11",
        "title": "Case Study Quản trị Dự án Chuỗi Cung Ứng (Procure-to-Pay): Lộ trình 20 Bước WBS & Đối soát 3-Way Match",
        "alias": "case-study-quan-tri-du-an-chuoi-cung-ung-procure-to-pay-p2p-20-buoc-chuan-pmbok-8",
        "meta_desc": "Case study thực chiến dự án chuẩn hóa quy trình Mua hàng đến Thanh toán (Procure-to-Pay P2P-FOUNDATION-2026): 5 giai đoạn, 20 bước WBS, 3-Way Matching và ngân sách $52,708.",
        "meta_key": "quy trình procure to pay, p2p là gì, quản lý dự án mua hàng, 3 way matching là gì, case study quản trị dự án chuỗi cung ứng, pmbok 8",
        "introtext": "<p>Bóc tách toàn diện Case Study dự án chuẩn hóa quy trình Mua hàng đến Thanh toán (P2P-FOUNDATION-2026) kéo dài 28 ngày làm việc với 7 phòng ban và tổng ngân sách phê duyệt $52,708. Từ chuẩn hóa PR, đấu thầu RFQ, phát hành PO đến chốt chặn đối soát ba bên (3-Way Matching: PO ↔ GRN ↔ Invoice) và thẻ điểm nhà cung cấp trên project-management.erx.vn.</p>",
        "hero_file": "pm11_1_p2p_20_steps_roadmap_light.jpg",
        "inline_file": "pm11_2_three_way_matching_control_light.jpg",
        "fulltext": pm11_html.strip()
    },
    {
        "code": "PM-12",
        "title": "Ứng dụng AI Agent, Giao thức MCP & Cảnh báo Executive Diff qua Telegram trong Quản trị Dự án",
        "alias": "ung-dung-ai-agent-giao-thuc-mcp-va-canh-bao-telegram-trong-quan-tri-du-an",
        "meta_desc": "Khám phá kiến trúc Quản trị Dự án AI-Native theo PMBOK 8: AI Project Co-Pilot, giao thức MCP Server, Cloud Check-out/Check-in và báo cáo Executive Diff qua Telegram.",
        "meta_key": "ai trong quản lý dự án, ai project management, giao thức mcp, executive diff telegram, pmo dashboard, project management erx",
        "introtext": "<p>Bước vào kỷ nguyên Quản trị Dự án AI-Native theo chuẩn PMBOK® 8: cách sử dụng trợ lý AI Project Co-Pilot để khởi tạo WBS & 13 hồ sơ PMBOK trong 60 giây, kết nối AI Agent qua giao thức MCP, kiểm soát phiên bản đám mây (Check-out/Check-in) và tự động bắn báo cáo chênh lệch điều hành (Executive Diff) qua Telegram cho Ban Giám đốc.</p>",
        "hero_file": "pm12_1_ai_copilot_mcp_architecture_light.jpg",
        "inline_file": "pm12_2_executive_diff_telegram_alert_light.jpg",
        "fulltext": pm12_html.strip()
    },
]

out_json = os.path.join(ASSET_DIR, "cluster_articles_clean.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(cluster_articles, f, ensure_ascii=False, indent=2)

print(f"Saved 8 Cluster Articles payload ({os.path.getsize(out_json)/1024:.1f} KB) to {out_json}")
