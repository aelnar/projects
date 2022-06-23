# https://towardsdatascience.com/ranking-algorithms-know-your-multi-criteria-decision-solving-techniques-20949198f23e
# https://www.codecademy.com/article/normalization

# the big one
# calculate best loadout and rate loadout based on weapons scored based on stats
# she's a big file

# -------------------------------------------------------------------------------------------------
# ---------------------------- BIG OL GLOBAL STUFF HERE COOL THX ----------------------------------
# -------------------------------------------------------------------------------------------------

# weapons: scores
weapons_scored = {}
# weapons: type of gun
# 0 -> ar, 1 -> shot, 2 -> smg, 3 -> sniper
weapons_cat = {'thermal_ar': 0, 'mk_ar': 0, 'ranger_ar': 0, 'striker_br': 0, 'auto_shotgun': 1, 'pump_shotgun': 1, 'drum_shotgun': 1, 'ranger_shotgun': 1,
'stinger_smg': 2, 'combat_smg': 2, 'heavy_sniper': 3, 'hunter_sniper': 3}
# list of weapons
weapons_list = ['thermal_ar', 'mk_ar', 'ranger_ar', 'striker_br', 'auto_shotgun', 'pump_shotgun', 'drum_shotgun', 'ranger_shotgun', 'stinger_smg',
'combat_smg', 'heavy_sniper', 'hunter_sniper']

# weapon name: (scope, damage, fire, reload)
ar = {'thermal_ar': (1, 28.0, 4.0, 2.0), 'mk_ar': (1, 19.0, 9.0, 3.3), 'ranger_ar': (0, 32.0, 4.0, 2.625), 'striker_br': (1, 29.0, 3.86, 2.73)}
ar_list = ['thermal_ar', 'mk_ar', 'ranger_ar', 'striker_br']
shotgun = {'auto_shotgun': (0, 80.4, 1.5, 5.99), 'pump_shotgun': (0, 91.2, 0.65, 5.25), 'drum_shotgun': (0, 60.0, 3.0, 3.68), 'ranger_shotgun': (0, 115.2, 3.0, 1.575)}
shotgun_list = ['auto_shotgun', 'pump_shotgun', 'drum_shotgun', 'ranger_shotgun']
smg = {'stinger_smg': (0, 16.0, 12.0, 2.625), 'combat_smg': (0, 19.0, 12.0, 2.52)}
smg_list = ['stinger_smg', 'combat_smg']
sniper = {'heavy_sniper': (1, 120.0, 0.33, 4.0), 'hunter_sniper': (1, 90.0, 0.64, 3.35)}
sniper_list = ['heavy_sniper', 'hunter_sniper']

# max, min damage -> we want max -> util 1
max_damage_ar = 32.0
max_damage_shot = 115.2
max_damage_smg = 19.0
max_damage_sniper = 120.0
min_damage_ar = 19.0
min_damage_shot = 60.0
min_damage_smg = 16.0
min_damage_sniper = 90.0

# max, min fire -> we want max -> util 2
max_fire_ar = 9.0
max_fire_shot = 3.0
max_fire_smg = 12.0
max_fire_sniper = 0.64
min_fire_ar = 3.86
min_fire_shot = 0.65
min_fire_smg = 12.0
min_fire_sniper = 0.33

# max, min reload -> we want min -> util 3
max_reload_ar = 3.3
max_reload_shot = 3.0
max_reload_smg = 2.652
max_reload_sniper = 4.0
min_reload_ar = 2.0
min_reload_shot = 1.575
min_reload_smg = 2.52
min_reload_sniper = 3.35

# -------------------------------------------------------------------------------------------------
# ---------------------------------- FUNCTIONS FOR CODE YAY COOL ----------------------------------
# -------------------------------------------------------------------------------------------------

# list, max val, min val, what we're scoring
def min_max(wl, max, min, util):
    result = {} # resulting min-max score list
    for i in wl: # go thru list
        if((max - min) != 0.0): # we can divide without zero
            result[i] = (wl[i][util] - min) / (max - min)
        else: # trying to divide by zero which naur
            result[i] = ((wl[i][util] - min) + 0.001) / ((max - min) + 0.001)
    return result

# now based on how many guns are in each category, add weights to the minmax values
# and add them together -> that's the gun's 'final score'
def weights(weight,type, damage, fire, reload):
    # add up scores with weights
    for i in type:
        weapons_scored[i] = (damage[i]*weight[0]) + (fire[i]*weight[1]) + (reload[i]*weight[2])

# aw = ar weight, sw = shotgun weight, sm = smg weight, sn = sniper weight
def big_calculations(aw, sw, sm, sn):

    # minmax damage
    minmax_damage_ar = min_max(ar, max_damage_ar, min_damage_ar, 1)
    minmax_damage_shot = min_max(shotgun, max_damage_shot, min_damage_shot, 1)
    minmax_damage_smg = min_max(smg, max_damage_smg, min_damage_smg, 1)
    minmax_damage_sniper = min_max(sniper, max_damage_sniper, min_damage_sniper, 1)

    # minmax fire
    minmax_fire_ar = min_max(ar, max_fire_ar, min_fire_ar, 2)
    minmax_fire_shot = min_max(shotgun, max_fire_shot, min_fire_shot, 2)
    minmax_fire_smg = min_max(smg, max_fire_smg, min_fire_smg, 2)
    minmax_fire_sniper = min_max(sniper, max_fire_sniper, min_fire_sniper, 2)

    # minmax reload
    minmax_reload_ar = min_max(ar, max_reload_ar, min_reload_ar, 3)
    minmax_reload_shot = min_max(shotgun, max_reload_shot, min_reload_shot, 3)
    minmax_reload_smg = min_max(smg, max_reload_smg, min_reload_smg, 3)
    minmax_reload_sniper = min_max(sniper, max_reload_sniper, min_reload_sniper, 3)

    # weights for ar, shot, smg, sniper
    weights(aw, ar_list, minmax_damage_ar, minmax_fire_ar, minmax_reload_ar)
    weights(sm, smg_list, minmax_damage_smg, minmax_fire_smg, minmax_reload_smg)
    weights(sw, shotgun_list, minmax_damage_shot, minmax_fire_shot, minmax_reload_shot)
    weights(sn, sniper_list, minmax_damage_sniper, minmax_fire_sniper, minmax_reload_sniper)

# helper fcn -> types of guns in current loadout
def loadout_type(loadout):
    types = []
    for i in loadout:
        types.append(weapons_cat[i])
    return types

# ideal_loadout(slots, pref)
def ideal_loadout(slots, pref):

    # take apart preferences so it's easier to deal with later
    # corresponds with type -> ar shotgun smg sniper
    preferences = {0: pref[0], 1: pref[2], 2: pref[1], 3: pref[3]}

    loadout = [] # going to give final loadout

    # go thru all weapons
    for i in weapons_list:

        # just fill loadout in initially
        if(len(loadout) < slots):
            loadout.append(i)

        else: # we do the big stuff here

            # first find the min weapon in loadout with lowest score and lowest preference
            # min weapon = (name, type, score, preference)
            min_weapon = (None, 0, float('inf'), float('inf'))

            for j in loadout:
                type = weapons_cat[str(j)]
                score = weapons_scored[str(j)]
                pr = preferences[type]

                # curr loadout weapon is lower -> make that the min weapon
                if(min_weapon[2] > score and min_weapon[3] > pr):
                    min_weapon = (str(j), type, score, pr)

            # then we find the best weapon to replace that one with higher score and highest preference
            types = loadout_type(loadout)
            max_weapon = (None, 0, float('-inf'), float('-inf'))

            for n in weapons_scored:
                tn = weapons_cat[str(n)]
                sn = weapons_scored[str(n)]
                pn = preferences[tn]

                # higher score, higher preference
                if(max_weapon[2] < sn and max_weapon[3] < pn):

                    # if we already have max in our loadout, go find next highest preference weapon
                    # NOT yet in loadout and find the max weapon there -> add it
                    if(str(n) in loadout):

                        next_weapon = (None, 0, float('-inf'), float('-inf'))
                        for m in weapons_scored:
                            tm = weapons_cat[str(m)]
                            sm = weapons_scored[str(m)]
                            pm = preferences[tm]

                            # next highest pref, not in loadout, next weapon is max
                            if(pn > pm and tm not in types and next_weapon[2] < sm):
                                next_weapon = (str(m), tm, sm, pm)

                        max_weapon = next_weapon # the max is set to the next best weapon

                    elif (tn in types): # we have this type of gun in loadout -> find next highest and make that the max

                        next_weapon = (None, 0, float('-inf'), float('-inf'))
                        for u in weapons_scored:
                            tu = weapons_cat[str(u)]
                            su = weapons_scored[str(u)]
                            pu = preferences[tu]

                            # next highest pref, not in loadout, next weapon is max
                            if(pn > pu and tu not in types and next_weapon[2] < su):
                                next_weapon = (str(u), tu, su, pu)

                        max_weapon = next_weapon # the max is set to the next best weapon

                    else: # max weapon found atm is not in loadout AND it's not a type in loadout already
                        max_weapon = (str(n), tn, sn, pn)

            # finally we found max weapon
            # remove min from loadout and add max
            loadout.remove(str(min_weapon[0]))
            loadout.append(str(max_weapon[0]))

    return loadout

# finding out curr score of loadout
def loadout_score(loadout, pref):
    score = 0
    for p in loadout:
        score += weapons_scored[str(p)]
    return score

# check_loadout(loadout, pref, slots)
def check_loadout(loadout, pref):

    better_loadout = []
    types = loadout_type(loadout)
    preferences = {0: pref[0], 1: pref[2], 2: pref[1], 3: pref[3]}
    min_pref = (pref[0] + pref[1] + pref[2] + pref[3]) / 4

    # first we find the current score of current loadout
    curr_score = loadout_score(loadout, pref)
    print("Currently, this loadout's combined score is: ", curr_score)

    # go thru the loadout
    for i in loadout:

        # curr weapon we're looking at
        ct = weapons_cat[str(i)]
        cs = weapons_scored[str(i)]
        cp = preferences[ct]
        curr_weapon = (str(i), ct, cs) # name, type, score

        max_weapon = (None, 0, float('-inf'))
        bt = loadout_type(better_loadout)

        # if gun is in loadout and we have a high preference for it
        if (cp >= min_pref):

            # if better_loadout already has a weapon of that type, find next best of a different type
            if (ct in bt):
                for y in weapons_scored:
                    #  and str(y) not in better_loadout
                    if(weapons_cat[str(y)] != ct and str(y) not in better_loadout and weapons_scored[str(y)] > max_weapon[2]):
                        max_weapon = (str(y), weapons_cat[str(y)], weapons_scored[str(y)])
            # else, we don't have one -> find best gun of that type
            else:
                for j in weapons_scored:
                    if(weapons_cat[str(j)] == ct and str(j) not in better_loadout and weapons_scored[str(j)] > max_weapon[2]):
                        max_weapon = (str(j), weapons_cat[str(j)], weapons_scored[str(j)])

        # if the gun is in loadout and we don't have the highest for it, find a gun of a different type
        # that makes the curr_score go up
        if (cp <= min_pref):

            max_score = 0

            # go through scores of guns not of that type and see if it raises curr_score
            for n in weapons_scored:

                # not the same type and not in better_loadout so far, but score is better
                if(weapons_cat[str(n)] != ct and str(n) not in better_loadout and weapons_cat[str(n)] not in bt and max_weapon[2] < weapons_scored[str(n)]):

                    # let's see the potential loadout score
                    # gotta make it a new list so it doesn't mess with loadout as it is
                    pl = loadout.copy()
                    pl.remove(str(i))
                    pl.append(str(n))
                    potential_score = loadout_score(pl, pref)

                    # if adding this weapon made curr_score < potential_score and potential_score > max_score, change max_weapon and max score
                    if(curr_score < potential_score and potential_score > max_score):
                        max_score = potential_score
                        max_weapon = (str(n), weapons_cat[str(n)], weapons_scored[str(n)])

        # finally, if max_weapon is not none, we found a better gun -> suggest and add it
        # else, we already have the best gun for our loadout
        if(max_weapon[0] != None):
            print("Instead of", str(i), "try", str(max_weapon[0]), "instead.")
            better_loadout.append(str(max_weapon[0]))
        else:
            print(str(i), "is the best weapon for this loadout.")
            better_loadout.append(str(i))

    return better_loadout

# -------------------------------------------------------------------------------------------------
# ----------------------------------- MAIN STUFF HAPPENING HERE -----------------------------------
# -------------------------------------------------------------------------------------------------

# give damage, fire, reload weights to type of gun

#print("--------------------------------------")

#print("Give preferences for 1) damage, 2) fire rate, and 3) reload weights to each element for each type of gun.")
#print("Will be used to calculate scores of guns according to preference.")
aw  = (0.6, 0.2, 0.2) # ar
sm = (0.5, 0.3, 0.2) # smg
sw = (0.7, 0.1, 0.2) # shotgun
sn = (0.7, 0.1, 0.2) # sniper
#print("Calaculating scores...")
big_calculations(aw, sw, sm, sn) # calc the scores so it's in weapons_scored
#print("Scores of weapons calculated.")

#print("--------------------------------------")

# preferences for each gun from 0 -> 1.0
# ar, smg, shotgun, sniper
pref = (0.8, 0.4, 0.6, 0.7)
result = ideal_loadout(3, pref)
#print("Based on the preferences given, the ideal loadout is: ", result)

#print("--------------------------------------")

print("Put in your current loadout as a list.")
print("Based on the preferences, check_loadout will check if you're currently running the best loadout.")
load = ['striker_br', 'auto_shotgun', 'heavy_sniper']
l2 = check_loadout(load, pref)
print("Based on scores, the better loadout is: ", l2)
print("This loadout's score is: ", loadout_score(l2, pref))
