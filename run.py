from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        # 폼에서 전달된 값 가져오기
        dep_date = request.form['dep_date']
        arr_date = request.form['arr_date']
        car_capacity = request.form['car_capacity']
        budget = request.form['budget']
        
        # 여기서부터는 기존 로직에 따라 데이터 처리 및 계산 로직을 추가하시면 됩니다.

        # 결과를 JSON 형식으로 반환
        result_data = {
            'dep_date': dep_date,
            'arr_date': arr_date,
            'car_capacity': car_capacity,
            'budget': budget,
            # 추가적인 결과 데이터도 필요한 경우 여기에 추가
        }
        return jsonify(result_data)
    else:
        return render_template('index.html')
    
@app.route('/result')
def result_page():
    # 전달받은 값을 가져와서 result.html에 전달합니다.
    dep_date = request.args.get('dep_date')
    arr_date = request.args.get('arr_date')
    car_capacity = request.args.get('car_capacity')
    budget = request.args.get('budget')
    
    # 이후에는 result.html에서 사용할 데이터를 가공하여 변수에 담고, render_template로 결과를 반환합니다.
    # (result.html 템플릿에 따라 결과를 가공하여 보여주는 부분을 구현하시면 됩니다.)

    return render_template('result.html', dep_date=dep_date, arr_date=arr_date, car_capacity=car_capacity, budget=budget)

if __name__ == '__main__':
    app.run()