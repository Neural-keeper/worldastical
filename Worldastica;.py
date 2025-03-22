# Worldastical

# A few useful functions for repetitive tasks below

def input_seq(liste, list_object, keyword = 'stop'):
    while list_object.lower() != keyword:
        liste.append(list_object)
        list_object = input("Next: ")
    else:
        print("Exiting input sequence...")

# data collected - dictionary

data= {'Name': '', 'Inspiration': '', 'Geology': '', 'Political Geography': '', 'Symbolism': '', \
       'Religion': '', 'Politics':'', 'History':'', 'Zoology and Botany':'', 'exit':''}

print(data)

##- Name
name = input('What is the name of the world? Put something in as a placeholder,\
we\'ll come back to this. ')

data['Name'] = name

##- Inspiration
inspo = input("Think about your story. Now think about the vibes of the world \
you're trying to create. Do you know what your real-world inspiration for your \
fantasy is? (If 'yes', enter the inspiration. Else, enter 'no')")

if inspo.lower() == 'no':
    time = input("Start with time period: what time period is it closest to? \
(Include three options: past, present, future)")
    while time.lower() not in ('past', 'present', 'future'):
        print('Sorry, that isn\'t an option. Try again.')
        time = input('Think of a time period: ')
    if time.lower() == 'past':
        inspo = input("Think about historical fiction. Is this similar to Regency \
Era England, Ancient China, or America admist the World War? Try to find a \
time period and place that matches the vibe of your story. What is the best match? ")
        data['Inspiration'] = inspo
    elif time.lower() == 'present':
        inspo = input("What present country has a similar vibe and tone for your \
story? Is it a democracy or is it like North Korea, trapping its inhabitants? This is a \
great time to research countries if you're not sure. ")
        data['Inspiration'] = inspo
    elif time.lower() == 'future':
        inspo = input("A world of the future is hard to relate to the modern, real-life, \
world. That doesn't mean its impossible, though. What country do you expect, \
several years in the future, to look the most like your world? Or, if you're feeling \
even more adventerous, what planets are included in your world (enter as a comma \
separated list)? ")
        inspi = []
        inspi.append('Planets:')
        inspi.append(inspo)
        data['Inspiration'] = inspi
else:
    data['Inspiration'] = inspo
    
##- Geology

print("The best way to do this part is to visualize. \
I'm not sure if you're a traditional paper person or a web person so I'll tell you how \
to do both. On paper, pour some rice and draw along the greater outlines. Online, \
go to [this website](https://azgaar.github.io/Fantasy-Map-Generator/). Don't pay \
too much attention to the map yet, we're just here for a random outline. ")

print("Now, think about the main features you want the part of the world your \
story takes place to have. If this story spans over the entire world, what diverse \
features do you want to include? Snowy mountains and parched deserts? What \
else? ")

scale = input("First and foremost, decide the scope of your world: small or large? \
(Keep your story in mind) ")

print("Great, now think about some really cool scenes you want in your story. \
Where do they take place? At the edge of a dangerously tall cliff? On the docks \
of a harbor? Out in the open sea, up in the sky, what are some cool stages and \
locations? It's tempting to want to think about every aspect of the world, but \
we're not gods.")

places = []

place = input("(type 'stop' to end the input sequence) ")

while place.lower() != 'stop':
    places.append(place)
    place = input("Next place? ")
else:
    print('Exiting input sequence...')

geology = [['Scale:', scale], ['Places:', places]]

data['Geology'] = geology  

##- Political Geography

countries = []

country = input("There are no doubt governing systems in your world. For the \
sake of convenience, we'll refer to them as 'countries' in this app. How many \
countries are in your world? What are their defining features? Enter in the form of \
country : features. \
Use a known language (or perhaps you've created your own) to generate country \
names based on the inspiration you picked earlier. Type 'stop' when completed.")

while country.lower() != 'stop':
    countries.append(country)
    country = input("Next Country: ")
else:
    print("Exiting input sequence...")

separators = []

separator = input("How are these countries separated? By mountain ranges, rivers, \
walls of fire, millions of miles of empty space, or just politically drawn imaginary \
lines? Keeping these ideas in mind, enter the relations in the form of \
country 1 - country 2 : border feature(s). Type 'stop' when completed. ")

input_seq(separators, separator)

data['Political Geography'] = [['Countries:', countries],['Borders:', separators]]

##- Symbolism

symbols = []

symbol = input("Use your inspiration to see how this works in real life. What are \
important things to each country? Think about the USA with its bald eagles and \
flag elements. Enter these potential elements in the form of Country : element 1, \
element 2, etc. Type 'stop' to exit sequence. ")

input_seq(symbols, symbol)

data['Symbolism'] = symbols

##- Religion

print("Religion is an important drive of humankind. You might not want to think \
about this, but the belief systems of people makes the world seem more real, even \
if you don't intend to address it directly in your book. What are important things for \
your people? What are values that different peoples debate against? What force \
keeps people on the morally right path? Is there one God, multiple Gods, or just \
the fear of the unknown? Write a couple sentences answering these questions so \
that you can refer to this later:")

data['Religion'] = input('')

##- Politics

print("Politics is inescapable, both in reality and fantasy. Again, this is a major plot \
progressor. Politics defines the world, its people, and their differences. Think about \
the main country your story will take place in. What are the political issues at play? \
What is the power system? If multiple countries are involved, what are the striking \
differences? Which countries' leaders strive for power and wish to conquer? Which \
leaders are trying to progress science and economy, which are trying to progress \
the arts? In short, what is the political state of your world? Is it embroiled in world \
wars, is it a peaceful time with slight economic tensions? Try to make a mindmap \
elsewhere connecting each country and its leaders.")

relations = []

relation = input("Here, though, just write a few sentences for each country in the \
form of country - allies - enemies - leaders - goals: ")

input_seq(relations, relation)

data['Politics'] = relations

##- History
print("What are some events that define the world? Maybe creation myths, maybe \
a war hundreds of years ago that still leaves its impression on the people.")

events = []

event = input("Type each event and hit enter. Type 'stop' to exit")

input_seq(events, event)

data['History'] = events

##- Zoology and Botany
print("What are some creatures that prowl the world? What about plants? Are \
there magical herbs, poisons, spirits, or demons? This is best to write on your own, \
so enter a link to the final version of your mini-encyclopedia here.")

data['Zoology and Botany'] = input('Enter link or reference here: ')

##- Quirks
data['Quirk'] = input("Each world has some quirks that make it memorable. \
The Koroks in Zelda, the 'dam' joke in Percy Jackson and the Olympians. What's \
yours? ")

## Closing remarks
print("And there we are. Now, we shall take this information and confer it to a \
file you can save. Pick a name for a file that doesn't already exist on your device. ")

file_name = input('Enter File Name (without extension): ') + '.txt'

with open(file_name, "w") as file:
    file.write(f'Name: {name}\n')
    file.write(f"Inspiration {data['Inspiration']}\n")
    file.write(f'Geology: \n')
    file.write(f'    Scale: {scale}\n')
    file.write(f'    Scenes: \n')
    for place in places:
        file.write(f'       {place}\n')
    file.write('Political Geography\n')
    file.write('    Countries: \n')
    for i in countries:
        file.write(f'       {i}\n')
    file.write('    Borders: \n')
    for i in separators:
        file.write(f'       {i}\n')
    file.write('Symbolism: \n')
    for i in symbols:
        file.write(f'   {i}\n')
    file.write(f"Religion: {data['Religion']}\n")
    file.write('Politics: \n')
    for i in relations:
        file.write(f'   {i}\n')
    file.write(f"Zoology and Botany: Link to reference -{data['Zoology and Botany']}\n")
    file.write(f"Quirk: {data['Quirk']}\n")

print(f'File {file_name} has been created. Search in your files for {file_name}')

print(''' Now, you can retrieve information that you've entered. Your options are
(case -sensitive):
- Name
- Inspiration
- Geology
- Political Geography
- Symbolism
- Religion
- Politics
- History
- Zoology and Botany
- Quirk''')
print('Type "exit" in the below prompt to leave the application:')

retrieve = input('What information do you want to retrieve?')

while retrieve not in data:
    print('Sorry, that isn\'t a valid option.')
    retrieve = input('Try again: ')

while retrieve != "exit":
    print(f'Requested data - \n {data[retrieve]}')
    retrieve = input('What else? ')
else:
    print('Thank you for using the program!')


    






