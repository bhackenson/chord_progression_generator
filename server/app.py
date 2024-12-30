from flask import Flask, jsonify, request, send_file
import os
from flask_cors import CORS
from generator import build_model, generate_chord_progression, randomize_seed, transpose_chord, show_chord_name, show_melody_notes, create_midi_from_progression

app = Flask(__name__)
CORS(app)

model1 = None
tone1 = None
history1 = None

model2 = None
tone2 = None
history2 = None

major_keys = ["G-", 'B', 'E', 'A', 'D', 'G', 'C', 'F', 'B-', 'E-', 'A-', 'D-']
minor_keys = ['e-', 'g#', 'c#', 'f#', 'b', 'e', 'a', 'd', 'g', 'c', 'f', 'b-']

with app.app_context():
    model1, tone1, history1 = build_model('major')
    model2, tone2, history2 = build_model('minor')

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': 'Unexpected error', 'description': str(e)}), 500

# request input: {"key_signature": "B-", "mode": "major", "time_signature": "4/4", "tempo": 120}
@app.route('/api/get_progression', methods=['POST'])
def get_progression():
    data = request.get_json()
    key = data['key_signature']
    mode = data['mode']
    time_sig = data['time_signature']
    tempo = data['tempo']

    if (key not in major_keys and key not in minor_keys):
        return jsonify({"error": "invalid key"}), 400
    
    if (key in major_keys):
        new_prog, chord_strings = generate_chord_progression(model1, randomize_seed(tone1), 4)
    else:
        new_prog, chord_strings = generate_chord_progression(model2, randomize_seed(tone2), 4)
    progression = {
            "key_signature": key,
            "mode": mode,
            "time_signature": time_sig,
            "tempo": tempo,
            "chords": [show_chord_name(c) for c in [transpose_chord(k, tone2, key) for k in chord_strings]],
            "melody": [show_melody_notes(c, time_sig) for c in [transpose_chord(k, tone2, key) for k in chord_strings]]
        }
    
    return jsonify({"status": "OK", "progression": progression}), 200

"""
request input:
{
   "progression":
        {
            "key_signature": "B-",
            "mode": "minor",
            "time_signature": "3/4",
            "tempo": 100,
            "chords": [
                {
                    "chord": "C major triad",
                    "notes": ["C", "E", "G"]
                },
                {
                    "chord": "A minor triad",
                    "notes": ["A", "C", "E"]
                }
            ],
            "melody": [
            ["E3", "G3", "C4", "E4"],
            ["C3", "E3", "A3", "C4"]
            ]
        }
}
"""
@app.route('/api/send_midi', methods=['POST'])
def send_midi():
    data = request.get_json()
    progression = data['progression']
    file_path = "output.mid"

    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    create_midi_from_progression(chords=progression['chords'],
                                 melody=progression['melody'],
                                 key_sig=progression['key_signature'],
                                 time_sig=progression['time_signature'],
                                 m_tempo=progression['tempo'],
                                 path=file_path)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name="export.mid")
    else:
        return jsonify({"status": "cannnot create file"}), 501

if __name__ == '__main__':
    app.run(debug=True)