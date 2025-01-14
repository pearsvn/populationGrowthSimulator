import random
import pandas as pd

class Person:
    def __init__(self, gender, age, socialClass, workRate, medicalCondition, healthFactor):
        self.gender = gender #0 = male, 1 = female
        self.age = age
        self.socialClass = socialClass #0 = empoverished, 5 = ruling class
        self.workRate = workRate #1 = poor workRate, 10 = good workRate
        self.medicalCondition = medicalCondition #0 = no medical condition, 1 = has medical condition
        self.healthFactor = healthFactor #5 is average health, anything less = bad, anything more = good

def harvest(food, agriculture):
    harvesters = 0
    nonHarvesters = 0
    for person in peopleDictionary:
        if person.age >= 8:
            harvesters += 1
        elif person.socialClass>4 or medicalCondition==1:
            nonHarvesters+=1
        elif person.workRate >= 8:
            agriculture+=2
    food += harvesters * agriculture - nonHarvesters

    if food < len(peopleDictionary):
        del peopleDictionary[0:int(len(peopleDictionary)-food)]
        food = 0
    else:
        food -= len(peopleDictionary)
    return food

def reproduce(fertilityX, fertilityY, infantMortality):
    new_people = []
    for person in peopleDictionary:
        if person.gender == 1 and fertilityX <= person.age <= fertilityY:
            if random.randint(0,5)==1 and random.randint(0,100) > infantMortality:
                new_people.append(Person(
                    gender,
                    0,
                    socialClass,
                    workRate,
                    medicalCondition,
                    healthFactor))
    peopleDictionary.extend(new_people)

def random_death_rate(age, healthFactor, food):
    baseDeathRate = 0.01 * (age - 50)  # Older people have a higher base death rate
    healthDeathRate = max(0, healthFactor - 1)  # Poor health increases death probability
    foodDeathRate = max(0, (len(peopleDictionary) - food) / len(peopleDictionary))  # Food scarcity increases death rate
    return baseDeathRate + healthDeathRate + foodDeathRate

def apply_death():
    global peopleDictionary
    for person in peopleDictionary[:]:
        deathRate = random_death_rate(person.age, healthFactor, food)
        if random.random() < deathRate:
            peopleDictionary.remove(person)

def simulateYear():
    global peopleDictionary
    new_people = []
    for person in peopleDictionary:
        person.age+=1
        if person.age > 80:
            peopleDictionary.remove(person)
        elif person.gender == 1 and 18 <= person.age <=45:
            if random.random() < 0.1:
                new_people.append(Person(gender,
                                         0,
                                         socialClass,
                                         workRate,
                                         medicalCondition,
                                         healthFactor))
    peopleDictionary.extend(new_people)

def runYear(food, agriculture, fertilityX, fertilityY, infantMortality, disasterChance):
    food = harvest(food, agriculture)
    reproduce(fertilityX, fertilityY, infantMortality)
    for person in peopleDictionary[:]:
        person.age+=1
        apply_death()
    if random.randint(0, 100) < disasterChance:
        del peopleDictionary[int(random.uniform(0.05,0.2) * len(peopleDictionary))]

    # decreasing infantMortality by 1.5% every year
    infantMortality *= 0.985
    return infantMortality

def beginSim():
    for x in range(startingPopulation):
        peopleDictionary.append(Person(
            gender,
            age,
            socialClass, 
            workRate,
            medicalCondition,
            healthFactor))

startingPopulation = 500
infantMortality = 5
agriculture = 5
disasterChance = 10
food = 0
fertilityX = 18
fertilityY = 35

peopleDictionary = []
gender = random.randint(0,1)
age = random.randint(18, 80)
socialClass = random.randint(0,5)
workRate = random.randint(1,10)
medicalCondition = random.randint(0, 1)
healthFactor = random.randint(1, 10)

beginSim()

#data collection for each year
simulation_data = []

# the below code continues the simulation until the peopleDictionary (population) grows to 1 million.
while len(peopleDictionary) < 1000000 and len(peopleDictionary) > 1:
    # adding infantMortality =, and parse argument to one line below = V2
    infantMortality = runYear(
        food,
        agriculture,
        fertilityX,
        fertilityY,
        infantMortality,
        disasterChance)
    
year_data = {
    "Year": len(simulation_data)+1,
    "Population": len(peopleDictionary),
    "Food": food,
    "Infant Mortality": infantMortality,
    "Agriculture": agriculture
}
simulation_data.append(year_data)

df = pd.DataFrame(simulation_data)
file_path = "population_growth_simulation_results.xlsx"
df.to_excel(file_path, index=False)
print(f"Simulation results saved to {file_path}")