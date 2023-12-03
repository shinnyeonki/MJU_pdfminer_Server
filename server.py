import os
import subprocess
import re
from pdf2docx import Converter
from flask import Flask, request, send_file
from flask_cors import CORS
from pdfminer.high_level import extract_text
import base64
import filename

app = Flask(__name__)
CORS(app)

# 데이터를 저장할 폴더
data_folder = 'data'

def base64encode(string):
    return base64.b64encode(string).decode('utf-8')

def base64decode(string):
    return base64.b64decode(string).decode('utf-8')




@app.route('/pdfminer/get_txt', methods=['POST'])
def get_txt():
    file = request.files['file']
    filename = file.filename
    # 파일을 'data' 폴더에 저장
    filepath = os.path.join(data_folder, filename)
    file.save(filepath)

    # PDF 파일에서 텍스트 추출
    text = extract_text(filepath)

    # 추출된 텍스트를 txt 파일로 저장
    result_filename = filepath.replace('.pdf', '.txt')
    with open(result_filename, 'w') as f:
        f.write(text)

    return send_file(result_filename, as_attachment=True)

# pdf  -> docx 변환 기능
@app.route('/pdfminer/get_doc', methods=['POST'])
def get_doc():
    file = request.files['file']
    filename = file.filename
    # 파일을 'data' 폴더에 저장
    filepath = os.path.join(data_folder, filename)
    file.save(filepath)
    result_filename = filepath.replace('.pdf', '.docx')

    cv = Converter(filepath)
    cv.convert(result_filename)
    cv.close()
    
    return send_file(result_filename, as_attachment=True)



@app.route('/pdfminer/get_html', methods=['POST'])
def get_html():
    file = request.files['file']
    filename = file.filename
    # 파일을 'data' 폴더에 저장
    filepath = os.path.join(data_folder, filename)
    file.save(filepath)
    result_filename = filepath.replace('.pdf', '.html')
    
    # pdf2htmlEX 명령의 인수로 파일의 이름을 넣어주면 html 파일로 변환
    # 이스케이프 처리할 문자 패턴
    escape_pattern = r'[^\w\d\s]'

# 이스케이프 처리 함수
    def escape_match(match):
        char = match.group()
        return '\\' + char
    command = "./pdfToHtml.sh {}".format(re.sub(escape_pattern, escape_match, filepath))
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        return str(e)
    
    return send_file(result_filename, as_attachment=True)


if __name__ == '__main__':
    # 'data' 폴더가 없으면 생성
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    app.run(host='0.0.0.0', port=5000)
#    app.run(host='localhost', port=5000)
