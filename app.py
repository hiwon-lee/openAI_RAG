from flask import Flask,render_template, request, jsonify
from blueai_langchain_rag_chroma_gpt_tojson_v7 import get_important_facts

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_query = request.form['query']  # 사용자 입력 쿼리
        response = get_important_facts(user_query)  # GPT 응답 생성
        
        return render_template('index.html', query=user_query, response=response)
    return render_template('index.html')
  

if __name__ == '__main__':
    app.debug = True
    app.run()
