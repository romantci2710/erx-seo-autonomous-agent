# -*- coding: utf-8 -*-
"""
Generates 16 BRIGHT, MINIMALIST, HIGH-CONTRAST LIGHT-TONE diagrams (1200x675)
for the 8 Cluster Articles (PM-02, PM-03, PM-05, PM-06, PM-07, PM-10, PM-11, PM-12)
of the "Project Management" (PMBOK 8 & ERX Gantt Planner) hub.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"D:\GIT\SEO Tool\pm_assets"
os.makedirs(OUT_DIR, exist_ok=True)

FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_MONO = r"C:\Windows\Fonts\consolab.ttf"

def fnt(path, size):
    return ImageFont.truetype(path, size)

# Light-Tone Clean Editorial Palette
BG_MAIN = (248, 250, 252)       # #F8FAFC
BG_WHITE = (255, 255, 255)      # #FFFFFF
BORDER_LIGHT = (203, 213, 225)  # #CBD5E1
GRID_LINE = (236, 242, 249)

TEXT_DARK = (15, 23, 42)        # #0F172A
TEXT_BODY = (51, 65, 85)        # #334155
TEXT_MUTED = (100, 116, 139)    # #64748B

EMERALD = (16, 185, 129)        # #10B981
EMERALD_DARK = (5, 150, 105)    # #059669
EMERALD_BG = (236, 253, 245)    # #ECFDF5

BLUE = (37, 99, 235)            # #2563EB
BLUE_BG = (239, 246, 255)       # #EFF6FF

TEAL = (13, 148, 136)           # #0D9488
TEAL_BG = (240, 253, 250)       # #F0FDFA

AMBER = (217, 119, 6)           # #D97706
AMBER_BG = (255, 251, 235)      # #FFFBEB

ROSE = (225, 29, 72)            # #E11D48
ROSE_BG = (255, 241, 242)       # #FFF1F2

PURPLE = (124, 58, 237)         # #7C3AED
PURPLE_BG = (245, 243, 255)     # #F5F3FF

def create_light_canvas(title, subtitle, tag="ERX.VN • PMBOK® 8TH EDITION"):
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), BG_MAIN)
    draw = ImageDraw.Draw(img)

    for x in range(0, W, 48):
        draw.line([(x, 0), (x, H)], fill=GRID_LINE, width=1)
    for y in range(0, H, 48):
        draw.line([(0, y), (W, y)], fill=GRID_LINE, width=1)

    draw.rectangle([0, 0, W - 1, H - 1], outline=BORDER_LIGHT, width=2)
    draw.rectangle([0, 0, W, 10], fill=EMERALD)

    draw.rounded_rectangle([48, 28, 390, 62], radius=17, fill=EMERALD_BG, outline=EMERALD, width=2)
    draw.text((66, 35), tag, font=fnt(FONT_BOLD, 15), fill=EMERALD_DARK)

    draw.rounded_rectangle([880, 28, 1152, 62], radius=17, fill=BLUE_BG, outline=BLUE, width=2)
    draw.text((902, 35), "project-management.erx.vn", font=fnt(FONT_BOLD, 15), fill=BLUE)

    draw.text((48, 76), title, font=fnt(FONT_BOLD, 33), fill=TEXT_DARK)
    draw.text((48, 122), subtitle, font=fnt(FONT_REG, 19), fill=TEXT_BODY)

    draw.rectangle([2, H - 44, W - 2, H - 2], fill=BG_WHITE)
    draw.line([(0, H - 44), (W, H - 44)], fill=BORDER_LIGHT, width=2)
    draw.text((48, H - 32), "ERX.VN — Cổng Kiến thức Quản trị Dự án Chuẩn PMBOK® 8 & Chuỗi Cung Ứng", font=fnt(FONT_BOLD, 14), fill=TEXT_MUTED)
    draw.text((870, H - 32), "WBS • CPM • EVM • Risk EMV • AI", font=fnt(FONT_BOLD, 14), fill=EMERALD_DARK)

    return img, draw

def draw_arrow(draw, x1, y1, x2, y2, color=EMERALD_DARK):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=4)
    if x2 > x1:
        draw.polygon([(x2 + 6, y2), (x2 - 8, y2 - 8), (x2 - 8, y2 + 8)], fill=color)
    elif y2 > y1:
        draw.polygon([(x2, y2 + 6), (x2 - 8, y2 - 8), (x2 + 8, y2 - 8)], fill=color)

def save_diagram(img, base_name):
    jpg_path = os.path.join(OUT_DIR, base_name + "_light.jpg")
    webp_path = os.path.join(OUT_DIR, base_name + "_light.webp")
    img.save(jpg_path, format="JPEG", quality=90, optimize=True)
    img.save(webp_path, format="WEBP", quality=86, method=6)
    print(f"Saved {base_name}_light: JPG={os.path.getsize(jpg_path)/1024:.1f}KB, WebP={os.path.getsize(webp_path)/1024:.1f}KB")

# ==============================================================================
# PM-02: PROJECT CHARTER & BUSINESS CASE
# ==============================================================================
def build_pm02():
    # 1. PM02-1: 6 Core Blocks of Project Charter
    img, draw = create_light_canvas(
        "ĐIỀU LỆ DỰ ÁN (PROJECT CHARTER) CHUẨN PMBOK® 8",
        "6 Thành phần Cốt lõi Khởi tạo & Trao quyền Chính thức cho Giám đốc Dự án"
    )
    cards = [
        ("01. BUSINESS CASE & ROI", "Căn cứ đầu tư & Lợi ích kỳ vọng", "Giảm 45% thời gian duyệt PR→PO", EMERALD_DARK, EMERALD_BG),
        ("02. TIÊU CHÍ THÀNH CÔNG", "Chỉ số đo lường nghiệm thu (KPIs)", "100% đơn hàng đối soát 3-Way Match", BLUE, BLUE_BG),
        ("03. PHẠM VI & RANH GIỚI", "In-Scope vs Out-of-Scope rõ ràng", "20 gói công việc WBS • 7 Phòng ban", PURPLE, PURPLE_BG),
        ("04. LỘ TRÌNH CỘT MỐC", "Milestone Summary (0 ngày)", "M1 Charter • M2 Thiết kế • M3 Go-Live", AMBER, AMBER_BG),
        ("05. NGÂN SÁCH PHÊ DUYỆT", "Approved Budget = BAC + EMV", "$49,448 (BAC) + $3,260 (EMV) = $52,708", TEAL, TEAL_BG),
        ("06. TRAO QUYỀN PM & SPONSOR", "Quyền điều phối nguồn lực & ngân sách", "Sponsor ký duyệt • PM chịu trách nhiệm A", ROSE, ROSE_BG),
    ]
    for i, (t, sub, ex, col, bg) in enumerate(cards):
        col_idx = i % 3
        row_idx = i // 3
        x = 48 + col_idx * 376
        y = 172 + row_idx * 214
        w, h = 352, 192
        draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 54], radius=12, fill=bg)
        draw.text((x + 20, y + 14), t, font=fnt(FONT_BOLD, 18), fill=col)
        draw.text((x + 20, y + 72), sub, font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
        draw.rounded_rectangle([x + 18, y + 118, x + w - 18, y + 168], radius=8, fill=BG_MAIN, outline=BORDER_LIGHT, width=1)
        draw.text((x + 28, y + 131), ex, font=fnt(FONT_BOLD, 15), fill=col)
    save_diagram(img, "pm02_1_project_charter_structure")

    # 2. PM02-2: Business Case -> Project Charter -> Benefits Management Plan
    img, draw = create_light_canvas(
        "CHU TRÌNH QUẢN TRỊ GIÁ TRỊ ĐẦU TƯ DỰ ÁN (PMBOK® 8)",
        "Liên kết Xuyên suốt: Business Case → Project Charter → Benefits Management Plan"
    )
    steps = [
        ("1. BUSINESS CASE", "Tại sao cần đầu tư dự án?", BLUE, BLUE_BG, [
            "• Nỗi đau: Duyệt PR/PO thủ công mất 9 ngày",
            "• Rủi ro: Sai lệch hóa đơn & vượt ngân sách",
            "• Chi phí đầu tư dự kiến: $52,708",
            "• Thời gian hoàn vốn (Payback): 4.5 tháng"
        ]),
        ("2. PROJECT CHARTER", "Ai được trao quyền thực thi?", EMERALD_DARK, EMERALD_BG, [
            "• Mã dự án: P2P-FOUNDATION-2026",
            "• Thời lượng chuẩn: 28 ngày làm việc",
            "• Ngân sách cơ sở (BAC): $49,448",
            "• Quỹ dự phòng rủi ro (EMV): +$3,260"
        ]),
        ("3. BENEFITS PLAN", "Đo lường lợi ích sau Go-Live", AMBER, AMBER_BG, [
            "• Rút ngắn Lead-time PR→PO: -45%",
            "• Tự động hóa đối soát 3-Way Match: 100%",
            "• Minh bạch điểm nhà cung cấp (Scorecard)",
            "• Bàn giao vận hành chuẩn SLA cho bộ phận"
        ]),
    ]
    for i, (t, sub, col, bg, pts) in enumerate(steps):
        x = 48 + i * 384
        y = 175
        w, h = 336, 415
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 96], radius=14, fill=bg)
        draw.text((x + 22, y + 20), t, font=fnt(FONT_BOLD, 22), fill=col)
        draw.text((x + 22, y + 54), sub, font=fnt(FONT_BOLD, 16), fill=TEXT_DARK)
        for idx, pt in enumerate(pts):
            py = y + 118 + idx * 68
            draw.rounded_rectangle([x + 16, py, x + w - 16, py + 52], radius=8, fill=BG_MAIN, outline=BORDER_LIGHT, width=1)
            draw.text((x + 26, py + 14), pt, font=fnt(FONT_BOLD, 14), fill=TEXT_DARK)
        if i < 2:
            draw_arrow(draw, x + w + 8, y + 205, x + 384 - 10, y + 205, col)
    save_diagram(img, "pm02_2_business_case_vs_benefits")

# ==============================================================================
# PM-03: RACI MATRIX & STAKEHOLDER REGISTER
# ==============================================================================
def build_pm03():
    # 1. PM03-1: RACI 4 Roles & Golden Rules
    img, draw = create_light_canvas(
        "MA TRẬN PHÂN QUYỀN RACI CHUẨN PMBOK® 8",
        "4 Vai trò Trách nhiệm & Quy tắc Chống Đùn đẩy trong Dự án Đa Phòng ban"
    )
    roles = [
        ("R", "RESPONSIBLE", "Người Trực tiếp Thực thi", BLUE, BLUE_BG, "Làm trực tiếp gói công việc WBS.\nMỗi Task phải có ít nhất 1 chữ R."),
        ("A", "ACCOUNTABLE", "Người Chịu Trách nhiệm Cuối", ROSE, ROSE_BG, "Có quyền phê duyệt nghiệm thu.\nBẮT BUỘC DUY NHẤT 1 CHỮ A / TASK!"),
        ("C", "CONSULTED", "Chuyên gia Tham vấn (2 chiều)", AMBER, AMBER_BG, "Cung cấp ý kiến chuyên môn trước\nkhi ra quyết định (Tài chính, Pháp chế)."),
        ("I", "INFORMED", "Người Nhận Thông báo (1 chiều)", EMERALD_DARK, EMERALD_BG, "Cập nhật kết quả sau khi hoàn tất\nqua báo cáo Executive Diff Telegram."),
    ]
    for i, (let, name, vn, col, bg, desc) in enumerate(roles):
        x = 48 + i * 282
        y = 172
        w, h = 260, 315
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 128], radius=14, fill=bg)
        draw.rounded_rectangle([x + 22, y + 22, x + 94, y + 94], radius=14, fill=col)
        draw.text((x + 42, y + 28), let, font=fnt(FONT_BOLD, 44), fill=BG_WHITE)
        draw.text((x + 110, y + 36), name, font=fnt(FONT_BOLD, 17), fill=col)
        draw.text((x + 22, y + 146), vn, font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
        for idx, line in enumerate(desc.split("\n")):
            draw.text((x + 22, y + 188 + idx * 28), line, font=fnt(FONT_REG, 15), fill=TEXT_BODY)

    draw.rounded_rectangle([48, 512, 1152, 594], radius=12, fill=EMERALD_BG, outline=EMERALD, width=2)
    draw.text((74, 526), "QUY TẮC KIỂM TOÁN RACI TRÊN PROJECT-MANAGEMENT.ERX.VN:", font=fnt(FONT_BOLD, 17), fill=EMERALD_DARK)
    draw.text((74, 554), "Hệ thống tự động cảnh báo nếu 1 Task có 0 chữ A (vô chủ), >= 2 chữ A (chồng chéo quyền phán quyết) hoặc thiếu chữ R.", font=fnt(FONT_BOLD, 16), fill=TEXT_DARK)
    save_diagram(img, "pm03_1_raci_matrix_rules")

    # 2. PM03-2: Stakeholder Power/Interest 2x2 Grid
    img, draw = create_light_canvas(
        "MA TRẬN PHÂN TÍCH BÊN LIÊN QUAN (POWER / INTEREST GRID)",
        "Chiến lược Tương tác 4 Nhóm Stakeholder trong Dự án Chuỗi Cung Ứng (P2P)"
    )
    quads = [
        (110, 175, "QUYỀN LỰC CAO • QUAN TÂM THẤP", "GIỮ HÀI LÒNG (KEEP SATISFIED)", AMBER, AMBER_BG,
         "• Đối tượng: Giám đốc Tài chính (CFO), Ban Pháp chế",
         "• Chiến lược: Báo cáo định kỳ ngân sách BAC/EAC, không làm phiền chi tiết nhỏ."),
        (640, 175, "QUYỀN LỰC CAO • QUAN TÂM CAO", "QUẢN LÝ SÁT SAO (MANAGE CLOSELY)", ROSE, ROSE_BG,
         "• Đối tượng: Giám đốc Dự án (Sponsor), Giám đốc Mua hàng (CPO)",
         "• Chiến lược: Họp cổng phê duyệt (Stage Gate), nhận cảnh báo Telegram tức thời."),
        (110, 395, "QUYỀN LỰC THẤP • QUAN TÂM THẤP", "THEO DÕI ĐỊNH KỲ (MONITOR)", TEXT_MUTED, BG_WHITE,
         "• Đối tượng: Các bộ phận gián tiếp ít phát sinh PR",
         "• Chiến lược: Gửi bản tin tổng hợp tiến độ chung qua cổng thông tin nội bộ."),
        (640, 395, "QUYỀN LỰC THẤP • QUAN TÂM CAO", "THÔNG TIN ĐẦY ĐỦ (KEEP INFORMED)", EMERALD_DARK, EMERALD_BG,
         "• Đối tượng: Chuyên viên Mua hàng, Thủ kho (GRN), Kế toán AP, Nhà cung cấp",
         "• Chiến lược: Đào tạo SOP thực chiến, lấy phản hồi UAT & hỗ trợ sát khi Go-Live."),
    ]
    for x, y, sub, title, col, bg, l1, l2 in quads:
        w, h = 510, 198
        draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 72], radius=12, fill=bg)
        draw.text((x + 22, y + 12), sub, font=fnt(FONT_BOLD, 14), fill=col)
        draw.text((x + 22, y + 36), title, font=fnt(FONT_BOLD, 20), fill=TEXT_DARK)
        draw.text((x + 22, y + 92), l1, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)
        draw.text((x + 22, y + 132), l2, font=fnt(FONT_REG, 15), fill=TEXT_BODY)
    save_diagram(img, "pm03_2_stakeholder_power_interest_grid")

# ==============================================================================
# PM-05: 4 PDM DEPENDENCIES (FS, SS, FF, SF) & FAST-TRACKING
# ==============================================================================
def build_pm05():
    # 1. PM05-1: 4 PDM Dependencies
    img, draw = create_light_canvas(
        "4 MỐI QUAN HỆ PHỤ THUỘC CÔNG VIỆC (PDM: FS • SS • FF • SF)",
        "Chuẩn Lập Lịch Microsoft Project 2016 Parity trên project-management.erx.vn"
    )
    items = [
        ("1. FINISH-TO-START (FS) — Phổ biến nhất (80%)", "Task A xong hoàn toàn thì Task B mới được bắt đầu", EMERALD_DARK, EMERALD_BG, "Ví dụ: Ký duyệt PO xong → Gửi PO cho Nhà cung cấp"),
        ("2. START-TO-START (SS + Lag) — Gối đầu rút ngắn tiến độ", "Task A bắt đầu thì Task B cùng bắt đầu (hoặc trễ +1d)", BLUE, BLUE_BG, "Ví dụ: Lập PR mua hàng → Kiểm tra ngân sách song song (SS+1d)"),
        ("3. FINISH-TO-FINISH (FF) — Đồng bộ thời điểm hoàn tất", "Task A hoàn thành thì Task B mới được chốt hoàn thành", PURPLE, PURPLE_BG, "Ví dụ: Nhập kho GRN hoàn tất ↔ Kiểm định chất lượng QA hoàn tất"),
        ("4. START-TO-FINISH (SF) — Chuyển giao hệ thống không gián đoạn", "Hệ thống mới (A) vận hành thì hệ thống cũ (B) mới ngừng", AMBER, AMBER_BG, "Ví dụ: Cổng ERP P2P mới Go-Live → Ngừng quy trình duyệt giấy cũ"),
    ]
    for i, (t, desc, col, bg, ex) in enumerate(items):
        col_idx = i % 2
        row_idx = i // 2
        x = 48 + col_idx * 564
        y = 172 + row_idx * 214
        w, h = 540, 194
        draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 54], radius=12, fill=bg)
        draw.text((x + 20, y + 14), t, font=fnt(FONT_BOLD, 17), fill=col)
        draw.text((x + 20, y + 72), desc, font=fnt(FONT_BOLD, 16), fill=TEXT_DARK)
        draw.rounded_rectangle([x + 18, y + 118, x + w - 18, y + 170], radius=8, fill=BG_MAIN, outline=BORDER_LIGHT, width=1)
        draw.text((x + 28, y + 132), ex, font=fnt(FONT_BOLD, 15), fill=col)
    save_diagram(img, "pm05_1_pdm_4_dependencies")

    # 2. PM05-2: Fast-Tracking vs Crashing
    img, draw = create_light_canvas(
        "2 KỸ THUẬT NÉN TIẾN ĐỘ ĐƯỜNG GĂNG (SCHEDULE COMPRESSION)",
        "So sánh Fast-Tracking (Làm gối đầu SS/FF) & Crashing (Tăng nguồn lực)"
    )
    boxes = [
        (48, 175, "KỸ THUẬT 1: FAST-TRACKING (LÀM SONG SONG)", BLUE, BLUE_BG, [
            "• Bản chất: Chuyển quan hệ tuần tự FS sang gối đầu SS+Lag hoặc FF",
            "• Ví dụ P2P: Kiểm tra ngân sách chạy gối đầu SS+1d với lập PR",
            "• Hiệu quả: Rút ngắn tổng tiến độ từ 34 ngày xuống 28 ngày (-18%)",
            "• Ưu điểm: KHÔNG làm tăng ngân sách cơ sở (BAC giữ nguyên $49,448)",
            "• Rủi ro cần kiểm soát: Dễ phải làm lại (Rework) nếu bước trước thay đổi"
        ]),
        (616, 175, "KỸ THUẬT 2: CRASHING (TĂNG CƯỜNG NGUỒN LỰC)", AMBER, AMBER_BG, [
            "• Bản chất: Bổ sung thêm nhân sự hoặc tăng ca (Overtime) vào Đường găng",
            "• Ví dụ P2P: Tăng từ 100% lên 200% kỹ sư CNTT cho gói tích hợp ERP",
            "• Hiệu quả: Rút ngắn thời lượng Task găng từ 6 ngày xuống 3 ngày",
            "• Đánh đổi: LÀM TĂNG CHI PHÍ trực tiếp (Direct Cost & Overtime Rate)",
            "• Nguyên tắc vàng: Chỉ Crash các công việc nằm trên Đường găng (Slack = 0)"
        ]),
    ]
    for x, y, title, col, bg, pts in boxes:
        w, h = 536, 415
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 66], radius=14, fill=bg)
        draw.text((x + 22, y + 20), title, font=fnt(FONT_BOLD, 18), fill=col)
        for idx, pt in enumerate(pts):
            py = y + 86 + idx * 62
            draw.rounded_rectangle([x + 18, py, x + w - 18, py + 48], radius=8, fill=BG_MAIN, outline=BORDER_LIGHT, width=1)
            draw.text((x + 28, py + 12), pt, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)
    save_diagram(img, "pm05_2_fast_tracking_vs_crashing")

# ==============================================================================
# PM-06: CRITICAL PATH METHOD (CPM) & SLACK
# ==============================================================================
def build_pm06():
    # 1. PM06-1: CPM Forward Pass & Backward Pass
    img, draw = create_light_canvas(
        "PHƯƠNG PHÁP ĐƯỜNG GĂNG (CRITICAL PATH METHOD - CPM)",
        "Cơ chế Tính Lượt đi (Forward Pass ES/EF) & Lượt về (Backward Pass LS/LF)"
    )
    cards = [
        ("1. LƯỢT ĐI (FORWARD PASS)", "Tính từ Trái sang Phải → Tìm Ngày Sớm nhất", BLUE, BLUE_BG, [
            "ES (Early Start) = Max(EF của các Task tiền nhiệm)",
            "EF (Early Finish) = ES + Duration (Thời lượng)",
            "Mục tiêu: Xác định tổng thời gian tối thiểu của dự án (28 ngày)"
        ]),
        ("2. LƯỢT VỀ (BACKWARD PASS)", "Tính từ Phải sang Trái ← Tìm Ngày Muộn nhất", PURPLE, PURPLE_BG, [
            "LF (Late Finish) = Min(LS của các Task kế nhiệm)",
            "LS (Late Start) = LF - Duration (Thời lượng)",
            "Mục tiêu: Xác định giới hạn trễ tối đa mà không vỡ hạn chót"
        ]),
    ]
    for i, (t, sub, col, bg, pts) in enumerate(cards):
        x = 48 + i * 564
        y = 172
        w, h = 540, 290
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 78], radius=14, fill=bg)
        draw.text((x + 22, y + 14), t, font=fnt(FONT_BOLD, 20), fill=col)
        draw.text((x + 22, y + 44), sub, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)
        for idx, pt in enumerate(pts):
            py = y + 96 + idx * 58
            draw.rounded_rectangle([x + 18, py, x + w - 18, py + 46], radius=8, fill=BG_MAIN, outline=BORDER_LIGHT, width=1)
            draw.text((x + 28, py + 11), pt, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)

    draw.rounded_rectangle([48, 485, 1152, 595], radius=14, fill=ROSE_BG, outline=ROSE, width=3)
    draw.text((74, 502), "ĐỊNH NGHĨA ĐƯỜNG GĂNG (CRITICAL PATH) TRÊN PROJECT-MANAGEMENT.ERX.VN:", font=fnt(FONT_BOLD, 18), fill=ROSE)
    draw.text((74, 536), "Chuỗi công việc dài nhất quyết định ngày kết thúc dự án, nơi Total Slack = LS - ES = LF - EF = 0 ngày.", font=fnt(FONT_BOLD, 18), fill=TEXT_DARK)
    draw.text((74, 564), "Bất kỳ Task nào trên Đường găng (tô đỏ trên Gantt) bị trễ 1 ngày → Toàn bộ dự án lập tức bị trễ 1 ngày!", font=fnt(FONT_REG, 16), fill=TEXT_BODY)
    save_diagram(img, "pm06_1_cpm_forward_backward_pass")

    # 2. PM06-2: Free Slack vs Total Slack
    img, draw = create_light_canvas(
        "PHÂN BIỆT FREE SLACK (ĐỘ DỰ TRỮ TỰ DO) & TOTAL SLACK",
        "Chỉ số Sống còn để Điều phối Nhân sự mà Không làm Vỡ Tiến độ Dự án"
    )
    slacks = [
        ("FREE SLACK (ĐỘ DỰ TRỮ TỰ DO)", "Trễ bao lâu mà KHÔNG ảnh hưởng Task kế tiếp ngay sau nó?", EMERALD_DARK, EMERALD_BG,
         "Free Slack = ES(Task kế tiếp) - EF(Task hiện tại)",
         [
             "• Ý nghĩa điều hành: Khoảng đệm an toàn nội bộ giữa 2 nhóm",
             "• Ứng dụng: Dùng để dịch chuyển lịch làm việc của nhân sự bị quá tải",
             "  (Resource Leveling) mà không làm phiền bộ phận nhận bàn giao kế tiếp."
         ]),
        ("TOTAL SLACK (ĐỘ DỰ TRỮ TOÀN PHẦN)", "Trễ bao lâu mà KHÔNG làm trễ Ngày Kết thúc Toàn Dự án?", AMBER, AMBER_BG,
         "Total Slack = LS - ES = LF - EF",
         [
             "• Ý nghĩa điều hành: Khoảng đệm tối đa của toàn nhánh công việc",
             "• Khi Total Slack = 0: Công việc nằm trên Đường găng (Critical Task)",
             "• Khi Total Slack < 0 (Negative Float): Dự án đã chính thức vỡ hạn chót!"
         ]),
    ]
    for i, (t, sub, col, bg, formula, pts) in enumerate(slacks):
        x = 48 + i * 564
        y = 172
        w, h = 540, 420
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 84], radius=14, fill=bg)
        draw.text((x + 22, y + 16), t, font=fnt(FONT_BOLD, 20), fill=col)
        draw.text((x + 22, y + 48), sub, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)
        draw.rounded_rectangle([x + 20, y + 104, x + w - 20, y + 162], radius=10, fill=bg, outline=col, width=2)
        draw.text((x + 34, y + 120), formula, font=fnt(FONT_BOLD, 17), fill=col)
        for idx, pt in enumerate(pts):
            draw.text((x + 24, y + 188 + idx * 44), pt, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)
    save_diagram(img, "pm06_2_free_slack_vs_total_slack")

# ==============================================================================
# PM-07: EXCEL VS MS PROJECT VS ERX AI GANTT PLANNER
# ==============================================================================
def build_pm07():
    # 1. PM07-1: 6 Fatal Flaws of Excel Gantt vs ERX AI Gantt Planner
    img, draw = create_light_canvas(
        "TẠI SAO QUẢN LÝ DỰ ÁN BẰNG EXCEL DỄ VỠ TIẾN ĐỘ & ĐỘI VỐN?",
        "So sánh Trực diện: Bảng tính Excel Thủ công vs Động cơ ERX AI Gantt Planner"
    )
    cols = [
        (48, "QUẢN LÝ DỰ ÁN BẰNG EXCEL THỦ CÔNG", "6 Điểm gãy khiến PM mất kiểm soát", ROSE, ROSE_BG, [
            "✗ Tô màu ô thủ công, không có động cơ tính lịch tự động",
            "✗ Không tính được 4 quan hệ FS/SS/FF/SF kèm Lag/Lead",
            "✗ Trễ 1 việc không tự động đẩy lùi các việc phụ thuộc phía sau",
            "✗ Không biết việc nào nằm trên Đường găng (Critical Path)",
            "✗ Không có Baseline chuẩn để đo lường 9 chỉ số EVM (SPI/CPI)",
            "✗ Gửi file qua lại tạo ra hàng chục bản nháp lệch số liệu"
        ]),
        (616, "NỀN TẢNG PROJECT-MANAGEMENT.ERX.VN", "Chuẩn Microsoft Project 2016 Parity + AI", EMERALD_DARK, EMERALD_BG, [
            "✓ Động cơ CPM tự động tính lại toàn bộ lịch trình trong 10ms",
            "✓ Hỗ trợ đầy đủ FS, SS, FF, SF, Lag/Lead & 8 loại Constraints",
            "✓ Tự động tô đỏ Đường găng (Slack = 0) & tính Free/Total Slack",
            "✓ Cân bằng nguồn lực tự động (Resource Leveling & 9 Contours)",
            "✓ Lưu 11 Baselines, tự động tính 9 chỉ số EVM & Quỹ rủi ro EMV",
            "✓ Cloud Check-out/Check-in & bắn báo cáo Executive Diff Telegram"
        ]),
    ]
    for x, title, sub, col, bg, pts in cols:
        w, h = 536, 420
        y = 172
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 76], radius=14, fill=bg)
        draw.text((x + 22, y + 14), title, font=fnt(FONT_BOLD, 19), fill=col)
        draw.text((x + 22, y + 44), sub, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)
        for idx, pt in enumerate(pts):
            py = y + 92 + idx * 52
            draw.rounded_rectangle([x + 18, py, x + w - 18, py + 42], radius=8, fill=BG_MAIN, outline=BORDER_LIGHT, width=1)
            draw.text((x + 28, py + 9), pt, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)
    save_diagram(img, "pm07_1_excel_vs_ai_gantt_comparison")

    # 2. PM07-2: 4 Pillars of MSP 2016 Parity + Cloud AI
    img, draw = create_light_canvas(
        "KIẾN TRÚC CHUẨN MICROSOFT PROJECT 2016 PARITY TRÊN WEB",
        "Kết hợp Sức mạnh Tính toán của MS Project với Cộng tác Đám mây & AI"
    )
    pillars = [
        ("1. ĐỘNG CƠ LẬP LỊCH", "WBS đa cấp • PDM FS/SS/FF/SF\nĐường găng CPM • 8 Constraints\nLịch làm việc & Ngày nghỉ lễ", BLUE, BLUE_BG),
        ("2. QUẢN TRỊ NGUỒN LỰC", "Work = Duration × Units\nFixed Units / Duration / Work\n9 Work Contours & Leveling", PURPLE, PURPLE_BG),
        ("3. KIỂM SOÁT TÀI CHÍNH", "11 Khe lưu trữ Baseline\n9 Chỉ số EVM (SPI, CPI, EAC)\nĐồng bộ BAC + EMV = Budget", EMERALD_DARK, EMERALD_BG),
        ("4. 13 HỒ SƠ PMBOK 8 & AI", "Charter • RACI • Risk EMV\nCloud Check-out / Check-in\nAI Co-Pilot & MCP Telegram", AMBER, AMBER_BG),
    ]
    for i, (t, desc, col, bg) in enumerate(pillars):
        x = 48 + i * 282
        y = 175
        w, h = 260, 410
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 84], radius=14, fill=bg)
        draw.text((x + 18, y + 28), t, font=fnt(FONT_BOLD, 17), fill=col)
        for idx, line in enumerate(desc.split("\n")):
            py = y + 115 + idx * 88
            draw.rounded_rectangle([x + 16, py, x + w - 16, py + 66], radius=10, fill=BG_MAIN, outline=BORDER_LIGHT, width=1)
            draw.text((x + 24, py + 20), line, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)
    save_diagram(img, "pm07_2_msp_parity_architecture")

# ==============================================================================
# PM-10: RESOURCE LEVELING & WORK = DURATION x UNITS
# ==============================================================================
def build_pm10():
    # 1. PM10-1: Work = Duration x Units & 3 Task Types
    img, draw = create_light_canvas(
        "PHƯƠNG TRÌNH NGUỒN LỰC: WORK = DURATION × UNITS",
        "Giải mã 3 Kiểu Công việc (Fixed Units • Fixed Duration • Fixed Work)"
    )
    draw.rounded_rectangle([48, 168, 1152, 244], radius=14, fill=BLUE_BG, outline=BLUE, width=2)
    draw.text((74, 182), "PHƯƠNG TRÌNH CỐT LÕI TRONG MICROSOFT PROJECT & PROJECT-MANAGEMENT.ERX.VN:", font=fnt(FONT_BOLD, 16), fill=BLUE)
    draw.text((74, 208), "Tổng Giờ công (Work - Giờ)  =  Thời lượng (Duration - Ngày × 8h)  ×  Tỷ lệ Phân bổ Nguồn lực (Units %)", font=fnt(FONT_BOLD, 20), fill=TEXT_DARK)

    types = [
        ("1. FIXED UNITS (Mặc định)", "Cố định Tỷ lệ Nhân sự (%)", EMERALD_DARK, EMERALD_BG, [
            "• Giữ nguyên: Units (ví dụ 100% = 1 người)",
            "• Khi tăng Work → Duration tự động tăng",
            "• Phù hợp: 80% các công việc văn phòng & kỹ thuật"
        ]),
        ("2. FIXED DURATION", "Cố định Thời gian Thực hiện", BLUE, BLUE_BG, [
            "• Giữ nguyên: Duration (ví dụ 5 ngày cố định)",
            "• Khi tăng nhân sự (Units) → Work tự tăng",
            "• Phù hợp: Hội thảo, chạy thử nghiệm UAT, đào tạo"
        ]),
        ("3. FIXED WORK", "Cố định Tổng Khối lượng Giờ công", AMBER, AMBER_BG, [
            "• Giữ nguyên: Tổng giờ công (ví dụ 80 giờ)",
            "• Thêm người (Units 200%) → Duration giảm còn 1 nửa",
            "• Phù hợp: Công việc định mức giờ công cố định"
        ]),
    ]
    for i, (t, sub, col, bg, pts) in enumerate(types):
        x = 48 + i * 376
        y = 266
        w, h = 352, 330
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 78], radius=14, fill=bg)
        draw.text((x + 20, y + 16), t, font=fnt(FONT_BOLD, 19), fill=col)
        draw.text((x + 20, y + 46), sub, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)
        for idx, pt in enumerate(pts):
            py = y + 98 + idx * 70
            draw.rounded_rectangle([x + 16, py, x + w - 16, py + 54], radius=8, fill=BG_MAIN, outline=BORDER_LIGHT, width=1)
            draw.text((x + 24, py + 15), pt, font=fnt(FONT_BOLD, 14), fill=TEXT_DARK)
    save_diagram(img, "pm10_1_work_duration_units_triangle")

    # 2. PM10-2: Resource Leveling Before vs After
    img, draw = create_light_canvas(
        "CÂN BẰNG NGUỒN LỰC TỰ ĐỘNG (RESOURCE LEVELING)",
        "Xử lý Quá tải Nhân sự (Over-allocation > 100%) bằng Độ dự trữ Free Slack"
    )
    panels = [
        (48, "TRƯỚC KHI CÂN BẰNG (OVER-ALLOCATION)", "Chuyên viên Mua hàng bị giao 2 việc trùng ngày → Quá tải 200%", ROSE, ROSE_BG, [
            ("Ngày 1 - Ngày 3", "Task A (Găng): Lập hồ sơ mời thầu RFQ (100%)", ROSE),
            ("Ngày 2 - Ngày 3", "Task B (Slack 3d): Cập nhật danh bạ NCC (100%)", ROSE),
            ("CẢNH BÁO ĐỎ:", "Tổng tải Ngày 2 & Ngày 3 = 200% (Vượt ngưỡng 100% Max Units!)", ROSE)
        ]),
        (616, "SAU KHI CHẠY RESOURCE LEVELING", "Hệ thống tự động dời Task B vào vùng Free Slack → Tải chuẩn 100%", EMERALD_DARK, EMERALD_BG, [
            ("Ngày 1 - Ngày 3", "Task A (Găng): Lập hồ sơ mời thầu RFQ (100% - Giữ nguyên)", EMERALD_DARK),
            ("Ngày 4 - Ngày 5", "Task B: Tự động dời sang Ngày 4-5 (Sử dụng 2 ngày Free Slack)", BLUE),
            ("KẾT QUẢ TỐI ƯU:", "Tải nhân sự mọi ngày = 100% • Ngày kết thúc dự án KHÔNG ĐỔI!", EMERALD_DARK)
        ]),
    ]
    for x, title, sub, col, bg, rows in panels:
        w, h = 536, 415
        y = 175
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 82], radius=14, fill=bg)
        draw.text((x + 22, y + 16), title, font=fnt(FONT_BOLD, 19), fill=col)
        draw.text((x + 22, y + 48), sub, font=fnt(FONT_BOLD, 14), fill=TEXT_DARK)
        for idx, (badge, text, rcol) in enumerate(rows):
            py = y + 106 + idx * 96
            draw.rounded_rectangle([x + 20, py, x + w - 20, py + 76], radius=10, fill=BG_MAIN, outline=rcol, width=2)
            draw.text((x + 34, py + 12), badge, font=fnt(FONT_BOLD, 16), fill=rcol)
            draw.text((x + 34, py + 42), text, font=fnt(FONT_BOLD, 14), fill=TEXT_DARK)
    save_diagram(img, "pm10_2_resource_leveling_before_after")

# ==============================================================================
# PM-11: P2P 20-STEP CASE STUDY & 3-WAY MATCHING
# ==============================================================================
def build_pm11():
    # 1. PM11-1: P2P-FOUNDATION-2026 5 Phases & 20 Steps
    img, draw = create_light_canvas(
        "CASE STUDY DỰ ÁN CHUỖI CUNG ỨNG: P2P-FOUNDATION-2026",
        "20 Bước WBS Chuẩn hóa Quy trình Mua hàng đến Thanh toán (28 Ngày • $52,708)"
    )
    phases = [
        ("PHASE 1", "Khởi tạo & Nhu cầu", "Ngày 1 - 5\n$8,400", EMERALD_DARK, EMERALD_BG, "1.1 Charter & RACI\n1.2 Chuẩn hóa PR\n1.3 Kiểm tra Ngân sách\n1.4 Cổng duyệt PR"),
        ("PHASE 2", "Đấu thầu & Chọn NCC", "Ngày 6 - 11\n$11,200", BLUE, BLUE_BG, "2.1 Phát hành RFQ\n2.2 Chấm điểm NCC\n2.3 Đàm phán SLA\n2.4 Phê duyệt NCC"),
        ("PHASE 3", "Hợp đồng & Đơn PO", "Ngày 12 - 16\n$9,848", PURPLE, PURPLE_BG, "3.1 Soạn thảo Hợp đồng\n3.2 Tạo PO tự động\n3.3 Xác nhận PO NCC\n3.4 Theo dõi ASN"),
        ("PHASE 4", "Nhận hàng & 3-Way", "Ngày 17 - 23\n$12,600", AMBER, AMBER_BG, "4.1 Nhập kho GRN\n4.2 Kiểm định QA/QC\n4.3 Đối soát 3-Way\n4.4 Giải ngân AP"),
        ("PHASE 5", "Scorecard & Đóng", "Ngày 24 - 28\n$7,400", TEAL, TEAL_BG, "5.1 Dashboard KPI\n5.2 Đánh giá NCC\n5.3 Đào tạo SOP\n5.4 Nghiệm thu Đóng"),
    ]
    for i, (code, name, meta, col, bg, tasks) in enumerate(phases):
        x = 48 + i * 224
        y = 172
        w, h = 208, 418
        draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 115], radius=12, fill=bg)
        draw.text((x + 16, y + 14), code, font=fnt(FONT_BOLD, 18), fill=col)
        draw.text((x + 16, y + 42), name, font=fnt(FONT_BOLD, 16), fill=TEXT_DARK)
        draw.text((x + 16, y + 70), meta, font=fnt(FONT_BOLD, 14), fill=col)
        for idx, line in enumerate(tasks.split("\n")):
            py = y + 135 + idx * 66
            draw.rounded_rectangle([x + 12, py, x + w - 12, py + 52], radius=8, fill=BG_MAIN, outline=BORDER_LIGHT, width=1)
            draw.text((x + 20, py + 15), line, font=fnt(FONT_BOLD, 14), fill=TEXT_DARK)
    save_diagram(img, "pm11_1_p2p_20_steps_roadmap")

    # 2. PM11-2: 3-Way Matching Control Gate
    img, draw = create_light_canvas(
        "CƠ CHẾ ĐỐI SOÁT BA BÊN (3-WAY MATCHING) TRONG DỰ ÁN P2P",
        "Chốt chặn Kiểm soát Chất lượng & Tài chính (PMBOK® 8 Quality & Finance Domain)"
    )
    docs = [
        ("1. ĐƠN MUA HÀNG (PO)", "Phòng Mua hàng (Procurement)", BLUE, BLUE_BG, "• Mã hàng & Quy cách kỹ thuật\n• Đơn giá đã đàm phán ($)\n• Số lượng đặt hàng chuẩn"),
        ("2. PHIẾU NHẬP KHO (GRN)", "Bộ phận Kho vận & QA/QC", EMERALD_DARK, EMERALD_BG, "• Số lượng thực nhận đạt chuẩn\n• Biên bản nghiệm thu chất lượng\n• Ngày giao hàng thực tế"),
        ("3. HÓA ĐƠN (INVOICE)", "Nhà cung cấp & Kế toán AP", PURPLE, PURPLE_BG, "• Số tiền đề nghị thanh toán\n• Thuế suất & Điều khoản công nợ\n• Khớp mã PO & mã phiếu GRN"),
    ]
    for i, (t, dept, col, bg, pts) in enumerate(docs):
        x = 48 + i * 376
        y = 172
        w, h = 352, 285
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 76], radius=14, fill=bg)
        draw.text((x + 20, y + 14), t, font=fnt(FONT_BOLD, 20), fill=col)
        draw.text((x + 20, y + 44), dept, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)
        for idx, line in enumerate(pts.split("\n")):
            draw.text((x + 22, y + 98 + idx * 52), line, font=fnt(FONT_BOLD, 16), fill=TEXT_DARK)

    draw.rounded_rectangle([48, 482, 1152, 595], radius=14, fill=EMERALD_BG, outline=EMERALD, width=3)
    draw.text((74, 500), "CỔNG KIỂM SOÁT TỰ ĐỘNG (STAGE GATE 4.3 — 100% 3-WAY MATCH):", font=fnt(FONT_BOLD, 18), fill=EMERALD_DARK)
    draw.text((74, 534), "Chỉ khi Số lượng & Đơn giá trên [PO] = [GRN] = [Invoice] (sai số cho phép 0%), hệ thống mới mở khóa", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
    draw.text((74, 562), "Bước 4.4 (Giải ngân Thanh toán AP) — loại bỏ 100% rủi ro thanh toán thừa hoặc nhận hàng lỗi!", font=fnt(FONT_REG, 16), fill=TEXT_BODY)
    save_diagram(img, "pm11_2_three_way_matching_control")

# ==============================================================================
# PM-12: AI AGENT, MCP PROTOCOL & EXECUTIVE DIFF TELEGRAM
# ==============================================================================
def build_pm12():
    # 1. PM12-1: AI Co-Pilot + MCP Server + Cloud PMO
    img, draw = create_light_canvas(
        "KIẾN TRÚC QUẢN TRỊ DỰ ÁN AI-NATIVE & GIAO THỨC MCP",
        "Tự động hóa Khởi tạo WBS, Đánh giá Rủi ro EMV & Điều hành Dự án Thời gian thực"
    )
    stages = [
        ("1. AI PROJECT CO-PILOT", "Khởi tạo Dự án từ Ngôn ngữ Tự nhiên", PURPLE, PURPLE_BG, [
            "• Tự động sinh cây WBS 20 bước",
            "• Gợi ý mối quan hệ FS/SS/FF/SF",
            "• Soạn thảo tự động 13 hồ sơ PMBOK",
            "• Định lượng bảng rủi ro EMV ($)"
        ]),
        ("2. GIAO THỨC MCP SERVER", "Kết nối AI Agent Chuẩn Mở", BLUE, BLUE_BG, [
            "• Truy vấn trạng thái dự án đám mây",
            "• Phân tích Đường găng & Quá tải",
            "• Cập nhật tiến độ hàng loạt an toàn",
            "• Quản lý khóa Check-out / Check-in"
        ]),
        ("3. CLOUD PMO & TELEGRAM", "Báo cáo Điều hành Thời gian thực", EMERALD_DARK, EMERALD_BG, [
            "• Tự động so sánh phiên bản (Diff)",
            "• Cảnh báo tức thời khi SPI/CPI < 1",
            "• Phát hiện dịch chuyển Đường găng",
            "• Bắn Executive Diff qua Telegram"
        ]),
    ]
    for i, (t, sub, col, bg, pts) in enumerate(stages):
        x = 48 + i * 384
        y = 175
        w, h = 336, 415
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 86], radius=14, fill=bg)
        draw.text((x + 20, y + 16), t, font=fnt(FONT_BOLD, 20), fill=col)
        draw.text((x + 20, y + 48), sub, font=fnt(FONT_BOLD, 14), fill=TEXT_DARK)
        for idx, pt in enumerate(pts):
            py = y + 108 + idx * 70
            draw.rounded_rectangle([x + 16, py, x + w - 16, py + 52], radius=8, fill=BG_MAIN, outline=BORDER_LIGHT, width=1)
            draw.text((x + 26, py + 14), pt, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)
        if i < 2:
            draw_arrow(draw, x + w + 8, y + 205, x + 384 - 10, y + 205, col)
    save_diagram(img, "pm12_1_ai_copilot_mcp_architecture")

    # 2. PM12-2: Executive Diff Telegram Alert Card
    img, draw = create_light_canvas(
        "BÁO CÁO CHÊNH LỆCH ĐIỀU HÀNH (EXECUTIVE DIFF) QUA TELEGRAM",
        "Cảnh báo Tự động cho Ban Giám đốc Mỗi khi Check-in Phiên bản Dự án Mới"
    )
    metrics = [
        ("1. BIẾN ĐỘNG TIẾN ĐỘ", "Finish Date: 12/11 → 14/11 (+2d)", "SPI giảm từ 1.00 xuống 0.91", ROSE, ROSE_BG),
        ("2. BIẾN ĐỘNG CHI PHÍ EVM", "CPI: 1.02 (Tiết kiệm ngân sách)", "EAC dự báo: $51,840 < $52,708", EMERALD_DARK, EMERALD_BG),
        ("3. THAY ĐỔI ĐƯỜNG GĂNG", "Phát sinh 1 Task Găng mới", "Bước 3.2 Tạo PO tự động (Slack = 0)", AMBER, AMBER_BG),
        ("4. QUỸ DỰ PHÒNG RỦI RO EMV", "EMV hiện hành: $3,260 (8 Rủi ro)", "Top Risk R4: Trễ tích hợp ERP ($990)", BLUE, BLUE_BG),
    ]
    for i, (t, m1, m2, col, bg) in enumerate(metrics):
        col_idx = i % 2
        row_idx = i // 2
        x = 48 + col_idx * 564
        y = 172 + row_idx * 214
        w, h = 540, 194
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 58], radius=14, fill=bg)
        draw.text((x + 22, y + 16), t, font=fnt(FONT_BOLD, 19), fill=col)
        draw.text((x + 22, y + 76), m1, font=fnt(FONT_BOLD, 21), fill=TEXT_DARK)
        draw.text((x + 22, y + 124), m2, font=fnt(FONT_BOLD, 17), fill=col)
    save_diagram(img, "pm12_2_executive_diff_telegram_alert")

if __name__ == "__main__":
    build_pm02()
    build_pm03()
    build_pm05()
    build_pm06()
    build_pm07()
    build_pm10()
    build_pm11()
    build_pm12()
    print("All 16 Light-Tone Minimalist Cluster Diagrams generated successfully!")
