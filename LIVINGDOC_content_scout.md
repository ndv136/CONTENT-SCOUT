# LIVING DOCUMENTATION: CONTENT SCOUT MAILER v1.0

> **Status:** PRODUCTION  
> **Last Updated:** 2026-05-15  
> **Version:** v1.0 (5-Tier Trend Architecture)  
> **Git Repo:** `github.com/ndv136/CONTENT-SCOUT.git`  
> **Schedule:** Daily 5:00 AM VN (22:00 UTC)

---

## ORIGIN & VISION

- **Vision:** Founder nhan email moi sang 5h — toan canh xu huong noi dung toan cau + Viet Nam + 5 y tuong content lam ngay. Zero-Touch.
- **Complementary to:** AI Radar Mailer (4:00 AM) — AI Radar = cong cu & tin cong nghe, Content Scout = xu huong & y tuong noi dung.

---

## TONG QUAN KIEN TRUC

### File Structure

```
CONTENT-SCOUT-/
├── .github/workflows/daily_scout.yml   <- Cron scheduler (5:00 AM VN)
├── content_scout_mailer.py             <- Core engine (class ContentScoutMailer)
├── requirements.txt                    <- feedparser, google-generativeai, python-dotenv
├── .env                                <- Local secrets (gitignored)
├── .gitignore
└── LIVINGDOC_content_scout.md          <- (File nay)
```

### Class Method Map

| # | Method | Chuc nang | LLM |
|---|---|---|---|
| 1 | `__init__()` | Setup Gemini Flash (temp 0.3) | — |
| 2 | `get_tier1_global_trends()` | Tang 1: 6 xu huong toan cau | 1 |
| 3 | `get_tier2_viral_video()` | Tang 2: 5 tin viral video/social | 1 |
| 4 | `get_tier3_content_strategy()` | Tang 3: 4 chien luoc content | 1 |
| 5 | `get_tier4_vietnam_trends()` | Tang 4: 5 xu huong VN | 1 |
| 6 | `get_tier5_content_ideas(t1-t4)` | Tang 5: 5 y tuong AI (synthesis) | 1 |
| 7 | `send_email_report(t1..t5)` | Dong goi & gui email | — |
| 8 | `run_daily_scout()` | Orchestrator | — |
| | **TOTAL** | | **5 LLM calls/run** |

### Deployment

| Thuoc tinh | Chi tiet |
|---|---|
| **Workflow** | `.github/workflows/daily_scout.yml` |
| **Schedule** | `cron '0 22 * * *'` UTC = **5:00 AM VN** |
| **Manual** | `workflow_dispatch` |
| **Runner** | `ubuntu-latest`, Python 3.10 |
| **LLM** | Gemini Flash (`gemini-flash-latest`, temp 0.3) |
| **Email** | Gmail SMTP (port 587, TLS, App Password) |

### Secrets (GitHub Repository -> Settings -> Secrets)

| Secret Name | Env Var |
|---|---|
| `GEMINI_KEY` | `GEMINI_API_KEY` |
| `SENDER` | `SENDER_EMAIL` |
| `RECEIVER` | `RECEIVER_EMAIL` |
| `GMAIL_APP_PASSWORD` | `GMAIL_APP_PASSWORD` |

---

## KIEN TRUC 5 TANG

### Pipeline Flow

```
GitHub Actions Cron (22:00 UTC = 5:00 AM VN)
    |
    v
run_daily_scout()
    |
    |-> T1: get_tier1_global_trends()      -> Gemini -> 6 trends (HTML)
    |-> T2: get_tier2_viral_video()        -> Gemini -> 5 viral (HTML)
    |-> T3: get_tier3_content_strategy()   -> Gemini -> 4 strategies (HTML)
    |-> T4: get_tier4_vietnam_trends()     -> Gemini -> 5 VN trends (HTML)
    |-> T5: get_tier5_content_ideas(t1-t4) -> Gemini -> 5 ideas (HTML)
    |
    v
send_email_report(t1, t2, t3, t4, t5)
    |
    v
Gmail SMTP -> Inbox
```

### Tang 1: XU HUONG TIM KIEM TOAN CAU (Do)

| Thuoc tinh | Chi tiet |
|---|---|
| **Mau** | `#E74C3C` |
| **Max items** | 6 |
| **Sources** | Google Trends US, Google Trends Global, Google News (viral/trending) |
| **Uu tien** | Cong nghe, AI, giai tri, lifestyle, tai chinh |
| **Loai bo** | The thao chuyen sau, chinh tri noi bo My, tin dia phuong |
| **Output/item** | Dang Hot vi -> Muc do viral -> Goc noi dung |

### Tang 2: VIRAL VIDEO & SOCIAL MEDIA (Tim)

| Thuoc tinh | Chi tiet |
|---|---|
| **Mau** | `#8E44AD` |
| **Max items** | 5 |
| **Sources** | Google News (YouTube/TikTok viral), Google News (social media), Reddit r/youtube |
| **Uu tien** | Video viral, algorithm changes, creator case studies |
| **Output/item** | Dien bien -> Nen tang -> Bai hoc cho Creator |

### Tang 3: CONTENT STRATEGY & CREATOR ECONOMY (Cam)

| Thuoc tinh | Chi tiet |
|---|---|
| **Mau** | `#E67E22` |
| **Max items** | 4 |
| **Sources** | Reddit (r/content_marketing, r/NewTubers, r/socialmedia, r/copywriting), Google News (content marketing) |
| **Keywords** | strategy, tip, how, guide, tool, growth, viral, algorithm, monetiz, income, engagement, seo, hook, thumbnail |
| **Output/item** | Insight chinh -> Ap dung ngay -> Danh cho |

### Tang 4: XU HUONG VIET NAM (Xanh ngoc)

| Thuoc tinh | Chi tiet |
|---|---|
| **Mau** | `#1ABC9C` |
| **Max items** | 5 |
| **Sources** | Google Trends VN, VnExpress (tin noi bat), Tuoi Tre (tin moi nhat) |
| **Uu tien** | Giai tri, doi song, cong nghe, tai chinh, scandal/drama, su kien van hoa |
| **Output** | Giu nguyen **tieng Viet** |
| **Output/item** | Dang hot vi -> Goc khai thac -> Doi tuong |

### Tang 5: GOI Y NOI DUNG AI — Synthesis (Xanh duong)

| Thuoc tinh | Chi tiet |
|---|---|
| **Mau** | `#3498DB` |
| **Max items** | 5 y tuong (3 tieng Viet + 2 tieng Anh) |
| **Source** | AI tong hop tu T1-T4 (strip HTML, lay 1500 chars moi tang) |
| **Uu tien** | Trend mashup, goc doc dao, phu hop kenh YouTube/TikTok |
| **Output/item** | Dinh dang -> Dan y -> Doi tuong -> Tai sao lam NGAY |

---

## RSS SOURCE REGISTRY (10+ feeds)

| Source | URL | Tang |
|---|---|---|
| Google Trends US | `trends.google.com/trending/rss?geo=US` | T1 |
| Google Trends Global | `trends.google.com/trending/rss?geo=US&hours=24` | T1 |
| Google News (viral) | `trending OR viral OR going viral when:24h` | T1 |
| Google News (YouTube viral) | `youtube viral OR tiktok viral when:48h` | T2 |
| Google News (social media) | `social media trending OR feature when:48h` | T2 |
| Reddit r/youtube | `reddit.com/r/youtube/hot.rss` | T2 |
| Reddit r/content_marketing | `reddit.com/r/content_marketing/hot.rss` | T3 |
| Reddit r/NewTubers | `reddit.com/r/NewTubers/hot.rss` | T3 |
| Reddit r/socialmedia | `reddit.com/r/socialmedia/hot.rss` | T3 |
| Reddit r/copywriting | `reddit.com/r/copywriting/hot.rss` | T3 |
| Google News (content marketing) | `content marketing OR creator economy when:3d` | T3 |
| Google Trends VN | `trends.google.com/trending/rss?geo=VN` | T4 |
| VnExpress | `vnexpress.net/rss/tin-noi-bat.rss` | T4 |
| Tuoi Tre | `tuoitre.vn/rss/tin-moi-nhat.rss` | T4 |

---

## EMAIL OUTPUT SPECIFICATION

### Subject
```
[Content Scout 5:00 AM] Xu Huong & Y Tuong Noi Dung - DD/MM/YYYY
```

### Body Sections

| # | Title | Color | Border |
|---|---|---|---|
| 1 | TANG 1: XU HUONG TIM KIEM TOAN CAU | `#E74C3C` | `#FDEDEC` |
| 2 | TANG 2: VIRAL VIDEO & SOCIAL MEDIA | `#8E44AD` | `#F5EEF8` |
| 3 | TANG 3: CONTENT STRATEGY & CREATOR ECONOMY | `#E67E22` | `#FEF5E7` |
| 4 | TANG 4: XU HUONG VIET NAM | `#1ABC9C` | `#E8F8F5` |
| 5 | TANG 5: GOI Y NOI DUNG AI | `#3498DB` | `#EBF5FB` |

### Footer
```
Content Scout Mailer v1.0 (5-Tier Trend Architecture) - GitHub Actions Cloud
```

---

## VERSION HISTORY

| Version | Date | Changes |
|---|---|---|
| **v1.0** | **2026-05-15** | **Initial release: 5-tier, 14 RSS, 5 LLM calls** |
