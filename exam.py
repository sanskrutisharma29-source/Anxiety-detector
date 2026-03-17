from http.server import SimpleHTTPRequestHandler, HTTPServer
import json

class MyServer(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes("""
<!DOCTYPE html>
<html>
<head>
<title>Exam Anxiety Detector</title>
</head>
<body>

<h2>AI Exam Anxiety Detector</h2>

<p>Do you feel nervous before exams?</p>
<select id="q1">
<option value="1">No</option>
<option value="2">Sometimes</option>
<option value="3">Yes</option>
</select>

<p>Do you lose sleep before exams?</p>
<select id="q2">
<option value="1">No</option>
<option value="2">Sometimes</option>
<option value="3">Yes</option>
</select>

<p>Do you panic in exam hall?</p>
<select id="q3">
<option value="1">No</option>
<option value="2">Sometimes</option>
<option value="3">Yes</option>
</select>

<br><br>
<button onclick="check()">Check Anxiety</button>

<h3 id="result"></h3>

<script>
function check(){
let q1 = document.getElementById("q1").value;
let q2 = document.getElementById("q2").value;
let q3 = document.getElementById("q3").value;

fetch("/analyze", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({q1:q1, q2:q2, q3:q3})
})
.then(res => res.json())
.then(data => {
document.getElementById("result").innerText = data.result;
});
}
</script>

</body>
</html>
""", "utf-8"))

        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/analyze":
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)
            data = json.loads(data)

            # Simple AI logic
            score = int(data["q1"]) + int(data["q2"]) + int(data["q3"])

            if score <= 3:
                result = "Low Anxiety 😊"
            elif score <= 6:
                result = "Moderate Anxiety 😐"
            else:
                result = "High Anxiety 😟"

            response = json.dumps({"result": result})

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode())

# Run server
server = HTTPServer(("localhost", 8000), MyServer)
print("Open: http://localhost:8000")
server.serve_forever()