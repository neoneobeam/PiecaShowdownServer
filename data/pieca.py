# code that makes porting the mons from our spreadsheets to showdown
# ez (code refrenced from w3schools, and geeksforgeeks)


# RIGHT NOW, this ONLY writes to the TESTpokedex.ts, TESTlearnsets.ts, and TESTformats-data.ts. I'd recommend making a backup of the actual files b4 copying and pasting the contents of these into those new ones/adding to them/whatevah. Also since it only writes to them, stuff like the sprites are still not set yet, you have to use the build tools in the client side still, and also they don't write ALL the info (abilities, weights, learnsets, and misc deets like colors, height, etc. are not included rn). The other thing is you do need the coresponding files downloaded and in the same file/directory as this one ** ALSO ALSO rn just appending to these files so you do have to delete the contents/the files b4 getting new values, and remove the test files from the data folder when copying over (client tries to read those and it messes with some stuff, might b a way for us to *just* use the test ones if we want, but doing it this way for now cuz dats what I know)

# TODO clean up some bugs with build tools 
# CHECK ~ pokedex.ts: doesn't like parenthesis names (do a quick replace for now, but might just cut them)
# CHECK ~ pokedex.ts: not specified in the build, but thinking about having something to catch the extra names getting read (like the "_ _ Dex" ones fosho, looks like 5 in total)
# CHECK ~ learnsets.ts: seemingly one double comma after a work up line
# CHECK B/C THESE OTEHRS, BUT HAVEN'T INVESTIGATED MUCH~ formats-data.ts: some } apparently (prob fixed with the other issues tho)

import csv
import pandas as pd



# attempting to code with csv:


# this stores the list of non mon names that may show up in the mon column (just a formatting thing that makes the spreadsheet easier to read for us relative to this parser helper filer thing)
listOfNonNames = ['Water','Ice','TYPE:','\n','Fire','Grass','Electric','Dark','Ground','Rock','Flying','Dragon','Farie','Steel','Poison','Bug','Normal','Fighting','Fairy','Ghost','Psychic','']


# these keep track of the mons names (to make sure when we open the files that they can be compared between them)
MonsNamesFromMoves = []
MonsNamesFromDex = []

# these are the final strings that determine the end of the files we write to (starting with the headers)
global writeToFormats
writeToFormats = "" #"export const FormatsData: import('../sim/dex-species').SpeciesFormatsDataTable = {\n"
global writeToDex
writeToDex = "" #"export const Pokedex: import('../sim/dex-species').SpeciesDataTable = {\n"
global writeToLearn 
writeToLearn = "" #"export const Learnsets: import('../sim/dex-species').LearnsetDataTable = {\n"



# ~~~ end of var defs, start of main code below:




# first we get a quick list of the abilities (using this one from the pieca data sheet so we can l8r add custom ones, but for now, this is just checking for old abilities). There are also 2 files for this (specifiying if the abils are signature or not)

# this stores the list of abilities that (currently) are old
listOfAbilities = []
with open("Pieca Region Data Sheet [Project Vista] - Ability Dex.csv","r") as f:
	abilityListOne = csv.DictReader(f)
	
	for row in abilityListOne:
	# if the ability is an old one, then it gets added to this array to cross refrence with (again skipping new abilities for now). This array will then be used below to find the abilities when making the entries for the mons
		if row['Status'] == 'Old':
			listOfAbilities.append(row['Ability'])
			
# same idea as above, but with the signature abilities csv
with open("Pieca Region Data Sheet [Project Vista] - Signature Abilities Dex.csv","r") as f:
	abilityListTwo = csv.DictReader(f)
	
	for row in abilityListTwo:
		if row['Status'] == 'Old':
			listOfAbilities.append(row['Ability'])


# same same idea as above, but with the moves
listOfMoves = []
stringOfMoves = ""
#with open("Pieca Region Data Sheet [Project Vista] - Move Dex.csv","r") as f:
# ^ keeping this here for when we add custom moves, but using the showdown one by default for those (ig we'd prob open the csv, and then write to text/moves.ts and moves.ts, but yeah)
with open("text/moves.ts","r") as f:
	#movesListOne = csv.DictReader(f)
	
	# the way how this list is formatted is the internal name is after the line that is labeled 'name' so we grab that first and then go back to get the internal one
	movesTSLines = f.readlines()
	for i in range(len(movesTSLines)):
		if movesTSLines[i].find('name') != -1:
			editedMoveName = movesTSLines[i - 1].lower().replace(" ","").replace(":","").replace("{","").replace('"','').replace("\t","").replace("\n","")
			# after editing the name (removing anything that makes it harder to parse later). We save it to an array and string (for different comparisons)
			listOfMoves.append(editedMoveName)	
			stringOfMoves += editedMoveName

	


# ~~~~ read move spreadsheet


# this list is used to compare the mons in the info csv to the learnsets one so we can match the learnset names with the dex indexs (omg I just realized that's why its call a ... a pokedex)

piecaDexNames = ""
MonNamesFromDex = []

# we read the moves first as not every mon has a moveset

# similar vars set as above
piecaDexNamesMoves = ""
MonsNamesFromMoves = []
# idk why this was ingorning my global definition lol so just gonna make the func return these
writeToLearn = ""
with open("Pieca Region Data Sheet [Project Vista] - Pokemon Learnsets (TBR).csv","r") as f:
	movesData = csv.DictReader(f)
	dexCountMoves = 20000
	for row in movesData:
	# similar ideas as above, but the csvs are categorized in a few different areas (namely learned by level, tm, and by mentor). These aren't specified rn, and was just trying to get the movesets in for now (similarly to above, headbutt and metronome are defaults in case the mon don't have the moves filled out yet =D (and they can be ... """""viable"""""))
	
	# first we get the name of the mon (similar to above, but w/ different vars as this file is formatted a bit differently)
		skipForFormatting = False
		for notAMonsName in listOfNonNames:
			if row['Pokemon'] == notAMonsName:
				skipForFormatting = True
		
		if skipForFormatting == False:
			dexCountMoves += 1
			nameString = "pieca"
			
			nameString += row['Pokemon'].replace('[','')
			nameString = nameString.replace(']','')
			nameString = nameString.replace(' ','')
			nameString = nameString.replace('(','')
			nameString = nameString.replace(')','')
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
				
			# saves the name of the mon to be compared to for l8r (as in when we check learnsets with a different file below
			piecaDexNamesMoves += nameString + '\n'	
			#if row['Pokemon'] == 'Phausque':
				#print(nameString)
			MonsNamesFromMoves.append(nameString)
			

			
		
		# ALSO ALSO a backup would not hurt with the pokemon-showdown part
		# could maybe be a bit more optimized with the new moves added in, but for now, we basically run a for to see if the move of a mon is in the list of moves
			showDownLearnset = []
		
			# else statements are used so there are no duplicates
			if row['Pokemon'] == 'Phausque':
				# TODO def a small bug here where if a move shares part of the name of one it will add it (see Phausque with the move 'Hexenring', as with this code below it still gets the move 'Hex' (more of a matter of using find on a string of the moves and iterating through the learnsets instead of the other way around, but not fixin this part to test other stuff rn) 
				#print(listOfMoves)
				for i in listOfMoves:
					if str(row['Move']).lower() == i:
						#print(i + " Move")
						showDownLearnset.append(i)
					else:
						if str(row['TM']).lower().replace(" ","").find(i) != -1:
						#	print(i + " TM")
							showDownLearnset.append(i)
						else:
							if str(row['Mentor']).lower().replace(" ","").find(i) != -1:
						#		print(i + " Mentor")
								showDownLearnset.append(i)
		
		# next part is the formatting of the string now that we have a list of the moves (this is an example of the formatting)
		#'	' + nameString + ': {\n		learnset: {\n			headbutt: ["9M"],\n			metronome: ["9M"],\n		},\n	},\n'
			# keeping this comment for testing:
			
			#if row['Pokemon'] == 'Phausque':
			#	print(" after parse " + str(showDownLearnset) + " len " + str(len(showDownLearnset)))
			#	print(" pre parse " + str(row['TM'].split(",")) + " len " + str(len(row['TM'].split(","))))
			
			
			# starts the string
			learnString = '	' + nameString + ': {\n		learnset: {'
			# iterates thru the mon's moves
			for i in range(len(showDownLearnset)):
				# idk if it needs to be lowercase but the examples they have do that so we are too
				
				# ` note to self w/ this, unsure about dashes n spaces for now so if u need to change those edit the string prob around here ish
				learnString += '\n			' + showDownLearnset[i].lower() + ': ["9M"]'
				if i < len(showDownLearnset) - 1:
					learnString += ','
			# ends the string
			learnString += ',\n		},\n	},\n'
		# end of for row in read
		writeToLearn += learnString
# end of move file read



# ~~~~~ read dex spreadsheet



# keeps track of the dex pos (starting here to be out of the way of other mons (if we want))
dexCount = 20000
# this is a bonus for keeping track of the different pokemon with the same name (???)
huh = 0
# alt version of keeping track of the names (string instead of an array for different checks, I was just trying this, but the array is prob better)
piecaDexNames = ""

with open("Pieca Region Data Sheet [Project Vista] - General Pokemon Info.csv","r") as f:
	data = csv.DictReader(f)
	

	for row in data:
			# when reading the file we format the 3 strings (each string gets appended to
			# formats-data.ts, pokedex.ts, and leansets.ts respectively):
			formatsString = ""
			dexString = ""
			learnString = ""
			nameString = ""
			# starts with the pokemon's name
			skipForFormatting = False
			for notAMonsName in listOfNonNames:
				if row['Pokémon'] == notAMonsName or row['Primary Type'].find('Dex') != -1:
					skipForFormatting = True
			
			if skipForFormatting == False:			
				# increase the dex count
				dexCount += 1
				
					# this reformats the name (just calling the name as is includes a lotta extra spaces, and also I don't think showdown likes the '[' ']''s (since its looking for java script stuff (we can play around with this, I *think* display names can use brackets, but not the species names in the code). Also needed to remove newlines (namely in megas' names). Also needed to remove dashes, and etc. etc. *The biggest edge case rn is that there are multiple mons named '???' so for now each name includes another QMark based on the dex so they can be told apart (their names confused the complier)
						# adding this to the name as any repeat mons (like sabeleye) that are already in showdown have the name and it messes with the code (also makes searching for them a bit easier)
				nameString = "pieca"
				
				nameString += row['Pokémon'].replace('[','')
				nameString = nameString.replace(']','')
				nameString = nameString.replace(' ','')	
				nameString = nameString.replace('(','')
				nameString = nameString.replace(')','')
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
				

				# saves the name of the mon to be compared to for l8r (as in when we check learnsets with a different file below
				piecaDexNames += nameString + '\n'			
				MonsNamesFromDex.append(nameString)
				
					# formats string is the easiest one and is just little cup since I needed to pick something not mainstream lol, all mons still work in customs anyways. If we wanna add a new format (or a few) it would be here
				formatsString = '	' + nameString + ': {\n		tier: "LC",\n	},\n'
				#print(formatsString)
				
					# dex string just starts with the name. We do need the dex number which I am just adding onto 20000. Ya know, just in case! (for now alternate forms have their own dex slots, I think that the main showdown code in the client has special rules for alternate forms so we will prob have to edit that, but doing it l8r)

				dexString = nameString + ':{num:' + str(dexCount) + ',name:"' + nameString + '",' #'	' + nameString + ': {\n 		num: ' + str(dexCount) + ',\n 		name: "' + nameString + '",\n'
					# ^ kinda b/c the extra forms thing the names are spaced out really long, am down to change that but just set it up like that for demoing


					# the learnset file is the last one to have the name. Rn this part just gives every mon headbutt and metronome (so they can ball), but the plan is to open up the other moveset file and add the movesets to the respective string (thinking about appending each learnset string to a list and using 'find' to know which mon to add moves to ALSO for demo def need to skip over custom moves/abilities)
			# Not every mon is in the learnset spreadsheet, so the ones that aren't get a default learnset 
			learnSetFound = False
			for i in MonsNamesFromMoves:
				if nameString == i:
					learnSetFound = True
			if learnSetFound == False:
				#print("not in moves " + nameString)
				learnString = '	' + nameString + ': {\n		learnset: {\n			headbutt: ["9M"],\n			metronome: ["9M"],\n		},\n	},\n'
				# ^ for adding moves in the future, make sure the formatting is like this. The '["9M"]' represents the gen/condition for the move being added (but since we are just using customs for the ruleset gen 9 is fine, i forgort what the M stands for but its like if it learns the move from evo or tm or smthn)
			
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
			
			# if the mon's ability is in the list of abilities, then it gets added to the string (otherwise default is simple)
			abilityExists = -1
			monsAbilities = []
			for i in listOfAbilities:
				# if we find the ability, set the abilityexists part to not be 0 (so as
				# to not add simple twice potentially). Also add the name of the ability to the list of abilities for this specific mon
				if row['Abilities'].find(i) != -1:
					abilityExists += 1
					monsAbilities.append(i)

			# adds simple as a default ability
			if abilityExists == -1:
				monsAbilities = ["Simple"]
			
			# then we set the string with the abilities that gets added to all dah files n stuff n yea
			abilityString = 'abilities:{'
			for i in range(len(monsAbilities)):
				addingAbilityString = '"' + str(i) + '":"' + monsAbilities[i] + '"'
				# if this isn't the last ability in the list, add a comma to the end of the string
				if i < len(monsAbilities) - 1:
					addingAbilityString += ","
				abilityString += addingAbilityString
			# closes off the ability segment with a }
			abilityString += "}"
				
			# finishes this stats string
			dexString += abilityString + ',heightm:0.6,weightkg:24,tier:"Illegal",doublesTier:"Illegal",gen:9},\n'
			# leaving this comment as a refrence since TODO add weights for moves effected by those and tiers n stuff (idk if height/specifying hidden abilities is as necessary for pvp, but this is where these stats would be added)
			#dexString += 'abilities:{"0":"Shell Armor",H:"Iron Barbs"},heightm:0.6,weightkg:24,tier:"Illegal",doublesTier:"Illegal",gen:9},\n'
			
			#print(dexString)
			
			
			# after each of the strings have been written to for the mon, we append them to the ones that actually get written into the files
			if skipForFormatting == False:
				writeToFormats += formatsString
				writeToDex += dexString
			
			# we only change/add the learnstring to this default one if the mon doesn't have a moveset rn (this does mean that the learnset file is technically out of order *at least until every mon has a moveset*, but if u are reading this comment then that part doesn't matter lol)
			if learnSetFound == False:
				writeToLearn += learnString


# ~~~~~end of read dex function/for loop/with open




# when the files are completely read thru, then we put the strings into a new file of they own (after adding the closing parts of the file)

#writeToFormats += '};'
#writeToDex += '};'
#writeToLearn += '};'

#fileFormats = open("TESTMonNamesFromMoves.txt","a")
#fileFormats.write(piecaDexNamesMoves)
#fileFormats.close()

#fileFormats = open("TESTMonNamesFromDex.txt","a")
#fileFormats.write(piecaDexNames)
#fileFormats.close()




# almost actual file writes happen below (technically these get copied n pasted into the 
# then main files, for now, but down to make it more automatic, just did this while figuring out which files to actually edit)

fileFormats = open("TESTV2formats-data.txt","a")
fileFormats.write(writeToFormats)
fileFormats.close()

fileDex = open("TESTV2pokedex.txt","a")
fileDex.write(writeToDex)
fileDex.close()

# ` double check learnests a bit (mentioned in other check point being usnusre about exact syntax for the moves tho. also def at least one extra entry in the dex (at the top LOL, might hard code that one out, unsure if there are more (suspect about entries that are other special spacing characters rn)) (Should be good with this, but leaving it in until I finish testing)
fileLearn = open("TESTV2learnsets.txt","a")
fileLearn.write(writeToLearn)
fileLearn.close()

# yay!
