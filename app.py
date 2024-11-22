import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF

app = Flask(__name__)

# Configuração do diretório de uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    # Verifica se o arquivo PDF e a palavra-chave foram enviados
    if 'pdf_file' not in request.files or 'keyword' not in request.form:
        return jsonify({"error": "Nenhum arquivo ou palavra-chave fornecido."}), 400

    pdf_file = request.files['pdf_file']
    keyword = request.form['keyword']

    if pdf_file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400

    if pdf_file and pdf_file.filename.endswith('.pdf'):
        # Salva o arquivo PDF
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        pdf_file.save(pdf_path)

        # Processa o arquivo PDF
        filtered_pdf_path = filter_pdf(pdf_path, keyword)

        if filtered_pdf_path:
            # Retorna o link para download do PDF gerado
            return jsonify({
                "message": "Arquivo processado e PDF gerado com sucesso!",
                "pdf": f"uploads/{os.path.basename(filtered_pdf_path)}"
            })

        else:
            return jsonify({"error": "Nenhum conteúdo encontrado com a palavra-chave."}), 404

    return jsonify({"error": "Formato de arquivo inválido."}), 400

def filter_pdf(pdf_path, keyword):
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()

            if text and keyword.lower() in text.lower():
                writer.add_page(page)

        # Salva o novo PDF filtrado
        if len(writer.pages) > 0:
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"filtered_{os.path.basename(pdf_path)}")
            with open(output_path, 'wb') as output_pdf:
                writer.write(output_pdf)
            return output_path
        else:
            return None

    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")
        return None

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
