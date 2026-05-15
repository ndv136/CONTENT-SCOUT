import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai
from datetime import datetime
import time
import os
import sys
from dotenv import load_dotenv

# Fix Cronjob path
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
load_dotenv(env_path)

class ContentScoutMailer:
    """
    Module: Content Scout v1.0 (5-Tier Trend Architecture)
    Schedule: Daily 5:00 AM VN (22:00 UTC)
    Location: GitHub Actions Cloud
    """

    def __init__(self, config: dict):
        self.config = config
        genai.configure(api_key=config['gemini_api_key'])
        self.model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            generation_config={"temperature": 0.3}
        )

    # ==========================================
    # TANG 1: XU HUONG TIM KIEM TOAN CAU
    # ==========================================
    def get_tier1_global_trends(self) -> str:
        print("🔍 Tầng 1: Xu hướng tìm kiếm toàn cầu...")

        raw_text = ""

        # Google Trends US
        us_feed = feedparser.parse("https://trends.google.com/trending/rss?geo=US")
        count = 0
        for entry in us_feed.entries:
            traffic = ""
            for key in entry:
                if 'traffic' in key.lower():
                    traffic = entry[key]
                    break
            raw_text += f"- [US] {entry.title} (Traffic: {traffic}) | Link: {entry.link}\n"
            count += 1
            if count >= 10: break

        # Google Trends Global
        gl_feed = feedparser.parse("https://trends.google.com/trending/rss?geo=US&hours=24")
        count = 0
        for entry in gl_feed.entries:
            title = entry.title
            if title not in raw_text:
                raw_text += f"- [Global] {title} | Link: {entry.link}\n"
                count += 1
            if count >= 5: break

        # Google News: viral trending topics
        gn_feed = feedparser.parse("https://news.google.com/rss/search?q=%22trending%22+OR+%22viral%22+OR+%22going+viral%22+when:24h&hl=en-US&gl=US&ceid=US:en")
        count = 0
        for entry in gn_feed.entries:
            raw_text += f"- [News] {entry.title} | Link: {entry.link}\n"
            count += 1
            if count >= 5: break

        if not raw_text.strip():
            return "<p>Không có xu hướng nổi bật nào hôm nay.</p>"

        prompt = f"""
        Du lieu THO ve XU HUONG TIM KIEM TOAN CAU tu Google Trends va tin tuc 24h qua:
        {raw_text}

        Ban la mot TREND ANALYST chuyen nghiep. Hay:
        1. CHON LOC dung 6 xu huong NONG NHAT va CO GIA TRI NHAT cho nguoi lam noi dung.
        2. UU TIEN: Xu huong lien quan den cong nghe, AI, giai tri, lifestyle, tai chinh — nhung chu de de lam VIDEO/CONTENT.
        3. LOAI BO: The thao chuyen sau, chinh tri noi bo My, tin dia phuong khong ai quan tam.

        YEU CAU TRINH BAY NGHIEM NGAT:
        - KHONG chao hoi, KHONG giai thich loi thoi.
        - Tra ve ma HTML thuan tuy (khong boc trong the ```html) voi dung cau truc sau cho moi muc:
        <div style="margin-bottom: 25px;">
            <h4 style="margin: 0 0 10px 0; color: #E74C3C; font-size: 16px;">[Ten Xu Huong]</h4>
            <ul style="margin: 0 0 12px 0; padding-left: 20px; font-size: 14px; color: #34495E; line-height: 1.5;">
                <li style="margin-bottom: 6px;"><strong>Dang Hot vi:</strong> [Tai sao xu huong nay dang bung no? Phan tich 2-3 cau]</li>
                <li style="margin-bottom: 6px;"><strong>Muc do viral:</strong> [Luong tim kiem/traffic neu co, va danh gia tiem nang lan toa]</li>
                <li style="margin-bottom: 6px;"><strong>Goc noi dung:</strong> [Goi y 1 goc khai thac cu the de lam video/bai viet]</li>
            </ul>
            <a href="[Link]" style="font-size: 13px; color: #E74C3C; text-decoration: none; font-weight: bold; background: #FDEDEC; padding: 4px 8px; border-radius: 4px; display: inline-block;">Xem chi tiet &rarr;</a>
        </div>
        """
        try: return self.model.generate_content(prompt).text.replace('```html', '').replace('```', '').strip()
        except: return "<p>Lỗi xử lý LLM Tầng 1</p>"

    # ==========================================
    # TANG 2: VIRAL VIDEO & SOCIAL MEDIA
    # ==========================================
    def get_tier2_viral_video(self) -> str:
        print("🔍 Tầng 2: Viral Video & Social Media...")

        raw_text = ""
        seen = set()

        # YouTube viral
        yt_feed = feedparser.parse('https://news.google.com/rss/search?q=("youtube+viral"+OR+"youtube+trending"+OR+"tiktok+viral"+OR+"most+watched")+(video+OR+creator+OR+channel)+when:48h&hl=en-US&gl=US&ceid=US:en')
        count = 0
        for entry in yt_feed.entries:
            if entry.title not in seen:
                seen.add(entry.title)
                raw_text += f"- [Viral] {entry.title} | Link: {entry.link}\n"
                count += 1
            if count >= 6: break

        # Social media news
        sm_feed = feedparser.parse('https://news.google.com/rss/search?q=("social+media"+OR+"instagram"+OR+"threads")+(trending+OR+viral+OR+feature+OR+update)+when:48h&hl=en-US&gl=US&ceid=US:en')
        count = 0
        for entry in sm_feed.entries:
            if entry.title not in seen:
                seen.add(entry.title)
                raw_text += f"- [Social] {entry.title} | Link: {entry.link}\n"
                count += 1
            if count >= 5: break

        # Reddit r/youtube
        time.sleep(1)
        ry_feed = feedparser.parse("https://www.reddit.com/r/youtube/hot.rss")
        count = 0
        for entry in ry_feed.entries:
            title = entry.title
            if title not in seen:
                seen.add(title)
                raw_text += f"- [r/youtube] {title} | Link: {entry.link}\n"
                count += 1
            if count >= 4: break

        if not raw_text.strip():
            return "<p>Không có tin viral nổi bật.</p>"

        prompt = f"""
        Du lieu ve VIDEO VIRAL va XU HUONG SOCIAL MEDIA 48h qua:
        {raw_text}

        CHON LOC dung 5 tin/xu huong DANG CHU Y NHAT cho nguoi sang tao noi dung.
        UU TIEN:
        - Video/format dang viral tren YouTube, TikTok
        - Thay doi algorithm, tinh nang moi cua cac nen tang (YouTube, TikTok, Instagram, Threads)
        - Case study creator thanh cong, chien luoc tang views/subs

        YEU CAU TRINH BAY NGHIEM NGAT:
        - KHONG chao hoi, KHONG giai thich loi thoi.
        - Tra ve ma HTML thuan tuy (khong boc trong the ```html) voi dung cau truc sau:
        <div style="margin-bottom: 25px;">
            <h4 style="margin: 0 0 10px 0; color: #8E44AD; font-size: 16px;">[Tieu De]</h4>
            <ul style="margin: 0 0 12px 0; padding-left: 20px; font-size: 14px; color: #34495E; line-height: 1.5;">
                <li style="margin-bottom: 6px;"><strong>Dien bien:</strong> [Tom tat su kien/xu huong 2-3 cau]</li>
                <li style="margin-bottom: 6px;"><strong>Nen tang:</strong> [YouTube/TikTok/Instagram/Threads — va tac dong den creator]</li>
                <li style="margin-bottom: 6px;"><strong>Bai hoc cho Creator:</strong> [Rut ra bai hoc/co hoi gi tu xu huong nay?]</li>
            </ul>
            <a href="[Link]" style="font-size: 13px; color: #8E44AD; text-decoration: none; font-weight: bold; background: #F5EEF8; padding: 4px 8px; border-radius: 4px; display: inline-block;">Xem chi tiet &rarr;</a>
        </div>
        """
        try: return self.model.generate_content(prompt).text.replace('```html', '').replace('```', '').strip()
        except: return "<p>Lỗi xử lý LLM Tầng 2</p>"

    # ==========================================
    # TANG 3: CONTENT STRATEGY & CREATOR ECONOMY
    # ==========================================
    def get_tier3_content_strategy(self) -> str:
        print("🔍 Tầng 3: Content Strategy & Creator Economy...")

        raw_text = ""
        seen = set()
        subs = ['content_marketing', 'NewTubers', 'socialmedia', 'copywriting']

        for sub in subs:
            feed = feedparser.parse(f"https://www.reddit.com/r/{sub}/hot.rss")
            count = 0
            for entry in feed.entries:
                title = entry.title
                combined = (title + " " + entry.get('summary', '')).lower()
                if any(kw in combined for kw in ['strategy', 'tip', 'how', 'guide', 'tool', 'growth', 'viral', 'algorithm', 'monetiz', 'income', 'engagement', 'seo', 'hook', 'thumbnail']):
                    if title not in seen:
                        seen.add(title)
                        raw_text += f"- [r/{sub}] {title} | Link: {entry.link}\n"
                        count += 1
                if count >= 3: break
            time.sleep(1)

        # Content marketing news
        cm_feed = feedparser.parse('https://news.google.com/rss/search?q=("content+marketing"+OR+"creator+economy"+OR+"youtube+strategy"+OR+"content+creation")+(tips+OR+guide+OR+strategy)+when:3d&hl=en-US&gl=US&ceid=US:en')
        count = 0
        for entry in cm_feed.entries:
            if entry.title not in seen:
                seen.add(entry.title)
                raw_text += f"- [News] {entry.title} | Link: {entry.link}\n"
                count += 1
            if count >= 5: break

        if not raw_text.strip():
            return "<p>Không có chiến lược nội dung mới.</p>"

        prompt = f"""
        Du lieu ve CHIEN LUOC NOI DUNG & CREATOR ECONOMY tu Reddit va tin tuc:
        {raw_text}

        CHON LOC dung 4 bai viet/chien luoc CO GIA TRI THUC TIEN NHAT.
        UU TIEN:
        - Chien luoc tang growth (subscribers, views, engagement)
        - Meo hook, thumbnail, SEO, algorithm hack
        - Cach kiem tien tu noi dung (monetization, sponsorship, affiliate)
        - Xu huong dinh dang moi (Shorts, Reels, long-form, podcast)

        LOAI BO: Bai ban hang, spam, bai qua chung chung khong co insight cu the.

        YEU CAU TRINH BAY NGHIEM NGAT:
        - KHONG chao hoi, KHONG giai thich loi thoi.
        - Tra ve ma HTML thuan tuy (khong boc trong the ```html) voi dung cau truc sau:
        <div style="margin-bottom: 25px;">
            <h4 style="margin: 0 0 10px 0; color: #E67E22; font-size: 16px;">[Tieu De Bai Viet/Chien Luoc]</h4>
            <ul style="margin: 0 0 12px 0; padding-left: 20px; font-size: 14px; color: #34495E; line-height: 1.5;">
                <li style="margin-bottom: 6px;"><strong>Insight chinh:</strong> [Tom tat gia tri cot loi cua bai viet 2-3 cau]</li>
                <li style="margin-bottom: 6px;"><strong>Ap dung ngay:</strong> [1 buoc cu the co the lam ngay hom nay]</li>
                <li style="margin-bottom: 6px;"><strong>Danh cho:</strong> [YouTuber/TikToker/Blogger/Marketer — va level nao]</li>
            </ul>
            <a href="[Link]" style="font-size: 13px; color: #E67E22; text-decoration: none; font-weight: bold; background: #FEF5E7; padding: 4px 8px; border-radius: 4px; display: inline-block;">Doc ngay &rarr;</a>
        </div>
        """
        try: return self.model.generate_content(prompt).text.replace('```html', '').replace('```', '').strip()
        except: return "<p>Lỗi xử lý LLM Tầng 3</p>"

    # ==========================================
    # TANG 4: XU HUONG VIET NAM
    # ==========================================
    def get_tier4_vietnam_trends(self) -> str:
        print("🔍 Tầng 4: Xu hướng Việt Nam...")

        raw_text = ""
        seen = set()

        # Google Trends VN
        vn_feed = feedparser.parse("https://trends.google.com/trending/rss?geo=VN")
        count = 0
        for entry in vn_feed.entries:
            raw_text += f"- [GoogleTrends VN] {entry.title} | Link: {entry.link}\n"
            seen.add(entry.title)
            count += 1
            if count >= 10: break

        # VnExpress hot
        vne_feed = feedparser.parse("https://vnexpress.net/rss/tin-noi-bat.rss")
        count = 0
        for entry in vne_feed.entries:
            title = entry.title
            if title not in seen:
                seen.add(title)
                raw_text += f"- [VnExpress] {title} | Link: {entry.link}\n"
                count += 1
            if count >= 5: break

        # Tuoi Tre
        tto_feed = feedparser.parse("https://tuoitre.vn/rss/tin-moi-nhat.rss")
        count = 0
        for entry in tto_feed.entries:
            title = entry.title
            if title not in seen:
                seen.add(title)
                raw_text += f"- [TuoiTre] {title} | Link: {entry.link}\n"
                count += 1
            if count >= 5: break

        if not raw_text.strip():
            return "<p>Không có xu hướng VN nổi bật.</p>"

        prompt = f"""
        Du lieu ve XU HUONG va TIN TUC HOT tai VIET NAM hom nay:
        {raw_text}

        Ban la TREND ANALYST chuyen ve thi truong Viet Nam. Hay:
        1. CHON LOC dung 5 xu huong/chu de NONG NHAT ma nguoi lam noi dung tai VN co the khai thac.
        2. UU TIEN: Xu huong giai tri, doi song, cong nghe, tai chinh ca nhan, scandal/drama, su kien van hoa — nhung gi NGUOI VIET dang ban tan nhieu nhat.
        3. LOAI BO: Tin the thao chuyen sau, tin hanh chinh nham chan.

        QUAN TRONG: Giu nguyen tieng Viet, KHONG dich sang tieng Anh.

        YEU CAU TRINH BAY NGHIEM NGAT:
        - KHONG chao hoi, KHONG giai thich loi thoi.
        - Tra ve ma HTML thuan tuy (khong boc trong the ```html) voi dung cau truc sau:
        <div style="margin-bottom: 25px;">
            <h4 style="margin: 0 0 10px 0; color: #1ABC9C; font-size: 16px;">[Ten Xu Huong/Chu De]</h4>
            <ul style="margin: 0 0 12px 0; padding-left: 20px; font-size: 14px; color: #34495E; line-height: 1.5;">
                <li style="margin-bottom: 6px;"><strong>Dang hot vi:</strong> [Tai sao nguoi Viet dang quan tam? 2-3 cau]</li>
                <li style="margin-bottom: 6px;"><strong>Goc khai thac:</strong> [Goi y 1 goc lam noi dung cho YouTube/TikTok VN]</li>
                <li style="margin-bottom: 6px;"><strong>Doi tuong:</strong> [Khach hang/khan gia muc tieu]</li>
            </ul>
            <a href="[Link]" style="font-size: 13px; color: #1ABC9C; text-decoration: none; font-weight: bold; background: #E8F8F5; padding: 4px 8px; border-radius: 4px; display: inline-block;">Xem chi tiet &rarr;</a>
        </div>
        """
        try: return self.model.generate_content(prompt).text.replace('```html', '').replace('```', '').strip()
        except: return "<p>Lỗi xử lý LLM Tầng 4</p>"

    # ==========================================
    # TANG 5: GOI Y NOI DUNG AI (Synthesis)
    # ==========================================
    def get_tier5_content_ideas(self, t1: str, t2: str, t3: str, t4: str) -> str:
        print("🔍 Tầng 5: Gợi ý nội dung AI...")

        # Extract text from HTML for context (strip tags roughly)
        import re
        def strip_html(html):
            return re.sub('<[^<]+?>', '', html)[:1500]

        context = f"""
        XU HUONG TOAN CAU: {strip_html(t1)}
        VIDEO VIRAL: {strip_html(t2)}
        CHIEN LUOC CONTENT: {strip_html(t3)}
        XU HUONG VIET NAM: {strip_html(t4)}
        """

        prompt = f"""
        Ban la mot CONTENT STRATEGIST hang dau. Dua tren TOAN BO du lieu xu huong sau:
        {context}

        Hay TONG HOP va DE XUAT dung 5 Y TUONG NOI DUNG cu the, co the bat tay lam ngay hom nay.

        Moi y tuong PHAI co:
        1. Tieu de video/bai viet hap dan (click-worthy nhung khong clickbait)
        2. Dinh dang tot nhat (YouTube long-form, Shorts, TikTok, Blog, Thread X)
        3. Dan y ngan gon (3-4 bullet points ve noi dung chinh)
        4. Doi tuong muc tieu va tiem nang views

        UU TIEN y tuong:
        - Ket hop nhieu xu huong voi nhau (trend mashup)
        - Co goc nhin doc dao, khong ai lam
        - Phu hop voi kenh YouTube/TikTok ve Cong nghe, AI, Doi song, Tai chinh

        QUAN TRONG: 3 y tuong dau bang Tieng Viet (cho thi truong VN), 2 y tuong cuoi bang Tieng Anh (cho thi truong quoc te).

        YEU CAU TRINH BAY NGHIEM NGAT:
        - KHONG chao hoi, KHONG giai thich loi thoi.
        - Tra ve ma HTML thuan tuy (khong boc trong the ```html) voi dung cau truc sau:
        <div style="margin-bottom: 25px; border-left: 3px solid #3498DB; padding-left: 15px;">
            <h4 style="margin: 0 0 10px 0; color: #2C3E50; font-size: 16px;">[So thu tu]. [Tieu de Video/Bai viet]</h4>
            <ul style="margin: 0 0 12px 0; padding-left: 20px; font-size: 14px; color: #34495E; line-height: 1.5;">
                <li style="margin-bottom: 6px;"><strong>Dinh dang:</strong> [YouTube/Shorts/TikTok/Blog/Thread]</li>
                <li style="margin-bottom: 6px;"><strong>Dan y:</strong> [3-4 bullets ve noi dung chinh]</li>
                <li style="margin-bottom: 6px;"><strong>Doi tuong:</strong> [Target audience + estimated tiem nang]</li>
                <li style="margin-bottom: 6px;"><strong>Tai sao lam NGAY:</strong> [Tinh cap thiet — xu huong nay se het hot khi nao?]</li>
            </ul>
        </div>
        """
        try: return self.model.generate_content(prompt).text.replace('```html', '').replace('```', '').strip()
        except: return "<p>Lỗi xử lý LLM Tầng 5</p>"

    # ==========================================
    # DONG GOI EMAIL
    # ==========================================
    def send_email_report(self, t1: str, t2: str, t3: str, t4: str, t5: str):
        print("✉️ Đang đóng gói và gửi Email...")
        sender_email = self.config['sender_email']
        receiver_email = self.config['receiver_email']
        app_password = self.config['gmail_app_password']

        all_receivers = [receiver_email]
        receivers_str = ", ".join(all_receivers)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receivers_str
        today_str = datetime.now().strftime("%d/%m/%Y")
        msg['Subject'] = f"[Content Scout 5:00 AM] Xu Hướng & Ý Tưởng Nội Dung - {today_str}"

        html_body = f"""
        <html>
            <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1C2833; line-height: 1.6; max-width: 800px; margin: auto;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2C3E50; margin-bottom: 5px;">CONTENT SCOUT</h1>
                    <p style="color: #7F8C8D; font-size: 13px; margin-top: 0;">{today_str} | Xu hướng & Ý tưởng nội dung mới nhất</p>
                </div>

                <h2 style="color: #E74C3C; border-bottom: 1px solid #FDEDEC; padding-bottom: 5px; font-size: 18px;">TẦNG 1: XU HƯỚNG TÌM KIẾM TOÀN CẦU</h2>
                <p style="font-size: 12px; color: #7F8C8D; margin-top: 2px;">Google Trends US/Global + Tin viral 24h</p>
                <div style="padding: 10px 0;">
                    {t1}
                </div>

                <h2 style="color: #8E44AD; border-bottom: 1px solid #F5EEF8; padding-bottom: 5px; font-size: 18px; margin-top: 30px;">TẦNG 2: VIRAL VIDEO & SOCIAL MEDIA</h2>
                <p style="font-size: 12px; color: #7F8C8D; margin-top: 2px;">YouTube, TikTok, Instagram, Threads — 48h qua</p>
                <div style="padding: 10px 0;">
                    {t2}
                </div>

                <h2 style="color: #E67E22; border-bottom: 1px solid #FEF5E7; padding-bottom: 5px; font-size: 18px; margin-top: 30px;">TẦNG 3: CONTENT STRATEGY & CREATOR ECONOMY</h2>
                <p style="font-size: 12px; color: #7F8C8D; margin-top: 2px;">Reddit + Tin tức content marketing</p>
                <div style="padding: 10px 0;">
                    {t3}
                </div>

                <h2 style="color: #1ABC9C; border-bottom: 1px solid #E8F8F5; padding-bottom: 5px; font-size: 18px; margin-top: 30px;">TẦNG 4: XU HƯỚNG VIỆT NAM</h2>
                <p style="font-size: 12px; color: #7F8C8D; margin-top: 2px;">Google Trends VN + VnExpress + Tuổi Trẻ</p>
                <div style="padding: 10px 0;">
                    {t4}
                </div>

                <h2 style="color: #3498DB; border-bottom: 1px solid #EBF5FB; padding-bottom: 5px; font-size: 18px; margin-top: 30px;">TẦNG 5: GỢI Ý NỘI DUNG AI</h2>
                <p style="font-size: 12px; color: #7F8C8D; margin-top: 2px;">5 ý tưởng nội dung từ AI — bắt tay làm ngay hôm nay</p>
                <div style="padding: 10px 0;">
                    {t5}
                </div>

                <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #EEE; text-align: center;">
                    <p style="font-size: 11px; color: #BDC3C7;">Content Scout Mailer v1.0 (5-Tier Trend Architecture) - GitHub Actions Cloud</p>
                </div>
            </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
            server.quit()
            print("✅ ĐÃ GỬI EMAIL THÀNH CÔNG!")
        except Exception as e:
            print(f"Loi gui email: {str(e)}")
            sys.exit(1)

    def run_daily_scout(self):
        print("=== BẮT ĐẦU CHẠY CONTENT SCOUT 5 TẦNG ===")
        t1 = self.get_tier1_global_trends()
        t2 = self.get_tier2_viral_video()
        t3 = self.get_tier3_content_strategy()
        t4 = self.get_tier4_vietnam_trends()
        t5 = self.get_tier5_content_ideas(t1, t2, t3, t4)
        self.send_email_report(t1, t2, t3, t4, t5)
        print("=== HOÀN TẤT ===")

if __name__ == "__main__":
    CONFIG = {
        'gemini_api_key': os.getenv("GEMINI_API_KEY"),
        'sender_email': os.getenv("SENDER_EMAIL"),
        'receiver_email': os.getenv("RECEIVER_EMAIL"),
        'gmail_app_password': os.getenv("GMAIL_APP_PASSWORD")
    }

    if CONFIG['gmail_app_password'] and CONFIG['gemini_api_key']:
        scout = ContentScoutMailer(CONFIG)
        scout.run_daily_scout()
    else:
        print("⚠️ LỖI: Không đọc được secrets! Kiểm tra GitHub Repository Secrets.")
        sys.exit(1)
