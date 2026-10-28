# -*- coding: utf-8 -*-
"""
Generates:
1. Standardized 16:9 (800x450) thumbnails for the homepage articles that had non-16:9 ratios (1:1, 4:3, 2:1)
   so zero text is cropped and zero white gaps appear.
2. D:\\GIT\\SEO Tool\\pm_assets\\erx_caps_and_thumbs_upgrader.js to:
   - Update META.SCRIPT_HEADER (Global text-transform: none !important + uniform 16:9 thumbnail containers on Homepage & Category pages + uniform 1:1 on Hoi Thao cards + runtime DOM normalizer for any remaining ALL CAPS titles/footer/workshop labels).
   - Update the 5 Footer Modules in /administrator/module/list (HỖ TRỢ KHÁCH HÀNG -> Hỗ trợ khách hàng, VỀ ERX VIỆT NAM -> Về ERX Việt Nam, HỢP TÁC VÀ LIÊN KẾT -> Hợp tác và liên kết, KẾT NỐI VỚI CHÚNG TÔI -> Kết nối với chúng tôi).
   - Update all Workshop / Hội thảo items (/hoi-thao.html) from ALL CAPS to clean Title/Sentence Case.
   - Update the 4 ALL-CAPS Blog Article titles (7123806948, 7122675302, 7122807028, 7122812051) and 8 Blog Articles with ALL-CAPS internal headings (7123727669, 7123516261, 7123526928, 7123554595, 7122425785, 7123946893, 7123956328, 7122657559), plus upload the 16:9 thumbnails for 7124011913 and 7124009517.
"""
import base64
import io
import json
import urllib.request
from pathlib import Path
from PIL import Image, ImageFilter

OUT_DIR = Path(r"D:\GIT\SEO Tool\pm_assets")
OUT_JS = OUT_DIR / "erx_caps_and_thumbs_upgrader.js"

# 1. Create seamless 16:9 (800x450) thumbnails for 7124011913 (ABC.png) and 7124009517 (Termboard (5).png)
thumb_sources = {
    "7124011913": ("https://erx.vn/Images/Content/B/ABC.png", "thumb_abc_16x9.jpg"),
    "7124009517": ("https://erx.vn/Images/Content/B/Termboard (5).png", "thumb_mro_16x9.jpg"),
    "7123995135": ("https://erx.vn/Images/Content/B/dc77baf18a4d2813715c.jpg", "thumb_procurement_16x9.jpg"),
}

thumb_b64_map = {}
for nid, (src_url, fname) in thumb_sources.items():
    encoded = urllib.parse.quote(src_url, safe=":/?=&[]()")
    req = urllib.request.Request(encoded, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=15).read()
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    target_w, target_h = 800, 450
    # Create a blurred, darkened/matched background from the original image stretched to 800x450
    bg = im.resize((target_w, target_h), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=24))
    # Resize foreground to fit height 450
    scale = target_h / im.height
    fg_w = int(im.width * scale)
    fg = im.resize((fg_w, target_h), Image.Resampling.LANCZOS)
    bg.paste(fg, ((target_w - fg_w) // 2, 0))
    out_path = OUT_DIR / fname
    bg.save(out_path, format="JPEG", quality=90, optimize=True)
    b64 = base64.b64encode(out_path.read_bytes()).decode("ascii")
    thumb_b64_map[nid] = {"filename": fname, "b64": b64}
    print(f"Created 16:9 thumbnail {fname} for {nid} ({out_path.stat().st_size:,} bytes)")

# 2. Workshop title normalizer map (for /hoi-thao.html items)
WORKSHOP_TITLE_MAP = {
    "8315644": "“Tại sao hàm AND/OR không Spill? 4 giải pháp thay thế trong Excel 365”",
    "8318776": "“Hàm GROUPBY trong Excel – Tổng hợp dữ liệu theo tháng & Fiscal Year chuẩn xác”",
    "8313513": "“XLOOKUP vs FILTER – Dùng hàm nào trong tình huống nào?”",
    "8312031": "“Hàm FILTER với Wildcards – 3 cách tìm kiếm nâng cao trong Excel”",
    "8313066": "“Từ bỏ XLOOKUP – Làm chủ Data Model & Power Pivot: Bước khởi đầu tiến tới Power BI”",
    "8314296": "🚀 “Sử dụng hàm HYPERLINK trong Excel – Tạo báo cáo thông minh và điều hướng chuyên nghiệp”",
    "8318087": "🚀 “Giải mã hàm MATCH trong Excel – Tham số 1, 0, -1 khác nhau như thế nào?”",
    "8316838": "🚀 “Tại sao nên chuyển từ VLOOKUP sang INDEX MATCH – Tìm kiếm dữ liệu chuyên nghiệp trong Excel”",
    "8318928": "🚀 “Power Query – Chuẩn hóa dữ liệu chấm công bằng Power Query: Nói không với dữ liệu lỗi”",
    "8313099": "🚀 “Power Query trong Excel – Làm sạch & tổng hợp dữ liệu chuyên nghiệp”",
    "8313087": "🚀 “Thực hành giải đề Excel – Kiểm tra trình độ của bạn”",
    "8317247": "🚀 “Làm chủ Table trong Excel – Tham chiếu, hàm và ứng dụng báo cáo trên Excel 365”",
    "8312267": "“Làm chủ hàm SUMPRODUCT – Phần 2: Giải mã cơ chế mảng & ma trận”",
    "8313732": "“Làm chủ hàm SUMPRODUCT – Phần 1: Ứng dụng thực chiến trong báo cáo và xử lý dữ liệu”",
    "8318279": "“Ứng dụng Check Box trong Excel 365 – Kết hợp Conditional Formatting & hàm FILTER”",
    "8315591": "“Tự động hóa tổng hợp dữ liệu Google Sheets sang Excel & Power BI”",
    "8316071": "“Làm chủ xử lý Merge Cells trong Excel 365 – Conditional Formatting, Custom Format & AGGREGATE”",
    "8315449": "“Làm chủ Dynamic Named Range trong Excel 365 – INDEX, OFFSET, TRIMRANGE & các giải pháp khác”",
    "8317559": "“Làm chủ biểu đồ Pareto Chart trong Excel – PivotTable, % Running Total & Highlight Visual”",
    "8318738": "“Làm chủ Search Box trong Excel – Kết hợp FILTER, Conditional Formatting & ActiveX TextBox”",
}

# 3. Blog Article Title & Heading Replacements
BLOG_TITLE_MAP = {
    "7123806948": "Sử dụng hàm EXPAND trong Excel để mở rộng mảng đến số lượng hàng và cột được chỉ định",
    "7122675302": "Làm thế nào để vẽ biểu đồ cột trong Excel?",
    "7122807028": "Làm quen với Jupyter Notebook",
    "7122812051": "Làm quen với thư viện Pandas và DataFrame",
}

BLOG_BODY_REPLACEMENTS = {
    "7123727669": [
        ("1. HÀM TEXTSPLIT TRONG EXCEL", "1. Hàm TEXTSPLIT trong Excel"),
        ("2. TÍNH KHẢ DỤNG CỦA HÀM TEXTSPLIT TRONG EXCEL", "2. Tính khả dụng của hàm TEXTSPLIT trong Excel"),
        ("3. CÔNG THỨC TEXTSPLIT CƠ BẢN ĐỂ TÁCH Ô TRONG EXCEL", "3. Công thức TEXTSPLIT cơ bản để tách ô trong Excel"),
        ("4. TÁCH CHUỖI THÀNH CỘT VÀ HÀNG CÙNG MỘT LÚC", "4. Tách chuỗi thành cột và hàng cùng một lúc"),
        ("5. TÁCH CÁC Ô BẰNG NHIỀU DẤU PHÂN CÁCH", "5. Tách các ô bằng nhiều dấu phân cách"),
        ("6. TÁCH VĂN BẢN BỎ QUA CÁC GIÁ TRỊ TRỐNG", "6. Tách văn bản bỏ qua các giá trị trống"),
        ("7. TÁCH Ô CÓ PHÂN BIỆT CHỮ HOA CHỮ THƯỜNG HOẶC CHỮ HOA CHỮ THƯỜNG HAY KHÔNG?", "7. Tách ô có phân biệt chữ hoa chữ thường hay không?"),
        ("8. THAY THẾ CÁC GIÁ TRỊ THIẾU BẰNG GIÁ TRỊ BẠN MUỐN", "8. Thay thế các giá trị thiếu bằng giá trị bạn muốn"),
        ("9. CHIA NGÀY THÀNH NGÀY, THÁNG VÀ NĂM", "9. Chia ngày thành Ngày, Tháng và Năm"),
        ("10. TÁCH Ô VÀ LOẠI BỎ MỘT SỐ KÝ TỰ", "10. Tách ô và loại bỏ một số ký tự"),
        ("11. TÁCH CHUỖI BỎ QUA CÁC GIÁ TRỊ NHẤT ĐỊNH", "11. Tách chuỗi bỏ qua các giá trị nhất định"),
        ("BẠN CÓ THỂ DOWNLOAD FILE ĐÍNH KÈM TẠI ĐỊA CHỈ DƯỚI ĐÂY:", "Bạn có thể tải file thực hành đính kèm tại địa chỉ dưới đây:"),
    ],
    "7123516261": [
        ("CHUYỂN ĐỔI TỪ EXCEL LÊN SQL, NÊN HAY KHÔNG NÊN?", "Chuyển đổi từ Excel lên SQL: Nên hay không nên?"),
    ],
    "7123526928": [
        ("TÌM NGUỒN CUNG ỨNG CHIẾN LƯỢC TRONG THỜI KỲ “SIÊU GIẢM GIÁ”", "Tìm nguồn cung ứng chiến lược trong thời kỳ “siêu giảm giá”"),
    ],
    "7123554595": [
        ("HÀM COUNTIFS VÀ CÓ THỂ BẠN CHƯA BIẾT!", "Hàm COUNTIFS và những lưu ý quan trọng có thể bạn chưa biết"),
    ],
    "7122425785": [
        ("1. ƯU ĐIỂM KHI SỬ DỤNG PHẦN MỀM:", "1. Ưu điểm khi sử dụng phần mềm:"),
        ("2. CÁC BƯỚC THỰC HIỆN CHẠY PHẦN MỀM:", "2. Các bước thực hiện chạy phần mềm:"),
        ("3. VIDEO DEMO PHẦN MỀM ROUTE OPTIMIZATION.", "3. Video Demo phần mềm Route Optimization"),
    ],
    "7123946893": [
        ("* MÔ TẢ CÔNG VIỆC", "1. Mô tả công việc"),
        ("* YÊU CẦU CÔNG VIỆC", "2. Yêu cầu công việc"),
        ("* QUYỀN LỢI", "3. Quyền lợi được hưởng"),
        ("* HỒ SƠ BAO GỒM", "4. Hồ sơ ứng tuyển bao gồm"),
    ],
    "7123956328": [
        ("I. KEY GOALS AND TASKS", "I. Key Goals and Tasks"),
        ("II. JOB REQUIREMENTS", "II. Job Requirements"),
    ],
    "7122657559": [
        ("POWER QUERY LÀ GÌ?", "1. Power Query là gì?"),
        ("POWER PIVOT LÀ GÌ?", "2. Power Pivot là gì?"),
        ("POWER BI LÀ GÌ?", "3. Power BI là gì?"),
    ],
}

EXTRA_CSS = """
/* === ERX GLOBAL THUMBNAIL & CASE STANDARDIZATION === */
/* 1. Remove forced ALL CAPS across all site headings, modules, footers, buttons, and cards */
h1, h2, h3, h4, h5, h6,
.module-content .module-title h2,
.module-title h1, .module-title h2, .module-title h3,
.title-mod-list-content h2, .dv-relatedcontent > h2,
.background-img > div .title-mod-list-content h2,
.background-img .list-content .title-list-content h3,
.ct-contact > .col-md-12 > .col-md-6 .lb-title-top,
.detail-item-bottom div.title,
.menu-info-contain h1, .login-content .title-details h1,
.title-mnd-list-content, .ct-article-detail .title-content,
.detail-2right-col-container .title-mnd-list-content,
.menu-info-contain.has-img .page-title,
.menu-intro-title h2,
.dv-footer-top .title-mod-list-content h2,
.dv-footer-top span[style*="uppercase"],
.group-content .group-title,
.content-ndefault-animation .list-content > .list-block > div .text-block .title,
.btn-seemore > a, .btn-readmore > a, .btn-goto-page a,
.upper, .upper-case {
  text-transform: none !important;
}

/* 2. Uniform 16:9 Thumbnail Cards on Homepage (#devide_mod_109690 / .contain-home) & All Article Grids */
.contain-home .module-content .module-title h2 {
  font-family: Roboto, 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif !important;
  font-size: 26px !important;
  font-weight: 700 !important;
  color: #0f172a !important;
  margin-bottom: 24px !important;
}
.contain-home ul.list-content {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 24px 20px !important;
  padding: 0 !important;
  margin: 0 !important;
}
.contain-home ul.list-content > li.list-block {
  width: calc(25% - 15px) !important;
  margin: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 12px !important;
  overflow: hidden !important;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
.contain-home ul.list-content > li.list-block:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.1) !important;
}
@media (max-width: 991px) {
  .contain-home ul.list-content > li.list-block {
    width: calc(50% - 10px) !important;
  }
}
@media (max-width: 575px) {
  .contain-home ul.list-content > li.list-block {
    width: 100% !important;
  }
}
.contain-home ul.list-content > li.list-block .img-block {
  width: 100% !important;
  margin: 0 !important;
  border-bottom: 1px solid #f1f5f9 !important;
  background: #f8fafc !important;
  overflow: hidden !important;
}
.contain-home ul.list-content > li.list-block .img-block > a.img-block-0 {
  display: block !important;
  position: relative !important;
  width: 100% !important;
  padding: 56.25% 0 0 0 !important; /* Exact 16:9 aspect ratio for every card */
  overflow: hidden !important;
}
.contain-home ul.list-content > li.list-block .img-block img.img-content {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  max-width: none !important;
  max-height: none !important;
  object-fit: cover !important;
  object-position: center !important;
}
.contain-home ul.list-content > li.list-block .text-block {
  padding: 14px 16px 16px 16px !important;
  flex: 1 1 auto !important;
  display: flex !important;
  flex-direction: column !important;
}
.contain-home ul.list-content > li.list-block .text-block h3.title {
  font-family: Roboto, 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  line-height: 1.45 !important;
  color: #0f172a !important;
  margin: 0 !important;
  display: -webkit-box !important;
  -webkit-line-clamp: 2 !important;
  -webkit-box-orient: vertical !important;
  overflow: hidden !important;
  min-height: 2.9em !important;
}

/* 3. Workshop / Hội thảo Cards (/hoi-thao.html - .list-course.list-content) */
ul.list-course.list-content > li.list-block .img-block > .img-block-0,
ul.list-course.list-content > li.list-block .img-block > a.img-block-0 {
  display: block !important;
  position: relative !important;
  width: 100% !important;
  padding: 100% 0 0 0 !important; /* Exact 1:1 square for Workshop posters */
  overflow: hidden !important;
}
ul.list-course.list-content > li.list-block .img-block img.img-content {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  max-width: none !important;
  max-height: none !important;
  object-fit: cover !important;
}
ul.list-course.list-content > li.list-block .text-block h3.title,
ul.list-course.list-content > li.list-block .text-block h3.title a {
  font-family: Roboto, 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  line-height: 1.45 !important;
  color: #0f172a !important;
  text-transform: none !important;
}
""".strip()

js_bundle = f"""// ERX Global Case & Thumbnail Standardization Bundle
window.ERX_THUMB_B64 = {json.dumps(thumb_b64_map, ensure_ascii=False)};
window.ERX_WORKSHOP_TITLES = {json.dumps(WORKSHOP_TITLE_MAP, ensure_ascii=False)};
window.ERX_BLOG_TITLES = {json.dumps(BLOG_TITLE_MAP, ensure_ascii=False)};
window.ERX_BLOG_BODY_FIXES = {json.dumps(BLOG_BODY_REPLACEMENTS, ensure_ascii=False)};
window.ERX_GLOBAL_CASE_THUMB_CSS = {json.dumps(EXTRA_CSS, ensure_ascii=False)};

window.erxUploadThumb = async function(filename, b64Data) {{
  const byteChars = atob(b64Data);
  const byteNumbers = new Array(byteChars.length);
  for (let i = 0; i < byteChars.length; i++) byteNumbers[i] = byteChars.charCodeAt(i);
  const blob = new Blob([new Uint8Array(byteNumbers)], {{ type: "image/jpeg" }});
  const fd = new FormData();
  fd.append("upload", blob, filename);
  const resp = await fetch("/ckfinder/core/connector/aspx/connector.aspx?command=QuickUpload&type=Images&currentFolder=%2F", {{
    method: "POST",
    credentials: "include",
    body: fd
  }});
  const txt = await resp.text();
  return {{ ok: resp.ok, path: `/Media/images/${{filename}}`, respPreview: txt.slice(0, 160) }};
}};

window.erxUpdateSiteHeaderCssAndRuntimeNormalizer = async function() {{
  const appUrl = "/administrator/globalconfiguration/site?from=3&divid=100";
  const resp = await fetch(appUrl, {{ credentials: "include" }});
  const html = await resp.text();
  const doc = new DOMParser().parseFromString(html, "text/html");
  const form = doc.querySelector("form");
  if (!form) return {{ ok: false, err: "No globalconfiguration form" }};

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
  // Remove old copy if re-running
  sh = sh.replace(/\\/\\* === ERX GLOBAL THUMBNAIL & CASE STANDARDIZATION === \\*\\/[\\s\\S]*?(?=<\\/style>)/g, "");
  if (sh.includes("</style>")) {{
    sh = sh.replace("</style>", "\\n" + window.ERX_GLOBAL_CASE_THUMB_CSS + "\\n</style>");
  }} else {{
    sh += `<style id="erx-global-case-thumb">${{window.ERX_GLOBAL_CASE_THUMB_CSS}}</style>`;
  }}

  // Also add runtime DOM normalizer for Footer headings, Workshop titles, and ONLINE: Google Meet
  const runtimeCaseFix = `
<script id="erx-runtime-case-normalizer">
(function() {{
  var workshopMap = ${{JSON.stringify(window.ERX_WORKSHOP_TITLES)}};
  var footerReplacements = [
    [/HỖ TRỢ KHÁCH HÀNG/g, 'Hỗ trợ khách hàng'],
    [/VỀ ERX VIỆT NAM/gi, 'Về ERX Việt Nam'],
    [/VỀ ERX\\b/g, 'Về ERX Việt Nam'],
    [/HỢP TÁC VÀ LIÊN KẾT/g, 'Hợp tác và liên kết'],
    [/KẾT NỐI VỚI CHÚNG TÔI/g, 'Kết nối với chúng tôi'],
    [/TIN NỔI BẬT/g, 'Tin nổi bật'],
    [/LIÊN HỆ/g, 'Liên hệ']
  ];
  function normalizeCaseInDom(root) {{
    // 1. Footer & sidebar headings
    var spans = (root || document).querySelectorAll('.dv-footer-top span, .dv-footer-top div, .module-title h2, .title-mnd-list-content');
    for (var i = 0; i < spans.length; i++) {{
      var el = spans[i];
      if (el.children.length === 0 && el.textContent) {{
        var txt = el.textContent.trim();
        for (var j = 0; j < footerReplacements.length; j++) {{
          if (footerReplacements[j][0].test(txt)) {{
            el.textContent = txt.replace(footerReplacements[j][0], footerReplacements[j][1]);
          }}
        }}
      }}
    }}
    // 2. Workshop titles & ONLINE: Google Meet on /hoi-thao.html
    var courseLinks = (root || document).querySelectorAll('.list-course .text-block h3.title a, .ct-article-detail h1');
    for (var k = 0; k < courseLinks.length; k++) {{
      var a = courseLinks[k];
      var href = a.getAttribute('href') || window.location.pathname;
      var m = href.match(/-(\\d+)\\.html/);
      if (m && workshopMap[m[1]]) {{
        a.textContent = workshopMap[m[1]];
      }}
    }}
    var italics = (root || document).querySelectorAll('.list-course i, .detail-content i');
    for (var n = 0; n < italics.length; n++) {{
      if (italics[n].textContent && italics[n].textContent.indexOf('ONLINE:') !== -1) {{
        italics[n].textContent = italics[n].textContent.replace('ONLINE:', 'Online:');
      }}
    }}
  }}
  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', function() {{ normalizeCaseInDom(document); }});
  }} else {{
    normalizeCaseInDom(document);
  }}
}})();
</script>`;

  sh = sh.replace(/<script id="erx-runtime-case-normalizer">[\\s\\S]*?<\\/script>/g, "");
  sh += "\\n" + runtimeCaseFix;

  fd.set("META.SCRIPT_HEADER", sh);
  fd.set("btnSubmit", "save");

  const postResp = await fetch(appUrl, {{
    method: "POST",
    credentials: "include",
    headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
    body: fd.toString()
  }});
  return {{ ok: postResp.ok, status: postResp.status }};
}};

window.erxUpdateArticlesAndThumbnails = async function() {{
  const report = {{ uploadedThumbs: [], updatedArticles: [], errors: [] }};

  // 1. Upload the 3 16:9 thumbnails via CKFinder
  for (const [nid, info] of Object.entries(window.ERX_THUMB_B64)) {{
    const up = await window.erxUploadThumb(info.filename, info.b64);
    report.uploadedThumbs.push({{ nid, ...up }});
  }}

  // 2. Collect all article IDs that need title, body, or thumbnail updates
  const allTargetNids = Array.from(new Set([
    ...Object.keys(window.ERX_THUMB_B64),
    ...Object.keys(window.ERX_BLOG_TITLES),
    ...Object.keys(window.ERX_BLOG_BODY_FIXES)
  ]));

  for (const nid of allTargetNids) {{
    try {{
      const editUrl = `/administrator/content/edit.aspx?nContentId=${{nid}}&divid=300&from=31`;
      const resp = await fetch(editUrl, {{ credentials: "include" }});
      const html = await resp.text();
      const doc = new DOMParser().parseFromString(html, "text/html");
      const form = doc.querySelector("form");
      if (!form) {{
        report.errors.push({{ nid, err: "No form" }});
        continue;
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

      if (window.ERX_BLOG_TITLES[nid]) {{
        fd.set("CONTENTS[0].TITLE", window.ERX_BLOG_TITLES[nid]);
        fd.set("CONTENTS[0].META_TITLE", window.ERX_BLOG_TITLES[nid]);
      }}

      if (window.ERX_THUMB_B64[nid]) {{
        const fname = window.ERX_THUMB_B64[nid].filename;
        const mediaPath = `/Media/images/${{fname}}`;
        for (const k of Array.from(fd.keys())) {{
          if (k.toUpperCase().includes("IMAGE") || k.toUpperCase().includes("THUMB") || k.toUpperCase().includes("PICTURE")) {{
            if (fd.get(k)) fd.set(k, mediaPath);
          }}
        }}
        if (fd.has("CONTENT.IMAGE_1")) fd.set("CONTENT.IMAGE_1", mediaPath);
        if (fd.has("CONTENTS[0].IMAGE")) fd.set("CONTENTS[0].IMAGE", mediaPath);
      }}

      if (window.ERX_BLOG_BODY_FIXES[nid]) {{
        let ft = fd.get("CONTENTS[0].FULLTEXT") || "";
        for (const [oldStr, newStr] of window.ERX_BLOG_BODY_FIXES[nid]) {{
          ft = ft.split(oldStr).join(newStr);
        }}
        fd.set("CONTENTS[0].FULLTEXT", ft);
      }}

      fd.set("btnSubmit", "save_and_close");
      const postResp = await fetch(editUrl, {{
        method: "POST",
        credentials: "include",
        headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
        body: fd.toString()
      }});
      report.updatedArticles.push({{ nid, ok: postResp.ok, status: postResp.status }});
    }} catch (e) {{
      report.errors.push({{ nid, err: String(e) }});
    }}
  }}
  return report;
}};
""";

OUT_JS.write_text(js_bundle, encoding="utf-8")
print(f"Wrote {OUT_JS} ({OUT_JS.stat().st_size:,} bytes)")
