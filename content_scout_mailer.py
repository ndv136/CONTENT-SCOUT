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
    # TẦNG 1: TIN TỨC AI & CÔNG NGHỆ TOÀN CẦU
    # ==========================================
    def get_tier1_ai_news(self) -> str:
        print("🔍 Tầng 1: Tin tức AI & Công nghệ toàn cầu...")

        raw_text = ""
        seen = set()

        ai_feeds = [
            ("https://news.google.com/rss/search?q=(\"artificial+intelligence\"+OR+\"AI\"+OR+\"machine+learning\"+OR+\"LLM\"+OR+\"GPT\"+OR+\"Gemini\"+OR+\"Claude\")+(launch+OR+release+OR+update+OR+breakthrough)+when:24h&hl=en-US&gl=US&ceid=US:en", "Google News AI", 8),
            ("https://news.google.com/rss/search?q=(\"OpenAI\"+OR+\"Google+AI\"+OR+\"Anthropic\"+OR+\"Meta+AI\"+OR+\"Midjourney\"+OR+\"Stability+AI\")+when:48h&hl=en-US&gl=US&ceid=US:en", "AI Companies", 5),
            ("https://news.google.com/rss/search?q=(\"generative+AI\"+OR+\"AI+agent\"+OR+\"AI+automation\"+OR+\"AI+coding\")+when:48h&hl=en-US&gl=US&ceid=US:en", "GenAI News", 5),
        ]

        for url, label, max_items in ai_feeds:
            feed = feedparser.parse(url)
            count = 0
            for entry in feed.entries:
                if entry.title not in seen:
                    seen.add(entry.title)
                    raw_text += f"- [{label}] {entry.title} | Link: {entry.link}\n"
                    count += 1
                if count >= max_items: break

        # Reddit AI subs
        for sub in ['artificial', 'MachineLearning']:
            feed = feedparser.parse(f"https://www.reddit.com/r/{sub}/hot.rss")
            count = 0
            for entry in feed.entries:
                if entry.title not in seen:
                    seen.add(entry.title)
                    raw_text += f"- [r/{sub}] {entry.title} | Link: {entry.link}\n"
                    count += 1
                if count >= 3: break
            time.sleep(1)

        if not raw_text.strip():
            return "<p>Không có tin AI nổi bật nào hôm nay.</p>"

        prompt = f"""
        Dữ liệu THÔ về TIN TỨC AI & CÔNG NGHỆ toàn cầu 24-48h qua:
        {raw_text}

        Bạn là một AI ANALYST chuyên nghiệp. Hãy:
        1. CHỌN LỌC đúng 6 tin AI QUAN TRỌNG NHẤT và CÓ GIÁ TRỊ NHẤT.
        2. ƯU TIÊN: Ra mắt model mới, công cụ AI mới, thay đổi lớn từ OpenAI/Google/Anthropic/Meta, breakthrough nghiên cứu, ứng dụng AI thực tế.
        3. LOẠI BỎ: Tin trùng lặp, tin PR không có giá trị, tin quá chuyên sâu academic.

        YÊU CẦU TRÌNH BÀY NGHIÊM NGẶT:
        - KHÔNG chào hỏi, KHÔNG giải thích lời thừa.
        - Trả về mã HTML thuần túy (không bọc trong thẻ ```html) với đúng cấu trúc sau cho mỗi mục:
        <div style="margin-bottom: 25px;">
            <h4 style="margin: 0 0 10px 0; color: #E74C3C; font-size: 16px;">[Tên Tin Tức]</h4>
            <ul style="margin: 0 0 12px 0; padding-left: 20px; font-size: 14px; color: #34495E; line-height: 1.5;">
                <li style="margin-bottom: 6px;"><strong>Đang Hot vì:</strong> [Tại sao tin này quan trọng? 2-3 câu]</li>
                <li style="margin-bottom: 6px;"><strong>Mức độ ảnh hưởng:</strong> [Tác động đến ngành AI/tech/người dùng]</li>
                <li style="margin-bottom: 6px;"><strong>Góc nội dung:</strong> [Gợi ý 1 góc khai thác cụ thể để làm video/bài viết]</li>
            </ul>
            <a href="[Link]" style="font-size: 13px; color: #E74C3C; text-decoration: none; font-weight: bold; background: #FDEDEC; padding: 4px 8px; border-radius: 4px; display: inline-block;">Xem chi tiết &rarr;</a>
        </div>
        """
        try: return self.model.generate_content(prompt).text.replace('```html', '').replace('```', '').strip()
        except: return "<p>Lỗi xử lý LLM Tầng 1</p>"

    # ==========================================
    # TẦNG 2: CÔNG CỤ AI & SẢN PHẨM MỚI
    # ==========================================
    def get_tier2_ai_tools(self) -> str:
        print("🔍 Tầng 2: Công cụ AI & Sản phẩm mới...")

        raw_text = ""
        seen = set()

        tool_feeds = [
            ('https://news.google.com/rss/search?q=("AI+tool"+OR+"AI+app"+OR+"AI+platform"+OR+"AI+startup")+(launch+OR+new+OR+free+OR+update)+when:48h&hl=en-US&gl=US&ceid=US:en', "AI Tools", 6),
            ('https://news.google.com/rss/search?q=("ChatGPT"+OR+"Copilot"+OR+"Gemini"+OR+"Claude"+OR+"Perplexity"+OR+"Cursor")+(feature+OR+update+OR+plugin)+when:48h&hl=en-US&gl=US&ceid=US:en', "AI Products", 5),
        ]

        for url, label, max_items in tool_feeds:
            feed = feedparser.parse(url)
            count = 0
            for entry in feed.entries:
                if entry.title not in seen:
                    seen.add(entry.title)
                    raw_text += f"- [{label}] {entry.title} | Link: {entry.link}\n"
                    count += 1
                if count >= max_items: break

        # Reddit AI tools
        for sub in ['ChatGPT', 'singularity', 'ArtificialIntelligence']:
            feed = feedparser.parse(f"https://www.reddit.com/r/{sub}/hot.rss")
            count = 0
            for entry in feed.entries:
                if entry.title not in seen:
                    seen.add(entry.title)
                    raw_text += f"- [r/{sub}] {entry.title} | Link: {entry.link}\n"
                    count += 1
                if count >= 3: break
            time.sleep(1)

        if not raw_text.strip():
            return "<p>Không có công cụ AI mới nổi bật.</p>"

        prompt = f"""
        Dữ liệu về CÔNG CỤ AI & SẢN PHẨM MỚI 48h qua:
        {raw_text}

        CHỌN LỌC đúng 5 công cụ/sản phẩm AI ĐÁNG CHÚ Ý NHẤT.
        ƯU TIÊN:
        - Công cụ AI mới ra mắt hoặc cập nhật lớn
        - AI tool miễn phí hoặc có free tier hữu ích
        - Tính năng mới của ChatGPT, Gemini, Claude, Copilot
        - AI cho content creation (viết, vẽ, video, nhạc)

        YÊU CẦU TRÌNH BÀY NGHIÊM NGẶT:
        - KHÔNG chào hỏi, KHÔNG giải thích lời thừa.
        - Trả về mã HTML thuần túy (không bọc trong thẻ ```html) với đúng cấu trúc sau:
        <div style="margin-bottom: 25px;">
            <h4 style="margin: 0 0 10px 0; color: #8E44AD; font-size: 16px;">[Tên Công Cụ/Sản Phẩm]</h4>
            <ul style="margin: 0 0 12px 0; padding-left: 20px; font-size: 14px; color: #34495E; line-height: 1.5;">
                <li style="margin-bottom: 6px;"><strong>Mô tả:</strong> [Công cụ này làm gì? 2-3 câu]</li>
                <li style="margin-bottom: 6px;"><strong>Điểm nổi bật:</strong> [Tính năng đặc biệt, giá, free tier?]</li>
                <li style="margin-bottom: 6px;"><strong>Ứng dụng thực tế:</strong> [Dùng cho việc gì? Ai nên dùng?]</li>
            </ul>
            <a href="[Link]" style="font-size: 13px; color: #8E44AD; text-decoration: none; font-weight: bold; background: #F5EEF8; padding: 4px 8px; border-radius: 4px; display: inline-block;">Xem chi tiết &rarr;</a>
        </div>
        """
        try: return self.model.generate_content(prompt).text.replace('```html', '').replace('```', '').strip()
        except: return "<p>Lỗi xử lý LLM Tầng 2</p>"

    # ==========================================
    # TẦNG 3: AI CHO CONTENT CREATION
    # ==========================================
    def get_tier3_ai_content(self) -> str:
        print("🔍 Tầng 3: AI cho Content Creation...")

        raw_text = ""
        seen = set()

        # AI content creation news
        ai_content_feeds = [
            ('https://news.google.com/rss/search?q=("AI+video"+OR+"AI+writing"+OR+"AI+image"+OR+"AI+music"+OR+"AI+content")+(tool+OR+generator+OR+creator)+when:3d&hl=en-US&gl=US&ceid=US:en', "AI Content", 6),
            ('https://news.google.com/rss/search?q=("Sora"+OR+"Runway"+OR+"Kling"+OR+"ElevenLabs"+OR+"Suno"+OR+"Udio"+OR+"Canva+AI"+OR+"Adobe+AI")+when:3d&hl=en-US&gl=US&ceid=US:en', "AI Creative Tools", 5),
        ]

        for url, label, max_items in ai_content_feeds:
            feed = feedparser.parse(url)
            count = 0
            for entry in feed.entries:
                if entry.title not in seen:
                    seen.add(entry.title)
                    raw_text += f"- [{label}] {entry.title} | Link: {entry.link}\n"
                    count += 1
                if count >= max_items: break

        # Reddit AI content subs
        for sub in ['aivideo', 'StableDiffusion', 'midjourney']:
            feed = feedparser.parse(f"https://www.reddit.com/r/{sub}/hot.rss")
            count = 0
            for entry in feed.entries:
                if entry.title not in seen:
                    seen.add(entry.title)
                    raw_text += f"- [r/{sub}] {entry.title} | Link: {entry.link}\n"
                    count += 1
                if count >= 3: break
            time.sleep(1)

        if not raw_text.strip():
            return "<p>Không có tin AI content mới.</p>"

        prompt = f"""
        Dữ liệu về AI CHO CONTENT CREATION từ tin tức và Reddit:
        {raw_text}

        CHỌN LỌC đúng 4 công cụ/xu hướng AI content CÓ GIÁ TRỊ THỰC TIỄN NHẤT.
        ƯU TIÊN:
        - AI tạo video (Sora, Runway, Kling, Pika)
        - AI tạo hình ảnh (Midjourney, DALL-E, Stable Diffusion, Flux)
        - AI viết nội dung (Claude, GPT, Jasper)
        - AI tạo nhạc/voice (Suno, ElevenLabs, Udio)
        - Workflow AI cho YouTuber/TikToker

        YÊU CẦU TRÌNH BÀY NGHIÊM NGẶT:
        - KHÔNG chào hỏi, KHÔNG giải thích lời thừa.
        - Trả về mã HTML thuần túy (không bọc trong thẻ ```html) với đúng cấu trúc sau:
        <div style="margin-bottom: 25px;">
            <h4 style="margin: 0 0 10px 0; color: #E67E22; font-size: 16px;">[Tên Công Cụ/Xu Hướng]</h4>
            <ul style="margin: 0 0 12px 0; padding-left: 20px; font-size: 14px; color: #34495E; line-height: 1.5;">
                <li style="margin-bottom: 6px;"><strong>Mô tả:</strong> [Công cụ này làm gì? 2-3 câu]</li>
                <li style="margin-bottom: 6px;"><strong>Áp dụng ngay:</strong> [1 bước cụ thể có thể làm ngay hôm nay]</li>
                <li style="margin-bottom: 6px;"><strong>Dành cho:</strong> [YouTuber/TikToker/Blogger/Designer — và level nào]</li>
            </ul>
            <a href="[Link]" style="font-size: 13px; color: #E67E22; text-decoration: none; font-weight: bold; background: #FEF5E7; padding: 4px 8px; border-radius: 4px; display: inline-block;">Xem chi tiết &rarr;</a>
        </div>
        """
        try: return self.model.generate_content(prompt).text.replace('```html', '').replace('```', '').strip()
        except: return "<p>Lỗi xử lý LLM Tầng 3</p>"

    # ==========================================
    # TẦNG 4: AI & TECH VIỆT NAM
    # ==========================================
    def get_tier4_ai_vietnam(self) -> str:
        print("🔍 Tầng 4: AI & Tech Việt Nam...")

        raw_text = ""
        seen = set()

        # Google News: AI Vietnam
        vn_feeds = [
            ('https://news.google.com/rss/search?q=("AI"+OR+"trí+tuệ+nhân+tạo"+OR+"công+nghệ"+OR+"ChatGPT"+OR+"Gemini")+when:3d&hl=vi&gl=VN&ceid=VN:vi', "AI Việt Nam", 8),
            ('https://news.google.com/rss/search?q=("startup+Việt"+OR+"fintech"+OR+"edtech"+OR+"chuyển+đổi+số")+when:3d&hl=vi&gl=VN&ceid=VN:vi', "Tech VN", 5),
        ]

        for url, label, max_items in vn_feeds:
            feed = feedparser.parse(url)
            count = 0
            for entry in feed.entries:
                if entry.title not in seen:
                    seen.add(entry.title)
                    raw_text += f"- [{label}] {entry.title} | Link: {entry.link}\n"
                    count += 1
                if count >= max_items: break

        # VnExpress Khoa hoc (Science/Tech section)
        vne_feed = feedparser.parse("https://vnexpress.net/rss/khoa-hoc.rss")
        count = 0
        for entry in vne_feed.entries:
            title = entry.title
            if title not in seen:
                seen.add(title)
                raw_text += f"- [VnExpress KH] {title} | Link: {entry.link}\n"
                count += 1
            if count >= 5: break

        if not raw_text.strip():
            return "<p>Không có tin AI/Tech VN nổi bật.</p>"

        prompt = f"""
        Dữ liệu về AI & TECH tại VIỆT NAM:
        {raw_text}

        Bạn là TECH ANALYST chuyên về thị trường Việt Nam. Hãy:
        1. CHỌN LỌC đúng 5 tin AI/Tech NÓNG NHẤT tại VN.
        2. ƯU TIÊN: Ứng dụng AI tại VN, startup công nghệ, chính sách AI, chuyển đổi số, AI trong giáo dục/y tế/tài chính VN.
        3. LOẠI BỎ: Tin không liên quan đến AI/tech.

        QUAN TRỌNG: Viết bằng tiếng Việt có dấu đầy đủ.

        YÊU CẦU TRÌNH BÀY NGHIÊM NGẶT:
        - KHÔNG chào hỏi, KHÔNG giải thích lời thừa.
        - Trả về mã HTML thuần túy (không bọc trong thẻ ```html) với đúng cấu trúc sau:
        <div style="margin-bottom: 25px;">
            <h4 style="margin: 0 0 10px 0; color: #1ABC9C; font-size: 16px;">[Tên Tin/Chủ Đề]</h4>
            <ul style="margin: 0 0 12px 0; padding-left: 20px; font-size: 14px; color: #34495E; line-height: 1.5;">
                <li style="margin-bottom: 6px;"><strong>Đang hot vì:</strong> [Tại sao người Việt đang quan tâm? 2-3 câu]</li>
                <li style="margin-bottom: 6px;"><strong>Góc khai thác:</strong> [Gợi ý 1 góc làm nội dung cho YouTube/TikTok VN]</li>
                <li style="margin-bottom: 6px;"><strong>Đối tượng:</strong> [Khách hàng/khán giả mục tiêu]</li>
            </ul>
            <a href="[Link]" style="font-size: 13px; color: #1ABC9C; text-decoration: none; font-weight: bold; background: #E8F8F5; padding: 4px 8px; border-radius: 4px; display: inline-block;">Xem chi tiết &rarr;</a>
        </div>
        """
        try: return self.model.generate_content(prompt).text.replace('```html', '').replace('```', '').strip()
        except: return "<p>Lỗi xử lý LLM Tầng 4</p>"

    # ==========================================
    # TẦNG 5: TỔNG HỢP & GỢI Ý NỘI DUNG
    # ==========================================
    def get_tier5_content_ideas(self, t1: str, t2: str, t3: str, t4: str) -> str:
        print("🔍 Tầng 5: Tổng hợp & Gợi ý nội dung...")

        import re
        def strip_html(html):
            return re.sub('<[^<]+?>', '', html)[:1500]

        context = f"""
        TIN TỨC AI TOÀN CẦU: {strip_html(t1)}
        CÔNG CỤ AI MỚI: {strip_html(t2)}
        AI CHO CONTENT CREATION: {strip_html(t3)}
        AI & TECH VIỆT NAM: {strip_html(t4)}
        """

        prompt = f"""
        Bạn là một CONTENT STRATEGIST hàng đầu chuyên về AI. Dựa trên TOÀN BỘ dữ liệu xu hướng AI sau:
        {context}

        Hãy TỔNG HỢP và ĐỀ XUẤT đúng 5 Ý TƯỞNG NỘI DUNG cụ thể, có thể bắt tay làm ngay hôm nay.

        Mỗi ý tưởng PHẢI có:
        1. Tiêu đề video/bài viết hấp dẫn (click-worthy nhưng không clickbait)
        2. Định dạng tốt nhất (YouTube long-form, Shorts, TikTok, Blog, Thread X)
        3. Dàn ý ngắn gọn (3-4 bullet points về nội dung chính)
        4. Đối tượng mục tiêu và tiềm năng views

        ƯU TIÊN ý tưởng:
        - Kết hợp nhiều xu hướng AI với nhau (trend mashup)
        - Có góc nhìn độc đáo, không ai làm
        - Phù hợp với kênh YouTube/TikTok về Công nghệ, AI, Đời sống, Tài chính

        QUAN TRỌNG: 3 ý tưởng đầu bằng Tiếng Việt (cho thị trường VN), 2 ý tưởng cuối bằng Tiếng Anh (cho thị trường quốc tế).

        YÊU CẦU TRÌNH BÀY NGHIÊM NGẶT:
        - KHÔNG chào hỏi, KHÔNG giải thích lời thừa.
        - Trả về mã HTML thuần túy (không bọc trong thẻ ```html) với đúng cấu trúc sau:
        <div style="margin-bottom: 25px; border-left: 3px solid #3498DB; padding-left: 15px;">
            <h4 style="margin: 0 0 10px 0; color: #2C3E50; font-size: 16px;">[Số thứ tự]. [Tiêu đề Video/Bài viết]</h4>
            <ul style="margin: 0 0 12px 0; padding-left: 20px; font-size: 14px; color: #34495E; line-height: 1.5;">
                <li style="margin-bottom: 6px;"><strong>Định dạng:</strong> [YouTube/Shorts/TikTok/Blog/Thread]</li>
                <li style="margin-bottom: 6px;"><strong>Dàn ý:</strong> [3-4 bullets về nội dung chính]</li>
                <li style="margin-bottom: 6px;"><strong>Đối tượng:</strong> [Target audience + ước tính tiềm năng]</li>
                <li style="margin-bottom: 6px;"><strong>Tại sao làm NGAY:</strong> [Tính cấp thiết — xu hướng này sẽ hết hot khi nào?]</li>
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
        msg['Subject'] = f"[AI Scout 5:00 AM] 20 Tin AI & Công Nghệ Nóng Nhất - {today_str}"

        html_body = f"""
        <html>
            <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1C2833; line-height: 1.6; max-width: 800px; margin: auto;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2C3E50; margin-bottom: 5px;">🤖 AI CONTENT SCOUT</h1>
                    <p style="color: #7F8C8D; font-size: 13px; margin-top: 0;">{today_str} | Tổng hợp 20 tin AI & Công nghệ nóng nhất</p>
                </div>

                <h2 style="color: #E74C3C; border-bottom: 1px solid #FDEDEC; padding-bottom: 5px; font-size: 18px;">TẦNG 1: TIN TỨC AI & CÔNG NGHỆ TOÀN CẦU</h2>
                <p style="font-size: 12px; color: #7F8C8D; margin-top: 2px;">OpenAI, Google, Anthropic, Meta + Tin AI nóng 24h</p>
                <div style="padding: 10px 0;">
                    {t1}
                </div>

                <h2 style="color: #8E44AD; border-bottom: 1px solid #F5EEF8; padding-bottom: 5px; font-size: 18px; margin-top: 30px;">TẦNG 2: CÔNG CỤ AI & SẢN PHẨM MỚI</h2>
                <p style="font-size: 12px; color: #7F8C8D; margin-top: 2px;">ChatGPT, Gemini, Claude, Copilot + AI Tools mới 48h</p>
                <div style="padding: 10px 0;">
                    {t2}
                </div>

                <h2 style="color: #E67E22; border-bottom: 1px solid #FEF5E7; padding-bottom: 5px; font-size: 18px; margin-top: 30px;">TẦNG 3: AI CHO CONTENT CREATION</h2>
                <p style="font-size: 12px; color: #7F8C8D; margin-top: 2px;">AI Video, AI Image, AI Writing, AI Music — công cụ sáng tạo</p>
                <div style="padding: 10px 0;">
                    {t3}
                </div>

                <h2 style="color: #1ABC9C; border-bottom: 1px solid #E8F8F5; padding-bottom: 5px; font-size: 18px; margin-top: 30px;">TẦNG 4: AI & TECH VIỆT NAM</h2>
                <p style="font-size: 12px; color: #7F8C8D; margin-top: 2px;">Tin AI/Tech tại Việt Nam + VnExpress Khoa học</p>
                <div style="padding: 10px 0;">
                    {t4}
                </div>

                <h2 style="color: #3498DB; border-bottom: 1px solid #EBF5FB; padding-bottom: 5px; font-size: 18px; margin-top: 30px;">TẦNG 5: TỔNG HỢP & GỢI Ý NỘI DUNG</h2>
                <p style="font-size: 12px; color: #7F8C8D; margin-top: 2px;">5 ý tưởng nội dung AI — bắt tay làm ngay hôm nay</p>
                <div style="padding: 10px 0;">
                    {t5}
                </div>

                <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #EEE; text-align: center;">
                    <p style="font-size: 11px; color: #BDC3C7;">AI Content Scout v2.0 (5-Tier AI Intelligence) - GitHub Actions Cloud</p>
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
        print("=== BẮT ĐẦU CHẠY AI CONTENT SCOUT 5 TẦNG ===")
        t1 = self.get_tier1_ai_news()
        t2 = self.get_tier2_ai_tools()
        t3 = self.get_tier3_ai_content()
        t4 = self.get_tier4_ai_vietnam()
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
