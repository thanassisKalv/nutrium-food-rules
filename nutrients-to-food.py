import json

'''
*Example output:*
Egg richIn Energy
Egg containsNutrient A
Black_currant lowIn Sugar
Black_currant richIn C
Black_currant containsNutrient B12
'''

with open('rules.json', "rb") as f:
    nutrientRules = json.load(f)

with open('sample-foods.json', "rb") as f:
    inputFoods = json.load(f)

with open('nutrium-food-data.json', "rb") as f:
    nutriumDB = json.load(f)
    
nutDBs = {}
for db in nutriumDB["food_information_sources"]:
    nutDBs[db["id"]] = db["code"]

def calc_rule(rule, foodItem, srchFd):
    
    ruleNutrients = []
    energyKcal = 0.0
    for nutInfo in foodItem["nutrition_informations"]:
        if nutInfo["nutrient_id"] == 5:
            energyKcal = nutInfo["value"]
    for nutrientID in rule["nutrients"]:
        for nutInfo in foodItem["nutrition_informations"]:
            if nutInfo["nutrient_id"] == nutrientID:
                ruleNutrients.append(nutInfo)
    # calculate according to rule's type
    result = 0.0
    if rule["ruleType"] == "calorie_percent":
        for nutInfo in ruleNutrients:
            result = result + nutInfo["value"]*rule["kcal"]
        result = result/energyKcal
    elif rule["ruleType"] == "quant_sum":
        for nutInfo in ruleNutrients:
            result = result + nutInfo["value"]

    if "richIn" in rule.keys():
        if rule["richIn"] < result:
            print(srchFd["name"] + " richIn " + rule["name"])
            return 
    if "containsNutrient" in rule.keys():
        if rule["containsNutrient"] < result:
            print(srchFd["name"] + " containsNutrient " + rule["name"])
            return 
    if "lowIn" in rule.keys():
        if rule["lowIn"] >= result:
            print(srchFd["name"] + " lowIn " + rule["name"])
            return
    #print(srchFd["name"] + " /// " + rule["name"])
            
"""
Firstly, keep the result with the shortest name from "COFID_2015" db if exists 
(e.g. keep "Haddock, flesh only, raw" and not "Haddock, flesh only, smoked, raw")
Only if "COFID_2015" returns nothing, report result from other DBs
"""
for srchFd in inputFoods["foods"]:
    otherDBs = []
    cofidDB = {}
    foundIn_COFID2015 = False
    for foodItem in nutriumDB["foods"]:
    
        if foodItem["information_source_id"] != 23:
            if srchFd["name"] in foodItem["name"].lower() and \
                (" "+srchFd["cooking"]) in foodItem["name"].lower():
                otherDBs.append(foodItem)
            continue
        else:
            if srchFd["name"] in foodItem["name"].lower() and \
                (" "+srchFd["cooking"]) in foodItem["name"].lower():
                foundIn_COFID2015 = True
                if len(cofidDB)==0:
                    cofidDB = foodItem
                if len(foodItem["name"]) < len(cofidDB["name"]) :
                    cofidDB = foodItem
          
    if foundIn_COFID2015==False:
        for foodItem in otherDBs:
            print("\n"+foodItem["name"] + " [DB: "+ nutDBs[foodItem["information_source_id"]]+"]")
            print("---------RULES---------")
            for rule in nutrientRules["solid"]["rules"]:
                calc_rule(rule, foodItem, srchFd)
            print("---------/RULES---------\n")
    else:
        print("\n"+cofidDB["name"] + " [DB: "+ nutDBs[cofidDB["information_source_id"]]+"]")
        print("---------RULES---------")
        for rule in nutrientRules["solid"]["rules"]:
            calc_rule(rule, cofidDB, srchFd)
        print("---------/RULES---------\n")