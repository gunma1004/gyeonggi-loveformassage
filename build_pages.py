import os
import itertools
import urllib.parse

BASE_URL = "https://gyeonggi-loveformassage.netlify.app"
BRAND_NAME = "건마러브"
YOUTUBE_ID = "DxwimcJq3_A"

# 5종 키워드 로테이션 (SEO 중복 방지)
KEYWORD_ROTATION = itertools.cycle([
    "온쉼 마사지",
    "쉼케어 마사지",
    "나이트릴렉스케어 마사지",
    "스테이케어 마사지",
    "딥슬립테라피 마사지"
])

# 6개 업체 풀, 로컬 이미지 경로(/images/shop*.jpg) 및 고유 전화번호
SHOPS_DATA = [
    {
        "name": "퀸즈홈테라피",
        "phone": "0507-1280-3296",
        "desc": "전문 힐러진의 체형 맞춤 피로회복 특화 프로그램 및 천연 에센셜 오일 관리",
        "price": "80,000원부터~",
        "score": "4.9",
        "img": "/images/shop1.jpg"
    },
    {
        "name": "한국미인테라피",
        "phone": "0507-1280-3140",
        "desc": "지친 일상에 맞춤형 피로회복 케어! 베테랑 한국인 테라피스트의 프라이빗 릴렉싱",
        "price": "70,000원부터~",
        "score": "4.9",
        "img": "/images/shop2.jpg"
    },
    {
        "name": "오늘밤테라피",
        "phone": "0507-1280-3199",
        "desc": "선입금 없는 100% 안심 후불제! 타이, 전신아로마 및 VIP 감성힐링 전문",
        "price": "60,000원부터~",
        "score": "4.9",
        "img": "/images/shop3.jpg"
    },
    {
        "name": "주주테라피",
        "phone": "0507-1280-3197",
        "desc": "재방문율 높은 안심 케어! 철저한 위생 관리와 최고급 럭셔리 스웨디시 프로그램",
        "price": "60,000원부터~",
        "score": "4.8",
        "img": "/images/shop4.jpg"
    },
    {
        "name": "기쁨테라피",
        "phone": "0507-1280-3183",
        "desc": "몸과 마음에 활력을 채워주는 세심하고 품격 있는 전신 힐링 테라피",
        "price": "60,000원부터~",
        "score": "4.9",
        "img": "/images/shop5.jpg"
    },
    {
        "name": "미인클럽테라피",
        "phone": "0507-1280-3180",
        "desc": "젊고 세련된 감각의 테라피스트들이 제공하는 스페셜 감성 아로마 테라피",
        "price": "70,000원부터~",
        "score": "4.9",
        "img": "/images/shop6.jpg"
    }
]

REGION_DATA = {
    'seoul': {
        'name': '서울',
        'districts': {
            'gangnam': {'name': '강남구', 'dongs': ['역삼1동', '역삼2동', '개포1동', '개포2동', '청담동', '삼성1동', '삼성2동', '대치1동', '대치2동', '논현1동', '논현2동', '압구정동', '도곡1동', '도곡2동']},
            'seocho': {'name': '서초구', 'dongs': ['서초1동', '서초2동', '서초3동', '서초4동', '잠원동', '반포1동', '반포2동', '방배1동', '방배2동', '양재1동', '양재2동']},
            'songpa': {'name': '송파구', 'dongs': ['잠실본동', '잠실2동', '잠실3동', '방이1동', '방이2동', '송파1동', '송파2동', '석촌동', '삼전동', '가락동', '문정동']},
            'mapo': {'name': '마포구', 'dongs': ['공덕동', '아현동', '도화동', '용강동', '대흥동', '서교동', '합정동', '망원동', '연남동', '상암동']}
        }
    },
    'incheon': {
        'name': '인천',
        'districts': {
            'yeonsu': {'name': '연수구', 'dongs': ['송도1동', '송도2동', '송도3동', '송도4동', '송도5동', '옥련동', '선학동', '연수동', '동춘동']},
            'namdong': {'name': '남동구', 'dongs': ['구월동', '간석동', '만수동', '서창동', '논현동', '논현고잔동']},
            'bupyeong': {'name': '부평구', 'dongs': ['부평동', '산곡동', '청천동', '갈산동', '삼산동', '부개동', '십정동']},
            'seohae': {'name': '서구', 'dongs': ['청라1동', '청라2동', '청라3동', '검암경서동', '연희동', '가정동', '석남동', '가좌동']}
        }
    },
    'gyeonggi': {
        'name': '경기',
        'districts': {
            'suwon_paldal': {'name': '수원시 팔달구', 'dongs': ['인계동', '매산동', '고등동', '화서동', '우만동']},
            'seongnam_bundang': {'name': '성남시 분당구', 'dongs': ['정자동', '서현동', '야탑동', '판교동', '백현동', '삼평동']}
        }
    }
}

HTML_TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="Yeti" content="index,follow,max-image-preview:large">
  <title>{page_title}</title>
  <meta name="description" content="{meta_description}">
  <link rel="canonical" href="{canonical_url}">
  
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{brand}">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{meta_description}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="/images/gallery1.jpg">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "{page_title_h1} - {brand}",
    "description": "{meta_description}",
    "url": "{canonical_url}",
    "priceRange": "60,000원 ~ 180,000원",
    "aggregateRating": {{
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "reviewCount": "158",
      "bestRating": "5",
      "worstRating": "1"
    }}
  }}
  </script>

  <style>
    :root {{
      --bg-dark: #121013;
      --card-bg: #1c181d;
      --card-inner: #151218;
      --card-border: #2c252f;
      --text-main: #f3eff5;
      --text-muted: #9e93a2;
      --accent-pink: #c76f8e;
      --accent-pink-hover: #db7d9e;
      --star-color: #f59e0b;
      --font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", Roboto, "Noto Sans KR", sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background-color: var(--bg-dark); color: var(--text-main); font-family: var(--font-family); line-height: 1.6; }}
    a {{ color: inherit; text-decoration: none; }}
    .wrap {{ max-width: 1040px; margin: 0 auto; padding: 0 16px; }}
    header.top {{ border-bottom: 1px solid var(--card-border); background: rgba(18, 16, 19, 0.96); position: sticky; top: 0; z-index: 100; backdrop-filter: blur(8px); }}
    .header-row {{ display: flex; align-items: center; justify-content: space-between; height: 64px; }}
    .brand {{ font-size: 1.35rem; font-weight: 800; letter-spacing: -0.5px; color: #fff; }}
    .brand span {{ color: var(--accent-pink); }}
    .nav {{ display: flex; gap: 14px; font-size: 0.9rem; font-weight: 600; }}
    .page-head {{ padding: 24px 0 16px; }}
    .breadcrumbs {{ font-size: 0.82rem; color: var(--text-muted); margin-bottom: 8px; }}
    .breadcrumbs a:hover {{ text-decoration: underline; color: var(--accent-pink); }}
    .title-line h1 {{ font-size: 1.75rem; font-weight: 800; margin-bottom: 4px; }}
    .star-summary-bar {{ display: inline-flex; align-items: center; gap: 8px; background: var(--card-inner); border: 1px solid var(--card-border); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; margin-top: 10px; }}
    .star-summary-bar .stars {{ color: var(--star-color); font-weight: bold; }}
    .tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 24px; }}
    .tag {{ background: var(--card-inner); border: 1px solid var(--card-border); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; transition: 0.2s; }}
    .tag:hover {{ border-color: var(--accent-pink); color: #fff; background: var(--accent-pink); }}
    .content-area {{ width: 100%; }}
    .panel {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 24px; margin-bottom: 20px; }}
    .panel h2 {{ font-size: 1.25rem; font-weight: 700; margin-bottom: 16px; color: #fff; }}
    .shop-list {{ display: flex; flex-direction: column; gap: 14px; margin-bottom: 10px; }}
    .shop-card-item {{ background: var(--card-inner); border: 1px solid var(--card-border); border-radius: 12px; padding: 16px; display: flex; gap: 16px; align-items: center; transition: 0.2s; }}
    .shop-card-item:hover {{ border-color: var(--accent-pink); transform: translateY(-2px); }}
    .shop-card-item img {{ width: 120px; height: 120px; object-fit: cover; border-radius: 8px; flex-shrink: 0; }}
    .shop-card-info {{ flex: 1; min-width: 0; }}
    .shop-card-info h3 {{ font-size: 1.1rem; font-weight: 800; color: #fff; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }}
    .shop-card-info p {{ font-size: 0.85rem; color: var(--text-muted); margin-bottom: 10px; line-height: 1.4; }}
    .shop-card-bottom {{ display: flex; justify-content: space-between; align-items: center; }}
    .shop-card-bottom .price {{ color: var(--star-color); font-weight: 800; font-size: 1rem; }}
    .call-btn-mini {{ background: var(--accent-pink); color: #fff; padding: 8px 16px; border-radius: 6px; font-size: 0.85rem; font-weight: bold; }}
    .map-frame, .video-frame {{ width: 100%; height: 320px; border: 0; border-radius: 8px; margin-top: 12px; }}
    footer {{ border-top: 1px solid var(--card-border); padding: 30px 0; text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-top: 40px; }}
    @media (max-width: 768px) {{
      .shop-card-item {{ flex-direction: column; align-items: flex-start; }}
      .shop-card-item img {{ width: 100%; height: 160px; }}
    }}
  </style>
</head>
<body class="design-suwon-layout-04-dark-luxury">
  <header class="top">
    <div class="wrap header-row">
      <a class="brand" href="/">{brand}<span>.</span></a>
      <nav class="nav">
        <a href="/">메인 홈</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <div class="wrap">
      <div class="page-head">
        <div class="breadcrumbs">{breadcrumbs}</div>
        <div class="title-line">
          <h1>{page_title_h1}</h1>
          <p class="page-description">선입금 없는 100% 안심 후불제! {location_title} 베스트 제휴업체 코스와 예약 정보를 확인하세요.</p>
        </div>
        <div class="star-summary-bar">
          <span class="stars">★★★★★ 4.9</span>
          <span>|</span>
          <span>제휴업체 <strong>6개사 공식입점</strong></span>
          <span>|</span>
          <span style="color: #6ee7b7;">선입금 0원 보장</span>
        </div>
      </div>

      {tag_section}

      <div class="content-area">
        <!-- 6곳 추천 제휴업체 목록 -->
        <section class="panel">
          <h2>{location_title} 추천 제휴업체 안내 (6곳)</h2>
          <div class="shop-list">
            {shop_cards_html}
          </div>
        </section>

        <!-- 실시간 고객 리뷰 -->
        <section class="panel">
          <h2>{location_title} 고객 실시간 후기 및 평점</h2>
          <div class="review-score-box" style="background:var(--card-inner); border:1px solid var(--card-border); border-radius:10px; padding:16px; display:flex; align-items:center; justify-content:space-around; margin-bottom:16px; text-align:center;">
            <div>
              <div style="font-size:2rem; font-weight:800; color:var(--star-color);">4.9</div>
              <div style="color:var(--star-color);">★★★★★</div>
              <small style="color:var(--text-muted);">158개 실제 후기 기준</small>
            </div>
            <div style="text-align: left; font-size: 0.85rem; line-height: 1.8;">
              <div>친절도 만족도 <strong style="color:var(--star-color);">5.0</strong> / 5.0</div>
              <div>신속 방문 만족도 <strong style="color:var(--star-color);">4.9</strong> / 5.0</div>
              <div>관리 퀄리티 <strong style="color:var(--star-color);">4.9</strong> / 5.0</div>
            </div>
          </div>
          <div style="background:var(--card-inner); border:1px solid var(--card-border); border-radius:8px; padding:14px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:6px;">
              <strong style="color:#fff;">김*우 고객님</strong>
              <span style="color:var(--star-color); font-weight:bold;">★★★★★ 5.0</span>
            </div>
            <p style="font-size:0.85rem; color:#d1c9d4;">{location_title} 인근인데 25분 만에 오셨네요. 선입금 전혀 없이 관리사분 오셔서 결제하니 너무 안심됩니다.</p>
          </div>
          <div style="background:var(--card-inner); border:1px solid var(--card-border); border-radius:8px; padding:14px;">
            <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:6px;">
              <strong style="color:#fff;">이*진 고객님</strong>
              <span style="color:var(--star-color); font-weight:bold;">★★★★★ 5.0</span>
            </div>
            <p style="font-size:0.85rem; color:#d1c9d4;">추천 보고 예약했는데 정말 힐링 그 자체였습니다. 부드러운 관리 덕분에 꿀잠 잤습니다.</p>
          </div>
        </section>

        <!-- 지도 및 유튜브 영상 -->
        <section class="panel">
          <h2>{location_title} 위치 및 안내 영상</h2>
          <iframe class="map-frame" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={map_query}&output=embed" title="{location_title} 지도"></iframe>
          <iframe class="video-frame" loading="lazy" src="https://www.youtube-nocookie.com/embed/{youtube_id}" title="건마러브 이용 안내 영상" allowfullscreen></iframe>
        </section>
      </div>
    </div>
  </main>

  <footer>
    <div class="wrap">
      <p>© 2026 {brand}. All Rights Reserved.</p>
    </div>
  </footer>
</body>
</html>
"""

def generate_shop_cards(location_name):
    cards = []
    for shop in SHOPS_DATA:
        card = f"""
        <div class="shop-card-item">
          <img src="{shop['img']}" alt="{location_name} {shop['name']}">
          <div class="shop-card-info">
            <h3>{shop['name']} <span style="font-size:0.75rem; color:#f59e0b;">★ {shop['score']}</span></h3>
            <p>{shop['desc']}</p>
            <div class="shop-card-bottom">
              <span class="price">{shop['price']}</span>
              <a class="call-btn-mini" href="tel:{shop['phone']}">예약상담 {shop['phone']}</a>
            </div>
          </div>
        </div>
        """
        cards.append(card)
    return "".join(cards)

def make_page(path, html_content):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

urls = [f"{BASE_URL}/"]

print("경기건마사랑(건마러브) 다중 업체 페이지 생성을 시작합니다...")

for reg_key, reg_val in REGION_DATA.items():
    reg_name = reg_val['name']
    
    # 1. 시/도 페이지
    current_kw = next(KEYWORD_ROTATION)
    reg_dir = os.path.join("region", reg_key)
    reg_url = f"{BASE_URL}/region/{reg_key}/"
    urls.append(reg_url)
    
    p_title = f"{reg_name} 출장 {current_kw} 지역별 업체안내 | {BRAND_NAME}"
    m_desc = f"{reg_name} 출장 힐링케어 마사지 업체와 코스 정보를 주요 지역별로 정리해 {BRAND_NAME} 에서 편리하게 확인할 수 있습니다."
    
    dist_tags = "".join([f'<a class="tag" href="/region/{reg_key}/{d_key}/">{d_val["name"]}</a>' for d_key, d_val in reg_val['districts'].items()])
    tag_html = f'<div class="tags">{dist_tags}</div>'
    
    make_page(reg_dir, HTML_TEMPLATE.format(
        brand=BRAND_NAME, youtube_id=YOUTUBE_ID,
        map_query=urllib.parse.quote(reg_name),
        page_title=p_title,
        page_title_h1=f"{reg_name} 출장 {current_kw}",
        meta_description=m_desc,
        location_title=reg_name,
        canonical_url=reg_url,
        breadcrumbs=f'홈 › <a href="/">지역별</a> › {reg_name}',
        tag_section=tag_html,
        shop_cards_html=generate_shop_cards(reg_name)
    ))
    
    # 2. 구/군 페이지
    for dist_key, dist_val in reg_val['districts'].items():
        dist_name = dist_val['name']
        current_kw = next(KEYWORD_ROTATION)
        dist_dir = os.path.join(reg_dir, dist_key)
        dist_url = f"{BASE_URL}/region/{reg_key}/{dist_key}/"
        urls.append(dist_url)
        
        full_dist_title = f"{reg_name} {dist_name}"
        p_title = f"{full_dist_title} 출장 {current_kw} 지역별 업체안내 | {BRAND_NAME}"
        m_desc = f"{full_dist_title} 출장 힐링케어 마사지 업체와 코스 정보를 주요 지역별로 정리해 {BRAND_NAME} 에서 편리하게 확인할 수 있습니다."
        
        dong_tags = "".join([f'<a class="tag" href="/region/{reg_key}/{dist_key}/{urllib.parse.quote(d)}/">{d}</a>' for d in dist_val['dongs']])
        tag_html = f'<div class="tags">{dong_tags}</div>'
        
        make_page(dist_dir, HTML_TEMPLATE.format(
            brand=BRAND_NAME, youtube_id=YOUTUBE_ID,
            map_query=urllib.parse.quote(full_dist_title),
            page_title=p_title,
            page_title_h1=f"{full_dist_title} 출장 {current_kw}",
            meta_description=m_desc,
            location_title=full_dist_title,
            canonical_url=dist_url,
            breadcrumbs=f'홈 › <a href="/region/{reg_key}/">{reg_name}</a> › {dist_name}',
            tag_section=tag_html,
            shop_cards_html=generate_shop_cards(full_dist_title)
        ))
        
        # 3. 동/읍/면 페이지
        for dong in dist_val['dongs']:
            current_kw = next(KEYWORD_ROTATION)
            dong_dir = os.path.join(dist_dir, dong)
            encoded_dong = urllib.parse.quote(dong)
            dong_url = f"{BASE_URL}/region/{reg_key}/{dist_key}/{encoded_dong}/"
            urls.append(dong_url)
            
            full_dong_title = f"{reg_name} {dist_name} {dong}"
            p_title = f"{full_dong_title} 출장 {current_kw} 지역별 업체안내 | {BRAND_NAME}"
            m_desc = f"{full_dong_title} 출장 힐링케어 마사지 업체와 코스 정보를 주요 지역별로 정리해 {BRAND_NAME} 에서 편리하게 확인할 수 있습니다."
            
            make_page(dong_dir, HTML_TEMPLATE.format(
                brand=BRAND_NAME, youtube_id=YOUTUBE_ID,
                map_query=urllib.parse.quote(full_dong_title),
                page_title=p_title,
                page_title_h1=f"{full_dong_title} 출장 {current_kw}",
                meta_description=m_desc,
                location_title=full_dong_title,
                canonical_url=dong_url,
                breadcrumbs=f'홈 › <a href="/region/{reg_key}/">{reg_name}</a> › <a href="/region/{reg_key}/{dist_key}/">{dist_name}</a> › {dong}',
                tag_section="",
                shop_cards_html=generate_shop_cards(full_dong_title)
            ))

# 4. sitemap.xml 생성
sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    sitemap_xml.append(f"  <url><loc>{u}</loc><priority>0.8</priority></url>")
sitemap_xml.append('</urlset>')

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap_xml))

# 5. robots.txt 생성
with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

print(f"완료! 총 {len(urls)}개 페이지 및 sitemap.xml, robots.txt 생성이 완료되었습니다.")