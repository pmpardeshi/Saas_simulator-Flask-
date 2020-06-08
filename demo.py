import os


file_list={}
total_size=0
start_path='ss'
posts=os.listdir('ss')

# for post in posts:
# 	files[i]= post

enctype="multipart/formdata"
# 	i=i+1

for path,dirs,files in os.walk(start_path):
	for f in files:
		fp=os.path.join(path,f)
		size=os.path.getsize(fp)/1000000
		total_size+=size
		file_list[i]=[f,size]
		i+=1

for sr,detail in file_list.items():
	print(sr, detail[0], detail[1])

print(f" total size of dir = {total_size} MB")
print(f" dict = {file_list} ")
