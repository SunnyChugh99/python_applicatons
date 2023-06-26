def stream(testing=None):
    f = open('test.log', 'r')
    while True:
        for chunk_ in f:
            try:
                yield f"{chunk_}\n"
            # pylint: disable=broad-except
            except Exception as ex:
                print(ex)

        if testing:
            break
log_stream = stream()

for log in log_stream:
    print(log)
