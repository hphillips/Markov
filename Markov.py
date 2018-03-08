import sys
import random
import re
from collections import Counter
#This class allows you to map multiple values to the same key and when retrieving a value for a key, 
#     returns one at randon weighted by how many times that value was added
#E.g. if
#add("test","a")
#add("test","b")
#add("test","b")
#Then get("test") has a 1/3 chance of returning "a" and a 2/3 chance of returning "b"
class RandomMap(object):
	
	def __init__(self):
		self.inserts=0
		self.sum=0
		self.retrievals=0
		self.map = {}
		self.word_counts= Counter()

	def options(self,key):
		return len(self.map[key])

	def add(self,key,value):
		self.inserts +=1
		if key not in self.map:
			self.map[key] = Counter()
		self.word_counts[key]+=1		
		value_counts = self.map[key]
		value_counts[value]+=1

	def get(self,key):
		if key not in self.map:
			return None
		else:
			key_map = self.map[key]
			rand=random.randint(1,self.word_counts[key])
			for value in key_map:
				rand -= key_map[value]
				if rand <= 0:
					return value

	def __str__(self):
		return self.map.__str__()

	def diagnose(self):
		keycount=0
		solocount=0
		for key in self.map:
			keycount+=1
			if key.count(' ')>1:
				print(key)
			if self.options(key)==1:
				solocount+=1
		print(solocount,keycount)

#This class ingests text to train a Markov chain and then generates text based on the chain
class Markov(object):

	def __init__(self,**kwargs):
		self.translations = RandomMap()
		self.chains       = RandomMap()
		if "chain_length" in kwargs:
			self.chain_length = kwargs["chain_length"]
		else:
			self.chain_length = "hybrid"

		if "text_type" in kwargs:
			self.text_type = kwargs["text_type"]
		else:
			self.text_type = "normal"

		if "training_set" in kwargs:
			for training_text in training_set:
				self.add(training_text)
	def __str__(self):
		return self.chains.__str__()

	def clean_text(self,text):
		if self.text_type=="nopunc":
			return re.sub(r'[^\w]','',text.lower())
		elif self.text_type=="lower":
			return text.lower()
		else:
			return text

	def add(self,words):
		if len(words)==0:
			return
		clean_start=self.clean_text(words[0])
		self.translations.add(clean_start,words[0])
		self.chains.add("__start__",clean_start)
		
		first_word  = None
		second_word = "__start__"
		following_word   = clean_start
		words.append("__end__")
		for cur_word in words[1:]:
			clean_cur=self.clean_text(cur_word)
			self.translations.add(clean_cur,cur_word)
		
			first_word  = second_word
			second_word = following_word
			following_word = clean_cur
		
			self.chains.add(first_word+" "+second_word,following_word)	
			self.chains.add(second_word,following_word)
		
	def generateText(self,separator):
		first_word  = "__start__"
		second_word = self.chains.get("__start__")
		output = []

		while second_word != "__end__":
			output.append(second_word)
			if self.chain_length=="short" or self.chain_length=="hybrid" and self.chains.options(first_word+" "+second_word)==1:
				next_word = self.chains.get(second_word)
			else:
				next_word = self.chains.get(first_word+" "+second_word)
			first_word  = second_word
			second_word = next_word
		
		ret = ""
		for word in output:
			ret += self.translations.get(word)+separator
		if separator=="":
			return ret
		else:
			return ret[:-len(separator)]

	def diagnose(self):
		self.chains.diagnose()

if __name__=='__main__':
	desired_output_ct=1
	args = sys.argv[1:]
	
	chain_length = "short"
	text_type = "normal"
	in_file = None
	separator=" "
	i=0
	while i < len(args):
		if args[i]=="-n":
			desired_output_ct=int(args[i+1])
			i+=1
		elif args[i]=="-l":
			chain_length=args[i+1].lower()
			i+=1
		elif args[i]=="-t":
			text_type=args[i+1].lower()
			i+=1
		elif args[i]=="-f":
			in_file=args[i+1]
			i+=1
		elif args[i]=="-s":
			separator=args[i+1]
			i+=1
		elif args[i]=="-S":
			separator=""
		i+=1

	input_set = []
	if in_file is not None:
		with open(in_file,'r') as f:
			for line in f.readlines():
				input_set.append(line.strip())
	else:
		for line in sys.stdin:
			input_set.append(line.strip())

	content=[]
	input_ct=0
	for line in input_set:
		if line=="":
			continue
		input_ct+=1
		parts=line.split("__split__")
		for i in range(0,len(parts)):
			if i>=len(content):
				content.append([])
			if separator is None or separator=="":
				content[i].append(list(parts[i].strip()))
			else:
				content[i].append(re.sub(r'\s+',' ',parts[i].strip()).split(" "))
	output=[]
	for training_set in content:
		chain = Markov(chain_length=chain_length,text_type=text_type,training_set=training_set)
		output_addition=[]
		for i in range(0,desired_output_ct):
			generated = chain.generateText(separator)
			while generated in input_set:
				generated=chain.generateText(separator)
			output_addition.append(generated)
		output.append(output_addition)
	for i in range(0,desired_output_ct):
		printed = ''
		for j in output:
			printed+=j[i]+" __split__ "
		print(printed[:-len(" __split__ ")])	
