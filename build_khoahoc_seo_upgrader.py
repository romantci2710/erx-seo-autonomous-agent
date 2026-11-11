# -*- coding: utf-8 -*-
"""Builds pm_assets/khoahoc_seo_upgrader.js — 1-click Hoola Admin Console SEO Upgrader for khoahoc.erx.vn.

Covers all 29 URLs on khoahoc.erx.vn:
  1. Homepage (/) via Settings.methods.getAppSetting -> Settings.methods.updateAppSetting
  2. 15 Courses (/course/*) via Courses.methods.getAllCourses -> getCourseEdit -> updateCourseInfoGeneral & updateCourseDescription
  3. 10 Child Pages (/p/*, including all 9 'undefined' pages) via Pages.methods.getPageTable -> getChildPageGrapeJs -> updateChildPageGrapeJS
  4. 3 Instructors (/instructor/*) via Instructors.methods.getInstructorTable -> getInstructor -> updateInstructor
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_JS = ROOT / "pm_assets" / "khoahoc_seo_upgrader.js"

KHOAHOC_HOME_SEO = {
    "url": "https://khoahoc.erx.vn/",
    "title": "ERX E-Learning — Khóa học Excel 365, Power BI, SQL & SCM",
    "meta_desc": "Học viện trực tuyến ERX E-Learning: đào tạo thực chiến Excel 365, VBA, Power Query, Power BI, SQL, Python và Quản trị Chuỗi cung ứng cho doanh nghiệp.",
}

KHOAHOC_COURSES_SEO = {
    "python-for-supply-chain": {
        "title": "Python cho Chuỗi cung ứng (Supply Chain) Thực chiến | ERX",
        "meta_desc": "Khóa học Python cho Supply Chain thực chiến tại ERX: xử lý dữ liệu lớn bằng Pandas, tự động hóa báo cáo tồn kho, dự báo nhu cầu và tối ưu hóa vận hành.",
    },
    "python-crash-course": {
        "title": "Python cơ bản thực chiến cho Phân tích dữ liệu mới bắt đầu",
        "meta_desc": "Khóa học Python cơ bản miễn phí cho người mới bắt đầu tại ERX: nắm vững cú pháp, cấu trúc dữ liệu, hàm xử lý bảng biểu và nền tảng phân tích dữ liệu.",
    },
    "master-power-query": {
        "title": "Master Power Query: Tự động hóa làm sạch & gộp dữ liệu | ERX",
        "meta_desc": "Làm chủ Power Query trong Excel & Power BI: tự động kết nối nhiều file/folder, chuẩn hóa bảng tính lộn xộn và làm mới báo cáo quản trị chỉ với 1 cú nhấp.",
    },
    "lam-quen-voi-power-query-trong-excel": {
        "title": "Làm quen Power Query trong Excel: Chuẩn hóa dữ liệu tự động",
        "meta_desc": "Khóa học nhập môn Power Query trong Microsoft Excel miễn phí từ ERX: hướng dẫn gộp file, tách cột, Unpivot và tự động hóa quy trình làm sạch dữ liệu.",
    },
    "finance-bi-mastery-bctc-powerbi": {
        "title": "Finance BI Mastery: Báo cáo tài chính trên Power BI | ERX",
        "meta_desc": "Xây dựng hệ thống Báo cáo tài chính (P&L, Balance Sheet, Cash Flow) tự động trên Power BI: thiết kế Data Model chuẩn, DAX tài chính và phân tích biến động.",
    },
    "import-xay-dung-data-model-dashboard-bctc-power-bi": {
        "title": "Xây dựng Data Model & Dashboard Báo cáo tài chính Power BI",
        "meta_desc": "Hướng dẫn thực hành Import dữ liệu, thiết kế Star Schema Data Model và trực quan hóa Dashboard Báo cáo tài chính chuyên nghiệp trên Microsoft Power BI.",
    },
    "data-analyst-learning-path": {
        "title": "Lộ trình Data Analyst thực chiến: Excel, SQL, Power BI | ERX",
        "meta_desc": "Lộ trình đào tạo Phân tích dữ liệu (Data Analyst) toàn diện tại ERX Việt Nam: kết hợp Excel 365, Power Query, SQL, Power BI DAX và Python cho doanh nghiệp.",
    },
    "master-excel-from-a-to-z": {
        "title": "Master Excel từ A đến Z: Hàm tra cứu, Pivot & Báo cáo | ERX",
        "meta_desc": "Làm chủ Microsoft Excel từ nền tảng đến chuyên sâu: hệ thống hàm tính toán, dò tìm nâng cao, PivotTable và thiết kế Dashboard báo cáo quản trị tự động.",
    },
    "master-excel-365": {
        "title": "Master Excel 365: Hàm mảng động XLOOKUP, FILTER, LAMBDA | ERX",
        "meta_desc": "Bứt phá hiệu suất với các hàm mảng động thế hệ mới trên Excel 365 (XLOOKUP, FILTER, SORT, UNIQUE, LET, LAMBDA, GROUPBY) tự động hóa bảng tính doanh nghiệp.",
    },
    "master-vba": {
        "title": "Master Excel VBA: Tự động hóa báo cáo, UserForm & SQL | ERX",
        "meta_desc": "Khóa học lập trình VBA trong Excel thực chiến: tự động hóa xử lý file hàng loạt, kết nối SQL qua ADODB, gửi email Outlook và xây dựng ứng dụng UserForm.",
    },
    "fast-track-to-power-bi": {
        "title": "Fast Track to Power BI: Thiết kế Dashboard & DAX nhanh | ERX",
        "meta_desc": "Khóa học Power BI tăng tốc cho người đi làm: chuẩn hóa dữ liệu với Power Query, xây dựng Data Model, viết hàm DAX cốt lõi và xuất bản Dashboard quản trị.",
    },
    "master-new-excel-365-function": {
        "title": "Làm chủ hệ thống hàm mới trên Microsoft Excel 365 | ERX",
        "meta_desc": "Thực hành chuyên sâu nhóm hàm mảng động và xử lý văn bản mới trên Excel 365 (TEXTSPLIT, VSTACK, HSTACK, CHOOSECOLS, WRAPROWS) giải quyết bài toán thực tế.",
    },
    "khoa-hoc-chuyen-vien-mua-hang-hands-on-procurement": {
        "title": "Khóa học Chuyên viên Mua hàng thực chiến (Procurement) | ERX",
        "meta_desc": "Đào tạo nghiệp vụ Mua hàng B2B (Hands-on Procurement) thực chiến: tìm nguồn cung, chấm điểm nhà cung cấp, phân tích chi phí TCO, đàm phán và quản lý hợp đồng.",
    },
    "how-to-become-a-procurement-manager": {
        "title": "How to Become a Procurement Manager — Quản trị Mua hàng | ERX",
        "meta_desc": "Chương trình phát triển năng lực Quản lý Mua sắm (Procurement Manager): chiến lược Category Management, Strategic Sourcing, quản trị rủi ro và tối ưu Saving.",
    },
    "operation-research-show-case-day-04": {
        "title": "Operations Research Showcase Day 04: Tối ưu hóa chuỗi cung ứng",
        "meta_desc": "Chuyên đề Operations Research ứng dụng trong Chuỗi cung ứng & Logistics: mô hình quy hoạch tuyến tính, bài toán phân bổ nguồn lực và tối ưu chi phí vận tải.",
    },
}

KHOAHOC_PAGES_SEO = {
    "giang-vien": {
        "title": "Đội ngũ Giảng viên Chuyên gia Phân tích Dữ liệu & SCM | ERX",
        "meta_desc": "Đội ngũ giảng viên thực chiến tại ERX E-Learning: các chuyên gia quản lý dữ liệu, tài chính và chuỗi cung ứng giàu kinh nghiệm tại tập đoàn đa quốc gia.",
    },
    "chinh-sach-bao-mat": {
        "title": "Chính sách bảo mật thông tin học viên — Học viện ERX Việt Nam",
        "meta_desc": "Quy định thu thập, lưu trữ và bảo mật thông tin cá nhân của học viên khi đăng ký và tham gia các khóa học trực tuyến trên nền tảng khoahoc.erx.vn của ERX.",
    },
    "dieu-khoan-dich-vu": {
        "title": "Điều khoản dịch vụ & Quy chế sử dụng nền tảng ERX E-Learning",
        "meta_desc": "Điều khoản dịch vụ, quyền lợi và trách nhiệm của học viên khi truy cập tài liệu, video bài giảng và hệ thống thực hành trực tuyến tại học viện khoahoc.erx.vn.",
    },
    "quy-dinh-ve-thanh-toan": {
        "title": "Quy định thanh toán học phí & Kích hoạt khóa học | ERX Academy",
        "meta_desc": "Hướng dẫn các phương thức thanh toán học phí chuyển khoản, xuất hóa đơn doanh nghiệp và quy trình kích hoạt tài khoản học trực tuyến tự động tại ERX Việt Nam.",
    },
    "tro-giup": {
        "title": "Trung tâm Trợ giúp & Hướng dẫn học trực tuyến | ERX E-Learning",
        "meta_desc": "Giải đáp câu hỏi thường gặp, hướng dẫn đăng nhập, tải file bài tập Excel/Power BI và kênh hỗ trợ kỹ thuật trực tiếp cho học viên trên hệ thống khoahoc.erx.vn.",
    },
    "trang-chu": {
        "title": "Giới thiệu hệ thống đào tạo trực tuyến thực chiến ERX Academy",
        "meta_desc": "Tổng quan nền tảng học trực tuyến ERX E-Learning: lộ trình học tập cá nhân hóa về Excel 365, Power BI, SQL, Python và Quản trị Chuỗi cung ứng thực chiến.",
        "recommended_status": "unpublished",
    },
    "gift": {
        "title": "Quà tặng Tài liệu & Khóa học miễn phí từ Học viện ERX Việt Nam",
        "meta_desc": "Nhận bộ quà tặng biểu mẫu Excel quản trị, tài liệu hướng dẫn Power BI, SQL và các khóa học nền tảng miễn phí dành riêng cho cộng đồng học viên ERX Việt Nam.",
    },
    "landingpage": {
        "title": "Chương trình Đào tạo Phân tích Dữ liệu & Chuỗi cung ứng | ERX",
        "meta_desc": "Đăng ký lộ trình nâng cao năng lực Phân tích dữ liệu kinh doanh và Quản trị chuỗi cung ứng thực chiến cùng đội ngũ chuyên gia tại Học viện ERX Việt Nam.",
        "recommended_status": "unpublished",
    },
    "workshop": {
        "title": "Chuỗi Workshop Thực chiến Data Analytics & Supply Chain | ERX",
        "meta_desc": "Tổng hợp lịch sự kiện và tài liệu chuỗi Workshop trực tuyến chuyên sâu về Excel 365, Power Query, Power BI, Python và Tối ưu hóa Chuỗi cung ứng tại ERX.",
    },
    "operations-research-showcase-day-02": {
        "title": "Workshop Operations Research Showcase Day 02: Tối ưu vận hành",
        "meta_desc": "Tài liệu và video Workshop Operations Research Showcase Day 02 tại ERX: giải quyết bài toán tối ưu hóa kế hoạch sản xuất, tồn kho và mạng lưới phân phối.",
    },
}

KHOAHOC_INSTRUCTORS_SEO = {
    "hoang-trung": {
        "title": "Giảng viên Hoàng Trung — Chuyên gia Data Analytics & BI | ERX",
        "meta_desc": "Giảng viên Hoàng Trung tại ERX E-Learning: chuyên gia đào tạo thực chiến Excel 365, Power Query, Power BI và xây dựng hệ thống báo cáo quản trị doanh nghiệp.",
    },
    "nguyen-minh-ngoc": {
        "title": "Giảng viên Nguyễn Minh Ngọc — Chuyên gia Supply Chain & Data",
        "meta_desc": "Giảng viên Nguyễn Minh Ngọc tại ERX Việt Nam: chuyên gia Quản trị Chuỗi cung ứng, Mua sắm chiến lược (Procurement), tối ưu hóa vận hành và phân tích dữ liệu.",
    },
    "giang-vien-operation-research": {
        "title": "Đội ngũ Giảng viên Operations Research & Tối ưu hóa | ERX",
        "meta_desc": "Nhóm chuyên gia giảng dạy Operations Research tại ERX Việt Nam: ứng dụng mô hình toán tối ưu và Python giải quyết bài toán Logistics, kho vận và sản xuất.",
    },
}


def lookup_khoahoc_curated_seo(url: str) -> dict[str, str] | None:
    """Return curated {title, meta_desc} for a known khoahoc.erx.vn URL, or None."""
    clean = url.split("?", 1)[0].rstrip("/")
    if clean in ("https://khoahoc.erx.vn", "http://khoahoc.erx.vn"):
        return {"title": KHOAHOC_HOME_SEO["title"], "meta_desc": KHOAHOC_HOME_SEO["meta_desc"]}
    for prefix, table in (
        ("https://khoahoc.erx.vn/course/", KHOAHOC_COURSES_SEO),
        ("https://khoahoc.erx.vn/p/", KHOAHOC_PAGES_SEO),
        ("https://khoahoc.erx.vn/instructor/", KHOAHOC_INSTRUCTORS_SEO),
    ):
        if clean.startswith(prefix):
            slug = clean[len(prefix):]
            if slug in table:
                return {"title": table[slug]["title"], "meta_desc": table[slug]["meta_desc"]}
    return None


def build_upgrader_js() -> str:
    payload = {
        "home": KHOAHOC_HOME_SEO,
        "courses": KHOAHOC_COURSES_SEO,
        "pages": KHOAHOC_PAGES_SEO,
        "instructors": KHOAHOC_INSTRUCTORS_SEO,
    }
    return f"""// ERX E-Learning (khoahoc.erx.vn) — 1-Click Hoola Admin Console SEO Upgrader
// Usage: Log in to https://khoahoc.erx.vn/manage, open DevTools Console, paste this file, and run:
//   await window.erxRunAllKhoahocSeoUpgrades();
window.ERX_KHOAHOC_SEO_PAYLOAD = {json.dumps(payload, ensure_ascii=False, indent=2)};

window.erxMeteorCall = function(method, args) {{
  return new Promise(function(resolve, reject) {{
    if (typeof Meteor === "undefined" || typeof Meteor.call !== "function") {{
      return reject(new Error("Meteor is not available — run this inside https://khoahoc.erx.vn/manage"));
    }}
    Meteor.call(method, args, function(err, res) {{
      if (err) {{
        const detail = (err && (err.reason || err.details || err.message || err.error)) || JSON.stringify(err);
        reject(new Error(method + ": " + detail));
      }} else {{
        resolve(res);
      }}
    }});
  }});
}};

// 1. Update Homepage SEO via Settings.methods.getAppSetting -> updateAppSetting
window.erxUpgradeKhoahocHomeSeo = async function() {{
  try {{
    const cur = await window.erxMeteorCall("Settings.methods.getAppSetting", {{}});
    if (!cur) return {{ ok: false, err: "No app setting returned" }};
    const seoConfigInfo = Object.assign({{}}, cur.seoConfigInfo || {{}}, {{
      title: window.ERX_KHOAHOC_SEO_PAYLOAD.home.title,
      description: window.ERX_KHOAHOC_SEO_PAYLOAD.home.meta_desc
    }});
    const payload = {{
      faviconInfo: cur.faviconInfo || {{}},
      colorInfo: cur.colorInfo || {{}},
      languageInfo: cur.languageInfo || {{}},
      seoConfigInfo: seoConfigInfo,
      fontInfo: cur.fontInfo || {{}}
    }};
    if (cur._id) payload.itemId = String(cur._id);
    await window.erxMeteorCall("Settings.methods.updateAppSetting", payload);
    return {{ ok: true, title: seoConfigInfo.title }};
  }} catch (e) {{
    return {{ ok: false, err: String(e && e.message || e) }};
  }}
}};

// 2. Update all 10 /p/* Child Pages (fixes all 9 'undefined' titleSEO/descriptionSEO pages)
window.erxUpgradeKhoahocPagesSeo = async function(options) {{
  const unpublishPlaceholders = !!(options && options.unpublishPlaceholders);
  const results = {{ updated: [], skipped: [], errors: [] }};
  let rows = [];
  try {{
    const table = await window.erxMeteorCall("Pages.methods.getPageTable", {{
      status: "all",
      limit: 100,
      pageIndex: 1
    }});
    rows = (table && (table.data || table.items || table.pages || table.rows)) || (Array.isArray(table) ? table : []);
  }} catch (e) {{
    results.errors.push({{ stage: "getPageTable", err: String(e && e.message || e) }});
    return results;
  }}

  for (const row of rows) {{
    const slug = (row.slug || (row.info && row.info.slug) || "").trim();
    const itemId = String(row._id || row.itemId || "");
    const seo = window.ERX_KHOAHOC_SEO_PAYLOAD.pages[slug];
    if (!itemId || !seo) {{
      results.skipped.push({{ slug, itemId }});
      continue;
    }}
    try {{
      let gjs = null;
      try {{
        gjs = await window.erxMeteorCall("Pages.methods.getChildPageGrapeJs", {{ itemId }});
      }} catch (_ignore) {{
        gjs = null;
      }}
      if (gjs) {{
        const src = (gjs.publishedPage && gjs.publishedPage.html) ? gjs.publishedPage : ((gjs.draftPage && gjs.draftPage.html) ? gjs.draftPage : gjs);
        const topComponents = gjs.components || (src && src.components) || [];
        // 1) Classic Builder (isNewBuilder: false) SSR reads top-level titleSEO & descriptionSEO (only written when pagePublishMode is omitted)
        await window.erxMeteorCall("Pages.methods.updateChildPageGrapeJS", {{
          itemId: itemId,
          html: gjs.html || (src && src.html) || "",
          css: gjs.css || (src && src.css) || "",
          js: gjs.js || (src && src.js) || "",
          components: typeof topComponents === "string" ? topComponents : JSON.stringify(topComponents),
          titleSEO: seo.title,
          descriptionSEO: seo.meta_desc,
          imageSEO: (gjs.imageSEO && gjs.imageSEO !== "undefined") ? String(gjs.imageSEO) : "",
          showConfig: gjs.showConfig || (src && src.showConfig) || {{}}
        }});
        // 2) New Builder (isNewBuilder: true) SSR reads publishedPage.titleSEO & publishedPage.descriptionSEO (written when pagePublishMode === "published")
        const pubComponents = (src && src.components) || gjs.components || [];
        await window.erxMeteorCall("Pages.methods.updateChildPageGrapeJS", {{
          itemId: itemId,
          html: (src && src.html) || gjs.html || "",
          css: (src && src.css) || gjs.css || "",
          twcss: (src && src.twcss) || gjs.twcss || "",
          js: (src && src.js) || gjs.js || "",
          components: typeof pubComponents === "string" ? pubComponents : JSON.stringify(pubComponents),
          titleSEO: seo.title,
          descriptionSEO: seo.meta_desc,
          imageSEO: (gjs.imageSEO && gjs.imageSEO !== "undefined") ? String(gjs.imageSEO) : "",
          showConfig: (src && src.showConfig) || gjs.showConfig || {{}},
          pagePublishMode: "published",
          status: (unpublishPlaceholders && seo.recommended_status) ? seo.recommended_status : (gjs.status || "published")
        }});
      }} else {{
        const simple = await window.erxMeteorCall("Pages.methods.getChildPage", {{ itemId }});
        const simpleInfo = (simple && simple.info) || simple || {{}};
        try {{
          await window.erxMeteorCall("Pages.methods.updateChildPageGrapeJS", {{
            itemId: itemId,
            titleSEO: seo.title,
            descriptionSEO: seo.meta_desc
          }});
          await window.erxMeteorCall("Pages.methods.updateChildPageGrapeJS", {{
            itemId: itemId,
            titleSEO: seo.title,
            descriptionSEO: seo.meta_desc,
            pagePublishMode: "published",
            status: (unpublishPlaceholders && seo.recommended_status) ? seo.recommended_status : "published"
          }});
        }} catch (_ignoreGjs) {{}}
        const updSimple = {{ name: seo.title, slug: slug }};
        if (typeof simpleInfo.content === "string") updSimple.content = simpleInfo.content;
        await window.erxMeteorCall("Pages.methods.updateChildPage", {{
          itemId: itemId,
          info: updSimple
        }});
      }}
      results.updated.push(slug);
    }} catch (e) {{
      results.errors.push({{ slug, err: String(e && e.message || e) }});
    }}
  }}
  return results;
}};

// 3. Update all 15 /course/* Courses & Learning Paths (title 50-65 chars & headline/meta_desc 140-160 chars, preserving slug)
window.erxUpgradeKhoahocCoursesSeo = async function() {{
  const results = {{ updated: [], skipped: [], errors: [] }};
  const byId = new Map();

  const productSpecs = [
    {{ table: "productsCourse", productType: "COURSE" }},
    {{ table: "productsPath", productType: "PATH" }},
    {{ table: "productsBundle", productType: "BUNDLE" }},
    {{ table: "productsMembership", productType: "MEMBERSHIP" }}
  ];
  for (const spec of productSpecs) {{
    try {{
      const tResp = await window.erxMeteorCall("Courses.methods.getProductTable", {{
        table: spec.table,
        fixedQuery: {{ productType: spec.productType }},
        status: "all",
        limit: 100,
        pageIndex: 1
      }});
      const tRows = (tResp && (tResp.data || tResp.items || tResp.rows || tResp.courses)) || (Array.isArray(tResp) ? tResp : []);
      for (const r of tRows) {{
        const id = String(r._id || r.courseId || "");
        if (id && !byId.has(id)) byId.set(id, r);
      }}
    }} catch (e) {{
      results.errors.push({{ stage: spec.table, err: String(e && e.message || e) }});
    }}
  }}

  try {{
    const rep = await window.erxMeteorCall("Courses.methods.getCoursesForReport", {{}});
    const repRows = (rep && (rep.data || rep.courses || rep.items || rep.rows)) || (Array.isArray(rep) ? rep : []);
    for (const r of repRows) {{
      const id = String(r._id || r.courseId || "");
      if (id && !byId.has(id)) byId.set(id, r);
    }}
  }} catch (_ignore) {{}}

  for (const [courseId, row] of byId.entries()) {{
    try {{
      const detail = await window.erxMeteorCall("Courses.methods.getCourseEdit", {{ courseId }});
      const c = (detail && (detail.course || detail)) || row;
      const slug = String(c.slug || row.slug || "").trim();
      const seo = window.ERX_KHOAHOC_SEO_PAYLOAD.courses[slug];
      if (!seo) {{
        results.skipped.push({{ slug, courseId }});
        continue;
      }}
      const genObj = {{
        title: seo.title,
        slug: String(c.slug || slug),
        instructor: Array.isArray(c.instructor) ? c.instructor.map(String) : [],
        topic: c.topic ? String(c.topic) : "",
        category: Array.isArray(c.category) ? c.category.map(String) : [],
        label: c.label ? String(c.label) : "",
        duration: c.duration != null ? String(c.duration) : ""
      }};
      if (c.required_membership_tier) genObj.required_membership_tier = String(c.required_membership_tier);
      if (c.membership_tier) genObj.membership_tier = String(c.membership_tier);

      await window.erxMeteorCall("Courses.methods.updateCourseInfoGeneral", {{
        courseId: courseId,
        courseObj: genObj
      }});

      const mapPairs = (arr) => Array.isArray(arr)
        ? arr.map((x) => ({{ title: (x && x.title) ? String(x.title) : "", content: (x && x.content) ? String(x.content) : "" }}))
        : [];
      const mapHighlights = (arr) => Array.isArray(arr)
        ? arr.map((x) => ({{ content: (x && x.content) ? String(x.content) : String(x || "") }}))
        : [];

      const descObj = {{
        headline: seo.meta_desc,
        use_combo_headline: !!c.use_combo_headline,
        combo_headline: c.combo_headline ? String(c.combo_headline) : "",
        bundle_highlights: mapHighlights(c.bundle_highlights),
        include: mapPairs(c.include),
        purpose: mapPairs(c.purpose),
        target_audience: mapPairs(c.target_audience),
        requirement: c.requirement ? String(c.requirement) : "",
        description: c.description ? String(c.description) : ""
      }};
      if (Array.isArray(c.course_related)) descObj.course_related = c.course_related.map(String);

      await window.erxMeteorCall("Courses.methods.updateCourseDescription", {{
        courseId: courseId,
        courseObj: descObj
      }});
      results.updated.push(slug);
    }} catch (e) {{
      results.errors.push({{ courseId, err: String(e && e.message || e) }});
    }}
  }}
  return results;
}};

// 4. Update all 3 /instructor/* Profiles (fixes 'undefined' & short meta descriptions)
window.erxUpgradeKhoahocInstructorsSeo = async function() {{
  const results = {{ updated: [], skipped: [], errors: [] }};
  let rows = [];
  try {{
    const table = await window.erxMeteorCall("Instructors.methods.getInstructorTable", {{
      status: "all",
      limit: 100,
      pageIndex: 1
    }});
    rows = (table && (table.data || table.items || table.instructors || table.rows)) || (Array.isArray(table) ? table : []);
  }} catch (e) {{
    results.errors.push({{ stage: "getInstructorTable", err: String(e && e.message || e) }});
    return results;
  }}

  for (const row of rows) {{
    const slug = (row.slug || (row.info && row.info.slug) || "").trim();
    const itemId = String(row._id || row.itemId || "");
    const seo = window.ERX_KHOAHOC_SEO_PAYLOAD.instructors[slug];
    if (!itemId || !seo) {{
      results.skipped.push({{ slug, itemId }});
      continue;
    }}
    try {{
      const cur = await window.erxMeteorCall("Instructors.methods.getInstructor", {{ itemId }});
      const info = (cur && (cur.info || cur)) || row.info || row;
      const updInfo = {{
        name: seo.title,
        slug: String(info.slug || slug),
        email: (info.email && info.email !== "undefined") ? String(info.email) : "info@erx.vn",
        title: (info.title && info.title !== "undefined") ? String(info.title) : "Giảng viên Chuyên gia ERX Việt Nam",
        description: seo.meta_desc,
        biography: (info.biography && info.biography !== "undefined") ? String(info.biography) : seo.meta_desc,
        images: info.images || {{}}
      }};
      if (info.linkedUserId) updInfo.linkedUserId = String(info.linkedUserId);
      await window.erxMeteorCall("Instructors.methods.updateInstructor", {{
        itemId: itemId,
        info: updInfo
      }});
      results.updated.push(slug);
    }} catch (e) {{
      results.errors.push({{ slug, err: String(e && e.message || e) }});
    }}
  }}
  return results;
}};

window.erxRunAllKhoahocSeoUpgrades = async function(options) {{
  const home = await window.erxUpgradeKhoahocHomeSeo();
  const pages = await window.erxUpgradeKhoahocPagesSeo(options);
  const courses = await window.erxUpgradeKhoahocCoursesSeo();
  const instructors = await window.erxUpgradeKhoahocInstructorsSeo();
  return {{ home, pages, courses, instructors }};
}};
""".strip() + "\n"


def main() -> None:
    OUT_JS.parent.mkdir(parents=True, exist_ok=True)
    js_code = build_upgrader_js()
    OUT_JS.write_text(js_code, encoding="utf-8")
    print(f"Wrote {OUT_JS} ({OUT_JS.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
