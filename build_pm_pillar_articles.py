# -*- coding: utf-8 -*-
"""
Builds the 4 comprehensive Pillar Articles (PM-01, PM-04, PM-08, PM-09)
with clean semantic HTML (no duplicate intro box, no duplicate hero diagram in body,
light-tone styling, and uniform typography).
"""
import os
import json

ASSET_DIR = r"D:\GIT\SEO Tool\pm_assets"

def figure_html(img_token, alt_text, caption_text):
    return f"""
<figure class="erx-figure" style="margin: 26px 0; text-align: center; background: #f8fafc; padding: 14px; border-radius: 12px; border: 1px solid #e2e8f0;">
  <img src="{{{{{img_token}}}}}" alt="{alt_text}" width="1200" height="675" loading="lazy" decoding="async" style="max-width: 100%; height: auto; border-radius: 8px; display: block; margin: 0 auto; border: 1px solid #e2e8f0;" />
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
# ARTICLE 1: PM-01
# ==============================================================================
pm01_html = f"""
<h2>1. Tại sao PMBOK® Guide – 8th Edition (PMBOK 8) là bước ngoặt lớn trong Quản trị Dự án hiện đại?</h2>
<p>
  Trong suốt hơn hai thập kỷ, các nhà quản trị dự án (Project Managers), Giám đốc PMO và chuyên gia Chuỗi cung ứng (Supply Chain &amp; Procurement Leaders) thường đứng trước một sự phân cực lớn:
</p>
<ul>
  <li><strong>PMBOK® 6th Edition (2017):</strong> Rất mạnh về quy trình kỹ thuật với 49 quy trình và cấu trúc <em>Inputs – Tools &amp; Techniques – Outputs (ITTOs)</em>, nhưng lại bị đánh giá là cứng nhắc khi áp dụng cho các dự án chuyển đổi số hoặc lai ghép (Hybrid/Agile).</li>
  <li><strong>PMBOK® 7th Edition (2021):</strong> Chuyển hẳn sang hướng tiếp cận dựa trên nguyên tắc (Principle-based) gồm 12 nguyên tắc và 8 miền hiệu suất, nhưng lại lược bỏ cấu trúc 5 Nhóm Quy trình quen thuộc, khiến nhiều đội ngũ triển khai thực tế lúng túng khi trả lời câu hỏi: <em>"Bắt đầu dự án từ đâu, lập kế hoạch thế nào và kiểm soát ngân sách ra sao?"</em></li>
</ul>
<p>
  Chính vì vậy, <strong>PMBOK® Guide – 8th Edition (PMBOK 8)</strong> ra đời như một <strong>kiến trúc hợp nhất hoàn chỉnh</strong>. PMBOK 8 tinh gọn thành <strong>6 Nguyên tắc cốt lõi (6 Core Principles)</strong>, <strong>7 Miền hiệu suất (7 Performance Domains)</strong>, đồng thời <strong>tích hợp chính thức trở lại 5 Nhóm Quy trình / Trọng tâm thực thi (Initiating, Planning, Executing, Monitoring &amp; Controlling, Closing)</strong> cùng các tiêu chuẩn về <strong>AI Co-Pilot, Quản trị dữ liệu thời gian thực và Tính bền vững</strong>.
</p>

<h2>2. Giải mã 6 Nguyên tắc Cốt lõi (6 Core Principles) trong PMBOK® 8</h2>
<p>
  Thay vì 12 nguyên tắc dàn trải như phiên bản cũ, PMBOK 8 cô đọng lại thành <strong>6 nguyên tắc kim chỉ nam</strong> định hình văn hóa ra quyết định của mọi Giám đốc Dự án:
</p>
<ol>
  <li><strong>Tư duy Hệ thống Tổng thể (Adopt a Holistic View):</strong> Không một gói công việc (Work Package) nào tồn tại độc lập. Khi một khâu trong quy trình phê duyệt yêu cầu mua hàng (PR) bị trễ 2 ngày, nó lập tức tác động dây chuyền đến lịch đấu thầu RFQ, kế hoạch dòng tiền của bộ phận Tài chính và lịch nhận hàng tại Kho. Trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, tư duy hệ thống được thể hiện qua mạng liên kết phụ thuộc PDM (<code>FS</code>, <code>SS</code>, <code>FF</code>, <code>SF</code>) và cơ chế tự động tính lại toàn bộ lịch trình khi có bất kỳ biến động nào.</li>
  <li><strong>Tập trung vào Giá trị Thực chất (Focus on Value):</strong> Một dự án hoàn thành đúng hạn và trong ngân sách nhưng không mang lại lợi ích kinh doanh (ROI, tiết giảm chi phí mua hàng, rút ngắn Lead-time) vẫn là một dự án thất bại. PMBOK 8 yêu cầu gắn chặt <em>Business Case</em> và <em>Benefits Management Plan</em> ngay trong giao diện điều hành dự án.</li>
  <li><strong>Nhúng Chất lượng vào Quy trình &amp; Giao phẩm (Embed Quality into Processes and Deliverables):</strong> Chất lượng không phải là khâu kiểm tra cuối cùng khi dự án đã xong, mà phải được định nghĩa thành tiêu chí nghiệm thu (<em>Acceptance Criteria</em>) và chỉ số <em>Quality Metrics</em> ở từng bước WBS.</li>
  <li><strong>Lãnh đạo có Trách nhiệm Giải trình (Be an Accountable Leader):</strong> Mọi gói công việc bắt buộc phải có duy nhất một người chịu trách nhiệm giải trình cuối cùng (<strong>Accountable - A</strong>) và ít nhất một người trực tiếp thực thi (<strong>Responsible - R</strong>) thông qua ma trận <strong>RACI</strong>.</li>
  <li><strong>Tích hợp Tính Bền vững &amp; Khả năng Phục hồi (Integrate Sustainability):</strong> Tối ưu hóa việc phân bổ nguồn lực (<em>Resource Leveling</em>), chống kiệt sức nhân sự (<em>Over-allocation</em>) và xây dựng chuỗi cung ứng bền vững.</li>
  <li><strong>Xây dựng Văn hóa Trao quyền &amp; Minh bạch Dữ liệu (Build an Empowered Culture):</strong> Thay thế văn hóa báo cáo thủ công bằng kho dữ liệu đám mây tập trung (Cloud Repository), nơi mọi thành viên cộng tác theo cơ chế <code>Check-out / Check-in</code> có kiểm soát phiên bản.</li>
</ol>

<h2>3. Phân tích Chuyên sâu 7 Miền Hiệu suất (7 Performance Domains) &amp; Ánh xạ sang 13 Hồ sơ Thực chiến</h2>
<p>
  Điểm đột phá giúp PMBOK 8 đi thẳng vào thực tiễn doanh nghiệp là sự phân tách rõ ràng <strong>7 Miền Hiệu suất (Performance Domains)</strong> — đặc biệt là việc nâng <strong>Quản trị (Governance)</strong>, <strong>Phạm vi (Scope)</strong>, <strong>Tiến độ (Schedule)</strong>, <strong>Tài chính (Finance)</strong> và <strong>Rủi ro (Risk)</strong> thành các miền độc lập có công thức đo lường định lượng rõ ràng.
</p>
<p>
  Trên nền tảng <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>ERX AI Project Gantt Planner</strong></a>, toàn bộ 7 miền hiệu suất này đã được số hóa thành <strong>13 Hồ sơ Quản trị Dự án Chuẩn PMBOK® 8</strong> liên kết trực tiếp với biểu đồ Gantt:
</p>

{figure_html("IMG_pm01_2", "Hệ thống 13 Hồ sơ Quản trị Dự án chuẩn PMBOK 8 đồng bộ thời gian thực trên project-management.erx.vn", "Hình 1: 13 Hồ sơ Quản trị Dự án chuẩn PMBOK® 8 được chia thành 4 nhóm chức năng đồng bộ trực tiếp với bảng WBS & Gantt.")}

<table>
  <thead>
    <tr>
      <th>Miền Hiệu suất PMBOK® 8</th>
      <th>Trọng tâm Quản trị &amp; Chỉ số Đo lường</th>
      <th>Hồ sơ &amp; Công cụ trên <code>project-management.erx.vn</code></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Governance (Quản trị)</strong></td>
      <td>Thiết lập quyền hạn, cổng phê duyệt (Stage Gate), tiêu chí thành công và căn cứ đầu tư dự án.</td>
      <td><strong>(01) Project Charter</strong>, <strong>(02) Business Case</strong>, <strong>(03) Benefits Plan</strong>, <strong>(09) Assumption &amp; Constraint Log</strong>.</td>
    </tr>
    <tr>
      <td><strong>2. Scope (Phạm vi &amp; Chất lượng)</strong></td>
      <td>Phân rã công việc theo Quy tắc 100%, kiểm soát trượt phạm vi (Scope Creep) và tiêu chuẩn nghiệm thu.</td>
      <td>Bảng <strong>WBS đa cấp</strong> (Summary / Work Package / Milestone), <strong>WBS Dictionary</strong> &amp; <strong>(07) Quality Metrics</strong>.</td>
    </tr>
    <tr>
      <td><strong>3. Schedule (Tiến độ)</strong></td>
      <td>Lập mạng logic PDM, xác định Đường găng (CPM), quản lý độ dự trữ <code>Free Slack</code> và <code>Total Slack</code>.</td>
      <td>Động cơ <strong>Gantt CPM chuẩn MS Project 2016</strong> (4 quan hệ <code>FS/SS/FF/SF</code>, Lag/Lead, 8 loại Constraints).</td>
    </tr>
    <tr>
      <td><strong>4. Finance (Tài chính Dự án)</strong></td>
      <td>Kiểm soát ngân sách cơ sở (<code>BAC</code>), giá trị thu được (<code>EV</code>), chi phí thực tế (<code>AC</code>) và dự báo <code>EAC</code>.</td>
      <td>Bảng <strong>9 chỉ số EVM thời gian thực</strong> (<code>BAC, PV, EV, AC, SV, CV, SPI, CPI, EAC</code>) &amp; <strong>11 khe Baseline</strong>.</td>
    </tr>
    <tr>
      <td><strong>5. Stakeholders (Bên liên quan)</strong></td>
      <td>Phân tích mức độ ảnh hưởng, phân quyền thực thi RACI và kế hoạch truyền thông điều hành.</td>
      <td><strong>(04) Stakeholder Register</strong> (Power/Interest), <strong>(05) RACI Matrix</strong>, <strong>(06) Communication Plan</strong> &amp; <strong>Executive Diff Telegram</strong>.</td>
    </tr>
    <tr>
      <td><strong>6. Resources (Nguồn lực)</strong></td>
      <td>Phương trình <code>Work = Duration × Units</code>, đường cong phân bổ công việc và cân bằng nhân sự.</td>
      <td><strong>(08) HR Plan</strong>, 3 kiểu Task (<code>Fixed Units/Duration/Work</code>), <strong>9 Work Contours</strong>, Rate Tables A–E &amp; <strong>Resource Leveling</strong>.</td>
    </tr>
    <tr>
      <td><strong>7. Risk (Quản trị Rủi ro)</strong></td>
      <td>Phân rã rủi ro (RBS), chấm điểm P×I và định lượng quỹ dự phòng bằng Giá trị Tiền tệ Kỳ vọng (<code>EMV</code>).</td>
      <td><strong>(10) RBS</strong>, <strong>(11) Risk Scale 1–5</strong>, <strong>(12) Risk Assessment (EMV = P% × Impact$)</strong> &amp; <strong>(13) Risk Register</strong>.</td>
    </tr>
  </tbody>
</table>

<h2>4. Vận hành Chu trình 5 Nhóm Quy trình (5 Process Groups) Kèm Case Study Thực tế</h2>
<p>
  Để thấy rõ cách PMBOK 8 vận hành trong thực tế, hãy xét dự án mẫu <strong>Chuẩn hóa Quy trình Mua hàng đến Thanh toán (Procure-to-Pay — Mã dự án: <code>P2P-FOUNDATION-2026</code>)</strong> được tích hợp sẵn trong Học viện Đào tạo của <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>:
</p>
<ul>
  <li><strong>Bước 1 — Khởi tạo (Initiating):</strong> Giám đốc Dự án lập <em>Project Charter</em> và <em>Business Case</em> xác định mục tiêu số hóa quy trình P2P trong <strong>28 ngày làm việc</strong> với sự tham gia của 7 bộ phận (PMO, Mua hàng, Tài chính, Kho vận, QA, CNTT, Nhà cung cấp).</li>
  <li><strong>Bước 2 — Lập kế hoạch (Planning):</strong> Phân rã phạm vi thành <strong>20 bước WBS</strong>. Thiết lập các mối quan hệ phụ thuộc thông minh (như kiểm tra ngân sách song song <code>SS+1d</code> để rút ngắn tiến độ). Tổng chi phí cơ sở của các gói công việc được hệ thống cuốn chiếu tự động là <code>BAC = $49,448</code>.</li>
  <li><strong>Bước 3 — Định lượng Rủi ro &amp; Chốt Baseline:</strong> Đội dự án nhận diện 8 rủi ro trọng yếu (<code>R1–R8</code>) và tính toán tổng quỹ dự phòng <code>EMV = $3,260</code>. Hệ thống lập tức đồng bộ <strong>Ngân sách Phê duyệt (Approved Budget) = $49,448 + $3,260 = $52,708</strong> và chốt <strong>Baseline 0</strong>.</li>
  <li><strong>Bước 4 — Thực thi Đám mây (Executing):</strong> Các trưởng nhóm sử dụng cơ chế <strong>Cloud Check-out</strong> để khóa dự án khi cập nhật phần trăm hoàn thành (<code>% Complete</code>) và giờ công thực tế (<code>Actual Work</code>), tránh xung đột dữ liệu.</li>
  <li><strong>Bước 5 — Giám sát EVM &amp; Đóng dự án (Monitoring, Controlling &amp; Closing):</strong> Mỗi khi thành viên <strong>Check-in</strong> phiên bản mới lên đám mây, hệ thống tự động tính toán lại chỉ số <code>SPI</code>, <code>CPI</code>, kiểm tra sự dịch chuyển của Đường găng (CPM) và gửi báo cáo <strong>Executive Diff</strong> trực tiếp qua Telegram cho Ban Giám đốc.</li>
</ul>

{figure_html("IMG_pm01_3", "Chu trình 5 bước quản trị dự án khép kín chuẩn PMBOK 8 trên project-management.erx.vn", "Hình 2: Chu trình 5 bước quản trị dự án khép kín từ khởi tạo Project Charter đến giám sát EVM và cảnh báo tự động.")}

{CTA_BOX_HTML}

<h2>5. Lộ trình Đọc Chuyên sâu: Bộ Cẩm nang Quản trị Dự án PMBOK® 8 trên ERX.VN</h2>
<p>
  Bài viết này là <strong>Trụ cột số 1 (Pillar 1)</strong> trong hệ sinh thái kiến thức <a href="https://erx.vn/project-management.html"><strong>Project Management</strong></a> của ERX. Để nắm vững từng kỹ thuật định lượng chuyên sâu, mời bạn đọc tiếp 3 bài trụ cột còn lại trong chuỗi bài:
</p>
<ul>
  <li>📘 <strong>Trụ cột 2 (Phạm vi &amp; Tiến độ):</strong> <a href="{{{{URL_PM04}}}}">Cấu trúc Phân rã Công việc (WBS) &amp; Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8</a> — Nắm vững Quy tắc 100%, Summary Task, Work Package và Milestone.</li>
  <li>📊 <strong>Trụ cột 3 (Kiểm soát Tài chính EVM):</strong> <a href="{{{{URL_PM08}}}}">Quản lý Giá trị Thu được (Earned Value Management - EVM): Cách tính BAC, PV, EV, AC, SPI, CPI &amp; Dự báo EAC</a>.</li>
  <li>🛡️ <strong>Trụ cột 4 (Định lượng Rủi ro EMV):</strong> <a href="{{{{URL_PM09}}}}">Định lượng Rủi ro Dự án bằng EMV (Expected Monetary Value) &amp; Cách tính Quỹ Dự phòng (Contingency Reserve)</a>.</li>
  <li>🔗 <strong>Liên kết Chuyên ngành Chuỗi Cung Ứng:</strong> Kết hợp cùng kiến thức tại chuyên mục <a href="https://erx.vn/procurement-management.html">Procurement Management (Quản trị Mua hàng)</a> và <a href="https://erx.vn/planning-management.html">Planning Management (Hoạch định Chuỗi cung ứng)</a>.</li>
</ul>

<h2>6. Câu hỏi Thường gặp (FAQ) về Chuẩn PMBOK® 8 &amp; Công cụ Quản lý Dự án</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: PMBOK 8 khác gì lớn nhất so với PMBOK 7?</h3>
  <p>
    PMBOK 8 tinh gọn 12 nguyên tắc xuống còn <strong>6 Nguyên tắc cốt lõi</strong>, tái cấu trúc thành <strong>7 Miền hiệu suất</strong> (tách bạch rõ <em>Governance, Scope, Schedule, Finance, Risk</em>) và đặc biệt là <strong>đưa 5 Nhóm Quy trình (Initiating → Closing) quay trở lại</strong> kết hợp với AI và dữ liệu thời gian thực, giúp người làm dự án dễ áp dụng hơn rất nhiều so với PMBOK 7.
  </p>
  <h3>Câu hỏi 2: Doanh nghiệp vừa và nhỏ có cần lập đủ 13 hồ sơ PMBOK 8 không?</h3>
  <p>
    Theo nguyên tắc <em>Tailoring (Tùy biến phù hợp)</em> của PMBOK 8, bạn không cần soạn 13 file Word dài hàng trăm trang. Khi sử dụng <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, cả 13 hồ sơ (từ Project Charter, RACI đến Risk EMV) được gói gọn trong các tab dữ liệu có cấu trúc sẵn và <strong>AI Co-Pilot</strong> có thể khởi tạo bản nháp chuẩn chỉnh chỉ trong 30 giây.
  </p>
  <h3>Câu hỏi 3: Nền tảng project-management.erx.vn có tương thích với Microsoft Project không?</h3>
  <p style="margin-bottom: 0;">
    Có. Động cơ lập lịch của <code>project-management.erx.vn</code> được thiết kế đạt chuẩn <strong>Microsoft Project 2016 Parity</strong> (hỗ trợ đầy đủ WBS, 4 quan hệ phụ thuộc <code>FS/SS/FF/SF</code>, Lag/Lead, Đường găng CPM, 11 Baselines, 9 chỉ số EVM, Resource Leveling) và hỗ trợ xuất/nhập dữ liệu hai chiều qua Excel (<code>.xlsx</code>) và JSON.
  </p>
</div>
"""

# ==============================================================================
# ARTICLE 2: PM-04
# ==============================================================================
pm04_html = f"""
<h2>1. WBS (Work Breakdown Structure) là gì theo định nghĩa chuẩn PMBOK® 8?</h2>
<p>
  Theo <strong>PMBOK® Guide – 8th Edition</strong> (Miền hiệu suất <em>Scope Performance Domain</em>), <strong>WBS (Cấu trúc Phân rã Công việc)</strong> là sự phân tách có thứ bậc, hướng theo giao phẩm (<em>deliverable-oriented hierarchical decomposition</em>) đối với toàn bộ phạm vi công việc mà đội dự án phải thực hiện để đạt được mục tiêu và tạo ra các sản phẩm bàn giao đã cam kết trong <em>Project Charter</em>.
</p>
<p>
  Nhiều người mới làm quản lý dự án thường nhầm lẫn WBS với một "danh sách việc cần làm" (To-do list) rời rạc. Sự khác biệt cốt lõi nằm ở chỗ:
</p>
<ul>
  <li><strong>To-do List thông thường:</strong> Chỉ liệt kê các hành động ngẫu nhiên nghĩ ra trong đầu, dễ trùng lặp hoặc bỏ sót các hạng mục kiểm thử, nghiệm thu, quản lý dự án.</li>
  <li><strong>WBS chuẩn PMBOK® 8:</strong> Phân rã từ tổng thể xuống chi tiết theo cấu trúc cây phân cấp (<em>Project Summary → Phase / Major Deliverable → Work Package &amp; Milestone</em>), trong đó mọi chi phí (<code>Cost</code>), giờ công (<code>Work</code>) và thời lượng (<code>Duration</code>) từ cấp dưới đều tự động cuốn chiếu (<em>roll-up</em>) lên cấp cha.</li>
</ul>

<h2>2. Hai Quy tắc Vàng khi Thiết kế WBS: Quy tắc 100% &amp; Quy tắc 8/80 Giờ</h2>
<h3>2.1. Quy tắc 100% (The 100% Rule)</h3>
<p>
  <strong>Quy tắc 100%</strong> là nguyên lý quan trọng nhất khi xây dựng WBS: <em>Tổng công việc ở cấp độ "con" (Child tasks) phải bằng đúng 100% phạm vi công việc được mô tả ở mục "cha" (Parent / Summary task)</em>.
</p>
<ul>
  <li><strong>Không nhỏ hơn 100% (Chống bỏ sót):</strong> Nếu Giai đoạn 2 là "Đấu thầu &amp; Lựa chọn Nhà cung cấp" nhưng các gói công việc con chỉ có "Phát hành RFQ" và "Nhận báo giá" mà quên mất gói "Đánh giá kỹ thuật &amp; Chấm điểm Scorecard" hoặc "Đàm phán hợp đồng", thì tiến độ và ngân sách cuốn chiếu lên sẽ bị thiếu hụt nghiêm trọng.</li>
  <li><strong>Không lớn hơn 100% (Chống mạ vàng / Gold Plating):</strong> Bất kỳ công việc nào không nằm trong phạm vi giao phẩm của mục cha thì tuyệt đối không được đưa vào WBS.</li>
</ul>

<h3>2.2. Quy tắc 8/80 Giờ (1 đến 10 Ngày làm việc) cho Gói Công việc (Work Package)</h3>
<p>
  Chúng ta nên chia nhỏ WBS đến mức nào thì dừng lại? PMBOK® khuyến nghị cấp thấp nhất của WBS — gọi là <strong>Gói công việc (Work Package)</strong> — nên tuân thủ <strong>Quy tắc 8/80 giờ</strong>:
</p>
<ul>
  <li>Không nên nhỏ hơn <strong>8 giờ làm việc (1 ngày)</strong>: Vì nếu chia vụn thành các việc 1–2 giờ, Giám đốc Dự án sẽ sa lầy vào quản lý vi mô (<em>Micromanagement</em>) và tốn quá nhiều thời gian cập nhật tiến độ.</li>
  <li>Không nên dài quá <strong>80 giờ làm việc (10 ngày / 2 tuần)</strong>: Vì một task kéo dài 30–45 ngày mà không được chia nhỏ sẽ trở thành "hộp đen" — bạn không thể phát hiện sớm sự chậm trễ cho đến khi thời hạn đã trôi qua.</li>
</ul>

<h2>3. Phân biệt 3 Loại Node trong Bảng WBS trên ERX AI Project Gantt Planner</h2>
<p>
  Khi thực hành lập tiến độ trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>project-management.erx.vn</strong></a>, động cơ lập lịch chuẩn MS Project 2016 phân biệt tự động 3 loại phần tử trong cây WBS:
</p>

{figure_html("IMG_pm04_2", "Mô hình bảng WBS và biểu đồ Gantt tự động tính Đường găng CPM trên project-management.erx.vn", "Hình 1: Mô hình bảng WBS kết hợp Biểu đồ Gantt và Đường găng (Critical Path màu đỏ) trên project-management.erx.vn.")}

<table>
  <thead>
    <tr>
      <th>Loại Phần tử WBS</th>
      <th>Đặc điểm Kỹ thuật &amp; Quy tắc Tính toán</th>
      <th>Thực hành Tốt nhất (Best Practice)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Summary Task (Công việc Tổng hợp &amp; Task 0)</strong></td>
      <td>
        Tự động tổng hợp (Roll-up) từ các task con:<br/>
        • <code>Start</code> = Min(Start của các con)<br/>
        • <code>Finish</code> = Max(Finish của các con)<br/>
        • <code>Cost / Work</code> = Tổng Cost / Work các con.
      </td>
      <td>Đặt tên theo <strong>Danh từ / Giao phẩm</strong> (VD: <em>Giai đoạn 2: Hồ sơ Đấu thầu RFQ &amp; Hợp đồng NCC</em>). Không gán trực tiếp nhân sự vào Summary Task.</td>
    </tr>
    <tr>
      <td><strong>2. Work Package (Gói công việc Thực thi)</strong></td>
      <td>
        Cấp lá (Leaf task) nơi phát sinh công sức và chi phí thực tế theo phương trình:<br/>
        <code>Work = Duration × Units</code>.
      </td>
      <td>Đặt tên bắt đầu bằng <strong>Động từ hành động + Kết quả</strong> (VD: <em>Phát hành hồ sơ mời thầu RFQ</em>). Luôn nối đủ Predecessor và Successor.</td>
    </tr>
    <tr>
      <td><strong>3. Milestone (Cột mốc Kiểm soát — <code>Duration = 0d</code>)</strong></td>
      <td>
        Có thời lượng bằng <strong>0 ngày (<code>0d</code>)</strong>, biểu diễn bằng hình thoi màu vàng trên biểu đồ Gantt, không tiêu tốn giờ công.
      </td>
      <td>Đặt ở cuối mỗi giai đoạn để làm cổng phê duyệt (<em>Stage Gate</em>) và đồng bộ sang bảng <em>Milestone Summary</em> trong Project Charter.</td>
    </tr>
  </tbody>
</table>

<h2>4. Từ điển WBS (WBS Dictionary) là gì? Tại sao Chỉ có Cây WBS là Chưa Đủ?</h2>
<p>
  Trên bảng tiến độ Gantt, tên mỗi dòng công việc thường chỉ dài từ 5 đến 10 từ (ví dụ: <code>WBS 3.1 — Đối soát Hóa đơn 3-Way Matching</code>). Nếu không có tài liệu định nghĩa rõ <em>"Đối soát như thế nào là đạt chuẩn? Dung sai cho phép là bao nhiêu? Ai ký duyệt?"</em>, các phòng ban sẽ đùn đẩy trách nhiệm khi nghiệm thu.
</p>
<p>
  Đó chính là vai trò của <strong>Từ điển WBS (WBS Dictionary)</strong> trong PMBOK® 8. Mỗi thẻ trong Từ điển WBS đóng vai trò như một "hợp đồng giao việc thu nhỏ" gồm 6 trường thông tin bắt buộc:
</p>

{figure_html("IMG_pm04_3", "Cấu trúc Từ điển WBS (WBS Dictionary) chuẩn PMBOK 8 gồm 6 trường thông tin trên project-management.erx.vn", "Hình 2: 6 trường thông tin cốt lõi của một thẻ Từ điển WBS (WBS Dictionary) chuẩn PMBOK® 8.")}

<ol>
  <li><strong>Mã định danh WBS &amp; Tên gói công việc (WBS Code &amp; Title):</strong> Đánh số phân cấp tự động (<code>1.1</code>, <code>1.2</code>, <code>2.1.1</code>) để truy vết xuyên suốt giữa bảng Gantt, bảng RACI và sổ đăng ký rủi ro (Risk Register).</li>
  <li><strong>Mô tả Phạm vi Công việc (Statement of Work):</strong> Nêu rõ ranh giới công việc cần làm (In-Scope) và không làm (Out-of-Scope).</li>
  <li><strong>Giao phẩm &amp; Tiêu chí Nghiệm thu (Deliverables &amp; Acceptance Metrics):</strong> Liên kết trực tiếp với hồ sơ <em>(07) Quality Metrics</em> trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>.</li>
  <li><strong>Giả định &amp; Ràng buộc Lịch trình (Assumptions &amp; Schedule Constraints):</strong> Xác định rõ loại ràng buộc (mặc định nên dùng <code>As Soon As Possible - ASAP</code> để không làm méo Đường găng CPM; chỉ dùng <code>Must Finish On - MFO</code> khi có hạn chót pháp lý cứng).</li>
  <li><strong>Định mức Nguồn lực &amp; Ngân sách Cơ sở (Resource &amp; Cost Baseline):</strong> Khai báo kiểu task (<code>Fixed Units</code>, <code>Fixed Duration</code> hay <code>Fixed Work</code>), nhân sự thực hiện, đơn giá theo bảng <code>Cost Rate Tables A–E</code> và ngân sách <code>BAC</code> của gói công việc.</li>
  <li><strong>Liên kết Trách nhiệm RACI &amp; Mã Rủi ro (RACI &amp; Risk ID):</strong> Chỉ định rõ ai là <code>R</code> (Responsible), ai là <code>A</code> (Accountable) và gắn mã rủi ro (ví dụ <code>R-05</code>) nếu gói công việc nằm trên Đường găng.</li>
</ol>

{CTA_BOX_HTML}

<h2>5. Bài viết Liên quan trong Hệ sinh thái Quản trị Dự án PMBOK® 8</h2>
<ul>
  <li>📘 <strong>Tổng quan Khung tiêu chuẩn:</strong> <a href="{{{{URL_PM01}}}}">Quản trị Dự án theo chuẩn PMBOK 8: Tổng quan 6 Nguyên tắc, 7 Miền hiệu suất &amp; 5 Nhóm quy trình thực chiến</a>.</li>
  <li>📊 <strong>Đo lường Tiến độ &amp; Chi phí từ WBS:</strong> <a href="{{{{URL_PM08}}}}">Quản lý Giá trị Thu được (Earned Value Management - EVM): Cách tính BAC, PV, EV, AC, SPI, CPI &amp; Dự báo EAC</a>.</li>
  <li>🛡️ <strong>Tính Quỹ Dự phòng Rủi ro cho các Gói WBS:</strong> <a href="{{{{URL_PM09}}}}">Định lượng Rủi ro Dự án bằng EMV (Expected Monetary Value) &amp; Cách tính Quỹ Dự phòng (Contingency Reserve)</a>.</li>
  <li>📦 <strong>Ứng dụng trong Quản trị Chuỗi Cung Ứng:</strong> Xem thêm tại chuyên mục <a href="https://erx.vn/supply-chain-management.html">Supply Chain Management</a> và <a href="https://erx.vn/excel-functions.html">Excel Functions</a>.</li>
</ul>

<h2>6. Câu hỏi Thường gặp (FAQ) về WBS &amp; Từ điển WBS</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: Có nên gắn mối quan hệ phụ thuộc (Predecessors) vào Summary Task không?</h3>
  <p>
    Theo chuẩn thực hành tốt nhất của PMI và Microsoft Project, bạn nên gắn quan hệ phụ thuộc (<code>FS, SS, FF, SF</code>) trực tiếp giữa các <strong>Work Packages (cấp lá)</strong> và <strong>Milestones</strong> thay vì gắn vào Summary Task. Việc gắn vào cấp lá giúp động cơ CPM tính toán <code>Free Slack</code> và <code>Total Slack</code> chính xác tuyệt đối, tránh lỗi vòng lặp logic (Circular Dependency).
  </p>
  <h3>Câu hỏi 2: Khi nào nên dùng Indentation (Thụt lề) trên project-management.erx.vn?</h3>
  <p>
    Trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, bạn chỉ cần bấm nút <strong>Indent (Thụt lề sang phải)</strong> hoặc <strong>Outdent (Thụt lề sang trái)</strong> trên thanh công cụ: hệ thống sẽ tự động biến công việc phía trên thành <em>Summary Task</em>, tự động đánh lại toàn bộ mã số WBS (<code>1.1 → 1.1.1</code>) và tự động cuốn chiếu thời lượng, chi phí theo thời gian thực.
  </p>
  <h3>Câu hỏi 3: Làm sao để tạo nhanh WBS chuẩn PMBOK 8 cho một dự án mới?</h3>
  <p style="margin-bottom: 0;">
    Bạn có thể mở tính năng <strong>AI Project Co-Pilot</strong> trên <code>project-management.erx.vn</code>, nhập mô tả mục tiêu dự án (ví dụ: <em>"Triển khai hệ thống WMS cho kho 10.000m2 trong 45 ngày"</em>), AI sẽ tự động sinh cây WBS đa cấp kèm Predecessors, phân bổ nguồn lực và bộ 13 hồ sơ PMBOK 8 hoàn chỉnh.
  </p>
</div>
"""

# ==============================================================================
# ARTICLE 3: PM-08
# ==============================================================================
pm08_html = f"""
<h2>1. Sai lầm Kinh điển khi Kiểm soát Ngân sách Dự án &amp; Bản chất của EVM</h2>
<p>
  Hãy hình dung một tình huống thực tế rất phổ biến tại các doanh nghiệp: Dự án của bạn có tổng ngân sách cơ sở (<code>BAC</code>) là <strong>$49,448</strong> và kéo dài trong <strong>28 ngày</strong>. Đến Ngày báo cáo (<em>Status Date</em> — ngày thứ 16), theo kế hoạch bạn dự kiến chi hết <strong>$29,600</strong>. Bộ phận kế toán báo cáo rằng số tiền thực tế đã chi trả (<code>AC</code>) đúng bằng <strong>$29,600</strong>.
</p>
<p>
  Nếu chỉ so sánh <em>Ngân sách Kế hoạch ($29,600)</em> với <em>Chi phí Thực tế ($29,600)</em>, nhiều người sẽ lầm tưởng rằng dự án đang đi đúng hướng 100%! Nhưng khi kiểm tra khối lượng công việc thực tế đã hoàn thành dưới hiện trường, đội dự án mới chỉ làm xong lượng công việc tương đương giá trị <strong>$26,640</strong>. Điều đó có nghĩa là:
</p>
<ul>
  <li>Dự án đang <strong>trễ tiến độ -$2,960</strong> giá trị công việc so với kế hoạch; VÀ</li>
  <li>Dự án đang <strong>vượt chi phí -$2,960</strong> (bỏ ra $29,600 nhưng chỉ thu về $26,640 giá trị).</li>
</ul>
<p>
  Đó chính là lý do <strong>Earned Value Management (EVM)</strong> trong Miền hiệu suất Tài chính (<em>Finance Performance Domain</em>) của <strong>PMBOK® 8</strong> là tiêu chuẩn vàng bắt buộc đối với mọi Giám đốc Dự án chuyên nghiệp.
</p>

<h2>2. Giải mã 4 Tham số Nền tảng của EVM: BAC, PV, EV và AC</h2>
<p>
  Trước khi tính toán các chỉ số chênh lệch và dự báo, hệ thống EVM trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a> thu thập 4 tham số gốc từ bảng WBS và Baseline đã chốt:
</p>
<ol>
  <li><strong>BAC (Budget at Completion — Ngân sách Cơ sở khi Hoàn thành):</strong> Tổng chi phí kế hoạch của tất cả các gói công việc (Work Packages) trong dự án khi bạn bấm chốt <code>Set Baseline</code>. Trong dự án mẫu P2P, <code>BAC = $49,448</code>.</li>
  <li><strong>PV (Planned Value — Giá trị Kế hoạch / BCWS):</strong> Giá trị ngân sách được phân bổ cho phần công việc <em>lẽ ra phải hoàn thành</em> tính đến Ngày báo cáo (Status Date). Công thức ở cấp từng task: <code>PV = BAC_task × % Kế hoạch tại Status Date</code>.</li>
  <li><strong>EV (Earned Value — Giá trị Thu được / BCWP):</strong> Giá trị ngân sách gốc của phần công việc <em>thực sự đã hoàn thành</em> tính đến Ngày báo cáo. Công thức: <code>EV = BAC_task × % Complete (Thực tế)</code>. Đây là chỉ số quan trọng nhất của EVM!</li>
  <li><strong>AC (Actual Cost — Chi phí Thực tế / ACWP):</strong> Tổng số tiền thực tế đã chi ra để hoàn thành phần công việc <code>EV</code> tính đến Ngày báo cáo (bao gồm giờ công thực tế <code>Actual Work × Standard/Overtime Rate</code> cộng với <code>Actual Fixed Cost</code>).</li>
</ol>

<h2>3. Bảng Tổng hợp Toàn bộ 9 Công thức EVM Chuẩn PMBOK® 8</h2>
<p>
  Từ 4 tham số gốc (<code>BAC, PV, EV, AC</code>), động cơ tài chính của <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>ERX AI Project Gantt Planner</strong></a> tự động tính toán tức thời toàn bộ 9 chỉ số kiểm soát và dự báo ngân sách:
</p>

{figure_html("IMG_pm08_3", "Bảng tổng hợp 9 công thức Earned Value Management (EVM) chuẩn PMBOK 8 trên project-management.erx.vn", "Hình 1: 9 công thức Earned Value Management (EVM) cốt lõi được tính tự động trên 11 khe Baseline của ERX Gantt Planner.")}

<table>
  <thead>
    <tr>
      <th>Chỉ số EVM</th>
      <th>Công thức Toán học</th>
      <th>Ý nghĩa Điều hành &amp; Ngưỡng Đánh giá</th>
      <th>Ví dụ P2P tại Ngày 16</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Chênh lệch Tiến độ (SV)</strong></td>
      <td><code>SV = EV − PV</code></td>
      <td><code>SV &lt; 0</code>: Trễ tiến độ | <code>SV &gt; 0</code>: Vượt tiến độ (tính bằng tiền).</td>
      <td><code>$26,640 − $29,600 = -$2,960</code></td>
    </tr>
    <tr>
      <td><strong>Chênh lệch Chi phí (CV)</strong></td>
      <td><code>CV = EV − AC</code></td>
      <td><code>CV &lt; 0</code>: Đội chi phí | <code>CV &gt; 0</code>: Tiết kiệm chi phí so với dự toán.</td>
      <td><code>$26,640 − $29,600 = -$2,960</code></td>
    </tr>
    <tr>
      <td><strong>Chỉ số Hiệu suất Tiến độ (SPI)</strong></td>
      <td><code>SPI = EV / PV</code></td>
      <td><code>SPI ≥ 1.00</code>: Tốt | <code>0.90–0.99</code>: Cảnh báo vàng | <code>&lt; 0.90</code>: Báo động đỏ.</td>
      <td><code>$26,640 / $29,600 = 0.90</code></td>
    </tr>
    <tr>
      <td><strong>Chỉ số Hiệu suất Chi phí (CPI)</strong></td>
      <td><code>CPI = EV / AC</code></td>
      <td>Cho biết mỗi <code>$1.00</code> chi ra thu về bao nhiêu <code>$</code> giá trị công việc.</td>
      <td><code>$26,640 / $29,600 = 0.90</code></td>
    </tr>
    <tr>
      <td><strong>Dự báo Chi phí Khi Hoàn thành (EAC)</strong></td>
      <td><code>EAC = BAC / CPI</code></td>
      <td>Dự báo tổng số tiền thực tế dự án sẽ tiêu tốn khi hoàn tất 100% nếu giữ hiệu suất <code>CPI</code> hiện tại.</td>
      <td><code>$49,448 / 0.90 = $54,942</code></td>
    </tr>
    <tr>
      <td><strong>Chi phí Cần thêm để Hoàn tất (ETC)</strong></td>
      <td><code>ETC = EAC − AC</code></td>
      <td>Số tiền dòng tiền (Cashflow) cần chuẩn bị thêm từ ngày báo cáo đến cuối dự án.</td>
      <td><code>$54,942 − $29,600 = $25,342</code></td>
    </tr>
    <tr>
      <td><strong>Chênh lệch Khi Hoàn thành (VAC)</strong></td>
      <td><code>VAC = BAC − EAC</code></td>
      <td>Dự báo mức thâm hụt ngân sách cuối kỳ (<code>VAC &lt; 0</code> cần đối chiếu ngay với Quỹ dự phòng EMV).</td>
      <td><code>$49,448 − $54,942 = -$5,494</code></td>
    </tr>
    <tr>
      <td><strong>Chỉ số Hiệu suất Cần đạt (TCPI)</strong></td>
      <td><code>(BAC − EV) / (BAC − AC)</code></td>
      <td>Hiệu suất chi phí bắt buộc phải đạt trong phần việc còn lại để không vượt ngân sách <code>BAC</code>.</td>
      <td><code>$22,808 / $19,848 = 1.15</code></td>
    </tr>
  </tbody>
</table>

<h2>4. Ma trận Chẩn đoán 4 Góc Phần tư (SPI × CPI) cho Giám đốc Dự án</h2>
<p>
  Trong thực tế điều hành, việc đọc riêng lẻ từng con số không quan trọng bằng việc <strong>kết hợp đồng thời cặp chỉ số <code>SPI</code> và <code>CPI</code></strong> để ra quyết định can thiệp đúng bệnh:
</p>

{figure_html("IMG_pm08_2", "Ma trận chẩn đoán sức khỏe dự án 4 góc phần tư SPI x CPI chuẩn PMBOK 8 trên project-management.erx.vn", "Hình 2: Ma trận 4 góc phần tư chẩn đoán sức khỏe dự án kết hợp SPI (Tiến độ) và CPI (Chi phí).")}

<ul>
  <li><strong>Góc phần tư 1 (<code>SPI &gt; 1.0</code> nhưng <code>CPI &lt; 1.0</code> — Nhanh tiến độ nhưng Đội chi phí):</strong> Đội dự án đang lạm dụng kỹ thuật <em>Crashing</em> (tăng ca Overtime hoặc thuê thêm nhà thầu phụ giá cao) cả ở những công việc không nằm trên Đường găng. Cần cắt giảm ngay giờ làm thêm ở các task có <code>Total Slack &gt; 0</code>.</li>
  <li><strong>Góc phần tư 2 (<code>SPI ≥ 1.0</code> và <code>CPI ≥ 1.0</code> — Dự án Lý tưởng):</strong> Tiến độ và ngân sách đều nằm trong vùng kiểm soát xanh. Duy trì Baseline hiện tại và giải phóng dần quỹ dự phòng rủi ro khi các rủi ro hết hiệu lực.</li>
  <li><strong>Góc phần tư 3 (<code>SPI &lt; 1.0</code> và <code>CPI &lt; 1.0</code> — Báo động Đỏ Toàn diện):</strong> Như ví dụ ở trên (<code>SPI = 0.90, CPI = 0.90</code>), dự án dự kiến đội vốn <code>-$5,494</code> trong khi quỹ dự phòng rủi ro <code>EMV</code> chỉ có <code>$3,260</code>. Giám đốc Dự án phải áp dụng <em>Fast-Tracking</em> (chuyển quan hệ <code>FS</code> sang <code>SS + Lag</code>) trên Đường găng và kích hoạt kế hoạch giảm thiểu rủi ro ngay lập tức.</li>
  <li><strong>Góc phần tư 4 (<code>SPI &lt; 1.0</code> nhưng <code>CPI ≥ 1.0</code> — Tiết kiệm chi phí nhưng Trễ tiến độ):</strong> Thường xảy ra khi thiếu nhân sự thực thi hoặc bị nghẽn cổ chai ở khâu chờ phê duyệt. Giải pháp là chạy công cụ <strong>Resource Leveling</strong> trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a> để điều chuyển nguồn lực sang các task nằm trên Đường găng.</li>
</ul>

{CTA_BOX_HTML}

<h2>5. Bài viết Liên quan trong Hệ sinh thái Quản trị Dự án PMBOK® 8</h2>
<ul>
  <li>📘 <strong>Tổng quan PMBOK 8:</strong> <a href="{{{{URL_PM01}}}}">Quản trị Dự án theo chuẩn PMBOK 8: Tổng quan 6 Nguyên tắc, 7 Miền hiệu suất &amp; 5 Nhóm quy trình thực chiến</a>.</li>
  <li>🌳 <strong>Xây dựng WBS để tính BAC chuẩn xác:</strong> <a href="{{{{URL_PM04}}}}">Cấu trúc Phân rã Công việc (WBS) &amp; Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8</a>.</li>
  <li>🛡️ <strong>Kết hợp BAC với Quỹ dự phòng EMV:</strong> <a href="{{{{URL_PM09}}}}">Định lượng Rủi ro Dự án bằng EMV (Expected Monetary Value) &amp; Cách tính Quỹ Dự phòng (Contingency Reserve)</a>.</li>
  <li>📊 <strong>Phân tích Dữ liệu Tài chính &amp; BI:</strong> Tham khảo thêm chuyên mục <a href="https://erx.vn/power-bi.html">Power BI</a> và <a href="https://erx.vn/procurement-management.html">Procurement Management</a>.</li>
</ul>

<h2>6. Câu hỏi Thường gặp (FAQ) về Earned Value Management (EVM)</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: Tại sao khi dự án hoàn thành 100%, chỉ số SV luôn bằng 0 và SPI luôn bằng 1.0 dù dự án bị trễ hạn?</h3>
  <p>
    Khi dự án kết thúc 100%, toàn bộ khối lượng kế hoạch đã được thực hiện xong nên <code>EV = PV = BAC</code>, dẫn đến <code>SV = 0</code> và <code>SPI = 1.0</code>. Đây là đặc tính toán học của EVM truyền thống (tính theo tiền). Vì vậy, trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, bạn nên theo dõi song song cả <strong>SPI (EVM)</strong> lẫn <strong>Đường găng CPM (Finish Variance so với Baseline Finish)</strong> để kiểm soát chặt cả tiền lẫn ngày kết thúc thực tế.
  </p>
  <h3>Câu hỏi 2: Khi nào được phép cập nhật lại Baseline (Re-baseline) trên hệ thống?</h3>
  <p>
    Bạn tuyệt đối không được tự ý ghi đè <code>Baseline 0</code> chỉ để làm đẹp chỉ số <code>SPI/CPI</code>! Chỉ khi có yêu cầu thay đổi phạm vi chính thức (<em>Approved Change Request</em>) được Sponsor phê duyệt, bạn mới lưu thêm vào các khe <strong>Baseline 1 đến Baseline 10</strong> trên <code>project-management.erx.vn</code> để giữ nguyên lịch sử đối chiếu với <code>Baseline 0</code> ban đầu.
  </p>
  <h3>Câu hỏi 3: Chỉ số TCPI &gt; 1.10 cảnh báo điều gì?</h3>
  <p style="margin-bottom: 0;">
    <code>TCPI (To-Complete Performance Index) &gt; 1.10</code> cho biết để không vượt ngân sách gốc, hiệu suất chi phí trong phần việc còn lại phải tăng đột biến trên 110% — một ngưỡng rất khó khả thi nếu không cắt giảm phạm vi hoặc trích Quỹ dự phòng Rủi ro (EMV).
  </p>
</div>
"""

# ==============================================================================
# ARTICLE 4: PM-09
# ==============================================================================
pm09_html = f"""
<h2>1. Tại sao Cộng Cảm tính "10% Dự phòng phí" luôn Làm Hỏng Kế hoạch Tài chính Dự án?</h2>
<p>
  Trong thực tế lập dự toán tại nhiều doanh nghiệp, sau khi cộng tổng chi phí các gói công việc WBS ra con số <code>BAC</code> (ví dụ <code>$49,448</code>), người lập kế hoạch thường nhân thêm một tỷ lệ cố định 5% hoặc 10% để làm "quỹ dự phòng rủi ro". Cách làm cảm tính này dẫn đến hai hệ lụy lớn khi bảo vệ ngân sách trước Hội đồng Đầu tư (Sponsor / CFO):
</p>
<ul>
  <li><strong>Không thể giải trình căn cứ toán học:</strong> Khi Giám đốc Tài chính hỏi <em>"Tại sao lại là $5,000 dự phòng mà không phải $2,500? Số tiền này gắn với rủi ro cụ thể nào?"</em>, đội dự án không có câu trả lời định lượng.</li>
  <li><strong>Không tự động cập nhật khi rủi ro thay đổi:</strong> Khi một rủi ro lớn ở giai đoạn đấu thầu đã qua đi an toàn hoặc một rủi ro kỹ thuật mới phát sinh, con số 10% cố định không phản ánh được mức độ phơi nhiễm rủi ro thực tế (<em>Risk Exposure</em>) của dự án.</li>
</ul>
<p>
  Trong Miền hiệu suất Rủi ro (<em>Risk Performance Domain</em>) của <strong>PMBOK® Guide – 8th Edition</strong>, giải pháp chuẩn mực để kết nối trực tiếp Quản trị Rủi ro với Quản trị Tài chính là sử dụng công thức <strong>EMV (Expected Monetary Value — Giá trị Tiền tệ Kỳ vọng)</strong>.
</p>

<h2>2. Quy trình 4 Bước từ Nhận diện Rủi ro (RBS) đến Công thức Định lượng EMV</h2>

<h3>Bước 1: Xây dựng Cấu trúc Phân rã Rủi ro (RBS — Risk Breakdown Structure)</h3>
<p>
  Giống như WBS dùng để chống bỏ sót phạm vi công việc, <strong>RBS (Hồ sơ số 10 trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>)</strong> giúp đội dự án quét toàn diện các nguồn phát sinh rủi ro theo 4 nhóm chính:
</p>
<ol>
  <li><strong>Rủi ro Kỹ thuật &amp; Tích hợp (Technical Risks):</strong> Lỗi cổng API ERP, sai lệch dữ liệu master data, hiệu năng hệ thống.</li>
  <li><strong>Rủi ro Quản trị &amp; Tổ chức (Governance &amp; Resource Risks):</strong> Chậm phê duyệt liên phòng ban, tắc nghẽn nhân sự chủ chốt giai đoạn UAT.</li>
  <li><strong>Rủi ro Thương mại &amp; Nhà cung cấp (Commercial &amp; Supply Chain Risks):</strong> Báo giá vượt trần dự toán, biến động Lead-time giao hàng, đứt gãy nguồn cung.</li>
  <li><strong>Rủi ro Bên ngoài &amp; Pháp lý (External &amp; Compliance Risks):</strong> Thay đổi quy định thuế/hóa đơn điện tử, tỷ giá ngoại tệ, bảo mật dữ liệu thầu.</li>
</ol>

<h3>Bước 2: Đánh giá Định tính trên Ma trận Nhiệt 5×5 (Probability × Impact Heatmap)</h3>
<p>
  Trước khi tính tiền, mỗi rủi ro được chấm điểm trên thang đo chuẩn hóa từ <code>1 đến 5</code> về <strong>Xác suất xảy ra (Probability - P)</strong> và <strong>Mức độ tác động (Impact - I)</strong> (Hồ sơ số 11 — <em>Risk Scale</em>). Tích số <code>Risk Score = P × I</code> (từ 1 đến 25) giúp phân tầng mức độ ưu tiên xử lý trên Ma trận Nhiệt 5×5:
</p>

{figure_html("IMG_pm09_2", "Ma trận nhiệt đánh giá rủi ro 5x5 (Probability x Impact Risk Heatmap) và chiến lược phản ứng chuẩn PMBOK 8", "Hình 1: Ma trận Nhiệt Rủi ro 5×5 (P×I Heatmap) và 4 ngưỡng chiến lược phản ứng rủi ro trên project-management.erx.vn.")}

<h3>Bước 3: Định lượng Giá trị Tiền tệ Kỳ vọng (<code>EMV = P% × Impact$</code>)</h3>
<p>
  Với từng rủi ro đã nhận diện, ta xác định:
</p>
<ul>
  <li><strong>Xác suất xảy ra định lượng (<code>P_i %</code>):</strong> Từ <code>0%</code> đến <code>100%</code> (ví dụ: <code>25%</code>).</li>
  <li><strong>Tác động tài chính nếu rủi ro xảy ra (<code>Impact_i $</code>):</strong> Chi phí khắc phục, tiền phạt trễ hạn hoặc chi phí làm lại (ví dụ: <code>$3,200</code>).</li>
</ul>
<p>
  Khi đó, <strong>Giá trị Tiền tệ Kỳ vọng (EMV)</strong> của rủi ro <code>i</code> và tổng <strong>Quỹ Dự phòng Rủi ro (Contingency Reserve)</strong> của toàn dự án được tính theo công thức:
</p>
<pre style="background: #f8fafc; color: #0f172a; border: 1px solid #cbd5e1; border-left: 4px solid #10b981; padding: 16px 20px; border-radius: 8px; overflow-x: auto;"><code>EMV_i ($) = Xác suất xảy ra (P_i %) × Tác động tài chính (Impact_i $)

Quỹ Dự phòng Rủi ro (Contingency Reserve) = Σ EMV_i = Σ (P_i % × Impact_i $)</code></pre>

<h3>Bước 4: Đồng bộ Tự động vào Ngân sách Phê duyệt (<code>Approved Budget = BAC + EMV</code>)</h3>
<p>
  Trên các phần mềm truyền thống, bảng Risk Register trong Excel hoàn toàn tách biệt với file MS Project. Ngược lại, trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener"><strong>project-management.erx.vn</strong></a>, module <em>Risk Assessment Matrix (Hồ sơ số 12)</em> được lập trình liên kết trực tiếp với bảng ngân sách trong <em>Project Charter</em>:
</p>
<ul>
  <li>Mỗi khi bạn thay đổi xác suất <code>P%</code> hoặc mức tác động <code>Impact($)</code> của bất kỳ rủi ro nào từ <code>R1</code> đến <code>R8</code>, hệ thống lập tức tính lại <code>EMV_i</code> và cộng tổng thành <strong>Contingency Reserve</strong>.</li>
  <li>Tổng <strong>Contingency Reserve</strong> này tự động cộng với <strong>BAC (Ngân sách Cơ sở từ WBS)</strong> để tạo ra <strong>Approved Budget (Ngân sách Phê duyệt / Cost Baseline)</strong> theo thời gian thực!</li>
</ul>

<h2>3. Minh họa Thực tế: Bảng Tính EMV cho 8 Rủi ro Dự án Chuỗi Cung Ứng P2P ($52,708)</h2>
<p>
  Dưới đây là bảng dữ liệu thực tế trích xuất từ dự án mẫu <strong><code>P2P-FOUNDATION-2026</code></strong> trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>, minh họa cách 8 rủi ro trọng yếu tạo nên quỹ dự phòng <strong>$3,260</strong> trên nền ngân sách WBS <strong>$49,448</strong>:
</p>

{figure_html("IMG_pm09_3", "Bảng tính Quỹ dự phòng EMV thực tế cho 8 rủi ro dự án Chuỗi cung ứng P2P ($49,448 BAC + $3,260 EMV = $52,708) trên project-management.erx.vn", "Hình 2: Bảng tính EMV chi tiết trong dự án P2P-FOUNDATION-2026 trên project-management.erx.vn.")}

<table>
  <thead>
    <tr>
      <th>Mã</th>
      <th>Sự kiện Rủi ro (Risk Event)</th>
      <th>Nhóm RBS</th>
      <th>Xác suất (P%)</th>
      <th>Impact ($)</th>
      <th>EMV = P×I ($)</th>
      <th>Chiến lược Phản ứng (PMBOK 8)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>R1</strong></td>
      <td>Chậm phê duyệt ngân sách PR liên phòng ban</td>
      <td>Governance</td>
      <td>25%</td>
      <td>$3,200</td>
      <td><strong>$800</strong></td>
      <td><strong>Mitigate:</strong> Áp dụng SLA 24h &amp; Escalation Matrix.</td>
    </tr>
    <tr>
      <td><strong>R2</strong></td>
      <td>Nhà cung cấp báo giá vượt trần dự toán</td>
      <td>Procurement</td>
      <td>30%</td>
      <td>$2,500</td>
      <td><strong>$750</strong></td>
      <td><strong>Mitigate:</strong> Đấu thầu cạnh tranh tối thiểu 3 NCC.</td>
    </tr>
    <tr>
      <td><strong>R3</strong></td>
      <td>Lỗi tích hợp cổng API ERP &amp; E-Procurement</td>
      <td>Technical</td>
      <td>20%</td>
      <td>$2,800</td>
      <td><strong>$560</strong></td>
      <td><strong>Mitigate:</strong> Kiểm thử tích hợp Sandbox sớm ở Phase 2.</td>
    </tr>
    <tr>
      <td><strong>R4</strong></td>
      <td>Giao hàng trễ hạn do biến động Lead-time</td>
      <td>Supply Chain</td>
      <td>25%</td>
      <td>$1,600</td>
      <td><strong>$400</strong></td>
      <td><strong>Transfer/Mitigate:</strong> Điều khoản phạt SLA &amp; cảnh báo ASN.</td>
    </tr>
    <tr>
      <td><strong>R5</strong></td>
      <td>Sai lệch bộ chứng từ 3-Way Matching (PO-GRN-Inv)</td>
      <td>Finance / AP</td>
      <td>20%</td>
      <td>$1,500</td>
      <td><strong>$300</strong></td>
      <td><strong>Mitigate:</strong> Tự động hóa đối soát dung sai ≤ 0.5%.</td>
    </tr>
    <tr>
      <td><strong>R6</strong></td>
      <td>Quá tải nhân sự chủ chốt giai đoạn UAT</td>
      <td>Resources</td>
      <td>15%</td>
      <td>$1,400</td>
      <td><strong>$210</strong></td>
      <td><strong>Mitigate:</strong> Chạy Resource Leveling &amp; bố trí nhân sự dự phòng.</td>
    </tr>
    <tr>
      <td><strong>R7</strong></td>
      <td>Phát sinh yêu cầu thay đổi biểu mẫu phê duyệt</td>
      <td>Scope</td>
      <td>15%</td>
      <td>$1,000</td>
      <td><strong>$150</strong></td>
      <td><strong>Avoid:</strong> Khóa WBS Dictionary &amp; kiểm soát qua Change Board.</td>
    </tr>
    <tr>
      <td><strong>R8</strong></td>
      <td>Rủi ro rò rỉ dữ liệu báo giá nhà cung cấp</td>
      <td>Compliance</td>
      <td>10%</td>
      <td>$900</td>
      <td><strong>$90</strong></td>
      <td><strong>Avoid:</strong> Phân quyền RBAC &amp; ký NDA điện tử.</td>
    </tr>
  </tbody>
  <tfoot>
    <tr style="background: #ecfdf5; font-weight: 700; color: #065f46;">
      <td colspan="5" style="text-align: right;">TỔNG QUỸ DỰ PHÒNG RỦI RO (CONTINGENCY RESERVE = Σ EMV):</td>
      <td>+$3,260</td>
      <td>Approved Budget = $49,448 + $3,260 = $52,708</td>
    </tr>
  </tfoot>
</table>

<h2>4. Phân biệt Contingency Reserve (Quỹ Dự phòng Rủi ro) và Management Reserve (Quỹ Dự phòng Quản lý)</h2>
<p>
  Trong kỳ thi chứng chỉ PMP® cũng như khi vận hành thực tế theo chuẩn PMBOK® 8, bạn cần phân biệt rõ hai tầng quỹ dự phòng:
</p>
<ul>
  <li><strong>Contingency Reserve (Quỹ Dự phòng Rủi ro — Giải quyết "Known-Unknowns"):</strong> Dành cho các rủi ro <em>đã được nhận diện trong Risk Register</em> (như R1–R8 ở trên) và được tính định lượng bằng tổng <code>EMV</code>. Quỹ này nằm trong <strong>Cost Baseline / Approved Budget</strong> và Giám đốc Dự án (PM) có thẩm quyền chủ động giải ngân khi rủi ro xảy ra.</li>
  <li><strong>Management Reserve (Quỹ Dự phòng Quản lý — Giải quyết "Unknown-Unknowns"):</strong> Dành cho các biến cố bất khả kháng chưa từng được nhận diện trước (thiên tai, đứt gãy địa chính trị đột ngột). Quỹ này nằm ngoài Cost Baseline (cộng thêm vào để tạo thành tổng <em>Project Budget</em>) và muốn sử dụng bắt buộc phải có phê duyệt của <strong>Sponsor / Ban Giám đốc</strong>.</li>
</ul>

{CTA_BOX_HTML}

<h2>5. Bài viết Liên quan trong Hệ sinh thái Quản trị Dự án PMBOK® 8</h2>
<ul>
  <li>📘 <strong>Tổng quan PMBOK 8:</strong> <a href="{{{{URL_PM01}}}}">Quản trị Dự án theo chuẩn PMBOK 8: Tổng quan 6 Nguyên tắc, 7 Miền hiệu suất &amp; 5 Nhóm quy trình thực chiến</a>.</li>
  <li>🌳 <strong>Xây dựng WBS &amp; WBS Dictionary:</strong> <a href="{{{{URL_PM04}}}}">Cấu trúc Phân rã Công việc (WBS) &amp; Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8</a>.</li>
  <li>📊 <strong>Kiểm soát Ngân sách bằng 9 chỉ số EVM:</strong> <a href="{{{{URL_PM08}}}}">Quản lý Giá trị Thu được (Earned Value Management - EVM): Cách tính BAC, PV, EV, AC, SPI, CPI &amp; Dự báo EAC</a>.</li>
  <li>🤝 <strong>Quản trị Rủi ro Nhà cung cấp &amp; Mua hàng:</strong> Đọc thêm tại <a href="https://erx.vn/procurement-management.html">Procurement Management</a>.</li>
</ul>

<h2>6. Câu hỏi Thường gặp (FAQ) về Định lượng Rủi ro EMV &amp; Quỹ Dự phòng</h2>
<div class="erx-faq-box" style="background: #f8fafc; padding: 20px 24px; border-radius: 10px; border: 1px solid #e2e8f0;">
  <h3>Câu hỏi 1: Nếu dự án có Cơ hội Tích cực (Opportunities / Positive Risks) thì tính EMV như thế nào?</h3>
  <p>
    Trong PMBOK 8, các mối đe dọa (<em>Threats</em>) mang giá trị chi phí tăng thêm (<code>+EMV</code> vào quỹ dự phòng), còn các cơ hội tích cực (<em>Opportunities</em>, ví dụ chiết khấu mua hàng số lượng lớn giúp tiết kiệm $2,000 với xác suất 40%) sẽ mang giá trị giảm chi phí (<code>-$800</code>), giúp tối ưu hóa tổng quỹ dự phòng cần trích lập.
  </p>
  <h3>Câu hỏi 2: Khi một rủi ro đã qua giai đoạn phát sinh mà không xảy ra, xử lý EMV của nó ra sao?</h3>
  <p>
    Khi giai đoạn chứa rủi ro đó (ví dụ <code>R2 - Đấu thầu NCC</code>) đã hoàn tất và đóng lại an toàn, bạn cập nhật trạng thái rủi ro sang <em>Closed (P = 0%)</em> trên <a href="https://project-management.erx.vn/" target="_blank" rel="noopener">project-management.erx.vn</a>. Khoản dự phòng <code>$750</code> của rủi ro R2 sẽ được giải phóng khỏi mức phơi nhiễm rủi ro hiện hành.
  </p>
  <h3>Câu hỏi 3: Làm sao để xuất toàn bộ bảng Risk EMV và 13 hồ sơ PMBOK 8 ra file báo cáo?</h3>
  <p style="margin-bottom: 0;">
    Trên <code>project-management.erx.vn</code>, bạn chỉ cần vào menu <strong>Export → Export Excel (.xlsx)</strong> hoặc <strong>Print / PDF</strong> trong tab <em>Project Charter &amp; PMBOK Docs</em> để xuất trọn bộ 13 hồ sơ quản trị kèm bảng tính EMV và biểu đồ Gantt chuẩn quốc tế.
  </p>
</div>
"""

articles = [
    {
        "code": "PM-01",
        "nid": "7124047589",
        "url": "https://erx.vn/quan-tri-du-an-theo-chuan-pmbok-8-tong-quan-nguyen-tac-va-quy-trinh-7124047589.html",
        "title": "Quản trị Dự án theo chuẩn PMBOK 8: Tổng quan 6 Nguyên tắc, 7 Miền hiệu suất & 5 Nhóm quy trình thực chiến",
        "alias": "quan-tri-du-an-theo-chuan-pmbok-8-tong-quan-nguyen-tac-va-quy-trinh",
        "meta_desc": "Giải mã chuẩn Quản trị Dự án PMBOK 8 (6 Nguyên tắc, 7 Miền hiệu suất, 5 Nhóm quy trình) và cách vận hành 13 hồ sơ PMBOK trên project-management.erx.vn.",
        "meta_key": "pmbok 8, quản trị dự án pmbok 8, quy trình quản lý dự án, 7 miền hiệu suất pmbok 8, project management erx, gantt planner",
        "introtext": "<p>Tiêu chuẩn PMBOK® Guide – 8th Edition (PMBOK 8) đánh dấu bước chuyển mình lớn nhất của PMI khi hợp nhất 6 Nguyên tắc tư duy, 7 Miền hiệu suất với 5 Nhóm quy trình thực thi và AI. Cùng khám phá kiến trúc PMBOK 8 và cách áp dụng thực chiến 13 hồ sơ quản trị dự án trên nền tảng ERX AI Project Gantt Planner.</p>",
        "hero_token": "IMG_pm01_1",
        "images": [
            {"token": "IMG_pm01_1", "file": "pm01_1_pmbok8_architecture.jpg"},
            {"token": "IMG_pm01_2", "file": "pm01_2_13_pmbok_artifacts.jpg"},
            {"token": "IMG_pm01_3", "file": "pm01_3_process_groups_workflow.jpg"}
        ],
        "fulltext": pm01_html.strip()
    },
    {
        "code": "PM-04",
        "nid": "7124054453",
        "url": "https://erx.vn/cau-truc-phan-ra-cong-viec-wbs-va-tu-dien-wbs-trong-quan-ly-du-an-7124054453.html",
        "title": "Cấu trúc Phân rã Công việc (WBS) & Từ điển WBS: Cách chia nhỏ Dự án chuẩn PMBOK 8",
        "alias": "cau-truc-phan-ra-cong-viec-wbs-va-tu-dien-wbs-trong-quan-ly-du-an",
        "meta_desc": "Hướng dẫn thiết kế Cấu trúc Phân rã Công việc (WBS) 4 cấp độ theo Quy tắc 100%, lập Từ điển WBS chuẩn PMBOK 8 và vẽ Gantt tự động trên project-management.erx.vn.",
        "meta_key": "wbs là gì, work breakdown structure, cấu trúc phân rã công việc, từ điển wbs, wbs dictionary, quy tắc 100% wbs, pmbok 8",
        "introtext": "<p>Cấu trúc Phân rã Công việc (Work Breakdown Structure - WBS) và Từ điển WBS là nền tảng chống trượt phạm vi (Scope Creep) trong chuẩn PMBOK® 8. Bài viết hướng dẫn chi tiết Quy tắc 100%, Quy tắc 8/80 giờ, cách phân biệt Summary Task, Work Package, Milestone và thực hành trực tiếp trên ERX AI Project Gantt Planner.</p>",
        "hero_token": "IMG_pm04_1",
        "images": [
            {"token": "IMG_pm04_1", "file": "pm04_1_wbs_hierarchy_100_rule.jpg"},
            {"token": "IMG_pm04_2", "file": "pm04_2_wbs_gantt_interface.jpg"},
            {"token": "IMG_pm04_3", "file": "pm04_3_wbs_dictionary_card.jpg"}
        ],
        "fulltext": pm04_html.strip()
    },
    {
        "code": "PM-08",
        "nid": "7124068075",
        "url": "https://erx.vn/earned-value-management-evm-cach-tinh-pv-ev-ac-spi-cpi-eac-trong-du-an-7124068075.html",
        "title": "Quản lý Giá trị Thu được (Earned Value Management - EVM): Cách tính BAC, PV, EV, AC, SPI, CPI & Dự báo EAC",
        "alias": "earned-value-management-evm-cach-tinh-pv-ev-ac-spi-cpi-eac-trong-du-an",
        "meta_desc": "Cẩm nang toàn diện về Earned Value Management (EVM) chuẩn PMBOK 8: Công thức tính 9 chỉ số BAC, PV, EV, AC, SV, CV, SPI, CPI, EAC và đồ thị S-Curve thực tế.",
        "meta_key": "earned value management, evm là gì, cách tính spi cpi, bac pv ev ac eac, quản lý chi phí dự án, pmbok 8, erx gantt planner",
        "introtext": "<p>Làm sao biết dự án đang thực sự đúng tiến độ hay đang ngầm đội vốn? Quản lý Giá trị Thu được (Earned Value Management - EVM) trong chuẩn PMBOK® 8 giúp đo lường chính xác sức khỏe tài chính và tiến độ dự án qua 9 chỉ số cốt lõi (BAC, PV, EV, AC, SV, CV, SPI, CPI, EAC) trên hệ thống 11 Baseline của project-management.erx.vn.</p>",
        "hero_token": "IMG_pm08_1",
        "images": [
            {"token": "IMG_pm08_1", "file": "pm08_1_evm_s_curve_chart.jpg"},
            {"token": "IMG_pm08_2", "file": "pm08_2_spi_cpi_quadrant_matrix.jpg"},
            {"token": "IMG_pm08_3", "file": "pm08_3_9_evm_formulas_table.jpg"}
        ],
        "fulltext": pm08_html.strip()
    },
    {
        "code": "PM-09",
        "nid": "7124079199",
        "url": "https://erx.vn/dinh-luong-rui-ro-du-an-bang-emv-expected-monetary-value-va-contingency-reserve-7124079199.html",
        "title": "Định lượng Rủi ro Dự án bằng EMV (Expected Monetary Value) & Cách tính Quỹ Dự phòng (Contingency Reserve)",
        "alias": "dinh-luong-rui-ro-du-an-bang-emv-expected-monetary-value-va-contingency-reserve",
        "meta_desc": "Hướng dẫn định lượng rủi ro dự án bằng công thức EMV = P% × Impact($), lập Ma trận P×I Heatmap và tự động đồng bộ Quỹ dự phòng vào Ngân sách chuẩn PMBOK 8.",
        "meta_key": "emv là gì, expected monetary value, định lượng rủi ro dự án, contingency reserve, quỹ dự phòng rủi ro, risk register pmbok 8",
        "introtext": "<p>Thay vì cộng cảm tính 10% chi phí dự phòng, chuẩn PMBOK® 8 yêu cầu định lượng rủi ro bằng Giá trị Tiền tệ Kỳ vọng (EMV = Xác suất P% × Tác động tài chính $). Khám phá quy trình 4 bước từ RBS, Ma trận nhiệt P×I đến cơ chế tự động đồng bộ Approved Budget = BAC + EMV trên project-management.erx.vn.</p>",
        "hero_token": "IMG_pm09_1",
        "images": [
            {"token": "IMG_pm09_1", "file": "pm09_1_emv_budget_sync_flow.jpg"},
            {"token": "IMG_pm09_2", "file": "pm09_2_pxi_risk_heatmap.jpg"},
            {"token": "IMG_pm09_3", "file": "pm09_3_p2p_risk_emv_table.jpg"}
        ],
        "fulltext": pm09_html.strip()
    }
]

# Pre-replace URL_PM01..09 tokens right here since we already know all 4 exact URLs!
url_map = {
    "{{URL_PM01}}": articles[0]["url"],
    "{{URL_PM04}}": articles[1]["url"],
    "{{URL_PM08}}": articles[2]["url"],
    "{{URL_PM09}}": articles[3]["url"],
}
for a in articles:
    for k, v in url_map.items():
        a["fulltext"] = a["fulltext"].replace(k, v)

out_json = os.path.join(ASSET_DIR, "pillar_articles_clean.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"Saved clean light-tone payload ({os.path.getsize(out_json)/1024:.1f} KB) to {out_json}")
