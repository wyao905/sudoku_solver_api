from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from solver import Solution

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    single_solve = request.json['single']
    board = request.json['board']

    solution = Solution(board)
    valid = solution.verify()
    if valid:
        solution_found = solution.solve()
        if solution_found:
            if single_solve:
                row_id = request.json['row_id']
                col_id = request.json['col_id']
                return jsonify({'solution': solution.board[row_id][col_id]})
            else:
                return jsonify({'solution': solution.board})
        else:
            return jsonify({'error': 'No Solutions Found'})
    else:
        return jsonify({'error': 'Invalid Puzzle'})


if __name__ == '__main__':
    app.run(debug=True)