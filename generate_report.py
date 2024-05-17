#!/usr/bin/python3

import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

def generate_pdf_report(report_data):
    # Créer un document PDF
    pdf = SimpleDocTemplate("rapport_scan.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Définir un style personnalisé pour le texte avec une taille de police réduite et aligné à gauche
    small_text_style = ParagraphStyle(
        name='SmallText',
        parent=styles['Normal'],
        fontSize=10,
        alignment=0,  # Alignement à gauche
    )

    title_style = ParagraphStyle(
        name='Title',
        parent=styles['Title'],
        fontSize=12,
        spaceAfter=12,
        alignment=0,  # Alignement à gauche
    )

    # Ajouter le titre du rapport
    main_title_style = ParagraphStyle(
        name='MainTitle',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=24,
        alignment=1,  # Alignement centré
    )

    elements.append(Paragraph('Rapport Projden', main_title_style))

    # Ajouter les informations du nom de l'hôte et de l'adresse IP
    elements.append(Paragraph('Voici les informations sur la cible', title_style))
    target_info = f"Nom de l'hôte : {report_data['hostname'] if report_data['hostname'] else 'N/A'}<br/>Adresse IP : {report_data['target_ip']}"
    elements.append(Paragraph(target_info, small_text_style))
    elements.append(Spacer(1, 12))

    # Ajouter les résultats du scan nmap de base
    elements.append(Paragraph('Ci-dessous vous trouverez les résultats du scan nmap de base', title_style))
    
    # Formater les résultats du scan Nmap en tableau
    header = ["Port Ouvert", "State", "Service", "Version"]
    table_lines = report_data['table'].split('\n')
    
    # Extraire les lignes de résultats du scan Nmap
    table_data = [header]
    for line in table_lines[3:-1]:  # Exclure les lignes de bordures
        if '|' in line:
            table_data.append([cell.strip() for cell in line.split('|')[1:-1]])

    # Ajuster les styles du tableau
    table = Table(table_data, colWidths=[70, 50, 70, 220])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Ajouter les résultats des CVE
    elements.append(Paragraph('Voici les CVE détectés lors du scan. Vous trouverez ci-joint l\'ID correspondant au CVE ainsi que l\'URL pour vous rendre sur le site en question :', title_style))
    cve_details = ""
    for port, cves in report_data['cve_results'].items():
        cve_details += f"<b>Port {port}:</b><br/>" + "<br/>".join(cve.strip('| ').replace('\t', ' ') for cve in cves) + "<br/><br/>"
    elements.append(Paragraph(cve_details, small_text_style))
    elements.append(Spacer(1, 12))

    # Ajouter les résultats brute force
    elements.append(Paragraph('Résultats Brute Force', title_style))
    brute_force_details = ""
    for service, results in report_data['brute_force_results'].items():
        if results:
            brute_force_details += f"<b>Service {service}:</b><br/>"
            for login, password in results:
                brute_force_details += f"Login : {login}, Password : {password}<br/>"
        else:
            brute_force_details += f"<b>Service {service} : Aucun résultat</b><br/>"
    elements.append(Paragraph(brute_force_details, small_text_style))

    # Générer le PDF
    pdf.build(elements)

if __name__ == "__main__":
    with open("report_data.json", "r") as report_file:
        report_data = json.load(report_file)
    generate_pdf_report(report_data)
