"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  brother.json

## Model
  constraints: Count, Element, Maximum, Sum

## Execution
  python Harmony.py -data=<datafile.json>
  python Harmony.py -data=<datafile.dzn> -parser=Harmony_ParserZ.py

## Links
  - https://www.ijcai.org/proceedings/2024/858
  - https://www.minizinc.org/challenge2024/results2024.html

## Tags
  realistic, mzn24
"""

from pycsp3 import *

key, melody, mins, max_stationary, enforce_cadences = data
nPitches = 128

notes = [["C"], ["C#", "Db"], ["D"], ["D#", "Eb"], ["E"], ["F"], ["F#", "Gb"], ["G"], ["G#", "Ab"], ["A"], ["A#", "Bb"], ["B"]]
I, ii, iii, IV, V, V7, vi = range(7)
nChords = 7


def pitch_for(note, octave):
    return next(i for i, t in enumerate(notes) if note in t) + (octave + 1) * 12


chord_pitches = [[0, 4, 7], [2, 5, 9], [4, 7, 11], [5, 9, 12], [7, 11, 14], [7, 11, 14, 17], [9, 12, 16]]
chord_offsets = cp_array([[(v + pitch_for(key, 4)) % 12 for v in chord_pitches[c]] for c in range(nChords)])  # cp_array necessary here

perfect_cadences = [(V, I), (V7, I)]
plagal_cadences = [(IV, I)]
imperfect_cadences = [(I, V), (ii, V), (IV, V), (vi, V)]
interrupted_cadences = [(V, vi), (V7, vi)]
all_cadences = perfect_cadences + plagal_cadences + imperfect_cadences + interrupted_cadences

SOPRANO, ALTO, TENOR, BASS = Voices = range(4)
otherVoices = Voices[ALTO:]  # Soprano discarded
nVoices = len(Voices)

voice_ranges = [(pitch_for(*lb), pitch_for(*ub)) for (lb, ub) in [[("C", 4), ("G", 5)], [("G", 3), ("C", 5)], [("C", 3), ("G", 4)], [("F", 2), ("C", 4)]]]

nSteps = len(melody)
assert nSteps % 4 == 0
Time = range(nSteps)

# music[v][t] is the note pitch for the vth voice at time t
music = VarArray(size=[nVoices, nSteps], dom=range(nPitches))

# chord[t] is the chord used at time t
chord = VarArray(size=nSteps, dom=range(nChords))

# note[v][t] is the note for the vth voice at time t
note = VarArray(size=[nVoices, nSteps], dom=range(12))

# the number of non-root position chords
non_root = Var(dom=range(nSteps + 1))

# the number of chords with a note other than the root doubled
non_doubled_root = Var(dom=range(nSteps + 1))

# max_jump[v] is the largest jump by the vth voice
max_jump = VarArray(size=nVoices, dom=range(nPitches))

# useful auxiliary array
cadences = [(chord[t], chord[t + 1]) for t in Time if t % 4 == 2]

satisfy(

    # melody for Soprano
    music[SOPRANO] == melody,

    # computing notes
    [note[v][t] == music[v][t] % 12 for v in Voices for t in Time],

    # played notes must be within allowed ranges
    [music[v][t] in range(lb, ub + 1) for v, (lb, ub) in enumerate(voice_ranges) for t in Time],

    # voices must not cross/overlap
    [Decreasing(music[:, t], strict=True) for t in Time],

    # played notes must be the notes of the chosen chord
    [chord_offsets[chord[t]] == set(note[:, t]) for t in Time],

    # no consecutive 5ths
    [
        If(
            abs(music[v][t] - music[u][t]) % 12 == 7,
            Then=abs(music[v][t + 1] - music[u][t + 1]) % 12 != 7
        ) for t in range(nSteps - 1) for u, v in combinations(nVoices, 2)
    ],

    # no consecutive 8ves
    [
        If(
            abs(music[v][t] - music[u][t]) % 12 == 0,
            Then=abs(music[v][t + 1] - music[u][t + 1]) % 12 != 0
        ) for t in range(nSteps - 1) for u, v in combinations(nVoices, 2)
    ],

    # Soprano-Alto and Alto-Tenor must be less than 8ve apart
    [
        [music[SOPRANO][t] - music[ALTO][t] <= 13 for t in Time],
        [music[ALTO][t] - music[TENOR][t] <= 13 for t in Time]
    ],

    # computing non-root
    non_root == Sum(note[BASS][t] != Minimum(note[:, t]) for t in range(nSteps)),

    # computing non-doubled-root
    non_doubled_root == Sum(ExactlyOne(note[v][t] == Minimum(note[:, t]) for v in Voices) for t in range(nSteps)),

    # chords must change t each time step
    [chord[t] != chord[t + 1] for t in range(nSteps - 1)],

    # enforcing minimum counts of cadence types
    [
        [Count(Exist(both(c[0] == v, c[1] == w) for v, w in perfect_cadences) for c in cadences) >= mins.perfect],
        [Count(Exist(both(c[0] == v, c[1] == w) for v, w in plagal_cadences) for c in cadences) >= mins.plagal],
        [Count(Exist(both(c[0] == v, c[1] == w) for v, w in imperfect_cadences) for c in cadences) >= mins.imperfect],
        [Count(Exist(both(c[0] == v, c[1] == w) for v, w in interrupted_cadences) for c in cadences) >= mins.interrupted]
    ],

    # no repetition of 4 chord progression
    [chord[(t - 1) * 4:t * 4] != chord[t * 4:(t + 1) * 4] for t in range(1, nSteps // 4)],

    # ensuring voices (except soprano) don't stay stationary for too long
    [NotAllEqual(music[v][t:t + max_stationary + 1]) for v in otherVoices for t in range(nSteps - max_stationary)],

    # ensuring phrases have some movement
    [Maximum(music[v][t:t + 8]) - Minimum(music[v][t:t + 8]) > 4 for v in otherVoices for t in range(0, nSteps, 8)],

    # computing the largest jump for each voice
    [max_jump[v] == Maximum(abs(music[v][t] - music[v][t + 1]) for t in range(nSteps - 1)) for v in Voices]
)

if enforce_cadences:
    satisfy(
        # the end of every 4 chords is a cadence
        [c in all_cadences for c in cadences],

        # leading note must go to tonic
        [
            If(
                note[v][t] == (pitch_for(key, 0) + 11) % 12,
                Then=music[v][t + 1] == music[v][t] + 1
            ) for v in Voices for t in range(0, nSteps, 2)
        ],

        # the final cadence must be perfect or plagal
        cadences[-1] in [(V, I), (IV, I)]
    )

minimize(
    Sum(max_jump) + non_root + non_doubled_root
)

"""
1) Note that:
 [chord_offsets[chord[t]] == set(note[:, t]) for t in Time],
  is equivalent to: 

  def T():
    t = []
    for c, offset in enumerate(chord_offsets):
        r = len(offset)
        for p in permutations(range(4)):
            t.extend([(c,) + tuple(offset[v] if v < r else offset[k] for v in p) for k in range(1 if r == 4 else 3)])
    return sorted(list(set(t)))

  [(chord[t], note[:, t]) in T() for t in Time],
"""
