from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_schema', methods=['POST'])
def generate_schema():
    data = request.json
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": data.get('name', ''),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": data.get('streetAddress', ''),
            "addressLocality": data.get('city', ''),
            "addressRegion": data.get('state', ''),
            "postalCode": data.get('postalCode', ''),
            "addressCountry": data.get('country', '')
        },
        "telephone": data.get('telephone', ''),
        "url": data.get('website', '')
    }
    return jsonify(schema)

if __name__ == '__main__':
    app.run(debug=True)