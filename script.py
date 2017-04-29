from PIL import Image
from random import randint
import glob, os, config, pyradox

pyradox.config.setDefaultGame('EU4')

CULTURES_FILE = 's'
HISTORY_DIR = 's'

if config.CULTURE_DIR == 'default':
    CULTURES_FILE = os.path.join(pyradox.config.getBasedir(),'common','cultures','00_cultures.txt')
else:
    CULTURES_FILE = os.path.join(config.CULTURE_DIR,'00_cultures.txt')

if config.HISTORY_DIR == 'default':
    HISTORY_DIR = os.path.join(pyradox.config.getBasedir(),'history','countries')
else:
    HISTORY_DIR = config.HISTORY_DIR

flags = {}
eyes = {}
eyes['default'] = []
cultures = {}
hist_cult = {}
shw = Image.open(config.SHADOW)

print('Init...')

#Read country history files and save each country's culture
if config.use_culture:
    for infile in glob.glob(os.path.join(HISTORY_DIR, '*.txt')):
        file = pyradox.txt.parseFile(infile)
        hist_cult[os.path.split(infile)[1][:3]] = file['primary_culture']

#Read cultures file and save cultures and culture groups
cult = pyradox.txt.parseFile(CULTURES_FILE)
for cg in cult:
    cultures[cg] = []
    for c in cult[cg]:
        if not (c == 'graphical_culture' or c == 'male_names' or c == 'female_names' or c == 'dynasty_names'):
            cultures[cg].append(c)
            print (cg+'/'+c)

#Check and create eyes directory
if not os.path.isdir(config.EYES_DIR):
    os.mkdir(config.EYES_DIR)
    print("Eyes directory created at %s." % config.EYES_DIR)
else:
    print("Eyes directory found.")

#Check and create flags directory
if not os.path.isdir(config.FLAGS_DIR):
    os.mkdir(config.FLAGS_DIR)
    print("Flags directory created at %s." % config.FLAGS_DIR)
else:
    print("Flags directory found.")

#Check and create output directory
if not os.path.isdir(config.OUTPUT_DIR):
    os.mkdir(config.OUTPUT_DIR)
    print("Output directory created at %s." % config.OUTPUT_DIR)
else:
    print("Output directory found.")

print('Directories OK')

#Open flag files and put them in an array
for infile in glob.glob(os.path.join(config.FLAGS_DIR, '*.tga')):
    print("Loading " + os.path.split(infile)[1])
    flags[os.path.splitext(os.path.split(infile)[1])[0]] = Image.open(infile).convert('RGBA')
    #print(flags[os.path.splitext(os.path.split(infile)[1])[0]].mode)

print('Flags OK')

#Open eye files and put them in the default group
#Check subfolders and put eye files in corresponding groups
for dir in os.listdir(config.EYES_DIR):
    if os.path.isdir(os.path.join(config.EYES_DIR,dir)):
        eyes[dir] = []
        print(dir)
        for infile in glob.glob(os.path.join(config.EYES_DIR, dir, '*.tga')):
            eyes[dir].append(Image.open(infile).convert('RGBA'))
            if dir.islower():
                eyes['default'].append(Image.open(infile).convert('RGBA'))

print('Eyes OK')


#Create new flags
for key in flags:
    print("Creating %s flag." % key)
    #add eyes to image
    i = Image.alpha_composite(flags[key],eyes['default'][randint(0,len(eyes['default'])-1)])
    #add shadow to image
    o = Image.alpha_composite(i,shw)
    print("Saving %s" % os.path.join(config.OUTPUT_DIR, key + ".tga"))
    #save image
    o.save(os.path.join(config.OUTPUT_DIR, key + ".tga"))

    #If culture filter is on check to see if it fits the criteria
    if config.use_culture:
        for filter in config.culture_filters:
            for ct in config.culture_filters[filter]:
                #Ignore rebels
                if key.isupper():
                    #Separate culture and culture groups
                    if ct.islower():
                        #If country's culture if part of a filter
                        try:
                            if hist_cult[key] == ct:
                                r = 0
                                if len(eyes[filter]) > 0:
                                    r = randint(0,len(eyes[filter])-1)
                                i = Image.alpha_composite(flags[key],eyes[filter][r])
                                o = Image.alpha_composite(i,shw)
                                o.save(os.path.join(config.OUTPUT_DIR, key + ".tga"))
                        except Exception as e:
                            pass
                    elif ct.isupper():
                        ct = ct.lower()
                        #Go through all cultures in all groups and check if one matches country's culture
                        for cg in cultures:
                            if cg == ct:
                                for c in cultures[ct]:
                                    try:
                                        if hist_cult[key] == c:
                                            r = 0
                                            if len(eyes[filter]) > 0:
                                                r = randint(0,len(eyes[filter])-1)
                                            i = Image.alpha_composite(flags[key],eyes[filter][r])
                                            o = Image.alpha_composite(i,shw)
                                            o.save(os.path.join(config.OUTPUT_DIR, key + ".tga"))
                                    except Exception as e:
                                        pass

    #If tag filter is on check to see if it fits the criteria
    if config.use_tags:
        for filter in config.tag_filters:
            for tag in config.tag_filters[filter]:
                if key == tag:
                    r = 0
                    if len(eyes[filter]) > 0:
                        r = randint(0,len(eyes[filter])-1)
                    i = Image.alpha_composite(flags[key],eyes[filter][r])
                    o = Image.alpha_composite(i,shw)
                    o.save(os.path.join(config.OUTPUT_DIR, key + ".tga"))
