f = open("coco-labels.txt", "r")
# print(f.readlines())

i = 0
coco_dict = dict()
for cococlass in f.readlines():
    # print(type(cococlass[:-1]))
    items = f"{cococlass[:-1]}"
    
    coco_dict[f"{i}"] = items
    
    i += 1
    
print(type(cococlass[-1]))
# print(f"{cococlass[:-1]}".encode())
print(coco_dict['0'])

import json

filename = "coco-labels.json"
# json.dump(coco_dict, open(filename, "wb"))
# print(json.load(open(filename)))

# with open(filename, 'w') as fp:
#     json.dump(coco_dict, fp)
    
print(json.load(open(filename)))