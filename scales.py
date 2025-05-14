import svgwrite

notes = {
    "A": 0,
    "A#": 1,
    "B": 2,
    "C": 3,
    "C#": 4,
    "D": 5,
    "D#": 6,
    "E": 7,
    "F": 8,
    "F#": 9,
    "G": 10,
    "G#": 11
}

def note_to_num(note, tones=12):
    if tones != 12:
        return notes[note] * (tones/12)
    else:
        return notes[note]

def num_to_note(note):
    return list(notes.keys())[note%len(notes)]

def offset_note(note, steps):
    return num_to_note(note_to_num(note) + steps)

class Fret:
    def __init__(self, note, color):
        self.note = note
        self.color = color
        self.flags = []

class Fretboard:
    num_strings = 6
    tuning = ["E", "B", "G", "D", "A", "E"]
    num_frets = 24
    strings = []
    def __init__(self):
        def fret_note(string_i, fret):
            return offset_note(self.tuning[string_i], fret)

        for string_i in range(self.num_strings):
            string = []
            for fret_i in range(self.num_frets):
                string.append(Fret(fret_note(string_i, fret_i), "gray"))
            self.strings.append(string)

def scale_notes(scale, key):
    notes = []
    at = key
    for step in scale.values:
        at = offset_note(at, step)
        notes.append(at)
    return notes

def annotate_scale(fretboard, scale, key):
    notes = scale_notes(scale, key)
    for string in fretboard.strings:
        for fret in string:
            if fret.note in notes:
                fret.color = "red"

def scale_notes1(scale, key):
    notes = []
    at = note_to_num(key, tones=scale.tones)
    for step in scale.values:
        at = (at + step) % scale.tones
        notes.append(at)
    return notes

def annotate_scale1(fretboard, scale, key):
    notes = scale_notes1(scale, key)
    print(notes)
    for string in fretboard.strings:
        for fret in string:
            if scale.tones == 24:
               frets = [note_to_num(fret.note) * 2, (note_to_num(fret.note) * 2) + 1]
            else:
                frets = [note_to_num(fret.note)]

            if frets[0] in notes:
                fret.flags.append("fret")
                fret.color = "red"
            if len(frets)>1 and frets[1] in notes:
                fret.flags.append("bend")
                fret.color = "red"

def draw_arrow(dwg, x, y, color):
    # Create a new SVG drawing

    # Define the arrow size and position
    arrow_size = 10
    arrow_x = x - arrow_size / 2
    arrow_y = y - arrow_size / 2

    # Define the path data for the upward-facing arrow
    path_data = f"M{arrow_x},{arrow_y + arrow_size} L{arrow_x + arrow_size / 2},{arrow_y} L{arrow_x + arrow_size},{arrow_y + arrow_size} L{arrow_x},{arrow_y + arrow_size}"

    # Create a path element for the arrow
    arrow = dwg.add(dwg.path(d=path_data, fill=color))
    rx = arrow_x + arrow_size/2
    dwg.add(dwg.rect((rx-2, arrow_y+9), (4, 10), fill=color))


def draw_fretboard(fretboard, width=800, height=200):
    fb_height = height * 0.9
    fb_width = width
    fb_y = (height - fb_height) / 2

    fret_spacing = fb_width/fretboard.num_frets
    fret_width = 5
    
    string_spacing = fb_height / (fretboard.num_strings - 1)

    nut_width = 5
    
    print(f"w {width} h {height}")
    dwg = svgwrite.Drawing("guitar_fretboard.svg", profile="tiny")

    bg = dwg.add(dwg.rect((0,0), (width,height), fill="white"))

    img = dwg.add(dwg.rect((0, fb_y), (fb_width, fb_height), fill="white"))

    nut = dwg.add(dwg.rect((0, fb_y), (nut_width, fb_height), fill='gray'))

    # Draw frets
    for i in range(fretboard.num_frets):
        x = fret_spacing * i
        fret = dwg.add(dwg.rect((x - fret_width / 2, fb_y), (fret_width, fb_height), fill="gray"))
    
    # Draw positional markers
    for i in range(1, num_frets):
        x = (i+0.5) * fret_spacing

        if i % 10 == 0:
            y = string_spacing * 1.5
            dwg.add(dwg.circle((x, fb_y+y), 4, fill="gray"))
            dwg.add(dwg.circle((x, fb_y+y), 3, fill="white"))
            y = string_spacing * 3.5
            dwg.add(dwg.circle((x, fb_y+y), 4, fill="gray"))
            dwg.add(dwg.circle((x, fb_y+y), 3, fill="white"))
            continue

        y = string_spacing * 2.5
        if i % 2 == 0:
            dwg.add(dwg.circle((x, fb_y+y), 4, fill="gray"))
            dwg.add(dwg.circle((x, fb_y+y), 3, fill="white"))

    # Draw strings
    for i in range(fretboard.num_strings):
        y = i * string_spacing
        string = dwg.add(dwg.line((0, fb_y + y), (fb_width, fb_y + y), stroke='black'))

    # Draw annotations
    for string_i, string in enumerate(fretboard.strings):
        for fret_i, fret in enumerate(string):
            if fret_i == 0:
                continue
            fret_i = fret_i - 1
            y =  string_i * string_spacing
            x = (fret_i + 0.5) * fret_spacing
            color = fret.color
            xp = x 
            yp = fb_y + y
            if "bend" in fret.flags and "fret" in fret.flags:
                dwg.add(dwg.circle((xp, fb_y + y), 10, fill="black"))
                draw_arrow(dwg, xp, yp-4, "gray")
                #dwg.add(dwg.text(fret.note, (xp-6, yp+6), fill="yellow"))
                # dwg.add(dwg.circle((xp, fb_y + y), 7, fill="black"))
                # dwg.add(dwg.circle((xp, fb_y + y + 3), 7, fill="red"))
                continue
            if "fret" in fret.flags:
                dwg.add(dwg.circle((xp, fb_y + y), 10, fill="black"))
                dwg.add(dwg.circle((xp, fb_y + y), 9, fill="black"))
                #dwg.add(dwg.text(fret.note, (xp-6, yp+6), fill="yellow"))
            if "bend" in fret.flags:
                draw_arrow(dwg, xp, yp-5, "black")
                #dwg.add(dwg.text(fret.note, (xp-6, yp+6), fill="red"))
            

    
    return dwg

def draw_fretboard1(fretboard, width=800, height=200):
    num_frets = fretboard.num_frets
    fretboard_width = width
    fretboard_height = height
    nut_width = 10
    fret_width = 5
    string_spacing = fretboard_height / (fretboard.num_strings - 1)
    fret_spacing = fretboard_width / num_frets

    print(f"width {fretboard_width} height {fretboard_height} num frets {num_frets} num strings {fretboard.num_strings} string spacing {string_spacing} fret_spacing {fret_spacing}   ")
    # Create a new SVG drawing
    dwg = svgwrite.Drawing('guitar_fretboard.svg', profile='tiny')
    
    # Draw the fretboard
    img = dwg.add(dwg.rect((0, 0), (fretboard_width, fretboard_height), fill='beige'))
    
    # Draw the nut
    nut = dwg.add(dwg.rect((0, 0), (nut_width, fretboard_height), fill='gray'))
    
    # Draw the frets
    for i in range(1, num_frets + 1):
        x = i * fret_spacing
        fret = dwg.add(dwg.rect((x - fret_width / 2, 0), (fret_width, fretboard_height), fill='gray'))

    # Draw the strings
    for i in range(fretboard.num_strings):
        y = (i+0.5) * string_spacing
        print(f"string {i} position y: {y}")
        string = dwg.add(dwg.line((0, y), (fretboard_width, y), stroke='black'))
    
    for string_i, string in enumerate(fretboard.strings):
        for fret_i, fret in enumerate(string):
            y =  string_i * string_spacing
            x = fret_i * fret_spacing
            color = fret.color
            # dwg.add(dwg.rect((x - fret_width / 2, y), (fret_width, fret_spacing), fill=color))

    return dwg

class Scale:
    name = ""
    tones = 12
    values = []
    def __init__(self, name, tones, values):
        self.name = name
        self.values = values
        self.tones = tones

scales = {}

def add_scale(name, tones, values):
    if type(values) == type(""):
        values = list(map(int, values.split()))
    scales[name] = Scale(name, tones, values)

whole = 2
half = 1 

add_scale("Pentatonic Ethiopia", 24, [2,8,3,6,5])
add_scale("Natural Minor", 12, [whole, half, whole, whole, half, whole, whole])
add_scale("Major", 12, [whole, whole, half, whole, whole, whole, half])
add_scale("Enharmonic Hypophrygian", 24, [8, 4, 1, 1, 8, 1, 1])
add_scale("Second plagal Byzantine Liturgical mode", 24, [2, 7, 1, 4, 2, 7, 1])
add_scale("Maqam Saba", 24, "3 3 2 6 2 4 2 2")
add_scale("Soft Diatonic Lydian", 24, "3 5 2 3 5 4 2")
add_scale("Maqam Bayati", 24, "3 3 4 4 2 1 3 4")
add_scale("Neutral Hypodorian", 24, "4 3 4 3 3 4 3")
add_scale("1 5 4 4 1 5 4", 24, "1 5 4 4 1 5 4")
add_scale("Enharmonic Lydian", 24, "1 8 1 1 8 4 1")
add_scale("Diminished", 24, "1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2")
# Usage example
num_frets = 24
num_strings = 6

fretboard = Fretboard()

annotate_scale1(fretboard, scales["Maqam Bayati"], "A")
draw_fretboard(fretboard).save()
