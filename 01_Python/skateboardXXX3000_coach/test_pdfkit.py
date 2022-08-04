import pdfkit
print("okokok")
with open('file.html') as f:
    pdfkit.from_file(f, 'out.pdf')