from flask import Flask, request

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test_endpoint():
    input_value = request.form.get('input', '')

    # SQL Injection simulieren
    if any(kw in input_value.lower() for kw in ["select", "union", "drop", "insert", "mysql"]):
        return "SQL syntax error: near '...'", 500

    # XSS simulieren
    if any(tag in input_value.lower() for tag in ["<script>", "<img", "<svg", "<iframe"]):
        return "<html><body>Possible XSS detected!</body></html>", 200

    # Path Traversal
    if "../" in input_value or "..\\" in input_value:
        return "Access denied: Directory traversal", 403

    # Format String
    if "%" in input_value:
        return "Format string error", 500

    # Command Injection
    if any(cmd in input_value for cmd in ["ls", "whoami", "cat", "&&", "||", "`"]):
        return "Command injection detected", 400

    # Unicode / Encoding
    if any(enc in input_value.lower() for enc in ["%u", "\\u", "%c0", "%e0"]):
        return "Unicode decode error", 500

    # Spezielle Statuscodes
    if "unauthorized" in input_value.lower():
        return "Unauthorized", 401
    if "notfound" in input_value.lower():
        return "Not Found", 404
    if "conflict" in input_value.lower():
        return "Conflict", 409
    if "unavailable" in input_value.lower():
        return "Service temporarily unavailable", 503

    # Default
    return "OK", 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)