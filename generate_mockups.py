import os

def create_svg(filename, width, height, content):
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <style>
        .text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        .shadow {{ filter: drop-shadow(0px 4px 4px rgba(0,0,0,0.1)); }}
    </style>
    <rect width="100%" height="100%" fill="#f5f5f5"/>
    {content}
    </svg>'''
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg_content)

# Helpers
def rect(x, y, w, h, fill, r=0, stroke=None, stroke_width=0, opacity=1):
    stroke_attr = f'stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" fill-opacity="{opacity}" {stroke_attr} />'

def text(x, y, content, size=14, color="#333", weight="normal", align="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{align}" class="text">{content}</text>'

def circle(cx, cy, r, fill, stroke=None):
    stroke_attr = f'stroke="{stroke}" stroke-width="2"' if stroke else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {stroke_attr} />'

def icon_placeholder(x, y, size, color="#ccc"):
    return rect(x, y, size, size, color, r=4)

# --- 1. App Home ---
def generate_app_home():
    w, h = 375, 812 # iPhone X size
    c = ""
    
    # Phone Body
    c += rect(0, 0, w, h, "#ffffff")
    
    # Header
    c += rect(0, 0, w, 88, "#1a1a1a")
    c += text(20, 58, "JIJING", 18, "#ffffff", "bold")
    c += text(330, 58, "🔍", 16, "#ffffff")
    
    # Banner
    c += rect(0, 88, w, 200, "#2d2d2d")
    c += text(20, 240, "极光系列 2.0", 24, "#ffffff", "bold")
    c += text(20, 265, "定义未来人居新高度", 14, "#aaaaaa")
    
    # King Kong Area (Grid Icons)
    y_grid = 310
    icons = ["预约量尺", "进度查询", "附近门店", "在线客服"]
    colors = ["#c6a87c", "#f0f0f0", "#f0f0f0", "#f0f0f0"]
    text_colors = ["#ffffff", "#333333", "#333333", "#333333"]
    
    for i, label in enumerate(icons):
        x = 20 + i * 90
        c += circle(x + 25, y_grid + 25, 25, colors[i])
        icon_char = "📏" if i == 0 else "●"
        c += text(x + 25, y_grid + 30, icon_char, 16, text_colors[i], align="middle")
        c += text(x + 25, y_grid + 70, label, 12, "#333", align="middle")

    # Horizontal Scroll
    y_scroll = 420
    c += text(20, y_scroll, "热销系列", 16, "#000", "bold")
    c += text(350, y_scroll, "全部 >", 12, "#999", align="end")
    
    for i in range(3):
        x = 20 + i * 130
        c += rect(x, y_scroll + 20, 120, 120, "#eeeeee", r=8)
        c += text(x, y_scroll + 160, "极光平开窗" if i==0 else "星际推拉" if i==1 else "阳光房", 12, "#333", "bold")
        c += text(x, y_scroll + 180, "¥1,280起", 12, "#c6a87c", "bold")

    # Tab Bar
    c += rect(0, h-80, w, 80, "#ffffff", stroke="#eeeeee", stroke_width=1)
    tabs = ["首页", "产品", "预约", "消息", "我的"]
    for i, tab in enumerate(tabs):
        x = 35 + i * 70
        color = "#1a1a1a" if i == 0 else "#cccccc"
        if i == 2: # Center button
            c += circle(x, h-50, 28, "#1a1a1a")
            c += text(x, h-42, "+", 24, "#ffffff", align="middle")
        else:
            c += text(x, h-45, "■", 18, color, align="middle")
            c += text(x, h-25, tab, 10, color, align="middle")

    create_svg("prototypes/01_App_Home.svg", w, h, c)

# --- 2. App Measure ---
def generate_app_measure():
    w, h = 375, 812
    c = ""
    
    # Body
    c += rect(0, 0, w, h, "#f9fafb")
    
    # Header
    c += rect(0, 0, w, 88, "#ffffff")
    c += text(20, 58, "←", 20, "#333")
    c += text(w/2, 58, "预约量尺", 18, "#333", "bold", align="middle")
    
    # Steps
    c += rect(0, 88, w, 100, "#1a1a1a")
    # Line
    c += rect(50, 130, 275, 2, "#444")
    # Dots
    steps = ["提交信息", "上门测量", "出具方案"]
    step_colors = ["#c6a87c", "#444", "#444"]
    for i, label in enumerate(steps):
        x = 60 + i * 127
        fill = step_colors[i]
        border = "#c6a87c" if i == 0 else "#666"
        text_col = "#c6a87c" if i == 0 else "#666"
        
        c += circle(x, 131, 12, fill, border)
        c += text(x, 136, str(i+1), 10, "#fff" if i==0 else "#888", align="middle")
        c += text(x, 160, label, 10, text_col, align="middle")

    # Form Card
    card_y = 210
    c += rect(20, card_y, w-40, 350, "#ffffff", r=12)
    c += text(40, card_y + 40, "房屋类型 *", 14, "#333", "bold")
    
    # Radio Buttons
    options = ["毛坯房", "旧房翻新", "封阳台"]
    for i, opt in enumerate(options):
        bx = 40 + i * 100
        bg = "#fff8f0" if i == 0 else "#ffffff"
        border = "#c6a87c" if i == 0 else "#ddd"
        text_c = "#c6a87c" if i == 0 else "#666"
        c += rect(bx, card_y + 55, 90, 40, bg, r=6, stroke=border, stroke_width=1)
        c += text(bx + 45, card_y + 80, opt, 12, text_c, align="middle")

    # Inputs
    inputs = ["联系人", "手机号", "详细地址"]
    for i, label in enumerate(inputs):
        y = card_y + 120 + i * 75
        c += text(40, y, label + " *", 14, "#333", "bold")
        c += rect(40, y + 15, w-80, 40, "#f5f5f5", r=6)
        c += text(50, y + 40, "请输入" + label, 12, "#999")

    # Button
    c += rect(0, h-90, w, 90, "#ffffff", stroke="#eee", stroke_width=1)
    c += rect(30, h-70, w-60, 50, "#1a1a1a", r=25)
    c += text(w/2, h-38, "立即预约", 16, "#ffffff", "bold", align="middle")

    create_svg("prototypes/02_App_Measure.svg", w, h, c)

# --- 3. Web Home ---
def generate_web_home():
    w, h = 1200, 800
    c = ""
    
    # Nav
    c += rect(0, 0, w, 70, "#ffffff", stroke="#eee", stroke_width=1)
    c += text(50, 45, "JIJING.WINDOW", 24, "#1a1a1a", "bold")
    menu = ["首页", "产品系列", "品牌故事", "服务流程"]
    for i, m in enumerate(menu):
        c += text(400 + i * 100, 45, m, 14, "#333")
    c += rect(1050, 15, 100, 40, "#1a1a1a", r=2)
    c += text(1100, 40, "立即预约", 14, "#ffffff", align="middle")

    # Hero
    c += rect(0, 70, w, 450, "#2d2d2d")
    c += text(w/2, 250, "重新定义 家 的边界", 48, "#ffffff", "bold", align="middle")
    c += text(w/2, 300, "静音 · 隔热 · 安全 —— 德系精工系统门窗", 18, "#cccccc", align="middle")
    c += rect(w/2 - 110, 350, 100, 40, "transparent", stroke="#fff", stroke_width=1)
    c += text(w/2 - 60, 375, "浏览产品", 14, "#fff", align="middle")
    c += rect(w/2 + 10, 350, 100, 40, "#c6a87c")
    c += text(w/2 + 60, 375, "免费量尺", 14, "#fff", align="middle")

    # Products
    y_prod = 580
    c += text(w/2, 560, "臻选系列", 24, "#333", "bold", align="middle")
    c += rect(w/2 - 20, 575, 40, 3, "#c6a87c")
    
    for i in range(3):
        x = 150 + i * 320
        c += rect(x, y_prod, 280, 180, "#eee")
        names = ["极光系列 · 平开窗", "星际系列 · 推拉门", "天幕系列 · 阳光房"]
        c += text(x, y_prod + 210, names[i], 18, "#333", "bold")
        c += text(x, y_prod + 235, "极致视野 / 超强密封", 12, "#666")

    create_svg("prototypes/03_Web_Home.svg", w, h, c)

# --- 4. Web Detail ---
def generate_web_detail():
    w, h = 1200, 800
    c = ""
    
    # Nav
    c += rect(0, 0, w, 70, "#ffffff", stroke="#eee", stroke_width=1)
    c += text(50, 45, "JIJING.WINDOW", 24, "#1a1a1a", "bold")

    # Content Layout
    c += rect(100, 120, 600, 450, "#eeeeee", r=8) # Main Image
    c += rect(100, 590, 140, 100, "#e0e0e0", r=4) # Thumb 1
    c += rect(250, 590, 140, 100, "#f0f0f0", r=4) # Thumb 2
    c += rect(400, 590, 140, 100, "#f0f0f0", r=4) # Thumb 3

    # Sidebar
    sx = 750
    sy = 120
    c += text(sx, sy + 30, "极光系列 · 系统平开窗", 32, "#1a1a1a", "bold")
    c += text(sx, sy + 60, "Aurora Series System Casement Window", 14, "#999")
    c += text(sx, sy + 110, "¥1,280", 36, "#c6a87c", "bold")
    c += text(sx + 130, sy + 110, "/ 平方米起", 14, "#999")

    # Config Options
    c += text(sx, sy + 160, "1. 选择颜色", 14, "#333", "bold")
    colors = ["#1a1a1a", "#666", "#8B4513", "#f0f0f0"]
    for i, col in enumerate(colors):
        stroke = "#c6a87c" if i == 0 else "#ddd"
        stroke_w = 2 if i == 0 else 1
        c += circle(sx + 25 + i * 60, sy + 200, 20, col, stroke)

    c += text(sx, sy + 260, "2. 玻璃配置", 14, "#333", "bold")
    c += rect(sx, sy + 280, 120, 40, "#fff8f0", r=4, stroke="#c6a87c", stroke_width=1)
    c += text(sx + 60, sy + 305, "标准中空", 12, "#333", align="middle")
    c += rect(sx + 140, sy + 280, 120, 40, "#fff", r=4, stroke="#ddd", stroke_width=1)
    c += text(sx + 200, sy + 305, "三玻两腔", 12, "#666", align="middle")

    # Buttons
    c += rect(sx, sy + 380, 350, 60, "#1a1a1a", r=4)
    c += text(sx + 175, sy + 415, "预约免费量尺", 18, "#ffffff", "bold", align="middle")
    
    c += rect(sx, sy + 450, 350, 60, "#ffffff", r=4, stroke="#ddd", stroke_width=1)
    c += text(sx + 175, sy + 485, "联系客服咨询", 18, "#333", align="middle")

    create_svg("prototypes/04_Web_Detail.svg", w, h, c)

if __name__ == "__main__":
    generate_app_home()
    generate_app_measure()
    generate_web_home()
    generate_web_detail()
