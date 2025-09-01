from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# 路由：首頁
@app.route('/')
def index():
    return render_template('index.html')

# 路由：查詢功能
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    name = data.get('product_name', '').strip()
    part = data.get('part_number', '').strip()
    model = data.get('model', '').strip()

    # 讀取 Excel（每次查詢時最新資料）
    df = pd.read_excel('data.xlsx', dtype=str).fillna('')

    # 過濾資料（模糊查詢）
    if name:
        df = df[df['品名'].str.contains(name, case=False, na=False)]
    if part:
        df = df[df['料號'].str.contains(part, case=False, na=False)]
    if model:
        df = df[df['適用機型'].str.contains(model, case=False, na=False)]

    # 回傳結果
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
