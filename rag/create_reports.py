from fpdf import FPDF
import os

os.makedirs("data/reports", exist_ok=True)

def create_pdf(filename, title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", size=11)
    for paragraph in content:
        safe = paragraph.replace("\u2014", "-").replace("\u2013", "-").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
        pdf.multi_cell(0, 7, safe)
        pdf.ln(3)
    pdf.output(f"data/reports/{filename}")
    print(f"Created {filename}")

# Report 1 — Q1 2017
create_pdf("q1_2017_report.pdf", "Olist Q1 2017 Business Report", [
    "Executive Summary",
    "Q1 2017 marked the early growth phase for Olist's e-commerce platform. Total orders for the quarter reached approximately 3,000, with January recording the lowest volume at 800 orders. The platform was still establishing its seller network and customer base during this period.",
    "Sales Performance",
    "Revenue growth was modest in Q1 2017. The bed and bath category (cama_mesa_banho) showed early dominance with consistent order volumes. Health and beauty products also performed well, indicating strong consumer demand in personal care segments. Average order value was approximately R$150.",
    "Operational Insights",
    "Delivery performance in Q1 2017 was strong, with over 95% of orders delivered successfully. Average delivery time was approximately 12 days. The seller onboarding process was streamlined during this quarter, adding 300 new sellers to the platform.",
    "Challenges",
    "Low brand awareness in northern Brazilian states limited order volumes. Marketing investment was concentrated in Sao Paulo and Rio de Janeiro, leaving significant untapped markets. Customer acquisition costs remained high due to limited organic traffic."
])

# Report 2 — Q3 2017
create_pdf("q3_2017_report.pdf", "Olist Q3 2017 Business Report", [
    "Executive Summary",
    "Q3 2017 represented a significant acceleration in Olist platform growth. Total orders surged to over 12,000 for the quarter, with August recording 4,331 orders — a 61% increase over Q1 monthly averages. The platform successfully expanded its seller base and product catalog.",
    "Sales Performance",
    "The sports and leisure category (esporte_lazer) emerged as a top performer in Q3 2017, capitalizing on end-of-year fitness trends. Computer accessories and electronics showed strong growth driven by back-to-school demand. Total quarterly revenue exceeded R$1.8 million, representing 40% growth over Q2 2017.",
    "November Peak Analysis",
    "November 2017 recorded 7,544 orders — the highest single month in the platform's history at that point. This spike was driven by Black Friday promotional campaigns and seasonal gifting demand. The bed and bath category alone accounted for over 2,000 November orders.",
    "Operational Challenges",
    "Rapid order growth in Q3 exposed logistics bottlenecks. Average delivery times increased from 12 to 15 days as carrier capacity was strained. Several sellers in the electronics category faced stockout issues during the November peak, leading to a 3% cancellation rate in that segment.",
    "Strategic Recommendations",
    "Management recommended expanding carrier partnerships ahead of Q4 to address delivery time concerns. Investment in seller inventory management tools was approved to reduce stockout incidents during high-demand periods."
])

# Report 3 — Q1 2018
create_pdf("q1_2018_report.pdf", "Olist Q1 2018 Business Report", [
    "Executive Summary",
    "Q1 2018 built on the strong momentum of late 2017. Orders averaged 7,000 per month, representing consistent year-over-year growth of over 200% compared to Q1 2017. The platform processed over 21,000 orders in the quarter with total revenue of approximately R$3.2 million.",
    "Category Performance",
    "Bed and bath products maintained leadership with 9,417 total orders year to date. Health and beauty reached 8,836 orders, showing particularly strong growth in skincare and personal care segments. The furniture and home decor category grew 45% driven by urban apartment purchases.",
    "Seller Ecosystem",
    "The seller base expanded to over 3,000 active sellers by end of Q1 2018. Seller satisfaction scores improved following the introduction of dedicated account management. Top sellers averaged R$45,000 in quarterly revenue, with the highest performing seller generating over R$120,000.",
    "Delivery Performance",
    "A new carrier partnership introduced in February 2018 reduced average delivery times from 15 to 11 days. Customer satisfaction scores improved by 12 percentage points following the delivery improvements. The cancellation rate dropped to 0.6% — the lowest in platform history.",
    "Outlook",
    "Management projected continued 30% quarterly growth through 2018 based on expanding seller catalog and improving brand recognition in underserved Brazilian states including Minas Gerais and Bahia."
])

# Report 4 — Annual 2017 Review
create_pdf("annual_2017_review.pdf", "Olist Annual 2017 Business Review", [
    "Year in Review",
    "2017 was a breakout year for Olist. Total orders grew from 800 in January to 7,544 in November, representing an 843% increase in monthly order volume. Full year orders totaled approximately 45,000 with total gross merchandise value exceeding R$6.5 million.",
    "Top Product Categories",
    "The top 5 categories by order volume in 2017 were: bed and bath (cama_mesa_banho) with 9,417 orders, health and beauty (beleza_saude) with 8,836 orders, sports and leisure (esporte_lazer) with 7,720 orders, computer accessories (informatica_acessorios) with 6,689 orders, and furniture and decor (moveis_decoracao) with 6,449 orders. These five categories accounted for 68% of total platform revenue.",
    "Payment Behavior",
    "Credit card payments dominated at 74% of transactions. The average payment value across all categories was R$154.91. Buy-now-pay-later installment plans were used in 42% of transactions, indicating strong consumer preference for flexible payment options. Boleto bancario accounted for 19% of payments.",
    "Geographic Distribution",
    "Sao Paulo state accounted for 42% of all orders, followed by Rio de Janeiro at 13% and Minas Gerais at 11%. Northern and northeastern states remained underpenetrated, representing a significant growth opportunity for 2018.",
    "Seller Performance",
    "The platform ended 2017 with 3,095 active sellers. Average seller rating was 4.1 out of 5.0. The top 10% of sellers generated 61% of total platform revenue. Seller churn rate was 8% annually, primarily among low-volume sellers in competitive categories.",
    "2018 Strategic Priorities",
    "Based on 2017 performance, management identified three strategic priorities: expanding logistics infrastructure in northern Brazil, launching a seller financing program to support inventory growth, and investing in mobile app development to capture the growing smartphone-first customer segment."
])

print("\nAll reports created in data/reports/")