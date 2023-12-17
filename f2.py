from flask import Flask, Response, stream_with_context, request

app = Flask(__name__)

@app.route('/stream-file/<path:file_path>')
def stream_file(file_path):
    row_count = int(request.args.get('row_count', 1))
    print(row_count)

    def generate():
        with open(file_path, 'rb') as file:
            i = 0
            while True:
                if i < row_count:
                    i += 1
                    line = file.readline().decode('utf-8')
                    if line:
                        print('--------------------------')
                        print(line)
                        yield f"data: {line}\n\n"
                else:
                    yield ""


    return Response(stream_with_context(generate()),
                    content_type="text/event-stream",
                    mimetype="text/event-stream",
                    headers={"Connection": "keep-alive"})


if __name__ == '__main__':
    app.run(port=5001, debug=True)
