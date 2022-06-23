# https://towardsdatascience.com/ranking-algorithms-know-your-multi-criteria-decision-solving-techniques-20949198f23e
# https://www.codecademy.com/article/normalization

# calculations for scores of the guns
# basically stuff i don't want in weap.py

# weapons: scores
weapons_scored = {}

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
# wd = 0.5, 0.2, 0.3
def weights(type, damage, fire, reload):
    # add up scores with weights
    for i in type:
        weapons_scored[i] = (damage[i]*0.5) + (fire[i]*0.2) + (reload[i]*0.3)

# -------------------------------------------------------------------------------------------------
# ----------------------------------- MAIN STUFF HAPPENING HERE -----------------------------------
# -------------------------------------------------------------------------------------------------

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
weights(ar_list, minmax_damage_ar, minmax_fire_ar, minmax_reload_ar)
weights(smg_list, minmax_damage_smg, minmax_fire_smg, minmax_reload_smg)
weights(shotgun_list, minmax_damage_shot, minmax_fire_shot, minmax_reload_shot)
weights(sniper_list, minmax_damage_sniper, minmax_fire_sniper, minmax_reload_sniper)
