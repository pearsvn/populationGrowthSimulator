
# the main() class is an exponential function too basic of a model to simulate,
# population growth. 

# issues with the below "simulation":
# - the total number of people in an environment won't increase by a set
#  percentage every cycle
# - there are many factors that affect the population that aren't included

# therefore, this main() class is the simplest form of the simulation 
def main ():
    totalPopulation = 50
    growthFactor = 1.00005
    dayCount = 0

    while totalPopulation < 1000000:
        totalPopulation *= growthFactor
        dayCount += 1
        if dayCount == 56:
            dayCount = 0
            print(totalPopulation)

"""a more realistic simulation of the human population will require more factors, such as:
when people are born, reproduce, die
=== Can check out some other factors that contribute to population growth ===
            
the chosen factors for the iteration of the function is:
- starting population
- infant mortality
- food
- fertility x & fertility y
- healthcare 
- agriculture
- chance of disaster
- age of death"""

import random

startingPopulation = 50
infantMortality = 5
"""agriculture = how many units of food each person produces
1 unit of food feed 1 person for 1 year
in this simulation, one person must eat 1 unit of food every year, otherwise they die
so if agriculture = 1, everyone eats. agriculture = 0.5, 50% of the population dies.
agriculture = 1.5, there is excess and can be used as backup incase the next year agriculture
value is not enough to support the population

In Layman's terms, if the agriculture !>= 1, population will not grow, but would starve."""

# 5 here means, one person produces enough for themselves and 4 others.
agriculture = 5

"""disasterChance = the probability every year that a disaster destroys the population
for example, a natural disaster.
it will affect the population by a random percentage, from 5-10% """

# 10 here means, on average, every 10 years a disaster will happen
disasterChance = 10

"""every year a harvest function will run and output of the harvest will be:
population * agriculture.
if you have stocks of food, you COULD maintain the population."""

food = 0

"""fertilityX and fertilityY are the ages at which a woman can become pregnant,
the two values are the age range, e.g. 18-35"""

fertilityX = 18 
fertilityY = 35

"""We need a way for these factors to control our population on a year by year basis.
COULD use mathematical method, but in this case, we will use OOP to simulate each person.

Each person will be an object with a few factors. Each cycle (one year of the simulation),
a person will be affected in some way, e.g their age increasing by 1.
=== could try the mathematical method at a later stage ==="""

# each person stored in this dictionary. Can use a loop to cycle through each person yearly,
# and alter them. 

peopleDictionary = []


# the reason we don't have the age set to 0 is because, the initial group of people shouldn't
# be all 0 years old, but of different ages, to begin with.
# more characteristics could also be added to this person object, e.g. medical condition,
# social class, income, etc.
class Person:
    def __init__(self, age):
        self.gender = random.randint(0,1)
        self.age = age

""" We want the simulation to simulate a population that exponentially increases over time,
like the main() class. However, now we need:
1. All people age>=8 works in the fields to produce food. Both genders.
2. Some number of women in fertility age range give birth per year.
3. age>80 dies."""

def harvest(food, agriculture):
    ablePeople = 0
    for person in peopleDictionary:
        if person.age >= 8:
            ablePeople += 1
    
    food += ablePeople * agriculture

    if food < len(peopleDictionary):
        del peopleDictionary[0:int(len(peopleDictionary)-food)]
        food = 0
    else:
        food -= len(peopleDictionary)

""" Every year, there is a "harvest". This function takes food and agriculture levels.
Calculates how many able people are producing food, by counting people(age>=8).
We multiply number of able people by agriculture to get total food produced for the year."""

""" If the food is not enough, s.t. not 1 unit of food per person, then the dictionary of
people is limited to the amount of food available, and excess die from starvation. This
ensures if there is not enough food to go around, people who can't eat will die, and the
population is limited. However, if there is excess food, each person consumes 1 unit, and
whatever is left is stored for the next year."""


"""to grow the population, there must be a reproduce function. Here, 1 in 5 women will become
pregnant each year. This figure is not necessarily representative of the actual numbers but
it will work for this simulation. The reproduce function cycles through every person in the
peopleDictionary and if said person is female and between the ages of 18 and 35, they have a
20% chance of giving birth and a new person of age 0 is appended to the peopleDictionary."""

""" V2 = Added complexity.
This a comment about the V2 added to this function.
20% of women give birth each year in this simulation, but 25% of those infants die.

Essentially, what the V2 code does is:
1. Random number generated from 0-100
2. Random number < 25% = baby dies
3. Random number > 25% = baby lives.

if infantMortality is high, less infants survive.
This is not very nice, so we strive for decreasing infantMortality with better healthcare over time."""
def reproduce(fertilityX, fertilityY, infantMortality):
    for person in peopleDictionary:
        if person.gender == 1:
            if person.age > fertilityX:
                if person.age < fertilityY:
                    if random.randint(0,5)==1:
                        # one line below = V2
                        if random.randint(0,100) > infantMortality:
                            peopleDictionary.append(Person(0))

""" Here we are starting the simulation with 50 people between the ages of 18 and 50"""
def beginSim():
    for x in range(startingPopulation):
        peopleDictionary.append(Person(random.randint(18, 50)))


""" This class performs the harvest and reproduce functions each year. This function runs
the harvest function to find out if the food will leave people to starve to death or if
there is enough to be stored. We then perform the reproduce function, so 20% of women between
18-35 give birth.

Next, we cycle through the peopleDictionary and remove anyone who is over the age of 80.
The rest of the population's age increase by 1.

=== to improve the simulator, the age of death could be randomised === 

Then we print out the total population using print(len(peopleDictionary))."""

def runYear(food, agriculture, fertilityX, fertilityY, infantMortality, disasterChance):
    harvest(food, agriculture)
    reproduce(fertilityX, fertilityY, infantMortality)
    for person in peopleDictionary:
        if person.age > 80:
            peopleDictionary.remove(person)
        else:
            person.age += 1
    # one line below = V2
    """ The below if statement takes the random number between 0 and 100 and checks it
    against the disasterChance range (in this case, 10% as set above). If this random
    number falls within this range, disaster occurs, otherwise no problemo.
    The uniform(0.05, 0.2) is generating a random number to figure out how much
    damage will be done. It'll fall between 5-20%. We'll multiply this by the length
    of the peopleDictionary to get a 5-20% slice of the population. Then, we simply
    remove this slice FROM the population (essentially, 5-20% of the population die)"""
    if random.randint(0,100)<disasterChance:
        del peopleDictionary[0:int(random.uniform(0.05, 0.2)*len(peopleDictionary))]
    print(len(peopleDictionary))
    
    # one line below = V2, decreasing infantMortality by 1.5% every year
    infantMortality *= 0.985
    return infantMortality

beginSim()
# the below code continues the simulation until the peopleDictionary (population) grows to 100k
while len(peopleDictionary) < 100000 and len(peopleDictionary) > 1:
    # adding infantMortality =, and parse argument to one line below = V2
    infantMortality = runYear(food, agriculture, fertilityX, fertilityY, infantMortality, disasterChance)

""" === can also export to excel using pandas for better data visualisation === """