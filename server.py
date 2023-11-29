from pdf2docx import Converter
from flask import Flask, request, send_file
from flask_cors import CORS

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

# pdf -> txt 변환 기능 추후 개발 예정
# @app.route('/pdfminer/get_txt', methods=['POST'])
# def run_python_program():
#     file = request.files['file']
#     filename = secure_filename(file.filename)
#     file.save(filename)

#     # 여기에서 filename 파일을 사용하여 Python 프로그램을 실행하고,
#     # 결과 파일을 생성합니다. 결과 파일의 이름을 result_filename이라고 가정합니다.
#     # Python 프로그램 실행 코드를 여기에 작성하세요.

#     return send_file(result_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
#    app.run(host='localhost', port=5000)