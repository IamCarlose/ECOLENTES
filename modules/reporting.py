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
        elements.append(Paragraph("ECOLENTES OS v4.0 - REPORTE INDUSTRIAL", styles['Title']))
        elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # 1. Dashboard Productivity
        elements.append(Paragraph("1. BITÁCORA DE PRODUCCIÓN", styles['Heading2']))
        data_cycles = self.db.get_full_history()
        if data_cycles:
            headers = ["ID", "Timestamp", "Dur.", "Op", "Status", "Mat. (kg)", "Temp", "Rej"]
            table_data = [headers] + [list(row) for row in data_cycles[:20]] # Limit to 20 for preview
            t = Table(table_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#10B981")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            elements.append(t)
        else:
            elements.append(Paragraph("No hay datos de producción registrados.", styles['Normal']))
            
        elements.append(Spacer(1, 20))
        
        # 2. SMED
        elements.append(Paragraph("2. REGISTRO DE MEJORAS SMED", styles['Heading2']))
        data_smed = self.db.get_smed_data()
        if data_smed:
            headers = ["ID", "Tarea", "Tipo", "Dur.", "Notas"]
            table_data = [headers] + [list(row) for row in data_smed]
            t = Table(table_data, colWidths=[30, 150, 60, 60, 180])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#3B82F6")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTSIZE', (0,0), (-1,-1), 9),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            elements.append(t)
        else:
            elements.append(Paragraph("No hay tareas SMED registradas.", styles['Normal']))

        elements.append(Spacer(1, 20))
        
        # 3. DOE
        elements.append(Paragraph("3. DISEÑO DE EXPERIMENTOS (DOE)", styles['Heading2']))
        data_doe = self.db.get_doe_data()
        if data_doe:
            headers = ["ID", "Factor A", "Factor B", "Resultado", "Timestamp"]
            table_data = [headers] + [list(row) for row in data_doe]
            t = Table(table_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#6366F1")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            elements.append(t)
        else:
            elements.append(Paragraph("No hay experimentos DOE almacenados en la base de datos central.", styles['Normal']))

        # Footer
        elements.append(Spacer(1, 40))
        elements.append(Paragraph("— Fin del Reporte ECOLENTES Industrial —", styles['Italic']))

        doc.build(elements)
        return os.path.abspath(filename)

    def generate_excel(self, filename="Ecolentes_Industrial_Report.xlsx"):
        """Genera un archivo Excel con múltiples hojas y gráficos de tendencia."""
        try:
            # 1. Obtener Datos
            h_logs = self.db.get_hildegard_logs()
            s_logs = self.db.get_hildegard_speed_logs()
            p_cycles = self.db.get_full_history()
            
            # Formatear timestamps para que Excel los entienda mejor (quitamos la T de ISO)
            def format_ts(rows):
                new_rows = []
                for r in rows:
                    lst = list(r)
                    if len(lst) > 1 and isinstance(lst[1], str):
                        try:
                            lst[1] = datetime.fromisoformat(lst[1]).strftime("%Y-%m-%d %H:%M")
                        except: pass
                    new_rows.append(lst)
                return new_rows

            h_logs = format_ts(h_logs)
            s_logs = format_ts(s_logs)
            p_cycles = format_ts(p_cycles)

            with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
                workbook = writer.book
                
                # --- FORMATOS ---
                header_fmt = workbook.add_format({'bold': True, 'bg_color': '#1E293B', 'font_color': 'white', 'border': 1})
                
                # --- HOJA 1: TERMOFORMADO (T/P) ---
                df_tech = pd.DataFrame(h_logs, columns=["ID", "Fecha/Hora", "Temp (°C)", "Presión (PSI)", "Notas"])
                df_tech.to_excel(writer, sheet_name='Termoformado', index=False)
                sheet_tech = writer.sheets['Termoformado']
                
                # Aplicar formato de cabecera
                for col_num, value in enumerate(df_tech.columns.values):
                    sheet_tech.write(0, col_num, value, header_fmt)
                
                # Gráfico Tº y Presión
                max_row = len(df_tech)
                if max_row > 1:
                    chart_tech = workbook.add_chart({'type': 'line'})
                    chart_tech.add_series({
                        'name':       'Temperatura (°C)',
                        'categories': ['Termoformado', 1, 1, max_row, 1],
                        'values':     ['Termoformado', 1, 2, max_row, 2],
                        'line':       {'color': '#EF4444', 'width': 2},
                    })
                    chart_tech.add_series({
                        'name':       'Presión (PSI)',
                        'categories': ['Termoformado', 1, 1, max_row, 1],
                        'values':     ['Termoformado', 1, 3, max_row, 3],
                        'line':       {'color': '#3B82F6', 'width': 2},
                    })
                    chart_tech.set_title({'name': 'TENDENCIA DE TERMOFORMADO'})
                    chart_tech.set_x_axis({'name': 'Tiempo'})
                    chart_tech.set_y_axis({'name': 'Magnitud'})
                    chart_tech.set_legend({'position': 'bottom'})
                    sheet_tech.insert_chart('G2', chart_tech, {'x_scale': 1.5, 'y_scale': 1.2})

                # --- HOJA 2: VELOCIDAD ---
                df_speed = pd.DataFrame(s_logs, columns=["ID", "Fecha/Hora", "Velocidad (m/min)", "Notas"])
                df_speed.to_excel(writer, sheet_name='Rapidez', index=False)
                sheet_speed = writer.sheets['Rapidez']
                
                for col_num, value in enumerate(df_speed.columns.values):
                    sheet_speed.write(0, col_num, value, header_fmt)

                max_row_s = len(df_speed)
                if max_row_s > 1:
                    chart_speed = workbook.add_chart({'type': 'area'})
                    chart_speed.add_series({
                        'name':       'Velocidad (m/min)',
                        'categories': ['Rapidez', 1, 1, max_row_s, 1],
                        'values':     ['Rapidez', 1, 2, max_row_s, 2],
                        'fill':       {'color': '#10B981', 'transparency': 50},
                        'line':       {'color': '#059669'},
                    })
                    chart_speed.set_title({'name': 'CONTROL DE VELOCIDAD'})
                    sheet_speed.insert_chart('F2', chart_speed, {'x_scale': 1.2, 'y_scale': 1.1})

                # --- HOJA 3: CICLOS DE PRODUCCIÓN ---
                df_prod = pd.DataFrame(p_cycles, columns=["ID", "Fecha/Hora", "Duración (s)", "Operador", "Estado", "Material (kg)", "Temp Amb", "Rechazos"])
                df_prod.to_excel(writer, sheet_name='Producción', index=False)
                sheet_prod = writer.sheets['Producción']
                
                for col_num, value in enumerate(df_prod.columns.values):
                    sheet_prod.write(0, col_num, value, header_fmt)

                max_row_p = len(df_prod)
                if max_row_p > 1:
                    chart_prod = workbook.add_chart({'type': 'column'})
                    chart_prod.add_series({
                        'name':       'Duración (s)',
                        'categories': ['Producción', 1, 1, max_row_p, 1],
                        'values':     ['Producción', 1, 2, max_row_p, 2],
                        'fill':       {'color': '#6366F1'},
                    })
                    chart_prod.set_title({'name': 'TIEMPOS DE CICLO'})
                    chart_prod.set_y_axis({'name': 'Segundos'})
                    sheet_prod.insert_chart('J2', chart_prod, {'x_scale': 1.4, 'y_scale': 1.1})

            return os.path.abspath(filename)
        except Exception as e:
            print(f"Error generando Excel: {e}")
            return None
