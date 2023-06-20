from flask import Flask, request, redirect, url_for, abort, Blueprint, g, request, Response, send_file
import os

# Set up the Flask app

app = Flask(__name__)

@app.route("/rounds/<int:round_id>/replay", methods=["GET", "OPTIONS"])
def page_round_replay(round_id):
    headers = {}

    origin = request.environ.get("HTTP_ORIGIN")
    headers["Access-Control-Allow-Credentials"] = "true"
    headers["Access-Control-Expose-Headers"] = "X-Allow-SS13-Replay-Streaming"
    headers["Access-Control-Allow-Headers"] = "Range"
    headers["Access-Control-Allow-Origin"] = "*"
    
    if request.method == "OPTIONS":
        return Response(status=204, headers=headers)
        

    if not round:
        return Response("Round does not exist", status=404, headers=headers)

    demo_file = os.path.join("replays", f"{round_id}_demo.txt")

    if not demo_file: # There is no replay for this one
                print("oops")
                return Response("No replay file found", status=404, headers=headers)

    response = send_file(demo_file,
        conditional=True, # Allow the file to be streamed with ranges
        max_age=-1 # Don't cache the file by default
    )
    print(headers)
    response.headers.update(headers)

    if demo_file.endswith(".gz"):
        response.headers.add("Content-Encoding", "gzip")
    
    if demo_file.endswith(".txt"):
        response.headers.add("X-Allow-SS13-Replay-Streaming", "true")
        
    if demo_file.endswith(".log"):
        response.headers.add("X-Allow-SS13-Replay-Streaming", "true")
        
    response.headers.add("Cache-Control", f"public,max-age=31536000,immutable")

    return response

# Start the Flask app
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=10101)
