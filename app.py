from flask import Flask, render_template, request, session, Response
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

app = Flask(__name__)

def original_line(txt):
    output_list = re.split(r'(\[[^\]]+\])', txt)
    return [s for s in output_list if s]

def split_lines(original_line):
    chord_line = ''
    lyric_line = ''
    chord_length = 0

    for item in original_line:
        if item[0] == '[':
            chord_line = chord_line + item.replace('[','').replace(']','')
            chord_length = len(item.replace('[','').replace(']',''))
        else:
            chord_line = chord_line + (len(item)-chord_length)*' '
            lyric_line = lyric_line + item
    
    return (chord_line, lyric_line)

def generate_pdf(txt,song,artist, filename):
    cv = canvas.Canvas(filename, pagesize=letter)
    cv.setFont("Courier-Bold", 16)
    cv.drawString(100, 750, song)
    cv.setFont("Courier-Bold", 14)
    cv.drawString(100, 730, artist)
    cv.drawString(100, 710, '----------------')
  
    y = 700
    
    cv.setFont("Courier", 12)
    lines = txt.split('\n')
    for line in lines:
        ol = original_line(line)
        l1,l2 = split_lines(ol)
        cv.setFillColor(colors.red)
        cv.drawString(100, y, l1)
        y = y - 10
        cv.setFillColor(colors.black)
        cv.drawString(100, y, l2)
        y = y - 20
    cv.save()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate")
def generate():
  txt = request.args.get("lyrics")
  song = str(request.args.get("songName"))
  artist = str(request.args.get("artistName"))
  generate_pdf(txt,song,artist, song+".pdf")
  with open(song+".pdf", "rb") as pdf_file:
      pdf_data = pdf_file.read()
  response = Response(pdf_data, content_type='application/pdf')
  response.headers['Content-Disposition'] = 'attachment; filename='+song+'.pdf'
  return response

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0', port=5000)