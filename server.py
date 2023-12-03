from pdf2docx import Converter
from flask import Flask, request, send_file
from flask_cors import CORS
from pdfminer.high_level import extract_text

app = Flask(__name__)
CORS(app)

# pdf  -> docx 변환 기능
@app.route('/pdfminer/get_doc', methods=['POST'])
def get_doc():
    file = request.files['file']
    filename = file.filename
    file.save(filename)

    result_filename = filename.replace('.pdf', '.docx')
    cv = Converter(filename)
    cv.convert(result_filename)
    cv.close()
    return send_file(result_filename, as_attachment=True)


@app.route('/pdfminer/get_txt', methods=['POST'])
def get_txt():
    file = request.files['file']
    filename = file.filename
    file.save(filename)

    # PDF 파일에서 텍스트 추출
    text = extract_text(filename)

    # 추출된 텍스트를 txt 파일로 저장
    result_filename = filename.replace('.pdf', '.txt')
    with open(result_filename, 'w') as f:
        f.write(text)

    return send_file(result_filename, as_attachment=True)

# @app.route('/pdfminer/get_txt', methods=['POST'])
# def get_html():
#     pass
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
#    app.run(host='localhost', port=5000)