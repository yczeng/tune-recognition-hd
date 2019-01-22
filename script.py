import csv
import numpy as np

def createSeedVector():
	noteList = ["C", "C#", "Cb", "D", "D#", "Db", "E", "E#", "Eb", "F", "F#", "Fb", "G", "G#", "Gb", "A", "A#", "Ab", "B", "B#", "Bb"]
	notes = {}
	for note in noteList:
		notes[note] = np.random.choice([-1, 1], size=10000)
	return notes

def songVector(noteSequence, songVector):
	noteSequence = noteSequence.replace('#', '# ').replace('b', 'b ').split(" ")
	noteSequence = list(filter(None, noteSequence))
	n = len(noteSequence)

	# print(noteSequence)
	
	# encode trigrams into the songVector
	# wan = rr(w) + r(a) + n
	for i in range(2, n):
		# print(i, "time!")
		firstNote = noteSequence[i-2]
		secondNote = noteSequence[i-1]
		thirdNote = noteSequence[i]

		# print(firstNote, secondNote, thirdNote)
		first = np.concatenate([notes[firstNote][2:], notes[firstNote][0:2]])
		second = np.concatenate([notes[secondNote][1:], notes[secondNote][0:1]])
		third = notes[thirdNote]

		multiplyResult = np.multiply( np.multiply(first, second), third)

		songVector += multiplyResult

	return songVector

if __name__ == "__main__":
	notes = createSeedVector()

	song = {}
	with open('data/themesOG.csv') as csvDataFile:
		csvReader = csv.reader(csvDataFile)

		for count, theme in enumerate(csvReader):
			if count != 0:
				if theme[0] in song:
					song[theme[0]] = songVector(theme[3], song[theme[0]])
				else:
					newSongVector = np.zeros(10000)
					song[theme[0]] = songVector(theme[3], newSongVector)