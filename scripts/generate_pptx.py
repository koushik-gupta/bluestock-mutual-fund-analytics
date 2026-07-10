"""
Generates the final 12-slide Capstone Presentation (Presentation.pptx).
Theme: Premium Dark Mode with custom layouts (Pyramid, Table, Columns).
Run from project root: python scripts/generate_pptx.py
"""
import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).parent.parent
OUT_PATH = ROOT / "reports" / "Presentation.pptx"

# ─── COLOR PALETTE (Dark Mode) ────────────────────────────────────────────
BG_COLOR = RGBColor(10, 10, 10)       # Near Black
TEXT_MAIN = RGBColor(240, 240, 240)   # Off-White
TEXT_SUB = RGBColor(180, 180, 180)    # Light Grey
ACCENT_ORANGE = RGBColor(211, 84, 0)  # Pumpkin / Burnt Orange
ACCENT_BLUE = RGBColor(41, 128, 185)  # Belize Hole Blue
ACCENT_RED = RGBColor(192, 57, 43)    # Pomegranate Red

def set_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_slide_title(slide, text):
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9), Inches(1))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = 'Georgia' # Elegant serif for titles
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN

def add_title_slide(prs, title, subtitle=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    
    # Title
    txBox = slide.shapes.add_textbox(Inches(1), Inches(2.0) if subtitle else Inches(2.5), Inches(8), Inches(1.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = 'Georgia'
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    p.alignment = PP_ALIGN.CENTER
    
    if subtitle:
        # Divider
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4), Inches(3.5), Inches(2), Inches(0.05))
        line.fill.solid()
        line.fill.fore_color.rgb = ACCENT_ORANGE
        line.line.fill.background()
        
        # Subtitle
        txBox2 = slide.shapes.add_textbox(Inches(1), Inches(3.8), Inches(8), Inches(1.5))
        tf2 = txBox2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = subtitle
        p2.font.name = 'Arial' # Sans-serif for body
        p2.font.size = Pt(20)
        p2.font.color.rgb = TEXT_SUB
        p2.alignment = PP_ALIGN.CENTER

def add_layered_slide(prs):
    # Slide 2: Business Problem & Objective
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_slide_title(slide, "Business Problem & Objective")
    
    layers = [
        ("01", ACCENT_ORANGE, "Solution: Analytics & Visualization", "Develop an interactive Power BI dashboard for intuitive fund comparison.\nIntegrate Python risk analytics to quickly identify suitable funds."),
        ("02", ACCENT_BLUE, "Objective: Automated Data Pipeline", "Build an end-to-end automated pipeline to extract public data from AMFI.\nCentralize NAV and AUM into a single, reliable database repository."),
        ("03", ACCENT_RED, "Problem: Data Fragmentation", "NAV and AUM data is scattered across multiple public sources.\nRetail investors and advisors find it difficult to make timely decisions.")
    ]
    
    top = 1.3
    for num, color, heading, desc in layers:
        shape = slide.shapes.add_shape(MSO_SHAPE.TRAPEZOID if num == "01" else MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(top), Inches(2.0), Inches(1.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()
        
        tf_shape = shape.text_frame
        p_shape = tf_shape.paragraphs[0]
        p_shape.text = num
        p_shape.font.size = Pt(24)
        p_shape.font.bold = True
        p_shape.alignment = PP_ALIGN.CENTER
        
        txBox = slide.shapes.add_textbox(Inches(4.0), Inches(top), Inches(5.5), Inches(1.1))
        tf = txBox.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = heading
        p1.font.name = 'Georgia'
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_MAIN
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = 'Arial'
        p2.font.size = Pt(14)
        p2.font.color.rgb = TEXT_SUB
        
        top += 1.4

def add_table_slide(prs):
    # Slide 3: Data Sources
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_slide_title(slide, "Data Sources & Project Scope")
    
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(3.5), Inches(3.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Coverage & Scale"
    p1.font.name = 'Georgia'
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_MAIN
    
    p2 = tf.add_paragraph()
    p2.text = "40 mutual fund schemes analyzed across Equity, Debt, and Hybrid categories.\n\n46,000+ continuous NAV records from Jan 2022 to May 2026.\n\n32,000+ investor transactions enabling robust behavioral analysis."
    p2.font.name = 'Arial'
    p2.font.size = Pt(15)
    p2.font.color.rgb = TEXT_SUB
    
    rows, cols = 5, 2
    table_shape = slide.shapes.add_table(rows, cols, Inches(4.5), Inches(1.5), Inches(5.0), Inches(3.5))
    table = table_shape.table
    table.columns[0].width = Inches(1.5)
    table.columns[1].width = Inches(3.5)
    
    for cell in table.iter_cells():
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(20, 20, 20)
    
    for i in range(cols):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = ACCENT_RED
        p = cell.text_frame.paragraphs[0]
        p.font.name = 'Arial'
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.alignment = PP_ALIGN.CENTER
        
    table.cell(0,0).text = "Category"
    table.cell(0,1).text = "Details"
    
    data = [
        ("Data Sources", "Primary datasets from AMFI India: Daily NAVs, AUMs, and Industry SIP flow statistics."),
        ("API Integration", "Real-time NAV anchoring and validation via API integration with mfapi.in"),
        ("Fund Coverage", "40 mutual fund schemes across Equity, Debt, and Hybrid categories"),
        ("Transaction Vol.", "32,000+ investor transactions enabling behavioral and performance analysis")
    ]
    
    for row_idx, (cat, desc) in enumerate(data):
        cell_cat = table.cell(row_idx+1, 0)
        cell_cat.text = cat
        cell_cat.text_frame.paragraphs[0].font.name = 'Arial'
        cell_cat.text_frame.paragraphs[0].font.color.rgb = TEXT_MAIN
        cell_cat.text_frame.paragraphs[0].font.size = Pt(14)
        
        cell_desc = table.cell(row_idx+1, 1)
        cell_desc.text = desc
        cell_desc.text_frame.paragraphs[0].font.name = 'Arial'
        cell_desc.text_frame.paragraphs[0].font.color.rgb = TEXT_SUB
        cell_desc.text_frame.paragraphs[0].font.size = Pt(12)

def add_columns_slide(prs):
    # Slide 4: System Architecture
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_slide_title(slide, "System Architecture & ETL Pipeline")
    
    cols_data = [
        ("01", ACCENT_ORANGE, "Layered ETL Design", "Three-tier architecture: Extraction, Transformation, and Storage for clear separation of responsibilities.\nPython, Pandas, and SQLite form a robust end-to-end stack."),
        ("02", ACCENT_BLUE, "Extraction Layer", "Automated Python scripts ingest raw CSV files and REST API JSON responses.\nEnsures consistent data inflow from multiple external sources."),
        ("03", ACCENT_RED, "Storage & Automation", "Cleaned data stored in a 5-table relational Star Schema (SQLite).\nCron job schedules ETL to run automatically every weekday at 8 PM."),
        ("04", ACCENT_BLUE, "Transformation Layer", "Pandas used to normalize schemas and standardize data formats.\nHandles temporal gaps by forward-filling weekends/holidays and computes daily returns.")
    ]
    
    col_width = 2.0
    spacing = 0.3
    start_left = 0.5
    
    for i, (num, color, title, desc) in enumerate(cols_data):
        left = start_left + (i * (col_width + spacing))
        
        shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left + 0.6), Inches(1.5), Inches(0.8), Inches(0.8))
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_COLOR
        shape.line.color.rgb = color
        shape.line.width = Pt(2)
        p = shape.text_frame.paragraphs[0]
        p.text = num
        p.font.color.rgb = TEXT_MAIN
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        
        if i < 3:
            line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left + col_width + (spacing/2)), Inches(1.3), Inches(0.02), Inches(3.8))
            line.fill.solid()
            line.fill.fore_color.rgb = RGBColor(50, 50, 50)
            line.line.fill.background()
            
        txBox = slide.shapes.add_textbox(Inches(left), Inches(2.5), Inches(col_width), Inches(2.8))
        tf = txBox.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = 'Georgia'
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_MAIN
        p1.alignment = PP_ALIGN.CENTER
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = 'Arial'
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_SUB
        p2.alignment = PP_ALIGN.CENTER

def add_dark_content_slide(prs, title, box_title, desc, img_path=None):
    # General Content Slides (EDA, Findings)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_slide_title(slide, title)
    
    width = Inches(4.2) if img_path else Inches(9.0)
    
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), width, Inches(4.0))
    txBox.line.color.rgb = ACCENT_ORANGE
    txBox.line.width = Pt(1)
    
    tf = txBox.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = box_title
    p1.font.name = 'Georgia'
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_MAIN
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = 'Arial'
    p2.font.size = Pt(15) if img_path else Pt(18)
    p2.font.color.rgb = TEXT_SUB
    p2.line_spacing = 1.2
    
    if img_path and Path(img_path).exists():
        pic = slide.shapes.add_picture(str(img_path), Inches(5.0), Inches(1.2), width=Inches(4.5))
        pic.line.color.rgb = RGBColor(255,255,255)
        pic.line.width = Pt(2)

def add_full_image_slide(prs, title, desc, img_path):
    # Dashboard screenshots
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_slide_title(slide, title)
    
    if Path(img_path).exists():
        # Center image and ensure it doesn't overlap text below
        pic = slide.shapes.add_picture(str(img_path), Inches(1.5), Inches(1.0), height=Inches(3.8))
        pic.line.color.rgb = ACCENT_ORANGE
        pic.line.width = Pt(2)
        
    txBox = slide.shapes.add_textbox(Inches(1), Inches(5.0), Inches(8), Inches(0.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = desc
    p.font.name = 'Arial'
    p.font.size = Pt(16)
    p.font.color.rgb = TEXT_SUB
    p.alignment = PP_ALIGN.CENTER

# ─── BUILD PRESENTATION ───────────────────────────────────────────────────
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(5.625)

# Slide 1
add_title_slide(prs, "Mutual Fund Analytics Platform", "Data Engineering & Dashboard Project\nPrepared by: Koushik Gupta")

# Slide 2
add_layered_slide(prs)

# Slide 3
add_table_slide(prs)

# Slide 4
add_columns_slide(prs)

# Slide 5
add_dark_content_slide(prs, "Industry Overview: Exponential Growth", 
                       "Retail Boom & AUM Scale", 
                       "The Indian mutual fund industry is witnessing a strong surge in retail participation.\n\nTop tracked funds have crossed Rs. 10.4 Lakh Crore in AUM.\n\nSIPs now dominate over lump-sum investments, signaling a shift towards disciplined, long-term wealth creation.", 
                       ROOT / "reports" / "aum_growth.png")

# Slide 6
add_dark_content_slide(prs, "Investor Demographics Analysis", 
                       "Age & Geographic Insights", 
                       "The 25-35 age bracket forms the largest share of retail investors, indicating strong millennial participation.\n\nTier 1 cities in Maharashtra and Karnataka are the primary hubs leading SIP volumes.\n\nThese young investors drove the record SIP inflows of Rs. 31,002 Cr in Dec 2025.", 
                       ROOT / "reports" / "age_distribution.png")

# Slide 7
add_dark_content_slide(prs, "Performance & Risk Analytics", 
                       "Risk-Adjusted Returns", 
                       "Top Equity Funds (e.g., HDFC Top 100) generated robust ~14.8% annualized 3-year returns.\n\nAchieved a Sharpe Ratio of 1.06, indicating excellent return per unit of risk.\n\nTracking error analysis confirms large-cap funds closely mirrored the Nifty 50 benchmark.", 
                       ROOT / "reports" / "return_distribution.png")

# Slide 8
add_dark_content_slide(prs, "Advanced Quantitative Models", 
                       "Simulation & Optimization", 
                       "Monte Carlo: Forecasted 5-year NAV growth paths utilizing 1,000 random walk simulations.\n\nEfficient Frontier: Executed 10,000 portfolio permutations to map the optimal risk/return curve.\n\nOptimal Portfolio targets a 16.75% Expected Return at only 9.37% Volatility.", 
                       ROOT / "reports" / "efficient_frontier.png")

# Slide 9
add_full_image_slide(prs, "Interactive Dashboard: Market Overview", 
                     "Power BI Desktop connected via DirectQuery to visualize Industry AUM and SIP KPIs.", 
                     ROOT / "Power_BI" / "PAGE_1.png")

# Slide 10
add_full_image_slide(prs, "Interactive Dashboard: Fund Performance", 
                     "Page 2 enables comprehensive Fund Performance comparison using Risk vs Return scatter plots.", 
                     ROOT / "Power_BI" / "PAGE_2.png")

# Slide 11 (No image, full width box)
add_dark_content_slide(prs, "Executive Summary & Value", 
                       "Key Business Takeaways", 
                       "Targeted Growth: Marketing should focus on the high-growth 25-35 demographic in emerging Tier-2 cities.\n\nData-Driven Diversification: The Efficient Frontier model allows investors to maximize returns while capping volatility.\n\nAutomated Reporting: Stakeholders receive weekly automated HTML email reports.", 
                       None)

# Slide 12 (Just Thank You)
add_title_slide(prs, "Thank You")

prs.save(str(OUT_PATH))
print(f"[OK] Enhanced Dark Mode PowerPoint saved to {OUT_PATH}")
