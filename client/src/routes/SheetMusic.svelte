<script>
    import Store from "./Store.js";
    import { Vex } from "vexflow";
    
    let data = {};
    Store.subscribe((progobj) => {
        data = progobj;
    });
    
    const { Factory } = Vex.Flow;
    let container;

    const renderSheetMusic = () => {
        if (!container) return;
        container.innerHTML = '';

        const insertSlash = (str) => { return str.slice(0, (str.length - 1)) + "/" + str.slice((str.length-1)); }

        let keySig = data['key_signature'];
        keySig = String(keySig).toUpperCase() !== String(keySig) ? String(keySig).toUpperCase() + 'm' : String(keySig)
        keySig = keySig.replace("-", "b")
        const time_sig = data.time_signature;
        const chords = data.chords;

        const vf = new Factory({ renderer: { elementId: container, width: 790, height: 300 } });

        if (time_sig == "4/4") {
            const staveTreble1 = new Vex.Flow.Stave(10, 30, 340);
            const staveTreble2 = new Vex.Flow.Stave(350, 30, 220);
            const staveBass1 = new Vex.Flow.Stave(10, 150, 340);
            const staveBass2 = new Vex.Flow.Stave(350, 150, 220);

            staveTreble1.addClef('treble').addTimeSignature('4/4').addKeySignature(keySig);
            staveBass1.addClef('bass').addTimeSignature('4/4').addKeySignature(keySig);

            staveTreble1.setContext(vf.getContext()).draw();
            staveTreble2.setContext(vf.getContext()).draw();
            staveBass1.setContext(vf.getContext()).draw();
            staveBass2.setContext(vf.getContext()).draw();

            let _chords = []; for (let c of chords) { _chords.push(c.notes); }
            _chords = _chords.map(notes => new Vex.Flow.StaveNote({keys: notes.map(n => insertSlash(n)), duration: 'h', clef: 'bass'}));
            let mel1 = data.melody.reduce((acc,e) => acc.concat(e), []).map(n => new Vex.Flow.StaveNote({keys: [insertSlash(n)], duration: "8"}));

            const bassVoice1 = new Vex.Flow.Voice({num_beats: 4, beat_value: 4});
            const bassVoice2 = new Vex.Flow.Voice({num_beats: 4, beat_value: 4});

            bassVoice1.addTickables(_chords.slice(0,2));
            bassVoice2.addTickables(_chords.slice(2,4));

            const trebleVoice1 = new Vex.Flow.Voice({num_beats: 4, beat_value: 4});
            const trebleVoice2 = new Vex.Flow.Voice({num_beats: 4, beat_value: 4});

            trebleVoice1.addTickables(mel1.slice(0,8));
            trebleVoice2.addTickables(mel1.slice(8,16));

            const beams = [
                new Vex.Flow.Beam(mel1.slice(0,4)),
                new Vex.Flow.Beam(mel1.slice(4,8)),
                new Vex.Flow.Beam(mel1.slice(8,12)),
                new Vex.Flow.Beam(mel1.slice(12,16))
            ]

            new Vex.Flow.Formatter()
            .formatToStave([trebleVoice1], staveTreble1)
            .formatToStave([trebleVoice2], staveTreble2)
            .formatToStave([bassVoice1], staveBass1)
            .formatToStave([bassVoice2], staveBass2)

            trebleVoice1.draw(vf.getContext(), staveTreble1);
            trebleVoice2.draw(vf.getContext(), staveTreble2);
            bassVoice1.draw(vf.getContext(), staveBass1);
            bassVoice2.draw(vf.getContext(), staveBass2);

            beams.forEach(beam => beam.setContext(vf.getContext()).draw());

        }
        else if (time_sig == "3/4") {
            const staveTreble1 = new Vex.Flow.Stave(10, 30, 230);
            const staveTreble2 = new Vex.Flow.Stave(240, 30, 110);
            const staveTreble3 = new Vex.Flow.Stave(350, 30, 110);
            const staveTreble4 = new Vex.Flow.Stave(460, 30, 110);
            const staveBass1 = new Vex.Flow.Stave(10, 150, 230);
            const staveBass2 = new Vex.Flow.Stave(240, 150, 110);
            const staveBass3 = new Vex.Flow.Stave(350, 150, 110);
            const staveBass4 = new Vex.Flow.Stave(460, 150, 110);

            staveTreble1.addClef('treble').addTimeSignature('3/4').addKeySignature(keySig);
            staveBass1.addClef('bass').addTimeSignature('3/4').addKeySignature(keySig);

            staveTreble1.setContext(vf.getContext()).draw();
            staveTreble2.setContext(vf.getContext()).draw();
            staveTreble3.setContext(vf.getContext()).draw();
            staveTreble4.setContext(vf.getContext()).draw();
            staveBass1.setContext(vf.getContext()).draw();
            staveBass2.setContext(vf.getContext()).draw();
            staveBass3.setContext(vf.getContext()).draw();
            staveBass4.setContext(vf.getContext()).draw();

            let _chords = []; for (let c of chords) { _chords.push(c.notes); }
            _chords = _chords.map(notes => new Vex.Flow.StaveNote({keys: notes.map(n => insertSlash(n)), duration: 'h', dots: 1, clef: 'bass'}));
            let mel1 = data.melody.reduce((acc,e) => acc.concat(e), []).map(n => new Vex.Flow.StaveNote({keys: [insertSlash(n)], duration: "q"}));

            const bassVoice1 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const bassVoice2 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const bassVoice3 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const bassVoice4 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});

            bassVoice1.addTickables(_chords.slice(0,1));
            bassVoice2.addTickables(_chords.slice(1,2));
            bassVoice3.addTickables(_chords.slice(2,3));
            bassVoice4.addTickables(_chords.slice(3,4));
            
            const trebleVoice1 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const trebleVoice2 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const trebleVoice3 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const trebleVoice4 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});

            trebleVoice1.addTickables(mel1.slice(0,3));
            trebleVoice2.addTickables(mel1.slice(3,6));
            trebleVoice3.addTickables(mel1.slice(6,9));
            trebleVoice4.addTickables(mel1.slice(9,12));

            new Vex.Flow.Formatter()
            .formatToStave([trebleVoice1], staveTreble1)
            .formatToStave([trebleVoice2], staveTreble2)
            .formatToStave([trebleVoice3], staveTreble3)
            .formatToStave([trebleVoice4], staveTreble4)
            .formatToStave([bassVoice1], staveBass1)
            .formatToStave([bassVoice2], staveBass2)
            .formatToStave([bassVoice3], staveBass3)
            .formatToStave([bassVoice4], staveBass4)

            trebleVoice1.draw(vf.getContext(), staveTreble1);
            trebleVoice2.draw(vf.getContext(), staveTreble2);
            trebleVoice3.draw(vf.getContext(), staveTreble3);
            trebleVoice4.draw(vf.getContext(), staveTreble4);
            bassVoice1.draw(vf.getContext(), staveBass1);
            bassVoice2.draw(vf.getContext(), staveBass2);
            bassVoice3.draw(vf.getContext(), staveBass3);
            bassVoice4.draw(vf.getContext(), staveBass4);

        }
        else if (time_sig == "6/8") {
            const staveTreble1 = new Vex.Flow.Stave(10, 30, 340);
            const staveTreble2 = new Vex.Flow.Stave(350, 30, 220);
            const staveBass1 = new Vex.Flow.Stave(10, 150, 340);
            const staveBass2 = new Vex.Flow.Stave(350, 150, 220);

            staveTreble1.addClef('treble').addTimeSignature('6/8').addKeySignature(keySig);
            staveBass1.addClef('bass').addTimeSignature('6/8').addKeySignature(keySig);

            staveTreble1.setContext(vf.getContext()).draw();
            staveTreble2.setContext(vf.getContext()).draw();
            staveBass1.setContext(vf.getContext()).draw();
            staveBass2.setContext(vf.getContext()).draw();

            let _chords = []; for (let c of chords) { _chords.push(c.notes); }
            _chords = _chords.map(notes => new Vex.Flow.StaveNote({keys: notes.map(n => insertSlash(n)), duration: 'q', dots: 1, clef: 'bass'}));
            let mel1 = data.melody.reduce((acc,e) => acc.concat(e), []).map(n => new Vex.Flow.StaveNote({keys: [insertSlash(n)], duration: "8"}));

            const bassVoice1 = new Vex.Flow.Voice({num_beats: 6, beat_value: 8});
            const bassVoice2 = new Vex.Flow.Voice({num_beats: 6, beat_value: 8});

            bassVoice1.addTickables(_chords.slice(0,2));
            bassVoice2.addTickables(_chords.slice(2,4));

            const trebleVoice1 = new Vex.Flow.Voice({num_beats: 6, beat_value: 8});
            const trebleVoice2 = new Vex.Flow.Voice({num_beats: 6, beat_value: 8});

            trebleVoice1.addTickables(mel1.slice(0,6));
            trebleVoice2.addTickables(mel1.slice(6,12));

            const beams = [
                new Vex.Flow.Beam(mel1.slice(0,3)),
                new Vex.Flow.Beam(mel1.slice(3,6)),
                new Vex.Flow.Beam(mel1.slice(6,9)),
                new Vex.Flow.Beam(mel1.slice(9,12))
            ]

            new Vex.Flow.Formatter()
            .formatToStave([trebleVoice1], staveTreble1)
            .formatToStave([trebleVoice2], staveTreble2)
            .formatToStave([bassVoice1], staveBass1)
            .formatToStave([bassVoice2], staveBass2)

            trebleVoice1.draw(vf.getContext(), staveTreble1);
            trebleVoice2.draw(vf.getContext(), staveTreble2);
            bassVoice1.draw(vf.getContext(), staveBass1);
            bassVoice2.draw(vf.getContext(), staveBass2);

            beams.forEach(beam => beam.setContext(vf.getContext()).draw());
        }
    }

    $: data, renderSheetMusic();

</script>
<div bind:this={container}></div>