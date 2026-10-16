import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, PageBreak, HRFlowable, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pymupdf

# Register Calibri fonts from Windows Fonts directory
pdfmetrics.registerFont(TTFont('Calibri', r'C:\Windows\Fonts\calibri.ttf'))
pdfmetrics.registerFont(TTFont('Calibri-Bold', r'C:\Windows\Fonts\calibrib.ttf'))
pdfmetrics.registerFont(TTFont('Calibri-Italic', r'C:\Windows\Fonts\calibrii.ttf'))
pdfmetrics.registerFont(TTFont('Calibri-BoldItalic', r'C:\Windows\Fonts\calibriz.ttf'))

pdfmetrics.registerFontFamily(
    'Calibri',
    normal='Calibri',
    bold='Calibri-Bold',
    italic='Calibri-Italic',
    boldItalic='Calibri-BoldItalic'
)

# Colors matching the original resume
NAVY = colors.HexColor('#1F3864')
LINK_BLUE = colors.HexColor('#0563C1')
GRAY = colors.HexColor('#595959')
BLACK = colors.HexColor('#000000')

PRINTABLE_WIDTH = 612 - 54  # 558 pt

def build_resume(output_pdf='Soham_Gaikwad_Resume.pdf'):
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=27,
        rightMargin=27,
        topMargin=22,
        bottomMargin=22
    )

    # Styles
    style_name = ParagraphStyle(
        'ResumeName',
        fontName='Calibri-Bold',
        fontSize=20.0,
        leading=22.0,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=3.0
    )

    style_subhead = ParagraphStyle(
        'ResumeSubhead',
        fontName='Calibri',
        fontSize=9.2,
        leading=11.2,
        textColor=BLACK,
        alignment=TA_CENTER,
        spaceAfter=1.4
    )

    # Page 1 section title (balanced spacing)
    style_sec_title_p1 = ParagraphStyle(
        'SectionTitleP1',
        fontName='Calibri-Bold',
        fontSize=10.5,
        leading=12.0,
        textColor=NAVY,
        spaceBefore=7,
        spaceAfter=1,
        keepWithNext=True
    )

    # Page 2 section title
    style_sec_title_p2 = ParagraphStyle(
        'SectionTitleP2',
        fontName='Calibri-Bold',
        fontSize=10.5,
        leading=12.0,
        textColor=NAVY,
        spaceBefore=4.5,
        spaceAfter=1,
        keepWithNext=True
    )

    style_item_left = ParagraphStyle(
        'ItemTitleLeft',
        fontName='Calibri-Bold',
        fontSize=9.8,
        leading=11.4,
        textColor=BLACK,
        alignment=TA_LEFT,
        spaceAfter=0
    )

    style_item_right = ParagraphStyle(
        'ItemTitleRight',
        fontName='Calibri-Italic',
        fontSize=9.0,
        leading=11.4,
        textColor=GRAY,
        alignment=TA_RIGHT,
        spaceAfter=0
    )

    style_subtitle = ParagraphStyle(
        'ItemSubtitle',
        fontName='Calibri-Italic',
        fontSize=8.8,
        leading=10.4,
        textColor=GRAY,
        spaceAfter=1.2,
        keepWithNext=True
    )

    # Page 1 body & bullet styles (comfortable spacing to fill page 1)
    style_body_p1 = ParagraphStyle(
        'BodyP1',
        fontName='Calibri',
        fontSize=9.1,
        leading=10.9,
        textColor=BLACK,
        spaceAfter=1.5
    )

    style_bullet_p1 = ParagraphStyle(
        'BulletP1',
        fontName='Calibri',
        fontSize=9.1,
        leading=10.9,
        textColor=BLACK,
        leftIndent=11,
        firstLineIndent=-11,
        spaceAfter=1.5
    )

    # Page 2 body & bullet styles (compacted to ensure 100% fit on page 2)
    style_body_p2 = ParagraphStyle(
        'BodyP2',
        fontName='Calibri',
        fontSize=9.1,
        leading=10.7,
        textColor=BLACK,
        spaceAfter=0.8
    )

    style_bullet_p2 = ParagraphStyle(
        'BulletP2',
        fontName='Calibri',
        fontSize=9.1,
        leading=10.7,
        textColor=BLACK,
        leftIndent=11,
        firstLineIndent=-11,
        spaceAfter=0.8
    )

    def section_header_p1(title):
        return [
            Paragraph(f"<b>{title}</b>", style_sec_title_p1),
            HRFlowable(width="100%", thickness=0.75, color=NAVY, spaceBefore=1, spaceAfter=2.5)
        ]

    def section_header_p2(title):
        return [
            Paragraph(f"<b>{title}</b>", style_sec_title_p2),
            HRFlowable(width="100%", thickness=0.75, color=NAVY, spaceBefore=1, spaceAfter=2.5)
        ]

    def link(url, text):
        return f'<font color="#0563C1"><a href="{url}"><u>{text}</u></a></font>'

    def row(left_html, right_html, right_width=140):
        left_w = PRINTABLE_WIDTH - right_width
        t = Table(
            [[Paragraph(left_html, style_item_left), Paragraph(right_html, style_item_right)]],
            colWidths=[left_w, right_width]
        )
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 1.8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ]))
        return t

    story = []

    # =========================================================================
    # PAGE 1
    # =========================================================================
    
    # 1. Header (Centered)
    story.append(Paragraph("<b>SOHAM HARIDAS GAIKWAD</b>", style_name))
    story.append(Paragraph("B.Tech CSE &bull; SPIT Mumbai &bull; 3rd Year (2024&ndash;2028)", style_subhead))
    story.append(Paragraph(
        f'{link("mailto:soham092510@gmail.com", "soham092510@gmail.com")} &bull; +91 8788156563 &bull; Mumbai, India',
        style_subhead
    ))
    story.append(Paragraph(
        f'{link("https://github.com/soham-092510", "GitHub")} &bull; '
        f'{link("https://portfolio-soham-two.vercel.app/", "Portfolio")} &bull; '
        f'{link("https://leetcode.com/u/Soham092510", "LeetCode")}',
        style_subhead
    ))

    # 2. Education
    story.extend(section_header_p1("EDUCATION"))
    story.append(row("<b>B.Tech &ndash; Computer Science &amp; Engineering</b>", "<i>2024 &ndash; 2028</i>", right_width=80))
    story.append(Paragraph("Sardar Patel Institute of Technology (SPIT), Mumbai", style_body_p1))
    story.append(Paragraph("<b>CGPA: 8.09</b> | <b>Coursework:</b> Data Structures &amp; Algorithms, Operating Systems, Computer Networks, DBMS, Computer Architecture, Data Science, Software Engineering, Theory of Computation", style_body_p1))

    # 3. Technical Skills
    story.extend(section_header_p1("TECHNICAL SKILLS"))
    skills = [
        ("Programming Languages", "Python, C, Java"),
        ("Machine Learning / Deep Learning / LLM", "Machine Learning, Deep Learning (Neural Networks), Large Language Models (LLM), Retrieval-Augmented Generation (RAG), LangChain, Google Gemini API, FAISS (Vector Search), Prompt Engineering, Conversational Memory Design, Supervised Learning, Gradient Boosting, XGBoost, LightGBM, Hyperparameter Tuning, Predictive Analytics, Time Series Forecasting (Prophet), PyTorch, TensorFlow, Keras, Scikit-learn"),
        ("Data Science &amp; Analysis", "Exploratory Data Analysis (EDA), Feature Engineering, Data Cleaning, Data Processing, Pandas, NumPy, Matplotlib, Seaborn, Jupyter Notebooks"),
        ("NLP &amp; AI Applications", "Sentiment Analysis (VADER), Named Entity Recognition, Multilingual NLP (langdetect), Multimodal AI (Text + Image Reasoning), Semantic Search, Retrieval-Grounded Chatbots"),
        ("Backend &amp; Web Development", "FastAPI (ASGI), WebSockets, REST APIs, SQLAlchemy ORM, Pydantic, Flask, Streamlit, HTML, CSS, JavaScript (ES6+), Chart.js, Web Scraping"),
        ("Observability, Systems &amp; Linux", "CNCF Kepler (eBPF), Linux Kernel, Intel/AMD RAPL, Prometheus, Grafana, PromQL, Google OR-Tools (MILP), OpenCV, YOLOv8, Real-Time / Async Systems"),
        ("Databases &amp; DevOps", "PostgreSQL, TimescaleDB, SQLite, MySQL, Database Management Systems (DBMS), Docker, Docker Compose, Git, GitHub Actions, CI/CD, Render Cloud, Linux, Windows, Conda/Environment Management"),
        ("Domain &amp; Fintech Engineering", "Double-Entry Bookkeeping, ACID Transactions, SHA-256 Cryptography, Scope 2 Carbon Accounting, CEA India Grid Baseline, SEBI BRSR / ESG Compliance"),
        ("CS Core", "Data Structures &amp; Algorithms, Operating Systems, Computer Networks, Computer Architecture, Software Engineering, Theory of Computation, Object-Oriented Programming (OOP)"),
        ("UI / UX &amp; Interpersonal", "Figma (Basic), Wireframing, User-Centered Design, Problem Solving")
    ]
    for cat, items in skills:
        story.append(Paragraph(f"<b>{cat}:</b> {items}", style_body_p1))

    # 4. Projects (Section Header)
    story.extend(section_header_p1("PROJECTS"))

    # Project 1: Real-Time Gen AI Customer Service Bot
    p1_title = link("https://github.com/soham-092510/customer-service-chatbot-llm-internship/tree/main", "Real-Time Gen AI Customer Service Bot &mdash; 6-Feature LLM System")
    story.append(row(f"<b>{p1_title}</b>", "<i>ElevanceSkills Internship | 2026</i>", right_width=150))
    p1_bullets = [
        "Built and extended a retrieval-augmented customer service chatbot (Google Gemini + LangChain + FAISS) into 6 production-style AI systems on top of a shared architecture.",
        "<b>Sentiment-Aware Chatbot:</b> integrated VADER sentiment classification to detect customer emotion and dynamically adapt response tone in real time.",
        "<b>Medical Q&amp;A Chatbot:</b> built a custom XML parser to process 16,000+ MedQuAD Q&amp;A pairs; implemented FAISS-based retrieval and keyword-driven medical entity recognition (symptoms/treatments).",
        "<b>Dynamic Knowledge Base:</b> designed an incremental vector-index update mechanism to add new information without full re-embedding.",
        "<b>arXiv Research Assistant &amp; Multimodal Assistant:</b> built a live arXiv paper-search/summarization system with query-rewriting for follow-ups, plus a Gemini-powered text + image reasoning assistant with persistent conversational memory.",
        "<b>Multilingual Chatbot:</b> built automatic language detection and cross-lingual response generation (English, Hindi, Marathi, Spanish) with context retention across language switches."
    ]
    for b in p1_bullets:
        story.append(Paragraph(f"&bull;&nbsp; {b}", style_bullet_p1))

    # Project 2: Green-Finance
    p2_title = link("https://github.com/soham-092510/Green-Finance", "Green-Finance &mdash; Real-Time Energy &amp; Computational Carbon Observability for Financial Microservices")
    story.append(row(f"<b>{p2_title}</b>", "<i>Personal Project | 2026</i>", right_width=120))
    story.append(Paragraph(
        f'{link("https://github.com/soham-092510/Green-Finance", "GitHub")} &bull; '
        f'{link("https://green-finance.onrender.com", "Live Demo")} | '
        f'<i>Tech Stack: Python, FastAPI, SQLAlchemy, CNCF Kepler (eBPF), Prometheus, Grafana, Docker, SQLite/PostgreSQL, Chart.js</i>',
        style_subtitle
    ))
    p2_bullets = [
        "<b>Architected an Atomic Core Banking Engine:</b> Implemented double-entry bookkeeping (&Sigma; Debits &equiv; &Sigma; Credits) with pessimistic row-level database locking and sub-45ms latency across simulated inter-bank UPI/NEFT transfers.",
        "<b>Microsecond Hardware Energy Profiling:</b> Integrated CNCF Kepler eBPF telemetry to profile CPU/DRAM energy draw via Linux Intel/AMD RAPL hardware registers, attributing ~0.695 Joules per atomic transfer.",
        "<b>Engineered 96.2% Attribution Accuracy Model:</b> Implemented an energy conservation validation model (E_host = &Sigma; E_containers + E_idle + &Delta;E_residual) with an Exponential Moving Average (EMA, &alpha;=0.2) filter, achieving <b>96.2% attribution fidelity</b> and &le; 5.4% repeatability coefficient.",
        "<b>Statutory ESG Carbon Accounting &amp; Cryptographic Proof:</b> Automated Scope 2 emissions calculations using Central Electricity Authority (CEA) of India baseline factors (713.0 gCO<sub>2</sub>/kWh) and sealed every ledger transaction with immutable SHA-256 block hash chaining.",
        "<b>Full-Stack Enterprise Portals &amp; Telemetry Pipelines:</b> Built three decoupled web interfaces (Core Banking Portal, Sustainability Investigator, and 7-panel Grafana v11 Prometheus dashboard) with automated SEBI BRSR / RBI compliance PDF and CSV report exporters."
    ]
    for b in p2_bullets:
        story.append(Paragraph(f"&bull;&nbsp; {b}", style_bullet_p1))

    # =========================================================================
    # PAGE BREAK
    # =========================================================================
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2
    # =========================================================================
    
    # Project 3: Drive-Shield
    p3_title = link("https://github.com/soham-092510/Drive-Shield", "Drive-Shield &mdash; Real-Time Edge ADAS &amp; Incident Forensics Platform")
    story.append(row(f"<b>{p3_title}</b>", "<i>Personal Project | 2026</i>", right_width=120))
    story.append(Paragraph("<i>Tech Stack: Python, PyTorch, YOLOv8, OpenCV, FastAPI, WebSockets, SORT, SQLite, JavaScript</i>", style_subtitle))
    p3_bullets = [
        "Developed an edge-computing ADAS pipeline using YOLOv8 and SORT tracking, achieving 30 FPS inference (&lt;45ms latency) for multi-class obstacle detection, monocular depth estimation, and optical flow speed tracking.",
        "Engineered predictive risk algorithms evaluating Time-to-Collision (TTC &le; 2.0s), abrupt deceleration (&gt;6.5 m/s&sup2;), and pedestrian fall/tumble postures to trigger millisecond safety warnings.",
        "Built a FastAPI &amp; WebSocket dual-stream cockpit UI with an in-memory rolling buffer, automatically capturing and archiving 30-second pre/post-incident forensic video evidence signed with SHA-256 cryptographic hashes."
    ]
    for b in p3_bullets:
        story.append(Paragraph(f"&bull;&nbsp; {b}", style_bullet_p2))

    # Project 4: BIT-SHIELD
    p4_title = link("https://github.com/soham-092510/BIT", "BIT-SHIELD &mdash; Bitcoin Forensics &amp; Anomaly Detection Engine")
    story.append(row(f"<b>{p4_title}</b>", "<i>Personal Project | 2026</i>", right_width=120))
    story.append(Paragraph("<i>Tech Stack: Python, FastAPI, NetworkX, Scikit-Learn, React 18, TypeScript, Cytoscape.js, SQLite</i>", style_subtitle))
    p4_bullets = [
        "Engineered an air-gapped, zero-cloud Bitcoin transaction forensics platform featuring a universal offline data fabric with fuzzy regex schema normalization for arbitrary CSV/JSON datasets and automated SHA-256 chain-of-custody verification.",
        "Implemented an algorithmic graph mining engine detecting 8 behavioral money-laundering motifs (Rapid-Hop, CoinJoin mixing, Peel Chains, High Fan-Out/In) across directed bipartite transaction topologies (Address &harr; Transaction).",
        "Built a 5-lens risk fusion pipeline fusing deterministic rules (R1&ndash;R8) with unsupervised Isolation Forest scoring, generating explainable, court-admissible evidence chains.",
        "Designed an interactive SOC forensic workstation with Cytoscape.js supporting 4 dynamic graph layouts, live entity search, and 2x high-resolution PNG evidence export."
    ]
    for b in p4_bullets:
        story.append(Paragraph(f"&bull;&nbsp; {b}", style_bullet_p2))

    # Project 5: LearnLens AI
    p5_title = link("https://github.com/soham-092510/Transcript-Agent", "LearnLens AI &mdash; Multimodal Lecture Observation &amp; Knowledge Synthesis Agent")
    story.append(row(f"<b>{p5_title}</b>", "<i>Personal Project | 2026</i>", right_width=120))
    story.append(Paragraph(
        f'{link("https://github.com/soham-092510/Transcript-Agent", "GitHub")} &bull; '
        f'{link("https://transcript-agent-frontend.onrender.com/", "Live Demo")} &bull; '
        f'{link("https://transcript-agent-backend.onrender.com/", "Backend API")} &bull; '
        f'{link("https://transcript-agent-backend.onrender.com/docs", "API Docs")} | '
        f'<i>Tech Stack: React 19, TypeScript, FastAPI, WebSockets, Python, Faster-Whisper, OpenCV, Ollama/LLMs, ReportLab, python-pptx</i>',
        style_subtitle
    ))
    p5_bullets = [
        "Architected a real-time multimodal learning agent that observes user-authorized educational Chrome tabs (Coursera, YouTube, Udemy) and synthesizes grounded lecture slide decks, notes, and interactive quizzes.",
        "Engineered a dual client-server audio transcription pipeline using browser Web Speech STT and containerized Faster-Whisper (int8, VAD filtering), streaming timestamped transcripts over full-duplex WebSockets.",
        "Built a perceptual frame-extraction engine combining client-side difference hashing with OpenCV Hamming-distance comparison, cutting redundant frame transfer by 85% while capturing genuine slide transitions.",
        "Developed automated study-export generators with ReportLab and python-pptx, producing 16:9 slide decks, OCR annotations, and study packs with single-click download.",
        "Deployed full-stack cloud infrastructure via Render Blueprints, tuning SQLite (WAL mode, B-tree indices) for sub-millisecond query latency across 500+ session records."
    ]
    for b in p5_bullets:
        story.append(Paragraph(f"&bull;&nbsp; {b}", style_bullet_p2))

    # Project 6: GridPulse
    p6_title = link("https://github.com/soham-092510/GridPulse", "GridPulse (NeighbourFlex) &mdash; AI Energy Intelligence Platform")
    story.append(row(f"<b>{p6_title}</b>", "<i>Schneider Electric Challenge | 2026</i>", right_width=170))
    story.append(Paragraph(
        f'{link("https://github.com/soham-092510/GridPulse", "GitHub")} &bull; '
        f'{link("https://neighbourflex-frontend-538f.onrender.com/", "Live Demo")} &bull; '
        f'{link("https://neighbourflex-backend-538f.onrender.com/", "Backend API")} &bull; '
        f'{link("https://neighbourflex-backend-538f.onrender.com/docs", "API Docs")} &bull; '
        f'{link("https://github.com/soham-092510/GridPulse/blob/main/.github/workflows/ci.yml", "CI/CD Pipeline")} | '
        f'<i>Tech Stack: Python (FastAPI), TypeScript, React, Google OR-Tools, PostgreSQL/TimescaleDB, Docker, WebSockets</i>',
        style_subtitle
    ))
    p6_bullets = [
        "Built a real-time IoT energy-intelligence platform for the Schneider Electric Innovation Challenge (PS3) to ingest, validate, and optimize distributed energy assets (solar PV, EV fleets, 100 kWh BESS) across a 100-endpoint microgrid.",
        "Formulated a Mixed-Integer Linear Programming (MILP) model with Google OR-Tools to optimize multi-period battery dispatch and EV charge deferral, achieving 101.4% planned-vs-measured dispatch efficiency.",
        "Engineered an autoregressive multi-horizon forecasting engine (15m/1h/6h/24h) integrating live weather telemetry, achieving a 96.2% confidence score and 2.4 kW MAE (3.8% MAPE).",
        "Implemented a stratified baseline engine and multi-factor anomaly diagnostics that attribute demand spikes to heatwaves versus synchronized EV charging in real time.",
        "Designed an asynchronous FastAPI + SQLAlchemy (async) + WebSocket backend with sub-2s telemetry streaming, SlowAPI rate-limiting, Docker Compose packaging, and automated GitHub Actions CI/CD."
    ]
    for b in p6_bullets:
        story.append(Paragraph(f"&bull;&nbsp; {b}", style_bullet_p2))

    # Project 7 & 8: Earlier Projects
    p7_title = link("https://github.com/soham-092510/RAG-Based-AI-Teaching-Assistant", "RAG-Based AI Teaching Assistant")
    story.append(row(f"<b>{p7_title}</b>", "<i>Personal Project | 2025</i>", right_width=120))
    story.append(Paragraph("&bull;&nbsp; Built a Retrieval-Augmented Generation pipeline combining an LLM with vector-based retrieval to answer course questions grounded in uploaded study material, reducing hallucination and citing sources.", style_bullet_p2))

    p8_title = link("https://github.com/soham-092510/Hyper-Local-Deamnd-Forecasting", "HyperLocal Demand Forecaster V2")
    story.append(row(f"<b>{p8_title}</b>", "<i>Data Science Course Project | 2025</i>", right_width=170))
    story.append(Paragraph("&bull;&nbsp; Ensemble model (LightGBM + XGBoost + CatBoost) with Optuna hyperparameter tuning and Ridge meta-learner stacking.", style_bullet_p2))
    story.append(Paragraph("&bull;&nbsp; Built a SHAP explainability layer and Indian-festival-proximity features to capture local demand patterns.", style_bullet_p2))

    # Certifications & Courses
    story.extend(section_header_p2("CERTIFICATIONS &amp; COURSES"))
    story.append(row("<b>Real-Time Gen AI Project Internship &mdash; Customer Service Bot</b>", "<i>ElevanceSkills | Jul 2026</i>", right_width=140))
    story.append(Paragraph("&bull;&nbsp; Mentor-guided internship extending a base LLM chatbot into 6 production-style AI systems (sentiment analysis, medical Q&amp;A, dynamic knowledge base, research assistant, multimodal AI, multilingual support).", style_bullet_p2))
    story.append(Paragraph(
        f'&bull;&nbsp; Training Certificate: {link("https://www.elevanceskills.com/certificates/6a521666f2f606fb09475bea", "View Certificate")} &bull; '
        f'Internship Completion Certificate: {link("https://www.elevanceskills.com/certificates/6a55dcf6d8d2b182c913194a", "View Certificate")}',
        style_bullet_p2
    ))

    story.append(row("<b>Data Science with Python</b>", "<i>CodeWithHarry | Mar 2026</i>", right_width=130))
    story.append(Paragraph(
        f'&bull;&nbsp; Covered end-to-end data science workflows &mdash; EDA, ML model building with Scikit-learn, and reproducible research; hands-on with Pandas, NumPy, Matplotlib, neural networks, and LLM concepts. '
        f'Certificate: {link("https://drive.google.com/file/d/1kx4WPUlmNdJOGUsoOduBc3oISxOb48hV/view", "View Certificate")}',
        style_bullet_p2
    ))

    # Academic Highlights
    story.extend(section_header_p2("ACADEMIC HIGHLIGHTS"))
    story.append(Paragraph("&bull;&nbsp; <b>CGPA 8.09</b> in a competitive CSE program at SPIT &mdash; consistently pushing for higher scores.", style_bullet_p2))
    story.append(Paragraph("&bull;&nbsp; Strong in core subjects: Operating Systems, Computer Networks (subnetting, TCP/IP, routing), DAA, DBMS, Software Engineering, Theory of Computation.", style_bullet_p2))

    doc.build(story)

    # Validate page count with PyMuPDF
    res_doc = pymupdf.open(output_pdf)
    num_pages = len(res_doc)
    print(f"Generated PDF page count: {num_pages}")
    for i, page in enumerate(res_doc):
        rects = [b[:4] for b in page.get_text('blocks')]
        min_y = min(r[1] for r in rects) if rects else 0
        max_y = max(r[3] for r in rects) if rects else 0
        print(f"  Page {i+1}: min_y={min_y:.1f}, max_y={max_y:.1f}, height={page.rect.height:.1f}, bottom margin={page.rect.height - max_y:.1f} pt")
    return num_pages

if __name__ == '__main__':
    build_resume()
