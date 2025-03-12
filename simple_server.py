from flask import Flask, render_template, request, Response, jsonify
import requests
import os
import io
import base64

app = Flask(__name__)
XTTS_SERVER_URL = "http://localhost:8008"  # Your XTTS server address

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clone_voice', methods=['POST'])
def clone_voice():
    """Handle voice sample upload and cloning"""
    if 'voice_sample' not in request.files:
        return jsonify({"error": "No voice sample provided"}), 400
    
    voice_file = request.files['voice_sample']
    
    # Forward to XTTS server
    files = {'wav_file': (voice_file.filename, voice_file.read(), voice_file.content_type)}
    response = requests.post(f"{XTTS_SERVER_URL}/clone_speaker", files=files)
    
    if response.status_code != 200:
        return jsonify({"error": f"Failed to clone voice: {response.text}"}), response.status_code
    
    # Return the speaker data to be stored in browser
    return jsonify(response.json())

@app.route('/tts', methods=['POST'])
def text_to_speech():
    """Generate speech from text using cloned voice (non-streaming)"""
    data = request.json
    
    # Forward request to XTTS server
    tts_response = requests.post(f"{XTTS_SERVER_URL}/tts", json=data)
    
    if tts_response.status_code != 200:
        return jsonify({"error": f"Failed to generate speech: {tts_response.text}"}), tts_response.status_code
    
    # Return the base64 audio data
    return jsonify({"audio": tts_response.text})

@app.route('/tts_stream', methods=['POST'])
def stream_tts():
    """Get audio from non-streaming endpoint but deliver it to the browser"""
    data = request.json
    
    # Use the non-streaming endpoint which is more reliable
    try:
        # Remove streaming-specific parameters
        non_streaming_data = {
            "text": data["text"],
            "language": data["language"],
            "speaker_embedding": data["speaker_embedding"],
            "gpt_cond_latent": data["gpt_cond_latent"]
        }
        
        response = requests.post(
            f"{XTTS_SERVER_URL}/tts",
            json=non_streaming_data
        )
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to generate speech"}), response.status_code
        
        # Convert the base64 response to binary
        audio_base64 = response.text.strip('"')
        audio_data = base64.b64decode(audio_base64)
        
        # Return as a streaming response to the browser
        return Response(io.BytesIO(audio_data), mimetype="audio/wav")
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
