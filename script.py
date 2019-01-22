import csv
import numpy as np

def createSeedVector():
	noteList = ["C", "C#", "Cb", "D", "D#", "Db", "E", "E#", "Eb", "F", "F#", "Fb", "G", "G#", "Gb", "A", "A#", "Ab", "B", "B#", "Bb"]
	notes = {}
	for note in noteList:
		notes[note] = np.random.choice([-1, 1], size=10000)
	return notes

def songVector(noteSequence, notes, songVector):
	noteSequence = noteSequence.replace('#', '# ').replace('b', 'b ').split(" ")
	noteSequence = list(filter(None, noteSequence))
	n = len(noteSequence)

	# print(noteSequence)

	# encode trigrams into the songVector
	# wan = rr(w) + r(a) + n
	for i in range(2, n):

		firstNote = noteSequence[i-2]
		secondNote = noteSequence[i-1]
		thirdNote = noteSequence[i]

		# print(firstNote, secondNote, thirdNote)
		first = np.concatenate([notes[firstNote][2:], notes[firstNote][0:2]])
		second = np.concatenate([notes[secondNote][1:], notes[secondNote][0:1]])
		third = notes[thirdNote]

		multiplyResult = np.multiply( np.multiply(first, second), third)

		songVector += multiplyResult

	return np.where(songVector >= 1, 1, -1)

def findTheme(noteSequence, notes, songs, transpose=False):
	''' noteSequence is a string '''

	if transpose:
		pass
		# do something...

	# noteSequence = noteSequence[::-1]
	noteSequence = noteSequence.split(" ")
	noteSequence = list(filter(None, noteSequence))
	n = len(noteSequence)

	songQuery = np.zeros(10000)

	# how many notes in sequence
	if n == 1:
		songQuery = notes[noteSequence[0]]
	if n == 2:
		firstNote = noteSequence[i-2]
		secondNote = noteSequence[i-1]

		first = np.concatenate([notes[firstNote][2:], notes[firstNote][0:2]])
		second = np.concatenate([notes[secondNote][1:], notes[secondNote][0:1]])

		songQuery = np.multiply(first, second)
	
	# if three notes or longer
	else:
		# print("this executed")
		for i in range(2, n):
			# print(i, "time!")
			firstNote = noteSequence[i-2]
			secondNote = noteSequence[i-1]
			thirdNote = noteSequence[i]

			# print(firstNote, secondNote, thirdNote)

			# print(firstNote, secondNote, thirdNote)
			first = np.concatenate([notes[firstNote][2:], notes[firstNote][0:2]])
			second = np.concatenate([notes[secondNote][1:], notes[secondNote][0:1]])
			third = notes[thirdNote]

			multiplyResult = np.multiply( np.multiply(first, second), third)

			songQuery += multiplyResult

	compareSongs = songs.copy()

	for song in songs:
		compareSongs[song] = np.dot(songs[song], songQuery)

	# print("MARY LAMB IS", compareSongs["MaryLamb"])
	# print(compareSongs)
	songResults = []
	for i in range(10):
		song = max(compareSongs, key=compareSongs.get)
		# print(song, compareSongs[song])

		compareSongs.pop(song)
		songResults.append(song)

	return songResults

if __name__ == "__main__":
	notes = createSeedVector()

	songs = {}
	print("Loading themes...")
	with open('data/themesOG.csv') as csvDataFile:
		csvReader = csv.reader(csvDataFile)

		for count, theme in enumerate(csvReader):
			if count != 0:
				# print(theme[0])
				if theme[0] in songs:
					newSongVector = np.zeros(10000)
					songs[theme[0] + " theme" + theme[1]] = songVector(theme[3], notes, newSongVector)
				else:
					newSongVector = np.zeros(10000)
					songs[theme[0]] = songVector(theme[3], notes, newSongVector)
			# print(theme)

	# print("----------------------------------------------")
	print("Done loading themes!")
	print("----------------------------------------------\n\n\n")
	print("Enter X to exit")
	print("Enter T to enable transpose mode")
	print("To search, enter note names in caps separated by spaces.")
	print("e.g. A B C# D Db D")
	print("\n\n\n----------------------------------------------")

	keepRolling = True
	transpose = False

	while keepRolling:
		if transpose:
			print("Transpose mode: On.")
		else:
			print("Transpose mode: Off.")

		noteSequence = input("Please enter a note sequence to look up: \n")
		if noteSequence == "X" or noteSequence == "x":
			exit()
		if noteSequence == "T" or noteSequence == "t":
			transpose = not(transpose)
		else:
			themes = findTheme(noteSequence, notes, songs, transpose)
			for count, theme in enumerate(themes):
				print(count+1, theme)
		
		print("\n")