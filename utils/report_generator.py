from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from io import BytesIO

def generate_pdf_report(results, startup_name):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title of the report
    title = Paragraph(f"{startup_name} Project Analysts Report by Selçuk Topal", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 24))
    
    # Sections for each analysis type
    sections = {
        "Porter's Five Forces": "Porter's Five Forces",
        "Systemic Thinking": "Systemic Thinking",
        "Cynefin Framework": "Cynefin Framework"
    }
    
    # Ratings section
    ratings = []
    
    # Iterate through results and organize content by sections
    analysis_content = {
        "Porter's Five Forces": [],
        "Systemic Thinking": [],
        "Cynefin Framework": []
    }
    
    conclusion_content = []

    for analysis_type, question, answer in results:
        if "Rating" in question:
            ratings.append((sections[analysis_type], answer))
        elif analysis_type == "Conclusion":
            conclusion_content.append(Paragraph(answer, styles['Normal']))
            conclusion_content.append(Spacer(1, 12))
        else:
            analysis_content[analysis_type].append(Paragraph(answer, styles['Normal']))
            analysis_content[analysis_type].append(Spacer(1, 12))
    
    # Add ratings section
    story.append(Paragraph("Startup Rating:", styles['Heading1']))
    rating_items = [ListItem(Paragraph(f"{analysis_type}: {rating}", styles['Normal'])) for analysis_type, rating in ratings]
    story.append(ListFlowable(rating_items, bulletType='bullet'))
    story.append(Spacer(1, 24))
    
    # Add analysis sections
    story.append(Paragraph("Analysis:", styles['Heading1']))
    for analysis_type, content in analysis_content.items():
        story.append(Paragraph(sections[analysis_type], styles['Heading2']))
        story.append(Spacer(1, 12))
        story.extend(content)
        story.append(Spacer(1, 24))
    
    # Add conclusion section
    if conclusion_content:
        story.append(Paragraph("Conclusion:", styles['Heading1']))
        story.extend(conclusion_content)
        story.append(Spacer(1, 24))
    
    # Build the PDF
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.seek(0)
    return pdf