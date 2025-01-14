# Population Growth Simulator
##### Work in Progress

In this short Python project, I'm making use of the OOP paradigm. Utilising classes, attributes, and methods for a simple simulation showing various changes over time determined by the following factors:

### Age
An attribute of the `Person` class, assigned to each new `Person` object is an important factor in relation to our population. Some relations age has to some changes over time include:
1. All people age >=8 works in the fields to produce food. Both genders.
2. Some percentage of women in fertility age range give birth per year.
3. Those age 80 or over have higher probability of dying


### Infant Mortality
This variable is not assigned to any objects, but is a value that can change over time due to the probability found in statistics. Some 

---
### Fertility
The variables `fertilityX` and `fertilityY` are the ages at which a woman can become pregnant, the two values are the age range, e.g. 18-35. To grow the population, there must be a reproduce function. Here, 1 in 5 women will become
pregnant each year. This figure is not necessarily representative of the actual numbers but it will work for this simulation. 
```python
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
```
The reproduce function cycles through every person in the peopleDictionary and if said person is female and between the ages of 18 and 35, they have a 20% chance of giving birth and a new person of age 0 is appended to the peopleDictionary (a child is born and added to the population).

---
### Agriculture
Refers to the unit of food a single person produces per year. 1 unit of food will feed 1 person for 1 year. In this simulation, one person must eat 1 unit of food every year, otherwise they will die. Ultimately, if agriculture !>=1, population will not grow because there is not enough units of food for each person. Population will decrease due to starvation.
```python
# 5 here means, one person produces enough for themselves and 4 others per year.
agriculture = 5
``` 
Every year, there is a "harvest".
```python
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
```
This function takes food and agriculture levels as input, calculates how many harvesters are producing food. We multiply the amount of `harvesters` by `agriculture` to get total `food` produced for the year.

---
### Disasters
A variable `disasterChance` considers the possibility of a disaster occuring from one year to the next, potentially destroying the population. In the case of a disaster occurring, the population may be reduced by 5-10%. You can see the `disasterChance` variable used in this `runYear` function:
```python
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
```
The `if` statement takes the `random.randint` between 0 and 100, then checks it
against the `disasterChance` value (in this case, `10`). If this 
`random.randint` is less than the `disasterChance` value, disaster occurs.
The `uniform(0.05, 0.2)` is generating a random float value to figure out how much
damage will be done. It'll fall between 5-20% once multiplying the value by the length of the peopleDictionary to giving us the chosen percentage slice of the population. Then, we simply remove this slice from the population (essentially, 5-20% of the population die)

---
Check out this article on medium for where I found the idea for this project:
https://towardsdatascience.com/building-simulations-in-python-a-complete-walkthrough-3965b2d3ede0

---
#### Further Improvements:
- randomization of death