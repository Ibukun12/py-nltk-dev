import nltk, config
from nltk.tree import Tree

#TODO: 
# 1) go through all sentences & search for missed names from DB!
# 2) Detection relations between found entities - scan text
class NERFinder:
	def __init__(self):
		self.load_names()
		#self.load_cities()
		#self.find(tagged_words, sentences, tagged_sentences)

	def load_names(self):
		with open(config.MALE_NAME_FILE) as fp:
			self.male = {line.strip():True for line in fp}
		with open(config.FEMALE_NAME_FILE) as fp:
			self.female = {line.strip():True for line in fp}
			
	def load_cities(self):
		first = True
		self.countries = {}
		self.cities = {}
		with open(config.CITY_FILE) as fp:
			for line in fp:
				if first: # skip first line 
					first = False 
					continue
				split = line.split(",")
				self.countries[split[0]] = True
				self.cities[split[1]] = True
				print "added:",split
	
	def is_city_or_country(self, name):
		return ((name.lower() in self.cities) or (name.lower() in self.countries))
	
	def name_in_db(self, name):
		lowcase = name.lower()
		lowcase = lowcase[0].upper() + lowcase[1:]
		if lowcase in self.male: return (True, "male")
		if lowcase in self.female: return (True, "female")
		return (False, None)
		
	def find_names(self, tree, peeps):
		if tree.node == "PERSON":
			peeps.append([e[0] for e in tree]) # drop the tag, get only names
		else:
			for ent in tree:
				if type(ent) == Tree:
					self.find_names(ent, peeps)

	def extract_fullnames(self, title_list):
		# join titles to form normal names
		names_list = {}
		for titles in title_list:
			if len(titles) > 3: 
				print "rejected long name title:", titles
				continue # reject names longer than 3 ids 
			name = " ".join(titles)
			names_list[name] = {'sex':'?', 'fullname':name, 'shortnames':[]}
		
		# some formed names are shortened versions(or names w/o surnames) - aggregate
		unique_names = []
		keys = names_list.keys()
		for i, key in enumerate(keys):
			if key not in unique_names: # it might be a good full unique name, check further
				add = True
				for j, test in enumerate(keys):
					if i == j: continue # no self test
					if key in test: # this is a shorter version of full name, skip it
						add = False
						names_list[key]['fullname'] = test
						names_list[test]['shortnames'].append(key)
						break
				if add:
					unique_names.append(key)
		
		for key, value in names_list.items():
			if key != value['fullname']: # delete shortended names leaving full names
				del names_list[key]
			else:
				parts = key.split(" ")
				for p in parts:
					result = self.name_in_db(p) # check if name exists in the database
					if result[0]:
						names_list[key]['sex'] = result[1] # store sex defined by name
						break
				#print key,"=",value
				
		return names_list
		
	def check_names(self, people, sentences, tagged_sentences):
		# check that all names found are valid - not places or smth.
		for fullname, data in people.items():
			name_good = None
			for index, s in enumerate(sentences):
				if not fullname in s: continue # sentence must contain the name
				
				name_part = fullname.split(" ")[0]
				prev_tag = None # previous tag
				prev_prev_tag = None # more previous than previous
				
				for i, (word, tag) in enumerate(tagged_sentences[index]):
					if word == name_part: # found the name
						if prev_tag: 
							# check for IN (which denotes place name instead of person)
							if prev_tag[1] == "IN" and (prev_tag[0] in ("in", "at", "of")):
								name_good = False
								break
							else:
								# the name starts with tags: "the"/"a"
								if prev_tag[1] == "DT" and (prev_tag[0] in ("the", "a")):
									if prev_prev_tag: # check deeper (one more tag back)
										# check for IN (which denotes place name instead of person)
										if prev_prev_tag[1] == "IN" and (prev_prev_tag[0] in ("in", "at", "of")):
											name_good = False
											break
					prev_prev_tag = prev_tag
					prev_tag = (word, tag) #store previous tag for later use
				if name_good != None:
					break
			
			# check if name is not a contry name
			#if self.is_city_or_country(fullname) or name_good == False:
			if name_good == False:
				print "Removing", fullname, "as not a person detected"
				del people[fullname]
	
	def check_extended_names(self, people, sentences, tagged_sentences):
		# check that all names found fully found
		for fullname, data in people.items():			
			for index, s in enumerate(sentences):
				if not fullname in s: continue # sentence must contain the name
				last_name = fullname.split(" ")[-1]
				tag_s = tagged_sentences[index]
				
				complete = False
				for i, (word, tag) in enumerate(tag_s):
					if word != last_name:  continue # we're interested in finding last name
					if len(tag_s) > i+1: # check if next tag starts with hispanic names 
						next_tag = tag_s[i+1]
						if next_tag[1] == "IN" and next_tag[0] in ("de"):
							if len(tag_s) > i+2: # now get the last name attachment
								next_next_tag = tag_s[i+2]
								if next_next_tag[1].startswith("N"):
									del people[fullname]
									new_fullname = fullname + " " + next_tag[0] + " " + next_next_tag[0]
									print "Found a spanish name, old name:", fullname,", new fullname:", new_fullname
									data['shortnames'].append(fullname)
									data['fullname'] = new_fullname
									people[new_fullname] = data
									complete = True
									break
			if complete: break # dont analyze more sentences
			
	def find(self, tagged_words, sentences, tagged_sentences):
		chunked = nltk.chunk.ne_chunk(tagged_words)
		title_list = []
		#print chunked
		self.find_names(chunked, title_list)
		
		people = self.extract_fullnames(title_list)
		self.check_names(people, sentences, tagged_sentences)
		self.check_extended_names(people, sentences, tagged_sentences)
			
		# ok, print the info
		print "People mentioned in article:"
		for i, (fullname, data) in enumerate(people.items()):
			print "\t%d. %s ="%(i+1, fullname), data
		#index = self.find_sentence(fullname, tagged_sentences)
		
		return people