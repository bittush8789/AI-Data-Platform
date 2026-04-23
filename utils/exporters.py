import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class Exporter:
    @staticmethod
    def to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    @staticmethod
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()

    @staticmethod
    def to_pdf(text_content, title="Report"):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, title)
        c.setFont("Helvetica", 12)
        
        y = 700
        for line in text_content.split('\n'):
            if y < 50:
                c.showPage()
                y = 750
            c.drawString(100, y, line)
            y -= 15
        
        c.save()
        return buffer.getvalue()
