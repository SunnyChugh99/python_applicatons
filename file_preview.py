from flask import Flask, Response, stream_with_context, request
import os
app = Flask(__name__)

@app.route('/stream-file/<path:filepath>')
def stream_file(filepath):
    row_count = int(request.args.get('row_count', 1))
    print(row_count)
    absolute_file_path = os.path.abspath(filepath)
    print("Absolute file path:", absolute_file_path)

    # Get the current directory
    current_directory = os.getcwd()
    print("Current directory:", current_directory)
    def generate():

        with open(filepath, 'rb') as file:
            i = 0
            while True:

                if i < row_count:
                    i = i + 1
                    line = file.readline().decode('utf-8')

                    if line:
                        print('--------------------------')
                        print(line)
                        yield f"data: {line}\n\n"
                    # else:
                    #     break

                if row_count > 1900:
                    break

    return Response(stream_with_context(generate()),
                    content_type="text/event-stream",
                    mimetype="text/event-stream",
                    headers={"Connection": "keep-alive"})


if __name__ == '__main__':
    app.run(port=5001, debug=True)
