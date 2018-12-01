import json

labels={}

def get_attributes(filename):
   with open('labels.json') as js:
       labels_dict=json.load(js)
       return labels_dict[filename]

#	return price,s,f,v,a

def open_file():
	filename="labels_all.txt"
	with open(filename) as f: #first 1000 links
		content = f.readlines()
		content = [x.strip() for x in content]
		for i in range(len(content)):

			rest_name, attr=content[i].split(".txt:")
			if rest_name=="":
				print(content[i])
				print(i)
			attr=attr.split("**")[:-1]
			if attr[0] == '$':
				price=1
			elif attr[0] == '$$ - $$$':
				price =2
			elif attr[0] == '$$$$':
				price=3
			else:
				price="NULL"
			labels[rest_name]={"price": price, "s":attr[1][2:], "f":attr[2][2:], "v":attr[3][2:], "a":attr[4][2:]}
	return labels

def dump_dict_to_json_file(labels):
	with open('labels.json', 'w') as fp:
	    json.dump(labels, fp)

labels=open_file()
dump_dict_to_json_file(labels)
#print(get_attributes('Crackerjack'))
