import requests

# Make a GET request to the stream-file endpoint with the filename parameter
#file_path = "inside/test.log"
file_path = "test.log"
response = requests.get(f'http://localhost:5001/stream-file/{file_path}?row_count=5', stream=True)

# Check that the response was successful
if response.status_code == 200:

    # Set up a loop to iterate over the content of the response

    for chunk in response:
        # Check that we received a chunk of data
        if chunk:
            print(chunk.decode('utf-8'), end='\n')
else:
    print("Error: ", response.status_code)
