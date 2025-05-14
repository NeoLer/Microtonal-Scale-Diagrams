# Microtonal Guitar Scale Diagram Example
```python
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
```
