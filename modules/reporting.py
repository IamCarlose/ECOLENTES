from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from datetime import datetime
import pandas as pd

class IndustrialReportGenerator:
    def __init__(self, db_manager):
        self.db = db_manager
        
    def generate_pdf(self, filename="Ecolentes_Industrial_Report.pdf"):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Header
        elements.append(Paragraph("ECOLENTES OS v4.0 - REPORTE INDUSTRIAL INTEGRAL", styles['Title']))
        elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        sections = [
            ("BITÁCORA DE PRODUCCIÓN (TIEMPOS)", self.db.get_full_history(), ["ID", "TS", "Dur", "Op", "Status", "Mat", "Temp", "Rej"], "#10B981"),
            ("REGISTRO DE TEMPERATURA", self.db.get_temp_logs(), ["ID", "Timestamp", "Temp (°C)", "Notas"], "#3B82F6"),
            ("REGISTRO DE PRESIÓN", self.db.get_pressure_logs(), ["ID", "Timestamp", "Presión (PSI)", "Notas"], "#F59E0B"),
            ("REGISTRO DE RPM / RAPIDEZ", self.db.get_rpm_logs(), ["ID", "Timestamp", "RPM / m/min", "Notas"], "#6366F1")
        ]
        
        for title, data, headers, color in sections:
            elements.append(Paragraph(title, styles['Heading2']))
            if data:
                table_data = [headers] + [list(row)[:len(headers)] for row in data[:20]] 
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor(color)),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                    ('FONTSIZE', (0,0), (-1,-1), 8)
                ]))
                elements.append(t)
            else:
                elements.append(Paragraph("Sin datos registrados en esta sección.", styles['Normal']))
            elements.append(Spacer(1, 15))

        elements.append(Paragraph("— Fin del Reporte ECOLENTES —", styles['Italic']))
        doc.build(elements)
        return os.path.abspath(filename)

    def generate_excel(self, filename="Ecolentes_Industrial_Report.xlsx"):
        try:
            data_map = {
                'Temperatura': (self.db.get_temp_logs(), ["ID", "Fecha", "Temp (°C)", "Notas"], '#3B82F6', 'Temperatura (°C)'),
                'Presión': (self.db.get_pressure_logs(), ["ID", "Fecha", "Presión (PSI)", "Notas"], '#F59E0B', 'Presión (PSI)'),
                'RPM': (self.db.get_rpm_logs(), ["ID", "Fecha", "RPM", "Notas"], '#6366F1', 'RPM'),
                'Producción': (self.db.get_full_history(), ["ID", "Fecha", "Duración (s)", "Op", "St", "Mat", "T.Amb", "Rej"], '#10B981', 'Duración (s)')
            }

            with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
                workbook = writer.book
                for sheet_name, (rows, cols, color, y_label) in data_map.items():
                    df = pd.DataFrame(rows, columns=cols[:len(rows[0])]) if rows else pd.DataFrame(columns=cols)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    sheet = writer.sheets[sheet_name]
                    
                    header_fmt = workbook.add_format({'bold': True, 'bg_color': color, 'font_color': 'white'})
                    for col_num, value in enumerate(df.columns.values):
                        sheet.write(0, col_num, value, header_fmt)
                        
                    if len(df) > 1:
                        chart = workbook.add_chart({'type': 'line'})
                        chart.add_series({
                            'name':       y_label,
                            'categories': [sheet_name, 1, 1, len(df), 1],
                            'values':     [sheet_name, 1, 2, len(df), 2],
                            'line':       {'color': color, 'width': 2},
                        })
                        chart.set_title({'name': f'TENDENCIA DE {sheet_name.upper()}'})
                        chart.set_y_axis({'name': y_label})
                        sheet.insert_chart('F2', chart, {'x_scale': 1.5, 'y_scale': 1.2})
            return os.path.abspath(filename)
        except Exception as e:
            print(f"Error Excel: {e}"); return None
