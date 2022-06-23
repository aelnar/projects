# weapon name: (scope, damage, fire, reload)
# based on green unless available in blue+
# no pistols + guns sold
weapons = { 'thermal_ar': (1, 28.0, 4.0, 2.0), 'mk_ar': (1, 19.0, 9.0, 3.3), 'ranger_ar': (0, 32.0, 4.0, 2.625), 'striker_br': (1, 29.0, 3.86, 2.73),
'auto_shotgun': (0, 80.4, 1.5, 5.99), 'pump_shotgun': (0, 91.2, 0.65, 5.25), 'drum_shotgun': (0, 60.0, 3.0, 3.68), 'ranger_shotgun': (0, 115.2, 3.0, 1.575),
'stinger_smg': (0, 16.0, 12.0, 2.625), 'combat_smg': (0, 19.0, 12.0, 2.52),
'heavy_sniper': (1, 120.0, 0.33, 4.0), 'hunter_sniper': (1, 90.0, 0.64, 3.35)}

# weapons 2.0
# rifle = 0, shotgun = 1, smg = 2, sniper = 3
weapons_cat = { ('thermal_ar', 0): (1, 28.0, 4.0, 2.0), ('mk_ar', 0): (1, 19.0, 9.0, 3.3), ('ranger_ar', 0): (0, 32.0, 4.0, 2.625), ('striker_br', 0): (1, 29.0, 3.86, 2.73),
('auto_shotgun', 1): (0, 80.4, 1.5, 5.99), ('pump_shotgun', 1): (0, 91.2, 0.65, 5.25), ('drum_shotgun', 1): (0, 60.0, 3.0, 3.68), ('ranger_shotgun', 1): (0, 115.2, 3.0, 1.575),
('stinger_smg', 2): (0, 16.0, 12.0, 2.625), ('combat_smg', 2): (0, 19.0, 12.0, 2.52),
('heavy_sniper', 3): (1, 120.0, 0.33, 4.0), ('hunter_sniper', 3): (1, 90.0, 0.64, 3.35)}

# do some stuff for the ideal loadout
def loadout(slots, scope, damage, fire, reload):

    # our loadout so chrew
    loadout = []
    sc = 0

    # we goge
    for i in weapons:

        # empty spaces
        if(len(loadout) < slots):

            # scoped
            if(weapons[i][0] == 1):
                if(sc < scope): # less than scope count
                    loadout.append(i)
                    sc += 1
                else: # max scope count
                    min_weapon = None
                    two_third = 0
                    # now checking for best damage, fire, reload closest to param
                    for j in loadout:
                        if(weapons[j][0] == 1): # we're replacing a scoped weapon
                            if(weapons[j][1] > weapons[i][1] and weapons[j][1] < damage):
                                two_third += 1
                            if(weapons[j][2] > weapons[i][2] and weapons[j][2] < fire):
                                two_third += 1
                            if(weapons[j][3] > weapons[i][3] and weapons[j][3] < reload):
                                two_third += 1

                            # two-thirds worse than input, we replace j with i
                            if(two_third >= 2):
                                min_weapon = j

                    # remove min weapon if there is one and then replace with i
                    if(min_weapon != None):
                        loadout.remove(str(min_weapon))
                        sc -= 1
                        loadout.append(i)
                        sc += 1

            else: # just add it
                loadout.append(i)

        else: # we're full on the loadout

            # check scope limit
            if(weapons[i][0] == 1):
                if(sc < scope): # less than scope count
                    loadout.append(i)
                    sc += 1
                else: # max scope count
                    min_weapon = None
                    two_third = 0
                    # now checking for best damage, fire, reload closest to param
                    for j in loadout:
                        if(weapons[j][0] == 1): # we're replacing a scoped weapon
                            if(weapons[j][1] > weapons[i][1] and weapons[j][1] < damage):
                                two_third += 1
                            if(weapons[j][2] > weapons[i][2] and weapons[j][2] < fire):
                                two_third += 1
                            if(weapons[j][3] > weapons[i][3] and weapons[j][3] < reload):
                                two_third += 1

                            # two-thirds worse than input, we replace j with i
                            if(two_third >= 2):
                                min_weapon = j

                    # take out min_weapon
                    if(min_weapon != None):
                        loadout.remove(str(min_weapon))
                        sc -= 1
                        loadout.append(i)
                        sc += 1

            else: # normal weapon -> we check damage, fire, reload
                    min_weapon = None
                    two_third = 0
                    # now checking for best damage, fire, reload closest to param
                    for j in loadout:
                        if(weapons[j][0] == 0): # we're replacing a normal weapon
                            if(weapons[j][1] > weapons[i][1] and weapons[j][1] < damage):
                                two_third += 1
                            if(weapons[j][2] > weapons[i][2] and weapons[j][2] < fire):
                                two_third += 1
                            if(weapons[j][3] > weapons[i][3] and weapons[j][3] < reload):
                                two_third += 1

                            # two-thirds worse than input, we replace j with i
                            if(two_third >= 2):
                                min_weapon = j

                    # replace
                    if(min_weapon != None):
                        loadout.remove(str(min_weapon))
                        loadout.append(i)

    return loadout

# helper fcn to find what type of weapon it is in cat
def find_in_cat(name):

    for j in weapons_cat: # go thru weapons list
        if name == j[0]:
            return j # return key

# check if loadout is good
def check_loadout(loadout):

    best_loadout = []

    for i in loadout: # go thru loadout

        val = find_in_cat(i) # find loadout weapon in cat
        best_loadout.append(i)

        for j in weapons_cat: # go thru weapons list
            two_third = 0
            best_weapon = None
            #print(weapons_cat[val][1], weapons_cat[val][2], weapons_cat[val][3])
            if(j[1] == val[1]): # same weapon type as what's in loadout -> check if it's better
                if(weapons_cat[val][1] < weapons_cat[j][1]):
                    two_third += 1
                if(weapons_cat[val][2] < weapons_cat[j][2]):
                    two_third += 1
                if(weapons_cat[val][3] < weapons_cat[j][3]):
                    two_third += 1

                if(two_third >= 2):
                    best_weapon = j

                # there's a better weapon in this category AND it's not in loadout
                if(best_weapon != None and best_weapon not in loadout):
                    print("Instead of", i, "try", best_weapon[0], "instead in your loadout.")
                    best_loadout.remove(str(i))
                    best_loadout.append(str(best_weapon[0]))

    print("Final best loadout is: ", best_loadout)

# ------------------------------------------------------------------------------------------
# ---------------------------------------- MAIN --------------------------------------------
# ------------------------------------------------------------------------------------------


""" Find out what loadout to run """
#print("Get ideal loadout for a game.")
#print("- Stats based on green rarity unless only available in blue and up (in that case blue is used)")
#print("Loadout parameters: amount for loadout, how many scoped weapons, ideal damage, ideal firing rate, ideal reload speed.")
print("---------------------------------------------------------------")
result = loadout(3, 1, 60.0, 2.0, 1.0)
print("Ideal loadout is: ", result)
print("---------------------------------------------------------------")
""" Find out if loadout is ideal/the best """
load = ['ranger_ar', 'combat_smg', 'hunter_sniper']
print("Current loadout: ", load)
check_loadout(load)
print("---------------------------------------------------------------")
