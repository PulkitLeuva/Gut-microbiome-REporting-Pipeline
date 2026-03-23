####### Author Pratik AND Pulkit

import pandas as pd
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import Flowable


BASE_PATH="input/Report_generation/"
CSV_PATH= sys.argv[1]
TEXT_CSV_PATH="input/Report_generation/static_texts.csv"
LOGO1_PATH="input/Report_generation/DiGeMed_logo.png"
LOGO2_PATH="input/Report_generation/igib_logo.png"
REPORT_PATH="output/metaphlan_plots/"
Firts_page_Image="input/Report_generation/gut_microbiome_ND.png"
Output_Path=sys.argv[2]
First_page_Canva="input/Report_generation/First_page.png"
Second_page_Canva="input/Report_generation/Second_page.png"
Third_page_Canva="input/Report_generation/Third_page.png"
'''
# Define paths at the top for easy modification
# Get paths from command-line arguments
BASE_PATH = sys.argv[1]
CSV_PATH = sys.argv[2]
TEXT_CSV_PATH = sys.argv[3]
LOGO1_PATH = sys.argv[4]
LOGO2_PATH = sys.argv[5]
REPORT_PATH = sys.argv[6]
Firts_page_Image=sys.argv[7]
Output_Path= sys.argv[8]
First_page_Canva = sys.argv[9]
Second_page_Canva = sys.argv[10]
Third_page_Canva = sys.argv[11]
'''

# Load static texts from CSV
texts_df = pd.read_csv(TEXT_CSV_PATH)
texts = {row['variable_name']: row['text'] for _, row in texts_df.iterrows()}

# Define custom styles
# Define custom styles
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(name='TitleStyle',
                          fontName='Times-Bold',
                          fontSize=40,
                          textColor=colors.HexColor('#4379F2'),
                          alignment=TA_CENTER))

styles.add(ParagraphStyle(name='SECOND_TITLE',
                          fontName='Times-Bold',
                          fontSize=20,
                          textColor=colors.HexColor('#333333'),
                          spaceAfter=20,
                          alignment=TA_CENTER))

styles.add(ParagraphStyle(name='THIRD_TITLE',
                          fontName='Times-Bold',
                          fontSize=22,
                          textColor=colors.HexColor('#333333'),
                          alignment=TA_CENTER))

styles.add(ParagraphStyle(name='Heading2Style',
                          fontName='Helvetica-Bold',
                          fontSize=14,
                          textColor=colors.HexColor('#333333'),
                          spaceAfter=10,
                          alignment=TA_JUSTIFY))

styles.add(ParagraphStyle(name='Heading1Style',
                          fontName='Helvetica-Bold',
                          fontSize=18,
                          textColor=colors.HexColor('#333333'),
                          spaceAfter=10,
                          alignment=TA_JUSTIFY))

styles.add(ParagraphStyle(name='NormalStyle',
                          fontName='Helvetica',
                          fontSize=12,
                          textColor=colors.HexColor('#333333'),
                          leading=14,
                          alignment=TA_JUSTIFY))

styles.add(ParagraphStyle(name='NormalStyle_centre',
                          fontName='Helvetica',
                          fontSize=12,
                          textColor=colors.HexColor('#333333'),
                          leading=14,
                          alignment=TA_CENTER))

styles.add(ParagraphStyle(name='NormalStyle_small_font',
                          fontName='Helvetica',
                          fontSize=9,
                          textColor=colors.HexColor('#333333'),
                          leading=14,
                          alignment=TA_JUSTIFY))

styles.add(ParagraphStyle(name='DisclaimerStyle',
                          fontName='Helvetica-Bold',
                          fontSize=10,
                          textColor=colors.HexColor('#555555'),
                          leading=16,
                          #spaceBefore=10,
                          alignment=TA_JUSTIFY))

styles.add(ParagraphStyle(name='Note',
                          fontName='Helvetica-Bold',
                          fontSize=11,
                          textColor=colors.HexColor('#555555'),
                          leading=16,
                          #spaceBefore=2,
                          alignment=TA_JUSTIFY))

styles.add(ParagraphStyle(name='ItalicStyle', 
                          fontName='Helvetica-Oblique', 
                          fontSize=12, 
                          textColor=colors.HexColor('#333333'), 
                          alignment=TA_JUSTIFY))


styles.add(ParagraphStyle(name='CenteredPresenceStyle',
                          fontName='Helvetica',
                          fontSize=12,
                          textColor=colors.HexColor('#333333'),
                          alignment=TA_CENTER,
                          spaceBefore=10))  # Add spaceBefore to center signs in column

styles.add(ParagraphStyle(name='email_style',
                          parent=styles['Normal'],
                          textColor='#0000FF',  # Blue color
                          underline=True))

styles.add(ParagraphStyle(
                          name='Lab_ID_Bold',
                          fontName='Helvetica-Bold',  # Use Helvetica-Bold for bold text
                          fontSize=12,
                          textColor=colors.HexColor('#333333'),
                          leading=14,
                          alignment=TA_JUSTIFY))

# Function to create a dynamic table from DataFrame
def create_table_from_df(df, col_widths):
    # Convert the DataFrame to a list of lists with formatting
    data = [df.columns.tolist()] + [
        [
            # Apply italic style to the first column (Species)
            Paragraph(str(cell), styles['ItalicStyle']) if i == 0 else
            # Apply centered style with padding to the Presence column
            Paragraph(str(cell), styles['CenteredPresenceStyle']) if i == 1 else
            # Apply normal style to other columns
            Paragraph(str(cell), styles['NormalStyle'])
            for i, cell in enumerate(row)
        ]
        for row in df.values.tolist()
    ]
    
    # Create the table with column widths
    table = Table(data, colWidths=col_widths)
    
    # Define table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    return table

def add_header(canvas, doc):
    width, height = A4
    '''try:
        canvas.drawImage(LOGO1_PATH, width - 97, height - 70, width=50, height=50)
    except OSError:
        print(f"Warning: {LOGO1_PATH} not found. Skipping this image.")
    try:
        canvas.drawImage(LOGO2_PATH, 44, height - 70, width=40, height=50)
    except OSError:
        print(f"Warning: {LOGO2_PATH} not found. Skipping this image.")
'''
    page_number_text = f"{doc.page}"
    canvas.setFont('Helvetica', 12)
    text_width = canvas.stringWidth(page_number_text, 'Helvetica', 12)
    canvas.drawString((width - text_width) / 2.0, 25, page_number_text)


def First_page (canvas, doc):
    width, height = A4
    '''try:
        canvas.drawImage(LOGO1_PATH, width - 140, height - 130, width=100, height=100)
    except OSError:
        print(f"Warning: {LOGO1_PATH} not found. Skipping this image.")
    try:
        canvas.drawImage(LOGO2_PATH, 35, height - 137, width=95, height=110)
    except OSError:
        print(f"Warning: {LOGO2_PATH} not found. Skipping this image.")
'''


    if doc.page == 1:
        canvas.setFont('Helvetica-Bold', 17)
        #canvas.drawCentredString(width / 2.0, height - 100, "PHENOME INDIA: CSIR COHORT HEALTH KNOWLEDGEBASE")
    page_number_text = f"{doc.page}"
    canvas.setFont('Helvetica', 12)
    text_width = canvas.stringWidth(page_number_text, 'Helvetica', 12)
    canvas.drawString((width - text_width) / 2.0, 25, page_number_text)



def add_resized_image(image_path, max_width, max_height):
    img = Image(image_path)
    img_width, img_height = img.wrap(max_width, max_height)
    scaling_factor = min(max_width / img_width, max_height / img_height)
    img_width = img_width * scaling_factor
    img_height = img_height * scaling_factor
    img._restrictSize(img_width, img_height)
    img.hAlign = 'CENTER'
    return img


#######Adding Ikmage to he left size
def add_resized_image_left(image_path, max_width, max_height):
    img = Image(image_path)
    img_width, img_height = img.wrap(max_width, max_height)
    scaling_factor = min(max_width / img_width, max_height / img_height)
    img_width *= scaling_factor
    img_height *= scaling_factor
    img._restrictSize(img_width, img_height)
    img.hAlign = 'LEFT'
    return img


def add_page_border(canvas, doc):
    width, height = A4
    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(0.8)
    canvas.rect(12.5, 12.5, width - 25, height - 25)

def add_disclaimer_box(elements):
    # Disclaimer text parts
    main_text = ("Disclaimer: These test results are generated using a research-grade testing protocol and are not equivalent to clinical diagnostics performed in accredited hospitals or laboratory settings. They are intended solely for informational purposes and should not be used to guide medical treatment or therapy. If you have any concerns regarding your results, please consult your physician. These reports are not intended for use in any medico-legal context and carry no legal liability.")
    
    
    # Create paragraphs with different styles
    main_paragraph = Paragraph(main_text, styles['DisclaimerStyle'])
    #note_paragraph = Paragraph(note_text, styles['Note'])  # Use a different style for the note
    
    # Create a table for the disclaimer
    table = Table([[main_paragraph]], colWidths=[500])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E8F9FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('TOPPADDING', (0, 1), (-1, -1), 0),  # Set top padding for note paragraph to 0
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Adjust bottom padding for main paragraph
    ]))
    
    # Append the table to the elements
    elements.append(table)

def add_fb_ratio_box(elements):
    elements.append(Paragraph("2) Firmicutes and Bacteroidetes Ratio:", styles['Heading2Style']))
    elements.append(Paragraph(texts['fb_ratio_Heading_type1'], styles['NormalStyle']))
    elements.append(Spacer(1, 12))




######### Species level Diversity table 

def create_image_reference_table(elements, image_paths, references, col_widths):
    data = []
    
    # Load styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    heading_style = styles['Heading2']
    
    heading_style = ParagraphStyle(
        name='HeadingStyle',
        parent=styles['Heading2'],
        fontSize=13,  # Adjust the font size as needed
        alignment=1   # Center alignment
    )
    # Define headers for images
    headers = [
        '3.1) Microbial Species Richness ',   # Header for the first image
        '3.2) Evenness Index',   # Header for the second image
        '3.3) Microbiome Diversity Index'    # Header for the third image
    ]
    headers2 = [
        'Description ',   # Header for the first image
        'Description',   # Header for the second image
        'Description'    # Header for the third image
    ]
    # Insert header rows and image/content rows
    for i, (image_path, reference_text) in enumerate(zip(image_paths, references)):
        # Add header before each image row
        if i < len(headers):
            header_paragraph = Paragraph(headers[i], heading_style)
            second_header_paragraph = Paragraph(headers2[i], heading_style)
            # Add a row for the header with only one column
            data.append([header_paragraph, second_header_paragraph])
        
        # Load the image and set its size
        img = Image(image_path, width=col_widths[0], height=2.2*inch)
        
        # Create bullet points
        
        # Create the table row with the image, reference text, and bullet points
        reference_paragraph = Paragraph(f"{reference_text}<br/><br/>", normal_style)
        row = [img, reference_paragraph]
        data.append(row)
    
    # Create the table with column widths
    table = Table(data, colWidths=250)
    
    # Define table style
    table.setStyle(TableStyle([
        # Header styles
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        
        ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.black),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 2), (-1, 2), 6),
        ('TOPPADDING', (0, 2), (-1, 2), 6),
        
        ('BACKGROUND', (0, 4), (-1, 4), colors.lightgrey),
        ('TEXTCOLOR', (0, 4), (-1, 4), colors.black),
        ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
        ('ALIGN', (0, 4), (-1, 4), 'CENTER'),
        ('BOTTOMPADDING', (0, 4), (-1, 4), 6),
        ('TOPPADDING', (0, 4), (-1, 4), 6),
        
        # General table styles
        #('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        #('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        #('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        #('BACKGROUND', (0, 1), (-1, -1), colors.white),
        #('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        

        
        # Keep outer borders
        ('GRID', (0, 0), (0, -1), 0.5, colors.black),  # Left border
        ('GRID', (0, 0), (-1, 0), 0.5, colors.black),  # Top border
        ('GRID', (0, -1), (-1, -1), 0.5, colors.black),  # Bottom border
        ('GRID', (-1, 0), (-1, -1), 0.5, colors.black),  # Right border
        
        # Remove vertical lines between the first and second column
        #('GRID', (1, 0), (1, -1), 0, colors.white),  # Remove vertical line for the second column only

        # Center text in the second column
        #('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Center-align text in the second column
        
        # Keep horizontal lines
        ('GRID', (0, 0), (-1, 0), 0.5, colors.black),  # Header horizontal lines
        ('GRID', (0, 2), (-1, 2), 0.5, colors.black),  # Second header horizontal lines
        ('GRID', (0, 4), (-1, 4), 0.5, colors.black),  # Third header horizontal lines
        ('GRID', (0, 5), (-1, 5), 0.5, colors.black)   # First content row horizontal lines
        
    ]))
    
    # Add table to elements
    elements.append(table)



def Firts_page_reference_table(elements, parameters, values, reference_ranges, col_widths):
    data = []
    
    # Load styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    normal_style.fontSize = 12
    heading_style = ParagraphStyle(
        name='HeadingStyle',
        parent=styles['Heading2'],
        fontSize=13,  # Adjust the font size as needed
        alignment=1   # Center alignment
    )

    # Define the headers for the table
    headers = [
        Paragraph('Parameters', heading_style),
        Paragraph('Value', heading_style),
        Paragraph('Reference Range', heading_style),
    ]
    
    # Insert the header row
    data.append(headers)

    # Insert data rows
    for parameter, value, reference_range in zip(parameters, values, reference_ranges):
        row = [
            Paragraph(parameter, normal_style),
            Paragraph(str(value), normal_style),
            Paragraph(reference_range, normal_style),
        ]
        data.append(row)
    
    # Create the table with column widths
    table = Table(data, colWidths=col_widths)
    
    # Define table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Header alignment
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Header bottom padding
        ('TOPPADDING', (0, 0), (-1, 0), 6),  # Header top padding
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # General grid
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment
        ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Left padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # Right padding
        ('TOPPADDING', (0, 0), (-1, -1), 5),  # Top padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Bottom padding
    ]))
    
    # Append the table to the elements
    elements.append(table)



def add_image_after_fb_ratio(lab_id, elements):
    ratio_image_path = f"{REPORT_PATH}{lab_id}_phylum_ratio.png"
    ratio_image = add_resized_image(ratio_image_path, max_width=4.5*inch, max_height=3*inch)
    elements.append(ratio_image)
    elements.append(Spacer(1, 12))


def generate_references(Richness, evenness, Shannon_Diversity):
    # Richness Reference
    if Richness < 46:
        richness_ref = f"Richness is the total number of microbial species identified within your sample.The number of species found in your gut microbiome is {Richness} and it is less than the average Indian population range."
    elif 46 <= Richness <= 308:
        richness_ref = f"Richness is the total number of microbial species identified within your sample. The number of species found in your gut microbiome is {Richness} and it is within the average Indian population range."
    else:  # richness > 308
        richness_ref = f"Richness is the total number of microbial species identified within your sample. The number of species found in your gut microbiome is {Richness} and it is more than the average Indian population range."


    # Evenness Reference
    if evenness < 0.5:
        evenness_ref = f"Evenness describes how uniformly all the species are present in your gut microbiome. \n The value of species evenness in your sample is {evenness:.2f} and it is less than the average Indian population range."
    elif 0.5 <= evenness <= 0.8:
        evenness_ref = f"Evenness describes how uniformly all the species are present in your gut microbiome. \n The value of species evenness in your sample is {evenness:.2f} and it is within the average Indian population range."
    else:  # evenness > 0.8
        evenness_ref = f"Evenness describes how uniformly all the species are present in your gut microbiome. \nThe value of species evenness in your sample is {evenness:.2f} and it is more than the average Indian population range."

    # Diversity Reference
    if Shannon_Diversity < 2.36:
        diversity_ref = f"The microbiome diversity index is calculated using both richness and evenness. The value of microbiome index of your sample is {Shannon_Diversity:.2f} and it is less than the average Indian population range."
    elif 2.36 <= Shannon_Diversity <= 4.24:
        diversity_ref = f"The microbiome diversity index is calculated using both richness and evenness. The value of microbiome index of your sample is {Shannon_Diversity:.2f} and it is within the average Indian population range."
    else:  # shannon_index > 4.24
        diversity_ref = f"The microbiome diversity index is calculated using both richness and evenness. The value of microbiome index of your sample is {Shannon_Diversity:.2f} and it is more than the average Indian population range."

    return [richness_ref, evenness_ref, diversity_ref]

# Example usage
# Get updated references



######### For addig values 




def create_pdf(lab_id, output_path, df_probiotics, fb_ratio, phylum_count, evenness):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=40,
                            rightMargin=40,
                            topMargin=80,
                            bottomMargin=20)
    elements = []

    ######## Colnames `
    new_column_names = ['Species', 'Presence', 'Short Chain Fatty\n Acid/s Produced', 'Description']
    df_probiotics = pd.read_csv(f"{REPORT_PATH}{lab_id}_beneficial_sp.csv")
    df_probiotics.columns = new_column_names
    df_probiotics = df_probiotics.fillna('Not Reported')
    df_probiotics = df_probiotics.sort_values(by="Species")


    ############## Calculate probiotic species count ###########################
    df = df_probiotics  # Use 'xlrd' for older Excel formats
# Check if the second column exists and is named correctly
    if df.shape[1] < 2:
        print("The file does not contain a second column.")
    else:
        # Select the second column (index 1, because indexing starts at 0)
        second_column = df.iloc[:, 1]
        
        # Count the occurrences of '+' in the second column
        plus_count = second_column.astype(str).apply(lambda x: x.count('+')).sum()

    
    #drawImage(LOGO1_PATH, width - 90, height - 70, width=50, height=50)
    # First Page Content
    # Define centered paragraph style if not already present
    centered_style = ParagraphStyle(
        name='CenteredStyle',
        parent=styles['Lab_ID_Bold'],
        alignment=TA_CENTER
    )

    # Create table with centered text
    lab_info_table = Table(
        [[Paragraph(f"Sample ID: {lab_id}", centered_style)]],
        colWidths=[6 * inch]  # Make the entire row span full width if needed
    )

    # Apply style to center cell content in the table
    lab_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

  # Adjust colWidths as needed
    elements.append(Spacer(1, 40))
    #gut_microbiome_image = add_resized_image(GUT_MICROBIOME_IMAGE_PATH, max_width=6*inch, max_height=4.5*inch)
    #elements.append(gut_microbiome_image)
    #canvas.drawImage(LOGO1_PATH, width - 90, height - 70, width=50, height=50)
    #elements.append(Paragraph("PHENOME INDIA:", styles['SECOND_TITLE']))
    #elements.append(Spacer(1, 0))
    #elements.append(Paragraph("CSIR COHORT HEALTH KNOWLEDGEBASE", styles['SECOND_TITLE']))
    #elements.append(Spacer(1, 15))
   

    
   ## Image 
    elements.append(add_resized_image(Firts_page_Image, max_width=5.8*inch, max_height=4.3*inch))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Gut Microbiome Report", styles['TitleStyle']))
    elements.append(Spacer(1, 50))
    elements.append(lab_info_table)
    elements.append(Spacer(1, 27))
    #elements.append(Spacer(1, 20))
    #elements.append(Paragraph(f'Note: The reference ranges for the interpretation of the results are based on the analysis of more than 2500 gut microbiome samples collected across India.', styles['NormalStyle']))
    #elements.append(Spacer(1, 10))
    add_disclaimer_box(elements)
    elements.append(Spacer(1, 10))
    elements.append(PageBreak())


    # Add a heading
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Index", getSampleStyleSheet()["Heading3"]))
    elements.append(Spacer(1, 6))

    # Table data
    sections_data = [
        ["Section", "Description"],
        ["1", "Phylum Diversity"],
        ["2", "Firmicutes / Bacteroidetes Ratio"],
        ["3", "Species-level Diversity"],
        ["3.1", "Species Richness"],
        ["3.2", "Evenness Index"],
        ["3.3", "Microbiome Diversity Index"],
        ["3.4", "Distribution of species"],
        ["4", "Probiotic Species and Short Chain Fatty Acid (SCFA) Producers"],
        ["5", "Gut Microbiome Wellness Index: GMWI2"],
    ]

    # Create table
    table = Table(sections_data, colWidths=[60, 380])  # Adjust widths as needed

    # Style
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ]))

    # Add to elements
    elements.append(table)
    elements.append(Spacer(1, 20))
# Add the table to your document (assuming 'elements' is a list where you collect your document components)
    
    
    ####################


    elements.append(Paragraph("Description", styles['Heading1Style']))
    elements.append(Spacer(1, 11))
    elements.append(Paragraph(texts['intro_text'], styles['NormalStyle']))
    elements.append(Spacer(1, 20))
    elements.append(PageBreak())

    

    '''fb_ratio_round= round(fb_ratio, 2)
    Shannon_Diversity_round =round(Shannon_Diversity, 2)
    col_widths = [3*inch, 3*inch]
    parameters = ["Gut Microbiome Wellness Index" ]
    values = [ Wellness_Index]
    reference_ranges = ["Wellness Index > 0 = Healthy &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Wellness Index < 0 = Non Healthy"]
    elements.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Report Summary:", styles['Heading2Style']))
    elements.append(Spacer(1, 10))
    Firts_page_reference_table(elements, parameters, values, reference_ranges, [150, 100, 200])
    # Add table with images and references
   
    #elements.append(Paragraph("", styles['SECOND_TITLE']))
    elements.append(Spacer(1, 37))
    #elements.append(Spacer(2, 27))
    elements.append(Paragraph("Interpretation of Your Results:", styles['Heading2Style']))
    elements.append(Spacer(1, 7))
    
    #elements.append(Paragraph("Microbiome Diversity Index:", styles['Heading2Style']))

    if Wellness_Index > 0:

        elements.append(Paragraph(f'Your overall gut microbiome analysis indicates a well-balanced and healthy microbiome, supporting optimal gut health.', styles['NormalStyle']))
    else:
        elements.append(Paragraph(f'Your overall gut microbiome analysis indicates an imbalance, suggesting potential areas for improvement in gut health.', styles['NormalStyle']))
    elements.append(Spacer(1, 20))'''

    








    ########### Phyluium count
     # Phylum Diversity
    elements.append(Paragraph("1) Phylum-Level Diversity of Your Gut Microbiome:", styles['Heading2Style']))
    elements.append(Paragraph(texts['phylum_diversity_text'], styles['NormalStyle']))


    phylum_image_path = f"{REPORT_PATH}{lab_id}_phylum.png"
    elements.append(add_resized_image(phylum_image_path, max_width=5*inch, max_height=3.5*inch))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f'Your gut microbiome profile indicates the presence of {phylum_count} distinct phyla. The average range of phyla present in gut microbiome of Indian population is 3-15.*', styles['NormalStyle']))
    elements.append(Spacer(1,20))
                    
    if phylum_count > 5:
        Phylum_result = (
            f"Your gut microbiome profile indicates the presence of {phylum_count} distinct phyla. The average range of phyla present in gut microbiome of Indian population is 3-15.*"
            
        )
    else:
        Phylum_result = (
            f"Your gut microbiome profile indicates the presence of {phylum_count} distinct phyla. The average range of phyla present in gut microbiome of Indian population is 3-15*. Having a varied diet and healthy lifestyle choices will help you increase the diversity for promoting good health. "
            
        )
    #elements.append(Paragraph(Phylum_result, styles['NormalStyle']))

    
    ################# Firmicutes/Bacteroidetes Ratio with border Page 3

    add_fb_ratio_box(elements)
    elements.append(Spacer(1, 0))
    add_image_after_fb_ratio(lab_id, elements)
    #elements.append(Paragraph("Interpretation:", styles['Heading2Style']))
   # if fb_ratio > 1:
       # elements.append(Paragraph(texts['fb_ratio_final'], styles['NormalStyle']))
   # elif fb_ratio == 1:
     #   elements.append(Paragraph(texts['fb_ratio_final'], styles['NormalStyle']))
   # else:
      #  elements.append(Paragraph(texts['fb_ratio_final'], styles['NormalStyle']))
   # elements.append(Spacer(1, 12))
    elements.append(PageBreak())


    ########### Species Diversity (Page 4)  ##############
    elements.append(Paragraph("3) Species-level Diversity of Your Gut Microbiome*:", styles['Heading2Style']))
    #diversity_image_size = (3.5*inch, 3.5*inch)
    elements.append(Spacer(1, 20))
      ################ Adding Images 
    image_paths = [
        f"{REPORT_PATH}{lab_id}_gauge_richness.png",
        f"{REPORT_PATH}{lab_id}_gauge_evenness.png",
        f"{REPORT_PATH}{lab_id}_gauge_shannon.png",
    ]
    references = generate_references(Richness, evenness, Shannon_Diversity)
    # Define column widths
    col_widths = [3*inch, 3*inch]
    # Add table with images and references
    create_image_reference_table(elements, image_paths, references, col_widths)
    elements.append(Spacer(1, 5))


    elements.append(Spacer(1, 5))
   # elements.append(Paragraph("Interpretation:", styles['Heading2Style']))
    if Shannon_Diversity > 4.24:
        evenness_text = (
            "Your gut microbiome exhibits a high level of microbial diversity, which is a strong indicator of a healthy and well-balanced gut microbiome. This diversity plays a crucial role in various bodily functions, including effective digestion, nutrient absorption, maintaining a robust immune system and protect against harmful pathogens."
            
        )
    elif  2.36 <= Shannon_Diversity <= 4.24:
        evenness_text = (
            "Your gut microbiome shows a healthy level of microbial diversity, indicating that your gut microbiome is functioning well. A diverse microbiome is essential for a range of vital processes, including efficient digestion, nutrient absorption, and protection against harmful pathogens."
            
        )
    else:
        evenness_text = (
            "Your gut microbiome shows a low microbial diversity, which may impact digestion and immune function. Low diversity indicates an imbalance in the distribution of species and is associated with dysbiosis that may lead to health issues. "
        
        )
    
    #elements.append(Paragraph(evenness_text, styles['NormalStyle']))

    elements.append(PageBreak())


    ################# Probiotic Species  Page numer 5 ##############################
   




    elements.append(Paragraph("3.4) Distribution of Species:", styles['Heading2Style']))
    elements.append(Paragraph('The top 15 species in your gut microbiome based on the relative abundance.*', styles['NormalStyle']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f'*When a bacterial species has numbers in its name, it signifies a recent discovery that has not been formally named yet.', styles['NormalStyle_small_font']))
    elements.append(Spacer(1, 15))
    DIstribution_of_S__image_path = f"{REPORT_PATH}{lab_id}_species_top15.png"
    elements.append(add_resized_image(DIstribution_of_S__image_path, max_width=6*inch, max_height=4.5*inch))
    elements.append(Spacer(1, 20))
    #elements.append(PageBreak())
    
  

    elements.append(Paragraph("4) Probiotic Species:", styles['Heading2Style']))
    #elements.append(Paragraph(texts['probiotic_intro_text'], styles['NormalStyle']))
    Probiotic_ = texts['probiotic_intro_text'] + '<a href="https://www.mdpi.com/2304-8158/11/18/2863"><font color="blue" size="10"> (Xiong et al., "Health benefits and side effects of short-chain fatty acids", <i>Foods</i>, 2022, Vol. 11, Issue 18, pp. 2863)</font></a>'

    elements.append(Paragraph(Probiotic_, styles['NormalStyle']))
    elements.append(Paragraph(f'This section presents the probiotic species detected in your gut microbiome and SCFA produced by them.', styles['NormalStyle']))



    elements.append(Spacer(1, 20))
    col_widths = [1.45*inch, 0.80*inch, 1.5*inch, 3.2*inch]
    table = create_table_from_df(df_probiotics, col_widths)
    elements.append(table)
    elements.append(Spacer(1, 20))
    

    ############# Interpretation results ###############
   # elements.append(Paragraph("Interpretation of Your Results:", styles['Heading1Style']))
    #elements.append(Spacer(1, 30))
    elements.append(Paragraph(f"Among the Top 16 probiotic species predominantly observed in the Indian population, we identified {plus_count} species in your gut microbiome.*", styles['NormalStyle']))
    #elements.append(Paragraph("Microbiome Diversity Index:", styles['Heading2Style']))
    elements.append(Spacer(1, 20))

    # Define column widths
    elements.append(Paragraph("<strong>*Note:</strong> The reference ranges used for interpreting the results are derived from a comprehensive review of publicly available scientific literature on the human gut microbiome."))
    #elements.append(Spacer(2, 27))
    
    #elements.append(Spacer(1, 6))
    
    #elements.append(Paragraph("Microbiome Diversity Index:", styles['Heading2Style']))

   
   
   #Shannon_Diversity
    elements.append(PageBreak())

    # Page 2 Content
    #Wellness_Index= round(Wellness_Index, 2)
    gmwi2_text = texts['GMWI2'] + '<a href="https://www.nature.com/articles/s41467-024-51651-9"><font color="blue" size="10"> (Chang et al., "Gut Microbiome Wellness Index 2 enhances health status prediction from gut microbiome taxonomic profiles", <i>Nature Communications</i>, 2024, Vol. 15, Issue 1, pp. 7447)</font></a>'

    elements.append(Paragraph("5) Gut Microbiome Wellness Index 2 (GMWI2):", styles['Heading2Style']))
    elements.append(Spacer(1, 11))
    #elements.append(Paragraph(texts['GMWI2'], styles['NormalStyle']))
    elements.append(Paragraph(gmwi2_text, styles['NormalStyle']))
    elements.append(Spacer(1, 20))
    elements.append(Spacer(1, 12))
    DIstribution_of_wellness = f"{REPORT_PATH}{lab_id}_gmwi2_plot.png"
    elements.append(add_resized_image(DIstribution_of_wellness, max_width=6*inch, max_height=4.5*inch))
    elements.append(Spacer(1, 20))
    if Wellness_Index > 0:

        elements.append(Paragraph(f'Your gut microbiome wellness score is {round(Wellness_Index,2)} which indicates good gut microbiome.', styles['NormalStyle']))
        
    elif  Wellness_Index == 0:
        elements.append(Paragraph(f'Your gut microbiome wellness score is {round(Wellness_Index,2)} which indicates balanced gut microbiome.', styles['NormalStyle']))
    else:
        elements.append(Paragraph(f'Your gut microbiome wellness score is {round(Wellness_Index,2)} which indicates poor gut microbiome.', styles['NormalStyle']))
    elements.append(Spacer(1, 15))


    elements.append(Paragraph("Interpretation of Your Results:", styles['Heading2Style']))
    if Wellness_Index > 0:

        elements.append(Paragraph(f'Your overall gut microbiome analysis indicates a well-balanced and healthy microbiome, supporting optimal gut health.', styles['NormalStyle']))
    else:
        elements.append(Paragraph(f'Your overall gut microbiome analysis does not indicate a well-balanced and healthy microbiome, suggesting potential areas for improvement in gut health.', styles['NormalStyle']))
        elements.append(Paragraph(f'Note: Antibiotics impact the gut microbiome significantly, consumption of antibiotics within one month of sampling may result in lower GMWI2.', styles['NormalStyle']))
    elements.append(Spacer(1, 15))
    elements.append(Spacer(1, 20))
    


   

############# GmWI2
   
    elements.append(PageBreak())

#########   fB/ rATIO iNTERPRETATION ##########################
    

    ########## calculate the Phylum species out of 20 #########



    # Adding Canva Pages
    def add_stretched_image(image_path, width, height):
        img = Image(image_path)
        img.width = width
        img.height = height
        img._restrictSize(width, height)  # Optional: Restrict size if needed
        img.hAlign = 'CENTER'
        return img

    # Add images stretched to specific width and height
    #elements.append(add_stretched_image(First_page_Canva, width=20*inch, height=10*inch))
      # Add some space between images
    #elements.append(add_stretched_image(Second_page_Canva, width=15*inch, height=10*inch))
    
    #elements.append(add_stretched_image(Third_page_Canva, width=15*inch, height=10*inch))
    #elements.append(PageBreak())

    ############## Three Canva Pages Added  ######################

    ################ Disclaimer Page  ###########################


    def add_last_disclaimer_box(elements):
        disclaimer_text = Paragraph(texts['last_Disclaimer'], styles['DisclaimerStyle'])
        table = Table([[disclaimer_text]], colWidths=[500])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFDCDC")),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ]))
        elements.append(table)
    #add_last_disclaimer_box(elements)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Contact us", styles['Heading2Style']))
    elements.append(Spacer(1, 11))
    email_address = "kumardeep.igib@csir.res.in"
    email_paragraph = Paragraph(
        f"Email: <a href='mailto:{email_address}' color='#0000FF' underline='true'>{email_address}</a>",
        styles['NormalStyle']
    )
    elements.append(email_paragraph)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Address: CSIR-Institute of Genomics & Integrative Biology, South Campus, Mathura Road, Opp: Sukhdev Vihar Bus Depot, New Delhi 110025", styles['NormalStyle']))


    # Build the document
    doc.build(elements, onFirstPage=lambda c, d: (First_page(c, d), add_page_border(c, d)),
              onLaterPages=lambda c, d: (add_header(c, d), add_page_border(c, d)))

# Load the main CSV file containing lab IDs and other relevant data
data_df = pd.read_csv(CSV_PATH)

# Iterate over each row in the CSV to generate a PDF for each lab ID
for index, row in data_df.iterrows():
    lab_id = row['Sample']
    #date = row['date_of_collection']
    output_path = f"{Output_Path}"
    print(lab_id)
    df_probiotics = pd.read_csv(f"{REPORT_PATH}{lab_id}_beneficial_sp.csv")
    df_probiotics = df_probiotics.fillna('')

    fb_ratio = row['F.B']  # Example placeholder value
    Shannon_Diversity = row['Shannon']       
    Wellness_Index = row['GMWI2']

    phylum_count = row['Phylum_count']  # Example placeholder value
    Richness =row['Richness']
    evenness = row['Evenness'] # Example placeholder value
    references = generate_references(Richness, evenness, Shannon_Diversity)
    print(f"Richness: {Richness}, Evenness: {evenness}, Shannon_Diversity: {Shannon_Diversity}")

    create_pdf(lab_id, output_path, df_probiotics, fb_ratio, phylum_count,evenness)

