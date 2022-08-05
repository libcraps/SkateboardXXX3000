import pdfkit

def html2pdf(html_path, pdf_path):
    """
    Convert html to pdf using pdfkit which is a wrapper of wkhtmltopdf
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    print(f"Making report from {html_path}")
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options)
    print(f"Success making report at {pdf_path}")