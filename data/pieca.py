# code that makes porting the mons from our spreadsheets to showdown
# ez (code refrenced from w3schools, and geeksforgeeks)


# RIGHT NOW, this ONLY writes to the TESTpokedex.ts, TESTlearnsets.ts, and TESTformats-data.ts. I'd recommend making a backup of the actual files b4 copying and pasting the contents of these into those new ones/adding to them/whatevah. Also since it only writes to them, stuff like the sprites are still not set yet, you have to use the build tools in the client side still, and also they don't write ALL the info (abilities, weights, learnsets, and misc deets like colors, height, etc. are not included rn). The other thing is you do need the coresponding files downloaded and in the same file/directory as this one ** ALSO ALSO rn just appending to these files so you do have to delete the contents/the files b4 getting new values, and remove the test files from the data folder when copying over (client tries to read those and it messes with some stuff, might b a way for us to *just* use the test ones if we want, but doing it this way for now cuz dats what I know)


# ` pausing here, some error is in build tools (I think it might have to do with the og mons missing or teambuildertables.js having something up (try running build tools and investigating the error, but it looks like all of the name cases were taken car of)

import csv
import pandas as pd



# attempting to code with csv:

# keeps track of the dex pos (starting here to be out of the way of other mons (if we want))
dexCount = 20000

# this is a bonus for keeping track of the different pokemon with the same name (???)
huh = 0

# these are the final strings that determine the end of the files we write to (starting with the headers)
writeToFormats = ""#"export const FormatsData: import('../sim/dex-species').SpeciesFormatsDataTable = {\n"
writeToDex = ""#"export const Pokedex: import('../sim/dex-species').SpeciesDataTable = {\n"
writeToLearn = ""#"export const Learnsets: import('../sim/dex-species').LearnsetDataTable = {\n"

with open("Pieca Region Data Sheet [Vista Region] - General Pokemon Info.csv","r") as f:
	data = csv.DictReader(f)
	

	for row in data:
		# when reading the file we format the 3 strings (each string gets appended to
		# formats-data.ts, pokedex.ts, and leansets.ts respectively):
		formatsString = ""
		dexString = ""
		learnString = ""
		# starts with the pokemon's name
		
		# increase the dex count
		dexCount += 1
		
			# this reformats the name (just calling the name as is includes a lotta extra spaces, and also I don't think showdown likes the '[' ']''s (since its looking for java script stuff (we can play around with this, I *think* display names can use brackets, but not the species names in the code). Also needed to remove newlines (namely in megas' names). Also needed to remove dashes, and etc. etc. *The biggest edge case rn is that there are multiple mons named '???' so for now each name includes another QMark based on the dex so they can be told apart (their names confused the complier)
				# adding this to the name as any repeat mons (like sabeleye) that are already in showdown have the name and it messes with the code (also makes searching for them a bit easier)
		nameString = "pieca"
		
		nameString += row['Pokémon'].replace('[','')
		nameString = nameString.replace(']','')
		nameString = nameString.replace(' ','')	
		nameString = nameString.replace('\n','')
		nameString = nameString.replace('-','')	
		nameString = nameString.replace('.','')	
		nameString = nameString.replace('?','qmark')	
		nameString = nameString.replace('!','yay')
		nameString = nameString.replace("'",'d')
		
		# from what I can tell, the vars used for pokemon name indicies cannot be uppercase so making them all lower (again, maybe the names can
		nameString = nameString.lower()
		
		if nameString == 'piecaqmarkqmarkqmark':
			for i in range(huh):
				nameString += 'qmark'
			huh += 1
		

		
		
		
			# formats string is the easiest one and is just little cup since I needed to pick something not mainstream lol, all mons still work in customs anyways. If we wanna add a new format (or a few) it would be here
		formatsString = '	' + nameString + ': {\n		tier: "LC",\n	},\n'
		print(formatsString)
		
			# dex string just starts with the name. We do need the dex number which I am just adding onto 20000. Ya know, just in case! (for now alternate forms have their own dex slots, I think that the main showdown code in the client has special rules for alternate forms so we will prob have to edit that, but doing it l8r)

		dexString = nameString + ':{num:' + str(dexCount) + ',name:"' + nameString + '",' #'	' + nameString + ': {\n 		num: ' + str(dexCount) + ',\n 		name: "' + nameString + '",\n'
			# ^ kinda b/c the extra forms thing the names are spaced out really long, am down to change that but just set it up like that for demoing


			# the learnset file is the last one to have the name. Rn this part just gives every mon headbutt and metronome (so they can ball), but the plan is to open up the other moveset file and add the movesets to the respective string (thinking about appending each learnset string to a list and using 'find' to know which mon to add moves to ALSO for demo def need to skip over custom moves/abilities)
		learnString = '	' + nameString + ': {\n		learnset: {\n			headbutt: ["9M"],\n			metronome: ["9M"],\n		},\n	},\n'
			# ^ for adding moves in the future, make sure the formatting is like this. The '["9M"]' represents the gen/condition for the move being added (but since we are just using customs for the ruleset gen 9 is fine, i forgort what the M stands for but its like if it learns the move from evo or tm or smthn)
		print(learnString)
		
		# then types
		
			# these get appended to the dexstring
			
			# if there is not a secondary type, then we just write the first one (no comma)
		if row['Secondary Type'] == '--':
			dexString +='types:["'+ row['Primary Type'] + '"],'
			
		# otherwise then we add the second type
		else:
			dexString +='types:["'+ row['Primary Type'] + '","' + row['Secondary Type'] + '"],'

		
		
		# then stats
			# p much the same idea as above (in case any of the stats are not filled in per the try statement check, then the mon just has smeargle stats)
		try:	
			int(row['HP'])
			int(row['Attack'])
			int(row['Defense'])
			int(row['Special Attack'])
			int(row['Special Defense'])
			int(row['Speed'])
			dexString += 'baseStats:{hp:' + row['HP'] + ',atk:' + row['Attack'] + ',def:' + row['Defense'] + ',spa:' + row['Special Attack'] + ',spd:' + row['Special Defense'] + ',spe:' + row['Speed'] + '},'
		except:
			dexString += 'baseStats:{hp:55,atk:20,def:35,spa:20,spd:45,spe:75},'
		
			# rest of the stats go here, but adding them in l8r (unsure if all of these are needed for custom mons, but just copied them over from the example with dop/spiny from mario mon)
		dexString += 'abilities:{"0":"Shell Armor",H:"Iron Barbs"},heightm:0.6,weightkg:24,tier:"Illegal",doublesTier:"Illegal",gen:9},\n'
		
		print(dexString)
		# after each of the strings have been written to for the mon, we append them to the ones that actually get written into the files
		writeToFormats += formatsString
		writeToDex += dexString
		writeToLearn += learnString

# when the file is completely read thru, then we put the strings into a new file of they own (after adding the closing parts of the file)

#writeToFormats += '};'
#writeToDex += '};'
#writeToLearn += '};'

fileFormats = open("TESTformats-data.txt","a")
fileFormats.write(writeToFormats)
fileFormats.close()

fileDex = open("TESTpokedex.txt","a")
fileDex.write(writeToDex)
fileDex.close()

fileLearn = open("TESTlearnsets.txt","a")
fileLearn.write(writeToLearn)
fileLearn.close()

# yay!
