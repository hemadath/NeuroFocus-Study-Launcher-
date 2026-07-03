import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Main route to serve your responsive Omni Index layout
@app.route('/')
def home():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return render_template_string(html_content)
    except FileNotFoundError:
        return "System File Configuration Error: index.html not found in repository root directory.", 404

# Core API Node to handle universal subject lookups and text synthesis
@app.route('/api/omni-search', methods=['POST'])
def omni_search_and_explain():
    data = request.get_json() or {}
    target_topic = data.get("query", "").strip()
    
    if not target_topic:
        return jsonify({"error": "Empty search query configuration parameter"}), 400

    try:
        # 1. Map dynamic high resolution keyword photography assets 
        dynamic_image_url = f"https://unsplash.com?{requests.utils.quote(target_topic)},education"
        
        # 2. Dispatch cross origin model payloads to the OpenRouter inference pipeline
        # Using free Llama model mapping blocks for server stability
        ai_response = requests.post(
            "https://openrouter.ai",
            headers={
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3.2-1b-instruct:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a world-class interactive personal tutor for AstroMindAI. Break down the user's topic into an immediate, clear, ultra-practical summary explanation. Keep it strictly under 3 sentences."
                    },
                    {
                        "role": "user",
                        "content": f"Explain this topic comprehensively: {target_topic}"
                    }
                ]
            },
            timeout=12
        )
        
        # Verify remote pipeline confirmation targets
        if ai_response.status_code != 200:
            return jsonify({"error": f"OpenRouter endpoint network error: Code {ai_response.status_code}"}), 502
            
        ai_data = ai_response.json()
        processed_answer = ai_data["choices"][0]["message"]["content"]

        return jsonify({
            "image_url": dynamic_image_url,
            "explanation": processed_answer
        })

    except Exception as e:
        return jsonify({"error": f"Server side compilation failure: {str(e)}"}), 500

if __name__ == '__main__':
    # Binds production sockets cleanly to Render environment variable ports
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
      
