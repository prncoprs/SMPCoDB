from flask import Flask, request, jsonify, Response
from flask import render_template
import json
from codegen.codegen import Parser
from codegen.table.table import Table
from codegen.table.free_connex_table import FreeConnexTable
import subprocess
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return jsonify()


@app.route("/generate", methods=["POST"])
def generate_code():
    try:
        data = request.json
        tables = [FreeConnexTable.load_from_json(t) for t in json.loads(data['table'])]
        sql = data['sql']
        parser = Parser(sql=sql, tables=tables)
        output = parser.parse().to_output()
        graph = parser.root_table.to_json(
            output_attrs=parser.get_output_attributes())

        is_free_connex, error_tables = parser.is_free_connex()
        error_tables = [e.variable_table_name for e in error_tables]
        return jsonify({"code": output, "joinGraph": graph, "isFreeConnex": is_free_connex, "errorTables": error_tables})
    except Exception as e:
        return Response(str(e), status=500)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
