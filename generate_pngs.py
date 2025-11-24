import os
from PIL import Image, ImageDraw, ImageFont

# Configuration
OUTPUT_DIR = "prototypes/images"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

COLORS = {
    "primary": "#1a1a1a",
    "accent": "#c6a87c",
    "bg": "#f5f5f5",
    "white": "#ffffff",
    "text_main": "#333333",
    "text_sub": "#666666",
    "text_light": "#999999",
    "border": "#e5e5e5"
}

class UIBuilder:
    def __init__(self, width, height, bg_color=COLORS["bg"]):
        self.width = width
        self.height = height
        self.img = Image.new("RGB", (width, height), bg_color)
        self.draw = ImageDraw.Draw(self.img)
        try:
            self.font_reg = ImageFont.truetype(FONT_REGULAR, 14)
            self.font_bold = ImageFont.truetype(FONT_BOLD, 14)
            self.font_h1 = ImageFont.truetype(FONT_BOLD, 24)
            self.font_h2 = ImageFont.truetype(FONT_BOLD, 18)
            self.font_h3 = ImageFont.truetype(FONT_BOLD, 16)
            self.font_small = ImageFont.truetype(FONT_REGULAR, 12)
            self.font_icon = ImageFont.truetype(FONT_BOLD, 20) # Simulate icon
        except:
            print("Warning: Fonts not found, using default.")
            self.font_reg = ImageFont.load_default()
            self.font_bold = ImageFont.load_default()
            # ... assign others to default

    def rect(self, x, y, w, h, color, outline=None, width=0):
        self.draw.rectangle([x, y, x+w, y+h], fill=color, outline=outline, width=width)

    def circle(self, cx, cy, r, color, outline=None):
        self.draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color, outline=outline)

    def text(self, x, y, text, font=None, color=COLORS["text_main"], align="left"):
        if font is None: font = self.font_reg
        
        bbox = self.draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        if align == "center":
            x -= text_w / 2
        elif align == "right":
            x -= text_w
        
        self.draw.text((x, y), text, font=font, fill=color)

    def button(self, x, y, w, h, text, bg_color=COLORS["primary"], text_color=COLORS["white"]):
        self.rect(x, y, w, h, bg_color)
        self.text(x + w/2, y + h/2 - 8, text, font=self.font_h3, color=text_color, align="center")

    def navbar_app(self, title):
        self.rect(0, 0, self.width, 88, COLORS["white"])
        self.text(20, 50, "<", font=self.font_h2, color=COLORS["primary"])
        self.text(self.width/2, 50, title, font=self.font_h2, color=COLORS["primary"], align="center")
        self.text(self.width-40, 50, "...", font=self.font_h2, color=COLORS["primary"])

    def navbar_web(self):
        self.rect(0, 0, self.width, 80, COLORS["white"])
        self.text(50, 25, "JIJING.WINDOW", font=self.font_h1, color=COLORS["primary"])
        menu = ["首页", "产品系列", "品牌故事", "服务流程"]
        for i, m in enumerate(menu):
            self.text(400 + i*120, 32, m, font=self.font_h3, color=COLORS["text_main"])
        self.button(self.width - 160, 20, 110, 40, "立即预约")

    def save(self, filename):
        self.img.save(os.path.join(OUTPUT_DIR, filename))

# --- Generators ---

def gen_app_home():
    ui = UIBuilder(375, 812)
    
    # Header
    ui.rect(0, 0, 375, 250, COLORS["primary"])
    ui.text(20, 60, "JIJING", font=ui.font_h2, color=COLORS["white"])
    ui.text(330, 60, "Q", font=ui.font_h2, color=COLORS["white"]) # Search icon
    
    ui.text(20, 120, "极光系列 2.0", font=ImageFont.truetype(FONT_BOLD, 32), color=COLORS["accent"])
    ui.text(20, 170, "定义未来人居新高度", font=ui.font_reg, color=COLORS["white"])
    
    # Grid
    y_grid = 230
    ui.rect(0, y_grid, 375, 100, COLORS["white"]) # Rounded top fake
    icons = ["预约量尺", "进度查询", "附近门店", "在线客服"]
    for i, label in enumerate(icons):
        x = 25 + i * 88
        ui.circle(x+20, y_grid+30, 25, COLORS["bg"])
        ui.text(x+12, y_grid+22, "★", font=ui.font_h2, color=COLORS["accent"] if i==0 else COLORS["text_light"])
        ui.text(x+20, y_grid+65, label, font=ui.font_small, align="center")

    # Scroll Area
    y_list = 350
    ui.text(20, y_list, "热销系列", font=ui.font_h2)
    
    for i in range(2):
        x = 20 + i * 170
        ui.rect(x, y_list+40, 150, 200, COLORS["white"])
        # Image placeholder
        ui.rect(x, y_list+40, 150, 120, "#dddddd") 
        ui.text(x+10, y_list+170, "极光平开窗" if i==0 else "星际推拉门", font=ui.font_bold)
        ui.text(x+10, y_list+195, "¥1,280起", font=ui.font_bold, color=COLORS["accent"])

    # Tab Bar
    ui.rect(0, 732, 375, 80, COLORS["white"])
    ui.text(187, 750, "+", font=ImageFont.truetype(FONT_BOLD, 30), color=COLORS["accent"], align="center")
    ui.text(50, 760, "首页", font=ui.font_small, color=COLORS["primary"], align="center")
    ui.text(325, 760, "我的", font=ui.font_small, color=COLORS["text_light"], align="center")

    ui.save("01_App_Home.png")

def gen_app_detail():
    ui = UIBuilder(375, 812, COLORS["white"])
    ui.navbar_app("产品详情")
    
    # Image
    ui.rect(0, 88, 375, 250, "#dddddd")
    ui.text(300, 300, "1/5", font=ui.font_small, color=COLORS["white"])

    # Info
    y_info = 350
    ui.text(20, y_info, "极光系列 · 系统平开窗", font=ui.font_h1)
    ui.text(20, y_info+40, "¥1,280 / 平米", font=ui.font_h2, color=COLORS["accent"])
    
    ui.text(20, y_info+80, "极简窄边框设计 | 35dB深海级静音", font=ui.font_small, color=COLORS["text_sub"])

    # Config
    y_conf = 480
    ui.text(20, y_conf, "颜色选择", font=ui.font_bold)
    colors = ["#000000", "#888888", "#8B4513"]
    for i, c in enumerate(colors):
        ui.circle(40 + i*50, y_conf+40, 15, c)
        if i == 0: ui.circle(40 + i*50, y_conf+40, 18, None, outline=COLORS["accent"])

    # Footer Action
    ui.rect(0, 732, 375, 80, COLORS["white"])
    ui.button(20, 742, 335, 50, "免费预约量尺")

    ui.save("02_App_Detail.png")

def gen_app_measure():
    ui = UIBuilder(375, 812, COLORS["white"])
    ui.navbar_app("预约量尺")

    # Steps
    ui.rect(0, 88, 375, 60, COLORS["primary"])
    ui.text(60, 110, "1.信息", font=ui.font_bold, color=COLORS["accent"], align="center")
    ui.text(187, 110, "2.上门", font=ui.font_bold, color=COLORS["text_light"], align="center")
    ui.text(315, 110, "3.方案", font=ui.font_bold, color=COLORS["text_light"], align="center")

    # Form
    y_form = 180
    fields = ["您的姓名", "联系电话", "所在地区", "房屋类型"]
    for i, f in enumerate(fields):
        y = y_form + i * 90
        ui.text(30, y, f, font=ui.font_bold)
        ui.rect(30, y+30, 315, 45, COLORS["bg"])
        ui.text(45, y+45, "请输入"+f, font=ui.font_small, color=COLORS["text_light"])

    ui.button(30, 600, 315, 50, "立即提交", bg_color=COLORS["accent"])
    
    ui.save("03_App_Measure.png")

def gen_app_success():
    ui = UIBuilder(375, 812, COLORS["white"])
    
    cx, cy = 187, 300
    ui.circle(cx, cy, 40, COLORS["bg"])
    ui.text(cx, cy-15, "✓", font=ImageFont.truetype(FONT_BOLD, 40), color="green", align="center")
    
    ui.text(cx, cy+60, "预约提交成功", font=ui.font_h1, align="center")
    ui.text(cx, cy+100, "专业设计师将在24小时内与您联系", font=ui.font_small, color=COLORS["text_sub"], align="center")
    
    ui.button(87, 500, 200, 50, "返回首页", bg_color=COLORS["bg"], text_color=COLORS["text_main"])

    ui.save("04_App_Success.png")

def gen_web_home():
    ui = UIBuilder(1200, 900)
    ui.navbar_web()
    
    # Hero
    ui.rect(0, 80, 1200, 500, COLORS["primary"])
    ui.text(600, 250, "重新定义 家 的边界", font=ImageFont.truetype(FONT_BOLD, 48), color=COLORS["white"], align="center")
    ui.text(600, 320, "静音 · 隔热 · 安全", font=ui.font_h2, color=COLORS["text_light"], align="center")
    
    ui.rect(500, 380, 200, 50, COLORS["accent"])
    ui.text(600, 395, "浏览产品系列", font=ui.font_h3, color=COLORS["white"], align="center")

    # Products
    ui.text(600, 650, "臻选系列", font=ui.font_h1, align="center")
    for i in range(3):
        x = 150 + i * 320
        ui.rect(x, 700, 280, 150, "#e0e0e0")
        ui.text(x, 860, ["极光平开窗", "星际推拉门", "阳光房"][i], font=ui.font_h3)

    ui.save("05_Web_Home.png")

if __name__ == "__main__":
    gen_app_home()
    gen_app_detail()
    gen_app_measure()
    gen_app_success()
    gen_web_home()
