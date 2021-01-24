import Orange
import os
# importing images
from orangecontrib.imageanalytics.import_images import ImportImages

import time
#import adminupload
import pymongo
import featurestodb

t0= time.clock()
db = featurestodb.db

import_images = ImportImages()

embeddings1 = []
embeddings2 = []
embeddings3 = []
import_images = ImportImages()
path = os.getcwd() + "\\..\\..\\uploaded"
data, err = import_images(path)    

#print(data)

# defining image path to pass to embedding
print(len(data))
image_file_paths = [None] * len(data)
for i in range(len(data)):
    image_file_paths[i] = path + "\\" +  str(data[i,'image'])

# extracting features from images (embedding)
from orangecontrib.imageanalytics.image_embedder import ImageEmbedder
with ImageEmbedder(model='inception-v3') as emb:
	embeddings1 = emb(image_file_paths)

with ImageEmbedder(model='vgg16') as emb:
	embeddings2 = emb(image_file_paths)

with ImageEmbedder(model='vgg19') as emb:
	embeddings3 = emb(image_file_paths)



q = {}
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[db]
mycol = mydb["fs.files"]


i = 0
for y in featurestodb.newfile:
	myquery = {"filename": y}

	newvalues1 = { "$set": { "metadata.Inception-v3": embeddings1[0]} }
	mycol.update_one(myquery, newvalues1)

	newvalues2 = { "$set": { "metadata.vgg16Features": embeddings2[0]} }
	mycol.update_one(myquery, newvalues2)

	newvalues3 = { "$set": { "metadata.vgg19Features": embeddings3[0]} }
	mycol.update_one(myquery, newvalues3)

	print('<br>Image ' + str(i) + 'inserted<br>')
	i = i + 1


import os, shutil
import glob

files = glob.glob(path + '/*.png')

for f in files:
    os.remove(f)
    
t1 = time.clock() - t0
print("Time elapsed: ", t1)
print('<br><a href="../Admin Upload/seite1.html"> Add more images </a>')
