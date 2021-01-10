import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes":10,"name":"cutie","views":10000},
		{"likes":20,"name":"Joe","views":20000},
		{"likes":30,"name":"joey","views":40000},
		{"likes":40,"name":"Bredon","views":5550}]


for i in range(len(data)):
	response = requests.put(BASE + "video/"+str(i) ,data[i])
	print(response.json()) 
	
#input()
response = requests.delete(BASE + "video/2")
print(response.json())
#input()
'''for i in range(len(data)):
	response = requests.get(BASE + "video/" +str(i), data[i])
	print(response.json())'''
#response = requests.patch(BASE + "video/3", {'views':300,'likes':400})
#print(response.json())

response = requests.get(BASE + "video/3")
print(response.json())

