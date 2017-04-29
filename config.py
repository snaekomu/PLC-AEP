#Directories for eyes, flags and output. If not found they will be created.
EYES_DIR = 'eyes'
FLAGS_DIR = 'flags'
OUTPUT_DIR = 'output'
SHADOW = 'shadow.tga'

CULTURE_DIR = 'default'
HISTORY_DIR = 'default'

#Culture filters
#Uppercase directories won't be added to default pool
use_culture = False
culture_filters = {
    #'directory name' : ['culture_1','culture_2', 'CULTURE_GROUP'],
    'EASTERN' : ['EAST_ASIAN','JAPANESE_G', 'korean', 'ESKALEUT']
}

#Tag filters
#Uppercase directories won't be added to default pool
use_tags = True
tag_filters = {
    #'directory name' : ['tag-1','tag-2'],
    #'angry' : ['PRU']
    'FIRE_WEST' : ['FRA', 'BYZ'],
    'FIRE_EAST' : ['RYU'],
    'angry' : ['YUA']
}
