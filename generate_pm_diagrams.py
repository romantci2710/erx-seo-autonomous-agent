# -*- coding: utf-8 -*-
"""
Generates 12 BRIGHT, MINIMALIST, HIGH-CONTRAST LIGHT-TONE diagrams (1200x675)
for the 4 Pillar Articles of the "Project Management" (PMBOK 8 & ERX Gantt Planner) hub.
Designed for instant legibility both as category thumbnails and inline figures.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"D:\GIT\SEO Tool\pm_assets"
os.makedirs(OUT_DIR, exist_ok=True)

FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_MONO = r"C:\Windows\Fonts\consolab.ttf"

def fnt(path, size):
    return ImageFont.truetype(path, size)

# Light-Tone Clean Editorial Palette
BG_MAIN = (248, 250, 252)       # #F8FAFC (Soft bright alabaster)
BG_WHITE = (255, 255, 255)      # #FFFFFF
BORDER_LIGHT = (203, 213, 225)  # #CBD5E1
GRID_LINE = (236, 242, 249)     # Subtle light grid

TEXT_DARK = (15, 23, 42)        # #0F172A (Deep Slate)
TEXT_BODY = (51, 65, 85)        # #334155
TEXT_MUTED = (100, 116, 139)    # #64748B

# Brand Accent Colors & Pastel Fills
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

    # Subtle background grid
    for x in range(0, W, 48):
        draw.line([(x, 0), (x, H)], fill=GRID_LINE, width=1)
    for y in range(0, H, 48):
        draw.line([(0, y), (W, y)], fill=GRID_LINE, width=1)

    # Outer frame & top emerald bar
    draw.rectangle([0, 0, W - 1, H - 1], outline=BORDER_LIGHT, width=2)
    draw.rectangle([0, 0, W, 10], fill=EMERALD)

    # Top badge pill
    draw.rounded_rectangle([48, 28, 370, 62], radius=17, fill=EMERALD_BG, outline=EMERALD, width=2)
    draw.text((66, 35), tag, font=fnt(FONT_BOLD, 15), fill=EMERALD_DARK)

    # Top-right platform pill
    draw.rounded_rectangle([880, 28, 1152, 62], radius=17, fill=BLUE_BG, outline=BLUE, width=2)
    draw.text((902, 35), "project-management.erx.vn", font=fnt(FONT_BOLD, 15), fill=BLUE)

    # Large, bold title & subtitle
    draw.text((48, 76), title, font=fnt(FONT_BOLD, 34), fill=TEXT_DARK)
    draw.text((48, 122), subtitle, font=fnt(FONT_REG, 19), fill=TEXT_BODY)

    # Clean bottom bar
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

def save_diagram(img, filename):
    path = os.path.join(OUT_DIR, filename)
    img.save(path, format="WEBP", quality=86, method=6)
    jpg_path = path.replace(".webp", ".jpg")
    img.save(jpg_path, format="JPEG", quality=90, optimize=True)
    print(f"Saved {filename}: WebP={os.path.getsize(path)/1024:.1f}KB, JPG={os.path.getsize(jpg_path)/1024:.1f}KB")

# ==============================================================================
# PM-01 DIAGRAMS (Light, Minimalist, Big Typography)
# ==============================================================================
def build_pm01():
    # 1. PM01-1: 3 Big Pillars of PMBOK 8
    img, draw = create_light_canvas(
        "CHUẨN QUẢN TRỊ DỰ ÁN PMBOK® 8",
        "Kiến trúc Hợp nhất: 6 Nguyên tắc • 7 Miền Hiệu suất • 5 Nhóm Quy trình & AI"
    )
    pillars = [
        ("06", "NGUYÊN TẮC CỐT LÕI", "Core Principles", EMERALD_DARK, EMERALD_BG, [
            "• Tư duy Hệ thống Tổng thể",
            "• Tập trung Giá trị & ROI",
            "• Nhúng Chất lượng từ đầu",
            "• Trách nhiệm Giải trình RACI"
        ]),
        ("07", "MIỀN HIỆU SUẤT", "Performance Domains", BLUE, BLUE_BG, [
            "• Quản trị (Governance) & Phạm vi",
            "• Tiến độ (CPM) & Tài chính (EVM)",
            "• Bên liên quan & Nguồn lực",
            "• Định lượng Rủi ro (EMV $)"
        ]),
        ("05", "NHÓM QUY TRÌNH + AI", "Process Groups & AI", AMBER, AMBER_BG, [
            "• Khởi tạo → Lập kế hoạch",
            "• Thực thi → Kiểm soát EVM",
            "• Đóng dự án & Bài học",
            "• AI Co-Pilot & Cloud Sync"
        ]),
    ]
    for i, (num, title, sub, col, bg_col, items) in enumerate(pillars):
        x = 48 + i * 376
        y = 172
        w, h = 352, 425
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + w - 3, y + 135], radius=14, fill=bg_col)
        # Big number badge
        draw.rounded_rectangle([x + 24, y + 22, x + 104, y + 102], radius=14, fill=col)
        draw.text((x + 40, y + 34), num, font=fnt(FONT_BOLD, 40), fill=BG_WHITE)
        draw.text((x + 120, y + 32), title, font=fnt(FONT_BOLD, 20), fill=col)
        draw.text((x + 120, y + 64), sub, font=fnt(FONT_REG, 16), fill=TEXT_MUTED)

        for idx, pt in enumerate(items):
            py = y + 162 + idx * 60
            draw.rounded_rectangle([x + 20, py, x + w - 20, py + 46], radius=8, fill=BG_MAIN, outline=BORDER_LIGHT, width=1)
            draw.text((x + 34, py + 10), pt, font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)

    save_diagram(img, "pm01_1_pmbok8_architecture.webp")

    # 2. PM01-2: 13 PMBOK Artifacts grouped into 4 clean visual quadrants
    img, draw = create_light_canvas(
        "13 HỒ SƠ QUẢN TRỊ DỰ ÁN CHUẨN PMBOK® 8",
        "Số hóa & Đồng bộ Thời gian thực trên Nền tảng project-management.erx.vn"
    )
    groups = [
        (48, 175, "NHÓM 1: KHỞI TẠO & QUẢN TRỊ", EMERALD_DARK, EMERALD_BG, [
            "01. Project Charter (Điều lệ Dự án)",
            "02. Business Case (Bài toán Đầu tư)",
            "03. Benefits Plan (Quản trị Lợi ích)"
        ]),
        (616, 175, "NHÓM 2: BÊN LIÊN QUAN & NHÂN SỰ", BLUE, BLUE_BG, [
            "04. Stakeholder Register (Power/Interest)",
            "05. Ma trận Trách nhiệm RACI",
            "06. Communication & 08. HR Plan"
        ]),
        (48, 395, "NHÓM 3: CHẤT LƯỢNG & RÀNG BUỘC", PURPLE, PURPLE_BG, [
            "07. Quality Metrics (Chỉ số Nghiệm thu)",
            "09. Assumption & Constraint Log",
            "Liên kết trực tiếp với Từ điển WBS"
        ]),
        (616, 395, "NHÓM 4: ĐỊNH LƯỢNG RỦI RO & EMV ($)", ROSE, ROSE_BG, [
            "10. Cây Rủi ro RBS & 11. Thang đo 1–5",
            "12. Ma trận EMV = P(%) × Impact($)",
            "13. Risk Register (Đồng bộ vào Ngân sách)"
        ]),
    ]
    for gx, gy, gtitle, col, bg_col, lines in groups:
        draw.rounded_rectangle([gx, gy, gx + 536, gy + 198], radius=14, fill=BG_WHITE, outline=col, width=3)
        draw.rectangle([gx + 3, gy + 3, gx + 533, gy + 52], fill=bg_col)
        draw.text((gx + 22, gy + 13), gtitle, font=fnt(FONT_BOLD, 19), fill=col)
        for li, line in enumerate(lines):
            draw.text((gx + 24, gy + 66 + li * 40), "•  " + line, font=fnt(FONT_BOLD, 18), fill=TEXT_DARK)

    save_diagram(img, "pm01_2_13_pmbok_artifacts.webp")

    # 3. PM01-3: 5 Process Groups Workflow
    img, draw = create_light_canvas(
        "CHU TRÌNH 5 BƯỚC QUẢN TRỊ DỰ ÁN KHÉP KÍN",
        "Từ Lập Điều lệ Dự án đến Cảnh báo Điều hành Tự động trên Đám mây"
    )
    steps = [
        ("BƯỚC 1", "KHỞI TẠO", "Project Charter\n& Ma trận RACI", EMERALD_DARK, EMERALD_BG),
        ("BƯỚC 2", "KẾ HOẠCH", "Cây WBS 100%\n& Đường găng CPM", BLUE, BLUE_BG),
        ("BƯỚC 3", "RỦI RO", "Tính Quỹ EMV ($)\n& Chốt Baseline", AMBER, AMBER_BG),
        ("BƯỚC 4", "THỰC THI", "Check-out Cloud\n& Cân bằng Nhân sự", TEAL, TEAL_BG),
        ("BƯỚC 5", "GIÁM SÁT", "Đo lường SPI / CPI\n& Báo cáo Telegram", ROSE, ROSE_BG),
    ]
    for i, (st_no, st_name, st_desc, col, bg_col) in enumerate(steps):
        x = 48 + i * 226
        y = 190
        draw.rounded_rectangle([x, y, x + 200, y + 260], radius=16, fill=BG_WHITE, outline=col, width=3)
        draw.rounded_rectangle([x + 3, y + 3, x + 197, y + 95], radius=13, fill=bg_col)
        draw.text((x + 22, y + 18), st_no, font=fnt(FONT_BOLD, 15), fill=col)
        draw.text((x + 22, y + 44), st_name, font=fnt(FONT_BOLD, 24), fill=TEXT_DARK)
        for li, l_txt in enumerate(st_desc.split("\n")):
            draw.text((x + 20, y + 125 + li * 36), l_txt, font=fnt(FONT_BOLD, 17), fill=TEXT_BODY)
        if i < 4:
            draw_arrow(draw, x + 203, y + 130, x + 221, y + 130, col)

    # Bottom highlight banner
    draw.rounded_rectangle([48, 485, 1152, 595], radius=14, fill=EMERALD_BG, outline=EMERALD, width=2)
    draw.text((76, 505), "ĐIỂM KHÁC BIỆT CỦA NỀN TẢNG PROJECT-MANAGEMENT.ERX.VN:", font=fnt(FONT_BOLD, 19), fill=EMERALD_DARK)
    draw.text((76, 542), "Mọi thay đổi tiến độ trên WBS/Gantt tự động cập nhật Đường găng (CPM), chỉ số EVM và Ngân sách Phê duyệt!", font=fnt(FONT_BOLD, 18), fill=TEXT_DARK)

    save_diagram(img, "pm01_3_process_groups_workflow.webp")

# ==============================================================================
# PM-04 DIAGRAMS (WBS & WBS Dictionary - Light, Minimalist)
# ==============================================================================
def build_pm04():
    # 1. PM04-1: Clean 3-Level Visual WBS Tree & 100% Rule
    img, draw = create_light_canvas(
        "CẤU TRÚC PHÂN RÃ CÔNG VIỆC (WBS)",
        "Cây Phân cấp Hướng Giao phẩm & Quy tắc 100% Chuẩn PMBOK® 8"
    )
    # Root Node
    draw.rounded_rectangle([320, 170, 880, 250], radius=14, fill=EMERALD_BG, outline=EMERALD_DARK, width=3)
    draw.text((355, 184), "CẤP 1 (TASK 0): DỰ ÁN TỔNG THỂ = 100% PHẠM VI", font=fnt(FONT_BOLD, 20), fill=EMERALD_DARK)
    draw.text((395, 215), "Tổng thời lượng: 28 Ngày   •   Ngân sách: $52,708", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)

    # Tree connectors
    draw.line([(600, 250), (600, 280)], fill=TEXT_MUTED, width=3)
    draw.line([(210, 280), (990, 280)], fill=TEXT_MUTED, width=3)

    branches = [
        ("1.0 KHỞI TẠO & PR", "20% Phạm vi • 5 Ngày", ["1.1 Lập Project Charter", "1.2 Phê duyệt Nhu cầu PR"], EMERALD_DARK, EMERALD_BG),
        ("2.0 ĐẤU THẦU (RFQ)", "45% Phạm vi • 8 Ngày", ["2.1 Phát hành Hồ sơ RFQ", "2.2 Chấm điểm & Chốt NCC"], BLUE, BLUE_BG),
        ("3.0 ĐẶT HÀNG & ĐÓNG", "35% Phạm vi • 15 Ngày", ["3.1 Đối soát 3-Way Match", "3.2 Nghiệm thu (Milestone 0d)"], AMBER, AMBER_BG),
    ]
    for i, (b_title, b_sub, leaves, col, bg_col) in enumerate(branches):
        cx = 210 + i * 390
        draw.line([(cx, 280), (cx, 305)], fill=col, width=3)
        x1 = cx - 165
        draw.rounded_rectangle([x1, 305, x1 + 330, 390], radius=12, fill=bg_col, outline=col, width=3)
        draw.text((x1 + 22, 318), b_title, font=fnt(FONT_BOLD, 20), fill=col)
        draw.text((x1 + 22, 350), b_sub, font=fnt(FONT_BOLD, 16), fill=TEXT_DARK)

        for li, leaf in enumerate(leaves):
            ly = 415 + li * 74
            draw.rounded_rectangle([x1, ly, x1 + 330, ly + 58], radius=10, fill=BG_WHITE, outline=BORDER_LIGHT, width=2)
            draw.rectangle([x1, ly, x1 + 8, ly + 58], fill=col)
            draw.text((x1 + 22, ly + 16), leaf, font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)

    # Bottom Rule 100% Pill
    draw.rounded_rectangle([48, 568, 1152, 616], radius=10, fill=BLUE_BG, outline=BLUE, width=2)
    draw.text((160, 580), "QUY TẮC 100%: Tổng khối lượng các gói công việc con bằng đúng 100% phạm vi mục cha!", font=fnt(FONT_BOLD, 18), fill=BLUE)

    save_diagram(img, "pm04_1_wbs_hierarchy_100_rule.webp")

    # 2. PM04-2: Clean 5-Row Gantt & WBS Table Preview
    img, draw = create_light_canvas(
        "MÔ HÌNH BẢNG WBS & BIỂU ĐỒ GANTT (CPM)",
        "Phân biệt Summary Task, Gói công việc (Work Package) và Cột mốc (Milestone 0d)"
    )
    draw.rounded_rectangle([48, 175, 1152, 590], radius=14, fill=BG_WHITE, outline=BORDER_LIGHT, width=2)
    draw.rectangle([48, 175, 1152, 228], fill=(241, 245, 249))
    draw.text((70, 190), "Mã WBS", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
    draw.text((180, 190), "Tên Hạng mục Công việc", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
    draw.text((550, 190), "Thời lượng", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
    draw.text((680, 190), "Phụ thuộc", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
    draw.text((820, 190), "Biểu đồ Gantt & Đường găng (CPM)", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)

    rows = [
        ("0", "▼ DỰ ÁN CHUỖI CUNG ỨNG P2P (Summary)", "28 Ngày", "-", 0.0, 1.0, "summary"),
        ("1.1", "   Lập Project Charter & Nhu cầu PR", "2 Ngày", "-", 0.0, 0.16, "critical"),
        ("1.2", "   Kiểm tra Ngân sách Song song", "3 Ngày", "1.1 SS+1d", 0.08, 0.32, "critical"),
        ("1.3", "   [M] Cột mốc: Chốt Điều lệ & PR", "0 Ngày", "1.2 FS", 0.32, 0.32, "milestone"),
        ("2.1", "   Đấu thầu RFQ & Chấm điểm NCC", "8 Ngày", "1.3 FS", 0.32, 0.72, "normal"),
        ("3.1", "   Đối soát 3-Way Matching & Nghiệm thu", "7 Ngày", "2.1 FS", 0.72, 1.0, "critical"),
    ]
    for idx, (wbs, name, dur, pred, s, e, rtype) in enumerate(rows):
        y = 230 + idx * 58
        row_bg = EMERALD_BG if rtype == "summary" else (BG_MAIN if idx % 2 == 1 else BG_WHITE)
        draw.rectangle([50, y, 1150, y + 56], fill=row_bg)
        draw.line([(50, y + 56), (1150, y + 56)], fill=BORDER_LIGHT, width=1)

        f_use = fnt(FONT_BOLD, 17) if rtype in ("summary", "milestone") else fnt(FONT_REG, 17)
        t_col = EMERALD_DARK if rtype == "summary" else (AMBER if rtype == "milestone" else TEXT_DARK)
        draw.text((70, y + 16), wbs, font=fnt(FONT_MONO, 17), fill=t_col)
        draw.text((180, y + 16), name, font=f_use, fill=t_col)
        draw.text((560, y + 16), dur, font=fnt(FONT_BOLD, 17), fill=t_col)
        draw.text((680, y + 16), pred, font=fnt(FONT_MONO, 16), fill=BLUE)

        gx1 = int(820 + s * 300)
        gx2 = int(820 + e * 300)
        if rtype == "milestone":
            pts = [(gx1, y + 14), (gx1 + 14, y + 28), (gx1, y + 42), (gx1 - 14, y + 28)]
            draw.polygon(pts, fill=AMBER)
        elif rtype == "summary":
            draw.rectangle([gx1, y + 22, gx2, y + 32], fill=EMERALD_DARK)
            draw.polygon([(gx1, y + 22), (gx1 + 8, y + 22), (gx1, y + 38)], fill=EMERALD_DARK)
            draw.polygon([(gx2, y + 22), (gx2 - 8, y + 22), (gx2, y + 38)], fill=EMERALD_DARK)
        else:
            b_col = ROSE if rtype == "critical" else BLUE
            draw.rounded_rectangle([gx1, y + 14, max(gx1 + 20, gx2), y + 42], radius=7, fill=b_col)

    save_diagram(img, "pm04_2_wbs_gantt_interface.webp")

    # 3. PM04-3: 6-Card Grid for WBS Dictionary
    img, draw = create_light_canvas(
        "CẤU TRÚC TỪ ĐIỂN WBS (WBS DICTIONARY)",
        "6 Trường Thông tin Biến Gói Công việc Thành Hợp đồng Giao việc Minh bạch"
    )
    cards = [
        ("01. MÃ SỐ & ĐỊNH DANH", "Mã phân cấp tự động\n(1.1, 1.2, 2.1.1)", EMERALD_DARK, EMERALD_BG),
        ("02. MÔ TẢ PHẠM VI", "Ranh giới công việc\nIn-Scope & Out-of-Scope", BLUE, BLUE_BG),
        ("03. TIÊU CHÍ NGHIỆM THU", "Chỉ số Quality Metrics\n& Dung sai cho phép", TEAL, TEAL_BG),
        ("04. LỊCH & RÀNG BUỘC", "Quan hệ FS/SS/FF/SF\n& Constraint (ASAP)", AMBER, AMBER_BG),
        ("05. ĐỊNH MỨC NGUỒN LỰC", "Work = Duration × Units\n& Ngân sách gốc (BAC)", PURPLE, PURPLE_BG),
        ("06. MA TRẬN RACI & RỦI RO", "Người chịu trách nhiệm (R/A)\n& Mã rủi ro liên kết", ROSE, ROSE_BG),
    ]
    for idx, (c_title, c_body, col, bg_col) in enumerate(cards):
        r = idx // 3
        c = idx % 3
        x = 48 + c * 376
        y = 180 + r * 205
        draw.rounded_rectangle([x, y, x + 352, y + 180], radius=14, fill=BG_WHITE, outline=col, width=3)
        draw.rectangle([x + 3, y + 3, x + 349, y + 58], fill=bg_col)
        draw.text((x + 22, y + 16), c_title, font=fnt(FONT_BOLD, 18), fill=col)
        for li, line in enumerate(c_body.split("\n")):
            draw.text((x + 22, y + 78 + li * 36), line, font=fnt(FONT_BOLD, 19), fill=TEXT_DARK)

    save_diagram(img, "pm04_3_wbs_dictionary_card.webp")

# ==============================================================================
# PM-08 DIAGRAMS (Earned Value Management - EVM - Light, Minimalist)
# ==============================================================================
def build_pm08():
    # 1. PM08-1: Bright Clean S-Curve & 3 Giant KPI Cards
    img, draw = create_light_canvas(
        "QUẢN LÝ GIÁ TRỊ THU ĐƯỢC (EVM S-CURVE)",
        "So sánh Kế hoạch (PV), Giá trị Đạt được (EV), Chi phí Thực tế (AC) & Dự báo EAC"
    )
    draw.rounded_rectangle([48, 175, 815, 595], radius=14, fill=BG_WHITE, outline=BORDER_LIGHT, width=2)
    ox, oy, cw, ch = 105, 545, 660, 330
    draw.line([(ox, oy), (ox + cw, oy)], fill=TEXT_DARK, width=3)
    draw.line([(ox, oy), (ox, oy - ch)], fill=TEXT_DARK, width=3)

    y_bac = oy - int(ch * 0.76)
    y_eac = oy - int(ch * 0.92)
    draw.line([(ox, y_bac), (ox + cw, y_bac)], fill=EMERALD_DARK, width=2)
    draw.text((ox + 12, y_bac - 26), "BAC (Ngân sách Gốc) = $49,448", font=fnt(FONT_BOLD, 16), fill=EMERALD_DARK)

    draw.line([(ox, y_eac), (ox + cw, y_eac)], fill=ROSE, width=2)
    draw.text((ox + 12, y_eac - 26), "EAC (Dự báo Cuối kỳ) = $54,942", font=fnt(FONT_BOLD, 16), fill=ROSE)

    sx = ox + int(cw * 0.58)
    draw.line([(sx, oy), (sx, oy - ch)], fill=AMBER, width=3)
    draw.text((sx - 85, oy + 12), "Ngày Báo cáo (Status Date)", font=fnt(FONT_BOLD, 15), fill=AMBER)

    def s_curve(t, max_y):
        val = 1 / (1 + math.exp(-8 * (t - 0.5)))
        v0 = 1 / (1 + math.exp(4))
        v1 = 1 / (1 + math.exp(-4))
        return ((val - v0) / (v1 - v0)) * max_y

    pv_pts = [(ox + int(i / 100 * cw), oy - int(s_curve(i / 100, ch * 0.76))) for i in range(101)]
    ev_pts = [(ox + int(i / 100 * cw), oy - int(s_curve(i / 100 * 0.90, ch * 0.70))) for i in range(59)]
    ac_pts = [(ox + int(i / 100 * cw), oy - int(s_curve(i / 100 * 1.03, ch * 0.88))) for i in range(59)]

    draw.line(pv_pts, fill=BLUE, width=5)
    draw.line(ev_pts, fill=EMERALD_DARK, width=5)
    draw.line(ac_pts, fill=ROSE, width=5)

    draw.text((sx - 155, ac_pts[-1][1] - 28), "AC ($29,600)", font=fnt(FONT_BOLD, 16), fill=ROSE)
    draw.text((sx + 70, pv_pts[68][1] + 18), "PV (Kế hoạch)", font=fnt(FONT_BOLD, 16), fill=BLUE)
    draw.text((sx + 16, ev_pts[-1][1] + 4), "EV ($26,640)", font=fnt(FONT_BOLD, 16), fill=EMERALD_DARK)

    # 3 Giant KPI Cards on the right
    kpis = [
        ("HIỆU SUẤT TIẾN ĐỘ (SPI)", "SPI = 0.90", "SV = -$2,960 (Trễ tiến độ)", AMBER, AMBER_BG),
        ("HIỆU SUẤT CHI PHÍ (CPI)", "CPI = 0.90", "CV = -$2,960 (Vượt dự toán)", ROSE, ROSE_BG),
        ("DỰ BÁO HOÀN THÀNH (EAC)", "$54,942", "EAC = BAC / CPI (+11.1%)", PURPLE, PURPLE_BG),
    ]
    for i, (k_t, k_big, k_sub, col, bg_col) in enumerate(kpis):
        ky = 175 + i * 144
        draw.rounded_rectangle([840, ky, 1152, ky + 128], radius=14, fill=bg_col, outline=col, width=3)
        draw.text((862, ky + 14), k_t, font=fnt(FONT_BOLD, 15), fill=col)
        draw.text((862, ky + 42), k_big, font=fnt(FONT_BOLD, 32), fill=TEXT_DARK)
        draw.text((862, ky + 88), k_sub, font=fnt(FONT_BOLD, 15), fill=TEXT_BODY)

    save_diagram(img, "pm08_1_evm_s_curve_chart.webp")

    # 2. PM08-2: 4 Clean Quadrants SPI x CPI
    img, draw = create_light_canvas(
        "MA TRẬN CHẨN ĐOÁN DỰ ÁN 4 GÓC PHẦN TƯ (SPI × CPI)",
        "Hướng dẫn Ra Quyết định Điều hành Ngay lập tức dựa trên Chỉ số Tiến độ & Chi phí"
    )
    quads = [
        (48, 175, "1. VƯỢT TIẾN ĐỘ • ĐỘI CHI PHÍ", "SPI > 1.0   |   CPI < 1.0", AMBER, AMBER_BG,
         "Hành động: Cắt giảm làm thêm giờ (OT) ở các công việc không nằm trên Đường găng."),
        (616, 175, "2. DỰ ÁN LÝ TƯỞNG (XANH)", "SPI ≥ 1.0   |   CPI ≥ 1.0", EMERALD_DARK, EMERALD_BG,
         "Hành động: Duy trì Baseline hiện tại, giải phóng dần Quỹ dự phòng EMV khi đóng rủi ro."),
        (48, 395, "3. BÁO ĐỘNG ĐỎ (TRỄ & ĐỘI VỐN)", "SPI < 1.0   |   CPI < 1.0", ROSE, ROSE_BG,
         "Hành động: Áp dụng Fast-Tracking (SS+Lag) trên Đường găng & kích hoạt Quỹ dự phòng EMV."),
        (616, 395, "4. TIẾT KIỆM • TRỄ TIẾN ĐỘ", "SPI < 1.0   |   CPI ≥ 1.0", BLUE, BLUE_BG,
         "Hành động: Chạy Resource Leveling điều chuyển nhân sự sang các gói việc trên Đường găng."),
    ]
    for qx, qy, qt, qformula, col, bg_col, qact in quads:
        draw.rounded_rectangle([qx, qy, qx + 536, qy + 198], radius=14, fill=BG_WHITE, outline=col, width=3)
        draw.rectangle([qx + 3, qy + 3, qx + 533, qy + 82], fill=bg_col)
        draw.text((qx + 24, qy + 12), qt, font=fnt(FONT_BOLD, 20), fill=col)
        draw.text((qx + 24, qy + 44), qformula, font=fnt(FONT_MONO, 18), fill=TEXT_DARK)
        draw.text((qx + 24, qy + 102), qact[:48], font=fnt(FONT_BOLD, 17), fill=TEXT_BODY)
        draw.text((qx + 24, qy + 132), qact[48:], font=fnt(FONT_BOLD, 17), fill=TEXT_BODY)

    save_diagram(img, "pm08_2_spi_cpi_quadrant_matrix.webp")

    # 3. PM08-3: 3x3 Clean Formula Cards
    img, draw = create_light_canvas(
        "9 CÔNG THỨC EVM CỐT LÕI CHUẨN PMBOK® 8",
        "Tính toán Tự động trên Hệ thống 11 Khe Baseline của project-management.erx.vn"
    )
    f_cards = [
        ("1. BAC", "Tổng PV toàn dự án", "Ngân sách cơ sở gốc", EMERALD_DARK, EMERALD_BG),
        ("2. PV (Kế hoạch)", "BAC × % Kế hoạch", "Ngân sách theo tiến độ", BLUE, BLUE_BG),
        ("3. EV (Thu được)", "BAC × % Thực tế", "Giá trị khối lượng đã xong", EMERALD_DARK, EMERALD_BG),
        ("4. AC (Thực chi)", "Chi phí thực tế đã bỏ ra", "Giờ công + Chi phí cố định", TEAL, TEAL_BG),
        ("5. SV (Lệch tiến độ)", "SV = EV − PV", "SV < 0: Dự án đang trễ", AMBER, AMBER_BG),
        ("6. CV (Lệch chi phí)", "CV = EV − AC", "CV < 0: Dự án vượt chi", ROSE, ROSE_BG),
        ("7. Chỉ số SPI", "SPI = EV / PV", "Chuẩn mục tiêu ≥ 1.00", AMBER, AMBER_BG),
        ("8. Chỉ số CPI", "CPI = EV / AC", "Chuẩn mục tiêu ≥ 1.00", ROSE, ROSE_BG),
        ("9. Dự báo EAC", "EAC = BAC / CPI", "Dự báo tổng chi cuối kỳ", PURPLE, PURPLE_BG),
    ]
    for idx, (ft, feq, fsub, col, bg_col) in enumerate(f_cards):
        r = idx // 3
        c = idx % 3
        x = 48 + c * 376
        y = 175 + r * 140
        draw.rounded_rectangle([x, y, x + 352, y + 124], radius=12, fill=BG_WHITE, outline=col, width=2)
        draw.rectangle([x + 2, y + 2, x + 350, y + 42], fill=bg_col)
        draw.text((x + 18, y + 9), ft, font=fnt(FONT_BOLD, 17), fill=col)
        draw.text((x + 18, y + 50), feq, font=fnt(FONT_BOLD, 21), fill=TEXT_DARK)
        draw.text((x + 18, y + 86), fsub, font=fnt(FONT_REG, 15), fill=TEXT_BODY)

    save_diagram(img, "pm08_3_9_evm_formulas_table.webp")

# ==============================================================================
# PM-09 DIAGRAMS (Risk EMV & Contingency Reserve - Light, Minimalist)
# ==============================================================================
def build_pm09():
    # 1. PM09-1: Giant Visual Equation BAC + EMV = Approved Budget
    img, draw = create_light_canvas(
        "ĐỊNH LƯỢNG RỦI RO DỰ ÁN BẰNG CÔNG THỨC EMV ($)",
        "Cơ chế Tự động Đồng bộ Quỹ Dự phòng vào Ngân sách Phê duyệt (PMBOK® 8)"
    )
    # Top Formula Banner
    draw.rounded_rectangle([48, 175, 1152, 285], radius=16, fill=AMBER_BG, outline=AMBER, width=3)
    draw.text((80, 192), "CÔNG THỨC GIÁ TRỊ TIỀN TỆ KỲ VỌNG (EXPECTED MONETARY VALUE - EMV):", font=fnt(FONT_BOLD, 18), fill=AMBER)
    draw.text((80, 228), "EMV ($)  =  Xác suất xảy ra (P %)  ×  Tác động Tài chính (Impact $)", font=fnt(FONT_BOLD, 28), fill=TEXT_DARK)

    # 3 Giant Equation Blocks at bottom
    b1x, b2x, b3x = 48, 444, 840
    by = 325
    bw, bh = 312, 260

    draw.rounded_rectangle([b1x, by, b1x + bw, by + bh], radius=16, fill=BLUE_BG, outline=BLUE, width=3)
    draw.text((b1x + 24, by + 24), "1. NGÂN SÁCH GỐC (BAC)", font=fnt(FONT_BOLD, 18), fill=BLUE)
    draw.text((b1x + 24, by + 75), "$49,448", font=fnt(FONT_BOLD, 46), fill=TEXT_DARK)
    draw.text((b1x + 24, by + 155), "Tổng chi phí cuốn chiếu\ntừ 20 gói công việc WBS", font=fnt(FONT_BOLD, 17), fill=TEXT_BODY)

    # Plus sign
    draw.text((382, by + 95), "+", font=fnt(FONT_BOLD, 56), fill=TEXT_DARK)

    draw.rounded_rectangle([b2x, by, b2x + bw, by + bh], radius=16, fill=AMBER_BG, outline=AMBER, width=3)
    draw.text((b2x + 24, by + 24), "2. QUỸ DỰ PHÒNG (EMV)", font=fnt(FONT_BOLD, 18), fill=AMBER)
    draw.text((b2x + 24, by + 75), "+$3,260", font=fnt(FONT_BOLD, 46), fill=AMBER)
    draw.text((b2x + 24, by + 155), "Tổng EMV của 8 rủi ro\ntrọng yếu (R1 đến R8)", font=fnt(FONT_BOLD, 17), fill=TEXT_BODY)

    # Equals sign
    draw.text((778, by + 95), "=", font=fnt(FONT_BOLD, 56), fill=EMERALD_DARK)

    draw.rounded_rectangle([b3x, by, b3x + bw, by + bh], radius=16, fill=EMERALD_BG, outline=EMERALD_DARK, width=3)
    draw.text((b3x + 24, by + 24), "3. NGÂN SÁCH DUYỆT", font=fnt(FONT_BOLD, 18), fill=EMERALD_DARK)
    draw.text((b3x + 24, by + 75), "$52,708", font=fnt(FONT_BOLD, 46), fill=EMERALD_DARK)
    draw.text((b3x + 24, by + 155), "Cost Baseline tự động\nđồng bộ vào Project Charter", font=fnt(FONT_BOLD, 17), fill=TEXT_BODY)

    save_diagram(img, "pm09_1_emv_budget_sync_flow.webp")

    # 2. PM09-2: Clean Bright 5x5 Heatmap
    img, draw = create_light_canvas(
        "MA TRẬN NHIỆT ĐÁNH GIÁ RỦI RO 5×5 (P × I HEATMAP)",
        "Phân tầng Mức độ Rủi ro: Thấp (1–4) • Trung bình (5–9) • Cao (10–15) • Nghiêm trọng (16–25)"
    )
    gx0, gy0, cw, ch = 195, 175, 102, 74
    probs = [("Mức 5 (80%)", 5), ("Mức 4 (60%)", 4), ("Mức 3 (40%)", 3), ("Mức 2 (25%)", 2), ("Mức 1 (10%)", 1)]
    imps = [("Tác động 1", 1), ("Tác động 2", 2), ("Tác động 3", 3), ("Tác động 4", 4), ("Tác động 5", 5)]

    for r, (p_lbl, p_val) in enumerate(probs):
        y = gy0 + r * ch
        draw.text((48, y + 24), p_lbl, font=fnt(FONT_BOLD, 16), fill=TEXT_DARK)
        for c, (i_lbl, i_val) in enumerate(imps):
            x = gx0 + c * cw
            sc = p_val * i_val
            if sc >= 16:
                bg_c, brd_c, txt_c = ROSE_BG, ROSE, ROSE
            elif sc >= 10:
                bg_c, brd_c, txt_c = AMBER_BG, AMBER, AMBER
            elif sc >= 5:
                bg_c, brd_c, txt_c = BLUE_BG, BLUE, BLUE
            else:
                bg_c, brd_c, txt_c = EMERALD_BG, EMERALD_DARK, EMERALD_DARK
            draw.rounded_rectangle([x + 3, y + 3, x + cw - 3, y + ch - 3], radius=8, fill=bg_c, outline=brd_c, width=2)
            draw.text((x + 32, y + 22), str(sc), font=fnt(FONT_BOLD, 22), fill=txt_c)

    for c, (i_lbl, _) in enumerate(imps):
        x = gx0 + c * cw
        draw.text((x + 8, gy0 + 5 * ch + 12), i_lbl, font=fnt(FONT_BOLD, 15), fill=TEXT_DARK)

    # Right 4 clean legend cards
    legends = [
        ("NGHIÊM TRỌNG (16–25)", "Né tránh (Avoid) hoặc Chuyển giao ngay", ROSE, ROSE_BG),
        ("RỦI RO CAO (10–15)", "Giảm thiểu (Mitigate) & Trích lập EMV ($)", AMBER, AMBER_BG),
        ("TRUNG BÌNH (5–9)", "Giám sát định kỳ & Trích lập EMV ($)", BLUE, BLUE_BG),
        ("RỦI RO THẤP (1–4)", "Chấp nhận (Accept) & Theo dõi Watchlist", EMERALD_DARK, EMERALD_BG),
    ]
    for i, (lt, ld, col, bg_col) in enumerate(legends):
        ly = 178 + i * 102
        draw.rounded_rectangle([740, ly, 1152, ly + 88], radius=12, fill=bg_col, outline=col, width=2)
        draw.text((762, ly + 14), lt, font=fnt(FONT_BOLD, 18), fill=col)
        draw.text((762, ly + 46), ld, font=fnt(FONT_BOLD, 16), fill=TEXT_DARK)

    save_diagram(img, "pm09_2_pxi_risk_heatmap.webp")

    # 3. PM09-3: Clean 5-Row Summary Table of Risk EMV
    img, draw = create_light_canvas(
        "BẢNG TÍNH QUỸ DỰ PHÒNG EMV THỰC TẾ ($3,260)",
        "Minh họa Cách Tính EMV = P(%) × Impact($) trong Dự án Chuỗi Cung Ứng P2P"
    )
    draw.rounded_rectangle([48, 175, 1152, 595], radius=14, fill=BG_WHITE, outline=BORDER_LIGHT, width=2)
    draw.rectangle([48, 175, 1152, 230], fill=(241, 245, 249))
    draw.text((68, 192), "Mã", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
    draw.text((140, 192), "Sự kiện Rủi ro Trọng yếu", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
    draw.text((570, 192), "Xác suất (P)", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
    draw.text((720, 192), "Tác động ($)", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
    draw.text((885, 192), "Quỹ EMV ($)", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
    draw.text((1030, 192), "Chiến lược", font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)

    r_rows = [
        ("R1", "Chậm phê duyệt ngân sách PR liên phòng ban", "25%", "$3,200", "+$800", "SLA 24h"),
        ("R2", "Nhà cung cấp báo giá vượt trần dự toán", "30%", "$2,500", "+$750", "Đấu thầu 3 NCC"),
        ("R3", "Lỗi tích hợp cổng API ERP & E-Procurement", "20%", "$2,800", "+$560", "Sandbox UAT"),
        ("R4", "Giao hàng trễ hạn do biến động Lead-time", "25%", "$1,600", "+$400", "Phạt hợp đồng"),
        ("R5..8", "Nhóm 4 rủi ro vận hành & đối soát khác", "10–20%", "$4,800", "+$750", "Kiểm soát tự động"),
    ]
    for i, (rc, rn, rp, ri, remv, rst) in enumerate(r_rows):
        y = 232 + i * 56
        draw.rectangle([50, y, 1150, y + 54], fill=BG_MAIN if i % 2 == 1 else BG_WHITE)
        draw.line([(50, y + 54), (1150, y + 54)], fill=BORDER_LIGHT, width=1)
        draw.text((68, y + 14), rc, font=fnt(FONT_MONO, 17), fill=AMBER)
        draw.text((140, y + 14), rn, font=fnt(FONT_BOLD, 17), fill=TEXT_DARK)
        draw.text((590, y + 14), rp, font=fnt(FONT_MONO, 17), fill=BLUE)
        draw.text((735, y + 14), ri, font=fnt(FONT_MONO, 17), fill=TEXT_DARK)
        draw.text((895, y + 14), remv, font=fnt(FONT_BOLD, 18), fill=EMERALD_DARK)
        draw.text((1030, y + 14), rst, font=fnt(FONT_REG, 16), fill=TEXT_BODY)

    # Footer total row inside table
    draw.rounded_rectangle([50, 518, 1150, 593], radius=12, fill=EMERALD_BG, outline=EMERALD_DARK, width=2)
    draw.text((75, 542), "TỔNG NGÂN SÁCH PHÊ DUYỆT  =  $49,448 (BAC)  +  $3,260 (Tổng Quỹ EMV)  =  $52,708", font=fnt(FONT_BOLD, 21), fill=EMERALD_DARK)

    save_diagram(img, "pm09_3_p2p_risk_emv_table.webp")

if __name__ == "__main__":
    build_pm01()
    build_pm04()
    build_pm08()
    build_pm09()
    print("ALL 12 LIGHT-TONE MINIMALIST DIAGRAMS GENERATED!")
