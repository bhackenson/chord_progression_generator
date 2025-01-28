# Machine Learning Chord Progression Generator
### About
This project uses a Tensorflow Sequential model to generate chord progressions based on a user's selected major or minor key signature, a time signature of one of 4/4, 3/4, or 6/8, and a tempo between 24 and 200.
The model is trained using common pop chord progressions; the dataset for these progressions is provided by this [this repository](https://github.com/ology/Data-Dataset-ChordProgressions/tree/master).
It converts roman numeral chords into 12-length binary vectors denoting which pitches are played in the chord and adds an LSTM layer to capture long-term dependencies in the progression.
A binary cross-entropy loss function guides the model's optimization process. A generated chord progression is converted to a chord progression array with chords written as a list of notes of type `string`.
The frontend application displays sheet music of a generated chord progression provided by the backend's progression model, which the user can play back on the digital piano or export the progression to MIDI.

Dependencies include [Tensorflow](https://pypi.org/project/tensorflow/) for the model, [music21](https://pypi.org/project/music21/) for computational musical analysis,
[Tone.js](https://github.com/Tonejs/Tone.js) for frontend audio context, and [Vexflow](https://github.com/0xfe/vexflow) for sheet music rendering.

The web application for this project can be found [here](https://chord-progression-generator-ysg3n.ondigitalocean.app/).
