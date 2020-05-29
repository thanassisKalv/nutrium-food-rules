# nutrium-food-rules
extract rules for food ontology

Using as input the "nutrium-food-data.json" database and mainly the "COFID_2015" ("McCance and Widdowson’s The Composition of Foods Integrated Dataset 2015")

### Example output:
 - Egg *richIn* Energy
 - Egg *containsNutrient* A
 - Black_currant *lowIn* Sugar
 - Black_currant *richIn* C
 - Black_currant *containsNutrient* B12

### To do:
 - complete with all rules from "thresholds.xlsx"
 - add more clever way to choose between databases (e.g. prefer the one that includes more nutrients info)
