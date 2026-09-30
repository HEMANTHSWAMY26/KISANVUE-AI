import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    # Color Palette Constants
    DARK_BG = RGBColor(9, 18, 14)       # #09120e
    CARD_BG = RGBColor(15, 28, 22)      # #0f1c16
    BORDER_EMERALD = RGBColor(16, 185, 129) # #10b981
    ACCENT_MINT = RGBColor(52, 211, 153)    # #34d399
    ACCENT_CYAN = RGBColor(6, 182, 212)     # #06b6d4
    ACCENT_AMBER = RGBColor(245, 158, 11)   # #f59e0b
    TEXT_WHITE = RGBColor(248, 250, 252)    # #f8fafc
    TEXT_MUTED = RGBColor(148, 163, 184)    # #94a3b8
    CARD_DARK = RGBColor(13, 24, 19)

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.color.rgb = DARK_BG
        return bg

    def add_header(slide, title, category="TRACK 4: AGRICULTURAL INTELLIGENCE"):
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_MINT

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, border_color=BORDER_EMERALD):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(4.8), Inches(0.45))
    pill.fill.solid()
    pill.fill.fore_color.rgb = CARD_BG
    pill.line.color.rgb = BORDER_EMERALD
    p_pill = pill.text_frame.paragraphs[0]
    p_pill.text = "GOOGLE CLOUD · BUILD WITH AI · TRACK 4"
    p_pill.font.size = Pt(11)
    p_pill.font.bold = True
    p_pill.font.color.rgb = ACCENT_MINT

    # Title & Tagline
    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(7.2), Inches(2.2))
    tf = tbox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "KISANVUE AI"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p2 = tf.add_paragraph()
    p2.text = "See. Understand. Act. Verify."
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_MINT
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "AI-Powered Agricultural Intelligence for India\nTurning multimodal imagery, satellite signals, and soil dynamics into verified farmer decisions."
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(12)

    # Key Badges on Slide 1
    badge_data = [
        ("Multimodal AI", "Google Gemini Reasoning"),
        ("Earth Observation", "Sentinel-2 NDVI & NDWI"),
        ("Soil & Weather", "SoilGrids & Open-Meteo"),
        ("Closed-Loop", "Verify-Again Engine")
    ]
    for i, (b_title, b_sub) in enumerate(badge_data):
        bx = 0.8 + (i * 2.85)
        by = 4.3
        c = add_card(s1, bx, by, 2.7, 1.4, border_color=BORDER_EMERALD)
        tf_b = c.text_frame
        tf_b.margin_left = tf_b.margin_top = Inches(0.15)
        pb1 = tf_b.paragraphs[0]
        pb1.text = b_title
        pb1.font.size = Pt(13)
        pb1.font.bold = True
        pb1.font.color.rgb = ACCENT_CYAN
        pb2 = tf_b.add_paragraph()
        pb2.text = b_sub
        pb2.font.size = Pt(11)
        pb2.font.color.rgb = TEXT_MUTED
        pb2.space_before = Pt(4)

    # Live Demo bar at bottom
    foot = s1.shapes.add_textbox(Inches(0.8), Inches(6.2), Inches(11.5), Inches(0.6))
    tf_f = foot.text_frame
    pf = tf_f.paragraphs[0]
    pf.text = "LIVE PLATFORM: https://kisanvue-ai.vercel.app/   |   BACKEND: FastAPI + Render   |   OPEN SOURCE"
    pf.font.size = Pt(11)
    pf.font.color.rgb = ACCENT_MINT

    # Insert hero screenshot on right side
    if os.path.exists("screenshots/01_hero_and_farm_snapshot.png"):
        s1.shapes.add_picture("screenshots/01_hero_and_farm_snapshot.png", Inches(7.8), Inches(1.2), width=Inches(4.8))

    # =========================================================================
    # SLIDE 2: THE PROBLEM
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Challenge: Farm Decisions Are Still Fragmented")

    # Lead Statement
    lead_box = s2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(0.6))
    p_lead = lead_box.text_frame.paragraphs[0]
    p_lead.text = "Small and marginal farmers need timely, localized guidance — but vital agricultural intelligence remains isolated in silos."
    p_lead.font.size = Pt(14)
    p_lead.font.color.rgb = TEXT_MUTED

    # 4 Siloed Cards
    silos = [
        ("🌦 Weather Forecasts", "Disconnected Micro-Climates", "Rainfall or humidity alerts sit on general apps without linking to active fungal incubation windows or spraying timing."),
        ("🛰 Satellite Imagery", "Inaccessible Earth Obs", "Sentinel-2 NDVI & NDWI data exists in complex GIS dashboards far removed from daily smallholder comprehension."),
        ("🧪 Soil Test Reports", "Static Physical Cards", "Soil organic carbon (SOC) and texture (clay/sand) metrics remain in drawer records rather than guiding immediate inputs."),
        ("🌱 Crop Health Advice", "Fragmented Field Diagnosis", "Farmers receive isolated visual symptom guesses without validating against local climate, soil suitability, or past advisories.")
    ]

    for i, (title, sub, body) in enumerate(silos):
        cx = 0.8 + (i * 2.95)
        cy = 2.4
        c = add_card(s2, cx, cy, 2.8, 3.2, border_color=ACCENT_AMBER)
        tf_c = c.text_frame
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = Inches(0.18)
        p1 = tf_c.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_AMBER

        p2 = tf_c.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(4)

        p3 = tf_c.add_paragraph()
        p3.text = body
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(8)

    # Core Problem Highlight Banner
    prob_banner = add_card(s2, 0.8, 5.9, 11.7, 1.0, border_color=BORDER_EMERALD)
    tf_pb = prob_banner.text_frame
    tf_pb.margin_top = Inches(0.18)
    p_pb = tf_pb.paragraphs[0]
    p_pb.alignment = PP_ALIGN.CENTER
    p_pb.text = "CORE PROBLEM STATEMENT:\n\"How do we turn fragmented agricultural data into one actionable, verified farmer decision?\""
    p_pb.font.size = Pt(13)
    p_pb.font.bold = True
    p_pb.font.color.rgb = ACCENT_MINT

    # =========================================================================
    # SLIDE 3: OUR SOLUTION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Our Solution: One Unified Intelligence Layer for the Farm")

    # Lead
    lead3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(0.5))
    pl3 = lead3.text_frame.paragraphs[0]
    pl3.text = "KisanVue AI fuses multimodal image reasoning with real-time field context into a single actionable advisory loop."
    pl3.font.size = Pt(14)
    pl3.font.color.rgb = TEXT_MUTED

    # Left: Core Pillars
    sol_cards = [
        ("Google Gemini Multimodal AI", "Visual pathology classification, lesion identification, and contextual agronomic reasoning."),
        ("Multi-Source Context Fusion", "Integrates Open-Meteo weather, Sentinel-2 vegetation indices, and SoilGrids soil properties."),
        ("Regenerative Crop Planning", "Soil- and weather-grounded crop rotations and regenerative organic soil practices."),
        ("Closed-Loop 'Verify Again'", "Post-treatment comparative visual assessment tracking recovery progress over time.")
    ]
    for i, (title, desc) in enumerate(sol_cards):
        cy = 2.2 + (i * 1.15)
        c = add_card(s3, 0.8, cy, 5.8, 1.0, border_color=BORDER_EMERALD)
        tf_c = c.text_frame
        tf_c.margin_left = tf_c.margin_right = Inches(0.18)
        tf_c.margin_top = Inches(0.12)
        p1 = tf_c.paragraphs[0]
        p1.text = f"{i+1}. {title}"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_MINT
        p2 = tf_c.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(3)

    # Right: Real Farm Snapshot Card Screenshot
    if os.path.exists("screenshots/crops/farm_snapshot_card.png"):
        s3.shapes.add_picture("screenshots/crops/farm_snapshot_card.png", Inches(6.9), Inches(2.2), width=Inches(5.6))

    # Right bottom: Weather banner screenshot
    if os.path.exists("screenshots/crops/weather_banner.png"):
        s3.shapes.add_picture("screenshots/crops/weather_banner.png", Inches(6.9), Inches(5.1), width=Inches(5.6))

    # =========================================================================
    # SLIDE 4: THE CORE WORKFLOW
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "The Core Workflow: From Field Observation to Verified Action")

    steps = [
        ("1. SCAN", "Farmer uploads crop image or captures live photo under field daylight.", "Supports leaf, stem, or vector infestation imagery."),
        ("2. UNDERSTAND", "Google Gemini performs multimodal reasoning on foliar lesions.", "AI-assisted visual assessment without unsupported claims."),
        ("3. CONTEXT", "Fuses real-time Weather, Sentinel-2 NDVI, and SoilGrids.", "Grounds visual diagnosis in active environmental reality."),
        ("4. RECOMMEND", "Generates succession crops & regenerative practices.", "Legume rotation, bio-mulching, and organic soil health."),
        ("5. ACT", "Delivers localized, multilingual IPM bio-advisory.", "Neem oil, sticky traps, balanced fertigation (Telugu/Hindi)."),
        ("6. VERIFY", "Farmer returns 5–7 days later with follow-up photo.", "AI-assisted visual comparison computes recovery score.")
    ]

    for i, (title, lead, sub) in enumerate(steps):
        col = i % 3
        row = i // 3
        cx = 0.8 + (col * 3.95)
        cy = 1.8 + (row * 2.65)
        c = add_card(s4, cx, cy, 3.75, 2.35, border_color=BORDER_EMERALD if i < 5 else ACCENT_AMBER)
        tf_c = c.text_frame
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = Inches(0.18)
        p1 = tf_c.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_AMBER if i == 5 else ACCENT_MINT
        p2 = tf_c.add_paragraph()
        p2.text = lead
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(6)
        p3 = tf_c.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(4)

    # =========================================================================
    # SLIDE 5: MULTIMODAL CROP INTELLIGENCE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Multimodal Crop Intelligence: Gemini-Powered Visual Reasoning")

    # Left: Explanation & Technical Safeguards
    lead5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.8), Inches(0.6))
    pl5 = lead5.text_frame.paragraphs[0]
    pl5.text = "Google Gemini turns raw foliar imagery into structured agronomic reasoning with transparent confidence markers."
    pl5.font.size = Pt(13)
    pl5.font.color.rgb = TEXT_MUTED

    cards5 = [
        ("AI-Assisted Visual Assessment", "Clearly designated as visual advisory rather than laboratory-grade pathology, avoiding false claims and maintaining farmer trust."),
        ("Observed Foliar Indicators", "Detects chlorosis, leaf curling, necrosis, fungal sporulation, and insect vectors (e.g., Bemisia tabaci)."),
        ("Context-Aware Severity Scoring", "Assigns calibrated risk levels (LOW / MEDIUM / HIGH) synthesized with local humidity and temperature windows."),
        ("Safe Actionable Advisory", "Emphasizes Integrated Pest Management (IPM), bio-controls, and clear escalation thresholds to Krishi Vigyan Kendras (KVK).")
    ]
    for i, (ct, cd) in enumerate(cards5):
        cy = 2.2 + (i * 1.15)
        c = add_card(s5, 0.8, cy, 5.8, 1.05, border_color=BORDER_EMERALD)
        tf_c = c.text_frame
        tf_c.margin_left = tf_c.margin_right = Inches(0.18)
        tf_c.margin_top = Inches(0.1)
        p1 = tf_c.paragraphs[0]
        p1.text = ct
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_MINT
        p2 = tf_c.add_paragraph()
        p2.text = cd
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(3)

    # Right: Sample crop image + Gemini reasoning visualization
    if os.path.exists("frontend/public/samples/chilli_leaf_curl.jpg"):
        s5.shapes.add_picture("frontend/public/samples/chilli_leaf_curl.jpg", Inches(6.9), Inches(1.6), width=Inches(2.6), height=Inches(2.4))

    # Gemini Analysis Card on the right
    diag_c = add_card(s5, 9.7, 1.6, 2.8, 2.4, border_color=ACCENT_CYAN)
    tf_dc = diag_c.text_frame
    tf_dc.margin_left = tf_dc.margin_top = Inches(0.15)
    pd1 = tf_dc.paragraphs[0]
    pd1.text = "GEMINI INFERENCE"
    pd1.font.size = Pt(11)
    pd1.font.bold = True
    pd1.font.color.rgb = ACCENT_CYAN
    pd2 = tf_dc.add_paragraph()
    pd2.text = "Condition: Chilli Leaf Curl\nRisk: HIGH (Vector active)\nConfidence: 89%\nVector: Bemisia tabaci\nAdvisory: Neem oil bio-spray"
    pd2.font.size = Pt(10)
    pd2.font.color.rgb = TEXT_WHITE
    pd2.space_before = Pt(6)

    # Lower right: UI Banner
    if os.path.exists("screenshots/crops/weather_banner.png"):
        s5.shapes.add_picture("screenshots/crops/weather_banner.png", Inches(6.9), Inches(4.3), width=Inches(5.6))

    note5 = add_card(s5, 6.9, 5.7, 5.6, 1.1, border_color=ACCENT_AMBER)
    tf_n5 = note5.text_frame
    tf_n5.margin_left = tf_n5.margin_top = Inches(0.15)
    pn1 = tf_n5.paragraphs[0]
    pn1.text = "TRANSPARENCY STANDARD:"
    pn1.font.size = Pt(11)
    pn1.font.bold = True
    pn1.font.color.rgb = ACCENT_AMBER
    pn2 = tf_n5.add_paragraph()
    pn2.text = "Every diagnostic card displays 'AI-assisted advisory' to keep expectations realistic and scientifically responsible."
    pn2.font.size = Pt(10)
    pn2.font.color.rgb = TEXT_MUTED
    pn2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 6: ENVIRONMENTAL INTELLIGENCE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Environmental Intelligence: Earth Observation & Field Context")

    # Lead
    lead6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.5))
    pl6 = lead6.text_frame.paragraphs[0]
    pl6.text = "Diagnosis becomes significantly stronger when visual symptoms are cross-referenced with satellite, soil, and atmospheric data."
    pl6.font.size = Pt(13)
    pl6.font.color.rgb = TEXT_MUTED

    # 3 Large Cards: Satellite, Soil, Weather
    env_cards = [
        ("🛰 SATELLITE INTELLIGENCE", "Sentinel-2 Multi-Spectral", [
            ("NDVI: 0.72", "Healthy vegetative density"),
            ("NDWI: 0.28", "Adequate canopy water index"),
            ("Trend: STABLE", "Multi-temporal consistency"),
            ("Provider:", "Live API + Domain Fallback")
        ], ACCENT_CYAN),
        ("🧪 SOIL INTELLIGENCE", "SoilGrids Global Dataset", [
            ("SOC: 8.4 g/kg", "Moderate organic carbon"),
            ("Clay: 44.5%", "Clay-dominant moisture retention"),
            ("Sand: 28.2%", "Balanced structural drainage"),
            ("Texture:", "Clay Loam field profile")
        ], BORDER_EMERALD),
        ("🌦 WEATHER INTELLIGENCE", "Open-Meteo Agro-Climate", [
            ("Temp: 27°C", "Moderate field temperature"),
            ("Humidity: 85%", "High fungal spore risk (>75%)"),
            ("Rain Risk: 0%", "Dry foliar spray window"),
            ("Wind: 2 km/h", "Ideal droplet deposition")
        ], ACCENT_AMBER)
    ]

    for i, (title, sub, metrics, col) in enumerate(env_cards):
        cx = 0.8 + (i * 3.95)
        c = add_card(s6, cx, 2.1, 3.75, 3.4, border_color=col)
        tf_c = c.text_frame
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = Inches(0.18)
        p1 = tf_c.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = col
        p2 = tf_c.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(3)

        for m_lbl, m_val in metrics:
            pm = tf_c.add_paragraph()
            pm.text = f"• {m_lbl} — {m_val}"
            pm.font.size = Pt(10)
            pm.font.color.rgb = TEXT_MUTED
            pm.space_before = Pt(6)

    # Bottom Fusion Summary Banner
    fuse = add_card(s6, 0.8, 5.8, 11.7, 1.1, border_color=BORDER_EMERALD)
    tf_f = fuse.text_frame
    tf_f.margin_top = Inches(0.15)
    pf1 = tf_f.paragraphs[0]
    pf1.alignment = PP_ALIGN.CENTER
    pf1.text = "SATELLITE + SOIL + WEATHER  →  TRIANGULATED AGRICULTURAL CONTEXT"
    pf1.font.size = Pt(13)
    pf1.font.bold = True
    pf1.font.color.rgb = ACCENT_MINT
    pf2 = tf_f.add_paragraph()
    pf2.alignment = PP_ALIGN.CENTER
    pf2.text = "High humidity (85%) warns of fungal spread, clay-heavy soil guides irrigation intervals, and NDVI confirms localized rather than plot-wide decline."
    pf2.font.size = Pt(10)
    pf2.font.color.rgb = TEXT_WHITE
    pf2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 7: CROP & REGENERATIVE RECOMMENDATIONS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Crop & Regenerative Advisory: What Farmers Can Do Next")

    lead7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.5))
    pl7 = lead7.text_frame.paragraphs[0]
    pl7.text = "Moving beyond disease identification: empowering farmers with climate-smart rotations and regenerative soil practices."
    pl7.font.size = Pt(13)
    pl7.font.color.rgb = TEXT_MUTED

    # Left: Crop Succession Cards
    c1 = add_card(s7, 0.8, 2.1, 5.6, 2.3, border_color=BORDER_EMERALD)
    tf_c1 = c1.text_frame
    tf_c1.margin_left = tf_c1.margin_top = Inches(0.18)
    pc1 = tf_c1.paragraphs[0]
    pc1.text = "RECOMMENDED ROTATION: Cotton / Kapas"
    pc1.font.size = Pt(13)
    pc1.font.bold = True
    pc1.font.color.rgb = ACCENT_MINT
    pc2 = tf_c1.add_paragraph()
    pc2.text = "• Agro-fit: Thrives in deep black clay-dominant soils of Andhra Pradesh.\n• Season match: Current Kharif cycle matches thermal & solar curves.\n• Soil benefit: Deep taproot system breaks soil compaction naturally.\n• Water requirement: Medium irrigation tolerance fits rainfall forecast."
    pc2.font.size = Pt(10)
    pc2.font.color.rgb = TEXT_WHITE
    pc2.space_before = Pt(6)

    c2 = add_card(s7, 0.8, 4.6, 5.6, 2.3, border_color=ACCENT_CYAN)
    tf_c2 = c2.text_frame
    tf_c2.margin_left = tf_c2.margin_top = Inches(0.18)
    pc2_1 = tf_c2.paragraphs[0]
    pc2_1.text = "SUCCESSION CROP: Black Gram / Urad (Legume)"
    pc2_1.font.size = Pt(13)
    pc2_1.font.bold = True
    pc2_1.font.color.rgb = ACCENT_CYAN
    pc2_2 = tf_c2.add_paragraph()
    pc2_2.text = "• Nitrogen fixation: Rhizobium nodules naturally replenish soil N.\n• Break pest cycles: Non-host crop disrupts Begomovirus & whitefly vectors.\n• Soil conditioning: Restores organic carbon (SOC) depleted by heavy feeders.\n• Low water requirement: Highly resilient short-duration catch crop."
    pc2_2.font.size = Pt(10)
    pc2_2.font.color.rgb = TEXT_WHITE
    pc2_2.space_before = Pt(6)

    # Right: Regenerative Options Card
    c3 = add_card(s7, 6.8, 2.1, 5.7, 4.8, border_color=ACCENT_AMBER)
    tf_c3 = c3.text_frame
    tf_c3.margin_left = tf_c3.margin_top = Inches(0.2)
    pr1 = tf_c3.paragraphs[0]
    pr1.text = "REGENERATIVE AGRICULTURAL PRACTICES"
    pr1.font.size = Pt(14)
    pr1.font.bold = True
    pr1.font.color.rgb = ACCENT_AMBER

    reg_items = [
        ("Crop Residue Mulching", "Spreading retained stubble conserves soil moisture, prevents surface crusting, and buffers root temperature in high clay soils."),
        ("Biological Bio-Control", "Prioritizes 5% Neem seed kernel extract (NSKE) and yellow sticky traps over synthetic organophosphates to protect beneficial pollinators."),
        ("Organic Carbon Enrichment", "Farmyard manure (FYM) and Jeevamrutha applications to systematically improve the 8.4 g/kg baseline SOC level."),
        ("Responsible Framing", "Strictly presented as 'potential regenerative practices' — preserving honesty without promising unrealistic guaranteed yields.")
    ]
    for r_title, r_desc in reg_items:
        pr_t = tf_c3.add_paragraph()
        pr_t.text = f"✔ {r_title}"
        pr_t.font.size = Pt(11)
        pr_t.font.bold = True
        pr_t.font.color.rgb = TEXT_WHITE
        pr_t.space_before = Pt(8)
        pr_d = tf_c3.add_paragraph()
        pr_d.text = r_desc
        pr_d.font.size = Pt(10)
        pr_d.font.color.rgb = TEXT_MUTED
        pr_d.space_before = Pt(2)

    # =========================================================================
    # SLIDE 8: VERIFY AGAIN (SIGNATURE DIFFERENTIATOR)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Verify Again: Closing the Agricultural Advisory Loop")

    # Lead
    lead8 = s8.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.5))
    pl8 = lead8.text_frame.paragraphs[0]
    pl8.text = "Most AI agritech tools end at diagnosis. KisanVue AI introduces a continuous verification loop to assess real treatment efficacy."
    pl8.font.size = Pt(13)
    pl8.font.color.rgb = TEXT_MUTED

    # Left: Baseline vs Follow-up comparison card screenshot
    if os.path.exists("screenshots/crops/verify_comparison_cards.png"):
        s8.shapes.add_picture("screenshots/crops/verify_comparison_cards.png", Inches(0.8), Inches(2.0), width=Inches(6.2))

    # Left lower: Verification result card screenshot
    if os.path.exists("screenshots/crops/verify_result_card.png"):
        s8.shapes.add_picture("screenshots/crops/verify_result_card.png", Inches(0.8), Inches(4.3), width=Inches(6.2))

    # Right side: Why This Matters
    right_card = add_card(s8, 7.3, 2.0, 5.2, 4.9, border_color=BORDER_EMERALD)
    tf_rc = right_card.text_frame
    tf_rc.margin_left = tf_rc.margin_top = Inches(0.22)
    prc1 = tf_rc.paragraphs[0]
    prc1.text = "THE 'VERIFY AGAIN' ENGINE"
    prc1.font.size = Pt(14)
    prc1.font.bold = True
    prc1.font.color.rgb = ACCENT_MINT

    diff_points = [
        ("The Industry Blind Spot", "Traditional farmer apps give a single prescription and vanish. Farmers never know if treatments worked or wasted money."),
        ("Multimodal Temporal Reasoning", "Google Gemini compares baseline Day-0 foliar symptoms against Day-5 follow-up photographs to evaluate recovery trajectory."),
        ("Quantitative Improvement Score", "Outputs an 85/100 Visual Improvement Score, risk reduction delta (HIGH → LOW), and milestone progression."),
        ("Rigorous Scientific Honesty", "Explicitly labeled: 'AI-assisted visual improvement assessment — not a laboratory measurement'."),
        ("Adaptive Recalibration", "If symptoms worsen, the engine flags non-responsiveness and immediately triggers escalation to a local KVK agronomist.")
    ]
    for dp_h, dp_b in diff_points:
        p_dh = tf_rc.add_paragraph()
        p_dh.text = f"▶ {dp_h}"
        p_dh.font.size = Pt(11)
        p_dh.font.bold = True
        p_dh.font.color.rgb = ACCENT_CYAN
        p_dh.space_before = Pt(6)
        p_db = tf_rc.add_paragraph()
        p_db.text = dp_b
        p_db.font.size = Pt(10)
        p_db.font.color.rgb = TEXT_MUTED
        p_db.space_before = Pt(2)

    # =========================================================================
    # SLIDE 9: BUILT FOR INDIA
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Built for India: Localized, Multilingual, Digital Public Good")

    lead9 = s9.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.5))
    pl9 = lead9.text_frame.paragraphs[0]
    pl9.text = "Designed for India's linguistic, regional, and climatic diversity — making complex AI accessible to every marginal farmer."
    pl9.font.size = Pt(13)
    pl9.font.color.rgb = TEXT_MUTED

    # 3 Language Cards
    langs = [
        ("English", "Technical & Global Ag-Tech", "Standard agronomic taxonomy, international soil definitions, and RESTful developer APIs."),
        ("తెలుగు (Telugu)", "Andhra Pradesh & Telangana", "చూడండి. అర్థం చేసుకోండి. ఆచరించండి. ధృవీకరించండి.\nLocalized vernacular advisory for chilli, cotton & paddy belts."),
        ("हिंदी (Hindi)", "Northern & Central Hindi Belt", "देखें. समझें. कार्य करें. सत्यापित करें.\nAccessible agro-terminology for wheat, mustard, and soybean farmers.")
    ]
    for i, (lname, sub, desc) in enumerate(langs):
        cx = 0.8 + (i * 3.95)
        c = add_card(s9, cx, 2.0, 3.75, 2.1, border_color=ACCENT_CYAN)
        tf_l = c.text_frame
        tf_l.margin_left = tf_l.margin_top = Inches(0.18)
        pl1 = tf_l.paragraphs[0]
        pl1.text = lname
        pl1.font.size = Pt(14)
        pl1.font.bold = True
        pl1.font.color.rgb = ACCENT_CYAN
        pl2 = tf_l.add_paragraph()
        pl2.text = sub
        pl2.font.size = Pt(11)
        pl2.font.color.rgb = TEXT_WHITE
        pl2.space_before = Pt(3)
        pl3 = tf_l.add_paragraph()
        pl3.text = desc
        pl3.font.size = Pt(10)
        pl3.font.color.rgb = TEXT_MUTED
        pl3.space_before = Pt(4)

    # Lower Left: Screenshot of Telugu UI
    if os.path.exists("screenshots/crops/telugu_interface_card.png"):
        s9.shapes.add_picture("screenshots/crops/telugu_interface_card.png", Inches(0.8), Inches(4.3), width=Inches(6.0))

    # Lower Right: Architectural Framing (DPG)
    dpg_card = add_card(s9, 7.1, 4.3, 5.4, 2.6, border_color=BORDER_EMERALD)
    tf_dpg = dpg_card.text_frame
    tf_dpg.margin_left = tf_dpg.margin_top = Inches(0.18)
    pd1 = tf_dpg.paragraphs[0]
    pd1.text = "DIGITAL PUBLIC GOOD ARCHITECTURE"
    pd1.font.size = Pt(13)
    pd1.font.bold = True
    pd1.font.color.rgb = ACCENT_MINT

    dpg_items = [
        ("Scalable Hierarchy:", "Field → Village → Block → District → State level intelligence."),
        ("No App Store Barrier:", "Zero-install progressive web application (PWA) running on mobile browsers."),
        ("Voice-First Inclusivity:", "Speech synthesis and voice agronomist for non-literate farmers."),
        ("Public Architecture:", "Designed to interoperate with open agricultural data standards across Indian agro-climatic zones.")
    ]
    for d_lbl, d_txt in dpg_items:
        p_di = tf_dpg.add_paragraph()
        p_di.text = f"• {d_lbl} {d_txt}"
        p_di.font.size = Pt(10)
        p_di.font.color.rgb = TEXT_WHITE
        p_di.space_before = Pt(4)

    # =========================================================================
    # SLIDE 10: TECHNOLOGY ARCHITECTURE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Technology Architecture: Composable Agricultural Intelligence")

    lead10 = s10.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.5))
    pl10 = lead10.text_frame.paragraphs[0]
    pl10.text = "Production stack built for high reliability, rapid inference, and graceful degradation across variable rural connectivity."
    pl10.font.size = Pt(13)
    pl10.font.color.rgb = TEXT_MUTED

    # Left: Architecture Modal screenshot
    if os.path.exists("screenshots/crops/architecture_modal_card.png"):
        s10.shapes.add_picture("screenshots/crops/architecture_modal_card.png", Inches(0.8), Inches(2.0), width=Inches(5.4))

    # Right: Stack Cards
    stack_items = [
        ("Frontend Layer (Vercel)", "React 18 + Vite SPA", "Ultra-lightweight dark-mode UI, multilingual i18n dictionary (EN/TE/HI), camera API integration, zero heavyweight framework overhead."),
        ("API Gateway Layer (Render)", "FastAPI / Python 3.12 Asynchronous Backend", "Pydantic validated schemas, multi-threaded upstream aggregation, graceful demo/live fallback handlers, high-throughput REST endpoints."),
        ("Multimodal Intelligence (Google Cloud)", "Google Gemini Multimodal API", "High-resolution foliar image reasoning, visual symptom localization, structured JSON pathology outputs, and multi-temporal recovery comparison."),
        ("Environmental Integrations", "Sentinel-2 + Open-Meteo + SoilGrids", "10m NDVI & NDWI satellite indices, real-time agro-meteorology (temp, humidity, rain), and SoilGrids physical properties (SOC, clay%, sand%).")
    ]
    for i, (layer, tech, detail) in enumerate(stack_items):
        cy = 2.0 + (i * 1.25)
        sc = add_card(s10, 6.5, cy, 6.0, 1.15, border_color=BORDER_EMERALD if i == 2 else ACCENT_CYAN)
        tf_sc = sc.text_frame
        tf_sc.margin_left = tf_sc.margin_top = Inches(0.15)
        p1 = tf_sc.paragraphs[0]
        p1.text = f"{layer} — {tech}"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_MINT if i == 2 else ACCENT_CYAN
        p2 = tf_sc.add_paragraph()
        p2.text = detail
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 11: IMPACT + SCALABILITY
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Potential Impact & Scalability: From One Field to National Telemetry")

    lead11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.5))
    pl11 = lead11.text_frame.paragraphs[0]
    pl11.text = "How localized farm insights aggregate into regional agricultural telemetry without compromising individual farm privacy."
    pl11.font.size = Pt(13)
    pl11.font.color.rgb = TEXT_MUTED

    # Progression Hierarchy Bar
    h_steps = [
        ("1. SINGLE FIELD", "Leaf photo + localized micro-climate + SoilGrids physical profile."),
        ("2. FARMER", "Actionable IPM advisory, vernacular voice guidance & Verify-Again."),
        ("3. MANDAL / BLOCK", "Early detection of vector hotspots (e.g. Whitefly in Chilli)."),
        ("4. DISTRICT / STATE", "Aggregated crop stress maps informing regional agricultural extension."),
        ("5. NATIONAL GRID", "Composable, standardized agricultural APIs for research & public good.")
    ]
    for i, (title, sub) in enumerate(h_steps):
        cx = 0.8 + (i * 2.35)
        c = add_card(s11, cx, 2.0, 2.25, 2.2, border_color=ACCENT_CYAN if i < 4 else ACCENT_AMBER)
        tf_c = c.text_frame
        tf_c.margin_left = tf_c.margin_top = Inches(0.15)
        p1 = tf_c.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_CYAN if i < 4 else ACCENT_AMBER
        p2 = tf_c.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(6)

    # Bottom Impact Areas
    imp_card = add_card(s11, 0.8, 4.4, 11.7, 2.5, border_color=BORDER_EMERALD)
    tf_ic = imp_card.text_frame
    tf_ic.margin_left = tf_ic.margin_top = Inches(0.2)
    pi1 = tf_ic.paragraphs[0]
    pi1.text = "PROJECTED VALUE PROPOSITIONS & SCALABILITY PATHWAYS"
    pi1.font.size = Pt(13)
    pi1.font.bold = True
    pi1.font.color.rgb = ACCENT_MINT

    impact_points = [
        ("Preventing Over-Chemicalization", "By prioritizing bio-controls (Neem oil, sticky traps) and soil mulching, farmers avoid excessive chemical expense and soil toxicity."),
        ("Early Stress Interception", "Fusing 10m Sentinel-2 NDVI with real-time humidity alerts catches fungal outbreaks days before visual catastrophic crop loss occurs."),
        ("Trust via Closed-Loop Verification", "Farmers can track and prove recovery before spending additional capital on follow-up treatments."),
        ("Frugal Rural Deployment", "Operates efficiently on mobile browsers without requiring high-end smartphones or expensive proprietary sensors.")
    ]
    for ip_t, ip_d in impact_points:
        p_ipt = tf_ic.add_paragraph()
        p_ipt.text = f"• {ip_t}: {ip_d}"
        p_ipt.font.size = Pt(10)
        p_ipt.font.color.rgb = TEXT_WHITE
        p_ipt.space_before = Pt(4)

    # =========================================================================
    # SLIDE 12: CLOSING
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)

    # Top Tagline
    tag_box = s12.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.5))
    ptg = tag_box.text_frame.paragraphs[0]
    ptg.alignment = PP_ALIGN.CENTER
    ptg.text = "GOOGLE CLOUD · BUILD WITH AI : CODE FOR COMMUNITIES · TRACK 4"
    ptg.font.size = Pt(12)
    ptg.font.bold = True
    ptg.font.color.rgb = ACCENT_MINT

    # Big Statement
    big_box = s12.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.2))
    pbb = big_box.text_frame.paragraphs[0]
    pbb.alignment = PP_ALIGN.CENTER
    pbb.text = "\"KisanVue doesn't stop at diagnosis.\""
    pbb.font.size = Pt(36)
    pbb.font.bold = True
    pbb.font.color.rgb = TEXT_WHITE

    # Four Pillars Center
    pillars = [
        ("SEE", "Farmer foliar scan & satellite Earth observation."),
        ("UNDERSTAND", "Google Gemini multimodal agronomic reasoning."),
        ("ACT", "Localized, soil-aware, weather-timed IPM advisory."),
        ("VERIFY", "Follow-up visual score closing the loop.")
    ]
    for i, (p_name, p_sub) in enumerate(pillars):
        cx = 0.8 + (i * 2.95)
        c = add_card(s12, cx, 3.0, 2.8, 2.0, border_color=BORDER_EMERALD)
        tf_p = c.text_frame
        tf_p.margin_left = tf_p.margin_top = Inches(0.18)
        pp1 = tf_p.paragraphs[0]
        pp1.text = p_name
        pp1.font.size = Pt(18)
        pp1.font.bold = True
        pp1.font.color.rgb = ACCENT_MINT
        pp2 = tf_p.add_paragraph()
        pp2.text = p_sub
        pp2.font.size = Pt(11)
        pp2.font.color.rgb = TEXT_WHITE
        pp2.space_before = Pt(8)

    # Bottom Summary Card
    close_card = add_card(s12, 0.8, 5.3, 11.7, 1.6, border_color=ACCENT_CYAN)
    tf_cc = close_card.text_frame
    tf_cc.margin_left = tf_cc.margin_top = Inches(0.2)
    pcc1 = tf_cc.paragraphs[0]
    pcc1.alignment = PP_ALIGN.CENTER
    pcc1.text = "KISANVUE AI  —  AI-Powered Agricultural Intelligence for India"
    pcc1.font.size = Pt(15)
    pcc1.font.bold = True
    pcc1.font.color.rgb = ACCENT_CYAN

    pcc2 = tf_cc.add_paragraph()
    pcc2.alignment = PP_ALIGN.CENTER
    pcc2.text = "Live Demo Application: https://kisanvue-ai.vercel.app/\nGitHub Repository: https://github.com/HEMANTHSWAMY26/KISANVUE-AI\nTrack 4: Agricultural Intelligence"
    pcc2.font.size = Pt(12)
    pcc2.font.color.rgb = TEXT_WHITE
    pcc2.space_before = Pt(6)

    # Save presentation
    output_pptx = "KISANVUE_AI_TRACK4_PITCH_DECK.pptx"
    prs.save(output_pptx)
    print(f"Presentation saved successfully to {output_pptx}")

if __name__ == "__main__":
    create_deck()
