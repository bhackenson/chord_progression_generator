<script>
    import SheetMusic from "./SheetMusic.svelte";
    import Store from "./Store.js";
    import StoreSampler from "./StoreSampler";
    import { onMount } from "svelte";
    import * as Tone from 'tone';

    let currClicked = null;
    let mode = "";
    let currTimeSig = null;
    let tempo = 100;
    let sampler = null;
    let chordnames = [];
    let isContextActivated = false;
    let progLoading = false;
    let firstProgression = false;

    let progression = {};

    let activeKeys = {
    "C2": false,
    "C#2": false,
    "D2": false,
    "D#2": false,
    "E2": false,
    "F2": false,
    "F#2": false,
    "G2": false,
    "G#2": false,
    "A2": false,
    "A#2": false,
    "B2": false,

    "C3": false,
    "C#3": false,
    "D3": false,
    "D#3": false,
    "E3": false,
    "F3": false,
    "F#3": false,
    "G3": false,
    "G#3": false,
    "A3": false,
    "A#3": false,
    "B3": false,

    "C4": false,
    "C#4": false,
    "D4": false,
    "D#4": false,
    "E4": false,
    "F4": false,
    "F#4": false,
    "G4": false,
    "G#4": false,
    "A4": false,
    "A#4": false,
    "B4": false,

    "C5": false,
    "C#5": false,
    "D5": false,
    "D#5": false,
    "E5": false,
    "F5": false,
    "F#5": false,
    "G5": false,
    "G#5": false,
    "A5": false,
    "A#5": false,
    "B5": false
}

    const note_to_id = {
        'C': 'C', 'B#': 'C',
        'C#': 'C#', 'Db': "C#",
        'D': 'D',
        'D#': 'D#', 'Eb': 'D#',
        'E': 'E', 'Fb': 'E',
        'F': 'F', 'E#': 'E#',
        'F#': 'F#', 'Gb': 'F#',
        'G': 'G',
        'G#': 'G#', 'Ab': 'G#',
        'A': 'A',
        'A#': 'A#', 'Bb': 'A#',
        'B': 'B', 'Cb': 'B'
    }

    onMount(async () => {
        await Tone.start();
        let sampler1 = new Tone.Sampler({
            urls: {
                "C2": "C2.m4a",
                "C3": "C3.m4a",
                "C4": "C4.m4a",
                "E4": "E4.m4a",
                "G4": "G4.m4a",
                "C5": "C5.m4a"
            },
            baseUrl: "/audio/",
            release: 1
        }).toDestination();

        Store.set({"key_signature": "", "mode": "", "time_signature": "", "tempo": 0, "chords": [], "melody": []});
        Store.subscribe(progobj => { progression = progobj; });
        Store.subscribe(progobj => {
            chordnames = progobj.chords.map(chord_obj => chord_obj.chord);
        })

        StoreSampler.set(sampler1);
        StoreSampler.subscribe((s) => { sampler = s; });
        StoreSampler.update(s => { return s; });
    });

    async function activateAudioContext() {
        await Tone.start();
        console.log("activated");
        isContextActivated = true;
    }
    
    function highlightKey(id) {
        activeKeys[id] = true;
    }

    function unhighlightKey(id) {
        activeKeys[id] = false;
    }

    function startNote(n) {
        sampler.triggerAttack(n);
    }

    function stopNote(n) {
        sampler.triggerRelease(n);
    }

    function playChord(chord, len) {
        sampler.triggerAttackRelease(chord, len);
    }

    async function playProg() {
       const data_chords = progression.chords;
       const data_melody = progression.melody;
       const time_sig = progression.time_signature;
       const tempo = progression.tempo;
        
        const chords = []
        for (let chord of data_chords) { chords.push(chord.notes) }
        const melody = data_melody;

        const playbtn = document.getElementById("playbtn");

        if (time_sig == "4/4") {
            Tone.getTransport().bpm.value = tempo;
            Tone.getTransport().timeSignature = [4, 4];
            const part = new Tone.Part(((time, chord) => {
                Tone.getTransport().scheduleOnce(() => {
                for (let note of chord) { unhighlightKey(note_to_id[note.slice(0, -1)] + note.charAt(note.length - 1)); }
                }, "+16n");
                sampler.triggerAttackRelease(chord, "4n", time);
                for (let note of chord) { highlightKey(note_to_id[note.slice(0, -1)] + note.charAt(note.length - 1)); }
            }),[[0,     chords[0].concat(melody[0][0])],
                ["0:0:2", [melody[0][1]]],
                ["0:1:0", [melody[0][2]]],
                ["0:1:2", [melody[0][3]]],
                ["0:2", chords[1].concat(melody[1][0])],
                ["0:2:2", [melody[1][1]]],
                ["0:3:0", [melody[0][2]]],
                ["0:3:2", [melody[0][3]]],
                ["1:0", chords[2].concat(melody[2][0])],
                ["1:0:2", [melody[2][1]]],
                ["1:1:0", [melody[2][2]]],
                ["1:1:2", [melody[2][3]]],
                ["1:2", chords[3].concat(melody[3][0])],
                ["1:2:2", [melody[3][1]]],
                ["1:3:0", [melody[3][2]]],
                ["1:3:2", [melody[3][3]]]])
            .start(0);

            Tone.getTransport().scheduleOnce(() => {
                part.stop();
                part.dispose();
                Tone.getTransport().stop();
                if (playbtn) playbtn.disabled = false;
                for (let key in activeKeys) { activeKeys[key] = false; }
            }, '2m');

            Tone.getTransport().scheduleOnce(() => {
                if (playbtn) playbtn.disabled = true;   
            }, 0);

            Tone.getTransport().start();
            return;
        }

        if (time_sig == "3/4" || time_sig == "6/8") {
            Tone.getTransport().bpm.value = tempo;
            Tone.getTransport().timeSignature = [3, 4];
            const part = new Tone.Part(((time, chord) => {
                Tone.getTransport().scheduleOnce(() => {
                for (let note of chord) { unhighlightKey(note_to_id[note.slice(0, -1)] + note.charAt(note.length - 1)); }
                }, "+8n");
                sampler.triggerAttackRelease(chord, "4n", time);
                for (let note of chord) { console.log("highlighted: " + note); highlightKey(note_to_id[note.slice(0, -1)] + note.charAt(note.length - 1)); }
            }),[[0,     chords[0].concat(melody[0][0])],
                ["0:1:0", [melody[0][1]]],
                ["0:2:0", [melody[0][2]]],
                ["1:0:0", chords[1].concat(melody[1][0])],
                ["1:1:0", [melody[1][1]]],
                ["1:2:0", [melody[0][2]]],
                ["2:0:0", chords[2].concat(melody[2][0])],
                ["2:1:0", [melody[2][1]]],
                ["2:2:0", [melody[2][2]]],
                ["3:0:0", chords[3].concat(melody[3][0])],
                ["3:1:0", [melody[3][1]]],
                ["3:2:0", [melody[3][2]]]])
            .start(0);

            Tone.getTransport().scheduleOnce(() => {
                part.stop();
                part.dispose();
                Tone.getTransport().stop();
                if (playbtn) playbtn.disabled = false;
            }, '4m');

            Tone.getTransport().scheduleOnce(() => {
                if (playbtn) playbtn.disabled = true;   
            }, 0);

            Tone.getTransport().start();
            return;
        }
    }

    async function generate() {
      progLoading = true;

      const genbtn = document.getElementById("genbtn")
      if (genbtn) genbtn.disabled = true;

      const playbtn = document.getElementById("playbtn");
      if (playbtn) playbtn.disabled = true;

      const exportbtn = document.getElementById("exportbtn");
      if (exportbtn) exportbtn.disabled = true;

      try {
        const response = await fetch(`http://chord-progression-generator-serv:5000/api/get_progression`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({"key_signature": currClicked.id, "mode": mode, "time_signature": currTimeSig.id, "tempo": tempo})
          });
        const data = await response.json();
        Store.update((progobj) => {
            return data.progression;
        });
      }
      catch(e) {
        console.error('Error fetching data: ', e);
      }

      finally {
        progLoading = false;
        genbtn.disabled = false;
        playbtn.disabled = false;
        exportbtn.disabled = false;
        firstProgression = true;
      }
    }

    const selectTime = (time) => {
        var timebtn = document.getElementById(time);

        if (currTimeSig && currTimeSig !== timebtn) {
            currTimeSig.style.backgroundColor = "lightblue";
        }

        if (timebtn.style.backgroundColor === "rgb(142, 177, 189)") {
            timebtn.style.backgroundColor = "lightblue";
            currTimeSig = null;
            let d = document.getElementById("genbtn");
            d.disabled = true;
        }
        else {
            timebtn.style.backgroundColor = "rgb(142, 177, 189)";
            currTimeSig = timebtn;
            let d = document.getElementById("genbtn");
            if (currClicked) { d.disabled = false; }
            else { d.disabled = true; }
      //TODO
        }
    }

    async function selectKey(id) {
        if (id.toUpperCase() !== id) { mode = "minor" }
        else { mode = "major"; }

        var div = document.getElementById(id);

        if (currClicked && currClicked !== div) {
            currClicked.style.backgroundColor = "lightblue";
        }

        if (div.style.backgroundColor === "rgb(142, 177, 189)") {
            div.style.backgroundColor = "lightblue";
            currClicked = null;
            let d = document.getElementById("genbtn");
            d.disabled = true;
        }
        else {
            div.style.backgroundColor = "rgb(142, 177, 189)";
            currClicked = div;
            let d = document.getElementById("genbtn");
            if (currTimeSig) { d.disabled = false; }
            else {d.disabled = true; }

            switch (id) {
              case "G-":
                playChord(['Gb4', 'Bb4', 'Db4'], "4n");
                break;
              case "B":
                playChord(['B4', 'D#4', 'F#4'], "4n");
                break;
              case "E":
                playChord(['E4', 'G#4', 'B4'], "4n")
                break;
              case "A":
                playChord(['A4', 'C#4', 'E4'], "4n")
                break;
              case "D":
                playChord(['D4', 'F#4', 'A4'], "4n")
                break;
              case "G":
                playChord(['G4', 'B4', 'D4'], "4n")
                break;
              case "C":
                playChord(['C4', 'E4', 'G4'], "4n")
                break;
              case "F":
                playChord(['F4', 'A4', 'C4'], "4n")
                break;
              case "B-":
                playChord(['Bb4', 'D4', 'F4'], "4n")
                break;
              case "E-":
                playChord(['Eb4', 'G4', 'Bb4'], "4n")
                break;
              case "A-":
                playChord(['Ab4', 'C4', 'Eb4'], "4n")
                break;
              case "D-":
                playChord(['Db4', 'F4', 'Ab4'], "4n")
                break;

              case "e-":
                playChord(['Eb4', 'Gb4', 'Bb4'], "4n");
                break;
              case "g#":
                playChord(['G#4', 'B4', 'D#4'], "4n");
                break;
              case "c#":
                playChord(['C#4', 'E4', 'G#4'], "4n");
                break;
              case "f#":
                playChord(['F#4', 'A4', 'C#4'], "4n");
                break;
              case "b":
                playChord(['B4', 'D4', 'F#4'], "4n");
                break;
              case "e":
                playChord(['E4', 'G4', 'B4'], "4n");
                break;
              case "a":
                playChord(['A4', 'C4', 'E4'], "4n");
                break;
              case "d":
                playChord(['D4', 'F4', 'A4'], "4n");
                break;
              case "g":
                playChord(['G4', 'Bb4', 'D4'], "4n");
                break;
              case "c":
                playChord(['C4', 'Eb4', 'G4'], "4n");
                break;
              case "f":
                playChord(['F4', 'Ab4', 'C4'], "4n");
                break;
              case "b-":
                playChord(['Bb4', 'Db4', 'F4'], "4n");
                break;
            }

        }
    }

    async function createMidiFile() {
        const response = await fetch(`http://chord-progression-generator-serv:5000/api/send_midi`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({progression})
        });
        if (!response.ok) {
            if (response.status == 400) {
                alert("Error creating MIDI file.")
            }
            else {
                console.log({"status": response.status, "message": "Error creating MIDI file."});
            }
            return;
        }

        const blob = await response.blob();
        const URL = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = URL;
        a.download = "export.mid";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(URL);
    };
</script>
  <div class="container">
    <div class="create-progression">
        <div class="wheels">
            <div class ="wheels-container">
                <div class="circle-container">
                    <div class="slice" id="G-" on:click={() => selectKey('G-')}><p class="key k1"><b>G&#9837;/F&#9839;</b></p></div>
                    <div class="slice" id="B" on:click={() => selectKey('B')}><p class="key k2"><b>B</b></p></div>
                    <div class="slice" id="E" on:click={() => selectKey('E')}><p class="key k3"><b>E</b></p></div>
                    <div class="slice" id="A" on:click={() => selectKey('A')}><p class="key k4"><b>A</b></p></div>
                    <div class="slice" id="D" on:click={() => selectKey('D')}><p class="key k5"><b>D</b></p></div>
                    <div class="slice" id="G" on:click={() => selectKey('G')}><p class="key k6"><b>G</b></p></div>
                    <div class="slice" id="C" on:click={() => selectKey('C')}><p class="key k7"><b>C</b></p></div>
                    <div class="slice" id="F" on:click={() => selectKey('F')}><p class="key k8"><b>F</b></p></div>
                    <div class="slice" id="B-" on:click={() => selectKey('B-')}><p class="key k9"><b>B&#9837;</b></p></div>
                    <div class="slice" id="E-" on:click={() => selectKey('E-')}><p class="key k10"><b>E&#9837;</b></p></div>
                    <div class="slice" id="A-" on:click={() => selectKey('A-')}><p class="key k11"><b>A&#9837;</b></p></div>
                    <div class="slice" id="D-" on:click={() => selectKey('D-')}><p class="key k12"><b>D&#9837;</b></p></div>
                    <div class="inner-circle"><p><b>Major</b></p></div>
                </div>
                <div class="circle-container">
                    <div class="slice" id="e-" on:click={() => selectKey('e-')}><p class="key k1"><b>e&#9837;/d&#9839;</b></p></div>
                    <div class="slice" id="g#" on:click={() => selectKey('g#')}><p class="key k2"><b>g&#9839;</b></p></div>
                    <div class="slice" id="c#" on:click={() => selectKey('c#')}><p class="key k3"><b>c&#9839;</b></p></div>
                    <div class="slice" id="f#" on:click={() => selectKey('f#')}><p class="key k4"><b>f&#9839;</b></p></div>
                    <div class="slice" id="b" on:click={() => selectKey('b')}><p class="key k5"><b>b</b></p></div>
                    <div class="slice" id="e" on:click={() => selectKey('e')}><p class="key k6"><b>e</b></p></div>
                    <div class="slice" id="a" on:click={() => selectKey('a')}><p class="key k7"><b>a</b></p></div>
                    <div class="slice" id="d" on:click={() => selectKey('d')}><p class="key k8"><b>d</b></p></div>
                    <div class="slice" id="g" on:click={() => selectKey('g')}><p class="key k9"><b>g</b></p></div>
                    <div class="slice" id="c" on:click={() => selectKey('c')}><p class="key k10"><b>c</b></p></div>
                    <div class="slice" id="f" on:click={() => selectKey('f')}><p class="key k11"><b>f</b></p></div>
                    <div class="slice" id="b-" on:click={() => selectKey('b-')}><p class="key k12"><b>b&#9837;</b></p></div>
                    <div class="inner-circle"><p><b>Minor</b></p></div>
                </div>
            </div>
        <div class="time-sigs">
            <p><b>Time signature:</b></p>
            <input type='button' id="4/4" class="time-sig" value="4/4" on:click={() => selectTime("4/4")} name="4/4">
            <input type='button' id="3/4" class="time-sig" value="3/4" on:click={() => selectTime("3/4")} name="3/4">
            <input type='button' id="6/8" class="time-sig" value="6/8" on:click={() => selectTime("6/8")} name="6/8">
            <div>&emsp;</div>
            <p><b>Tempo:</b></p>
            <div class="tempo-btn">
                <input type="number" min="24" max="200" class="input" bind:value={tempo} name="tempo" placeholder="Enter tempo">
            </div>
        </div>
        </div>
        <div class="generate-btn">
            <input id="genbtn" type='submit' class="submit" value="Generate" on:click={generate} disabled>
        </div>
    </div>
    <div id="sheetmusic" class:loading={progLoading}>
      <div class="chordnames">
        {#each chordnames as c}
            <p class="chordname"><b>{c}</b></p>
        {/each}
    </div>
      <div id="prog" class='progression'>
        <p id="prog-hidden" hidden={firstProgression}><i>No current progression</i></p>
        <SheetMusic/>
      </div>
      <div class="musicbtn">
            <button id="playbtn" class="play-btn" on:click={playProg} hidden={!firstProgression}>Play progression</button>
            <button id="exportbtn" class="export-btn" on:click={createMidiFile} hidden={!firstProgression}>Export to MIDI</button>
      </div>
    </div>
    <button class="audio-btn" on:click={activateAudioContext} hidden={isContextActivated}>Enable audio</button>
    <div class="piano">
      <div id = "C2" class="white-key" class:highlightwhite={activeKeys["C2"]} on:mousedown={() => startNote('C2')} on:mouseup={() => stopNote('C2')}></div>
      <div id = "C#2" class="black-key" class:highlightblack={activeKeys["C#2"]} on:mousedown={() => startNote('C#2')} on:mouseup={() => stopNote('C#2')}></div>
      <div id = "D2" class="white-key" class:highlightwhite={activeKeys["D2"]} on:mousedown={() => startNote('D2')} on:mouseup={() => stopNote('D2')}></div>
      <div id = "D#2" class="black-key" class:highlightblack={activeKeys["D#2"]} on:mousedown={() => startNote('D#2')} on:mouseup={() => stopNote('D#2')}></div>
      <div id = "E2" class="white-key" class:highlightwhite={activeKeys["E2"]} on:mousedown={() => startNote('E2')} on:mouseup={() => stopNote('E2')}></div>
      <div id = "F2" class="white-key" class:highlightwhite={activeKeys["F2"]} on:mousedown={() => startNote('F2')} on:mouseup={() => stopNote('F2')}></div>
      <div id = "F#2" class="black-key" class:highlightblack={activeKeys["F#2"]} on:mousedown={() => startNote('F#2')} on:mouseup={() => stopNote('F#2')}></div>
      <div id = "G2" class="white-key" class:highlightwhite={activeKeys["G2"]} on:mousedown={() => startNote('G2')} on:mouseup={() => stopNote('G2')}></div>
      <div id = "G#2" class="black-key" class:highlightblack={activeKeys["G#2"]} on:mousedown={() => startNote('G#2')} on:mouseup={() => stopNote('G#2')}></div>
      <div id = "A2" class="white-key" class:highlightwhite={activeKeys["A2"]} on:mousedown={() => startNote('A2')} on:mouseup={() => stopNote('A2')}></div>
      <div id = "A#2" class="black-key" class:highlightblack={activeKeys["A#2"]} on:mousedown={() => startNote('A#2')} on:mouseup={() => stopNote('A#2')}></div>
      <div id = "B2" class="white-key" class:highlightwhite={activeKeys["B2"]} on:mousedown={() => startNote('B2')} on:mouseup={() => stopNote('B2')}></div>
      
      <div id = "C3" class="white-key" class:highlightwhite={activeKeys["C3"]} on:mousedown={() => startNote('C3')} on:mouseup={() => stopNote('C3')}></div>
      <div id = "C#3" class="black-key" class:highlightblack={activeKeys["C#3"]} on:mousedown={() => startNote('C#3')} on:mouseup={() => stopNote('C#3')}></div>
      <div id = "D3" class="white-key" class:highlightwhite={activeKeys["D3"]} on:mousedown={() => startNote('D3')} on:mouseup={() => stopNote('D3')}></div>
      <div id = "D#3" class="black-key" class:highlightblack={activeKeys["D#3"]} on:mousedown={() => startNote('D#3')} on:mouseup={() => stopNote('D#3')}></div>
      <div id = "E3" class="white-key" class:highlightwhite={activeKeys["E3"]} on:mousedown={() => startNote('E3')} on:mouseup={() => stopNote('E3')}></div>
      <div id = "F3" class="white-key" class:highlightwhite={activeKeys["F3"]} on:mousedown={() => startNote('F3')} on:mouseup={() => stopNote('F3')}></div>
      <div id = "F#3" class="black-key" class:highlightblack={activeKeys["F#3"]} on:mousedown={() => startNote('F#3')} on:mouseup={() => stopNote('F#3')}></div>
      <div id = "G3" class="white-key" class:highlightwhite={activeKeys["G3"]} on:mousedown={() => startNote('G3')} on:mouseup={() => stopNote('G3')}></div>
      <div id = "G#3" class="black-key" class:highlightblack={activeKeys["G#3"]} on:mousedown={() => startNote('G#3')} on:mouseup={() => stopNote('G#3')}></div>
      <div id = "A3" class="white-key" class:highlightwhite={activeKeys["A3"]} on:mousedown={() => startNote('A3')} on:mouseup={() => stopNote('A3')}></div>
      <div id = "A#3" class="black-key" class:highlightblack={activeKeys["A#3"]} on:mousedown={() => startNote('A#3')} on:mouseup={() => stopNote('A#3')}></div>
      <div id = "B3" class="white-key" class:highlightwhite={activeKeys["B3"]} on:mousedown={() => startNote('B3')} on:mouseup={() => stopNote('B3')}></div>

      <div id = "C4" class="white-key" class:highlightwhite={activeKeys["C4"]} on:mousedown={() => startNote('C4')} on:mouseup={() => stopNote('C4')}></div>
      <div id = "C#4" class="black-key" class:highlightblack={activeKeys["C#4"]} on:mousedown={() => startNote('C#4')} on:mouseup={() => stopNote('C#4')}></div>
      <div id = "D4" class="white-key" class:highlightwhite={activeKeys["D4"]} on:mousedown={() => startNote('D4')} on:mouseup={() => stopNote('D4')}></div>
      <div id = "D#4" class="black-key" class:highlightblack={activeKeys["D#4"]} on:mousedown={() => startNote('D#4')} on:mouseup={() => stopNote('D#4')}></div>
      <div id = "E4" class="white-key" class:highlightwhite={activeKeys["E4"]} on:mousedown={() => startNote('E4')} on:mouseup={() => stopNote('E4')}></div>
      <div id = "F4" class="white-key" class:highlightwhite={activeKeys["F4"]} on:mousedown={() => startNote('F4')} on:mouseup={() => stopNote('F4')}></div>
      <div id = "F#4" class="black-key" class:highlightblack={activeKeys["F#4"]} on:mousedown={() => startNote('F#4')} on:mouseup={() => stopNote('F#4')}></div>
      <div id = "G4" class="white-key" class:highlightwhite={activeKeys["G4"]} on:mousedown={() => startNote('G4')} on:mouseup={() => stopNote('G4')}></div>
      <div id = "G#4" class="black-key" class:highlightblack={activeKeys["G#4"]} on:mousedown={() => startNote('G#4')} on:mouseup={() => stopNote('G#4')}></div>
      <div id = "A4" class="white-key" class:highlightwhite={activeKeys["A4"]} on:mousedown={() => startNote('A4')} on:mouseup={() => stopNote('A4')}></div>
      <div id = "A#4" class="black-key" class:highlightblack={activeKeys["A#4"]} on:mousedown={() => startNote('A#4')} on:mouseup={() => stopNote('A#4')}></div>
      <div id = "B4" class="white-key" class:highlightwhite={activeKeys["B4"]} on:mousedown={() => startNote('B4')} on:mouseup={() => stopNote('B4')}></div>

      <div id = "C5" class="white-key" class:highlightwhite={activeKeys["C5"]} on:mousedown={() => startNote('C5')} on:mouseup={() => stopNote('C5')}></div>
      <div id = "C#5" class="black-key" class:highlightblack={activeKeys["C#5"]} on:mousedown={() => startNote('C#5')} on:mouseup={() => stopNote('C#5')}></div>
      <div id = "D5" class="white-key" class:highlightwhite={activeKeys["D5"]} on:mousedown={() => startNote('D5')} on:mouseup={() => stopNote('D5')}></div>
      <div id = "D#5" class="black-key" class:highlightblack={activeKeys["D#5"]} on:mousedown={() => startNote('D#5')} on:mouseup={() => stopNote('D#5')}></div>
      <div id = "E5" class="white-key" class:highlightwhite={activeKeys["E5"]} on:mousedown={() => startNote('E5')} on:mouseup={() => stopNote('E5')}></div>
      <div id = "F5" class="white-key" class:highlightwhite={activeKeys["F5"]}  on:mousedown={() => startNote('F5')} on:mouseup={() => stopNote('F5')}></div>
      <div id = "F#5" class="black-key" class:highlightblack={activeKeys["F#5"]} on:mousedown={() => startNote('F#5')} on:mouseup={() => stopNote('F#5')}></div>
      <div id = "G5" class="white-key" class:highlightwhite={activeKeys["G5"]} on:mousedown={() => startNote('G5')} on:mouseup={() => stopNote('G5')}></div>
      <div id = "G#5" class="black-key" class:highlightblack={activeKeys["G#5"]} on:mousedown={() => startNote('G#5')} on:mouseup={() => stopNote('G#5')}></div>
      <div id = "A5" class="white-key" class:highlightwhite={activeKeys["A5"]} on:mousedown={() => startNote('A5')} on:mouseup={() => stopNote('A5')}></div>
      <div id = "A#5" class="black-key" class:highlightblack={activeKeys["A#5"]} on:mousedown={() => startNote('A#5')} on:mouseup={() => stopNote('A#5')}></div>
      <div id = "B5" class="white-key" class:highlightwhite={activeKeys["B5"]} on:mousedown={() => startNote('B5')} on:mouseup={() => stopNote('B5')}></div>
    </div>
  </div>

<style>
    * {
        font-family: Arial, Helvetica, sans-serif;
    }

    .audio-btn {
        position: absolute;
        top: 0;
        border: none;
        font-size: medium;
        padding: 10px 10px;
        color: black;
        background-color: lightyellow;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
        transition: background-color 0.3s;
    }

    .musicbtn {
      display: flex;
      margin-top: 30px;
      font-size: 14px;
      border-radius: 5px;
      justify-content: space-around;
      align-items: center;
    }

    .audio-btn:hover {
        cursor: pointer;
        background-color: rgb(239, 239, 210)
    }

    .play-btn, .export-btn {
        border: none;
        color: black;
        background-color: lightblue;
        border-radius: 10px;
        padding-top: 15px;
        padding-bottom: 15px;
        padding-left: 20px;
        padding-right: 20px;
        font-size: x-large;
        transition: background-color 0.3s;
    }

    .play-btn:not(:disabled):hover, .export-btn:not(:disabled):hover {
        cursor: pointer;
        background-color: rgb(160, 199, 212);
    }

    .play-btn:not(:disabled):active, .export-btn:not(:disabled):active {
        cursor: pointer;
        background-color: rgb(142, 177, 189);
    }

    .play-btn:disabled, .export-btn:disabled {
      cursor: not-allowed;
      opacity: 50%;
      transition: none;
    }

    .container {
        position: relative;
        display: grid;
        justify-content: center;
        align-items: center;
        /*height: 98vh;
        width: 98vw;*/
        height: 855px;
        width: 1485px;
  }
    .input {
      border-style: solid;
      border-radius: 8px;
      display: block;
      width: 50%;
      font-size: 1.125rem;
      padding: 1rem 0.25rem;
      margin-top: 1rem;
      margin-bottom: 1rem;
      justify-content: center;
  }

    .create-progression {
        border: 1px solid #2c2c2c;
        position: absolute;
        top: 0;
        height: 606px;
        width: 844px;
        align-content: center;
        justify-content: center;
        align-items: center;
    }

    .time-sigs {
        display: flex;
        margin-top: 1rem;
        width: 100%;
        justify-content: center;
        align-items: center;
    }

    .time-sig {
        border-style: none;
        font-size: 1.5rem;
        padding: 0.5rem 0.5rem;
        color: black;
        border-radius: 8px;
        margin-left: 0.5rem;
        margin-right: 0.5rem;
        background-color: lightblue;
        transition: background-color 0.2s;
        align-items: center;
    }

    .time-sig:hover {
        cursor: pointer;
        background-color: rgb(160, 199, 212);
    }

    #sheetmusic {
      border: 1px solid #2c2c2c;
      position: absolute;
      top: 0;
      width: 638px;
      left: 845px;
      height: 606px;
      display: block;
      /* flex-direction: column; */
      justify-content: center;
      align-items: center;
      /* max-height: 500px; */
      overflow: hidden;
      transition: max-height 0.5s ease;
      opacity: 1;
    }

    #sheetmusic.loading {
     opacity: 50%;
    }

    #prog-hidden {
        width: 400px;
        font-size: x-large;
        color: dimgray;
        position: absolute;
        justify-content: center;
        align-items: center;
        padding-left: 180px;
    }

    .progression {
        height: 350px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: rgb(228, 228, 228);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

  .wheels {
    display: block;
    justify-content: center;
  }
  .wheels-container {
    display: flex;
    justify-content: center;
  }

  .circle-container {
    margin-top: 10px;
    margin-bottom: 10px;
    margin-left: 10px;
    margin-right: 10px;
    position: relative;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    overflow: hidden;
  }

  .inner-circle {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: Arial, Helvetica, sans-serif;
    font-size: x-large;
    left: 25%;
    bottom: -25%;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background-color: white;
  }

  .slice {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    bottom: 0;
    width: 50%;
    height: 50%;
    left: 25%;
    transform-origin: top center;
    clip-path: polygon(50% 0, 75% 100%, 25% 100%);
    background-color: lightblue;
    transition: background-color 0.2s;
  }

  .slice:hover {
    cursor: pointer;
    background-color: rgb(160, 199, 212);
  }

  .slice:nth-child(1) { transform: rotate(0deg); }
  .slice:nth-child(2) { transform: rotate(-30deg); }
  .slice:nth-child(3) { transform: rotate(-60deg); }
  .slice:nth-child(4) { transform: rotate(-90deg); }
  .slice:nth-child(5) { transform: rotate(-120deg); }
  .slice:nth-child(6) { transform: rotate(-150deg); }
  .slice:nth-child(7) { transform: rotate(-180deg); }
  .slice:nth-child(8) { transform: rotate(-210deg); }
  .slice:nth-child(9) { transform: rotate(-240deg); }
  .slice:nth-child(10) { transform: rotate(-270deg); }
  .slice:nth-child(11) { transform: rotate(-300deg); }
  .slice:nth-child(12) { transform: rotate(-330deg); }

  .key {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 25%;
    height: 25%;
    bottom: 0;
    position: absolute;
    font-size: x-large;
    color: black;
    transform-origin: center;
  }

  .k1 { transform: rotate(0deg); }
  .k2 { transform: rotate(30deg); }
  .k3 { transform: rotate(60deg); }
  .k4 { transform: rotate(90deg); }
  .k5 { transform: rotate(120deg); }
  .k6 { transform: rotate(150deg); }
  .k7 { transform: rotate(180deg); }
  .k8 { transform: rotate(210deg); }
  .k9 { transform: rotate(240deg); }
  .k10 { transform: rotate(270deg); }
  .k11 { transform: rotate(300deg); }
  .k12 { transform: rotate(330deg); }

  .tempo-btn {
    display: flex;
    justify-content: center;
  }

  .generate-btn {
    display: flex;
    margin-top: 10px;
    margin-bottom: 10px;
    justify-content: center;
    align-items: center;
  }

  .submit {
        border-style: none;
        display: block;
        width: 50%;
        font-size: x-large;
        padding: 10px 10px;
        color: black;
        background-color: lightblue;
        border-radius: 10px;
        margin-bottom: 10px;
        transition: background-color 0.3s;
    }

    .submit:not(:disabled):hover {
        cursor: pointer;
        background-color: rgb(160, 199, 212);
    }

    .submit:not(:disabled):active {
        cursor: pointer;
        background-color: rgb(142, 177, 189);
    }

    .submit:disabled {
      cursor: not-allowed;
      opacity: 50%;
      transition: none;
    }

    .piano {
        display: flex;
        position: absolute;
        top: 607px;
        left: 0;
        height: 248px;
        width: 1485px;
        /* width: 100%; */
    }

    .white-key {
        border: 1px solid #2c2c2c;
        border-bottom-left-radius: 5%;
        border-bottom-right-radius: 5%;
        margin-left: 2px;
        margin-right: 2px;
        width: 51px;
        height: 247px;
        background-color: #fff;
        z-index: 1;
    }
    #C2 {
        margin-left: 0;
    }

    #B5 {
        margin-right: 0;
    }

    .white-key:hover {
      background-color: rgb(234, 234, 234);
    }

    .white-key:active {
      background-color: rgb(187, 187, 187);
    }

    .black-key {
      width: 25px;
      height: 150px;
      background: linear-gradient(to bottom, #2c2c2c 67% , rgb(124, 124, 124) 100%);
      border-bottom-left-radius: 8%;
      border-bottom-right-radius: 8%;
      margin-left: -14px;
      margin-right: -14px;
      z-index: 2;
    }

    .black-key:hover {
      filter: brightness(1.3);
    }

    .black-key:active {
      filter: brightness(1.6);
    }

    .highlightwhite {
      background-color: lightblue;
    }

    .highlightblack {
      background: lightblue;
    }

    [id^="C#"], [id^="F#"] {
      margin-left: -18px;
      margin-right: -10px;
    }

    [id^="D#"], [id^="A#"] {
      margin-left: -10px;
      margin-right: -18px;

    }

    .white-key + .white-key {
       margin-left: -1px;
    }

    .chordnames {
      display: flex;
      height: 100px;
      justify-content: center;
      align-items: center;
      white-space: normal;
    }

    .chordname {
        justify-content: center;
        align-items: center;
        text-align: center;
        padding-left: 8px;
        padding-right: 8px;
        font-size: large;
    }

</style>