"""
Generates the sample annual report used by this project:
data/veltrix_annual_report_fy2026.pdf

Veltrix Technologies Limited is a FICTIONAL company. All names, figures and
events are invented for demonstration. The numbers are internally consistent
(P&L, balance sheet and cash flow tie out) so the RAG system can be tested
on precise, verifiable questions.

Run:  python scripts/generate_report.py
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent.parent / "data" / "veltrix_annual_report_fy2026.pdf"
COMPANY = "Veltrix Technologies Limited"
NAVY = colors.HexColor("#1F3A5F")
LIGHT = colors.HexColor("#E8EEF5")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=20, textColor=NAVY, spaceAfter=10)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=13.5, textColor=NAVY, spaceBefore=8, spaceAfter=5)
BODY = ParagraphStyle("Body", parent=ss["BodyText"], fontSize=10.5, leading=15, spaceAfter=7)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=9, leading=12, textColor=colors.HexColor("#444444"))
QUOTE = ParagraphStyle("Quote", parent=BODY, fontSize=12, leading=17, textColor=NAVY,
                       leftIndent=12, borderPadding=6, fontName="Helvetica-Oblique")


def h1(t):
    return Paragraph(t, H1)


def h2(t):
    return Paragraph(t, H2)


def p(t):
    return Paragraph(t, BODY)


def bullets(items):
    return [Paragraph(f"&bull;&nbsp;&nbsp;{i}", BODY) for i in items]


def table(rows, widths=None, header=True):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    style = [
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4D2")),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    for r in range(1 if header else 0, len(rows)):
        if r % 2 == 0:
            style.append(("BACKGROUND", (0, r), (-1, r), LIGHT))
    t.setStyle(TableStyle(style))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    if doc.page > 1:
        canvas.drawString(18 * mm, 10 * mm, f"{COMPANY}  |  Annual Report 2025-26")
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build():
    s = []

    # ---------------- Page 1: Cover ----------------
    s += [Spacer(1, 70 * mm),
          Paragraph(COMPANY, ParagraphStyle("c1", parent=H1, fontSize=30, alignment=TA_CENTER, leading=36)),
          Spacer(1, 8 * mm),
          Paragraph("Annual Report 2025-26", ParagraphStyle("c2", parent=H1, fontSize=20, alignment=TA_CENTER, textColor=colors.HexColor("#4A6FA5"))),
          Spacer(1, 6 * mm),
          Paragraph("Engineering Intelligent Enterprises", ParagraphStyle("c3", parent=BODY, fontSize=14, alignment=TA_CENTER)),
          Spacer(1, 60 * mm),
          Paragraph("Financial year ended 31 March 2026<br/>Registered Office: Outer Ring Road, Bellandur, Bengaluru 560103, Karnataka, India<br/>CIN: L72200KA2004PLC034512",
                    ParagraphStyle("c4", parent=SMALL, alignment=TA_CENTER)),
          Spacer(1, 6 * mm),
          Paragraph("Note: Veltrix Technologies Limited is a fictional company created for a software demonstration project. All figures are illustrative.",
                    ParagraphStyle("c5", parent=SMALL, alignment=TA_CENTER, fontSize=8)),
          PageBreak()]

    # ---------------- Page 2: Contents ----------------
    s += [h1("Contents"),
          table([["Section", "Page"],
                 ["Financial Highlights", "3"], ["Chairman's Letter", "4"], ["Message from the CEO & Managing Director", "5"],
                 ["Company Overview", "7"], ["Board of Directors", "8"], ["Key Management Team", "9"],
                 ["Business Segment: Cloud & Infrastructure Services", "10"], ["Business Segment: Digital Engineering", "11"],
                 ["Business Segment: Enterprise Software Products", "12"], ["Clients and Geographies", "13"],
                 ["Acquisition of DataHarbor Analytics", "14"], ["Research, Innovation and Patents", "15"],
                 ["Our People", "16"], ["Sustainability and ESG", "17"], ["Corporate Social Responsibility", "18"],
                 ["Risk Management", "19"], ["Management Discussion and Analysis", "20"],
                 ["Corporate Governance Report", "22"], ["Statement of Profit and Loss", "23"], ["Balance Sheet", "24"],
                 ["Statement of Cash Flows", "25"], ["Notes to the Financial Statements", "26"],
                 ["Independent Auditor's Report", "27"], ["Shareholder Information and AGM Notice", "28"]],
                [130 * mm, 25 * mm]),
          PageBreak()]

    # ---------------- Page 3: Financial highlights ----------------
    s += [h1("Financial Highlights FY2025-26"),
          p("All amounts are in Indian Rupees crore (Rs. crore) unless otherwise stated. FY2025-26 refers to the financial "
            "year from 1 April 2025 to 31 March 2026 (also called FY26). FY2024-25 (FY25) is the comparative year."),
          table([["Metric", "FY2025-26", "FY2024-25", "Change"],
                 ["Revenue from operations", "4,820", "4,150", "+16.1%"],
                 ["EBITDA", "1,012", "830", "+21.9%"],
                 ["EBITDA margin", "21.0%", "20.0%", "+100 bps"],
                 ["Profit after tax (PAT)", "612", "498", "+22.9%"],
                 ["Earnings per share (Rs.)", "30.60", "24.90", "+22.9%"],
                 ["Total dividend per share (Rs.)", "9.00", "7.50", "+20.0%"],
                 ["Free cash flow", "535", "441", "+21.3%"],
                 ["Return on equity (ROE)", "16.8%", "15.2%", "+160 bps"],
                 ["Cash and cash equivalents", "1,240", "1,379", "-10.1%"],
                 ["Total debt", "180", "225", "-20.0%"],
                 ["Employees (year end)", "18,450", "16,900", "+9.2%"]],
                [70 * mm, 32 * mm, 32 * mm, 26 * mm]),
          Spacer(1, 6 * mm),
          h2("Quarterly revenue FY2025-26"),
          table([["Quarter", "Revenue (Rs. crore)", "QoQ growth"],
                 ["Q1 (Apr-Jun 2025)", "1,135", "-"],
                 ["Q2 (Jul-Sep 2025)", "1,190", "4.8%"],
                 ["Q3 (Oct-Dec 2025)", "1,228", "3.2%"],
                 ["Q4 (Jan-Mar 2026)", "1,267", "3.2%"]],
                [60 * mm, 45 * mm, 35 * mm]),
          Spacer(1, 4 * mm),
          p("Total contract value (TCV) of new deals signed during the year was Rs. 6,350 crore, the highest in the "
            "company's history, including four deals each above Rs. 400 crore."),
          PageBreak()]

    # ---------------- Page 4: Chairman ----------------
    s += [h1("Chairman's Letter"),
          p("Dear Shareholders,"),
          p("It is my privilege to present the twenty-second Annual Report of Veltrix Technologies Limited. FY2025-26 was a "
            "year in which enterprises across the world moved from experimenting with artificial intelligence to running it "
            "in production. Your company was ready for that shift. Revenue grew 16.1% to Rs. 4,820 crore and profit after "
            "tax rose 22.9% to Rs. 612 crore, while we continued to invest in our people, our platforms and our communities."),
          p("When Veltrix was founded in Bengaluru in 2004 with 14 engineers, our ambition was simple: to be the engineering "
            "partner our clients trust with their most complex problems. Twenty-two years later we serve 412 active clients "
            "in 31 countries with a team of 18,450 people. The principles have not changed. We still measure ourselves by "
            "the outcomes we create for clients and by the integrity with which we create them."),
          p("The Board approved a total dividend of Rs. 9.00 per equity share for the year, comprising an interim dividend "
            "of Rs. 3.00 paid in November 2025 and a final dividend of Rs. 6.00 recommended for approval at the Annual "
            "General Meeting. This represents a payout of 29.4% of earnings, in line with our capital allocation policy of "
            "returning 25% to 35% of annual profit to shareholders."),
          p("During the year we completed the acquisition of DataHarbor Analytics B.V. in the Netherlands, strengthening our "
            "data engineering capabilities in Europe. We also opened our new delivery centre in Pune, which can seat 4,000 "
            "professionals."),
          p("Governance remains the foundation of everything we do. Five of our nine directors are independent, and three "
            "of our directors are women. The Board met seven times during the year with an average attendance of 96%."),
          p("On behalf of the Board, I thank our clients, employees, shareholders and partners for their continued trust."),
          Spacer(1, 4 * mm),
          p("<b>Rajeev Malhotra</b><br/>Chairman<br/>Bengaluru, 12 May 2026"),
          PageBreak()]

    # ---------------- Pages 5-6: CEO ----------------
    s += [h1("Message from the CEO & Managing Director"),
          Paragraph("\"FY26 proved that disciplined execution and bold investment can go together.\"", QUOTE),
          p("Dear Shareholders,"),
          p("FY2025-26 was a record year for Veltrix on almost every measure. Revenue from operations grew 16.1% to "
            "Rs. 4,820 crore, EBITDA margin expanded by 100 basis points to 21.0%, and we signed new deals with a total "
            "contract value of Rs. 6,350 crore. Every one of our three business segments grew by double digits."),
          h2("What drove our growth"),
          p("Three trends shaped demand this year. First, clients accelerated the migration of core workloads to the cloud, "
            "and our Cloud & Infrastructure Services segment grew 14.6%. Second, product companies and manufacturers "
            "increased spending on software-defined products, lifting Digital Engineering by 17.8%. Third, our Enterprise "
            "Software Products segment, led by our VeltrixFlow workflow automation platform, grew 16.8% as more clients "
            "chose subscription licences."),
          p("Generative AI moved firmly into production. We delivered 140 generative AI projects during the year, up from "
            "38 in FY25, and certified 9,200 employees on our internal AI engineering curriculum. Our AI-assisted delivery "
            "toolkit, Veltrix Forge, is now used on 70% of active development projects and has improved developer "
            "productivity on measured projects by an average of 22%."),
          h2("Margins and cash"),
          p("EBITDA increased 21.9% to Rs. 1,012 crore. Margin expansion came mainly from a higher share of fixed-price "
            "and product revenue, better utilisation (which improved from 81% to 84%), and a lower subcontracting share. "
            "These gains more than offset annual salary increases that averaged 7.5% in India and 3.5% overseas."),
          p("Operating cash flow was Rs. 845 crore and free cash flow was Rs. 535 crore, a conversion of 87% of profit after "
            "tax. Days sales outstanding (DSO) improved from 84 days to 80 days."),
          PageBreak(),
          h2("Investing for the future"),
          p("We invested Rs. 265 crore in research and development, equal to 5.5% of revenue. Capital expenditure was "
            "Rs. 310 crore, most of which went into the new Pune campus in Hinjewadi and into GPU infrastructure for our "
            "AI Centre of Excellence. We also completed the acquisition of DataHarbor Analytics for EUR 42 million."),
          h2("Our people"),
          p("We ended the year with 18,450 employees, a net addition of 1,550. We welcomed 2,100 fresh graduates, and "
            "voluntary attrition declined from 16.2% to 13.8%. Women now make up 34% of our workforce and 24% of our "
            "senior leadership."),
          h2("Outlook for FY2026-27"),
          p("For FY2026-27 we expect revenue growth of 13% to 15% in constant currency and an EBITDA margin in the range "
            "of 20.5% to 21.5%. Our pipeline is healthy, but we remain watchful of macroeconomic uncertainty in Europe and "
            "of pricing pressure in traditional application maintenance work."),
          p("Our medium-term ambition, which we call Vision 2030, is to reach Rs. 10,000 crore in annual revenue by "
            "FY2029-30 while keeping EBITDA margin above 20%, and to derive at least 30% of revenue from AI-led services "
            "and platforms."),
          p("Thank you for your continued confidence in Veltrix."),
          Spacer(1, 4 * mm),
          p("<b>Ananya Krishnan</b><br/>Chief Executive Officer & Managing Director"),
          PageBreak()]

    # ---------------- Page 7: Company overview ----------------
    s += [h1("Company Overview"),
          p("Veltrix Technologies Limited is an information technology services and software products company "
            "headquartered in Bengaluru, India. The company was incorporated on 3 March 2004 and its equity shares are "
            "listed on the National Stock Exchange of India (NSE) and BSE Limited under the symbol VELTRIX (BSE scrip "
            "code 543921). The company was listed in October 2017."),
          h2("Vision and mission"),
          p("Our vision is to be the most trusted engineering partner for intelligent enterprises. Our mission is to help "
            "clients build, run and continuously improve the technology that powers their business, responsibly and at scale."),
          h2("At a glance"),
          table([["Fact", "Detail"],
                 ["Founded", "2004, Bengaluru"],
                 ["Employees", "18,450 as on 31 March 2026"],
                 ["Active clients", "412"],
                 ["Countries served", "31"],
                 ["Delivery centres", "9 (Bengaluru, Pune, Hyderabad, Chennai, Noida, Kraków, Rotterdam, Dallas, Manila)"],
                 ["Business segments", "3 (Cloud & Infrastructure, Digital Engineering, Enterprise Software Products)"],
                 ["Flagship product", "VeltrixFlow workflow automation platform"],
                 ["Stock symbol", "VELTRIX (NSE), 543921 (BSE)"]],
                [45 * mm, 115 * mm], header=True),
          Spacer(1, 4 * mm),
          h2("Milestones"),
          *bullets(["2004: Founded in Bengaluru by Rajeev Malhotra and Suresh Iyer with 14 engineers.",
                    "2011: Opened first overseas office in Dallas, United States.",
                    "2015: Launched VeltrixFlow, the company's first software product.",
                    "2017: Initial public offering on NSE and BSE.",
                    "2021: Crossed Rs. 2,000 crore in annual revenue.",
                    "2025: Opened Pune (Hinjewadi) campus and acquired DataHarbor Analytics, Netherlands."]),
          PageBreak()]

    # ---------------- Page 8: Board ----------------
    s += [h1("Board of Directors"),
          p("The Board of Directors consists of nine members: one executive director, three non-executive "
            "non-independent directors and five independent directors. Three of the nine directors are women."),
          table([["Name", "Designation", "Category"],
                 ["Rajeev Malhotra", "Chairman", "Non-Executive, Non-Independent (Co-founder)"],
                 ["Ananya Krishnan", "CEO & Managing Director", "Executive"],
                 ["Suresh Iyer", "Director", "Non-Executive, Non-Independent (Co-founder)"],
                 ["Dr. Meera Kulkarni", "Director", "Non-Executive, Non-Independent"],
                 ["Arvind Bhatnagar", "Lead Independent Director", "Independent"],
                 ["Farah Siddiqui", "Director", "Independent"],
                 ["Prof. Daniel Hart", "Director", "Independent"],
                 ["Kavita Raman", "Director", "Independent"],
                 ["Harish Chandra Gupta", "Director", "Independent"]],
                [45 * mm, 50 * mm, 70 * mm]),
          Spacer(1, 4 * mm),
          h2("Board committees"),
          *bullets(["Audit Committee: chaired by Arvind Bhatnagar; met 6 times.",
                    "Nomination and Remuneration Committee: chaired by Farah Siddiqui; met 4 times.",
                    "Risk Management Committee: chaired by Prof. Daniel Hart; met 4 times.",
                    "Corporate Social Responsibility and ESG Committee: chaired by Kavita Raman; met 3 times.",
                    "Stakeholders Relationship Committee: chaired by Harish Chandra Gupta; met 4 times."]),
          p("Ananya Krishnan was appointed CEO & Managing Director with effect from 1 April 2022. She previously led the "
            "company's Digital Engineering business and joined Veltrix in 2009."),
          PageBreak()]

    # ---------------- Page 9: Key management ----------------
    s += [h1("Key Management Team"),
          table([["Name", "Role", "With Veltrix since"],
                 ["Ananya Krishnan", "Chief Executive Officer & Managing Director", "2009"],
                 ["Vikram Sethi", "Chief Financial Officer", "2019"],
                 ["Neha Bansal", "Chief Operating Officer", "2012"],
                 ["Rohan D'Souza", "Chief Technology Officer", "2016"],
                 ["Lakshmi Venkatesh", "Chief People Officer", "2020"],
                 ["Martin Fischer", "President, Europe", "2026 (via DataHarbor)"],
                 ["Karthik Subramanian", "President, North America", "2014"],
                 ["Pooja Nair", "Company Secretary & Compliance Officer", "2018"]],
                [45 * mm, 80 * mm, 40 * mm]),
          Spacer(1, 4 * mm),
          p("During the year, Martin Fischer, the founder and former CEO of DataHarbor Analytics, joined the management "
            "team as President, Europe with effect from 1 January 2026. Rohan D'Souza leads the AI Centre of Excellence in "
            "addition to his role as Chief Technology Officer."),
          p("The remuneration of the CEO & Managing Director for FY2025-26 was Rs. 14.2 crore, including fixed pay of "
            "Rs. 5.8 crore and performance-linked variable pay of Rs. 8.4 crore. The ratio of CEO remuneration to the median "
            "employee remuneration was 142:1."),
          PageBreak()]

    # ---------------- Pages 10-12: Segments ----------------
    s += [h1("Business Segment: Cloud & Infrastructure Services"),
          p("Cloud & Infrastructure Services (CIS) is our largest segment. It helps clients migrate applications and data to "
            "public and hybrid clouds, modernise data centres, and run infrastructure through managed services and "
            "site reliability engineering."),
          table([["Metric", "FY2025-26", "FY2024-25"],
                 ["Segment revenue (Rs. crore)", "2,120", "1,850"],
                 ["Share of total revenue", "44%", "45%"],
                 ["Revenue growth", "14.6%", "11.2%"],
                 ["Segment operating margin", "19.4%", "18.9%"],
                 ["Employees", "8,300", "7,700"]],
                [70 * mm, 40 * mm, 40 * mm]),
          Spacer(1, 4 * mm),
          p("Key wins during the year included a five-year managed cloud services contract with a large North American "
            "health insurer valued at Rs. 780 crore, the largest single deal in the company's history, and a data centre "
            "exit programme for a European logistics company."),
          p("The segment holds premier partner status with all three major hyperscale cloud providers. Our FinOps practice "
            "helped clients reduce cloud spending by an average of 27% on engagements completed during the year."),
          PageBreak(),
          h1("Business Segment: Digital Engineering"),
          p("Digital Engineering (DE) designs and builds software-defined products, embedded systems, connected devices and "
            "digital customer experiences for product companies, manufacturers and automotive firms."),
          table([["Metric", "FY2025-26", "FY2024-25"],
                 ["Segment revenue (Rs. crore)", "1,590", "1,350"],
                 ["Share of total revenue", "33%", "33%"],
                 ["Revenue growth", "17.8%", "15.0%"],
                 ["Segment operating margin", "20.6%", "19.8%"],
                 ["Employees", "6,450", "5,850"]],
                [70 * mm, 40 * mm, 40 * mm]),
          Spacer(1, 4 * mm),
          p("Automotive software was the fastest-growing practice within the segment, growing 31% during the year, driven "
            "by software-defined vehicle programmes for two European car makers. Our medical devices engineering practice "
            "received ISO 13485 certification in September 2025."),
          PageBreak(),
          h1("Business Segment: Enterprise Software Products"),
          p("Enterprise Software Products (ESP) develops and sells the company's own software. The flagship product is "
            "VeltrixFlow, a low-code workflow automation platform used by banks, insurers and government agencies. The "
            "segment also includes VeltrixInsight, an analytics product, and Veltrix Forge, the AI-assisted delivery toolkit "
            "that is used internally and licensed to selected clients."),
          table([["Metric", "FY2025-26", "FY2024-25"],
                 ["Segment revenue (Rs. crore)", "1,110", "950"],
                 ["Share of total revenue", "23%", "23%"],
                 ["Revenue growth", "16.8%", "18.5%"],
                 ["Segment operating margin", "28.1%", "26.5%"],
                 ["Subscription share of segment revenue", "68%", "61%"],
                 ["Annual recurring revenue (ARR)", "Rs. 760 crore", "Rs. 590 crore"]],
                [70 * mm, 40 * mm, 40 * mm]),
          Spacer(1, 4 * mm),
          p("VeltrixFlow added 46 new enterprise customers during the year, taking its customer base to 318. Net revenue "
            "retention for subscription customers was 118%. Version 9 of VeltrixFlow, released in February 2026, introduced "
            "AI agents that can draft, route and approve routine workflow steps under human supervision."),
          PageBreak()]

    # ---------------- Page 13: Clients & geographies ----------------
    s += [h1("Clients and Geographies"),
          h2("Revenue by geography"),
          table([["Region", "Share of revenue FY26", "Share of revenue FY25", "Growth FY26"],
                 ["North America", "52%", "54%", "11.8%"],
                 ["Europe", "27%", "24%", "30.7%"],
                 ["India", "14%", "14%", "16.2%"],
                 ["Rest of World", "7%", "8%", "1.6%"]],
                [45 * mm, 40 * mm, 40 * mm, 30 * mm]),
          Spacer(1, 3 * mm),
          p("Europe was the fastest-growing region, helped by the DataHarbor acquisition, which contributed Rs. 96 crore of "
            "revenue in the four and a half months after closing. Excluding DataHarbor, Europe grew 21.3%."),
          h2("Revenue by industry"),
          table([["Industry", "Share of revenue FY26"],
                 ["Banking, financial services and insurance (BFSI)", "34%"],
                 ["Healthcare and life sciences", "18%"],
                 ["Manufacturing and automotive", "17%"],
                 ["Retail and consumer", "12%"],
                 ["Communications and media", "10%"],
                 ["Public sector and others", "9%"]],
                [100 * mm, 45 * mm]),
          Spacer(1, 3 * mm),
          h2("Client metrics"),
          *bullets(["Active clients: 412 (FY25: 376).",
                    "Clients contributing more than Rs. 50 crore of annual revenue: 21 (FY25: 17).",
                    "Clients contributing more than Rs. 10 crore of annual revenue: 84 (FY25: 72).",
                    "Revenue from the top 10 clients: 31% of total revenue (FY25: 33%).",
                    "Revenue from the single largest client: 6.2% of total revenue.",
                    "Repeat business: 91% of revenue came from clients who were also clients in the previous year."]),
          PageBreak()]

    # ---------------- Page 14: Acquisition ----------------
    s += [h1("Acquisition of DataHarbor Analytics"),
          p("On 14 November 2025, Veltrix completed the acquisition of 100% of the share capital of DataHarbor Analytics "
            "B.V., a data engineering and analytics consultancy headquartered in Rotterdam, the Netherlands. The total "
            "purchase consideration was EUR 42 million (approximately Rs. 385 crore), paid entirely in cash from internal "
            "accruals. An additional earn-out of up to EUR 6 million may be payable over two years, subject to revenue and "
            "client-retention targets."),
          h2("About DataHarbor"),
          p("DataHarbor was founded in 2013 by Martin Fischer. At the time of acquisition it had 420 employees across "
            "Rotterdam and Kraków and served 35 clients, mainly in logistics, energy and retail. Its revenue for calendar "
            "year 2024 was EUR 31 million."),
          h2("Strategic rationale"),
          *bullets(["Adds deep data platform and data governance expertise in continental Europe.",
                    "Gives Veltrix a near-shore delivery centre in Kraków, Poland, for European clients.",
                    "Brings eight new enterprise clients with strong cross-selling potential for VeltrixFlow.",
                    "Supports the Vision 2030 goal of growing Europe to one-third of company revenue."]),
          h2("Accounting impact"),
          p("The acquisition resulted in goodwill of Rs. 228 crore and customer-related intangible assets of Rs. 96 crore, "
            "which are being amortised over seven years. Integration costs of Rs. 11 crore were charged to the statement of "
            "profit and loss during the year. The integration is expected to be completed by September 2026."),
          PageBreak()]

    # ---------------- Page 15: R&D ----------------
    s += [h1("Research, Innovation and Patents"),
          p("Research and development spending in FY2025-26 was Rs. 265 crore, equal to 5.5% of revenue (FY25: Rs. 212 "
            "crore, 5.1% of revenue). Of this amount, Rs. 58 crore was capitalised as product development cost and the rest "
            "was expensed."),
          h2("AI Centre of Excellence"),
          p("The AI Centre of Excellence, established in Bengaluru in 2023, has 620 specialists working on applied machine "
            "learning, generative AI, model evaluation and AI safety. During the year it built a private GPU cluster with "
            "512 GPUs to support fine-tuning and evaluation of models for clients that cannot send data to public services."),
          p("The Centre published a Responsible AI framework that every client AI project must follow. It requires bias "
            "testing, human oversight for consequential decisions, documentation of training data sources and a red-team "
            "review before production release."),
          h2("Intellectual property"),
          table([["Patents", "FY2025-26", "Cumulative"],
                 ["Patent applications filed", "47", "238"],
                 ["Patents granted", "19", "112"]],
                [60 * mm, 35 * mm, 35 * mm]),
          Spacer(1, 3 * mm),
          p("Patents granted during the year included methods for automated cloud cost optimisation, privacy-preserving "
            "document extraction and agent-based workflow orchestration."),
          h2("Academic partnerships"),
          p("Veltrix funds research collaborations with IISc Bengaluru, IIT Madras and Delft University of Technology. In "
            "FY26 these partnerships supported 14 research projects and 22 PhD fellowships."),
          PageBreak()]

    # ---------------- Page 16: People ----------------
    s += [h1("Our People"),
          table([["People metric", "FY2025-26", "FY2024-25"],
                 ["Total employees", "18,450", "16,900"],
                 ["Fresh graduates hired", "2,100", "1,650"],
                 ["Voluntary attrition", "13.8%", "16.2%"],
                 ["Women in workforce", "34%", "32%"],
                 ["Women in senior leadership", "24%", "21%"],
                 ["Average training hours per employee", "46", "41"],
                 ["Employees certified in AI engineering", "9,200", "3,100"],
                 ["Utilisation (excluding trainees)", "84%", "81%"],
                 ["Employee engagement score", "78/100", "74/100"],
                 ["Nationalities", "38", "33"]],
                [80 * mm, 35 * mm, 35 * mm]),
          Spacer(1, 4 * mm),
          p("Total employee benefit expense for the year was Rs. 2,700 crore, which is 56.0% of revenue. Average salary "
            "increases were 7.5% for employees in India and 3.5% for employees overseas, effective 1 July 2025."),
          p("The Veltrix Learning Academy launched a 12-week AI engineering programme for all new hires. The company also "
            "introduced a hybrid work policy under which most employees work from an office three days a week."),
          p("Under the Employee Stock Option Plan 2023, 1.2 million options were granted to 640 employees during the year."),
          PageBreak()]

    # ---------------- Page 17: ESG ----------------
    s += [h1("Sustainability and ESG"),
          p("Veltrix has committed to reaching net zero greenhouse gas emissions across Scope 1, 2 and 3 by 2040, with an "
            "interim target of reducing Scope 1 and Scope 2 emissions by 60% by 2030 against a FY2022 baseline."),
          table([["Environmental metric", "FY2025-26", "FY2024-25"],
                 ["Scope 1 + 2 emissions (tCO2e)", "21,400", "26,100"],
                 ["Scope 3 emissions (tCO2e)", "88,900", "84,300"],
                 ["Renewable share of electricity", "62%", "48%"],
                 ["Water consumption (megalitres)", "312", "298"],
                 ["Waste recycled", "81%", "76%"]],
                [80 * mm, 35 * mm, 35 * mm]),
          Spacer(1, 4 * mm),
          p("Scope 1 and 2 emissions fell 18% compared with FY25, mainly because of a new 14 MW solar power purchase "
            "agreement in Karnataka and the move to a LEED Platinum certified campus in Pune. Scope 3 emissions rose 5.5% "
            "because of increased business travel and higher purchased cloud capacity."),
          h2("Social and governance highlights"),
          *bullets(["Zero data breaches resulting in regulatory penalties during the year.",
                    "ISO 27001 and SOC 2 Type II certifications maintained across all delivery centres.",
                    "MSCI ESG rating upgraded from A to AA in January 2026.",
                    "100% of employees completed the annual code of conduct and data privacy training."]),
          PageBreak()]

    # ---------------- Page 18: CSR ----------------
    s += [h1("Corporate Social Responsibility"),
          p("Under Section 135 of the Companies Act, 2013, Veltrix is required to spend at least 2% of its average net "
            "profit of the three preceding financial years on CSR activities. The prescribed amount for FY2025-26 was "
            "Rs. 12.9 crore. The company spent Rs. 13.1 crore during the year through the Veltrix Foundation."),
          table([["CSR programme", "Spend (Rs. crore)"],
                 ["Code for Tomorrow (digital skills for government school students)", "5.4"],
                 ["Women in Tech scholarships", "2.8"],
                 ["Primary healthcare in rural Karnataka", "2.6"],
                 ["Lake restoration in Bengaluru", "1.5"],
                 ["Disaster relief and other programmes", "0.8"],
                 ["Total", "13.1"]],
                [115 * mm, 40 * mm]),
          Spacer(1, 4 * mm),
          p("The Code for Tomorrow programme reached 64,000 students in 410 government schools across Karnataka, "
            "Maharashtra and Tamil Nadu. The Women in Tech scholarship supported 1,150 women engineering students. Under the "
            "lake restoration programme, the Foundation completed the restoration of Kaikondrahalli lake in partnership with "
            "a local citizens' trust."),
          p("Employees volunteered more than 52,000 hours during the year through the company's Give an Hour programme."),
          PageBreak()]

    # ---------------- Page 19: Risk ----------------
    s += [h1("Risk Management"),
          p("The Risk Management Committee of the Board reviews the enterprise risk register every quarter. The principal "
            "risks and their mitigations are summarised below."),
          table([["Risk", "Description", "Mitigation"],
                 [Paragraph("Client concentration", SMALL), Paragraph("Top 10 clients provide 31% of revenue; loss of a large client could hurt growth.", SMALL), Paragraph("Broaden client base; no client above 7% of revenue; multi-year contracts.", SMALL)],
                 [Paragraph("Currency", SMALL), Paragraph("About 86% of revenue is earned in foreign currencies, mainly USD and EUR.", SMALL), Paragraph("Rolling hedge programme covering 12 months of net exposure; hedges outstanding of USD 410 million at year end.", SMALL)],
                 [Paragraph("Talent", SMALL), Paragraph("Shortage of skilled AI and cloud engineers; wage inflation.", SMALL), Paragraph("Campus hiring, Learning Academy, ESOPs, career frameworks.", SMALL)],
                 [Paragraph("Cybersecurity", SMALL), Paragraph("Breach of client or company data could cause legal and reputational damage.", SMALL), Paragraph("24x7 security operations centre, zero-trust architecture, annual third-party penetration tests.", SMALL)],
                 [Paragraph("AI disruption", SMALL), Paragraph("AI tools may reduce demand for traditional effort-based services.", SMALL), Paragraph("Shift to outcome-based pricing; invest in AI platforms such as Veltrix Forge.", SMALL)],
                 [Paragraph("Regulatory", SMALL), Paragraph("Changes in data protection, immigration and tax laws in key markets.", SMALL), Paragraph("Global compliance team; monitoring of EU AI Act and India's DPDP Act.", SMALL)]],
                [32 * mm, 62 * mm, 70 * mm]),
          Spacer(1, 4 * mm),
          p("A one rupee movement in the USD/INR exchange rate affects annual operating margin by approximately 25 basis "
            "points, before hedging. The average USD/INR rate realised during FY26 was 85.9 (FY25: 83.6)."),
          PageBreak()]

    # ---------------- Pages 20-21: MD&A ----------------
    s += [h1("Management Discussion and Analysis"),
          h2("Industry overview"),
          p("Global technology services spending grew an estimated 7% in calendar year 2025, according to industry "
            "estimates. Spending on cloud, data and AI services grew faster than the overall market, while demand for "
            "traditional application maintenance was flat. The Indian IT services industry recorded revenue growth of "
            "about 6% in USD terms during the year."),
          h2("Revenue"),
          p("Revenue from operations increased 16.1% from Rs. 4,150 crore to Rs. 4,820 crore. In constant currency terms, "
            "revenue grew 13.4%; the remaining 2.7 percentage points came from the depreciation of the rupee against the "
            "US dollar and euro. Organic constant-currency growth, excluding DataHarbor, was 11.1%."),
          p("Fixed-price contracts made up 58% of services revenue (FY25: 54%), and time-and-material contracts made up the rest."),
          h2("Expenses"),
          table([["Expense (Rs. crore)", "FY2025-26", "% of revenue", "FY2024-25", "% of revenue"],
                 ["Employee benefit expense", "2,700", "56.0%", "2,340", "56.4%"],
                 ["Subcontracting cost", "410", "8.5%", "365", "8.8%"],
                 ["Other expenses", "698", "14.5%", "615", "14.8%"],
                 ["Depreciation and amortisation", "176", "3.7%", "148", "3.6%"],
                 ["Finance costs", "14", "0.3%", "16", "0.4%"]],
                [55 * mm, 26 * mm, 24 * mm, 26 * mm, 24 * mm]),
          Spacer(1, 3 * mm),
          p("Other expenses include travel of Rs. 118 crore, software licences and cloud costs of Rs. 164 crore, facility "
            "costs of Rs. 132 crore, and the Rs. 11 crore of DataHarbor integration costs."),
          PageBreak(),
          h2("Profitability"),
          p("EBITDA rose 21.9% to Rs. 1,012 crore and EBITDA margin improved from 20.0% to 21.0%. Profit before tax was "
            "Rs. 886 crore. The effective tax rate was 30.9% (FY25: 30.6%). Profit after tax increased 22.9% to Rs. 612 crore, "
            "and the net profit margin was 12.7%."),
          h2("Key financial ratios"),
          table([["Ratio", "FY2025-26", "FY2024-25"],
                 ["Return on equity", "16.8%", "15.2%"],
                 ["Return on capital employed", "22.4%", "20.7%"],
                 ["Net profit margin", "12.7%", "12.0%"],
                 ["Debt to equity", "0.05", "0.07"],
                 ["Current ratio", "2.73", "2.58"],
                 ["Days sales outstanding (DSO)", "80 days", "84 days"],
                 ["Interest coverage", "64.3x", "45.9x"]],
                [80 * mm, 35 * mm, 35 * mm]),
          Spacer(1, 3 * mm),
          p("Return on equity improved because profit grew faster than average equity. The current ratio is calculated as "
            "total current assets of Rs. 3,260 crore divided by total current liabilities of Rs. 1,195 crore."),
          h2("Capital allocation"),
          p("Our capital allocation policy prioritises investment in organic growth, followed by strategic acquisitions, "
            "and then shareholder returns. We aim to return 25% to 35% of annual profit after tax to shareholders through "
            "dividends. We do not plan a share buyback in FY2026-27."),
          PageBreak()]

    # ---------------- Page 22: Governance ----------------
    s += [h1("Corporate Governance Report"),
          p("Veltrix complies with the corporate governance requirements of the SEBI (Listing Obligations and Disclosure "
            "Requirements) Regulations, 2015. The Board met seven times during FY2025-26, on 9 May 2025, 24 July 2025, "
            "28 August 2025, 23 October 2025, 13 November 2025, 22 January 2026 and 19 March 2026. Average attendance was 96%."),
          h2("Shareholding pattern as on 31 March 2026"),
          table([["Category", "Shareholding"],
                 ["Promoters and promoter group", "38.4%"],
                 ["Foreign portfolio investors", "24.7%"],
                 ["Mutual funds and insurance companies", "21.3%"],
                 ["Retail and individual investors", "11.9%"],
                 ["Others (including employee trust)", "3.7%"],
                 ["Total", "100.0%"]],
                [90 * mm, 40 * mm]),
          Spacer(1, 3 * mm),
          p("The promoters have not pledged any of their shares. The company has 20 crore (200 million) equity shares of "
            "face value Rs. 10 each outstanding."),
          h2("Whistle-blower and ethics"),
          p("The company received 37 complaints under its whistle-blower policy during the year, of which 33 were "
            "investigated and closed and 4 were under investigation at year end. No complaint involved a member of the Board."),
          PageBreak()]

    # ---------------- Page 23: P&L ----------------
    s += [h1("Statement of Profit and Loss"),
          p("Consolidated statement of profit and loss for the year ended 31 March 2026 (Rs. crore)"),
          table([["Particulars", "FY2025-26", "FY2024-25"],
                 ["Revenue from operations", "4,820.0", "4,150.0"],
                 ["Other income", "64.0", "52.0"],
                 ["Total income", "4,884.0", "4,202.0"],
                 ["Employee benefit expense", "2,700.0", "2,340.0"],
                 ["Subcontracting cost", "410.0", "365.0"],
                 ["Other expenses", "698.0", "615.0"],
                 ["EBITDA (revenue less operating expenses)", "1,012.0", "830.0"],
                 ["Depreciation and amortisation", "176.0", "148.0"],
                 ["Finance costs", "14.0", "16.0"],
                 ["Profit before tax", "886.0", "718.0"],
                 ["Current tax", "289.0", "231.0"],
                 ["Deferred tax", "(15.0)", "(11.0)"],
                 ["Total tax expense", "274.0", "220.0"],
                 ["Profit for the year", "612.0", "498.0"],
                 ["Other comprehensive income, net of tax", "28.0", "(9.0)"],
                 ["Total comprehensive income", "640.0", "489.0"],
                 ["Basic and diluted EPS (Rs.)", "30.60", "24.90"]],
                [95 * mm, 32 * mm, 32 * mm]),
          Spacer(1, 3 * mm),
          p("Other income consists mainly of interest on bank deposits and gains on mutual fund investments. Other "
            "comprehensive income for FY26 includes a gain of Rs. 22 crore on cash flow hedges."),
          PageBreak()]

    # ---------------- Page 24: Balance sheet ----------------
    s += [h1("Balance Sheet"),
          p("Consolidated balance sheet as at 31 March 2026 (Rs. crore)"),
          table([["Particulars", "31 Mar 2026", "31 Mar 2025"],
                 ["Property, plant and equipment", "920", "760"],
                 ["Goodwill", "610", "382"],
                 ["Other intangible assets", "285", "190"],
                 ["Right-of-use assets", "240", "205"],
                 ["Other non-current assets", "195", "170"],
                 ["Total non-current assets", "2,250", "1,707"],
                 ["Trade receivables", "1,060", "955"],
                 ["Unbilled revenue", "330", "290"],
                 ["Cash and cash equivalents", "1,240", "1,379"],
                 ["Current investments", "420", "360"],
                 ["Other current assets", "210", "176"],
                 ["Total current assets", "3,260", "3,160"],
                 ["TOTAL ASSETS", "5,510", "4,867"],
                 ["Equity share capital", "200", "200"],
                 ["Other equity", "3,690", "3,210"],
                 ["Total equity", "3,890", "3,410"],
                 ["Non-current borrowings", "120", "160"],
                 ["Non-current lease liabilities", "210", "180"],
                 ["Other non-current liabilities", "95", "92"],
                 ["Current borrowings", "60", "65"],
                 ["Trade payables", "410", "370"],
                 ["Current lease liabilities", "45", "40"],
                 ["Other current liabilities", "520", "460"],
                 ["Provisions", "160", "90"],
                 ["Total current liabilities", "1,195", "1,225"],
                 ["TOTAL EQUITY AND LIABILITIES", "5,510", "4,867"]],
                [95 * mm, 32 * mm, 32 * mm]),
          PageBreak()]

    # ---------------- Page 25: Cash flow ----------------
    s += [h1("Statement of Cash Flows"),
          p("Consolidated statement of cash flows for the year ended 31 March 2026 (Rs. crore)"),
          table([["Particulars", "FY2025-26", "FY2024-25"],
                 ["Profit before tax", "886", "718"],
                 ["Adjustments for depreciation, finance costs and other non-cash items", "142", "120"],
                 ["Changes in working capital", "(4)", "(38)"],
                 ["Income taxes paid", "(179)", "(173)"],
                 ["Net cash from operating activities (A)", "845", "627"],
                 ["Purchase of property, plant and equipment and intangibles", "(310)", "(186)"],
                 ["Acquisition of DataHarbor Analytics, net of cash acquired", "(385)", "-"],
                 ["Net purchase of current investments", "(60)", "(45)"],
                 ["Interest received", "40", "34"],
                 ["Net cash used in investing activities (B)", "(715)", "(197)"],
                 ["Dividends paid", "(160)", "(130)"],
                 ["Net repayment of borrowings", "(45)", "(40)"],
                 ["Payment of lease liabilities", "(50)", "(44)"],
                 ["Interest paid", "(14)", "(16)"],
                 ["Net cash used in financing activities (C)", "(269)", "(230)"],
                 ["Net change in cash (A+B+C)", "(139)", "200"],
                 ["Cash and cash equivalents at beginning of year", "1,379", "1,179"],
                 ["Cash and cash equivalents at end of year", "1,240", "1,379"]],
                [105 * mm, 28 * mm, 28 * mm]),
          Spacer(1, 3 * mm),
          p("Free cash flow, defined as net cash from operating activities less capital expenditure, was Rs. 535 crore "
            "(Rs. 845 crore minus Rs. 310 crore). Cash declined during the year mainly because of the cash payment for "
            "the DataHarbor acquisition."),
          PageBreak()]

    # ---------------- Page 26: Notes ----------------
    s += [h1("Notes to the Financial Statements"),
          h2("Note 1: Basis of preparation"),
          p("The consolidated financial statements are prepared in accordance with Indian Accounting Standards (Ind AS) "
            "notified under the Companies Act, 2013. The group comprises Veltrix Technologies Limited and its eleven "
            "subsidiaries, including DataHarbor Analytics B.V. from 14 November 2025."),
          h2("Note 2: Revenue recognition"),
          p("Revenue from time-and-material contracts is recognised as services are performed. Revenue from fixed-price "
            "contracts is recognised using the percentage-of-completion method based on costs incurred. Subscription "
            "revenue for VeltrixFlow is recognised evenly over the subscription period."),
          h2("Note 3: Goodwill"),
          p("Goodwill increased from Rs. 382 crore to Rs. 610 crore, an increase of Rs. 228 crore arising from the "
            "acquisition of DataHarbor Analytics. Goodwill is tested for impairment annually; no impairment was required "
            "for FY2025-26."),
          h2("Note 4: Borrowings"),
          p("Total borrowings of Rs. 180 crore consist of a term loan taken in 2022 to fund the Hyderabad campus. The loan "
            "carries an interest rate of 7.9% per annum and is repayable in quarterly instalments ending in June 2029."),
          h2("Note 5: Contingent liabilities"),
          p("Contingent liabilities not provided for amount to Rs. 74 crore, mainly relating to income tax demands under "
            "appeal. Management believes these demands are not sustainable."),
          h2("Note 6: Events after the reporting period"),
          p("On 28 April 2026, the company signed a definitive agreement to set up a new delivery centre in Coimbatore, "
            "Tamil Nadu, with an initial capacity of 1,500 seats, expected to be operational in the third quarter of "
            "FY2026-27."),
          PageBreak()]

    # ---------------- Page 27: Auditor ----------------
    s += [h1("Independent Auditor's Report"),
          p("To the Members of Veltrix Technologies Limited"),
          h2("Opinion"),
          p("We have audited the consolidated financial statements of Veltrix Technologies Limited and its subsidiaries, "
            "which comprise the consolidated balance sheet as at 31 March 2026, the consolidated statement of profit and "
            "loss, the statement of changes in equity and the statement of cash flows for the year then ended, and notes "
            "to the financial statements."),
          p("In our opinion, the consolidated financial statements give a true and fair view in conformity with Ind AS and "
            "other accounting principles generally accepted in India. Our opinion is unmodified."),
          h2("Key audit matters"),
          *bullets(["Revenue recognition on fixed-price contracts, because estimating costs to complete requires significant judgement.",
                    "Purchase price allocation for the acquisition of DataHarbor Analytics, including valuation of customer-related intangible assets.",
                    "Evaluation of uncertain tax positions and contingent liabilities."]),
          p("The audit fee for FY2025-26 was Rs. 2.4 crore."),
          Spacer(1, 4 * mm),
          p("<b>For Mehta Srinivasan & Co.</b><br/>Chartered Accountants<br/>Firm Registration No. 104582W<br/><br/>"
            "Ramesh Srinivasan, Partner<br/>Membership No. 058213<br/>Bengaluru, 12 May 2026"),
          PageBreak()]

    # ---------------- Page 28: Shareholder info ----------------
    s += [h1("Shareholder Information and AGM Notice"),
          h2("Annual General Meeting"),
          p("The 22nd Annual General Meeting of Veltrix Technologies Limited will be held on Friday, 14 August 2026 at "
            "11:00 a.m. IST through video conference. The record date for the final dividend is 31 July 2026, and the "
            "final dividend of Rs. 6.00 per share, if approved, will be paid on or after 19 August 2026."),
          h2("Dividend history"),
          table([["Financial year", "Dividend per share (Rs.)"],
                 ["FY2021-22", "5.00"], ["FY2022-23", "6.00"], ["FY2023-24", "6.50"],
                 ["FY2024-25", "7.50"], ["FY2025-26", "9.00"]],
                [60 * mm, 50 * mm]),
          Spacer(1, 3 * mm),
          h2("Share price data (NSE)"),
          p("During FY2025-26 the share price reached a high of Rs. 1,184 on 6 February 2026 and a low of Rs. 812 on "
            "7 April 2025. The closing price on 31 March 2026 was Rs. 1,096, giving a market capitalisation of about "
            "Rs. 21,920 crore."),
          h2("Investor contacts"),
          p("Registrar and share transfer agent: KFin Technologies Limited, Hyderabad.<br/>"
            "Investor relations: investors@veltrix.example<br/>"
            "Company Secretary: Pooja Nair, Veltrix Technologies Limited, Outer Ring Road, Bellandur, Bengaluru 560103."),
          p("Shareholders are encouraged to register their email addresses with their depository participants to receive "
            "communications electronically.")]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm,
                            title="Veltrix Technologies Limited - Annual Report 2025-26",
                            author="Veltrix Technologies Limited (fictional)")
    doc.build(s, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
