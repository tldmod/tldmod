#OUTPUT module_items copy column to python
from module_constants import *
from header_items import  *
from header_operations import *
from header_triggers import *
from header_factions import *
from module_info import wb_compile_switch as is_a_wb_item
#
#
####################################################################################################################
### Each item record contains the following fields:
### 1) Item id: used for referencing items in other files.
###    The prefix itm_ is automatically added before each item id.
### 2) Item name. Name of item as it'll appear in inventory window
### 3) List of meshes.  Each mesh record is a tuple containing the following fields:
###   3.1) Mesh name.
###   3.2) Modifier bits that this mesh matches.
###    Note that the first mesh record is the default.
### 4) Item flags. See header_items.py for a list of available flags.
### 5) Item capabilities. Used for which animations this item is used with. See header_items.py for a list of available flags.
### 6) Item value.
### 7) Item stats: Bitwise-or of various stats about the item such as:
###     weight, abundance, difficulty, head_armor, body_armor,leg_armor, etc...
### 8) Modifier bits: Modifiers that can be applied to this item.
### 9)[Optional] Triggers: List of simple triggers to be associated with the item.
####################################################################################################################
#

#raw_damage = weapon_damage * hold_bonus * speed_bonus * (proficiency*0.01*0.15+0.85) * (powerstrike * 0,08 + 1) + STR/5

#effective_damage = raw_damage - soak_factor - ((1 - 1/reduction_factor) * (raw_damage - soak_factor)) 

	# if item_flags & itp_extra_penetration:
		# soak_factor *= module.ini_extra_penetration_soak_factor
		# reduction_factor *= module.ini_extra_penetration_reduction_factor
		
	# if hit_bone == head:
		# effective_damage *= 1.2

		# if item_is_ranged:
			# effective_damage *= 1.75
	# elif hit_bone == calf or hit_bone == thigh:
		# effective_damage *= 0.9


def troll_aoe(item):
  return (ti_on_weapon_attack, [
    ] + (is_a_wb_item==1 and [

    (store_trigger_param_1, ":agent_no"),

    (agent_is_active, ":agent_no"),
    (agent_is_alive, ":agent_no"),

    (store_random_in_range, ":rand", 0, 2),
    (eq, ":rand", 0), # 1/2 chance of dealing AOE

    (agent_get_attack_action, ":action", ":agent_no"),
  
    (is_between, ":action", 2, 7),
    #(display_message, "@Clear"), 

    (agent_get_position, pos9, ":agent_no"),
    (set_fixed_point_multiplier, 100),

    (try_for_agents, ":aoe_hit", pos9, 200),
      (agent_is_active, ":aoe_hit"),
      (agent_is_alive, ":aoe_hit"),
      (agent_is_human, ":aoe_hit"),
      (neq, ":aoe_hit", ":agent_no"), #don't hit yourself
      (gt, ":aoe_hit", 0),

      (agent_get_troop_id, ":victim_troop_id", ":aoe_hit"),
      (troop_get_type, ":victim_type", ":victim_troop_id"),
      (agent_get_horse, ":victim_horse", ":aoe_hit"),
      
      (store_random_in_range, ":flyback_anim", 0, 2),
      # then, set animation
      
      (neq, ":victim_type", tf_troll), #no flyback for trolls

      (try_begin),   
      # human (non trolls, non horse) victims
        (try_begin),
          (eq, ":flyback_anim", 0),
      # troll is in front of victim
          (agent_set_animation, ":aoe_hit", "anim_strike_fly_back_rise_from_left"), # send them flying back
        (else_try),
          (agent_set_animation, ":aoe_hit", "anim_strike_fly_back_rise"), # send them flying back
        (try_end),

      (store_random_in_range, ":rand_sound", 0, 6),
      (try_begin),
        (eq, ":rand_sound", 0),
        (agent_play_sound, ":aoe_hit", "snd_wooden_hit_low_armor_low_damage"),
      (else_try),
        (eq, ":rand_sound", 1),
        (agent_play_sound, ":aoe_hit", "snd_wooden_hit_low_armor_high_damage"),
      (else_try),
        (eq, ":rand_sound", 2),
        (agent_play_sound, ":aoe_hit", "snd_wooden_hit_high_armor_low_damage"),
      (else_try),
        (eq, ":rand_sound", 3),
        (agent_play_sound, ":aoe_hit", "snd_wooden_hit_high_armor_low_damage"),
      (else_try),
        (eq, ":rand_sound", 4),
        (agent_play_sound, ":aoe_hit", "snd_wooden_hit_high_armor_high_damage"),
      (else_try),
        (agent_play_sound, ":aoe_hit", "snd_blunt_hit"),
      (try_end),

        (try_begin),
          (gt, ":victim_horse", 1),
          (agent_start_running_away, ":victim_horse"),
          (agent_stop_running_away, ":victim_horse"),
        (try_end),
        (store_random_in_range,":random_timings",1,5),
        (agent_set_animation_progress, ":aoe_hit", ":random_timings"), # differentiate timings a bit

        (item_get_swing_damage, ":damage", item),
        (val_div, ":damage", 2),
        (agent_deliver_damage_to_agent, ":agent_no", ":aoe_hit", ":damage"),

      (try_end),
    (try_end),
     ] or []) + [ 
    ])

def custom_reskin(item):
  return (ti_on_init_item, [
    ] + (is_a_wb_item==1 and [
    # (store_trigger_param_1, ":agent_no"), #disabled to suppress compiler warnings
    (store_trigger_param_2, ":troop_no"),
    (troop_slot_eq, ":troop_no", slot_troop_has_custom_armour, 1),

    (call_script, "script_cf_get_custom_armor_ranges", ":troop_no", item),
    (assign, ":start", reg0),
    (assign, ":end", reg1),

    (str_clear, s1),
    #(item_get_slot, ":start", item, slot_item_materials_begin),
    #(item_get_slot, ":end", item, slot_item_materials_end),
    (store_sub, ":total", ":end", ":start"),
    (gt, ":total", 0),
    (try_begin),
      (gt, ":troop_no", -1),
      (troop_is_hero, ":troop_no"),
      (item_get_slot, ":value", item, slot_item_player_color),
      (neq, ":value", -1),
      (val_mod, ":value", ":total"),
      (val_add, ":value", ":start"),
    (else_try),
      (store_random_in_range, ":value", ":start", ":end"),
    (try_end),
    (try_begin),
      (str_store_string, s1, ":value"),
      (cur_item_set_material, s1, 0),
    (try_end),
    ] or []) + [ 
    ])


# Female Armour Variation

def custom_female(item):
  return (ti_on_init_item, [
    ] + (is_a_wb_item==1 and [
    # (store_trigger_param_1, ":agent_no"), #disabled to suppress compiler warnings
    (store_trigger_param_2, ":troop_no"),

    (troop_get_type, ":is_female", ":troop_no"),
    (eq, ":is_female", tf_female),
    
    (str_clear, s1),
    (item_get_slot, ":start", item, slot_item_materials_begin),
    (item_get_slot, ":end", item, slot_item_materials_end),
    (store_sub, ":total", ":end", ":start"),
    (gt, ":total", 0),
    (try_begin),
      (gt, ":troop_no", -1),
      (troop_is_hero, ":troop_no"),
      (item_get_slot, ":value", item, slot_item_player_color),
      (neq, ":value", -1),
      (val_mod, ":value", ":total"),
      (val_add, ":value", ":start"),
    (else_try),
      (store_random_in_range, ":value", ":start", ":end"),
    (try_end),
    (try_begin),
      (str_store_string, s1, ":value"),
      (cur_item_set_material, s1, 0),
    (try_end),
    ] or []) + [ 
    ])

# Dunde's 1 Liner Heraldic Code
def heraldic(item_tableau):
  return (ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", item_tableau, ":agent_no", ":troop_no")])

###Some constants for ease of use.
### Kham - Unused imods for mesh hack
### poor old cheap well_made sharp deadly exquisite powerful rough fresh day_old two-day_old rotten
### InVain - checked and removed non-existent ones. Just choose any imod that can't be acquired by the specific item.

###InVain: Weight ranges

# Super Light: 0-5 (nude, light leather, cloth)
# Light 5-10 (reinforced leather, padded cloth)
# Med 10-20 (layered light, light scale)
# Light Mail 18-25
# Mail 25-30
# Heavy 30-40 (heavy Mail, layered mail)

# hat/hood - 0,5
# Light helm - 1-1.5
# regular helm 1.5-2.5
# heavy helm 2.5-4.5 

# light boots - 1
# med boots - 1.5-2
# heavy boots - 2.5-4

imodbits_none = 0
#
imodbits_horse_basic = imodbit_swaybacked | imodbit_lame | imodbit_heavy | imodbit_stubborn | imodbit_timid 
imodbits_horse_good = imodbit_spirited | imodbit_heavy   | imodbit_champion | imodbit_timid 
imodbits_warg = imodbit_swaybacked | imodbit_lame | imodbit_heavy | imodbit_stubborn  | imodbit_heavy   | imodbit_champion
#
imodbits_good   = 0#imodbit_sturdy | imodbit_thick | imodbit_hardened | imodbit_reinforced
imodbits_bad    = 0#imodbit_rusty | imodbit_chipped | imodbit_tattered | imodbit_ragged | imodbit_cracked | imodbit_bent
#
imodbits_cloth  =   imodbit_tattered | imodbit_ragged | imodbit_sturdy | imodbit_thick | imodbit_hardened
imodbits_orc_cloth  = imodbit_tattered | imodbit_ragged | imodbit_sturdy | imodbit_thick | imodbit_hardened
imodbits_elf_cloth  = imodbit_sturdy | imodbit_thick | imodbit_hardened | imodbit_reinforced 
#
imodbits_armor  = imodbit_cracked | imodbit_rusty  | imodbit_crude | imodbit_thick | imodbit_reinforced
imodbits_armor_bad  = imodbit_cracked | imodbit_rusty  | imodbit_crude
imodbits_armor_good  = imodbit_thick | imodbit_reinforced
imodbits_orc_armor  = imodbit_tattered | imodbit_ragged | imodbit_cracked | imodbit_rusty  | imodbit_crude | imodbit_thick | imodbit_reinforced
imodbits_orc_bad  = imodbit_cracked | imodbit_tattered | imodbit_ragged | imodbit_rusty  | imodbit_crude
imodbits_orc_good  = imodbit_thick | imodbit_reinforced | imodbit_hardened																  

imodbits_elf_armor  = imodbit_thick | imodbit_reinforced | imodbit_lordly
imodbits_elf_good = imodbit_thick | imodbit_reinforced | imodbit_lordly| imodbit_hardened
#
imodbits_thrown   =  imodbit_bent | imodbit_heavy| imodbit_balanced| imodbit_large_bag
imodbits_missile  = imodbit_crude | imodbit_bent | imodbit_large_bag | imodbit_fine | imodbit_balanced
imodbits_good_missile  = imodbit_large_bag | imodbit_fine | imodbit_balanced
imodbits_bow = imodbit_cracked | imodbit_bent | imodbit_crude | imodbit_fine | imodbit_strong
imodbits_good_bow = imodbit_fine | imodbit_strong | imodbit_masterwork 
#
imodbits_shield  = imodbit_cracked | imodbit_battered | imodbit_crude | imodbit_sturdy | imodbit_hardened | imodbit_thick | imodbit_reinforced
imodbits_shield_good = imodbit_thick | imodbit_hardened | imodbit_reinforced | imodbit_lordly
imodbits_weapon   = imodbit_rusty | imodbit_chipped | imodbit_crude | imodbit_fine | imodbit_heavy | imodbit_balanced |imodbit_tempered
imodbits_weapon_bad  = imodbit_cracked | imodbit_rusty | imodbit_chipped | imodbit_crude
imodbits_weapon_bad_heavy = imodbit_heavy | imodbit_strong
imodbits_weapon_good  = imodbit_fine | imodbit_balanced | imodbit_tempered | imodbit_masterwork
imodbits_weapon_wood   = imodbit_bent | imodbit_crude | imodbit_fine | imodbit_heavy | imodbit_balanced

#
items =[
###item_name, mesh_name, item_properties, item_capabilities, slot_no, cost, bonus_flags, weapon_flags, scale, view_dir, pos_offset
#next one is used in scripts
["no_item","INVALID_ITEM",[("invalid_item",0)],itp_type_goods,0,3,weight(1.5)|abundance(90)|0,imodbits_none],
["horse_meat","Horse_Meat",[("raw_meat",0)],itp_type_goods|itp_consumable|itp_food,0,12,weight(40)|abundance(0)|food_quality(30)|max_ammo(40),imodbits_none],
###Items before this point are hardwired and their order should not be changed!
#next one used by tutorial swordsman and in arena missions
["practice_sword","Practice_Sword",[("practice_sword",0)],itp_primary|itp_wooden_parry|itp_type_one_handed_wpn|itp_secondary|itp_wooden_attack,itc_longsword,1,weight(1.5)|difficulty(0)|spd_rtng(103)|weapon_length(90)|swing_damage(16,blunt)|thrust_damage(12,blunt),0],
#["arena_axe","Axe",[("arena_axe",0)],itp_primary|itp_wooden_parry|itp_type_one_handed_wpn|itp_secondary|itp_bonus_against_shield,itc_scimitar|itcf_carry_axe_left_hip,1,weight(1.5)|difficulty(0)|spd_rtng(100)|weapon_length(69)|swing_damage(23,blunt)|thrust_damage(0,blunt),0],
#["arena_sword","Sword",[("arena_sword_one_handed",0)],itp_primary|itp_wooden_parry|itp_type_one_handed_wpn,itc_longsword|itcf_carry_sword_left_hip,1,weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(95)|swing_damage(21,blunt)|thrust_damage(17,blunt),0],
#["arena_sword_two_handed","Two_Handed_Sword",[("arena_sword_two_handed",0)],itp_primary|itp_wooden_parry|itp_type_two_handed_wpn|itp_two_handed,itc_greatsword|itcf_carry_sword_back,1,weight(2.75)|difficulty(0)|spd_rtng(93)|weapon_length(110)|swing_damage(29,blunt)|thrust_damage(21,blunt),0],
#used in arena missions?
["arena_lance","Lance",[("arena_lance",0)],itp_primary|itp_wooden_parry|itp_type_polearm|itp_no_blur|itp_spear|itp_penalty_with_shield|itp_couchable,itc_staff|itcf_carry_spear, 1,weight(2.5)|difficulty(0)|spd_rtng(96)|weapon_length(150)|swing_damage(20,blunt)|thrust_damage(25,blunt),0],
["practice_staff","Wooden_Staff",[("wooden_staff",0)],itp_primary|itp_wooden_parry|itp_type_polearm|itp_no_blur|itp_spear|itp_penalty_with_shield|itp_wooden_attack, itc_staff|itcf_carry_sword_back,1,weight(2.5)|difficulty(0)|spd_rtng(103)|weapon_length(118)|swing_damage(16,blunt)|thrust_damage(12,blunt),0],
["practice_bow","Practice_Bow",[("small_bow",0),("small_bow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_two_handed|itp_type_bow|itp_primary|itp_two_handed, itcf_shoot_bow|itcf_carry_bow_back,1,weight(1.5)|difficulty(0)|shoot_speed(40)|spd_rtng(90)|thrust_damage(19,blunt),0],
["wooden_javelin","Wooden_javelin",[("wooden_javelin",0)],itp_type_thrown|itp_primary|itp_bonus_against_shield, itcf_throw_javelin,100,weight(3)|difficulty(0)|shoot_speed(27)|spd_rtng(89)|weapon_length(65)|thrust_damage(25,blunt)|max_ammo(5),imodbits_thrown],
#
#foods (first one is smoked_fish)
["human_meat","Human_Flesh",[("human_flesh",0)],itp_shop|itp_type_goods|itp_consumable|itp_food,0,103,weight(20)|abundance(50)|food_quality(80)|max_ammo(30),imodbits_none],
["maggoty_bread","Maggoty_Bread",[("maggoty_bread",0)],itp_shop|itp_type_goods|itp_consumable|itp_food,0,32,weight(10)|abundance(100)|food_quality(50)|max_ammo(50),imodbits_none],
["cram","Cram_Ration",[("cram",0)],itp_shop|itp_type_goods|itp_consumable|itp_food,0,44,weight(10)|abundance(100)|food_quality(50)|max_ammo(50),imodbits_none],
["lembas","Lembas",[("lembas",0)],itp_type_goods|itp_consumable,0,200,weight(1.3)|abundance(10)|food_quality(80)|max_ammo(100),imodbits_none],
["smoked_fish","Smoked_Fish",[("smoked_fish",0)],itp_shop|itp_type_goods|itp_consumable|itp_food,0,59,weight(15)|abundance(110)|food_quality(50)|max_ammo(50),imodbits_none],
["dried_meat","Dried_Meat",[("smoked_meat",0)],itp_shop|itp_type_goods|itp_consumable|itp_food,0,72,weight(15)|abundance(100)|food_quality(60)|max_ammo(50),imodbits_none],
["cattle_meat","Beef",[("raw_meat",0)],itp_shop|itp_type_goods|itp_consumable|itp_food,0,103,weight(20)|abundance(100)|food_quality(70)|max_ammo(70),imodbits_none],
#other trade goods (first one is wine)
["grain","Wheat",[("wheat_sack",0)],itp_type_goods|itp_consumable,0,77,weight(50)|abundance(110)|food_quality(40)|max_ammo(50),imodbits_none],
#in-game, but serve no purpose? Used for trade routes?
["tools","Tools",[("iron_hammer",0)],itp_type_goods,0,410,weight(50)|abundance(90)|0,imodbits_none],
#************************************************************************************************
###ITEMS before this point are hardcoded into item_codes.h and their order should not be changed!
#************************************************************************************************
###Quest Items
["siege_supply","Supplies",[("ale_barrel",0)],itp_type_goods,0,96,weight(40)|abundance(70)|0,imodbits_none],
["quest_wine","Wine",[("amphora_slim",0)],itp_type_goods,0,46,weight(40)|abundance(60)|max_ammo(50),imodbits_none],
["quest_ale","Ale",[("ale_barrel",0)],itp_type_goods,0,31,weight(40)|abundance(70)|max_ammo(50),imodbits_none],

["metal_scraps_bad","Low_grade_metal_scraps",[("weapon_scraps_a",0)],itp_type_goods,0,scrap_bad_value,weight(40)|abundance(0)|0,imodbits_none],
["metal_scraps_medium","Usable_metal_scraps",[("weapon_scraps_b",0)],itp_type_goods,0,scrap_medium_value/2,weight(40)|abundance(0)|0,imodbits_none],
["metal_scraps_good","Good_quality_metal_scraps",[("weapon_scraps_c",0)],itp_type_goods,0,scrap_good_value/2,weight(40)|abundance(0)|0,imodbits_none],
# 
###Horses: sumpter horse/ pack horse, saddle horse, steppe horse, warm blood, geldling, stallion,   war mount, charger, 
###Carthorse, hunter, heavy hunter, hackney, palfrey, courser, destrier.
# scraps_end in constants points here
["oliphant","Oliphaunt",[("oliphant",0)],itp_type_horse,0,1,hit_points(255)|body_armor(255)|difficulty(255)|horse_speed(1)|horse_maneuver(1)|horse_charge(500),imodbits_horse_basic|0],

["sumpter_horse","Sumpter_Horse",[("sumpter_horse",0),("CWE_horse_light_a",imodbit_cracked),("CWE_horse_light_b",imodbit_rusty),("CWE_horse_light_c",imodbit_bent)],itp_type_horse|itp_shop,0,70,hit_points(40)|body_armor(1)|difficulty(1)|horse_speed(28)|horse_maneuver(33)|horse_charge(5)|horse_scale(95)|abundance(90),imodbits_horse_basic|imodbits_horse_basic,[]],
["saddle_horse","Saddle_Horse",[("sumpter_horse",0)],itp_type_horse|itp_shop,0,150,hit_points(60)|body_armor(7)|difficulty(1)|horse_speed(39)|horse_maneuver(34)|horse_charge(8)|horse_scale(100)|abundance(90),imodbits_horse_basic|imodbits_horse_basic,[]],
["steppe_horse","Steppe_Horse",[("steppe_horse",0)],itp_type_horse|itp_shop,0,160,hit_points(70)|body_armor(10)|difficulty(2)|horse_speed(35)|horse_maneuver(41)|horse_charge(7)|horse_scale(95)|abundance(90),imodbits_horse_basic|imodbits_horse_basic,[]],
["courser","Courser",[("courser",0)],itp_type_horse|itp_shop,0,350,hit_points(70)|body_armor(10)|difficulty(2)|horse_speed(43)|horse_maneuver(37)|horse_charge(11)|horse_scale(100)|abundance(91),imodbits_horse_basic|imodbits_horse_basic,[]],
["hunter","Hunter",[("saddle_horse",0)],itp_type_horse|itp_shop,0,600,hit_points(90)|body_armor(20)|difficulty(3)|horse_speed(36)|horse_maneuver(34)|horse_charge(18)|horse_scale(100)|abundance(91),imodbits_horse_basic|imodbits_horse_basic,[]],
["pony","Pony",[("pony",0)],itp_type_horse|itp_shop,0,70,hit_points(30)|body_armor(0)|difficulty(0)|horse_speed(20)|horse_maneuver(40)|horse_charge(1)|horse_scale(100)|abundance(90),imodbits_horse_basic|imodbits_horse_good,[]],
["free_arnor_warhorse","Arnorian_Warhorse",[("arnor_warhorse_b",0)],itp_type_horse|itp_shop,0,2200,hit_points(150)|body_armor(40)|difficulty(4)|horse_speed(37)|horse_maneuver(34)|horse_charge(35)|horse_scale(100)|abundance(92),imodbits_horse_basic|imodbits_horse_good,[]],
["dunedain_warhorse","Dunedain_Warhorse",[("arnor_warhorse_a",0),("arnor_warhorse_b",imodbit_heavy)],itp_type_horse|itp_shop,0,1800,hit_points(140)|body_armor(36)|difficulty(4)|horse_speed(38)|horse_maneuver(35)|horse_charge(30)|horse_scale(100)|abundance(94),imodbits_horse_basic|imodbits_horse_good,[]],
["rohirrim_courser","Rohirrim_Courser",[("rohan_horse01",0)],itp_type_horse|itp_shop,0,700,hit_points(90)|body_armor(12)|difficulty(2)|horse_speed(46)|horse_maneuver(40)|horse_charge(29)|horse_scale(100)|abundance(91),imodbits_horse_basic|imodbits_horse_basic,[]],
["rohirrim_hunter","Rohirrim_Hunter",[("rohan_horse02",0)],itp_type_horse|itp_shop,0,1150,hit_points(120)|body_armor(18)|difficulty(3)|horse_speed(42)|horse_maneuver(39)|horse_charge(34)|horse_scale(100)|abundance(92),imodbits_horse_basic|imodbits_horse_basic,[]],
["rohirrim_courser2","Rohirrim_Armoured_Courser",[("rohan_horse03b",0)],itp_type_horse|itp_shop,0,1150,hit_points(110)|body_armor(28)|difficulty(3)|horse_speed(42)|horse_maneuver(40)|horse_charge(31)|horse_scale(100)|abundance(95),imodbits_horse_basic|imodbits_horse_basic,[]],
["rohan_warhorse","Rohirrim_Warhorse",[("rohan_warhorse01",0)],itp_type_horse|itp_shop,0,1700,hit_points(135)|body_armor(30)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(44)|horse_scale(100)|abundance(96),imodbits_horse_basic|imodbits_horse_good,[]],
["thengel_warhorse","Eorl_Warhorse",[("rohan_warhorse01",0),("rohan_warhorse02",imodbit_heavy)],itp_type_horse|itp_shop,0,1900,hit_points(135)|body_armor(35)|difficulty(4)|horse_speed(36)|horse_maneuver(36)|horse_charge(53)|horse_scale(105)|abundance(97),imodbits_horse_basic|imodbits_horse_good,[]],
["rhun_horse_a","Rhun_Horse",[("rhunhorselight1",0)],itp_type_horse|itp_shop,0,320,hit_points(70)|body_armor(10)|difficulty(2)|horse_speed(38)|horse_maneuver(39)|horse_charge(15)|horse_scale(100)|abundance(91),imodbits_horse_basic|imodbits_horse_basic,[]],
["rhun_horse_b","Rhun_Horse",[("rhunhorselight2",0)],itp_type_horse|itp_shop,0,320,hit_points(70)|body_armor(10)|difficulty(2)|horse_speed(38)|horse_maneuver(39)|horse_charge(15)|horse_scale(100)|abundance(91),imodbits_horse_basic|imodbits_horse_basic,[]],
["rhun_horse_d","Rhun_Horse",[("rhunhorselight4",0)],itp_type_horse|itp_shop,0,320,hit_points(70)|body_armor(10)|difficulty(2)|horse_speed(38)|horse_maneuver(39)|horse_charge(15)|horse_scale(100)|abundance(91),imodbits_horse_basic|imodbits_horse_basic,[]],
["rhun_horse_e","Rhun_Heavy_Horse",[("rhunhorseheav1",0)],itp_type_horse|itp_shop,0,1400,hit_points(130)|body_armor(30)|difficulty(3)|horse_speed(37)|horse_maneuver(38)|horse_charge(33)|horse_scale(108)|abundance(93),imodbits_horse_basic|imodbits_horse_basic,[]],
["rhun_horse_f","Rhun_Heavy_Horse",[("rhunhorseheav2",0)],itp_type_horse|itp_shop,0,1400,hit_points(130)|body_armor(30)|difficulty(3)|horse_speed(37)|horse_maneuver(38)|horse_charge(33)|horse_scale(108)|abundance(93),imodbits_horse_basic|imodbits_horse_basic,[]],
["rhun_horse_g","Rhun_Heavy_Horse",[("rhunhorseheav3",0)],itp_type_horse|itp_shop,0,2100,hit_points(160)|body_armor(35)|difficulty(4)|horse_speed(36)|horse_maneuver(36)|horse_charge(36)|horse_scale(112)|abundance(94),imodbits_horse_basic|imodbits_horse_basic,[]],
["rhun_horse_h","Rhun_Heavy_Horse",[("rhunhorseheav4",0)],itp_type_horse,0,2400,hit_points(160)|body_armor(37)|difficulty(4)|horse_speed(40)|horse_maneuver(38)|horse_charge(42)|horse_scale(115)|abundance(96),imodbits_horse_basic|imodbits_horse_basic,[]],
["dale_horse","Rhovanion_Horse",[("bry_rus_horse_ponyfied_2",0)],itp_type_horse|itp_shop,0,550,hit_points(90)|body_armor(16)|difficulty(2)|horse_speed(41)|horse_maneuver(35)|horse_charge(12)|horse_scale(92)|abundance(91),imodbits_horse_basic|imodbits_horse_basic,[]],
["dale_warhorse","Rhovanion_Warhorse",[("bry_rus_horse_ponyfied",0)],itp_type_horse|itp_shop,0,900,hit_points(110)|body_armor(24)|difficulty(3)|horse_speed(39)|horse_maneuver(32)|horse_charge(18)|horse_scale(97)|abundance(93),imodbits_horse_basic|imodbits_horse_basic,[]],
["riv_warhorse","Rivendell Warhorse",[("rivendell_warhorse01",0)],itp_type_horse|itp_shop,0,1500,hit_points(135)|body_armor(32)|difficulty(4)|horse_speed(39)|horse_maneuver(38)|horse_charge(24)|horse_scale(102)|abundance(95),imodbits_horse_basic|imodbits_horse_good,[]],
["riv_warhorse2","Imladris Steed",[("rivendell_warhorse02",0)],itp_type_horse|itp_unique,0,2100,hit_points(150)|body_armor(38)|difficulty(4)|horse_speed(43)|horse_maneuver(40)|horse_charge(26)|horse_scale(104)|abundance(100),imodbits_horse_basic|imodbits_horse_good,[]],
["mordor_warhorse","Mordor_Warhorse",[("mordor_warhorse01",0)],itp_type_horse|itp_shop,0,1700,hit_points(135)|body_armor(35)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(33)|horse_scale(108)|abundance(94),imodbits_horse_basic|imodbits_horse_basic,[]],
["mordor_warhorse2","Mordor_Sinister_Warhorse",[("mordor_warhorse02",0)],itp_type_horse|itp_unique,0,3000,hit_points(150)|body_armor(60)|difficulty(4)|horse_speed(33)|horse_maneuver(30)|horse_charge(50)|horse_scale(118)|abundance(100),imodbits_horse_basic|imodbits_horse_good,[]],
["gondor_courser","Gondor_Courser",[("gondor_horse02",0)],itp_type_horse|itp_shop,0,470,hit_points(80)|body_armor(16)|difficulty(2)|horse_speed(43)|horse_maneuver(37)|horse_charge(10)|horse_scale(102)|abundance(91),imodbits_horse_basic|imodbits_horse_basic,[]],
["gondor_hunter","Gondor_Hunter",[("gondor_horse01",0)],itp_type_horse|itp_shop,0,760,hit_points(100)|body_armor(21)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(18)|horse_scale(104)|abundance(92),imodbits_horse_basic|imodbits_horse_basic,[]],
["dol_amroth_warhorse","Dol_Amroth_Warhorse",[("da_warhorse02",0)],itp_type_horse|itp_shop,0,1800,hit_points(140)|body_armor(35)|difficulty(4)|horse_speed(35)|horse_maneuver(33)|horse_charge(36)|horse_scale(110)|abundance(95),imodbits_horse_basic|imodbits_horse_good,[]],
["dol_amroth_warhorse2","Dol_Amroth_Heavy_Warhorse",[("da_warhorse01",0)],itp_type_horse|itp_shop,0,2200,hit_points(140)|body_armor(48)|difficulty(4)|horse_speed(35)|horse_maneuver(31)|horse_charge(41)|horse_scale(112)|abundance(96),imodbits_horse_basic|imodbits_horse_good,[]],
["gondor_warhorse","Gondor_Warhorse",[("gondor_warhorse01",0),("gondor_warhorse02",imodbit_heavy)],itp_type_horse|itp_shop,0,1800,hit_points(135)|body_armor(42)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(33)|horse_scale(108)|abundance(95),imodbits_horse_basic|imodbits_horse_good,[]],
["gondor_lam_horse","Lamedon_Armored_Horse",[("lam_warhorse01",0)],itp_type_horse|itp_shop,0,1500,hit_points(135)|body_armor(35)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(26)|horse_scale(102)|abundance(94),imodbits_horse_basic|imodbits_horse_basic,[]],
["lorien_warhorse","Lothlorien_Warhorse",[("loth_warhorse01",0)],itp_type_horse|itp_shop,0,1700,hit_points(135)|body_armor(40)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(28)|horse_scale(100)|abundance(94),imodbits_horse_basic|imodbits_horse_good,[]],
["harad_horse","Harad_Horse",[("harad_horse01",0)],itp_type_horse|itp_shop,0,450,hit_points(80)|body_armor(10)|difficulty(2)|horse_speed(40)|horse_maneuver(49)|horse_charge(10)|horse_scale(95)|abundance(91),imodbits_horse_basic|imodbits_horse_basic,[]],
["harad_warhorse","Harad_Warhorse",[("harad_horse02",0)],itp_type_horse|itp_shop,0,1500,hit_points(135)|body_armor(31)|difficulty(4)|horse_speed(38)|horse_maneuver(36)|horse_charge(23)|horse_scale(96)|abundance(95),imodbits_horse_basic|imodbits_horse_basic,[]],
["variag_pony","Variag_Pony",[("steppe_horse",0)],itp_type_horse|itp_shop,0,350,hit_points(70)|body_armor(10)|difficulty(2)|horse_speed(39)|horse_maneuver(40)|horse_charge(10)|horse_scale(95)|abundance(90),imodbits_horse_basic|imodbits_horse_basic,[]],
["variag_kataphrakt","Easterling_Warhorse",[("easterling_warhorse01",0)],itp_type_horse|itp_shop,0,2000,hit_points(135)|body_armor(48)|difficulty(4)|horse_speed(35)|horse_maneuver(31)|horse_charge(40)|horse_scale(102)|abundance(95),imodbits_horse_basic|imodbits_horse_basic,[]],

#########WARGS#########
#first non-horse / first warg in list: warg_1b (see in module_constants)
["warg_1b","Warg",[("warg_1B",0)],itp_type_horse|itp_shop,0,600,hit_points(80)|body_armor(10)|difficulty(2)|horse_speed(36)|horse_maneuver(64)|horse_charge(35)|horse_scale(95)|abundance(90),imodbits_horse_basic|imodbits_warg,[]],
["warg_1c","Warg",[("warg_1C",0)],itp_type_horse|itp_shop,0,600,hit_points(80)|body_armor(10)|difficulty(2)|horse_speed(36)|horse_maneuver(64)|horse_charge(35)|horse_scale(95)|abundance(90),imodbits_horse_basic|imodbits_warg,[]],
["warg_1d","Warg",[("warg_1D",0)],itp_type_horse|itp_shop,0,600,hit_points(80)|body_armor(10)|difficulty(2)|horse_speed(36)|horse_maneuver(64)|horse_charge(35)|horse_scale(95)|abundance(90),imodbits_horse_basic|imodbits_warg,[]],
["wargarmored_1b","Armored_Warg",[("wargArmored_1B",0)],itp_type_horse|itp_shop,0,1200,hit_points(100)|body_armor(25)|difficulty(4)|horse_speed(33)|horse_maneuver(61)|horse_charge(38)|horse_scale(95)|abundance(92),imodbits_horse_basic|imodbits_warg,[]],
["wargarmored_1c","Armored_Warg",[("wargArmored_1C",0)],itp_type_horse|itp_shop,0,1200,hit_points(100)|body_armor(25)|difficulty(4)|horse_speed(33)|horse_maneuver(61)|horse_charge(38)|horse_scale(95)|abundance(92),imodbits_horse_basic|imodbits_warg,[]],
["wargarmored_2b","Armored_Warg",[("wargArmored_2B",0)],itp_type_horse|itp_shop,0,1500,hit_points(110)|body_armor(30)|difficulty(4)|horse_speed(33)|horse_maneuver(61)|horse_charge(40)|horse_scale(95)|abundance(93),imodbits_horse_basic|imodbits_warg,[]],
["wargarmored_2c","Armored_Warg",[("wargArmored_2C",0)],itp_type_horse|itp_shop,0,1600,hit_points(120)|body_armor(30)|difficulty(4)|horse_speed(33)|horse_maneuver(61)|horse_charge(40)|horse_scale(95)|abundance(94),imodbits_horse_basic|imodbits_warg,[]],
["wargarmored_3a","Armored_Warg",[("wargArmored_3A",0)],itp_type_horse|itp_shop,0,2000,hit_points(130)|body_armor(35)|difficulty(5)|horse_speed(33)|horse_maneuver(60)|horse_charge(45)|horse_scale(95)|abundance(95),imodbits_horse_basic|imodbits_warg,[]],
["warg_reward","Huge_Warg",[("wargArmored_huge",0)],itp_type_horse,0,3000,hit_points(180)|body_armor(45)|difficulty(5)|horse_speed(35)|horse_maneuver(62)|horse_charge(62)|horse_scale(100)|abundance(100),imodbits_horse_basic,[]],
#first non WARG item: itm_warg_reward+1

["animal_big","Big_Animal", [("bry_cow_a",0),("bry_cow_b",imodbit_cracked),("bry_cow_c",imodbit_rusty),("bry_cow_d",imodbit_bent),("CWE_cow_mod_a",imodbit_chipped),("bry_wild_donkey",imodbit_rotten),("spak_yak1",imodbit_smelling),("spak_yak2",imodbit_large_bag)],itp_disable_agent_sounds, 0, 10,abundance(10)|hit_points(25)|body_armor(0)|difficulty(10)|horse_speed(5)|horse_maneuver(5)|horse_charge(0)|horse_scale(90),imodbits_horse_basic],
["animal_small","Small_Animal", [("bry_goat",0),("bry_goat_c",imodbit_cracked),("CWE_sheep_mod_a",imodbit_rusty),("CWE_sheep_mod_b",imodbit_bent),("wolf_dog",imodbit_chipped)],		itp_disable_agent_sounds, 0, 10,abundance(10)|hit_points(25)|body_armor(0)|difficulty(10)|horse_speed(5)|horse_maneuver(5)|horse_charge(0)|horse_scale(60),imodbits_horse_basic],

#Troll weapons
["troll_weapon_long","Giant_Halberd",[("isengard_halberd_troll",0),],																																		itp_no_pick_up_from_ground|itp_type_polearm|itp_no_blur|itp_two_handed|itp_primary|itp_crush_through|itp_bonus_against_shield|itp_can_penetrate_shield,itcf_overswing_polearm|0,1,													weight(250)|difficulty(0)|spd_rtng(70)|weapon_length(200)|swing_damage(30,blunt)|thrust_damage(30,blunt)|horse_speed(70),0,[]],
["troll_weapon_dmg","Giant_Mace",[("0",imodbit_cracked),("orc_sledgehammer_troll",imodbit_bent),("giant_mace",imodbit_plain),("giant_hammer",imodbit_strong)],																itp_no_pick_up_from_ground|itp_type_two_handed_wpn|itp_primary|itp_crush_through|itp_bonus_against_shield|itp_can_penetrate_shield,itc_troll_attack|0,1,									weight(250)|difficulty(0)|spd_rtng(85)|weapon_length(110)|swing_damage(30,blunt)|thrust_damage(30,blunt)|horse_speed(50),0,[]],
["tree_trunk_club_a","Tree_Trunk",[("0",0),("bone_cudgel_troll",imodbit_crude),("troll_club",imodbit_bent),("tree_trunk_club",imodbit_fine),("orc_club_a_troll",imodbit_heavy),("giant_mace_b",imodbit_strong)],itp_no_pick_up_from_ground|itp_type_two_handed_wpn|itp_primary|itp_wooden_parry|itp_wooden_attack|itp_crush_through|itp_can_penetrate_shield|itp_bonus_against_shield,itc_troll_attack|0,1,	weight(250)|difficulty(0)|spd_rtng(70)|weapon_length(130)|swing_damage(25,blunt)|thrust_damage(25,blunt)|horse_speed(100),0, []],

["troll_aoe","troll_aoe",[("0",0),],itp_no_pick_up_from_ground|itp_type_two_handed_wpn|itp_primary|itp_crush_through|itp_bonus_against_shield|itp_can_penetrate_shield,itc_troll_attack|0,1,									weight(250)|difficulty(0)|spd_rtng(90)|weapon_length(110)|swing_damage(1,blunt)|thrust_damage(1,blunt)|horse_speed(0),0,[]],

["free_2_handed_axe","Northmen_Longaxe",[("2_handed_axe",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,700,weight(8)|difficulty(10)|spd_rtng(82)|weapon_length(110)|swing_damage(47,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
# ["tree_trunk_club_b","Tree_Trunk",[("tree_trunk_club",0)],itp_no_pick_up_from_ground|itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_wooden_attack,itc_big_weapon|0,1,weight(250)|difficulty(0)|spd_rtng(92)|weapon_length(175)|swing_damage(48,cut)|thrust_damage(48,cut),0],
# ["tree_trunk_invis","Tree_Trunk",[("0",0)],itp_no_pick_up_from_ground|itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_wooden_attack,itc_big_weapon|0,1,weight(250)|difficulty(0)|spd_rtng(92)|weapon_length(175)|swing_damage(48,cut)|thrust_damage(48,cut),0],
["free_giant_hammer","Giant_Hammer",[("giant_hammer",0)],itp_no_pick_up_from_ground|itp_type_one_handed_wpn|itp_primary|0,itc_big_weapon|0,1,weight(250)|difficulty(0)|spd_rtng(96)|weapon_length(150)|swing_damage(80,cut)|thrust_damage(65,cut),0],
["giant_mace","Giant_Mace",[("giant_mace",0),("giant_hammer",imodbit_poor),("giant_mace_b",imodbit_old)],itp_no_pick_up_from_ground|itp_type_two_handed_wpn|itp_primary|itp_crush_through|itp_bonus_against_shield|itp_can_penetrate_shield,itc_troll_attack|0,1,weight(250)|difficulty(0)|spd_rtng(80)|weapon_length(130)|swing_damage(30,blunt)|thrust_damage(30,blunt),0,[]],
["troll_shield_a","Troll_Shield",[("troll_shield_a",0),("troll_shield_b",imodbit_poor)],itp_type_shield|itp_no_pick_up_from_ground|itp_wooden_parry|itp_unique,itcf_carry_round_shield,100,weight(50)|difficulty(0)|hit_points(500)|body_armor(10)|spd_rtng(96)|weapon_length(60),imodbits_shield,],
#
["free_olog_feet_boots","Olog_Hai_Feet",[("olog_feet",0)],itp_no_pick_up_from_ground|itp_type_foot_armor|itp_unique,0,1,weight(250)|head_armor(0)|body_armor(0)|leg_armor(62)|difficulty(70),0],
["free_olog_head_helm","Olog_Hai_Head",[("olog_head",0)],itp_no_pick_up_from_ground|itp_type_head_armor|itp_unique,0,1,weight(250)|head_armor(62)|difficulty(70),0],
["free_olog_head_helm_b","Olog_Hai_Head",[("olog_head_b",0)],itp_no_pick_up_from_ground|itp_type_head_armor|itp_unique,0,1,weight(250)|head_armor(62)|difficulty(70),0],
["free_olog_head_helm_c","Olog_Hai_Head",[("olog_head_c",0)],itp_no_pick_up_from_ground|itp_type_head_armor|itp_unique,0,1,weight(250)|head_armor(62)|difficulty(70),0],
["free_olog_body","Olog_Hai_Armor",[("olog_body",0),("olog_body",imodbit_rusty),("olog_body_b",imodbit_tattered)],itp_no_pick_up_from_ground|itp_type_body_armor|itp_covers_legs|itp_unique,0,1,weight(250)|head_armor(0)|body_armor(62)|leg_armor(0)|difficulty(70),0,],
["free_olog_body_b","Olog_Hai_Armor",[("olog_body_b",0)],itp_no_pick_up_from_ground|itp_type_body_armor|itp_covers_legs|itp_unique,0,1,weight(250)|head_armor(0)|body_armor(62)|leg_armor(0)|difficulty(70),0,],
["free_olog_hands","Olog_Hai_Hands",[("olog_hand_L",0)],itp_no_pick_up_from_ground|itp_type_hand_armor|itp_unique,0,1,weight(250)|body_armor(1)|difficulty(70),0],
#
# warg ghost items...  (mtarini)
#  invisible items which are used for ghost riders (riding unmounted wargs)
["warg_ghost_armour","HIDEME_armour" ,[("dummy_mesh_skinned",0)],itp_unique|itp_no_pick_up_from_ground|itp_type_body_armor|itp_covers_head|itp_covers_legs,0,0,weight(0)|head_armor(200)|body_armor(200)|leg_armor(200)|difficulty(0),0],
["warg_ghost_lance" ,"HIDEME_lance"  ,[("0",0)],itp_unique|itp_no_pick_up_from_ground|itp_type_polearm|itp_no_blur|itp_primary|itp_no_parry,0,0,weight(1)|difficulty(0)|spd_rtng(100)|weapon_length(1)|thrust_damage(0,pierce),imodbits_none],
# CC: ghost lance had itcf_thrust_onehanded_lance_horseback before, changed to prevent animals from couching
# other HIDEME items already ingame

#BOW MISSILES
["arrows","Arrows",[("plain_arrow",0),("plain_arrow_flying",ixmesh_flying_ammo),("common_quiver",ixmesh_carry)],itp_type_arrows|itp_shop,itcf_carry_quiver_front_right,72,weight(3)|thrust_damage(1,cut)|max_ammo(30)|weapon_length(95),imodbits_missile,[]],
["gondor_arrows","Gondor_Arrows",[("gondor_arrow",0),("gondor_arrow_flying",ixmesh_flying_ammo),("gondor_quiver",ixmesh_carry)],itp_type_arrows|itp_shop,itcf_carry_quiver_front_right,100,weight(3)|thrust_damage(2,cut)|max_ammo(30)|weapon_length(95),imodbits_missile,[]],
["orc_javelin","Orc_Heavy_Javelin",[("orc_javelin",0),("orc_javelin_quiver", ixmesh_carry),("orc_javelin_quiver", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn,400,weight(5)|difficulty(1)|shoot_speed(30)|spd_rtng(89)|weapon_length(88)|thrust_damage(37,pierce)|accuracy(83)|max_ammo(3),imodbits_thrown,[] ],
["khergit_arrows","Rohirrim_Arrows",[("rohan_arrow1",0),("rohan_arrow1_flying",ixmesh_flying_ammo),("rohan_quiver2",ixmesh_carry)],itp_type_arrows|itp_shop,itcf_carry_quiver_front_right,300,weight(3.5)|thrust_damage(2,cut)|max_ammo(30)|weapon_length(95),imodbits_missile,[]],
#unused:
["free_rohan_arrows_2","Rohirrim_Arrows",[("rohan_arrow1",0),("rohan_arrow1_flying",ixmesh_flying_ammo),("rohan_quiver2",ixmesh_carry)],itp_type_arrows|itp_shop,itcf_carry_quiver_front_right,300,weight(3.5)|thrust_damage(2,cut)|max_ammo(30)|weapon_length(95),imodbits_missile,[]],
["harad_arrows","Haradrim_Arrows",[("harad_arrow",0),("harad_arrow_flying",ixmesh_flying_ammo),("harad_quiver",ixmesh_carry)],itp_type_arrows|itp_shop,itcf_carry_quiver_front_right,300,weight(3)|thrust_damage(1,cut)|max_ammo(30)|weapon_length(95),imodbits_missile,[]],
["corsair_arrows","Corsair_Arrows",[("corsair_arrow",0),("corsair_arrow_flying",ixmesh_flying_ammo),("corsair_quiver",ixmesh_carry)],itp_type_arrows|itp_shop,itcf_carry_quiver_front_right,300,weight(3)|thrust_damage(1,cut)|max_ammo(29)|weapon_length(91),imodbits_missile,[]],
["ithilien_arrows","Ithilien_Arrows",[("ilithien_arrow",0),("ilithien_arrow_flying",ixmesh_flying_ammo),("ithilien_quiver",ixmesh_carry)],itp_type_arrows|itp_shop,itcf_carry_quiver_back_right,500,weight(3)|thrust_damage(3,cut)|max_ammo(29)|weapon_length(91),imodbits_good_missile,[]],
["woodelf_arrows","Woodelf_Arrows",[("mirkwood_arrow",0),("mirkwood_arrow_flying",ixmesh_flying_ammo),("mirkwood_quiver_new",ixmesh_carry)],itp_type_arrows|itp_shop,itcf_carry_quiver_back,500,weight(3)|thrust_damage(4,pierce)|max_ammo(29)|weapon_length(91),imodbits_good_missile,[]],
["elven_arrows","Elven_Arrows",[("white_elf_arrow",0),("white_elf_arrow_flying",ixmesh_flying_ammo),("lothlorien_quiver",ixmesh_carry)],itp_type_arrows|itp_shop,itcf_carry_quiver_back,500,weight(3)|thrust_damage(4,pierce)|max_ammo(29)|weapon_length(91),imodbits_good_missile,[]],
["orc_hook_arrow","Orc_Hook_Arrows",[("orc_hook_arrow",0),("orc_hook_arrow_flying",ixmesh_flying_ammo),("orc_quiver",ixmesh_carry)],itp_type_arrows|itp_shop,itcf_carry_quiver_back_right,100,weight(3)|thrust_damage(0,pierce)|max_ammo(30)|weapon_length(95),imodbits_missile,[]],
["isengard_arrow","Isengard_Arrows",[("isengard_arrow",0),("isengard_arrow_flying",ixmesh_flying_ammo),("isengard_quiver",ixmesh_carry)],itp_type_arrows|itp_shop,itcf_carry_quiver_back_right,200,weight(3)|thrust_damage(1,pierce)|max_ammo(30)|weapon_length(95),imodbits_missile,[]],
#free Jan 2017
["free_pilgrim_disguise","Pilgrim_Disguise",[("tld_robe_generic_dress",0)],itp_type_body_armor|itp_covers_legs|itp_civilian|itp_shop,0,25,weight(2)|head_armor(0)|body_armor(14)|leg_armor(8)|difficulty(0),imodbits_cloth,[]],

###ARMOR
#handwear, boots
["leather_gloves","Leather_Gloves",[("CWE_gloves_a_L",imodbits_armor_bad),("CWE_gloves_a_h_L",0),("narf_leather_gauntlet_L",imodbits_armor_good), ("undeadtest_handL",imodbit_poor)],itp_type_hand_armor|itp_shop,0,150,weight(0.2)|body_armor(2)|difficulty(0),imodbits_armor,[]],
["mail_mittens","Mail_Mittens",[("CWE_gauntlets_crysader_L",0)],itp_type_hand_armor|itp_shop,0,600,weight(1)|body_armor(4)|difficulty(0),imodbits_armor|imodbit_lordly,[]],
["leather_boots","Leather_Boots",[("fi_boot13",imodbits_armor_bad),("fi_boot8",0)],itp_type_foot_armor|itp_shop,0,300,weight(2)|abundance(90)|leg_armor(12)|difficulty(0),imodbits_cloth],
["leather_boots_dark","Rider_Boots",[("fi_boot7",imodbits_armor_bad),("narf_rus_cav_boots",0)],itp_type_foot_armor|itp_shop,0,450,weight(3)|abundance(90)|leg_armor(14)|difficulty(0),imodbits_cloth],
["splinted_greaves","Splinted_Greaves",[("fi_boot9",0),("narf_rus_splint_greaves",imodbits_armor_good)],itp_type_foot_armor|itp_shop,0,1300,weight(8)|abundance(94)|leg_armor(24)|difficulty(12),imodbits_armor|imodbit_lordly],

# TLD civilian wear
#all marked civilian items free Jan 2017, -> itm_white_tunic_a
["white_tunic_a","Civilian_Outfit",
    [("gondor_tunic_b",0),("gondor_dress_a",imodbit_poor),("gondor_dress_b",imodbit_old),("generic_tunic_c",imodbit_cheap),("dale_tunic",imodbit_well_made),("rohan_tunic",imodbit_sharp),
    ("smith_leather_apron",imodbit_deadly),("generic_leather_jerkin",imodbit_exquisite),("dale_coat",imodbit_powerful),("rohan_dress",imodbit_rough),("tld_robe_generic_dress",imodbit_fresh),
    ("L_roh_shirt_M1",imodbit_two_day_old),("L_roh_long_shirt_cape_M4",imodbit_smelling),("generic_tunic_a",imodbit_day_old),("rohan_fine_outfit_dale_dress",imodbit_rotten),("gondor_fine_outfit_dress",imodbit_large_bag),],
    itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(6)|leg_armor(1)|difficulty(0),imodbits_cloth,[]],
 ] + (is_a_wb_item==1 and [
["rohan_shoes","Leather_Shoes",[("ankle_boots_a_new",imodbits_armor_bad),("narf_rus_shoes",0),("fi_boot14",imodbit_fine)],itp_type_foot_armor|itp_shop|itp_attach_armature|itp_civilian,0,80,weight(1)|abundance(90)|leg_armor(8)|difficulty(0),imodbits_cloth],
        ] or [
        ["rohan_shoes","Leather_Shoes",[("fi_boot14",imodbits_armor_bad),("narf_rus_shoes",0)],itp_type_foot_armor|itp_shop|itp_attach_armature|itp_civilian,0,80,weight(1)|abundance(90)|leg_armor(8)|difficulty(0),imodbits_cloth],
        ]) + [ 
["furry_boots","Furry_Boots",[("furry_boots",0)],itp_type_foot_armor|itp_shop,0,200,weight(2)|abundance(90)|leg_armor(10)|difficulty(0),imodbits_orc_cloth],
["free_blue_tunic","Blue_Tunic",[("dale_tunic",0)],itp_type_body_armor|itp_covers_legs|itp_civilian|itp_shop,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["black_tunic","Black_Tunic",[("gondor_tunic",0)],itp_type_body_armor|itp_covers_legs|itp_civilian|itp_shop,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["hood_black","Black_Hood",[("fi_helm10_black",0),("hood_black_simple",imodbits_armor_bad),("fi_helm10_black_mask",imodbits_armor_good),("gondor_wimple_a",imodbit_smelling),("gondor_wimple_b",imodbit_rotten),("gondor_fine_fem_hat",imodbit_large_bag)],itp_type_head_armor|itp_shop|itp_fit_to_head|itp_civilian,0,100,weight(1)|head_armor(12)|difficulty(0),imodbits_armor,[]],
["hood_green","Green_Hood",[("fi_helm10_green",0),("hood_green_simple",imodbits_armor_bad),("fi_helm10_green_mask",imodbits_armor_good)],itp_type_head_armor|itp_shop|itp_fit_to_head|itp_civilian,0,120,weight(1)|head_armor(14)|difficulty(0),imodbits_armor,[]],
["hood_grey","Grey_Hood",[("fi_helm10_grey",0),("hood_grey_simple",imodbits_armor_bad),("hood_grey_large",imodbits_armor_good)],itp_type_head_armor|itp_shop|itp_fit_to_head|itp_civilian,0,80,weight(1)|head_armor(11)|difficulty(0),imodbits_armor,[]],
["hood_leather","Leather_Hood",[("fi_helm10_leather",0),("hood_leather_simple",imodbits_armor_bad),("fi_helm10_leather_mask",imodbits_armor_good)],itp_type_head_armor|itp_shop|itp_fit_to_head|itp_civilian,0,250,weight(1)|head_armor(15)|difficulty(0),imodbits_armor,[]],
["mail_coif","Mail_Coif",[("maci_mail_coif",0),("crusader_koif_a",imodbits_armor_good)],itp_type_head_armor|itp_shop|itp_fit_to_head,0,250,weight(2)|head_armor(22)|difficulty(0),imodbits_armor,[]],
["free_green_dress","Green_Dress",[("rohan_dress",0)],itp_type_body_armor|itp_covers_legs|itp_civilian|itp_shop,0,500,weight(6)|head_armor(0)|body_armor(10)|leg_armor(6)|difficulty(0),imodbits_cloth,[]],
["free_tld_tunic","Tunic",[("tld_tunic",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]], #InVain: Removed script (ti_on_init_item,[(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_initialize_civilian_clothes", "tableau_tld_tunic", ":agent_no", ":troop_no")])

#Common Weapons
["axe_a","Northmen_Axe",[("axe_a",0),("axe_a_carry",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,250,weight(2)|abundance(90)|difficulty(0)|spd_rtng(105)|weapon_length(45)|swing_damage(25,cut)|thrust_damage(0,pierce),imodbits_weapon],
["axe_b","Northmen_Bearded_Axe",[("axe_b",0),("axe_b_carry",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,250,weight(2)|abundance(90)|difficulty(0)|spd_rtng(98)|weapon_length(47)|swing_damage(27,cut)|thrust_damage(0,pierce),imodbits_weapon],
["axe_c","Northmen_Axe",[("axe_c",0),("axe_c_carry",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,290,weight(2)|abundance(90)|difficulty(0)|spd_rtng(96)|weapon_length(57)|swing_damage(29,cut)|thrust_damage(0,pierce),imodbits_weapon],
["axe_d","Northmen_Axe",[("axe_d",0),("axe_d_carry",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,300,weight(2)|abundance(90)|difficulty(0)|spd_rtng(94)|weapon_length(60)|swing_damage(31,cut)|thrust_damage(0,pierce),imodbits_weapon],
["long_bearded_axe","Northmen_Bearded_Longaxe",[("long_bearded_axe",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,500,weight(7)|abundance(92)|difficulty(14)|spd_rtng(84)|weapon_length(106)|swing_damage(45,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
["2_handed_axe","Northmen_Longaxe",[("2_handed_axe",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,550,weight(8)|abundance(93)|difficulty(16)|spd_rtng(82)|weapon_length(110)|swing_damage(47,cut)|thrust_damage(0,pierce),imodbits_weapon_good],

["shortened_spear","Shortened_Spear",[("spear_g_1-9m",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry,itc_spear_upstab,100,weight(2)|abundance(90)|difficulty(0)|spd_rtng(102)|weapon_length(120)|thrust_damage(25,pierce)|swing_damage(19,blunt),imodbits_weapon_wood,[]],
["spear","Spear",[("spear_h_2-15m",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry,itc_spear_upstab,250,weight(2.25)|abundance(90)|difficulty(0)|spd_rtng(98)|weapon_length(135)|thrust_damage(26,pierce)|swing_damage(20,blunt),imodbits_weapon_wood,[]],
["light_lance","Light_Lance",[("spear_b_2-75m",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable,itc_lance_upstab,400,weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(90)|weapon_length(175)|thrust_damage(27,pierce),imodbits_weapon_wood,[]],
["lance","Lance",[("spear_d_2-8m",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable,itc_pike,400,weight(2.5)|abundance(91)|difficulty(0)|spd_rtng(88)|weapon_length(180)|thrust_damage(26,pierce),imodbits_weapon_wood,[]],

###SHIELDS
["tab_shield_small_round_b","Round_Cavalry_Shield",[("tableau_shield_small_round_1",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(2)|abundance(90)|difficulty(0)|hit_points(200)|body_armor(13)|spd_rtng(98)|weapon_length(33),imodbits_shield,[(ti_on_init_item,[(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_shield_item_set_banner", "tableau_small_round_shield_1", ":agent_no", ":troop_no")])]],

#RANGED
["short_bow","Short_Bow",[("small_bow",0),("small_bow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop,itcf_shoot_bow|itcf_carry_bow_back,50,weight(1)|difficulty(0)|shoot_speed(46)|spd_rtng(99)|thrust_damage(23,cut)|accuracy(86),imodbits_bow,[] ],
["regular_bow","Bow",[("regular_bow",0),("regular_bow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop|itp_cant_use_on_horseback,itcf_shoot_bow|itcf_carry_bow_back,100,weight(1)|difficulty(1)|shoot_speed(52)|spd_rtng(98)|thrust_damage(26,cut)|accuracy(90),imodbits_bow,[] ],
["nomad_bow","Nomad_Bow",[("nomad_bow",0),("nomad_bow_case",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn,200,weight(1.3)|difficulty(2)|shoot_speed(48)|spd_rtng(96)|thrust_damage(24,cut)|accuracy(86),imodbits_bow,[] ],
["gondor_bow","Gondor_Bow",[("gondor_bow",0),("gondor_bow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_two_handed|itp_shop|itp_cant_use_on_horseback,itcf_shoot_bow|itcf_carry_bow_back,600,weight(1.8)|difficulty(3)|shoot_speed(57)|spd_rtng(82)|thrust_damage(30,cut)|accuracy(88),imodbits_bow,[] ],
["strong_bow","Strong_Bow",[("strong_bow",0),("strong_bow_case",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn,400,weight(1.3)|difficulty(3)|shoot_speed(52)|spd_rtng(94)|thrust_damage(26,cut)|accuracy(85),imodbits_bow,[] ],
["elven_bow","Elven_Bow",[("GA_BowE_Medium_B",0),("GA_BowE_Medium_B_Carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop|itp_cant_use_on_horseback,itcf_shoot_bow|itcf_carry_bow_back,1000,weight(1.5)|difficulty(3)|shoot_speed(65)|spd_rtng(93)|thrust_damage(20,pierce)|accuracy(93),imodbits_good_bow,[] ],
["corsair_bow","Corsair_Bow",[("corsair_bow",0),("corsair_bow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop|itp_cant_use_on_horseback,itcf_shoot_bow|itcf_carry_bow_back,900,weight(1.5)|difficulty(4)|shoot_speed(58)|spd_rtng(80)|thrust_damage(20,pierce)|accuracy(87),imodbits_bow,[] ],
["dwarf_horn_bow","Dwarf_Horn_Bow",[("dwarf_horn_bow",0),("dwarf_horn_bow",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop,itcf_shoot_bow|itcf_carry_bowcase_left,500,weight(1.3)|difficulty(3)|shoot_speed(56)|spd_rtng(84)|thrust_damage(28,cut)|accuracy(86),imodbits_good_bow,[] ],
["dwarf_short_bow","Dwarf_Short_Bow",[("dwarf_short_bow",0),("dwarf_short_bow",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop,itcf_shoot_bow|itcf_carry_bowcase_left,300,weight(1.3)|difficulty(1)|shoot_speed(53)|spd_rtng(86)|thrust_damage(25,cut)|accuracy(84),imodbits_bow,[] ],
["harad_bow","Harad_Curved_Bow",[("harad_bow",0),("harad_bow",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop,itcf_shoot_bow|itcf_carry_back,300,weight(1.3)|difficulty(1)|shoot_speed(56)|spd_rtng(95)|thrust_damage(23,cut)|accuracy(84),imodbits_bow,[] ],
["lg_bow","Eagle_Guard_Bow",[("lg_bow",0),("lg_bow",ixmesh_carry)],itp_type_bow|itp_primary|itp_two_handed|itp_shop|itp_cant_use_on_horseback,itcf_shoot_bow|itcf_carry_back,1100,weight(1.3)|difficulty(4)|shoot_speed(56)|spd_rtng(90)|thrust_damage(28,cut)|accuracy(93),imodbits_bow,[] ],
["riv_bow","Rivendell_Bow",[("rivendellbow",0),("rivendellbow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_two_handed|itp_shop|itp_cant_use_on_horseback,itcf_shoot_bow|itcf_carry_bow_back,1100,weight(1.8)|difficulty(3)|shoot_speed(65)|spd_rtng(88)|thrust_damage(23,pierce)|accuracy(90),imodbits_good_bow,[] ],
["rhun_bow","Balchoth_Bow",[("khazad_orc_bow_3",0),("khazad_orc_bow_3_case",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn,600,weight(1.3)|difficulty(3)|shoot_speed(52)|spd_rtng(96)|thrust_damage(26,cut)|accuracy(85),imodbits_bow,[] ],
["lorien_bow","Galadhrim_Bow",[("Elfbow",0),("Elfbow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop|itp_cant_use_on_horseback,itcf_shoot_bow|itcf_carry_bow_back,1300,weight(1.5)|difficulty(4)|shoot_speed(65)|spd_rtng(93)|thrust_damage(23,pierce)|accuracy(96),imodbits_good_bow,[] ],
["isengard_large_bow","Isengard_Large_Bow",[("isengard_large_bow",0),("isengard_large_bow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_two_handed|itp_shop|itp_cant_use_on_horseback,itcf_shoot_bow|itcf_carry_bow_back,800,weight(1.5)|difficulty(3)|shoot_speed(58)|spd_rtng(81)|thrust_damage(19,pierce)|accuracy(84),imodbits_bow,[] ],
["dale_bow","Dale_Bow",[("dale_bow",0),("dale_bow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_two_handed|itp_shop|itp_cant_use_on_horseback,itcf_shoot_bow|itcf_carry_bow_back,600,weight(1.5)|difficulty(4)|shoot_speed(64)|spd_rtng(93)|thrust_damage(27,cut)|accuracy(96),imodbits_bow,[] ],
["uruk_bow","Orc_Horn_Bow",[("khazad_orc_bow_2",0),("khazad_orc_bow_2_case",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn,500,weight(1.3)|difficulty(2)|shoot_speed(57)|spd_rtng(94)|thrust_damage(23,cut)|accuracy(84),imodbits_bow,[] ],
["mirkwood_bow","Mirkwood_Bow",[("mirkwood_bow",0),("mirkwood_bow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_shop|itp_cant_use_on_horseback,itcf_shoot_bow|itcf_carry_bow_back,1100,weight(1.5)|difficulty(4)|shoot_speed(65)|spd_rtng(95)|thrust_damage(21,pierce)|accuracy(93),imodbits_good_bow,[] ],

["dunland_javelin","Dunland_Javelins",[("dunland_javelin",0),("dunland_javelin_quiver", ixmesh_carry),("dunland_javelin_quiver", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn,200,weight(4)|difficulty(0)|shoot_speed(47)|spd_rtng(93)|weapon_length(65)|thrust_damage(35,cut)|accuracy(93)|max_ammo(5),imodbits_thrown,[] ],
["orc_throwing_arrow","Orc_Darts",[("orc_throwing_arrow",0),("orc_throwing_arrow_bag",ixmesh_carry),("orc_throwing_arrow_bag", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_javelin|itcf_carry_quiver_back_right|itcf_show_holster_when_drawn,200,weight(4)|difficulty(0)|shoot_speed(35)|spd_rtng(89)|weapon_length(65)|thrust_damage(29,cut)|accuracy(88)|max_ammo(6),imodbits_thrown,[] ],
["heavy_throwing_spear","Heavy_Throwing_Spear",[("rohan_throwing_spear",0),("rohan_throwing_spear_quiver", ixmesh_carry),("rohan_throwing_spear_quiver", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield|itp_can_penetrate_shield,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn,200,weight(4)|difficulty(2)|shoot_speed(27)|spd_rtng(82)|weapon_length(65)|thrust_damage(45,pierce)|accuracy(87)|max_ammo(3),imodbits_thrown,[] ],
["javelin","Javelin",[("javelin",0),("javelins_quiver",ixmesh_carry),("javelins_quiver", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn,200,weight(5)|difficulty(0)|shoot_speed(42)|spd_rtng(91)|weapon_length(75)|thrust_damage(28,pierce)|accuracy(91)|max_ammo(4),imodbits_thrown,[] ],
["harad_javelin","Harad_Javelin",[("harad_javelin",0),("harad_javelins_quiver",ixmesh_carry),("harad_javelins_quiver", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn,200,weight(4)|difficulty(0)|shoot_speed(40)|spd_rtng(89)|weapon_length(65)|thrust_damage(30,pierce)|accuracy(93)|max_ammo(4),imodbits_thrown,[] ],
["gondor_javelin","Gondor_Javelin",[("gondor_javelin",0),("jarid_quiver",ixmesh_carry)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn,200,weight(4)|difficulty(0)|shoot_speed(40)|spd_rtng(89)|weapon_length(65)|thrust_damage(32,pierce)|accuracy(91)|max_ammo(4),imodbits_thrown,[] ],
["rohirrim_throwing_axe","Northmen_Throwing_Axes",[("faradon_axe_c",0),("faradon_axe_c_quiver", ixmesh_carry),("faradon_axe_c_inventory", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_axe|itcf_carry_quiver_front_right|itcf_show_holster_when_drawn,300,weight(5)|difficulty(0)|shoot_speed(20)|spd_rtng(99)|weapon_length(53)|thrust_damage(53,cut)|accuracy(91)|max_ammo(3),imodbits_thrown,[] ],
["loss_throwing_axes","Lossarnach_Throwing_Axes",[("loss_throwing_axe",0),("loss_throwing_axe_quiver", ixmesh_carry),("loss_throwing_axe_inventory", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_axe|itcf_carry_quiver_front_right|itcf_show_holster_when_drawn,300,weight(5)|difficulty(0)|shoot_speed(20)|spd_rtng(99)|weapon_length(53)|thrust_damage(53,cut)|accuracy(92)|max_ammo(3),imodbits_thrown,[] ],

##########TLD ITEMS START##########
#####RIVENDELL/DUNEDAIN ITEMS##########
###ARNOR HELMS######## #free July 2023
["free_dunedain_helm_a","Arnor_Light_Helm",[("arnor_helm_a1",0)],itp_type_head_armor|itp_shop|itp_fit_to_head,0,300,weight(1)|head_armor(14)|difficulty(0),imodbits_elf_cloth,[]], #free July 2023
["free_dunedain_helm_b","Arnor_Helm",[("arnor_helm_b1",0)],itp_type_head_armor|itp_shop,0,1400,weight(6)|abundance(95)|head_armor(38)|body_armor(0)|difficulty(15),imodbits_elf_armor,[]], #free July 2023
["arnor_helm_c","Arnor_Decorated_Helm",[("arnor_helm_c1",imodbits_armor_bad),("arnor_helm_c2",imodbit_plain),("arnor_helm_c2",0),("arnor_helm_c3",imodbits_armor_good|imodbit_lordly)],itp_type_head_armor|itp_shop,0,1200,weight(4)|abundance(95)|head_armor(38)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly,[]],
["arnor_helm_b","Arnor_Helm",[("arnor_helm_b1",imodbits_armor_bad),("arnor_helm_b2",imodbit_plain),("arnor_helm_b2",0),("arnor_helm_b3",imodbits_armor_good|imodbit_lordly)],itp_type_head_armor|itp_shop,0,1000,weight(3)|abundance(93)|head_armor(35)|body_armor(0)|difficulty(13),imodbits_armor|imodbit_lordly,[]],
["arnor_helm_a","Arnor_Light_Helm",[("arnor_helm_a1",imodbits_armor_bad),("arnor_helm_a2",imodbit_plain),("arnor_helm_a2",0),("arnor_helm_a3",imodbits_armor_good|imodbit_lordly)],itp_type_head_armor|itp_shop,0,1000,weight(3)|abundance(92)|head_armor(32)|body_armor(0)|difficulty(12),imodbits_armor|imodbit_lordly,[]],

#free July 2023
["free_arnor_armor_a","Arnorian_Armor",[("arnor_armor_a1",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2300,weight(27)|abundance(92)|head_armor(0)|body_armor(35)|leg_armor(13)|difficulty(16),imodbits_armor|imodbit_lordly,[]], 

#ARNOR ARMORS########
["arnor_light_a","Dunedain_Ranger_Jerkin",[("arnor_leather_jerkin_1",imodbits_armor_bad),("arnor_leather_jerkin_2",imodbit_plain),("arnor_leather_jerkin_2",0),("arnor_leather_jerkin_2_cape",imodbit_cloak),("arnor_leather_jerkin_3",imodbits_armor_good),("arnor_leather_jerkin_3_cape",imodbit_reinforced|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,250,weight(5)|abundance(90)|head_armor(0)|body_armor(10)|leg_armor(6)|difficulty(0),imodbits_armor|imodbit_cloak,[]],
["arnor_light_b","Dunedain_Ranger_Mail",[("arnor_leather_mail_1",imodbits_armor_bad),("arnor_leather_mail_2",imodbit_plain),("arnor_leather_mail_1",0),("arnor_leather_mail_2_cape",imodbit_cloak),("arnor_leather_mail_3",imodbits_armor_good),("arnor_leather_mail_3_cape",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1000,weight(21)|abundance(92)|head_armor(0)|body_armor(24)|leg_armor(8)|difficulty(12),imodbits_armor|imodbit_lordly|imodbit_cloak,[]],
["arnor_med_a","Dunedain_Ranger_Coat",[("arnor_leather_light_1",imodbits_armor_bad),("arnor_leather_light_2",imodbit_plain),("arnor_leather_light_2",0),("arnor_leather_light_2_cape",imodbit_cloak),("arnor_leather_light_3",imodbits_armor_good),("arnor_leather_light_3_cape",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,700,weight(15)|abundance(91)|head_armor(0)|body_armor(18)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly|imodbit_cloak,[]],
["arnor_med_b","Dunedain_Mail",[("arnor_leather_heavy_1",imodbits_armor_bad),("arnor_leather_heavy_2",imodbit_plain),("arnor_leather_heavy_2",0),("arnor_leather_heavy_2_cape",imodbit_cloak),("arnor_leather_heavy_3",imodbits_armor_good),("arnor_leather_heavy_3_cape",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1700,weight(27)|abundance(94)|head_armor(0)|body_armor(32)|leg_armor(10)|difficulty(16),imodbits_armor|imodbit_lordly|imodbit_cloak,[]],
["arnor_heavy","Arnorian_High_Armor",[("arnor_armor_a1",imodbits_armor_bad),("arnor_armor_a2",imodbit_plain),("arnor_armor_a2",0),("arnor_armor_a2_cape",imodbit_cloak),("arnor_armor_a3",imodbits_armor_good),("arnor_armor_a3_cape",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,3000,weight(33)|abundance(95)|head_armor(0)|body_armor(40)|leg_armor(15)|difficulty(20),imodbits_armor|imodbit_lordly|imodbit_cloak,[]],

["arnor_greaves","Arnorian_Greaves",[("narf_splinted_greaves_nospurs",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,1800,weight(7)|abundance(94)|leg_armor(28)|difficulty(15),imodbits_armor|imodbit_lordly,[]],
["arnor_shield_c","Arnor_Cavalry_Shield",[("arnor_kite_shield_a",imodbits_armor_bad),("arnor_kite_shield_b",imodbit_plain),("arnor_kite_shield_b",0),("arnor_kite_shield_c",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(2)|abundance(93)|difficulty(3)|hit_points(340)|body_armor(19)|spd_rtng(82)|weapon_length(60),imodbits_shield_good,[]],
["arnor_shield_a","Arnor_Round_Shield",[("arnor_cav_shield",0),("arnor_cav_shield_b",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,400,weight(2)|abundance(91)|difficulty(1)|hit_points(300)|body_armor(15)|spd_rtng(90)|weapon_length(30),imodbits_shield_good,[]],

####ARNOR WEAPONS########
["arnor_sword_c","Arnor_War_Sword",[("arnor_sword_b",0),("arnor_sword_b_scab",ixmesh_carry)],itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_shop,itc_greatsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,700,weight(2.25)|abundance(93)|difficulty(13)|spd_rtng(102)|weapon_length(110)|swing_damage(37,cut)|thrust_damage(26,pierce),imodbits_weapon_good,[]],
["arnor_sword_a","Arnor_Bastard_Sword",[("arnor_sword_c",0),("arnor_sword_c_scab",ixmesh_carry)],itp_type_two_handed_wpn|itp_primary|itp_shop,itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,650,weight(2.25)|abundance(92)|difficulty(11)|spd_rtng(110)|weapon_length(101)|swing_damage(33,cut)|thrust_damage(26,pierce),imodbits_weapon_good,[]],
["arnor_sword_f","Arnor_Shortsword",[("arnor_sword_a",0),("arnor_sword_a_scab",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,300,weight(1.25)|abundance(90)|difficulty(0)|spd_rtng(107)|weapon_length(83)|swing_damage(28,cut)|thrust_damage(21,pierce),imodbits_weapon_good,[]],

#free July 2023
["free_arnor_sword_a","Arnor_Bastard_Sword",[("arnor_sword_c",0),("arnor_sword_c_scab",ixmesh_carry)],itp_type_two_handed_wpn|itp_primary|itp_shop,itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,650,weight(2.25)|abundance(92)|difficulty(11)|spd_rtng(110)|weapon_length(101)|swing_damage(33,cut)|thrust_damage(26,pierce),imodbits_weapon_good,[]],
["free_arnor_shield_c","Arnor_Cavalry_Shield",[("arnor_kite_shield_a",imodbits_armor_bad),("arnor_kite_shield_b",imodbit_plain),("arnor_kite_shield_b",0),("arnor_kite_shield_c",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(2)|abundance(93)|difficulty(3)|hit_points(340)|body_armor(19)|spd_rtng(82)|weapon_length(60),imodbits_shield_good,[]],
["free_arnor_sword_f","Arnor_Shortsword",[("arnor_sword_a",0),("arnor_sword_a_scab",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,300,weight(1.25)|abundance(90)|difficulty(0)|spd_rtng(107)|weapon_length(83)|swing_damage(28,cut)|thrust_damage(21,pierce),imodbits_weapon_good,[]],
#
#RIVENDELL HELMS##########
["riv_helm_a","Rivendell_Coif",[("rivendell_coif_new",0)],itp_type_head_armor,0,800,weight(1)|head_armor(24)|difficulty(0),imodbits_armor|imodbit_lordly,[]],
["riv_helm_b","Rivendell_Archer_Helm",[("rivendellarcherhelmet",0)],itp_type_head_armor|itp_shop,0,1200,weight(2)|abundance(93)|head_armor(35)|body_armor(0)|difficulty(12),imodbits_armor|imodbit_lordly,[]],
["riv_helm_c","Rivendell_Infantry_Helm",[("rivendellswordfighterhelmet",0)],itp_type_head_armor|itp_shop,0,1600,weight(3)|abundance(96)|head_armor(40)|body_armor(0)|difficulty(15),imodbits_elf_armor,[]],
#free Jan 2017, -> itm_witchking_helmet
["free_riv_helm_glorfi","Glorfi_Hair",[("glorfindelhair",0)],itp_no_pick_up_from_ground|itp_type_head_armor|itp_unique,0,3000,weight(1.2)|head_armor(70)|difficulty(0),0,[]],
["tiara_reward","Elf_Lord_Tiara",[("tiara",0)],itp_type_head_armor|itp_unique|itp_doesnt_cover_hair,0,3000,weight(0.5)|head_armor(10)|difficulty(0),0,[]],
##########RIVENDELL SHIELDS##########
["riv_shield_a","Rivendell_Shield",[("riv_inf_shield_b",0),("riv_inf_shield",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,700,weight(2.5)|abundance(91)|difficulty(3)|hit_points(340)|body_armor(16)|spd_rtng(85)|weapon_length(60),imodbits_shield_good,[]],
["riv_shield_b","Rivendell_Shield",[("riv_cav_shield_b",0),("riv_cav_shield",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,600,weight(2)|abundance(94)|difficulty(1)|hit_points(290)|body_armor(19)|spd_rtng(95)|weapon_length(40),imodbits_shield_good,[]],
#####RIVENDELL WEAPONS########
["riv_bas_sword","Rivendell_Bastard_Sword",[("rivendell_handandahalf1",0),("scab_rivendell_handandahalf1",ixmesh_carry)],itp_type_two_handed_wpn|itp_primary|itp_shop,itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,670,weight(2.25)|abundance(94)|difficulty(12)|spd_rtng(106)|weapon_length(105)|swing_damage(35,cut)|thrust_damage(26,pierce),imodbits_weapon_good,[]],
["riv_1h_sword","Rivendell_Sword",[("rivendellsword1",0),("scab_rivendell_sword1",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,500,weight(1.25)|abundance(92)|difficulty(0)|spd_rtng(103)|weapon_length(95)|swing_damage(28,cut)|thrust_damage(21,pierce),imodbits_weapon_good,[]],
["riv_riding_sword","Rivendell_Longsword",[("rivendelllongsword1",0),("scab_rivendelllongsword1",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,550,weight(2)|abundance(93)|difficulty(11)|spd_rtng(98)|weapon_length(103)|swing_damage(29,cut)|thrust_damage(21,pierce),imodbits_weapon_good,[]],
["riv_archer_sword","Rivendell_Short_Sword",[("rivendellshortsword1",0),("scab_rivendell_shortsword1",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,300,weight(1.25)|abundance(91)|difficulty(0)|spd_rtng(110)|weapon_length(80)|swing_damage(27,cut)|thrust_damage(23,pierce),imodbits_weapon_good,[]],
["riv_spear","Rivendell_Spear",[("riv_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_wooden_parry|itp_couchable,itc_spear_upstab|itcf_carry_spear,500,weight(2.25)|abundance(92)|difficulty(0)|spd_rtng(102)|weapon_length(171)|thrust_damage(30,pierce)|swing_damage(20,blunt),imodbits_weapon_good,[]],
########RIVENDELL ARMORS########
["riv_light","Rivendell_Tunic",[("riv_light",0),("riv_light_cloak",imodbit_cloak)],itp_type_body_armor|itp_covers_legs|itp_shop,0,100,weight(6)|head_armor(0)|body_armor(10)|leg_armor(6)|difficulty(0),imodbits_elf_cloth|imodbit_cloak,[]],
["riv_leather","Rivendell_Leather_Armor",[("riv_leather",0),("riv_leather_cloak",imodbit_cloak)],itp_type_body_armor|itp_covers_legs|itp_shop,0,250,weight(12)|head_armor(0)|body_armor(16)|leg_armor(6)|difficulty(0),imodbits_armor|imodbit_lordly|imodbit_cloak,[]],
["riv_foot_mail","Rivendell_Mail",[("riv_foot_mail_a",0),("riv_foot_mail_a",imodbit_plain),("riv_foot_mail_a_cloak",imodbit_cloak),("riv_foot_mail_b",imodbits_armor_good),("riv_foot_mail_b_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1200,weight(22)|abundance(92)|head_armor(0)|body_armor(28)|leg_armor(6)|difficulty(10),imodbits_armor|imodbit_lordly|imodbit_cloak,[]],
["riv_foot_scale","Rivendell_Scale",[("riv_foot_scale_a",0),("riv_foot_scale_a",imodbit_plain),("riv_foot_scale_a_cloak",imodbit_cloak),("riv_foot_scale_b",imodbits_armor_good),("riv_foot_scale_b_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2100,weight(28)|abundance(94)|head_armor(0)|body_armor(34)|leg_armor(12)|difficulty(15),imodbits_armor|imodbit_lordly|imodbit_cloak,[]],
["riv_surcoat","Rivendell_Surcoat",[("riv_surcoat_a",0),("riv_surcoat_a",imodbit_plain),("riv_surcoat_a_cloak",imodbit_cloak),("riv_surcoat_b",imodbits_armor_good),("riv_surcoat_b_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2000,weight(25)|abundance(93)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(11),imodbits_armor|imodbit_lordly|imodbit_cloak,[]],
["riv_knight","Rivendell_Knightly_Armour",[("riv_knight_a",0),("riv_knight_a",imodbit_plain),("riv_knight_a_cloak",imodbit_cloak),("riv_knight_b",imodbits_armor_good),("riv_knight_b_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,3200,weight(32)|abundance(95)|head_armor(0)|body_armor(38)|leg_armor(19)|difficulty(18),imodbits_elf_armor|imodbit_cloak,[]],
["riv_armor_h_archer","Rivendell_Armor",[("riv_foot_scale_a",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2700,weight(25)|abundance(96)|head_armor(0)|body_armor(36)|leg_armor(16)|difficulty(18),imodbits_armor|imodbit_lordly,[]],
["free_riv_armor_leader","Rivendell_Leader_Armor",[("riv_knight_b_cloak",0)],itp_type_body_armor|itp_covers_legs,0,3600,weight(28)|abundance(100)|head_armor(1)|body_armor(40)|leg_armor(20)|difficulty(20),imodbits_armor|imodbit_lordly,[]],
["riv_boots","Rivendell_Boots",[("rivendell_boots",0)],itp_type_foot_armor|itp_shop|itp_attach_armature|itp_civilian,0,1000,weight(2)|abundance(92)|leg_armor(20)|difficulty(0),imodbits_elf_cloth],

####GONDOR ITEMS##########
####ARMORS
["gon_footman","Gondor_Mail_Shirt",[("gondor_footman",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1100,weight(25)|abundance(91)|head_armor(0)|body_armor(25)|leg_armor(8)|difficulty(11),imodbits_armor|imodbit_lordly,[]],
["gon_jerkin","Gondor_Jerkin",[("gondor_jerkin",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,150,weight(7)|head_armor(0)|body_armor(12)|leg_armor(4)|difficulty(0),imodbits_elf_cloth,[]],
["gon_regular","Gondor_Heavy_Mail",[("gondor_regular",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1700,weight(29)|abundance(92)|head_armor(0)|body_armor(33)|leg_armor(8)|difficulty(15),imodbits_armor|imodbit_lordly,[]],
["gon_bowman","Gondor_Gambeson",[("gondor_bowman",0)],itp_type_body_armor|itp_covers_legs|itp_civilian|itp_shop,0,800,weight(12)|abundance(90)|head_armor(0)|body_armor(20)|leg_armor(8)|difficulty(8),imodbits_cloth,[]],
["gon_archer","Gondor_Gambeson_with_Cloak",[("gondor_archer",0)],itp_type_body_armor|itp_covers_legs|itp_civilian|itp_shop,0,1100,weight(13)|abundance(90)|head_armor(0)|body_armor(24)|leg_armor(9)|difficulty(8),imodbits_cloth,[]],
["gon_noble_cloak","Gondor_Noble's_Jerkin",[("gondor_noble_cloak",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,500,weight(10)|head_armor(0)|body_armor(18)|leg_armor(5)|difficulty(0),imodbits_elf_cloth,[]],
["gon_squire","Gondor_Mail_with_Cloak",[("gondor_squire",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1200,weight(26)|abundance(91)|head_armor(0)|body_armor(26)|leg_armor(9)|difficulty(11),imodbits_armor|imodbit_lordly,[]],
["gon_knight","Gondor_Heavy_Mail_and_Cloak",[("gondor_knight",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1900,weight(30)|abundance(93)|head_armor(0)|body_armor(35)|leg_armor(9)|difficulty(16),imodbits_armor|imodbit_lordly,[]],
["gon_ranger_cloak","Gondor_Ranger_Cloak",[("gondor_ranger_cloak",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1000,weight(3)|head_armor(0)|body_armor(18)|leg_armor(7)|difficulty(0),imodbits_elf_cloth,[]],
["gon_ranger_skirt","Gondor_Ranger_Skirt",[("gondor_ranger_skirt",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1200,weight(5)|head_armor(0)|body_armor(18)|leg_armor(12)|difficulty(0),imodbits_armor|imodbit_lordly,[]],
["gon_steward_guard","Gondor_Steward_Guard_Armor",[("gondor_steward_guard",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2900,weight(38)|abundance(96)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(20),imodbits_elf_armor,[]],
["gon_tower_guard","Gondor_Tower_Guard_Armor",[("gondor_tower_guard",0)],itp_type_body_armor|itp_covers_legs|0,0,3500,weight(36)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(14)|difficulty(20),imodbits_elf_armor,[]],
["gon_tower_knight","Gondor_Tower_Knight_Armor",[("gondor_tower_knight",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,3000,weight(38)|abundance(96)|head_armor(0)|body_armor(40)|leg_armor(15)|difficulty(20),imodbits_elf_armor,[]],
["gon_leader_surcoat_cloak","Gondor_Leader's_Surcoat",[("gon_leader_surcoat",0),("gon_leader_surcoat_cloak",imodbit_cloak)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2900,weight(36)|abundance(96)|head_armor(0)|body_armor(42)|leg_armor(12)|difficulty(19),imodbits_elf_armor|imodbit_cloak,[]],
["gondor_ranger_hood","Green_Hood",[("gondor_ranger_hood",0)],itp_type_head_armor|itp_shop|itp_fit_to_head,0,100,weight(0.5)|head_armor(13)|difficulty(0),imodbits_cloth,[]],
["gondor_ranger_hood_mask","Gondor_Ranger_Hood",[("gondor_ranger_hood_mask",0)],itp_type_head_armor|itp_shop|itp_fit_to_head,0,400,weight(0.6)|head_armor(15)|difficulty(0),imodbits_elf_cloth,[]],
["gondor_light_greaves","Gondorian_Leather_Greaves",[("gondor_light_greaves",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,500,weight(3)|abundance(90)|leg_armor(15)|difficulty(0),imodbits_cloth,[]],
["gondor_med_greaves","Gondorian_Medium_Greaves",[("gondor_medium_greaves",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,900,weight(6)|abundance(92)|leg_armor(20)|difficulty(0),imodbits_armor|imodbit_lordly,[]],
["gondor_heavy_greaves","Gondorian_Mailed_Greaves",[("gondor_heavy_greaves",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,1400,weight(8)|abundance(94)|leg_armor(25)|difficulty(13),imodbits_armor|imodbit_lordly,[]],
####Helms #free oct 2021
["free_gondorian_light_helm","Gondorian_Footman_Helm",[("gondor_footman_helm",0)],itp_type_head_armor,0,900,weight(2)|head_armor(29)|difficulty(0),imodbits_armor | imodbit_cracked,[]],
["free_gondor_infantry_helm","Gondor_Infantry_Helm",[("gondor_footman_helm",imodbits_armor_bad),("gondor_regular_helm",imodbit_plain),("gondor_regular_helm",0),("gondor_regular_helm2",imodbits_armor|imodbit_lordly)],itp_type_head_armor|itp_shop,0,1200,weight(5)|abundance(93)|head_armor(34)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly,[]],
["free_gondor_auxila_helm","Gondor_Light_Helm",[("gondor_auxila_helm",imodbits_armor_bad),("gondor_auxila_helm2",imodbit_plain),("gondor_auxila_helm2",0),("gondor_auxila_helm3",imodbits_armor|imodbit_lordly)],itp_type_head_armor|itp_shop,0,400,weight(1.5)|abundance(90)|head_armor(20)|body_armor(0)|difficulty(9),imodbits_armor|imodbit_lordly,[]],

["gondor_auxila_helm","Gondor_Light_Helm",[("gondor_auxila_helm",imodbits_armor_bad),("gondor_auxila_helm2",imodbit_plain),("gondor_auxila_helm2",0),("gondor_auxila_helm3",imodbits_elf_armor)],itp_type_head_armor|itp_shop,0,400,weight(1.5)|abundance(90)|head_armor(20)|body_armor(0)|difficulty(9),imodbits_armor|imodbit_lordly,[]],
["gondorian_archer_helm","Gondor_Archer_Helm",[("gondor_bowman_helm",imodbits_armor_bad),("gondor_archer_helm",imodbit_plain),("gondor_archer_helm",0),("gondor_archer_helm2",imodbits_elf_armor)],itp_type_head_armor|itp_shop,0,700,weight(2)|abundance(92)|head_armor(27)|body_armor(0)|difficulty(11),imodbits_armor|imodbit_lordly,[]],
["tower_archer_helm","Tower_Archer_Helm",[("gondor_tower_archer_helm",0)],itp_type_head_armor|itp_shop,0,1100,weight(2.5)|abundance(94)|head_armor(31)|body_armor(0)|difficulty(12),imodbits_armor|imodbit_lordly,[]],
["gondor_leader_helm","Gondor_High_Helmet",[("gondor_leader_helm",0)],itp_type_head_armor|itp_shop,0,1800,weight(7)|abundance(97)|head_armor(41)|body_armor(0)|difficulty(17),imodbits_armor|imodbit_lordly,[]],
["tower_guard_helm","Tower_Guard_Helm",[("gondor_tower_guard_helm",0)],itp_type_head_armor,0,2100,weight(9)|abundance(96)|head_armor(46)|body_armor(0)|difficulty(21),imodbits_armor|imodbit_lordly,[]],
["gondor_citadel_knight_helm","Citadel_Knight_Helm",[("gondor_citadel_knight_helm",0)],itp_type_head_armor|itp_shop,0,1500,weight(6)|abundance(96)|head_armor(39)|body_armor(0)|difficulty(16),imodbits_armor|imodbit_lordly,[]],
["gondor_infantry_helm","Gondor_Infantry_Helm",[("gondor_footman_helm",imodbits_armor_bad),("gondor_regular_helm",imodbit_plain),("gondor_regular_helm",0),("gondor_regular_helm2",imodbits_elf_armor)],itp_type_head_armor|itp_shop,0,1200,weight(5)|abundance(93)|head_armor(34)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly,[]],
["gondor_knight_helm","Gondor_Cavalry_Helm",[("gondor_squire_helm",0),("gondor_knight_helm",imodbit_plain),("gondor_knight_helm",0),("gondor_knight_helm2",imodbits_elf_armor)],itp_type_head_armor|itp_shop,0,1300,weight(5)|abundance(93)|head_armor(35)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly],
["gondor_dolamroth_helm","Dol_Amroth_Helm",[("gondor_dolamroth_helm_1",imodbits_armor_bad),("gondor_dolamroth_helm_2",imodbit_plain),("gondor_dolamroth_helm_2",0),("gondor_dolamroth_helm_3",imodbits_elf_armor)],itp_type_head_armor|itp_shop,0,1300,weight(6)|abundance(93)|head_armor(36)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly],
["swan_knight_helm","Swan_Knight_Helm",[("gondor_dolamroth_knight_helm",0)],itp_type_head_armor|itp_shop,0,1800,weight(8)|abundance(96)|head_armor(42)|body_armor(0)|difficulty(18),imodbits_armor|imodbit_lordly],
["gondor_lamedon_helm","Lamedon_Helm",[("gondor_lamedon_helm",0)],itp_type_head_armor|itp_shop,0,1000,weight(2)|abundance(93)|head_armor(32)|body_armor(0)|difficulty(12),imodbits_armor|imodbit_lordly],
["gondor_lamedon_leader_helm","Lamedon_High_Helmet",[("gondor_lamedon_leader_helm",0)],itp_type_head_armor|itp_shop,0,1300,weight(4)|abundance(95)|head_armor(36)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly],
###BRV
["blackroot_archer","Blackroot_Vale_Cloaked_Gambeson",[("blackroot_archer",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,200,weight(7)|head_armor(0)|body_armor(16)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly,],
["blackroot_bowman","Blackroot_Vale_Cloaked_Jerkin",[("blackroot_bowman",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,100,weight(5)|head_armor(0)|body_armor(14)|leg_armor(8)|difficulty(0),imodbits_elf_cloth,],
["blackroot_footman","Blackroot_Vale_Jerkin",[("blackroot_footman",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1000,weight(5)|head_armor(0)|body_armor(14)|leg_armor(7)|difficulty(0),imodbits_armor|imodbit_lordly,],
["blackroot_warrior","Blackroot_Vale_Gambeson",[("blackroot_warrior",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1200,weight(7)|head_armor(0)|body_armor(20)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly,],
["blackroot_leader","Blackroot_Vale_Mail",[("blackroot_leader",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1300,weight(25)|abundance(91)|head_armor(0)|body_armor(26)|leg_armor(10)|difficulty(11),imodbits_armor|imodbit_lordly,],
["blackroot_hood","Black_Hood",[("blackroot_hood",0),("gondor_wimple_a",imodbit_bent),("gondor_wimple_b",imodbit_cracked),("gondor_fine_fem_hat",imodbit_rusty)],itp_type_head_armor|itp_shop|itp_fit_to_head|itp_civilian,0,100,weight(0.5)|head_armor(12)|difficulty(0),imodbits_cloth],
#["blackroot_helm", "Blackroot Helm",[("blackroot_helm",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
###DOL AMROTH
["dol_hauberk","Dol_Amroth_Hauberk",[("dol_hauberk",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1400,weight(27)|abundance(92)|head_armor(0)|body_armor(25)|leg_armor(12)|difficulty(11),imodbits_armor|imodbit_lordly,],
["dol_heavy_mail","Dol_Amroth_Heavy_Mail",[("dol_heavy_mail",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2400,weight(31)|abundance(94)|head_armor(0)|body_armor(35)|leg_armor(14)|difficulty(17),imodbits_armor|imodbit_lordly,],
["dol_padded_coat","Dol_Amroth_Padded_Coat",[("dol_padded_coat",0)],itp_type_body_armor|itp_covers_legs|itp_civilian|itp_shop,0,1200,weight(14)|abundance(90)|head_armor(0)|body_armor(25)|leg_armor(10)|difficulty(9),imodbits_cloth,],
["dol_shirt","Dol_Amroth_Shirt",[("dol_shirt",0)],itp_type_body_armor|itp_covers_legs|itp_civilian|itp_shop,0,100,weight(5)|head_armor(0)|body_armor(10)|leg_armor(3)|difficulty(0),imodbits_cloth,],
["dol_very_heavy_mail","Dol_Amroth_Very_Heavy_Mail",[("dol_very_heavy_mail",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,3000,weight(38)|abundance(96)|head_armor(0)|body_armor(40)|leg_armor(15)|difficulty(20),imodbits_elf_armor,],
["dol_greaves","Dol_Amroth_Greaves",[("dol_greaves",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,1600,weight(10)|abundance(95)|leg_armor(27)|difficulty(15),imodbits_armor|imodbit_lordly],
["dol_shoes","Dol_Amroth_Light_Boots",[("dol_shoes",0)],itp_type_foot_armor|itp_shop|itp_attach_armature|itp_civilian,0,200,weight(3)|abundance(90)|leg_armor(14)|difficulty(0),imodbits_cloth],
######LAMEDON
["lamedon_clansman","Lamedon_Clansman_Armor",[("lamedon_clansman",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,70,weight(8)|head_armor(0)|body_armor(8)|leg_armor(5)|difficulty(0),imodbits_elf_cloth,],
["lamedon_footman","Lamedon_Footman_Armor",[("lamedon_footman",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,900,weight(13)|head_armor(0)|body_armor(18)|leg_armor(5)|difficulty(0),imodbits_armor|imodbit_lordly,],
["lamedon_knight","Lamedon_Knight_Armor",[("lamedon_knight",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2000,weight(32)|abundance(93)|head_armor(0)|body_armor(33)|leg_armor(12)|difficulty(16),imodbits_armor|imodbit_lordly,],
["lamedon_leader_surcoat_cloak","Lamedon_Leader_Armor",[("lamedon_leader_surcoat_cloak",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2300,weight(30)|abundance(96)|head_armor(0)|body_armor(35)|leg_armor(13)|difficulty(17),imodbits_armor|imodbit_lordly,],
["lamedon_warrior","Lamedon_Warrior_Armor",[("lamedon_warrior",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1100,weight(26)|abundance(90)|head_armor(0)|body_armor(25)|leg_armor(8)|difficulty(10),imodbits_armor|imodbit_lordly,],
["lamedon_veteran","Lamedon_Veteran_Armor",[("lamedon_veteran",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1200,weight(20)|head_armor(0)|body_armor(20)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly,],
["lamedon_vet_warrior","Lamedon_Veteran_Warrior_Armor",[("lamedon_vet_warrior",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1600,weight(28)|abundance(91)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(15),imodbits_armor|imodbit_lordly,],
["lamedon_hood","Hood",[("lamedon_hood",0)],itp_type_head_armor|itp_civilian|itp_shop,0,100,weight(1)|head_armor(10)|difficulty(0),imodbits_cloth],
#["lamedon_helmet", "Lamedon Helm",[("lamedon_helmet",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
#####PINNATH GELIN
["pinnath_archer","Pinnath_Gelin_Archer_Armor",[("pinnath_archer",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,800,weight(14)|head_armor(0)|body_armor(20)|leg_armor(8)|difficulty(0),imodbits_elf_cloth,],
["pinnath_footman","Pinnath_Gelin_Footman_Armor",[("pinnath_footman",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,400,weight(10)|head_armor(0)|body_armor(16)|leg_armor(4)|difficulty(0),imodbits_armor|imodbit_lordly,],
["pinnath_leader","Pinnath_Gelin_Knight_Armor",[("pinnath_leader",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1300,weight(26)|abundance(92)|head_armor(0)|body_armor(26)|leg_armor(10)|difficulty(11),imodbits_armor|imodbit_lordly,],
["pinnath_vet_footman","Pinnath_Gelin_Veteran_Footman_Armor",[("pinnath_vet_footman",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,600,weight(12)|head_armor(0)|body_armor(18)|leg_armor(4)|difficulty(0),imodbits_armor|imodbit_lordly,],
["pinnath_warrior","Pinnath_Gelin_Warrior_Armor",[("pinnath_warrior",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1000,weight(15)|head_armor(0)|body_armor(22)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly,],
#["pinnath_hood", "Pinnath Gelin Hood",[("pinnath_hood",0)], 0|itp_type_head_armor |itp_civilian  ,0, 35 , weight(1.25)|abundance(100)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
######PEL
["pel_footman","Pelargir_Footman_Armor",[("pelargir_footman",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1100,weight(27)|abundance(90)|head_armor(0)|body_armor(25)|leg_armor(8)|difficulty(10),imodbits_armor|imodbit_lordly,],
["pel_jerkin","Pelargir_Jerkin",[("pelargir_jerkin",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,300,weight(6)|head_armor(0)|body_armor(12)|leg_armor(6)|difficulty(0),imodbits_elf_cloth,],
["pel_leader","Pelargir_Leader_Armor",[("pelargir_leader",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1900,weight(26)|abundance(96)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(16),imodbits_elf_armor,],
["pel_marine","Pelargir_Marine",[("pelargir_marine",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1000,weight(18)|abundance(91)|head_armor(0)|body_armor(25)|leg_armor(6)|difficulty(8),imodbits_armor|imodbit_lordly,],
["pelargir_marine_leader","Pelargir_Marine_Leader",[("pelargir_marine_leader",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1600,weight(28)|abundance(96)|head_armor(0)|body_armor(34)|leg_armor(6)|difficulty(15),imodbits_elf_armor,],
["pelargir_regular","Pelargir_Regular",[("pelargir_regular",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1500,weight(26)|abundance(92)|head_armor(0)|body_armor(33)|leg_armor(6)|difficulty(9),imodbits_armor|imodbit_lordly,],
["pelargir_hood","White_Hood",[("pelargir_hood",0)],itp_type_head_armor|itp_civilian|itp_shop,0,100,weight(1)|head_armor(10)|difficulty(0),imodbits_cloth],
["pelargir_helmet_light","Pelargir_Helm",[("pelargir_helmet_light",0)],itp_type_head_armor|itp_shop,0,1100,weight(2)|head_armor(32)|difficulty(0),imodbits_armor|imodbit_lordly],
["pelargir_helmet_heavy","Pelargir_Heavy_Helm",[("pelargir_helmet_heavy",0)],itp_type_head_armor|itp_shop,0,1400,weight(3)|head_armor(38)|difficulty(0),imodbits_armor|imodbit_lordly],
["pelargir_greaves","Pelargir_Greaves",[("pelargir_greaves",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,1200,weight(6)|abundance(90)|leg_armor(23)|difficulty(12),imodbits_armor|imodbit_lordly],
######LOS
["lossarnach_shirt","Lossarnach_Shirt",[("lossarnach_shirt",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,100,weight(6)|head_armor(0)|body_armor(8)|leg_armor(4)|difficulty(0),imodbits_elf_cloth,],
["lossarnach_axeman","Lossarnach_Axeman_Armor",[("lossarnach_axeman",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,800,weight(13)|head_armor(0)|body_armor(16)|leg_armor(5)|difficulty(0),imodbits_elf_cloth,],
["lossarnach_leader","Lossarnach_Leader_Armor",[("lossarnach_leader",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1600,weight(33)|abundance(93)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(12),imodbits_elf_armor,],
["lossarnach_vet_axeman","Lossarnach_Veteran_Axeman_Armor",[("lossarnach_vet_axeman",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,900,weight(15)|head_armor(0)|body_armor(20)|leg_armor(7)|difficulty(0),imodbits_armor|imodbit_lordly,],
["lossarnach_vet_warrior","Lossarnach_Veteran_Warrior_Armor",[("lossarnach_vet_warrior",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1200,weight(21)|abundance(92)|head_armor(0)|body_armor(25)|leg_armor(10)|difficulty(11),imodbits_armor|imodbit_lordly,],
["lossarnach_warrior","Lossarnach_Warrior_Armor",[("lossarnach_warrior",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1100,weight(19)|abundance(91)|head_armor(0)|body_armor(25)|leg_armor(8)|difficulty(9),imodbits_armor|imodbit_lordly,],
["lossarnach_cloth_cap","Lossarnach_Cloth_Cap",[("lossarnach_cloth_cap",0)],itp_type_head_armor|itp_shop,0,100,weight(1)|head_armor(12)|difficulty(0),imodbits_cloth],
["lossarnach_leather_cap","Lossarnach_Leather_Cap",[("lossarnach_leather_cap",0)],itp_type_head_armor|itp_shop,0,500,weight(1.6)|head_armor(22)|difficulty(0),imodbits_cloth],
["lossarnach_scale_cap","Lossarnach_Scale_Cap",[("lossarnach_scale_cap",0)],itp_type_head_armor|itp_shop,0,800,weight(3)|head_armor(28)|difficulty(0),imodbits_armor|imodbit_lordly],
["lossarnach_greaves","Lossarnach_Greaves",[("lossarnach_greaves",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,1200,weight(6)|abundance(90)|leg_armor(23)|difficulty(12),imodbits_armor|imodbit_lordly],
####SHIELDS#####
["gondor_shield_a","Gondor_Square_Shield",[("gondor_square_shield",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,600,weight(4.5)|abundance(94)|difficulty(5)|hit_points(340)|body_armor(20)|spd_rtng(82)|weapon_length(60),imodbits_shield,],
["gondor_shield_b","Gondor_Kite_Shield",[("gondor_point_shield",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(2.5)|abundance(92)|difficulty(4)|hit_points(320)|body_armor(16)|spd_rtng(82)|weapon_length(60),imodbits_shield,],
["gondor_shield_c","Gondor_Tower_Shield",[("gondor_tower_shield",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,500,weight(3.5)|abundance(91)|difficulty(3)|hit_points(320)|body_armor(14)|spd_rtng(82)|weapon_length(70),imodbits_shield,],
["gondor_shield_d","Gondor_Kite_Shield",[("gondorian_kite_shield",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(2.5)|abundance(91)|difficulty(1)|hit_points(290)|body_armor(17)|spd_rtng(90)|weapon_length(40),imodbits_shield,],
["gondor_shield_e","Gondor_Citadel_Shield",[("denethor_shield",0)],itp_type_shield|itp_unique|itp_wooden_parry,itcf_carry_kite_shield,1000,weight(2.5)|abundance(100)|difficulty(3)|hit_points(300)|body_armor(25)|spd_rtng(90)|weapon_length(60),imodbits_shield_good,],
#
["gon_tab_shield_a","Heraldic_Gondor_Round_Shield",[("tableau_shield_round",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(2)|abundance(90)|difficulty(0)|hit_points(280)|body_armor(13)|spd_rtng(92)|weapon_length(40),imodbits_shield,[(ti_on_init_item,[(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_round_shield_banner", "tableau_gon_shield_round", ":agent_no", ":troop_no")])]],
# [(ti_on_init_item,[(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_round_shield_banner", "tableau_gon_shield_round", ":agent_no", ":troop_no")])]],
["gon_tab_shield_b","Heraldic_Gondor_Square_Shield",[("tableau_shield_square",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,200,weight(4.5)|abundance(93)|difficulty(4)|hit_points(320)|body_armor(18)|spd_rtng(82)|weapon_length(60),imodbits_shield,[(ti_on_init_item,[(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_square_shield_banner", "tableau_gon_shield_square", ":agent_no", ":troop_no")])]],
# [(ti_on_init_item,[(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_square_shield_banner", "tableau_gon_shield_square", ":agent_no", ":troop_no")])]],
["gon_tab_shield_c","Heraldic_Gondor_Kite_Shield",[("tableau_shield_kite",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(2.5)|abundance(91)|difficulty(1)|hit_points(270)|body_armor(16)|spd_rtng(90)|weapon_length(40),imodbits_shield,[(ti_on_init_item,[(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_kite_shield_banner", "tableau_gon_shield_kite", ":agent_no", ":troop_no")])]],	
# [(ti_on_init_item,[(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_kite_shield_banner", "tableau_gon_shield_kite", ":agent_no", ":troop_no")])]],
["gon_tab_shield_d","Heraldic_Gondor_Tower_Shield",[("tableau_shield_tower",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,300,weight(3.5)|abundance(91)|difficulty(4)|hit_points(300)|body_armor(13)|spd_rtng(82)|weapon_length(70),imodbits_shield,[(ti_on_init_item,[(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_tower_shield_banner", "tableau_gon_shield_tower", ":agent_no", ":troop_no")])]],						
# [(ti_on_init_item,[(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_tower_shield_banner", "tableau_gon_shield_tower", ":agent_no", ":troop_no")])]],
#######WEAPONS##########
["amroth_sword_a","Dol_Amroth_Sword",[("DA_sword_a_new",0),("scab_DA_sword_a",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,500,weight(1.25)|abundance(92)|difficulty(0)|spd_rtng(96)|weapon_length(100)|swing_damage(31,cut)|thrust_damage(21,pierce),imodbits_weapon],
["amroth_sword_b","Dol_Amroth_Knight_Sword",[("DA_sword_b",0),("scab_DA_sword_b",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,600,weight(2)|abundance(94)|difficulty(11)|spd_rtng(95)|weapon_length(100)|swing_damage(33,cut)|thrust_damage(26,pierce),imodbits_weapon_good],
["gondor_sword","Gondor_Infantry_Sword",[("gondor_inf_new",0),("scab_gondor_inf_new",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,500,weight(1.25)|abundance(92)|difficulty(0)|spd_rtng(99)|weapon_length(95)|swing_damage(28,cut)|thrust_damage(21,pierce),imodbits_weapon],
["amroth_bastard","Dol_Amroth_Swan_Blade",[("DA_bastard",0),("scab_DA_bastard",ixmesh_carry)],itp_type_two_handed_wpn|itp_primary|itp_shop,itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,720,weight(3)|abundance(95)|difficulty(14)|spd_rtng(102)|weapon_length(108)|swing_damage(39,cut)|thrust_damage(26,pierce),imodbits_weapon_good],
#
["gondor_short_sword","Linhir_Eket",[("linhir_eket",0),("scab_linhir_eket",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,300,weight(1.25)|abundance(90)|difficulty(0)|spd_rtng(113)|weapon_length(53)|swing_damage(26,cut)|thrust_damage(25,pierce),imodbits_weapon],
["pelargir_eket","Pelargir_Eket",[("pelargir_eket",0),("scab_pelargir_eket",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,400,weight(1.25)|abundance(90)|difficulty(0)|spd_rtng(119)|weapon_length(49)|swing_damage(25,cut)|thrust_damage(27,pierce),imodbits_weapon],
["pelargir_sword","Pelargir_Sword",[("pelargir_sword",0),("scab_pelargir_sword",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,450,weight(1.25)|abundance(91)|difficulty(0)|spd_rtng(103)|weapon_length(72)|swing_damage(27,cut)|thrust_damage(21,pierce),imodbits_weapon],
#
["gondor_ranger_sword","Gondor_Ranger_Sword",[("gondor_bastard",0),("scab_gondor_ranger",ixmesh_carry)],itp_type_two_handed_wpn|itp_primary|itp_shop,itc_bastardsword|itcf_carry_sword_back|itcf_show_holster_when_drawn,700,weight(2)|abundance(94)|difficulty(11)|spd_rtng(108)|weapon_length(103)|swing_damage(37,cut)|thrust_damage(26,pierce),imodbits_weapon],
["gondor_2h_sword","Gondor_War_Sword",[("gondor_bastard_new",0),("scab_gondor_bastard_new",ixmesh_carry)],itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_shop,itc_greatsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,720,weight(2.8)|abundance(94)|difficulty(12)|spd_rtng(101)|weapon_length(109)|swing_damage(39,cut)|thrust_damage(26,pierce),imodbits_weapon],
["gondor_citadel_sword","Gondor_Citadel_Sword",[("gondor_citadel",0),("scab_gondor_citadel",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,650,weight(1.25)|abundance(95)|difficulty(0)|spd_rtng(100)|weapon_length(95)|swing_damage(35,cut)|thrust_damage(30,pierce),imodbits_weapon_good],
["gondor_cav_sword","Gondor_Cavalry_Sword",[("gondor_riding_sword",0),("scab_gondor_riding_sword",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,550,weight(2)|abundance(93)|difficulty(10)|spd_rtng(97)|weapon_length(100)|swing_damage(30,cut)|thrust_damage(21,pierce),imodbits_weapon],
#
["gondor_spear","Gondorian_Spear",[("gondor_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_wooden_parry,itc_spear_upstab|itcf_carry_spear,400,weight(2.25)|abundance(90)|difficulty(0)|spd_rtng(102)|weapon_length(153)|thrust_damage(30,pierce)|swing_damage(20,blunt),imodbits_weapon_good],
["gondor_tower_spear","Gondorian_Tower_Spear",[("gondor_tower_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry,itc_spear_upstab,800,weight(2.35)|abundance(95)|difficulty(0)|spd_rtng(99)|weapon_length(173)|thrust_damage(37,pierce)|swing_damage(26,blunt),imodbits_weapon_good],
["gondor_lance","Gondor_Lance",[("amroth_lance",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable,itc_pike,450,weight(2.35)|abundance(91)|difficulty(0)|spd_rtng(89)|weapon_length(204)|thrust_damage(28,pierce),imodbits_weapon_good],
["loss_axe","Gondor_Fighting_Axe",[("loss_axe",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,270,weight(2)|abundance(90)|difficulty(0)|spd_rtng(103)|weapon_length(47)|swing_damage(28,cut)|thrust_damage(0,pierce),imodbits_weapon],
["loss_war_axe","Gondor_War_Axe",[("loss_axe_2h",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,430,weight(6)|abundance(91)|difficulty(16)|spd_rtng(87)|weapon_length(75)|swing_damage(44,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
#
###########LORIEN ITEMS##########
#######LORIEN WEAPONS########
["lorien_sword_a","Lorien_Longsword",[("lorien_sword_long",0),("scab_lorien_sword_long",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,500,weight(2)|abundance(91)|difficulty(0)|spd_rtng(104)|weapon_length(86)|swing_damage(28,cut)|thrust_damage(20,pierce),imodbits_weapon_good],
["lorien_sword_b","Lorien_Shortsword",[("lorien_sword_short",0),("scab_lorien_sword_short",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,460,weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(110)|weapon_length(65)|swing_damage(26,cut)|thrust_damage(25,pierce),imodbits_weapon_good],
["lorien_sword_c","Lorien_War_Sword",[("lorien_sword_hand_and_half",0),("scab_lorien_sword_hand_and_half",ixmesh_carry)],itp_type_two_handed_wpn|itp_primary|itp_shop,itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,640,weight(2.5)|abundance(94)|difficulty(10)|spd_rtng(110)|weapon_length(93)|swing_damage(36,cut)|thrust_damage(23,pierce),imodbits_weapon_good],
###########LORIEN ARMORS########
["lorien_archer","Lorien_Archer_Armor",[("lorien_archer",0),("lorien_warden_cloak",imodbit_cloak),("lorien_archer_heavy",imodbits_armor_good),("lorien_archer_heavy_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,150,weight(5)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(5)|difficulty(0),imodbits_armor|imodbit_lordly,],
["lorien_armor_a","Lorien_Quilted_Armor",[("lorien_light_1",imodbits_armor_bad),("lorien_light_2",0),("lorien_light_2_cloak",imodbit_cloak),("lorien_light_3",imodbits_armor_good),("lorien_light_3_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,700,weight(8)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly,],
["lorien_armor_b","Lorien_Mail_Armor",[("lorien_med_1",imodbits_armor_bad),("lorien_med_2",imodbit_plain),("lorien_med_2",0),("lorien_med_2_cloak",imodbit_cloak),("lorien_med_3",imodbits_armor_good),("lorien_med_3_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1200,weight(12)|abundance(93)|head_armor(0)|body_armor(25)|leg_armor(10)|difficulty(8),imodbits_armor|imodbit_lordly|imodbit_cloak,],
["lorien_armor_c","Lorien_Scale_Armor",[("lorien_heavy_1",imodbits_armor_bad),("lorien_heavy_2",imodbit_plain),("lorien_heavy_2",0),("lorien_heavy_2_cloak",imodbit_cloak),("lorien_heavy_3",imodbits_armor_good),("lorien_heavy_3_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1800,weight(18)|abundance(95)|head_armor(0)|body_armor(32)|leg_armor(10)|difficulty(9),imodbits_armor|imodbit_lordly|imodbit_cloak,],
["free_lorien_armor_d","Lorien_Royal_Swordsman_Armor",[("lorien_heavy_3_cloak",0)],itp_type_body_armor|itp_covers_legs,0,2400,weight(12)|head_armor(0)|body_armor(35)|leg_armor(10)|difficulty(0),imodbits_armor,],
["free_lorien_armor_e","Lorien_Warden_Cloak",[("lorien_archer_heavy_cloak",0)],itp_type_body_armor|itp_covers_legs,0,700,weight(12)|head_armor(0)|body_armor(28)|leg_armor(10)|difficulty(0),imodbits_armor,],
["free_lorien_armor_f","Lorien_Elite_Armor",[("lorien_heavy_3",0)],itp_type_body_armor|itp_covers_legs,0,2000,weight(12)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0),imodbits_armor,],
#
["lorien_boots","Lothlorien_Boots",[("lorien_boots",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,800,weight(2)|abundance(92)|leg_armor(19)|difficulty(0),imodbits_elf_cloth],
########LORIEN SHIELDS#####
["lorien_shield_b","Lorien_Tower_Shield",[("lorien_kite",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,700,weight(2)|abundance(92)|difficulty(4)|hit_points(330)|body_armor(15)|spd_rtng(82)|weapon_length(70),imodbits_shield_good,],
["lorien_shield_c","Lorien_Kite_Shield",[("lorien_kite_small",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,500,weight(2)|abundance(92)|difficulty(2)|hit_points(290)|body_armor(18)|spd_rtng(90)|weapon_length(60),imodbits_shield_good,],
["lorien_round_shield","Lorien_Round_Shield",[("lorien_round_shield",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,400,weight(1)|abundance(90)|difficulty(1)|hit_points(300)|body_armor(15)|spd_rtng(92)|weapon_length(40),imodbits_shield_good,],
# 
########LORIEN HELMS#######
["lorien_helm_a","Lorien_Archer_Helm",[("lorienhelmetarcherlow",0)],itp_type_head_armor|itp_shop,0,1300,weight(2)|abundance(93)|head_armor(35)|body_armor(0)|difficulty(12),imodbits_armor|imodbit_lordly],
["lorien_helm_b","Lorien_Archer_Helm",[("lorienhelmetarcherhigh",0)],itp_type_head_armor|itp_shop,0,1800,weight(3)|abundance(95)|head_armor(40)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly],
["lorien_helm_c","Lorien_Infantry_Helm",[("lorienhelmetinf_a",0),("lorienhelmetinf_a",imodbit_plain),("lorienhelmetinf_b",imodbits_elf_armor)],itp_type_head_armor|itp_shop,0,1900,weight(4)|abundance(96)|head_armor(42)|body_armor(0)|difficulty(16),imodbits_armor|imodbit_lordly],


########GENERIC ORC ITEMS#####
#next one unused:
["free_orc_chain_greaves","Orc_Greaves",[("orc_chain_greaves_lr",0)],itp_type_foot_armor|itp_shop,0,701,weight(3)|leg_armor(15)|difficulty(0),imodbits_orc_armor],
["orc_coif","Orc_Skullcap",[("orc_skullcap_a",imodbits_orc_bad),("orc_skullcap_b",0),("orc_skullcap_c",imodbits_orc_good)],itp_type_head_armor|itp_shop|itp_fit_to_head,0,200,weight(2.3)|head_armor(16)|difficulty(0),imodbits_orc_armor],
["orc_greaves","Orc_Chain_Boots",[("old_orc_chain_greave_lr",0)],itp_type_foot_armor|itp_shop,0,301,weight(8)|abundance(92)|leg_armor(15)|difficulty(10),imodbits_orc_armor],
["orc_ragwrap","Orc_Ragwrap",[("orc_ragwrap_lr",0)],itp_type_foot_armor|itp_shop,0,21,weight(1)|abundance(90)|leg_armor(3)|difficulty(0),imodbits_orc_cloth],
["orc_furboots","Orc_Fur_Boots",[("orc_furboot_lr",0)],itp_type_foot_armor|itp_shop,0,201,weight(4)|abundance(90)|leg_armor(10)|difficulty(0),imodbits_orc_cloth],
#free JAN 2017
["free_orc_furboot_tall","Orc_Fur_Boots",[("orc_furboot_tall",0)],itp_type_foot_armor|itp_shop,0,201,weight(3)|leg_armor(10)|difficulty(0),imodbits_orc_cloth],
#
["orc_tribal_a","Untreated_Skin",[("orc_tribal_a",0)],itp_type_body_armor|itp_covers_legs|itp_unique,0,1,weight(3)|head_armor(0)|body_armor(3)|leg_armor(0)|difficulty(0),imodbits_orc_cloth,],
["orc_tribal_b","Untreated_Skin",[("orc_tribal_b",0)],itp_type_body_armor|itp_covers_legs|itp_unique,0,1,weight(3)|head_armor(0)|body_armor(2)|leg_armor(1)|difficulty(0),imodbits_orc_cloth,],
["orc_tribal_c","Untreated_Skin",[("orc_tribal_c",0)],itp_type_body_armor|itp_covers_legs|itp_unique,0,1,weight(3)|head_armor(0)|body_armor(1)|leg_armor(2)|difficulty(0),imodbits_orc_cloth,],
["evil_gauntlets_a","Black_Gloves",[("CWE_gloves_a_black_L",imodbits_armor_bad),("CWE_gloves_a_black_h_L",0),("CWE_gloves_lord_black_L",imodbits_elf_cloth),("CWE_gauntlets_arabs_a_L",imodbit_reinforced)],itp_type_hand_armor|itp_shop,0,500,weight(0.4)|body_armor(2)|difficulty(0),imodbits_orc_cloth],
["evil_gauntlets_b","Black_Gauntlets",[("narf_wisby_gauntlets_black_L",0),("narf_wisby_gauntlets_red_L",imodbits_armor_good|imodbit_lordly)],itp_type_hand_armor|itp_shop,0,500,weight(1.2)|body_armor(4)|difficulty(0),imodbits_armor|imodbit_lordly],
#
###ISENGARD ITEMS##########
##########ARMORS##########
["free_isen_orc_armor_a","Isengard_Orc_Armor",[("orc_isen_light_1_b",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,51,weight(5)|head_armor(0)|body_armor(5)|leg_armor(3)|difficulty(0),imodbits_orc_cloth,],
["isen_orc_light_a","Isengard_Orc_Light_Harness",[("orc_isen_light_1_b",imodbit_plain),("orc_isen_light_1_b",0),("orc_isen_light_1_a",imodbits_armor_bad),("orc_isen_light_1_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,401,weight(4)|abundance(90)|head_armor(0)|body_armor(7)|leg_armor(2)|difficulty(0),imodbits_orc_cloth,],
["isen_orc_light_b","Isengard_Orc_Light_Harness",[("orc_isen_light_2_b",imodbit_plain),("orc_isen_light_2_b",0),("orc_isen_light_2_a",imodbits_armor_bad),("orc_isen_light_2_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,401,weight(6)|abundance(91)|head_armor(0)|body_armor(13)|leg_armor(4)|difficulty(8),imodbits_orc_cloth,],
["isen_orc_pad_a","Isengard_Orc_Light_Segmented_Armor",[("orc_isen_pad_1_b",imodbit_plain),("orc_isen_pad_1_b",0),("orc_isen_pad_1_a",imodbits_armor_bad),("orc_isen_pad_1_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,501,weight(19)|abundance(92)|head_armor(0)|body_armor(15)|leg_armor(5)|difficulty(12),imodbits_orc_armor,],
["isen_orc_pad_b","Isengard_Orc_Medium_Segmented_Armor",[("orc_isen_pad_2_b",imodbit_plain),("orc_isen_pad_2_b",0),("orc_isen_pad_2_a",imodbits_armor_bad),("orc_isen_pad_2_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,601,weight(25)|abundance(93)|head_armor(0)|body_armor(17)|leg_armor(9)|difficulty(14),imodbits_orc_armor,],
["isen_orc_mail_a","Isengard_Orc_Mail",[("orc_isen_mail_b",imodbit_plain),("orc_isen_mail_b",0),("orc_isen_mail_a",imodbits_armor_bad),("orc_isen_mail_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,701,weight(30)|abundance(94)|head_armor(0)|body_armor(18)|leg_armor(9)|difficulty(14),imodbits_orc_armor,],
["isen_orc_mail_b","Isengard_Orc_Heavy_Segmented_Armor",[("orc_isen_heavy_b",imodbit_plain),("orc_isen_heavy_b",0),("orc_isen_heavy_a",imodbits_armor_bad),("orc_isen_heavy_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,801,weight(36)|abundance(95)|head_armor(0)|body_armor(22)|leg_armor(9)|difficulty(18),imodbits_orc_armor,],
["isen_uruk_light_a","Uruk-hai_Light_Harness",[("urukhai_isen_light_harness_b",imodbit_plain),("urukhai_isen_light_harness_b",0),("urukhai_isen_light_harness_a",imodbits_armor_bad),("urukhai_isen_light_harness_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,52,weight(4)|abundance(90)|head_armor(0)|body_armor(8)|leg_armor(3)|difficulty(0),imodbits_orc_armor,],
["isen_uruk_light_b","Uruk-hai_Fighting_Harness",[("urukhai_isen_med_harness_b",imodbit_plain),("urukhai_isen_med_harness_b",0),("urukhai_isen_med_harness_a",imodbits_armor_bad),("urukhai_isen_med_harness_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,402,weight(6)|abundance(91)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(10),imodbits_orc_armor,],
["isen_uruk_light_c","Uruk-hai_Berserker_Harness",[("urukhai_isen_berserker_b",imodbit_plain),("urukhai_isen_berserker_b",0),("urukhai_isen_berserker_a",imodbits_armor_bad),("urukhai_isen_berserker_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,702,weight(8)|abundance(95)|head_armor(0)|body_armor(20)|leg_armor(9)|difficulty(12),imodbits_orc_armor,],
["isen_uruk_med_a","Uruk-hai_Light_Segmented_Armour",[("urukhai_isen_med_pad_b",imodbit_plain),("urukhai_isen_med_pad_b",0),("urukhai_isen_med_pad_a",imodbits_armor_bad),("urukhai_isen_med_pad_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1002,weight(25)|abundance(92)|head_armor(0)|body_armor(20)|leg_armor(12)|difficulty(12),imodbits_orc_armor,],
["isen_uruk_med_b","Uruk-hai_Mail",[("urukhai_isen_med_mail_b",imodbit_plain),("urukhai_isen_med_mail_b",0),("urukhai_isen_med_mail_a",imodbits_armor_bad),("urukhai_isen_med_mail_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1102,weight(27)|abundance(93)|head_armor(0)|body_armor(22)|leg_armor(12)|difficulty(14),imodbits_orc_armor,],
["isen_uruk_heavy_a","Uruk-hai_Medium_Segmented_Armour",[("urukhai_isen_heavy_pad_b",imodbit_plain),("urukhai_isen_heavy_pad_b",0),("urukhai_isen_heavy_pad_a",imodbits_armor_bad),("urukhai_isen_heavy_pad_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1462,weight(30)|abundance(94)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(16),imodbits_orc_armor,],
["isen_uruk_heavy_b","Uruk-hai_Heavy_Mail",[("urukhai_isen_heavy_mail_b",imodbit_plain),("urukhai_isen_heavy_mail_b",0),("urukhai_isen_heavy_mail_a",imodbits_armor_bad),("urukhai_isen_heavy_mail_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2102,weight(36)|abundance(95)|head_armor(0)|body_armor(32)|leg_armor(14)|difficulty(18),imodbits_orc_armor,],
["isen_uruk_heavy_c","Uruk-hai_Full_Segmented_Armour",[("urukhai_isen_plate_b",imodbit_plain),("urukhai_isen_plate_b",0),("urukhai_isen_plate_a",imodbits_armor_bad),("urukhai_isen_plate_a",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2702,weight(38)|abundance(96)|head_armor(0)|body_armor(36)|leg_armor(16)|difficulty(20),imodbits_orc_armor,],
["isen_uruk_heavy_d","Uruk-hai_Tracker_Leather",[("urukhai_isen_tracker_b",imodbit_plain),("urukhai_isen_tracker_b",0),("urukhai_isen_tracker_a",imodbits_armor_bad),("urukhai_isen_tracker_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,802,weight(7)|abundance(92)|head_armor(0)|body_armor(15)|leg_armor(10)|difficulty(10),imodbits_orc_cloth,],
["isen_uruk_heavy_e","Uruk-hai_Tracker_Leather",[("urukhai_isen_tracker_b",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,802,weight(7)|abundance(92)|head_armor(0)|body_armor(18)|leg_armor(10)|difficulty(10),imodbits_orc_cloth,],
["uruk_tracker_boots","Uruk_Tracker_Boots",[("uruk_furboot_lr",0)],itp_type_foot_armor|itp_shop,0,303,weight(2)|abundance(90)|leg_armor(12)|difficulty(0),imodbits_orc_cloth],
["uruk_greaves","Uruk_Greaves",[("uruk_light_greave_lr",0)],itp_type_foot_armor|itp_shop,0,803,weight(8)|abundance(92)|leg_armor(19)|difficulty(13),imodbits_orc_armor],
["uruk_chain_greaves","Uruk_Chain_Greaves",[("uruk_greave_lr",0)],itp_type_foot_armor|itp_shop,0,1103,weight(10)|abundance(94)|leg_armor(22)|difficulty(15),imodbits_orc_armor],
["uruk_ragwrap","Uruk_Ragwrap",[("uruk_ragwrap_lr",0)],itp_type_foot_armor|itp_shop,0,23,weight(2)|abundance(90)|leg_armor(3)|difficulty(0),imodbits_orc_armor],
#["isengard_surcoat"  , "Isengard Surcoat"  ,[("uruk_body",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(13)|difficulty(8) ,imodbits_armor ],
#########HELMS########## #free Nov 2021
["free_isen_orc_helm_a","Isengard_Orc_Helm",[("orc_isen_helm_a",0)],itp_type_head_armor|itp_shop|itp_fit_to_head,0,400,weight(3)|abundance(91)|head_armor(21)|body_armor(0)|difficulty(9),imodbits_orc_armor | imodbit_cracked],
["free_isen_orc_helm_b","Isengard_Orc_Helm",[("orc_isen_helm_b",0)],itp_type_head_armor|itp_shop|itp_fit_to_head,0,400,weight(3)|abundance(91)|head_armor(21)|body_armor(0)|difficulty(9),imodbits_orc_armor | imodbit_cracked],
["isen_orc_helm_a","Isengard_Orc_Helm",[("orc_isen_helm_b",0),("orc_isen_helm_b",imodbit_plain),("orc_isen_helm_a",imodbits_orc_bad),("orc_isen_helm_c",imodbits_orc_good)],itp_type_head_armor|itp_shop,0,400,weight(4)|abundance(91)|head_armor(21)|body_armor(0)|difficulty(9),imodbits_orc_armor | imodbit_cracked],
["free_isen_uruk_helm_a","Uruk-Hai_Helm",[("urukhai_helm_a",0)],itp_type_head_armor|itp_shop,0,600,weight(5)|abundance(92)|head_armor(25)|body_armor(0)|difficulty(12),imodbits_orc_armor | imodbit_cracked],
["isen_uruk_helm_a","Uruk-Hai_Helm",[("urukhai_helm_b",0),("urukhai_helm_b",imodbit_plain),("urukhai_helm_a",imodbits_orc_bad),("urukhai_helm_c",imodbits_orc_good)],itp_type_head_armor|itp_shop,0,700,weight(5)|abundance(93)|head_armor(27)|body_armor(0)|difficulty(13),imodbits_orc_armor | imodbit_cracked],
["free_isen_uruk_helm_c","Uruk-Hai_Helm",[("urukhai_helm_c",0)],itp_type_head_armor|itp_shop,0,900,weight(6)|abundance(94)|head_armor(30)|body_armor(0)|difficulty(14),imodbits_armor|imodbit_lordly],
["isen_uruk_helm_d","Uruk-Hai_Captain_Helm",[("urukhai_captainhelm",0)],itp_type_head_armor|itp_shop,0,1300,weight(8)|abundance(95)|head_armor(35)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly],
["isen_uruk_helm_e","Uruk-Hai_Tracker_Helm",[("urukhai_trackerhelm_a",0),("urukhai_trackerhelm_a",imodbit_plain),("urukhai_trackerhelm_b",imodbits_orc_good)],itp_type_head_armor|itp_shop,0,500,weight(2)|abundance(91)|head_armor(23)|body_armor(0)|difficulty(11),imodbits_orc_armor | imodbit_cracked],
["free_isen_uruk_helm_f","Uruk-Hai_Tracker_Helm",[("urukhai_trackerhelm_b",0)],itp_type_head_armor|itp_shop,0,600,weight(2)|abundance(92)|head_armor(25)|body_armor(0)|difficulty(12),imodbits_orc_armor | imodbit_cracked],
##############WEAPONS##########
########Uruk Weapons
#unused ->#
["free_uruk_pike_a","Uruk_Pike",[("isengard_pike",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_cant_use_on_horseback|itp_spear|itp_two_handed|itp_wooden_parry,itc_cutting_spear,400,weight(3)|abundance(90)|difficulty(0)|spd_rtng(81)|weapon_length(227)|thrust_damage(26,pierce)|swing_damage(16,blunt),imodbits_weapon_wood],
["uruk_pike_b","Mordor_Pike",[("uruk_pike",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_two_handed|itp_wooden_parry|itp_couchable,itc_lance_upstab,300,weight(3)|abundance(91)|difficulty(11)|spd_rtng(81)|weapon_length(200)|thrust_damage(29,pierce)|swing_damage(0,blunt),imodbits_weapon_wood],
["uruk_falchion_a","Uruk_Falchion",[("uruk_falchion_a",0),("uruk_falchion_b",imodbits_weapon_bad_heavy)],itp_type_two_handed_wpn|itp_primary|itp_penalty_with_shield|itp_shop,itc_bastardfalchion|itcf_carry_sword_left_hip,300,weight(2.5)|abundance(92)|difficulty(11)|spd_rtng(104)|weapon_length(74)|swing_damage(35,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["uruk_falchion_b","Orc_Great_Scimitar",[("khazad_orc_bastard_scimitar_3",0),("khazad_orc_bastard_scimitar_1",imodbits_weapon_bad),("khazad_orc_bastard_scimitar_2",imodbits_weapon_bad_heavy|imodbit_balanced)],itp_type_two_handed_wpn|itp_primary|itp_penalty_with_shield|itp_shop,itc_bastardfalchion|itcf_carry_sword_left_hip,350,weight(2.5)|abundance(92)|difficulty(12)|spd_rtng(99)|weapon_length(90)|swing_damage(37,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["free_uruk_spear","Mordor_Spear",[("uruk_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable,itc_spear_upstab,300,weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(96)|weapon_length(168)|thrust_damage(27,pierce)|swing_damage(20,blunt),imodbits_weapon_wood],
["free_uruk_skull_spear","Uruk_Skull_Spear",[("uruk_skull_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_two_handed|itp_wooden_parry|itp_couchable,itc_spear_upstab,300,weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(96)|weapon_length(176)|thrust_damage(27,pierce)|swing_damage(20,blunt),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["free_uruk_voulge","Uruk_Voulge",[("uruk_voulge",0)],itp_type_polearm|itp_no_blur|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,400,weight(8)|abundance(90)|difficulty(0)|spd_rtng(87)|weapon_length(139)|swing_damage(38,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["free_uruk_heavy_axe","Uruk_Heavy_Axe",[("uruk_heavy_axe",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_cant_use_on_horseback|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,300,weight(7)|abundance(90)|difficulty(0)|spd_rtng(90)|weapon_length(99)|swing_damage(45,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
############Isengard Weapons
["isengard_sword","Isengard_Sword",[("isengard_sword",0)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,300,weight(2.5)|abundance(91)|difficulty(11)|spd_rtng(93)|weapon_length(75)|swing_damage(30,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["isengard_axe","Isengard_Axe",[("isengard_axe",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,300,weight(2)|abundance(90)|difficulty(9)|spd_rtng(85)|weapon_length(73)|swing_damage(35,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["isengard_hammer","Isengard_Hammer",[("isengard_hammer",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_wooden_parry|itp_crush_through|itp_unbalanced|itp_can_knock_down,itc_scimitar|itcf_carry_mace_left_hip,300,weight(4.5)|abundance(92)|difficulty(12)|spd_rtng(85)|weapon_length(61)|swing_damage(24,blunt)|thrust_damage(15,blunt),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["isengard_halberd","Isengard_Halberd",[("isengard_halberd",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_two_handed|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_cutting_spear,750,weight(6)|abundance(94)|difficulty(18)|spd_rtng(81)|weapon_length(150)|swing_damage(38,cut)|thrust_damage(21,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["isengard_mallet","Isengard_Mallet",[("isengard_mallet",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack|itp_crush_through|itp_unbalanced|itp_can_knock_down,itc_nodachi,700,weight(7)|abundance(94)|difficulty(19)|spd_rtng(82)|weapon_length(83)|swing_damage(35,blunt)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["isengard_heavy_axe","Isengard_Heavy_Axe",[("isengard_heavy_axe",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_cant_use_on_horseback|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,500,weight(4.5)|abundance(94)|difficulty(17)|spd_rtng(87)|weapon_length(116)|swing_damage(38,cut),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["isengard_heavy_sword","Isengard_Heavy_Sword",[("isengard_heavy_sword",0)],itp_type_two_handed_wpn|itp_primary|itp_cant_use_on_horseback|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_shop,itc_nodachi|itcf_carry_sword_left_hip,500,weight(4.5)|abundance(95)|difficulty(15)|spd_rtng(93)|weapon_length(102)|swing_damage(40,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["isengard_spear","Isengard_Spear",[("isengard_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_two_handed|itp_wooden_parry,itc_lance_upstab,300,weight(2.5)|abundance(90)|difficulty(9)|spd_rtng(96)|weapon_length(150)|thrust_damage(27,pierce)|swing_damage(0,blunt),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["isengard_pike","Isengard_Pike",[("isengard_pike",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_cant_use_on_horseback|itp_two_handed|itp_wooden_parry,itc_cutting_spear,400,weight(3.5)|abundance(91)|difficulty(11)|spd_rtng(92)|weapon_length(226)|thrust_damage(26,pierce)|swing_damage(20,blunt),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
########shields
["isen_orc_shield_a","Isen_Orc_Shield",[("isen_orc_shield_a",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,100,weight(3)|abundance(91)|difficulty(1)|hit_points(240)|body_armor(15)|spd_rtng(88)|weapon_length(30),imodbits_shield,],
["isen_orc_shield_b","Isen_Orc_Shield",[("isen_orc_shield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(3)|abundance(91)|difficulty(1)|hit_points(240)|body_armor(15)|spd_rtng(88)|weapon_length(30),imodbits_shield,],
["isen_uruk_shield_b","Isen_Uruk_Shield",[("isen_uruk_shield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,450,weight(4)|abundance(93)|difficulty(3)|hit_points(300)|body_armor(17)|spd_rtng(82)|weapon_length(45),imodbits_shield,],
########Orc Weapons
#
#Clubs
["wood_club","Wooden_Club",[("orc_club_a",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_wooden_parry|itp_wooden_attack,itc_scimitar|itcf_carry_mace_left_hip,5,weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(90)|weapon_length(62)|swing_damage(20,blunt)|thrust_damage(0,blunt),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["twohand_wood_club","Large_Wooden_Club",[("orc_club_d",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_shop|itp_wooden_attack|itp_can_knock_down|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,10,weight(3.5)|abundance(90)|difficulty(10)|spd_rtng(85)|weapon_length(75)|swing_damage(25,blunt)|thrust_damage(0,blunt),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["bone_cudgel","Bone_Cudgel",[("bone_cudgel",0),("skull_club",imodbits_weapon_bad_heavy)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_no_parry|itp_wooden_attack,itc_cleaver|itcf_carry_mace_left_hip,5,weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(90)|weapon_length(53)|swing_damage(15,blunt)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_pick","Orc_Pick",[("khazad_orc_pick_1",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_no_parry,itc_cleaver|itcf_carry_mace_left_hip,240,weight(2)|abundance(91)|difficulty(9)|spd_rtng(92)|weapon_length(53)|swing_damage(25,pierce)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_hammer","Evil_Hammer",[("khazad_orc_th_hammer_1",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_unbalanced,itc_scimitar|itcf_carry_mace_left_hip,600,weight(4.5)|abundance(93)|difficulty(11)|spd_rtng(83)|weapon_length(80)|swing_damage(30,blunt)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_club_b","Warg_Rider_Club",[("orc_club_b",0),("khazad_orc_club_1",imodbits_weapon_bad_heavy)],itp_type_two_handed_wpn|itp_primary|itp_shop|itp_penalty_with_shield,itc_bastardfalchion|itcf_carry_mace_left_hip,400,weight(3)|abundance(91)|difficulty(11)|spd_rtng(85)|weapon_length(77)|swing_damage(27,blunt)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_club_c","Spiky_Orc_Club",[("orc_club_c",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_no_parry,itc_dagger|itcf_carry_mace_left_hip,230,weight(2.5)|abundance(90)|difficulty(9)|spd_rtng(85)|weapon_length(70)|swing_damage(20,pierce)|thrust_damage(25,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_club_d","Evil_Mace",[("khazad_orc_th_club_2",0),("khazad_orc_th_club_1",imodbits_weapon_bad_heavy)],itp_type_one_handed_wpn|itp_primary|itp_can_knock_down,itc_scimitar|itcf_carry_mace_left_hip,500,weight(3.5)|abundance(93)|difficulty(12)|spd_rtng(87)|weapon_length(65)|swing_damage(27,blunt)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_sledgehammer","Orc_Sledgehammer",[("orc_sledgehammer",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_two_handed|itp_no_parry|itp_wooden_attack|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced|itp_can_knock_down,itc_cut_two_handed|itcf_carry_back,150,weight(7)|abundance(91)|difficulty(13)|spd_rtng(80)|weapon_length(75)|swing_damage(27,blunt)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_simple_spear","Orc_Spear",[("orc_simple_spear",0),("uruk_spear",imodbits_weapon_bad_heavy)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield,itc_lance_upstab,50,weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(96)|weapon_length(152)|thrust_damage(22,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_skull_spear","Orc_Skull_Spear",[("orc_skull_spear",0),("uruk_skull_spear",imodbits_weapon_bad_heavy)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_couchable,itc_lance_upstab,200,weight(3)|abundance(90)|difficulty(0)|spd_rtng(92)|weapon_length(162)|thrust_damage(25,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_bill","Orc_Polearm",[("khazad_orc_th_axe_1",0),("orc_bill",imodbits_weapon_bad),("uruk_voulge",imodbits_weapon_bad_heavy)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_two_handed|itp_cant_use_on_horseback,itc_poleaxe|itcf_carry_spear,400,weight(4.5)|abundance(92)|difficulty(11)|spd_rtng(83)|weapon_length(122)|swing_damage(30,cut)|thrust_damage(12,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_slasher","Orc_Short_Sword",[("orc_machete",0),("orc_slasher",imodbits_weapon_bad_heavy)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,50,weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(98)|weapon_length(54)|swing_damage(23,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_falchion","Orc_Falchion",[("orc_falchion",0),("orc_scimitar",imodbits_weapon_bad),("orc_sabre",imodbits_weapon_bad_heavy)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,150,weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(90)|weapon_length(65)|swing_damage(26,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_scimitar","Orc_Scimitar",[("khazad_orc_scimitar_4",0),("khazad_orc_scimitar_5",imodbits_weapon_bad),("khazad_orc_scimitar_6",imodbits_weapon_bad_heavy)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,200,weight(1.5)|abundance(91)|difficulty(0)|spd_rtng(93)|weapon_length(75)|swing_damage(25,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_sabre","Orc_Sabre",[("khazad_orc_scimitar_1",0),("khazad_orc_scimitar_2",imodbits_weapon_bad),("khazad_orc_scimitar_3",imodbits_weapon_bad_heavy)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,150,weight(2.5)|abundance(91)|difficulty(0)|spd_rtng(85)|weapon_length(73)|swing_damage(27,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_battle_axe","Orc_Battle_Axe",[("khazad_orc_axe_2",0),("khazad_orc_axe_3",imodbits_weapon_bad_heavy)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_no_parry|itp_shop|itp_crush_through|itp_unbalanced,itc_cut_two_handed|itcf_carry_axe_back,400,weight(5)|abundance(93)|difficulty(11)|spd_rtng(90)|weapon_length(85)|swing_damage(38,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_axe","Orc_Axe",[("orc_axe",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_no_parry,itc_cleaver|itcf_carry_axe_left_hip,150,weight(2)|abundance(90)|difficulty(0)|spd_rtng(85)|weapon_length(61)|swing_damage(28,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_two_handed_axe","Orc_Great_Axe",[("orc_twohanded_axe",0),("uruk_heavy_axe",imodbits_weapon_bad_heavy)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_no_parry|itp_shop|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_cut_two_handed|itcf_carry_axe_back,400,weight(5)|abundance(94)|difficulty(12)|spd_rtng(87)|weapon_length(92)|swing_damage(35,cut)|thrust_damage(0,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["orc_throwing_axes","Orc_Throwing_Axes",[("orc_throwing_axe",0),("orc_throwing_axe_quiver", ixmesh_carry),("orc_throwing_axe_inventory", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_axe|itcf_carry_quiver_front_right|itcf_show_holster_when_drawn,200,weight(5)|difficulty(1)|shoot_speed(20)|spd_rtng(99)|weapon_length(53)|thrust_damage(38,cut)|accuracy(87)|max_ammo(4),imodbits_thrown,[] ],
["orc_bow","Orc_Bow",[("orc_bow",0),("orc_bow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_two_handed|itp_shop,itcf_shoot_ganstabow|itcf_carry_bowcase_left,200,weight(1.25)|difficulty(0)|shoot_speed(53)|spd_rtng(86)|thrust_damage(20,cut)|accuracy(74),imodbits_bow,[] ],
# uruk_bow is a orc_bow intended for uruks/humans (vertical shooting position)
####Orc Shields
["orc_shield_a","Simple_Shield",[("orc_shield_a",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,100,weight(3)|abundance(90)|difficulty(0)|hit_points(180)|body_armor(5)|spd_rtng(96)|weapon_length(40),imodbits_shield,],
["orc_shield_b","Fur_Shield",[("orc_shield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,100,weight(3)|abundance(90)|difficulty(0)|hit_points(180)|body_armor(5)|spd_rtng(96)|weapon_length(40),imodbits_shield,],
["orc_shield_c","Fur_Tower_Shield",[("orc_shield_c",0),("orc_shield_c_strong", imodbit_reinforced), ("orc_shield_c_strong", imodbit_hardened), ("orc_shield_c_strong", imodbit_thick)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,250,weight(5)|abundance(90)|difficulty(2)|hit_points(230)|body_armor(6)|spd_rtng(82)|weapon_length(65),imodbits_shield,],
["mordor_orc_shield_a","Mordor_Orc_Shield",[("mordor_orc_shield_a",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,100,weight(3)|abundance(90)|difficulty(0)|hit_points(200)|body_armor(8)|spd_rtng(96)|weapon_length(35),imodbits_shield,],
["mordor_orc_shield_b","Mordor_Orc_Shield",[("mordor_orc_shield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,100,weight(3)|abundance(90)|difficulty(0)|hit_points(200)|body_armor(9)|spd_rtng(96)|weapon_length(35),imodbits_shield,],
["mordor_orc_shield_c","Mordor_Orc_Shield",[("mordor_orc_shield_c",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,100,weight(3)|abundance(90)|difficulty(0)|hit_points(200)|body_armor(9)|spd_rtng(96)|weapon_length(35),imodbits_shield,],
["mordor_orc_shield_d","Mordor_Orc_Shield",[("mordor_orc_shield_d",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(3)|abundance(91)|difficulty(1)|hit_points(250)|body_armor(15)|spd_rtng(92)|weapon_length(35),imodbits_shield,],
["mordor_orc_shield_e","Mordor_Orc_Shield",[("mordor_orc_shield_e",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(3)|abundance(91)|difficulty(1)|hit_points(250)|body_armor(15)|spd_rtng(92)|weapon_length(40),imodbits_shield,],
["mordor_uruk_shield_a","Mordor_Uruk_Shield",[("mordor_uruk_shield_a",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_round_shield,300,weight(4)|abundance(92)|difficulty(3)|hit_points(290)|body_armor(11)|spd_rtng(82)|weapon_length(60),imodbits_shield,],
["mordor_uruk_shield_b","Mordor_Uruk_Shield",[("mordor_uruk_shield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_round_shield,350,weight(4)|abundance(92)|difficulty(3)|hit_points(290)|body_armor(13)|spd_rtng(82)|weapon_length(60),imodbits_shield,],
["mordor_uruk_shield_c","Mordor_Uruk_Shield",[("mordor_uruk_shield_c",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_round_shield,400,weight(4)|abundance(92)|difficulty(3)|hit_points(290)|body_armor(14)|spd_rtng(82)|weapon_length(60),imodbits_shield,],
["mordor_man_shield_a","Mordor_Man_Shield",[("mordor_man_shield_a",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,600,weight(3)|abundance(94)|difficulty(2)|hit_points(330)|body_armor(17)|spd_rtng(90)|weapon_length(40),imodbits_shield,],
["mordor_man_shield_b","Mordor_Man_Shield",[("mordor_man_shield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,600,weight(3)|abundance(94)|difficulty(2)|hit_points(310)|body_armor(15)|spd_rtng(93)|weapon_length(40),imodbits_shield,],
["angmar_shield","Angmar_Shield",[("angmar_shield",0)],itp_type_shield|itp_wooden_parry|itp_unique,itcf_carry_round_shield,3000,weight(4)|abundance(100)|difficulty(3)|hit_points(1600)|body_armor(20)|spd_rtng(96)|weapon_length(40),0,],
#### Generic orc helmets #free Feb 2018
["orc_nosehelm","Orc_Nosehelm",[("orc_helm_nose_b",0),("orc_helm_nose_b",imodbit_plain),("orc_helm_nose_a",imodbits_orc_bad),("orc_helm_nose_c",imodbits_orc_good)],itp_type_head_armor|itp_shop,0,200,weight(2)|abundance(90)|head_armor(18)|body_armor(0)|difficulty(8),imodbits_orc_armor | imodbit_cracked],
["orc_kettlehelm","Orc_Kettlehelm",[("orc_helm_kettle_b",0),("orc_helm_kettle_b",imodbit_plain),("orc_helm_kettle_a",imodbits_orc_bad),("orc_helm_kettle_c",imodbits_orc_good)],itp_type_head_armor|itp_shop,0,500,weight(3)|abundance(91)|head_armor(22)|body_armor(0)|difficulty(10),imodbits_orc_armor | imodbit_cracked],
["orc_buckethelm","Orc_Buckethelm",[("orc_helm_sallet_b",0),("orc_helm_sallet_b",imodbit_plain),("orc_helm_sallet_a",imodbits_orc_bad),("orc_helm_sallet_c",imodbits_orc_good)],itp_type_head_armor|itp_shop,0,650,weight(5)|abundance(92)|head_armor(25)|body_armor(0)|difficulty(12),imodbits_orc_armor | imodbit_cracked],
["orc_morion","Orc_Morion",[("orc_helm_morion_b",0),("orc_helm_morion_b",imodbit_plain),("orc_helm_morion_a",imodbits_orc_bad),("orc_helm_morion_c",imodbits_orc_good)],itp_type_head_armor|itp_shop,0,500,weight(4)|abundance(91)|head_armor(23)|body_armor(0)|difficulty(11),imodbits_orc_armor | imodbit_cracked],
["orc_beakhelm","Orc_Beakhelm",[("orc_helm_vulture_b",0),("orc_helm_vulture_b",imodbit_plain),("orc_helm_vulture_a",imodbits_orc_bad),("orc_helm_vulture_c",imodbits_orc_good),("orc_helm_crow",imodbit_lordly)],itp_type_head_armor|itp_shop,0,600,weight(4)|abundance(91)|head_armor(24)|body_armor(0)|difficulty(11),imodbits_orc_armor | imodbit_cracked |imodbit_lordly],
["orc_bughelm","Orc_Bughelm",[("orc_helm_bug_b",0),("orc_helm_bug_b",imodbit_plain),("orc_helm_bug_a",imodbits_orc_bad),("orc_helm_bug_c",imodbits_orc_good),("orc_helm_bug_d",imodbit_lordly)],itp_type_head_armor|itp_shop,0,650,weight(5)|abundance(92)|head_armor(25)|body_armor(0)|difficulty(12),imodbits_orc_armor | imodbit_cracked| imodbit_lordly],
["orc_visorhelm","Orc_Visorhelm",[("orc_helm_visor_b",0),("orc_helm_visor_b",imodbit_plain),("orc_helm_visor_a",imodbits_orc_bad),("orc_helm_visor_c",imodbits_orc_good)],itp_type_head_armor|itp_shop,0,600,weight(4)|abundance(91)|head_armor(24)|body_armor(0)|difficulty(11),imodbits_orc_armor | imodbit_cracked],
["free_orc_helm_g","oldOrc_Crowhelm",[("orc_helm_crow",0)],itp_type_head_armor|itp_shop,0,400,weight(3)|head_armor(23)|difficulty(0),imodbits_orc_armor | imodbit_cracked],
["free_orc_helm_i","oldOrc_Snouthelm",[("orc_helm_sallet_b",0)],itp_type_head_armor|itp_shop,0,600,weight(3)|head_armor(25)|difficulty(0),imodbits_orc_armor | imodbit_cracked],
["free_orc_helm_j","oldOrc_Lizardhelm",[("orc_helm_visor_b",0)],itp_type_head_armor|itp_shop,0,400,weight(3)|head_armor(23)|difficulty(0),imodbits_orc_armor | imodbit_cracked],
["free_orc_helm_k","oldOrc_Vulturehelm",[("orc_helm_vulture_b",0)],itp_type_head_armor|itp_shop,0,500,weight(3)|head_armor(24)|difficulty(0),imodbits_orc_armor | imodbit_cracked],
#MORDOR ITEMS##########
###ORC ARMORS##########
["m_orc_light_a","Mordor_Orc_Light_Armor",[("orc_mordor_a",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,31,weight(1.5)|head_armor(0)|body_armor(5)|leg_armor(3)|difficulty(0),imodbits_orc_cloth,],
["m_orc_light_b","Mordor_Orc_Light_Armor",[("orc_mordor_b",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,51,weight(5)|head_armor(0)|body_armor(7)|leg_armor(5)|difficulty(0),imodbits_orc_cloth,],
["m_orc_light_c","Mordor_Orc_Light_Armor",[("orc_mordor_c",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,101,weight(6)|head_armor(0)|body_armor(8)|leg_armor(6)|difficulty(0),imodbits_orc_cloth,],
["m_orc_light_d","Mordor_Orc_Light_Armor",[("orc_mordor_d",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,501,weight(12)|head_armor(0)|body_armor(13)|leg_armor(5)|difficulty(0),imodbits_orc_cloth,],
["m_orc_light_e","Mordor_Orc_Light_Armor",[("orc_mordor_e",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,501,weight(14)|head_armor(0)|body_armor(13)|leg_armor(6)|difficulty(0),imodbits_orc_cloth,],
["m_orc_heavy_a","Mordor_Orc_Heavy_Armor",[("orc_mordor_f",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,601,weight(22)|abundance(91)|head_armor(0)|body_armor(17)|leg_armor(8)|difficulty(12),imodbits_orc_cloth,],
["m_orc_heavy_b","Mordor_Orc_Heavy_Armor",[("orc_mordor_g",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,601,weight(24)|abundance(91)|head_armor(0)|body_armor(18)|leg_armor(7)|difficulty(13),imodbits_orc_armor,],
["m_orc_heavy_c","Mordor_Orc_Heavy_Armor",[("orc_mordor_h",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,701,weight(26)|abundance(92)|head_armor(0)|body_armor(18)|leg_armor(8)|difficulty(13),imodbits_orc_armor,],
["m_orc_heavy_d","Mordor_Orc_Heavy_Armor",[("orc_mordor_i",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,801,weight(28)|abundance(94)|head_armor(0)|body_armor(20)|leg_armor(8)|difficulty(15),imodbits_orc_armor,],
["m_orc_heavy_e","Mordor_Orc_Heavy_Armor",[("orc_mordor_j",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,901,weight(31)|abundance(95)|head_armor(0)|body_armor(20)|leg_armor(10)|difficulty(15),imodbits_orc_armor,],
["m_uruk_light_a","Uruk_Harness",[("uruk_mordor_harness_c",imodbit_plain),("uruk_mordor_harness_c",0),("uruk_mordor_harness_c",imodbits_orc_bad),("uruk_mordor_harness_c",imodbits_orc_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,142,weight(8)|abundance(90)|head_armor(0)|body_armor(9)|leg_armor(3)|difficulty(6),imodbits_orc_cloth,],
["m_uruk_light_b","Uruk_Leather_Armor",[("uruk_mordor_light_leather_b",imodbit_plain),("uruk_mordor_light_leather_b",0),("uruk_mordor_light_leather_a",imodbits_orc_bad),("uruk_mordor_light_leather_c",imodbits_orc_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,282,weight(16)|abundance(91)|head_armor(0)|body_armor(12)|leg_armor(5)|difficulty(8),imodbits_orc_cloth,],
["m_uruk_light_c","Uruk_Light_Mail",[("uruk_mordor_light_mail_b",imodbit_plain),("uruk_mordor_light_mail_b",0),("uruk_mordor_light_mail_a",imodbits_orc_bad),("uruk_mordor_light_mail_c",imodbits_orc_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,502,weight(23)|abundance(92)|head_armor(0)|body_armor(18)|leg_armor(5)|difficulty(10),imodbits_orc_cloth,],
["m_uruk_med_a","Uruk_Heavy_Leather",[("uruk_mordor_heavy_leather_b",imodbit_plain),("uruk_mordor_heavy_leather_b",0),("uruk_mordor_heavy_leather_a",imodbits_orc_bad),("uruk_mordor_heavy_leather_c",imodbits_orc_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,902,weight(25)|abundance(93)|head_armor(0)|body_armor(20)|leg_armor(10)|difficulty(12),imodbits_orc_cloth,],
["m_uruk_med_b","Uruk_Heavy_Mail",[("uruk_mordor_heavy_mail_b",imodbit_plain),("uruk_mordor_heavy_mail_b",0),("uruk_mordor_heavy_mail_a",imodbits_orc_bad),("uruk_mordor_heavy_mail_c",imodbits_orc_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1102,weight(29)|abundance(95)|head_armor(0)|body_armor(24)|leg_armor(9)|difficulty(13),imodbits_orc_armor,],
["m_uruk_med_c","Uruk_Light_Scale",[("uruk_mordor_light_scale_b",imodbit_plain),("uruk_mordor_light_scale_b",0),("uruk_mordor_light_scale_a",imodbits_orc_bad),("uruk_mordor_light_scale_c",imodbits_orc_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,802,weight(26)|abundance(94)|head_armor(0)|body_armor(22)|leg_armor(6)|difficulty(14),imodbits_orc_armor,],
["m_uruk_heavy_a","Uruk_Heavy_Scale",[("uruk_mordor_heavy_scale_b",imodbit_plain),("uruk_mordor_heavy_scale_b",0),("uruk_mordor_heavy_scale_a",imodbits_orc_bad),("uruk_mordor_heavy_scale_c",imodbits_orc_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1202,weight(33)|abundance(95)|head_armor(0)|body_armor(27)|leg_armor(8)|difficulty(16),imodbits_orc_armor,],
["m_uruk_heavy_b","Uruk_Platemail",[("uruk_mordor_platemail_b",imodbit_plain),("uruk_mordor_platemail_b",0),("uruk_mordor_platemail_a",imodbits_orc_bad),("uruk_mordor_platemail_c",imodbits_orc_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1502,weight(35)|abundance(96)|head_armor(0)|body_armor(29)|leg_armor(10)|difficulty(18),imodbits_orc_armor,],
["m_uruk_heavy_c","Lugburz_Platemail",[("uruk_mordor_segmented_b",imodbit_plain),("uruk_mordor_segmented_b",0),("uruk_mordor_segmented_a",imodbits_orc_bad),("uruk_mordor_segmented_c",imodbits_orc_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1802,weight(38)|abundance(97)|head_armor(0)|body_armor(32)|leg_armor(10)|difficulty(20),imodbits_armor|imodbit_lordly,],
#next two free, Mai 2018
["free_m_uruk_heavy_j","Uruk_Heavy_Armor",[("uruk_mordor_platemail_a",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2000,weight(26)|head_armor(0)|body_armor(24)|leg_armor(10)|difficulty(0),imodbits_armor|imodbit_lordly,],
["free_m_uruk_heavy_k","Uruk_Guard_Armor",[("uruk_mordor_segmented_a",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2500,weight(28)|head_armor(0)|body_armor(26)|leg_armor(12)|difficulty(0),imodbits_armor|imodbit_lordly,],
["m_cap_armor","Mordor_Captain_Armor",[("mordor_captain_armor",0)],itp_type_body_armor|itp_covers_legs|itp_unique,0,3600,weight(37)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(18)|difficulty(20),imodbits_armor|imodbit_lordly,],
["black_num_armor","Black_Numenorean_Armor",[("black_numenor_armor",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,3600,weight(37)|abundance(97)|head_armor(0)|body_armor(42)|leg_armor(18)|difficulty(20),imodbits_armor|imodbit_lordly,],
["m_armor_a","Mordor_Armor",[("mordor_armor_a",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2000,weight(26)|abundance(94)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(16),imodbits_armor|imodbit_lordly,],
["m_armor_b","Mordor_Armor",[("mordor_armor_b",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2000,weight(26)|abundance(94)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(16),imodbits_armor|imodbit_lordly,],
["evil_light_armor","Sinister_Garb",[("evil_light_armor",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,400,weight(18)|head_armor(0)|body_armor(15)|leg_armor(10)|difficulty(0),imodbits_orc_cloth,],
######HELMS##########
["uruk_helm_a","Uruk_Helm",[("uruk_helm_a",0)],itp_type_head_armor|itp_shop,0,700,weight(4)|abundance(92)|head_armor(27)|body_armor(0)|difficulty(13),imodbits_orc_armor | imodbit_cracked],
["uruk_helm_b","Uruk_Helm",[("uruk_helm_b",0)],itp_type_head_armor|itp_shop,0,850,weight(5)|abundance(93)|head_armor(29)|body_armor(0)|difficulty(14),imodbits_orc_armor | imodbit_cracked],
["uruk_helm_c","Uruk_Beak_Helm",[("uruk_helm_c",0)],itp_type_head_armor|itp_shop,0,700,weight(4)|abundance(92)|head_armor(27)|body_armor(0)|difficulty(13),imodbits_orc_armor | imodbit_cracked],
["uruk_helm_d","Uruk_Grill_Helm",[("uruk_helm_d",0)],itp_type_head_armor|itp_shop,0,800,weight(4)|abundance(93)|head_armor(28)|body_armor(0)|difficulty(14),imodbits_orc_armor | imodbit_cracked],
["uruk_helm_e","Uruk_Mask_Helm",[("uruk_helm_e",0)],itp_type_head_armor|itp_shop,0,100,weight(6)|abundance(95)|head_armor(32)|body_armor(0)|difficulty(16),imodbits_orc_armor | imodbit_cracked],
["uruk_helm_f","Uruk_Helm",[("uruk_helm_f",0)],itp_type_head_armor|itp_shop,0,900,weight(5)|abundance(94)|head_armor(30)|body_armor(0)|difficulty(15),imodbits_orc_armor | imodbit_cracked],
#####HELMS##########
["mordor_cap_helm","Mordor_Captain_Helm",[("mordor_captain_helmet",0)],itp_type_head_armor|itp_shop,0,1700,weight(9)|abundance(97)|head_armor(41)|body_armor(0)|difficulty(20),imodbits_armor|imodbit_lordly],
["mordor_helm","Mordor_Helm",[("mordor_helmet_a",0)],itp_type_head_armor|itp_shop,0,1100,weight(5)|abundance(93)|head_armor(33)|body_armor(0)|difficulty(16),imodbits_orc_armor | imodbit_cracked],
["black_num_helm","Black_Numenorean_Helm",[("black_numenor_helmet",0)],itp_type_head_armor|itp_shop,0,1500,weight(7)|abundance(96)|head_armor(38)|body_armor(0)|difficulty(20),imodbits_armor|imodbit_lordly],
#######WEAPONS##########
["mordor_sword","Bastard_Sword_of_Mordor",[("mordor_sword_giles",0),("scab_mordor_sword_giles",ixmesh_carry)],itp_type_two_handed_wpn|itp_primary|itp_penalty_with_shield|itp_shop,itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,700,weight(2.25)|abundance(94)|difficulty(11)|spd_rtng(101)|weapon_length(109)|swing_damage(37,cut)|thrust_damage(26,pierce),imodbits_weapon_bad],
["mordor_longsword","Sword_of_Mordor",[("sword_of_mordor_giles",0),("scab_sword_of_mordor_giles",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,650,weight(2.75)|abundance(96)|difficulty(10)|spd_rtng(97)|weapon_length(94)|swing_damage(34,cut)|thrust_damage(31,pierce),imodbits_weapon_bad],

##MORIA ITEMS##########
#########ARMORS##########
["moria_armor_a","Moria_Breast_Harness",[("orc_moria_a",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,51,weight(8)|head_armor(0)|body_armor(6)|leg_armor(4)|difficulty(0),imodbits_orc_armor | imodbit_cracked,],
["moria_armor_b","Moria_Breast_and_Shoulders",[("orc_moria_b",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,261,weight(15)|head_armor(0)|body_armor(10)|leg_armor(6)|difficulty(0),imodbits_orc_armor | imodbit_cracked,],
["moria_armor_c","Moria_Orc_Mail",[("orc_moria_c",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,501,weight(26)|abundance(92)|head_armor(0)|body_armor(16)|leg_armor(7)|difficulty(12),imodbits_orc_armor,],
["moria_armor_d","Moria_Bolted_Leather",[("orc_moria_d",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,801,weight(27)|abundance(93)|head_armor(0)|body_armor(18)|leg_armor(10)|difficulty(13),imodbits_orc_armor,],
["moria_armor_e","Moria_Orc_Heavy_Mail",[("orc_moria_e",0),("uruk_mordor_light_mail_a_orc",imodbit_sturdy),("uruk_mordor_heavy_mail_b_orc",imodbit_reinforced),("uruk_mordor_platemail_a_orc",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1201,weight(30)|abundance(95)|head_armor(0)|body_armor(23)|leg_armor(11)|difficulty(16),imodbits_armor,],
#######SHIELDS##########
["moria_orc_shield_a","Moria_Great_Shield",[("moria_orc_shield_a",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,500,weight(5)|abundance(93)|difficulty(4)|hit_points(330)|body_armor(18)|spd_rtng(86)|weapon_length(60),imodbits_shield,],
["moria_orc_shield_b","Moria_Orc_Shield",[("moria_orc_shield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,300,weight(3)|abundance(91)|difficulty(1)|hit_points(300)|body_armor(15)|spd_rtng(92)|weapon_length(40),imodbits_shield,],
["moria_orc_shield_c","Moria_Orc_Shield",[("moria_orc_shield_c",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,300,weight(3)|abundance(91)|difficulty(1)|hit_points(300)|body_armor(15)|spd_rtng(92)|weapon_length(40),imodbits_shield,],

###GUNDABAD ITEMS##########
#ARMORS##########
["gundabad_armor_a","Gundabad_Orc_Rags",[("orc_gunda_a",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,41,weight(2)|head_armor(0)|body_armor(5)|leg_armor(4)|difficulty(0),imodbits_orc_cloth,],
["gundabad_armor_b","Gundabad_Orc_Fur",[("orc_gunda_b",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,251,weight(5)|head_armor(0)|body_armor(9)|leg_armor(6)|difficulty(0),imodbits_orc_cloth,],
["gundabad_armor_c","Gundabad_Orc_Armor",[("orc_gunda_c",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,401,weight(9)|abundance(91)|head_armor(0)|body_armor(14)|leg_armor(7)|difficulty(9),imodbits_orc_armor,],
["gundabad_armor_d","Gundabad_Orc_Armor",[("orc_gunda_d",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,601,weight(13)|abundance(92)|head_armor(0)|body_armor(16)|leg_armor(8)|difficulty(12),imodbits_orc_armor,],
["gundabad_armor_e","Gundabad_Orc_Heavy_Armor",[("orc_gunda_e",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,801,weight(15)|abundance(94)|head_armor(0)|body_armor(20)|leg_armor(8)|difficulty(14),imodbits_orc_armor,],
#HELMS##########
["gundabad_helm_a","Leather_Cap",[("orc_gunda_cap",0)],itp_type_head_armor|itp_shop,0,50,weight(1)|abundance(90)|head_armor(12)|body_armor(0)|difficulty(0),imodbits_orc_cloth],
["gundabad_helm_b","Leather_Helm",[("orc_gunda_helm_a",0)],itp_type_head_armor|itp_shop,0,300,weight(2)|abundance(90)|head_armor(18)|body_armor(0)|difficulty(0),imodbits_orc_cloth],
["gundabad_helm_c","Gundabad_Helm",[("orc_gunda_helm_b",0)],itp_type_head_armor|itp_shop,0,500,weight(2)|abundance(91)|head_armor(22)|body_armor(0)|difficulty(10),imodbits_orc_armor | imodbit_cracked],
["gundabad_helm_d","Gundabad_Helm",[("orc_gunda_helm_c",0)],itp_type_head_armor|itp_shop,0,500,weight(2)|abundance(91)|head_armor(23)|body_armor(0)|difficulty(11),imodbits_orc_armor | imodbit_cracked],
["gundabad_helm_e","Wargrider_Helm",[("orc_wargrider_helm",0)],itp_type_head_armor|itp_fit_to_head,0,600,weight(2)|abundance(93)|head_armor(25)|body_armor(0)|difficulty(12),imodbits_orc_armor | imodbit_cracked],


####DUNLAND ITEMS##########
["dunland_wolfboots","Dunland_Wolfboots",[("dunland_wolfboots",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,300,weight(2)|abundance(91)|leg_armor(12)|difficulty(0),imodbits_cloth],
##ARMORS########
["free_dunland_armor_a","Dunnish_Fur_Armor",[("dunland_tunic_1a",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,50,weight(6)|head_armor(1)|body_armor(10)|leg_armor(4)|difficulty(0),imodbits_cloth,],
["free_dunland_armor_b","Dunnish_Fur_Armor",[("dunland_tunic_2a",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,400,weight(7)|head_armor(1)|body_armor(12)|leg_armor(8)|difficulty(0),imodbits_cloth,],
["free_dunland_armor_c","Dunnish_Fur_Armor",[("dunland_fur_1a",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,400,weight(7)|head_armor(1)|body_armor(12)|leg_armor(8)|difficulty(0),imodbits_cloth,],
["dunland_tunic_1","Dunnish_Leather_Tunic",[("dunland_tunic_1b",imodbit_plain),("dunland_tunic_1b",0),("dunland_tunic_1a",imodbits_armor_bad),("dunland_tunic_1c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,50,weight(4)|abundance(92)|head_armor(2)|body_armor(8)|leg_armor(5)|difficulty(9),imodbits_armor,],
["dunland_tunic_2","Dunnish_Leather_Tunic",[("dunland_tunic_2b",imodbit_plain),("dunland_tunic_2b",0),("dunland_tunic_2a",imodbits_armor_bad),("dunland_tunic_2c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,60,weight(4)|abundance(92)|head_armor(2)|body_armor(9)|leg_armor(6)|difficulty(9),imodbits_armor,],
["dunland_fur_1","Dunnish_Fur",[("dunland_fur_2a",imodbit_plain),("dunland_fur_2a",0),("dunland_fur_1a",imodbits_armor_bad),("dunland_fur_2b",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,250,weight(6)|abundance(92)|head_armor(2)|body_armor(13)|leg_armor(7)|difficulty(9),imodbits_armor,],
["dunland_fur_2","Dunnish_Fur",[("dunland_fur_3b",imodbit_plain),("dunland_fur_3b",0),("dunland_fur_3a",imodbits_armor_bad),("dunland_fur_3c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,350,weight(8)|abundance(92)|head_armor(2)|body_armor(16)|leg_armor(7)|difficulty(9),imodbits_armor,],
["dunland_mail_1","Dunnish_Hauberk",[("dunland_hauberk_1b",imodbit_plain),("dunland_hauberk_1b",0),("dunland_hauberk_1a",imodbits_armor_bad),("dunland_hauberk_1c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,800,weight(23)|abundance(92)|head_armor(2)|body_armor(22)|leg_armor(7)|difficulty(12),imodbits_armor,],
["dunland_mail_2","Dunnish_Hauberk",[("dunland_hauberk_2b",imodbit_plain),("dunland_hauberk_2b",0),("dunland_hauberk_2a",imodbits_armor_bad),("dunland_hauberk_2c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1000,weight(23)|abundance(92)|head_armor(2)|body_armor(22)|leg_armor(10)|difficulty(12),imodbits_armor,],
["dunland_chieftain","Dunnish_Chief_Armor",[("dunland_chieftain_b",imodbit_plain),("dunland_chieftain_b",0),("dunland_chieftain_a",imodbits_armor_bad),("dunland_chieftain_c",imodbits_armor_good), ("dunland_chieftain_spirit",imodbit_old),("barf_skeleton_greaves", imodbit_poor)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1800,weight(26)|abundance(93)|head_armor(2)|body_armor(30)|leg_armor(13)|difficulty(14),imodbits_armor|imodbit_lordly,],
#######HELMS##########
["dun_helm_a","Dunnish_Wolf_Cap",[("dunland_wolfcap",0)],itp_type_head_armor|itp_shop,0,600,weight(1)|abundance(92)|head_armor(25)|body_armor(0)|difficulty(12),imodbits_cloth],
["dun_helm_b","Dunnish_Fur_Cap",[("dunland_furcap_1",imodbits_armor_bad),("dunland_furcap_2",imodbit_plain),("dunland_furcap_2",0),("dunland_antlercap",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,400,weight(1)|abundance(91)|head_armor(21)|body_armor(0)|difficulty(10),imodbits_cloth],
["dun_helm_c","Dunnish_Tall_Helm",[("dunland_helm_a",imodbits_armor_bad),("dunland_helm_b",imodbit_plain),("dunland_helm_b",0),("dunland_helm_c",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,900,weight(2)|abundance(93)|head_armor(30)|body_armor(0)|difficulty(16),imodbits_armor | imodbit_cracked],
["free_dun_helm_d","Dunnish_Tall_Helm",[("dunland_helm_b",0)],itp_type_head_armor|itp_shop,0,900,weight(2)|abundance(93)|head_armor(30)|body_armor(0)|difficulty(16),imodbits_armor | imodbit_cracked],
["free_dun_helm_e","Dunnish_Antler_Helm",[("dunland_helm_c",0)],itp_type_head_armor|itp_shop,0,1200,weight(4)|abundance(94)|head_armor(35)|body_armor(0)|difficulty(17),imodbits_armor|imodbit_lordly],
#["dun_helm_f", "Dunnish Helm",[("dunland_helm_c",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
#######SHIELDS##########
["dun_shield_a","Dunnish_Roundshield",[("dun_roundshield",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,300,weight(2)|abundance(90)|difficulty(2)|hit_points(290)|body_armor(15)|spd_rtng(88)|weapon_length(55),imodbits_shield,],
["dun_shield_b","Dunnish_Oval_Shield",[("dun_roundshield_b_new",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,300,weight(3.5)|abundance(90)|difficulty(2)|hit_points(320)|body_armor(13)|spd_rtng(82)|weapon_length(65),imodbits_shield,],
#["dun_shield_c", "Dunnish Shield",[("dunland_shield_c",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["dun_shield_z", "Dunnish Shield",[("dunland_shield_d",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["dun_shield_e", "Dunnish Shield",[("dunland_shield_e",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["dun_shield_f", "Dunnish Shield",[("dunland_shield_f_spike",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["dun_shield_g", "Dunnish Shield",[("dunland_shield_g",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#WEAPONS##########
["dun_berserker","Dunland_Chieftain_Sword",[("dunland_sword_1",0),("dunland_sword_1_scab",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_crush_through,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,540,weight(3)|abundance(95)|difficulty(12)|spd_rtng(97)|weapon_length(98)|swing_damage(32,cut)|thrust_damage(18,pierce),imodbits_weapon_bad|imodbits_weapon_bad_heavy],
["dunnish_antler_axe","Dunnish_Antler_Axe",[("dunland_antleraxe",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,300,weight(2)|abundance(90)|difficulty(0)|spd_rtng(85)|weapon_length(73)|swing_damage(35,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["dunnish_war_axe","Dunnish_War_Axe",[("dunland_axe_a",0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,360,weight(2)|abundance(92)|difficulty(11)|spd_rtng(97)|weapon_length(50)|swing_damage(40,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["dunnish_axe","Dunnish_Axe",[("dunland_axe_b",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,320,weight(2)|abundance(91)|difficulty(0)|spd_rtng(100)|weapon_length(50)|swing_damage(35,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["dunland_spear","Dunnish_Spear",[("dunland_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable,itc_lance_upstab,150,weight(2)|abundance(90)|difficulty(0)|spd_rtng(95)|weapon_length(150)|thrust_damage(20,pierce),imodbits_weapon_wood],
["dunnish_pike","Dunnish_Pike",[("dunland_pike_2",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_cant_use_on_horseback|itp_penalty_with_shield|itp_wooden_parry,itc_lance_upstab,250,weight(3)|abundance(91)|difficulty(10)|spd_rtng(85)|weapon_length(205)|thrust_damage(26,pierce),imodbits_weapon_wood],


####ROHAN ITEMS##########
########ARMORS########## #free Dec 2018
["free_rohan_armor_a","Rohan_Shirt",[("rohan_recruit_poor",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,50,weight(2)|head_armor(0)|body_armor(3)|leg_armor(2)|difficulty(0),imodbits_cloth,],
["free_rohan_armor_b","Rohan_Shirt_Cape",[("rohan_recruit_poor",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,400,weight(3)|head_armor(0)|body_armor(5)|leg_armor(3)|difficulty(0),imodbits_cloth,],
["free_rohan_armor_c","Rohan_Long_Shirt",[("rohan_recruit_poor",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,500,weight(5)|head_armor(0)|body_armor(8)|leg_armor(5)|difficulty(0),imodbits_cloth,],
["free_rohan_armor_d","Rohan_Hauberk",[("rohan_mail",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,800,weight(12)|head_armor(0)|body_armor(20)|leg_armor(9)|difficulty(0),imodbits_armor,],
##WEAPONS##########
["rohan_cav_sword","Rohan_Riding_Sword",[("rohan_sword_a",0),("scab_rohan_sword_a",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,540,weight(1.5)|abundance(93)|difficulty(0)|spd_rtng(99)|weapon_length(95)|swing_damage(31,cut)|thrust_damage(21,pierce),imodbits_weapon],
["rohan_inf_sword","Rohan_Sword",[("rohan_sword_b",0),("scab_rohan_sword_b",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,530,weight(1.25)|abundance(92)|difficulty(0)|spd_rtng(100)|weapon_length(95)|swing_damage(29,cut)|thrust_damage(22,pierce),imodbits_weapon],
["rohan_spear","Rohan_Spear",[("rohan_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry,itc_spear_upstab,300,weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(92)|weapon_length(170)|thrust_damage(29,pierce)|swing_damage(16,blunt),imodbits_weapon_wood],
["rohan_lance","Rohan_Lance",[("rohan_lance",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable,itc_pike,500,weight(2.5)|abundance(92)|difficulty(11)|spd_rtng(88)|weapon_length(208)|thrust_damage(26,pierce),imodbits_weapon_wood],
#rohan_lance_standard
["rohan_sword_c","Rohan_Sword",[("rohan_sword_c",0),("scab_rohan_sword_c",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,520,weight(1.25)|abundance(91)|difficulty(0)|spd_rtng(99)|weapon_length(96)|swing_damage(29,cut)|thrust_damage(21,pierce),imodbits_weapon],
["rohirrim_short_axe","Rohirrim_Short_Axe",[("rohan_1haxe",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_secondary|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,300,weight(2)|abundance(90)|difficulty(0)|spd_rtng(100)|weapon_length(50)|swing_damage(35,cut)|thrust_damage(0,pierce),imodbits_weapon],
["rohirrim_long_hafted_axe","Rohirrim_Long_Hafted_Axe",[("rohan_2haxe",0)],itp_type_two_handed_wpn|itp_primary|itp_shop|itp_penalty_with_shield|itp_bonus_against_shield|itp_wooden_parry|itp_crush_through|itp_unbalanced,itc_bastardfalchion|itcf_carry_axe_left_hip,440,weight(4.5)|abundance(92)|difficulty(12)|spd_rtng(100)|weapon_length(76)|swing_damage(40,cut)|thrust_damage(0,pierce),imodbits_weapon],
["rohan_2h_sword","Rohan_War_Sword",[("rohan_sword_a_2h",0)],itp_type_two_handed_wpn|itp_primary|itp_penalty_with_shield|itp_shop,itc_bastardsword|itcf_carry_sword_back,700,weight(3)|abundance(93)|difficulty(13)|spd_rtng(104)|weapon_length(103)|swing_damage(39,cut)|thrust_damage(31,pierce),imodbits_weapon],

["rohan_recruit","Rohan_Padded_Jerkin",[("rohan_padded_1",imodbits_armor_bad),("rohan_lamellar",imodbit_plain),("rohan_padded_2",0),("rohan_padded_3",imodbit_thick)],itp_type_body_armor|itp_covers_legs|itp_shop,0,50,weight(4)|head_armor(0)|body_armor(8)|leg_armor(2)|difficulty(0),imodbits_cloth,],
["rohan_leather","Rohan_Leather_Vest",[("rohan_lamellar_poor",imodbits_armor_bad),("rohan_lamellar",imodbit_plain),("rohan_lamellar",0),("rohan_lamellar_cape",imodbit_cloak),("rohan_lamellar_reinforced",imodbit_thick|imodbit_reinforced)],itp_type_body_armor|itp_covers_legs|itp_shop,0,300,weight(9)|head_armor(0)|body_armor(13)|leg_armor(9)|difficulty(0),imodbits_armor|imodbit_cloak,],
["rohan_mail","Rohan_Hauberk",[("rohan_mail_poor",imodbits_armor_bad),("rohan_mail",imodbit_plain),("rohan_mail",0),("rohan_mail_cape",imodbit_cloak),("rohan_mail_reinforced",imodbit_thick),("rohan_mail_reinforced_cape",imodbit_reinforced|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1225,weight(24)|abundance(91)|head_armor(0)|body_armor(24)|leg_armor(11)|difficulty(10),imodbits_armor|imodbit_lordly|imodbit_cloak,],
["rohan_rider","Rohan_Rider_Armor",[("rohan_rider_poor",imodbits_armor_bad),("rohan_rider",imodbit_plain),("rohan_rider",0),("rohan_rider_cape",imodbit_cloak),("rohan_rider_reinforced",imodbit_thick),("rohan_rider_reinforced_cape",imodbit_reinforced|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1600,weight(27)|abundance(91)|head_armor(0)|body_armor(27)|leg_armor(13)|difficulty(12),imodbits_armor|imodbit_lordly|imodbit_cloak,],
["rohan_scale","Rohan_Scale_Armor",[("rohan_scale_poor",imodbits_armor_bad),("rohan_scale",imodbit_plain),("rohan_scale",0),("rohan_scale_cape",imodbit_cloak),("rohan_scale_reinforced",imodbit_thick),("rohan_scale_reinforced_cape",imodbit_reinforced|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2000,weight(30)|abundance(92)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(16),imodbits_armor|imodbit_lordly|imodbit_cloak,],
["rohan_surcoat","Rohan_Surcoat",[("rohan_tabard_poor",imodbits_armor_bad),("rohan_tabard",imodbit_plain),("rohan_tabard",0),("rohan_tabard_cape",imodbit_cloak),("rohan_tabard_reinforced",imodbit_thick),("rohan_tabard_reinforced_cape",imodbit_reinforced|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2600,weight(34)|abundance(94)|head_armor(0)|body_armor(36)|leg_armor(15)|difficulty(18),imodbits_armor|imodbit_lordly|imodbit_cloak,],
["rohan_guard","Rohan_Guard_Armor",[("rohan_royal_guard_armor2",imodbits_armor_bad),("rohan_royal_guard_armor1",imodbit_plain),("rohan_royal_guard_armor1",0),("rohan_royal_guard_armor1_cape",imodbit_cloak),("rohan_royal_guard_armor1_lordly",imodbits_armor_good|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,3000,weight(38)|abundance(95)|head_armor(0)|body_armor(38)|leg_armor(17)|difficulty(20),imodbits_armor|imodbit_lordly|imodbit_cloak,],
##HELMS##########
["rohan_light_helmet_a","Rohan_Light_Helm",[("rohan_recruit_helm_a",imodbits_armor_bad),("rohan_recruit_helm_b",imodbit_plain),("rohan_recruit_helm_b",0),("rohan_recruit_helm_c",imodbits_armor_good|imodbit_lordly)],itp_type_head_armor|itp_shop,0,500,weight(1.5)|abundance(91)|head_armor(26)|body_armor(0)|difficulty(9),imodbits_armor| imodbit_cracked],
["rohan_light_helmet_b","Rohan_Light_Helm",[("rohan_light_helmet_a",imodbits_armor_bad),("rohan_light_helmet_b",imodbit_plain),("rohan_light_helmet_b",0),("rohan_light_helmet_b",imodbits_armor_good|imodbit_lordly)],itp_type_head_armor|itp_shop,0,600,weight(1.5)|abundance(92)|head_armor(28)|body_armor(0)|difficulty(10),imodbits_armor | imodbit_cracked],
["rohan_inf_helmet_a","Rohan_Eyeguard_Helm",[("rohan_inf_helmet_a",imodbits_armor_bad),("rohan_inf_helmet_b",imodbit_plain),("rohan_inf_helmet_b",0),("rohan_inf_helmet_c",imodbits_armor_good),("rohan_captain_helmet",imodbit_lordly)],itp_type_head_armor|itp_shop,0,1100,weight(3)|abundance(94)|head_armor(33)|body_armor(0)|difficulty(12),imodbits_armor | imodbit_cracked|imodbit_lordly],
["rohan_inf_helmet_b","Rohan_Eyeguard_Helm",[("rohan_eye_helm_a",imodbits_armor_bad),("rohan_eye_helm_b",imodbit_plain),("rohan_eye_helm_b",0),("rohan_eye_helm_c",imodbits_armor_good|imodbit_lordly)],itp_type_head_armor|itp_shop,0,1100,weight(3)|abundance(94)|head_armor(33)|body_armor(0)|difficulty(12),imodbits_armor | imodbit_cracked|imodbit_lordly],
["rohan_archer_helmet_a","Rohan_Nasal_Helm",[("rohan_archer_helmet_a",imodbits_armor_bad),("rohan_archer_helmet_b",imodbit_plain),("rohan_archer_helmet_b",0),("rohan_archer_helm_d",imodbits_armor_good|imodbit_lordly)],itp_type_head_armor|itp_shop,0,1000,weight(3)|abundance(93)|head_armor(31)|body_armor(0)|difficulty(11),imodbits_armor | imodbit_cracked|imodbit_lordly],
["rohan_archer_helmet_b","Rohan_Nasal_Helm",[("rohan_nasal_helm_a",imodbits_armor_bad),("rohan_nasal_helm_b",imodbit_plain),("rohan_nasal_helm_b",0),("rohan_nasal_helm_c",imodbits_armor_good|imodbit_lordly)],itp_type_head_armor|itp_shop,0,1000,weight(3)|abundance(93)|head_armor(31)|body_armor(0)|difficulty(11),imodbits_armor | imodbit_cracked|imodbit_lordly],
["rohan_archer_helmet_c","Rohan_Guard_Helm",[("rohan_guard_helm_a",imodbits_armor_bad),("rohan_guard_helm_b",imodbit_plain),("rohan_guard_helm_b",0),("rohan_guard_helm_c",imodbits_armor_good),("rohan_theoden_helm",imodbit_lordly)],itp_type_head_armor|itp_shop,0,1200,weight(5)|abundance(95)|head_armor(35)|body_armor(0)|difficulty(15),imodbits_armor | imodbit_cracked|imodbit_lordly],
#next 4 free, Dec 2018
["free_rohan_cav_helmet_a","Rohan_Cavalry_Helm",[("rohan_light_helmet_a",imodbits_armor_bad),("rohan_light_helmet_b",0),("rohan_light_helmet_b",imodbits_armor_good)],itp_type_head_armor,0,1300,weight(2)|head_armor(34)|difficulty(0),imodbits_armor | imodbit_cracked],
["free_rohan_cav_helmet_b","Rohan_Cavalry_Helm",[("rohan_light_helmet_a",imodbits_armor_bad),("rohan_light_helmet_b",0),("rohan_light_helmet_b",imodbits_armor_good)],itp_type_head_armor,0,1300,weight(2)|head_armor(34)|difficulty(0),imodbits_armor | imodbit_cracked],
["free_rohan_cav_helmet_c","Rohan_Cavalry_Helm",[("rohan_light_helmet_a",imodbits_armor_bad),("rohan_light_helmet_b",0),("rohan_light_helmet_b",imodbits_armor_good)],itp_type_head_armor,0,1500,weight(2)|head_armor(36)|difficulty(0),imodbits_armor|imodbit_lordly],
["free_rohan_captain_helmet","Rohan_Captain_Helm",[("rohan_captain_helmet",0)],itp_type_head_armor,0,3000,weight(3.5)|head_armor(40)|difficulty(0),imodbits_armor|imodbit_lordly],
##SHIELDS##########
["rohan_shield_a","Rohan_Shield",[("rohan_shield_green",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(3)|abundance(90)|difficulty(0)|hit_points(260)|body_armor(14)|spd_rtng(94)|weapon_length(40),imodbits_shield,[(ti_on_init_item,[(store_random_in_range,":p",0,7), (val_add,":p", "mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_plain_shield", ":p")])]],
["rohan_shield_b","Rohan_Shield",[("rohan_shield_red",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(3)|abundance(90)|difficulty(0)|hit_points(260)|body_armor(14)|spd_rtng(94)|weapon_length(40),imodbits_shield,[(ti_on_init_item,[(store_random_in_range,":p",0,7), (val_add,":p", "mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_plain_shield", ":p")])]],
["rohan_shield_c","Rohan_Shield",[("rohan_shield_plain",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(3)|abundance(90)|difficulty(0)|hit_points(260)|body_armor(14)|spd_rtng(94)|weapon_length(40),imodbits_shield,[(ti_on_init_item,[(store_random_in_range,":p",0,7), (val_add,":p", "mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_plain_shield", ":p")])]],
["rohan_shield_d","Rohan_Shield",[("rohan_shield_green_boss",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,400,weight(3.5)|abundance(92)|difficulty(1)|hit_points(300)|body_armor(16)|spd_rtng(90)|weapon_length(40),imodbits_shield,[(ti_on_init_item,[(store_random_in_range,":p",4,7), (val_add,":p", "mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_boss_shield" ,":p")])]],
["rohan_shield_e","Rohan_Shield",[("rohan_shield_red_boss",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,400,weight(3.5)|abundance(92)|difficulty(1)|hit_points(300)|body_armor(16)|spd_rtng(90)|weapon_length(40),imodbits_shield,[(ti_on_init_item,[(store_random_in_range,":p",4,7), (val_add,":p", "mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_boss_shield" ,":p")])]],
["rohan_shield_f","Rohan_Shield",[("rohan_shield_plain_boss",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,400,weight(3.5)|abundance(92)|difficulty(1)|hit_points(300)|body_armor(16)|spd_rtng(90)|weapon_length(40),imodbits_shield,[(ti_on_init_item,[(store_random_in_range,":p",4,7), (val_add,":p", "mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_boss_shield" ,":p")])]],
["rohan_shield_g","Rohan_Royal_Shield",[("rohan_shield_royal",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,600,weight(3.5)|abundance(95)|difficulty(2)|hit_points(330)|body_armor(18)|spd_rtng(90)|weapon_length(40),imodbits_shield_good,[(ti_on_init_item,[(store_random_in_range,":p",4,7), (val_add,":p", "mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_boss_shield" ,":p")])]],
##FOOTGEAR##########
["rohan_light_greaves","Rohan_Light_Greaves",[("rohan_scale_greaves",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,500,weight(4)|abundance(92)|leg_armor(18)|difficulty(0),imodbits_cloth],
["rohirrim_war_greaves","Rohirrim_War_Greaves",[("rohan_greaves",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,1500,weight(8)|abundance(94)|leg_armor(26)|difficulty(15),imodbits_armor|imodbit_lordly],
#free Dec 2019, also used by a lot of non-Rohan troops!
["free_rohan_shoes","Leather_Shoes",[("narf_rus_shoes",0)],itp_type_foot_armor|itp_shop|itp_attach_armature|itp_civilian,0,50,weight(1)|leg_armor(8)|difficulty(0),imodbits_cloth],
##WEAPONS########## #moved upwards Dec 2019, keep these for savegame compatibility
["free_rohan_cav_sword2","Rohan_Riding_Sword",[("rohan_sword_a",0),("scab_rohan_sword_a",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,500,weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(95)|swing_damage(31,cut)|thrust_damage(21,pierce),imodbits_weapon],
["free_rohan_inf_sword2","Rohan_Sword",[("rohan_sword_b",0),("scab_rohan_sword_b",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,500,weight(1.25)|difficulty(0)|spd_rtng(100)|weapon_length(95)|swing_damage(29,cut)|thrust_damage(22,pierce),imodbits_weapon],
["free_rohan_spear2","Rohan_Spear",[("rohan_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry,itc_spear_upstab,189,weight(2.5)|difficulty(0)|spd_rtng(92)|weapon_length(170)|swing_damage(16,blunt)|thrust_damage(29,pierce),imodbits_weapon_wood],
["free_rohan_lance2","Rohan_Lance",[("rohan_lance",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable,itc_pike,300,weight(2.5)|difficulty(0)|spd_rtng(88)|weapon_length(208)|thrust_damage(26,pierce),imodbits_weapon_wood],
["free_rohan_sword_c2","Rohan_Sword",[("rohan_sword_c",0),("scab_rohan_sword_c",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,500,weight(1.25)|difficulty(0)|spd_rtng(103)|weapon_length(96)|swing_damage(29,cut)|thrust_damage(21,pierce),imodbits_weapon],
["free_rohirrim_short_axe2","Rohirrim_Short_Axe",[("rohan_1haxe",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_secondary|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,500,weight(2)|difficulty(0)|spd_rtng(100)|weapon_length(50)|swing_damage(35,cut)|thrust_damage(0,pierce),imodbits_weapon],
["free_rohirrim_long_hafted_axe2","Rohirrim_Long_Hafted_Axe",[("rohan_2haxe",0)],itp_type_two_handed_wpn|itp_primary|itp_shop|itp_penalty_with_shield|itp_bonus_against_shield|itp_wooden_parry|itp_crush_through|itp_unbalanced,itc_bastardfalchion|itcf_carry_axe_left_hip,500,weight(4.5)|difficulty(0)|spd_rtng(92)|weapon_length(76)|swing_damage(35,cut)|thrust_damage(0,pierce),imodbits_weapon],
["free_rohan_2h_sword2","Rohan_War_Sword",[("rohan_sword_a_2h",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_shop|itp_cant_use_on_horseback,itc_greatsword|itcf_carry_sword_back,524,weight(3)|difficulty(0)|spd_rtng(94)|weapon_length(101)|swing_damage(40,cut)|thrust_damage(31,pierce),imodbits_weapon],

###TLD WOODELF ITEMS##########
#ARMORS##########
["mirkwood_leather","Woodelf_Leather_Armor",[("mirkwood_leather_b",0),("mirkwood_leather_a",imodbits_armor_bad),("mirkwood_leather_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,150,weight(2)|head_armor(0)|body_armor(16)|leg_armor(2)|difficulty(0),imodbits_armor|imodbit_lordly,],
["mirkwood_pad","Greenwood_Quilted_Coat",[("mirkwood_quiltedsurcoat_01",0),("mirkwood_quiltedsurcoat_01",imodbits_armor_bad),("mirkwood_quiltedsurcoat_01_b",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,800,weight(6)|head_armor(0)|body_armor(20)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly,],
["mirkwood_mail","Greenwood_Mail",[("mirkwood_maillewithsurcoat_01_b",0),("mirkwood_maillewithsurcoat_01",imodbits_armor_bad),("mirkwood_royal",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1800,weight(17)|abundance(94)|head_armor(0)|body_armor(29)|leg_armor(14)|difficulty(12),imodbits_armor|imodbit_lordly,],
["mirkwood_scale","Greenwood_Light_Scale",[("mirkwood_light_scale",0),("mirkwood_scalequilted_01",imodbits_armor_bad),("mirkwood_scalequilted_01b",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1400,weight(12)|abundance(93)|head_armor(0)|body_armor(26)|leg_armor(12)|difficulty(11),imodbits_armor|imodbit_lordly,],
["mirkwood_heavy_scale","Greenwood_Leafscale",[("mirkwood_scaleovermaille_01",0),],itp_type_body_armor|itp_covers_legs|itp_shop,0,2500,weight(23)|abundance(96)|head_armor(0)|body_armor(38)|leg_armor(12)|difficulty(15),imodbits_armor|imodbit_lordly,],
#next two free Jan 2020
["free_mirkwood_armor_e","Light_Mail_and_Surcoat",[("mirkwood_maillewithsurcoat_01",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2500,weight(17)|head_armor(0)|body_armor(25)|leg_armor(14)|difficulty(0),imodbits_armor|imodbit_lordly,],
#WEAPONS##########
["mirkwood_sword","Woodelf_Sword",[("mirkwood_shortsword",0),("scab_mirkwood_shortsword",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_primary|itp_secondary,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,500,weight(1.25)|abundance(92)|difficulty(0)|spd_rtng(103)|weapon_length(76)|swing_damage(29,cut)|thrust_damage(27,pierce),imodbits_weapon_bad],
["mirkwood_great_spear","Greenwood_Great_Spear",[("mirkwood_great_spear_large",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry,itc_spear_upstab,900,weight(2.5)|abundance(95)|difficulty(13)|spd_rtng(106)|weapon_length(150)|thrust_damage(35,pierce)|swing_damage(30,cut),imodbits_weapon_good],
["mirkwood_war_spear","Greenwood_War_Spear",[("mirkwood_war_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry,itc_spear_upstab,400,weight(2.5)|abundance(93)|difficulty(12)|spd_rtng(109)|weapon_length(150)|thrust_damage(31,pierce)|swing_damage(25,cut),imodbits_weapon_good],
["mirkwood_short_spear","Woodelf_Spear",[("mirkwood_short_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_wooden_parry,itc_spear_upstab,200,weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(104)|weapon_length(114)|thrust_damage(27,pierce)|swing_damage(15,blunt),imodbits_weapon_good],
["mirkwood_knife","Woodelf_Knife",[("mirkwood_white_knife",0),("scab_mirkwood_white_knife",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_primary|itp_secondary,itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn,100,weight(0.75)|abundance(90)|difficulty(0)|spd_rtng(120)|weapon_length(51)|swing_damage(24,cut)|thrust_damage(17,pierce),imodbits_weapon_bad],
["mirkwood_axe","Woodelf_Axe",[("mirkwood_axe",0),("mirkwood_axe_carry",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,150,weight(1)|abundance(91)|difficulty(0)|spd_rtng(115)|weapon_length(51)|swing_damage(30,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
#SHIELDS##########
["mirkwood_spear_shield_a","Woodelf_Shield",[("mirkwood_med_shield",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,300,weight(2)|abundance(90)|difficulty(1)|hit_points(290)|body_armor(16)|spd_rtng(95)|weapon_length(50),imodbits_shield_good,],
["mirkwood_spear_shield_b","Greenwood_War_Shield",[("mirkwood_spear_shield",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,600,weight(3)|abundance(93)|difficulty(3)|hit_points(320)|body_armor(15)|spd_rtng(86)|weapon_length(65),imodbits_shield_good,],
["mirkwood_spear_shield_c","Woodelf_Round_Shield",[("mirkwood_royal_round",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,700,weight(2)|abundance(94)|difficulty(2)|hit_points(300)|body_armor(18)|spd_rtng(93)|weapon_length(40),imodbits_shield_good,],
#HELMETS##########
["mirkwood_helm_a","Woodelf_Archer_Helm",[("mirkwood_helm_a",imodbits_armor_bad),("mirkwood_helm_b",imodbit_plain),("mirkwood_helm_b",0),("mirkwood_helm_c",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,600,weight(1)|abundance(92)|head_armor(25)|body_armor(0)|difficulty(0),imodbits_armor],
["mirkwood_helm_b","Greenwood_Helm",[("mirkwoodnormalspearman_a_light",imodbits_armor_bad),("mirkwoodnormalspearman_a",imodbit_plain),("mirkwoodnormalspearman_a",0),("mirkwoodnormalspearman_b",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,900,weight(1)|abundance(93)|head_armor(30)|body_armor(0)|difficulty(10),imodbits_armor],
["mirkwood_helm_c","Greenwood_Heavy_Helm",[("mirkwoodroyalspearman_a_light",imodbits_armor_bad),("mirkwoodroyalspearman_a",imodbit_plain),("mirkwoodroyalspearman_a",0),("mirkwoodroyalspearman_b",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1200,weight(2)|abundance(94)|head_armor(34)|body_armor(0)|difficulty(12),imodbits_armor],
["mirkwood_helm_d","Greenwood_Royal_Helm",[("mirkwoodroyalarcher_a",imodbit_plain),("mirkwoodroyalarcher_a",0),("mirkwoodroyalarcher_b",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1300,weight(3)|abundance(95)|head_armor(36)|body_armor(0)|difficulty(13),imodbits_elf_armor],
####BOOTS
["woodelf_leather_boots","Woodelf_Leather_Boots",[("TLDO_elf_boots",0),("TLDO_mirkwood_boots",imodbits_armor_good)],itp_type_foot_armor|itp_shop,0,550,weight(1)|abundance(90)|leg_armor(16)|difficulty(0),imodbits_armor],
["mirkwood_boots","Greenwood_Boots",[("mirkwood_boots",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,650,weight(1)|abundance(92)|leg_armor(17)|difficulty(0),imodbits_armor],

#####TLD HARAD ITEMS##########
###########ARMOR##########
["harad_tunic","Harad_Tunic",[("harad_skirmisher",imodbits_armor_bad), ("harad_tunic",imodbit_plain), ("harad_tunic",0), ("harad_archer",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,50,weight(4)|abundance(90)|head_armor(0)|body_armor(12)|leg_armor(3)|difficulty(0),imodbits_armor,],
["harad_padded","Harad_Padded_Jerkin",[("CWE_arabian_light_armor_a",imodbits_armor_bad), ("CWE_arabian_light_armor_b",imodbit_plain), ("CWE_arabian_light_armor_b",0), ("CWE_arabian_light_armor_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,350,weight(9)|abundance(90)|head_armor(0)|body_armor(14)|leg_armor(5)|difficulty(0),imodbits_armor,],
["harad_lamellar","Harad_Scale_Vest",[("CWE_heavy_armor_arabs_1a",imodbits_armor_bad), ("CWE_heavy_armor_arabs_1b",imodbit_plain), ("CWE_heavy_armor_arabs_1b",0), ("CWE_heavy_armor_arabs_1c",imodbits_armor_good|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,900,weight(22)|abundance(92)|head_armor(0)|body_armor(22)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly,],
["harad_heavy_lamellar","Harad_Heavy_Scale_Vest",[("CWE_heavy_armor_arabs_2a",imodbits_armor_bad), ("CWE_heavy_armor_arabs_2b",imodbit_plain), ("CWE_heavy_armor_arabs_2b",0), ("CWE_heavy_armor_arabs_2c",imodbits_armor_good), ("CWE_heavy_armor_arabs_2d",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1400,weight(26)|abundance(94)|head_armor(0)|body_armor(28)|leg_armor(10)|difficulty(11),imodbits_armor|imodbit_lordly,],
["harad_heavy","Harasjala_Armor",[("harad_heavy_0",imodbits_armor_bad), ("harad_heavy_1",imodbit_plain), ("harad_heavy_1",0), ("harad_heavy",imodbits_armor_good|imodbit_lordly),],itp_type_body_armor|itp_covers_legs|itp_shop,0,2200,weight(30)|abundance(96)|head_armor(1)|body_armor(35)|leg_armor(12)|difficulty(18),imodbits_armor|imodbit_lordly,],
["harad_pectoral","Harad_Breastplate",[("harad_tier_1_giles",imodbits_armor_bad), ("harad_tier_2_giles",imodbit_plain), ("harad_tier_2_giles",0), ("harad_tier_3_giles",imodbits_armor_good|imodbit_lordly|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,900,weight(4)|abundance(90)|head_armor(0)|body_armor(25)|leg_armor(5)|difficulty(9),imodbits_armor,],
["free_harad_archer","Harad_Archer_Armor",[("harad_archer",0)],itp_type_body_armor|itp_covers_legs,0,600,weight(8)|abundance(90)|head_armor(0)|body_armor(16)|leg_armor(6)|difficulty(0),imodbits_armor,],
["black_snake_armor","Maranka_Armor",[("black_snake_armor_light",imodbits_armor_bad),("black_snake_armor",0),("black_snake_armor",imodbit_plain)],itp_type_body_armor|itp_covers_legs,0,1300,weight(16)|abundance(100)|head_armor(2)|body_armor(25)|leg_armor(11)|difficulty(9),imodbits_armor|imodbit_lordly,],
["harad_champion","Far_Harad_Garb",[("harad_champion",0), ("panther_guard",imodbits_armor_good|imodbit_lordly)],itp_type_body_armor|itp_covers_legs,0,500,weight(4)|abundance(90)|head_armor(0)|body_armor(14)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly,],
["free_panther_guard","Panther_Hide",[("panther_guard",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,900,weight(5)|abundance(90)|head_armor(0)|body_armor(15)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly,],
["harad_scale","Harad_Scale_Armor",[("CWE_armor_archer_saracin_4a",imodbits_armor_bad), ("CWE_armor_archer_saracin_4b",imodbit_plain), ("CWE_armor_archer_saracin_4c",0), ("harad_scale_3",imodbits_armor_good|imodbit_lordly)],itp_type_body_armor|itp_covers_legs,0,1200,weight(28)|abundance(94)|head_armor(0)|body_armor(27)|leg_armor(9)|difficulty(11),imodbits_armor|imodbit_lordly,],
["free_harad_tiger_scale","Tiger_Guard_Armor",[("harad_tier_3_giles",0)],itp_type_body_armor|itp_covers_legs,0,1400,weight(30)|abundance(95)|head_armor(2)|body_armor(30)|leg_armor(8)|difficulty(15),imodbits_armor|imodbit_lordly,],
["harad_lion_scale","Lion_Guard_Armor",[("CWE_heavy_armor_arabs_2d",0)],itp_type_body_armor|itp_covers_legs,0,1400,weight(30)|abundance(95)|head_armor(2)|body_armor(30)|leg_armor(8)|difficulty(15),imodbits_armor|imodbit_lordly,],
###########HELMS##########
#HARONDOR
["harad_dragon_helm","Kiloka_Helm",[("harad_dragon_helm",0)],itp_type_head_armor|itp_shop,0,1500,weight(6)|abundance(96)|head_armor(39)|body_armor(0)|difficulty(20),imodbits_armor|imodbit_lordly],
["harad_cav_helm_a","Harondor_Light_Helm",[("harad_cav_helm_a",0)],itp_type_head_armor|itp_shop,0,600,weight(3)|abundance(91)|head_armor(24)|body_armor(0)|difficulty(11),imodbits_armor | imodbit_cracked],
["harad_cav_helm_b","Harondor_Light_Helm",[("harad_cav_helm_b",0)],itp_type_head_armor|itp_shop,0,600,weight(3)|abundance(91)|head_armor(24)|body_armor(0)|difficulty(11),imodbits_armor | imodbit_cracked],
["black_snake_helm","Maranka_Helm",[("black_snake_helm",0)],itp_type_head_armor|itp_shop,0,1200,weight(4)|abundance(95)|head_armor(34)|body_armor(0)|difficulty(17),imodbits_armor|imodbit_lordly],
#GREAT HARAD
["harad_finhelm","Harad_Heavy_Footman_Helmet",[("harad_finhelm",0)],itp_type_head_armor|itp_shop,0,1000,weight(5)|abundance(95)|head_armor(32)|body_armor(0)|difficulty(16),imodbits_armor|imodbit_lordly],
["harad_heavy_inf_helm","Harad_Footman_Helmet",[("harad_heavy_inf_helm",0)],itp_type_head_armor|itp_shop,0,800,weight(3)|abundance(92)|head_armor(28)|body_armor(0)|difficulty(13),imodbits_armor|imodbit_lordly | imodbit_cracked],
["harad_wavy_helm","Harad_Conical_Helmet",[("harad_wavy_helm",0)],itp_type_head_armor|itp_shop,0,900,weight(4)|abundance(93)|head_armor(30)|body_armor(0)|difficulty(16),imodbits_armor|imodbit_lordly | imodbit_cracked],
["harad_eaglehelm","Eagle_Guard_Helm",[("eagle_guard_helmet",0)],itp_type_head_armor|itp_shop,0,1200,weight(4)|abundance(95)|head_armor(34)|body_armor(0)|difficulty(17),imodbits_armor|imodbit_lordly],
["lion_helm","Lion_Guard_Helm",[("lion_helm",0)],itp_type_head_armor|itp_shop,0,1300,weight(6)|abundance(96)|head_armor(36)|body_armor(0)|difficulty(19),imodbits_elf_armor],
#FAR HARAD
["harad_pantherhelm","Panther_Guard_Cap",[("harad_pantherhelm",0)],itp_type_head_armor|itp_shop,0,600,weight(1)|abundance(92)|head_armor(25)|body_armor(0)|difficulty(12),imodbits_cloth],
##########WEAPONS##########
["harad_khopesh","Harad_Khopesh",[("harad_khopesh",0)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,340,weight(2.5)|abundance(92)|difficulty(0)|spd_rtng(90)|weapon_length(80)|swing_damage(30,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
["black_snake_sword","Harad_Cobra_Sword",[("harad_sword_cobra_low",0),("harad_sword_cobra",imodbits_weapon_good),("scab_cobra_low",ixmesh_carry),("scab_cobra",ixmesh_carry|imodbits_weapon_good)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,360,weight(2.5)|abundance(91)|difficulty(0)|spd_rtng(97)|weapon_length(80)|swing_damage(30,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
["harad_heavy_sword","Harad_Dragon_Sword",[("harad_sword_dragon_low",0),("harad_sword_dragon",imodbits_weapon_good),("scab_dragon_low",ixmesh_carry),("scab_dragon",ixmesh_carry|imodbits_weapon_good)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,400,weight(2.5)|abundance(95)|difficulty(0)|spd_rtng(92)|weapon_length(95)|swing_damage(32,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
["horandor_a","Harad_Scimitar",[("horandor_a",0)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,320,weight(2.5)|abundance(91)|difficulty(0)|spd_rtng(96)|weapon_length(90)|swing_damage(22,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
["skirmisher_sword","Harad_Skirmisher_Sword",[("skirmisher_sword",0)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,300,weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(96)|weapon_length(60)|swing_damage(30,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
["harad_sabre","Harad_Salamander_Sword",[("harad_sword_salamander_low",0),("harad_sword_salamander",imodbits_weapon_good),("scab_salamander_low",ixmesh_carry),("scab_salamander",ixmesh_carry|imodbits_weapon_good)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,320,weight(2.5)|abundance(91)|difficulty(0)|spd_rtng(102)|weapon_length(68)|swing_damage(27,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
["harad_mace","Far_Harad_Mace",[("harad_mace",0)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,350,weight(2.5)|abundance(93)|difficulty(12)|spd_rtng(96)|weapon_length(50)|swing_damage(30,blunt)|thrust_damage(0,blunt),imodbits_weapon_good],
["far_harad_2h_mace","Far_Harad_Two_Handed_Mace",[("far_harad_2h_mace",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_shop|itp_crush_through|itp_can_knock_down,itc_nodachi|itcf_carry_back,500,weight(4.5)|abundance(92)|difficulty(14)|spd_rtng(100)|weapon_length(74)|swing_damage(28,blunt)|thrust_damage(0,pierce),imodbits_weapon_wood],
["harad_dagger","Harad_Knife",[("harad_dagger",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_primary|itp_secondary|itp_no_parry,itc_dagger|itcf_carry_dagger_front_left,100,weight(0.75)|abundance(90)|difficulty(0)|spd_rtng(120)|weapon_length(47)|swing_damage(22,cut)|thrust_damage(19,pierce),imodbits_weapon_bad],
["harad_short_spear","Harad_Short_Spear",[("harad_short_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_wooden_parry,itc_spear_upstab,200,weight(2)|abundance(90)|difficulty(0)|spd_rtng(100)|weapon_length(132)|thrust_damage(20,pierce)|swing_damage(10,blunt),imodbits_weapon_wood],
["harad_long_spear","Harad_Spear",[("harad_long_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable,itc_lance_upstab,300,weight(3)|abundance(92)|difficulty(0)|spd_rtng(81)|weapon_length(190)|thrust_damage(26,pierce)|swing_damage(0,blunt),imodbits_weapon_wood],
["eagle_guard_spear","Harasjala_Polearm",[("eagle_guard_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_cant_use_on_horseback|itp_spear|itp_penalty_with_shield|itp_wooden_parry,itc_cutting_spear,780,weight(3)|abundance(94)|difficulty(13)|spd_rtng(86)|weapon_length(149)|swing_damage(36,cut)|thrust_damage(26,pierce),imodbits_weapon_good],
###########SHIELDS##########
["harad_long_shield_a","Harad_Leopard_Shield",[("harad_long_shield_a",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,500,weight(3)|abundance(93)|difficulty(2)|hit_points(300)|body_armor(17)|spd_rtng(82)|weapon_length(65),imodbits_shield,],
["harad_long_shield_b","Harad_Bronze_Shield",[("harad_long_shield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,800,weight(4)|abundance(94)|difficulty(3)|hit_points(310)|body_armor(18)|spd_rtng(80)|weapon_length(65),imodbits_shield,],
["harad_long_shield_c","Harad_Sun_Shield",[("harad_long_shield_c",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(2.5)|abundance(92)|difficulty(2)|hit_points(300)|body_armor(11)|spd_rtng(82)|weapon_length(60),imodbits_shield,],
["harad_long_shield_d","Harad_Snake_Shield",[("harad_long_shield_d",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,400,weight(2.5)|abundance(91)|difficulty(1)|hit_points(280)|body_armor(11)|spd_rtng(82)|weapon_length(60),imodbits_shield,],
["harad_long_shield_e","Harad_Snake_Shield",[("harad_long_shield_e",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,400,weight(2.5)|abundance(91)|difficulty(1)|hit_points(280)|body_armor(11)|spd_rtng(82)|weapon_length(60),imodbits_shield,],
["harad_shield_a","Harondor_Shield",[("harad_shield_a",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,300,weight(2)|abundance(90)|difficulty(0)|hit_points(240)|body_armor(14)|spd_rtng(90)|weapon_length(40),imodbits_shield,],
["harad_shield_b","Harondor_Buckler",[("harad_shield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,100,weight(2)|abundance(90)|difficulty(0)|hit_points(210)|body_armor(14)|spd_rtng(97)|weapon_length(40),imodbits_shield,],
["harad_shield_c","Harondor_Buckler",[("harad_shield_c",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,100,weight(2)|abundance(90)|difficulty(0)|hit_points(210)|body_armor(14)|spd_rtng(97)|weapon_length(40),imodbits_shield,],
#unused ->
["free_harad_tribal_a","Far_Harad_Shield",[("far_harad_c_giles",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_board_shield,200,weight(2.5)|hit_points(480)|body_armor(0)|spd_rtng(82)|weapon_length(80),imodbits_shield,],
["free_harad_tribal_b","Far_Harad_Shield",[("far_harad_c_giles",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_board_shield,200,weight(2.5)|hit_points(480)|body_armor(0)|spd_rtng(82)|weapon_length(80),imodbits_shield,],
["harad_yellow_shield","Harad_Shield",[("harad_yellow_shield",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,600,weight(2.5)|abundance(94)|difficulty(2)|hit_points(300)|body_armor(18)|spd_rtng(90)|weapon_length(50),imodbits_shield,],
############BOOTS##########
["desert_boots","Desert_Boots",[("desert_boots",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,200,weight(1)|abundance(90)|leg_armor(11)|difficulty(0),imodbits_cloth],
["harad_leather_greaves","Harad_Leather_Greaves",[("harad_leather_greaves",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,550,weight(4)|abundance(92)|leg_armor(16)|difficulty(0),imodbits_cloth],
["harad_scale_greaves","Harad_Greaves",[("harad_greaves_giles",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,1100,weight(6)|abundance(93)|leg_armor(22)|difficulty(11),imodbits_armor|imodbit_lordly],
["harad_lamellar_greaves","Harad_Splinted_Greaves",[("harad_lamellar_greaves",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,1300,weight(7)|abundance(94)|leg_armor(24)|difficulty(12),imodbits_armor|imodbit_lordly],
### CAMEL ###
["camel","Harad_Camel",[("giles_evil_camel_brown",0),("giles_evil_camel",imodbits_horse_good)],itp_type_horse|itp_unique,0,2000,hit_points(180)|body_armor(22)|difficulty(2)|horse_speed(28)|horse_maneuver(48)|horse_charge(18)|horse_scale(110)|abundance(100),imodbits_horse_basic|0],

#####TLD KHAND ITEMS##########
###HELMS########### #free Dec 2019
#["free_khand_helmet_a1","Khand_Helm_With_Camail",[("khand_inf_helm_a2",0)],itp_type_head_armor|itp_shop,0,1000,weight(3)|head_armor(35)|difficulty(0),imodbits_armor|imodbit_lordly | imodbit_cracked],
["free_khand_helmet_a2","Khand_Helm",[("khand_inf_helm_a3",0)],itp_type_head_armor|itp_shop,0,800,weight(2)|head_armor(30)|difficulty(0),imodbits_armor|imodbit_lordly | imodbit_cracked],
["free_khand_helmet_a3","Khand_Veiled_Helm",[("khand_inf_helm_a1",0)],itp_type_head_armor|itp_shop,0,600,weight(2)|head_armor(28)|difficulty(0),imodbits_armor|imodbit_lordly | imodbit_cracked],
["free_khand_helmet_b1","Khand_Decorated_Helm",[("khand_cav_helm_c",0)],itp_type_head_armor|itp_shop,0,900,weight(3)|head_armor(33)|difficulty(0),imodbits_armor|imodbit_lordly | imodbit_cracked],
["free_khand_helmet_b2","Khand_Masked_Helm",[("khand_cav_helm_a3",0)],itp_type_head_armor|itp_shop,0,1200,weight(3.5)|head_armor(38)|difficulty(0),imodbits_armor|imodbit_lordly],
["free_khand_helmet_b3","Khand_Veiled_Helm",[("khand_cav_helm_a1",0)],itp_type_head_armor|itp_shop,0,600,weight(2)|head_armor(28)|difficulty(0),imodbits_armor|imodbit_lordly | imodbit_cracked],
["free_khand_helmet_b4","Khand_Helm_With_Camail",[("khand_cav_helm_a2",0)],itp_type_head_armor|itp_shop,0,1000,weight(3)|head_armor(35)|difficulty(0),imodbits_armor|imodbit_lordly | imodbit_cracked],
["free_khand_helmet_c3","Khand_Infantry_Helm",[("khand_inf_helm_c2b",0)],itp_type_head_armor|itp_shop,0,800,weight(3)|head_armor(30)|difficulty(0),imodbits_armor|imodbit_lordly | imodbit_cracked],
["free_khand_helmet_c4","Khand_Infantry_Helm",[("khand_inf_helm_c1b",0)],itp_type_head_armor|itp_shop,0,800,weight(3)|head_armor(30)|difficulty(0),imodbits_armor|imodbit_lordly | imodbit_cracked],
["free_khand_helmet_d1","Khand_Masked_Helm",[("khand_inf_helm_d4",0)],itp_type_head_armor|itp_shop,0,1200,weight(3.5)|head_armor(38)|difficulty(0),imodbits_armor|imodbit_lordly],
["khand_inf_helm_a","Khand_Helm",[("khand_inf_helm_a1",imodbits_armor_bad),("khand_inf_helm_a2",imodbit_plain),("khand_inf_helm_a2",0),("khand_inf_helm_a3",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,800,weight(3)|abundance(92)|head_armor(28)|body_armor(0)|difficulty(13),imodbits_armor| imodbit_cracked],
["khand_inf_helm_b","Khand_Helm",[("khand_inf_helm_b1",imodbits_armor_bad),("khand_inf_helm_b2",imodbit_plain),("khand_inf_helm_b2",0),("khand_inf_helm_b3",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,850,weight(3)|abundance(93)|head_armor(29)|body_armor(0)|difficulty(14),imodbits_armor| imodbit_cracked],
["khand_inf_helm_c1","Khand_Bowl_Helm",[("khand_inf_helm_c1a",imodbits_armor_bad),("khand_inf_helm_c1b",imodbit_plain),("khand_inf_helm_c1b",0),("khand_inf_helm_c1c",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1000,weight(4)|abundance(94)|head_armor(31)|body_armor(0)|difficulty(16),imodbits_armor| imodbit_cracked],
["khand_inf_helm_c2","Khand_Bowl_Helm",[("khand_inf_helm_c2a",imodbits_armor_bad),("khand_inf_helm_c2b",imodbit_plain),("khand_inf_helm_c2b",0),("khand_inf_helm_c2c",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1000,weight(4)|abundance(94)|head_armor(31)|body_armor(0)|difficulty(16),imodbits_armor| imodbit_cracked],
["khand_inf_helm_d","Khand_Cone_Helm",[("khand_inf_helm_d1",imodbits_armor_bad),("khand_inf_helm_d2",imodbit_plain),("khand_inf_helm_d2",0),("khand_inf_helm_d4",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1200,weight(5)|abundance(95)|head_armor(34)|body_armor(0)|difficulty(17),imodbits_armor| imodbit_cracked],
["khand_cav_helm_a","Khand_Rider_Helm",[("khand_cav_helm_a1",imodbits_armor_bad),("khand_cav_helm_a2",imodbit_plain),("khand_cav_helm_a2",0),("khand_cav_helm_a3",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1100,weight(5)|abundance(94)|head_armor(33)|body_armor(0)|difficulty(16),imodbits_armor| imodbit_cracked|imodbit_lordly],
["khand_cav_helm_b","Khand_Rider_Helm",[("khand_cav_helm_b",imodbit_plain),("khand_cav_helm_b",0),("khand_cav_helm_b2",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1100,weight(5)|abundance(94)|head_armor(33)|body_armor(0)|difficulty(16),imodbits_armor],
["khand_cav_helm_c","Khand_Decorated_Helm",[("khand_cav_helm_c",imodbit_plain),("khand_cav_helm_c",0),("khand_cav_helm_c3",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1600,weight(9)|abundance(97)|head_armor(40)|body_armor(0)|difficulty(20),imodbits_elf_armor],
["khand_helm_mask","Khand_Mask",[("Khand_Helmet_Mask2",imodbit_plain),("Khand_Helmet_Mask2",0),("Khand_Helmet_Mask1",imodbits_armor_good)],itp_type_head_armor|itp_shop|itp_doesnt_cover_hair,0,100,weight(0.5)|abundance(91)|head_armor(20)|body_armor(0)|difficulty(0),imodbits_armor| imodbit_cracked],
#########ARMOR########## #free Dec 2019
["khand_light","Khand_Kilt",[("khand_light_a",imodbits_armor_bad),("khand_light_b",imodbit_plain),("khand_light_b",0),("khand_light_c",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,40,weight(2)|abundance(90)|head_armor(0)|body_armor(10)|leg_armor(8)|difficulty(0),imodbits_armor| imodbit_cracked, [custom_female("itm_khand_light")]],
["khand_light_lam","Khand_Light_Footmen_Armor",[("CWE_turk_med_a1",imodbits_armor_bad),("CWE_turk_med_a2",imodbit_plain),("CWE_turk_med_a2",0),("CWE_turk_med_a3",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,700,weight(18)|abundance(92)|head_armor(0)|body_armor(22)|leg_armor(8)|difficulty(9),imodbits_armor| imodbit_cracked],
["khand_foot_lam","Khand_Heavy_Footman_Armor",[("CWE_turk_med_a1",imodbits_armor_bad),("CWE_turk_med_a2",imodbit_plain),("CWE_turk_med_a2",0),("CWE_turk_med_a3",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1300,weight(25)|abundance(93)|head_armor(0)|body_armor(28)|leg_armor(8)|difficulty(14),imodbits_armor| imodbit_cracked],
["khand_med_lam","Khand_Medium_Lamellar",[("CWE_turk_heavy_b1",imodbits_armor_bad),("CWE_turk_heavy_b2",imodbit_plain),("CWE_turk_heavy_b2",0),("CWE_turk_heavy_b3",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1450,weight(30)|abundance(94)|head_armor(0)|body_armor(25)|leg_armor(13)|difficulty(14),imodbits_armor| imodbit_cracked],
["khand_heavy_lam","Khand_Heavy_Lamellar",[("CWE_turk_heavy_c1",imodbits_armor_bad),("CWE_turk_heavy_c2",imodbit_plain),("CWE_turk_heavy_c2",0),("CWE_turk_heavy_c3",imodbits_armor_good|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2300,weight(34)|abundance(95)|head_armor(0)|body_armor(32)|leg_armor(16)|difficulty(18),imodbits_armor| imodbit_cracked|imodbit_lordly],
["khand_mail","Khand_Mail",[("CWE_turk_heavy_a1",imodbits_armor_bad),("CWE_turk_heavy_a2",imodbit_plain),("CWE_turk_heavy_a2",0),("CWE_turk_heavy_a3",imodbits_armor_good|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2100,weight(28)|abundance(94)|head_armor(0)|body_armor(30)|leg_armor(16)|difficulty(14),imodbits_armor| imodbit_cracked|imodbit_lordly],
["khand_noble_lam","Khand_Noble_Armor",[("CWE_ghulam_heavy1",imodbits_armor_bad),("CWE_ghulam_heavy2",imodbit_plain),("CWE_ghulam_heavy2",0),("CWE_ghulam_heavy3",imodbits_armor_good|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2900,weight(40)|abundance(96)|head_armor(0)|body_armor(38)|leg_armor(16)|difficulty(20),imodbits_armor| imodbit_cracked|imodbit_lordly],
["free_khand_med_lam_c","Khand_Medium_Lamellar",[("khand_med_lam_c",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1300,weight(23)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0),imodbits_armor],
["free_khand_med_lam_d","Khand_Medium_Lamellar",[("khand_med_lam_d",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1400,weight(23)|head_armor(0)|body_armor(28)|leg_armor(10)|difficulty(0),imodbits_armor],
["free_khand_noble_lam","Khand_Noble_Armor",[("khand_noble_lam",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,3000,weight(26)|head_armor(2)|body_armor(32)|leg_armor(13)|difficulty(0),imodbits_armor|imodbit_lordly],
["free_variag_greaves","Variag_Greaves",[("variag_boots",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,1000,weight(3)|leg_armor(24)|difficulty(0),imodbits_armor|imodbit_lordly],
#########WEAPONS##########
["khand_axe_great","Khand_Great_Axe",[("Khand_Weapon_Axe_Great",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,500,weight(4.5)|abundance(94)|difficulty(16)|spd_rtng(87)|weapon_length(109)|swing_damage(41,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["khand_axe_winged","Khand_Winged_Axe",[("Khand_Weapon_Axe_Winged",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,430,weight(3)|abundance(94)|difficulty(15)|spd_rtng(93)|weapon_length(96)|swing_damage(35,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["khand_halberd","Khand_Halberd",[("Khand_Weapon_Halberd",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_two_handed|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_cutting_spear|itcf_carry_axe_back,800,weight(6)|abundance(94)|difficulty(18)|spd_rtng(88)|weapon_length(164)|swing_damage(38,cut)|thrust_damage(21,pierce),imodbits_weapon_bad],
["khand_trident","Khand_Trident",[("Khand_Weapon_Trident",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_two_handed|itp_wooden_parry|itp_cant_use_on_horseback,itc_pike_upstab|itcf_carry_axe_back,400,weight(2.5)|abundance(93)|difficulty(13)|spd_rtng(88)|weapon_length(164)|thrust_damage(35,pierce),imodbits_weapon_bad],
["khand_voulge","Khand_Voulge",[("Khand_Weapon_Voulge",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_two_handed|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_cutting_spear|itcf_carry_axe_back,550,weight(5)|abundance(91)|difficulty(17)|spd_rtng(88)|weapon_length(126)|swing_damage(38,cut)|thrust_damage(21,pierce),imodbits_weapon_bad],
["khand_mace1","Khand_Mace",[("Khand_Weapon_Mace1",0)],itp_type_two_handed_wpn|itp_primary|itp_shop|itp_penalty_with_shield|itp_wooden_parry|itp_unbalanced,itc_bastardfalchion|itcf_carry_mace_left_hip,300,weight(3.5)|abundance(91)|difficulty(11)|spd_rtng(95)|weapon_length(94)|swing_damage(21,blunt)|thrust_damage(0,pierce),imodbits_weapon_bad],
["khand_mace2","Khand_Mace",[("Khand_Weapon_Mace2",0)],itp_type_two_handed_wpn|itp_primary|itp_shop|itp_penalty_with_shield|itp_wooden_parry|itp_unbalanced,itc_bastardfalchion|itcf_carry_mace_left_hip,350,weight(3.5)|abundance(92)|difficulty(13)|spd_rtng(91)|weapon_length(94)|swing_damage(24,blunt)|thrust_damage(0,pierce),imodbits_weapon_bad],
["khand_throwing_axe","Khand_Throwing_Axe",[("Khand_Weapon_Throwing_Axe",0),("Khand_Weapon_Throwing_Axe_quiver", ixmesh_carry),("Khand_Weapon_Throwing_Axe_inventory", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield|itp_can_penetrate_shield,itcf_throw_axe|itcf_carry_quiver_front_right|itcf_show_holster_when_drawn,300,weight(5)|difficulty(2)|shoot_speed(20)|spd_rtng(103)|weapon_length(53)|thrust_damage(60,cut)|accuracy(83)|max_ammo(3),imodbits_thrown,[] ],
["khand_rammace","Khand_Ram_Mace",[("Khand_Weapon_Mace_Ram",0)],itp_type_polearm|itp_no_blur|itp_unique|itp_primary|itp_wooden_parry|itp_wooden_attack|itp_crush_through|itp_can_knock_down,itc_bastardfalchion|itcf_carry_back,400,weight(6)|abundance(95)|difficulty(14)|spd_rtng(84)|weapon_length(102)|swing_damage(33,blunt)|thrust_damage(0,pierce),imodbits_weapon_wood],
["khand_pitsword","Pit_Fighter_Sword",[("Khand_Weapon_Sword_Pit",0)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip,250,weight(1.25)|abundance(90)|difficulty(0)|spd_rtng(107)|weapon_length(66)|swing_damage(27,cut)|thrust_damage(25,pierce),imodbits_weapon_bad],
["khand_tulwar","Khand_Tulwar",[("Khand_Weapon_Tulwar",0)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,400,weight(1.25)|abundance(91)|difficulty(0)|spd_rtng(98)|weapon_length(94)|swing_damage(30,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["khand_2h_tulwar","Khand_Great_Tulwar",[("Khand_Weapon_Tulwar_Long",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_shop,itc_nodachi|itcf_carry_sword_back,540,weight(2.75)|abundance(93)|difficulty(11)|spd_rtng(92)|weapon_length(116)|swing_damage(40,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["khand_lance","Khand_Lance",[("khand_lance",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable,itc_spear,450,weight(2.5)|abundance(91)|difficulty(10)|spd_rtng(88)|weapon_length(218)|thrust_damage(26,pierce),imodbits_weapon_bad],
####KHAND & RHUN SHIELDS
["easterling_round_horseman","Easterling_Round_Shield",[("eastershield_c",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(1)|abundance(90)|difficulty(0)|hit_points(260)|body_armor(13)|spd_rtng(96)|weapon_length(35),imodbits_shield,],
["variag_gladiator_shield","Easterling_Pit_Shield",[("eastershield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(1)|abundance(90)|difficulty(0)|hit_points(230)|body_armor(11)|spd_rtng(98)|weapon_length(35),imodbits_shield,],
["easterling_hawk_shield","Easterling_Hawk_Shield",[("eastershield_a",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,500,weight(3)|abundance(92)|difficulty(2)|hit_points(310)|body_armor(13)|spd_rtng(82)|weapon_length(60),imodbits_shield,],
["rhun_bull1_shield","Rhun_Shield",[("eastershield_d",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(2.5)|abundance(90)|difficulty(0)|hit_points(230)|body_armor(14)|spd_rtng(90)|weapon_length(40),imodbits_shield,],
["rhun_bull2_shield","Rhun_Shield",[("eastershield_e",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(2.5)|abundance(90)|difficulty(0)|hit_points(230)|body_armor(14)|spd_rtng(90)|weapon_length(40),imodbits_shield,],
["rhun_bull3_shield","Rhun_Shield",[("eastershield_f",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,500,weight(2.5)|abundance(90)|difficulty(0)|hit_points(320)|body_armor(15)|spd_rtng(86)|weapon_length(40),imodbits_shield,],
["rhun_shield","Rhun_Kite_Shield",[("rhun_shield",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(2.5)|abundance(92)|difficulty(2)|hit_points(290)|body_armor(15)|spd_rtng(82)|weapon_length(50),imodbits_shield,],

###TLD RHUN ITEMS##########
###ARMOR##########
["rhun_armor_a","Rhun_Light_Battlewear",[("RhunArmorLight1",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,20,weight(5)|head_armor(0)|body_armor(2)|leg_armor(6)|difficulty(0),imodbits_cloth,[]],
["rhun_armor_b","Rhun_Light_Battlewear",[("RhunArmorLight2",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,30,weight(5)|head_armor(0)|body_armor(3)|leg_armor(6)|difficulty(0),imodbits_cloth,[]],
["rhun_armor_d","Rhun_Light_Battlewear",[("RhunArmorLight4",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,30,weight(6)|head_armor(0)|body_armor(4)|leg_armor(6)|difficulty(0),imodbits_cloth,[]],
["rhun_armor_g","Rhun_Heavy_Battlewear",[("RhunArmorHeavy2",0),("RhunArmorHeavy2b",imodbits_armor_good|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1700,weight(19)|abundance(93)|head_armor(0)|body_armor(25)|leg_armor(16)|difficulty(13),imodbits_armor|imodbit_lordly,],
["rhun_armor_h","Rhun_Heavy_Battlewear",[("RhunArmorHeavy3",0),("RhunArmorHeavy3b",imodbits_armor_good|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1600,weight(18)|abundance(93)|head_armor(0)|body_armor(24)|leg_armor(16)|difficulty(13),imodbits_armor|imodbit_lordly,],
["rhun_armor_j","Rhun_Medium_Battlewear",[("RhunArmorMedium1",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,800,weight(7)|head_armor(0)|body_armor(10)|leg_armor(12)|difficulty(0),imodbits_cloth,],
["rhun_armor_m","Rhun_Medium_Battlewear",[("RhunArmorMedium3",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,560,weight(8)|head_armor(0)|body_armor(11)|leg_armor(12)|difficulty(0),imodbits_cloth,],
["rhun_armor_n","Rhun_Medium_Battlewear",[("RhunArmorMedium4",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,750,weight(9)|head_armor(0)|body_armor(12)|leg_armor(14)|difficulty(0),imodbits_cloth,],
["rhun_armor_o","Rhun_Medium_Battlewear",[("RhunArmorMedium5",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1000,weight(10)|head_armor(0)|body_armor(14)|leg_armor(14)|difficulty(0),imodbits_cloth,],
["rhun_armor_p","Rhun_Noble_Armor",[("RhunArmorNoble1A_medium",0),("RhunArmorNoble1A_light",imodbits_armor_bad), ("RhunArmorNoble1A",imodbits_armor_good|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2600,weight(26)|abundance(97)|head_armor(0)|body_armor(34)|leg_armor(17)|difficulty(19),imodbits_armor|imodbit_lordly,],
["rhun_armor_k","Rhun_Noble_Armor",[("RhunArmorNoble1B_medium",0),("RhunArmorNoble1B_light",imodbits_armor_bad), ("RhunArmorNoble1B",imodbits_armor_good|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2600,weight(26)|abundance(97)|head_armor(0)|body_armor(34)|leg_armor(17)|difficulty(19),imodbits_armor|imodbit_lordly,],
#########Helms########## #free Oct 2021
["free_rhun_helm_barbed","Rhun_Barbed_Helm",[("RhunHelmConical0",imodbits_armor_bad),("RhunHelmConical1",0),("RhunHelmConical2",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,600,weight(2)|abundance(91)|head_armor(25)|body_armor(0)|difficulty(12),imodbits_armor | imodbit_cracked],
["free_rhun_helm_b","Rhun_Barbed_Helm_Camail",[("RhunHelmConical2",0)],itp_type_head_armor|itp_shop,0,700,weight(3)|head_armor(30)|difficulty(0),imodbits_armor|imodbit_lordly | imodbit_cracked],
["free_rhun_helm_horde","Rhun_Horde_Helm",[("RhunHelmHorde1_new",imodbits_armor_bad),("RhunHelmHorde2",0),("RhunHelmHorde3",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,800,weight(4)|abundance(92)|head_armor(28)|body_armor(0)|difficulty(13),imodbits_armor | imodbit_cracked],
["rhun_helm_chieftain","Rhun_Chieftain_Helm",[("RhunHelmDeathDealer1",imodbit_plain),("RhunHelmDeathDealer1",0),("RhunHelmDeathDealer2",imodbits_elf_armor)],itp_type_head_armor|itp_shop,0,1600,weight(8)|abundance(97)|head_armor(40)|body_armor(0)|difficulty(20),imodbits_elf_armor],
["rhun_helm_pot","Rhun_Pot_Helm",[("RhunHelmPot1",imodbits_armor_bad),("RhunHelmPot2",imodbit_plain),("RhunHelmPot2",0),("RhunHelmPot3",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1200,weight(6)|abundance(95)|head_armor(34)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly | imodbit_cracked],
["rhun_helm_barbed","Rhun_Barbed_Helm",[("RhunHelmConical0",imodbits_armor_bad),("RhunHelmConical1",imodbit_plain),("RhunHelmConical1",0),("RhunHelmConical2",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,600,weight(2)|abundance(91)|head_armor(25)|body_armor(0)|difficulty(12),imodbits_armor | imodbit_cracked],
["rhun_helm_round","Rhun_Round_Helm",[("RhunHelmRound0",imodbits_armor_bad),("RhunHelmRound1",imodbit_plain),("RhunHelmRound1",0),("RhunHelmRound2",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,800,weight(3)|abundance(92)|head_armor(28)|body_armor(0)|difficulty(13),imodbits_armor | imodbit_cracked],
["rhun_helm_horde","Rhun_Horde_Helm",[("RhunHelmHorde1_new",imodbits_armor_bad),("RhunHelmHorde2",imodbit_plain),("RhunHelmHorde2",0),("RhunHelmHorde3",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,800,weight(4)|abundance(92)|head_armor(28)|body_armor(0)|difficulty(13),imodbits_armor | imodbit_cracked],
["rhun_helm_leather","Rhun_Leather_Helm",[("RhunHelmLeather1",imodbits_armor_bad),("RhunHelmLeather2",imodbit_plain),("RhunHelmLeather2",0),("RhunHelmLeather3",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,600,weight(1.5)|abundance(91)|head_armor(25)|body_armor(0)|difficulty(12),imodbits_cloth],
["free_rhun_helm_l","Rhun_Chieftain_Helm",[("RhunHelmDeathDealer1",0),("RhunHelmDeathDealer2",imodbits_armor|imodbit_lordly)],itp_type_head_armor|itp_shop,0,1600,weight(8)|abundance(97)|head_armor(40)|body_armor(0)|difficulty(20),imodbits_armor|imodbit_lordly],
["free_rhun_helm_m","Rhun_Leather_Helm",[("RhunHelmLeather3",0)],itp_type_head_armor|itp_shop,0,500,weight(1.5)|head_armor(25)|difficulty(0),imodbits_cloth],
["free_rhun_helm_chieftain","Rhun_Chieftain_Helm",[("RhunHelmDeathDealer1",0),("RhunHelmDeathDealer2",imodbits_armor|imodbit_lordly)],itp_type_head_armor|itp_shop,0,1600,weight(8)|abundance(97)|head_armor(40)|body_armor(0)|difficulty(20),imodbits_armor|imodbit_lordly],
########WEAPONS##########
["rhun_warpick","Rhun_War_Pick",[("rhun_pick",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_two_handed|itp_cant_use_on_horseback|itp_bonus_against_shield|itp_wooden_parry|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,450,weight(5)|abundance(93)|difficulty(15)|spd_rtng(86)|weapon_length(108)|swing_damage(29,pierce)|thrust_damage(0,pierce),imodbits_weapon_bad],
["rhun_greataxe","Rhun_Great_Axe",[("rhun_greataxe",0)],itp_type_two_handed_wpn|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,560,weight(6)|abundance(95)|difficulty(18)|spd_rtng(84)|weapon_length(115)|swing_damage(45,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["rhun_battleaxe","Rhun_Battle_Axe",[("rhun_battle_axe",0)],itp_type_two_handed_wpn|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,510,weight(5)|abundance(94)|difficulty(16)|spd_rtng(86)|weapon_length(108)|swing_damage(42,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["rhun_falchion","Savage_Falchion",[("rhun_falchion",0)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,300,weight(2.5)|abundance(91)|difficulty(0)|spd_rtng(96)|weapon_length(77)|swing_damage(30,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["rhun_glaive","Rhun_Glaive",[("rhun_glaive",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_two_handed|itp_cant_use_on_horseback|itp_wooden_parry|itp_crush_through|itp_unbalanced,itc_cutting_spear|itcf_carry_axe_back,650,weight(4)|abundance(93)|difficulty(15)|spd_rtng(84)|weapon_length(156)|swing_damage(36,cut)|thrust_damage(19,pierce),imodbits_weapon_bad],
["rhun_greatfalchion","Savage_Great_Falchion",[("rhun_greatfalchion",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_shop,itc_greatsword|itcf_carry_sword_back,730,weight(3)|abundance(92)|difficulty(12)|spd_rtng(92)|weapon_length(102)|swing_damage(42,cut)|thrust_damage(31,pierce),imodbits_weapon_bad],
["rhun_greatsword","Savage_Great_Sword",[("rhun_greatsword",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_shop,itc_greatsword|itcf_carry_sword_back,710,weight(3)|abundance(93)|difficulty(12)|spd_rtng(94)|weapon_length(101)|swing_damage(40,cut)|thrust_damage(31,pierce),imodbits_weapon_bad],
["rhun_shortsword","Savage_Shortsword",[("rhun_shortsword",0)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,150,weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(98)|weapon_length(70)|swing_damage(28,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["rhun_sword","Savage_Sword",[("rhun_sword",0)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,400,weight(2.9)|abundance(90)|difficulty(0)|spd_rtng(92)|weapon_length(89)|swing_damage(32,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["rhun_mangler","Rhun_Mangler",[("mackie_mangler_short",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_shop,itc_nodachi|itcf_carry_axe_back,550,weight(3)|abundance(93)|difficulty(13)|spd_rtng(92)|weapon_length(90)|swing_damage(28,pierce)|thrust_damage(0,pierce),imodbits_weapon_bad],
#TLD DALE ITEMS##########
########ARMORS##########
["dale_light_a","Dale_Militia_Jacket",[("dale_light_b1",imodbits_armor_bad),("dale_light_b2",imodbit_plain),("dale_light_b3",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,150,weight(7)|head_armor(0)|body_armor(13)|leg_armor(2)|difficulty(0),imodbits_armor,],
["dale_light_b","Northmen_Light_Lamellar",[("northmen_light_a2",imodbits_armor_bad),("northmen_light_a3",imodbit_plain),("northmen_light_a3_cloak",imodbit_cloak),("northmen_light_a1",imodbits_armor_good),("northmen_light_a1_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,400,weight(12)|head_armor(0)|body_armor(18)|leg_armor(6)|difficulty(0),imodbits_armor|imodbit_lordly|imodbit_cloak],
["dale_med_a","Northmen_Heavy_Lamellar",[("northmen_med_a3",imodbit_plain),("northmen_med_a3_cloak",imodbit_cloak),("northmen_med_a2",imodbits_armor_bad),("northmen_med_a1",imodbits_armor_good),("northmen_med_a1_pelt",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1100,weight(19)|abundance(93)|head_armor(0)|body_armor(26)|leg_armor(7)|difficulty(11),imodbits_armor|imodbit_lordly,],
["dale_med_b","Dale_Leather_Armor",[("dale_med_b",imodbits_armor_bad),("dale_med_b2",imodbit_plain),("dale_med_b3",imodbits_armor_good),("dale_med_b4",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,900,weight(20)|head_armor(0)|body_armor(18)|leg_armor(6)|difficulty(10),imodbits_armor|imodbit_lordly,],
["dale_med_c","Dale_Leather_Over_Mail",[("dale_med_c1",imodbits_armor_bad),("dale_med_c2",imodbit_plain),("dale_med_c3",imodbits_armor_good),("dale_med_c1_cloaked",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1000,weight(27)|abundance(93)|head_armor(0)|body_armor(26)|leg_armor(6)|difficulty(12),imodbits_armor|imodbit_lordly,],
["dale_med_d","Dale_Lamellar_Armor",[("dale_med_a1",imodbits_armor_bad),("dale_med_a2",imodbit_plain),("dale_med_a3",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,800,weight(25)|abundance(91)|head_armor(0)|body_armor(24)|leg_armor(4)|difficulty(10),imodbits_armor|imodbit_lordly,],
["dale_heavy_a","Dale_Lamellar_Over_Mail",[("dale_heavy_a1",imodbits_armor_bad),("dale_heavy_a2",imodbit_plain),("dale_heavy_a3",imodbits_armor_good),("dale_heavy_a3_pelt",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1600,weight(32)|abundance(94)|head_armor(0)|body_armor(32)|leg_armor(8)|difficulty(12),imodbits_armor|imodbit_lordly,],
["dale_heavy_b","Dale_Plated_Coat",[("dale_heavy_b",imodbits_armor_bad),("dale_heavy_b2",imodbit_plain),("dale_heavy_b3",imodbit_thick),("dale_heavy_b_cloaked",imodbit_reinforced),("dale_heavy_b_pelt",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2400,weight(38)|abundance(95)|head_armor(0)|body_armor(38)|leg_armor(11)|difficulty(17),imodbits_armor|imodbit_lordly,],
["dale_heavy_c","Rhovanion_Mail",[("northmen_heavy_a",imodbit_plain),("northmen_heavy_b",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1800,weight(28)|abundance(93)|head_armor(0)|body_armor(31)|leg_armor(12)|difficulty(12),imodbits_armor|imodbit_lordly,],
["north_leather","Northmen_Leather_Vest",[("northmen_light_b1",imodbits_armor_bad),("northmen_light_b2",imodbit_plain),("northmen_light_b3",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,100,weight(7)|head_armor(0)|body_armor(13)|leg_armor(2)|difficulty(0),imodbits_armor,],
#Next 2 free, July 2018
["free_dale_armor_k","Dale_Noble_Armor",[("northmen_heavy_b",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2000,weight(22)|head_armor(2)|body_armor(38)|leg_armor(15)|difficulty(0),imodbits_armor|imodbit_lordly,],
["free_dale_armor_l","Dale_Noble_Gorget",[("dale_reward",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2000,weight(22)|head_armor(2)|body_armor(38)|leg_armor(15)|difficulty(0),imodbits_armor|imodbit_lordly,],
###########HELMS##########
["dale_helmet_a","Dale Light Infantry Helm",[("dale_helmet_a",0),("dale_helmet_a",imodbit_plain),("dale_helmet_a_good",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,800,weight(2)|abundance(92)|head_armor(28)|body_armor(0)|difficulty(10),imodbits_armor | imodbit_cracked],
["dale_helmet_b","Dale Light Archer Helm",[("dale_helmet_b",imodbit_plain),("dale_helmet_b",0),("dale_helmet_b_good",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,600,weight(2)|abundance(91)|head_armor(25)|body_armor(0)|difficulty(9),imodbits_armor | imodbit_cracked],
["dale_helmet_c","Dale Infantry Helm",[("dale_helmet_c",imodbit_plain),("dale_helmet_c",0),("dale_helmet_c_good",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1100,weight(4)|abundance(93)|head_armor(33)|body_armor(0)|difficulty(12),imodbits_armor|imodbit_lordly | imodbit_cracked],
["dale_helmet_d","Dale Archer Helm",[("dale_helmet_d",imodbit_plain),("dale_helmet_d",0),("dale_helmet_d_good",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,800,weight(3)|abundance(92)|head_armor(28)|body_armor(0)|difficulty(10),imodbits_armor|imodbit_lordly | imodbit_cracked],
["dale_helmet_e","Barding_Helm",[("dale_inf_helm_a",0),("dale_inf_helm_a_lordly",imodbit_lordly)],itp_type_head_armor|itp_shop,0,1200,weight(6)|abundance(95)|head_armor(35)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly],
["dale_helmet_f","Barding Helm",[("dale_inf_helm_c",0),("dale_inf_helm_c_lordly",imodbit_lordly)],itp_type_head_armor|itp_shop,0,1200,weight(6)|abundance(95)|head_armor(35)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly],
#########WEAPONS##########
["dale_sword","Dale_Shortsword",[("dale_sword_c",0),("scab_dale_sword_c",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,350,weight(1)|abundance(90)|difficulty(0)|spd_rtng(108)|weapon_length(77)|swing_damage(26,cut)|thrust_damage(23,pierce),imodbits_weapon],
["dale_sword_long","Dale_Longsword",[("dale_sword_a",0),("scab_dale_sword_a",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,500,weight(1.25)|abundance(92)|difficulty(11)|spd_rtng(101)|weapon_length(95)|swing_damage(29,cut)|thrust_damage(19,pierce),imodbits_weapon],
["dale_sword_broad","Dale_Infantry_Sword",[("dale_sword_b",0),("scab_dale_sword_b",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,500,weight(1.25)|abundance(91)|difficulty(0)|spd_rtng(103)|weapon_length(88)|swing_damage(28,cut)|thrust_damage(21,pierce),imodbits_weapon],
["dale_pike","Dale_Spear",[("dale_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_cant_use_on_horseback|itp_penalty_with_shield|itp_wooden_parry,itc_lance_upstab,250,weight(3)|abundance(90)|difficulty(0)|spd_rtng(95)|weapon_length(171)|thrust_damage(30,pierce)|swing_damage(0,blunt),imodbits_weapon_wood],
["dale_billhook","Dale_Billhook",[("dale_billhook",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_cant_use_on_horseback|itp_two_handed|itp_wooden_parry|itp_crush_through|itp_unbalanced,itc_cutting_spear,600,weight(4.5)|abundance(93)|difficulty(15)|spd_rtng(95)|weapon_length(185)|thrust_damage(31,pierce)|swing_damage(36,cut),imodbits_weapon_wood],
#####SHIELDS##########
["dale_shield_a","Dale_Tower_Shield",[("dale_shield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,300,weight(4)|abundance(92)|difficulty(3)|hit_points(320)|body_armor(13)|spd_rtng(80)|weapon_length(60),imodbits_shield,],
["dale_shield_b","Dale_Tower_Shield",[("dale_shield_i",0),("dale_shield_j",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop|itp_cant_use_on_horseback,itcf_carry_kite_shield,400,weight(4)|abundance(93)|difficulty(3)|hit_points(320)|body_armor(13)|spd_rtng(80)|weapon_length(60),imodbits_shield,],
["dale_shield_c","Dale_Round_Shield",[("dwarf_round_shield_e",0),("dwarf_round_shield_m",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(3)|abundance(91)|difficulty(2)|hit_points(280)|body_armor(15)|spd_rtng(87)|weapon_length(35),imodbits_shield,],
#unused Aug/Sept 2018:
["free_dale_shield_d","Dale_Shield",[("dwarf_round_shield_m",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,200,weight(2)|hit_points(360)|body_armor(8)|spd_rtng(82)|weapon_length(50),imodbits_shield,],

#TLD UMBAR ITEMS##########
##ARMOR##########
#next three free, July 2018
["free_umb_armor_a1","Corsair_Heavy_Leather_Armor",[("corsair_light_leather_1",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,500,weight(9)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0),imodbits_cloth,],
["free_umb_armor_d","Corsair_Heavy_Padded_Armor",[("corsair_leather_pad_1",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,700,weight(14)|head_armor(0)|body_armor(18)|leg_armor(5)|difficulty(0),imodbits_cloth,],
["free_umb_armor_g","Corsair_Hauberk_Pauldrons",[("corsair_mail_1",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2000,weight(22)|head_armor(0)|body_armor(25)|leg_armor(7)|difficulty(0),imodbits_armor|imodbit_lordly,],

["umb_armor_a","Corsair_Leather_Vest",	[("corsair_light_leather_1",0),("corsair_light_leather_0",imodbits_armor_bad),("corsair_light_leather_2",imodbits_armor_good),("corsair_light_leather_1b",imodbit_cloak)],itp_type_body_armor|itp_covers_legs|itp_shop,0,260,weight(4)|head_armor(0)|body_armor(10)|leg_armor(4)|difficulty(0),imodbits_armor|imodbit_lordly|imodbit_cloak,],
["umb_armor_b","Corsair_Leather_Armor",	[("corsair_leather_pad_1",0),("corsair_leather_pad_0",imodbits_armor_bad),("corsair_leather_pad_2",imodbits_armor_good),("corsair_leather_pad_1b",imodbit_cloak)],itp_type_body_armor|itp_covers_legs|itp_shop,0,400,weight(8)|head_armor(0)|body_armor(12)|leg_armor(5)|difficulty(0),imodbits_armor|imodbit_lordly|imodbit_cloak,],
["umb_armor_c","Corsair_Light_Scale",[("corsair_light_scale_1",imodbit_plain),("corsair_light_scale_1",0),("corsair_light_scale_0",imodbits_armor_bad),("corsair_light_scale_2",imodbits_armor_good),("corsair_light_scale_1b",imodbit_cloak)],itp_type_body_armor|itp_covers_legs|itp_shop,0,400,weight(12)|abundance(91)|head_armor(0)|body_armor(15)|leg_armor(4)|difficulty(9),imodbits_armor|imodbit_lordly|imodbit_cloak,],
["umb_armor_d","Corsair_Scale",[("corsair_scale_pad_1",imodbit_plain),("corsair_scale_pad_1",0),("corsair_scale_pad_0",imodbits_armor_bad),("corsair_scale_pad_3",imodbits_armor_good),("corsair_scale_pad_cape_pauldron",imodbit_cloak)],itp_type_body_armor|itp_covers_legs|itp_shop,0,400,weight(14)|abundance(92)|head_armor(0)|body_armor(16)|leg_armor(5)|difficulty(12),imodbits_armor|imodbit_lordly|imodbit_cloak,],
["umb_armor_e","Corsair_Hauberk",[("corsair_mail_1",imodbit_plain),("corsair_mail_1",0),("corsair_mail_0",imodbits_armor_bad),("corsair_mail_3",imodbits_armor_good),("corsair_mail_1b",imodbit_cloak)],itp_type_body_armor|itp_covers_legs|itp_shop,0,900,weight(20)|abundance(93)|head_armor(0)|body_armor(23)|leg_armor(7)|difficulty(9),imodbits_armor|imodbit_lordly|imodbit_cloak,],
["umb_armor_f","Corsair_Noble_Armour",[("corsair_heavy_1",imodbit_plain),("corsair_heavy_1",0),("corsair_heavy_0",imodbits_armor_bad),("corsair_heavy_2",imodbits_armor_good),("corsair_heavy_3",imodbit_cloak)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1100,weight(24)|abundance(94)|head_armor(1)|body_armor(25)|leg_armor(8)|difficulty(10),imodbits_armor|imodbit_lordly|imodbit_cloak,],
#######HELMS##########
["umb_helm_a","Corsair_Shell_Helm",[("shell_helmet",imodbit_plain),("shell_helmet",0),("shell_helmet_b",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1200,weight(4)|abundance(96)|head_armor(35)|body_armor(0)|difficulty(16),imodbits_elf_armor],
["umb_helm_b","Corsair_Tall_Helm",[("umbar_tall_helmet",imodbit_plain),("umbar_tall_helmet",0),("umbar_tall_helmet_b",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1200,weight(5)|abundance(96)|head_armor(35)|body_armor(0)|difficulty(16),imodbits_armor|imodbit_lordly],
["umb_helm_c","Corsair_Militia_Helm",[("umbar_militia_helmet",imodbit_plain),("umbar_militia_helmet",0),("umbar_militia_helmet_b",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,700,weight(2)|abundance(90)|head_armor(25)|body_armor(0)|difficulty(11),imodbits_armor | imodbit_cracked],
["umb_helm_d","Corsair_Raider_Helm",[("raider_helmet",imodbit_plain),("raider_helmet",0),("raider_helmet_b",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,800,weight(2)|abundance(90)|head_armor(28)|body_armor(0)|difficulty(12),imodbits_armor | imodbit_cracked],
["umb_helm_reward","Ancient_Numenorean_Karma",[("umbar_karma",0)],itp_type_head_armor|itp_unique,0,1200,weight(3)|head_armor(35)|difficulty(0),imodbits_armor|imodbit_lordly],
["free_umb_helm_f","Corsair_Tall_Helm",[("umbar_tall_helmet_b",0)],itp_type_head_armor|itp_shop,0,1200,weight(3)|head_armor(35)|difficulty(0),imodbits_armor|imodbit_lordly],
["corsair_trident","Trident_of_Sea_Fury",[("corsair_trident",0)],itp_type_polearm|itp_no_blur|itp_unique|itp_primary|itp_spear|itp_two_handed|itp_unique,itc_pike_upstab,2000,weight(4.5)|abundance(100)|difficulty(12)|spd_rtng(107)|weapon_length(166)|thrust_damage(42,pierce),imodbits_weapon_wood],
["corsair_boots","Corsair_Boots",[("corsair_boots",0)],itp_type_foot_armor|itp_shop|itp_attach_armature|itp_civilian,0,400,weight(1)|abundance(90)|leg_armor(14)|difficulty(0),imodbits_cloth],
########SHIELDS##########
["umb_shield_a","Corsair_Shield",[("corsair_buckler_long_a",0),("corsair_buckler_long_a_carry",ixmesh_carry),("corsair_buckler_long_b",imodbits_armor_good),("corsair_buckler_long_b_carry",ixmesh_carry|imodbits_armor_good)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_round_shield,300,weight(2)|abundance(92)|difficulty(1)|hit_points(240)|body_armor(16)|spd_rtng(92)|weapon_length(35),imodbits_shield,],
["umb_shield_b","Corsair_Buckler",[("corsair_buckler_round_a",0),("corsair_buckler_round_a_carry",ixmesh_carry)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_buckler_left,200,weight(1)|abundance(90)|difficulty(0)|hit_points(240)|body_armor(18)|spd_rtng(100)|weapon_length(20),imodbits_shield,],
["umb_shield_c","Corsair_Buckler",[("corsair_buckler_round_b",0),("corsair_buckler_round_b_carry",ixmesh_carry)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_buckler_left,200,weight(1)|abundance(90)|difficulty(0)|hit_points(240)|body_armor(18)|spd_rtng(100)|weapon_length(20),imodbits_shield,],
["umb_shield_d","Corsair_Buckler",[("corsair_buckler_round_c",0),("corsair_buckler_round_c_carry",ixmesh_carry)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_buckler_left,200,weight(1)|abundance(90)|difficulty(0)|hit_points(240)|body_armor(18)|spd_rtng(100)|weapon_length(20),imodbits_shield,],
##########WEAPONS##########
["umbar_spear","Umbar_Short_Spear",[("corsair_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_wooden_parry,itc_spear_upstab,200,weight(2)|abundance(90)|difficulty(0)|spd_rtng(102)|weapon_length(132)|swing_damage(19,blunt)|thrust_damage(26,pierce),imodbits_weapon_wood],
["umbar_cutlass","Umbar_Cutlass",[("corsair_cutlass",0),("scab_corsair_cutlass",ixmesh_carry|imodbits_good)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,350,weight(1.5)|abundance(91)|difficulty(0)|spd_rtng(104)|weapon_length(86)|swing_damage(26,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["kraken","Kraken_Cutlass",[("umbar_weapon_kraken_cutlass",0),("scab_kraken_cutlass",ixmesh_carry|imodbits_good)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_scimitar|itcf_carry_sword_left_hip,500,weight(1.5)|abundance(94)|difficulty(0)|spd_rtng(108)|weapon_length(103)|swing_damage(28,cut)|thrust_damage(0,pierce),imodbits_weapon_bad],
["umbar_rapier","Umbar_Boarding_Sword",[("corsair_sword_a",0),("scab_corsair_sword_a",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,450,weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(96)|weapon_length(81)|swing_damage(29,cut)|thrust_damage(26,pierce),imodbits_weapon_bad],
["corsair_harpoon","Corsair_Harpoon",[("corsair_harpoon",0),("corsair_harpoon_quiver", ixmesh_carry),("corsair_harpoon_quiver", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield|itp_can_penetrate_shield,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn,200,weight(4)|difficulty(3)|shoot_speed(27)|spd_rtng(85)|weapon_length(87)|thrust_damage(45,pierce)|accuracy(88)|max_ammo(3),imodbits_thrown,[] ],
["corsair_sword","Corsair_Eket",[("corsair_sword",0),("scab_corsair_sword",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,200,weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(113)|weapon_length(53)|swing_damage(24,cut)|thrust_damage(28,pierce),imodbits_weapon_bad],
["corsair_throwing_dagger","Crooked_Throwing_Daggers",[("corsair_throwing_dagger",0)],itp_type_thrown|itp_shop|itp_primary|0,itcf_throw_knife,250,weight(3.5)|difficulty(0)|shoot_speed(24)|spd_rtng(110)|weapon_length(0)|thrust_damage(30,cut)|max_ammo(10),imodbits_thrown],
["umbar_pike","Corsair_Trident",[("corsair_trident_b",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_cant_use_on_horseback|itp_spear|itp_penalty_with_shield|itp_wooden_parry,itc_lance_upstab,400,weight(3)|abundance(94)|difficulty(11)|spd_rtng(81)|weapon_length(175)|thrust_damage(39,cut),imodbits_weapon_wood],
#
#TLD NORTHMENMEN ITEMS##########
######ARMOR##########
["woodman_tunic","Woodmen_Tunic",			[("woodman_tunic",0),("woodman_tunic_cloak",imodbit_cloak),("woodman_tunic_light",imodbits_armor_bad),("woodman_tunic_heavy",imodbits_armor_good),("woodman_tunic_heavy_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,40,weight(4)|head_armor(0)|body_armor(7)|leg_armor(3)|difficulty(0),imodbits_armor|imodbit_lordly,],
["woodman_scout","Woodmen_Scout_Cape",		[("woodman_scout",0),("woodman_scout_cloak",imodbit_cloak),("woodman_scout_light",imodbits_armor_bad),("woodman_scout_heavy",imodbits_armor_good),("woodman_scout_heavy_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,600,weight(8)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0),imodbits_armor|imodbit_lordly,],
["woodman_padded","Woodmen_Padded_Armor",	[("woodman_padded",0),("woodman_padded_cloak",imodbit_cloak),("woodman_padded_light",imodbits_armor_bad),("woodman_padded_heavy",imodbits_armor_good),("woodman_padded_heavy_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,800,weight(12)|head_armor(0)|body_armor(20)|leg_armor(6)|difficulty(0),imodbits_armor|imodbit_lordly,],
["beorn_tunic","Beorning_Tunic",			[("beorn_tunic",0),("beorn_tunic_light",imodbits_armor_bad),("beorn_tunic_heavy",imodbits_armor_good)],	itp_type_body_armor|itp_covers_legs|itp_shop,0,30,weight(2)|head_armor(0)|body_armor(7)|leg_armor(3)|difficulty(0),imodbits_armor|imodbit_lordly,],
["beorn_padded","Beorning_Padded_Armor",	[("beorn_padded",0),("beorn_padded_light",imodbits_armor_bad),("beorn_padded_heavy",imodbits_armor_good)],	itp_type_body_armor|itp_covers_legs|itp_shop,0,500,weight(10)|head_armor(0)|body_armor(12)|leg_armor(6)|difficulty(0),imodbits_armor|imodbit_lordly,],
["beorn_heavy","Beorning_Heavy_Armor",		[("beorn_heavy",0),("beorn_heavy_light",imodbits_armor_bad),("beorn_heavy_heavy",imodbits_armor_good)],	itp_type_body_armor|itp_covers_legs|itp_shop,0,600,weight(13)|head_armor(0)|body_armor(16)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly,],
["beorn_berserk","Beorning_Berserker_Kit",	[("beorn_berserker",0),("beorn_berserker_light",imodbits_armor_bad),("beorn_berserker_heavy",imodbits_armor_good)],itp_type_body_armor|itp_covers_legs|itp_shop,0,500,weight(2)|head_armor(0)|body_armor(10)|leg_armor(6)|difficulty(0),imodbits_armor|imodbit_lordly,[custom_female("itm_beorn_berserk")]],
["beorn_chief","Beorning_Chieftan's_Tunic",[("beorn_chieftain",0)],itp_type_body_armor|itp_covers_legs,0,2300,weight(18)|abundance(100)|head_armor(1)|body_armor(33)|leg_armor(15)|difficulty(18),imodbits_armor|imodbit_lordly,],
######HELMS##########
["beorn_helmet","Bear_Skullcap",[("beorn_helmet",0),("beorn_helmet",imodbit_plain),("beorn_helmet_light",imodbits_armor_bad)],itp_type_head_armor|itp_shop,0,1000,weight(6)|abundance(94)|head_armor(32)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly | imodbit_cracked],
#####SHIELDS##########
["beorn_shield","Northmen_Shield",[("northmen_shield",0),("northmen_shield",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,200,weight(3)|abundance(90)|difficulty(1)|hit_points(290)|body_armor(14)|spd_rtng(86)|weapon_length(35),imodbits_shield,],
######WEAPONS###########
["beorn_axe","Beorning_Axe",[("beorning_axe",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_back,470,weight(5)|abundance(93)|difficulty(15)|spd_rtng(94)|weapon_length(92)|swing_damage(43,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
# use itm_dale_sword, itm_dwarf_sword_a, itm_dwarf_sword_b for Beorning's imported swords
["beorn_staff","Woodmen_Staff",[("woodman_staff",0),("gandstaff",imodbit_crude),("sarustaff",imodbit_tattered),],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack|itp_can_knock_down,itc_staff|itcf_carry_back,100,weight(2)|abundance(90)|difficulty(0)|spd_rtng(114)|weapon_length(104)|swing_damage(22,blunt)|thrust_damage(20,blunt),imodbits_weapon_wood],
["beorn_battle_axe","Beorning_War_Axe",[("beorning_war_axe",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through,itc_nodachi|itcf_carry_back,540,weight(6)|abundance(94)|difficulty(16)|spd_rtng(94)|weapon_length(90)|swing_damage(48,cut)|thrust_damage(0,pierce),imodbits_weapon_good],

###TLD DWARF ITEMS##########
########SHIELDS##########
["dwarf_shield_a","Dwarven_Angular_Shield",[("dwarf_angular_shield_a",0),("dwarf_angular_shield_b",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,300,weight(3)|abundance(91)|difficulty(2)|hit_points(320)|body_armor(16)|spd_rtng(86)|weapon_length(35),imodbits_shield_good,],
["dwarf_shield_b","Dwarven_Tower_Shield",[("dwarf_tear_shield_a",0),("dwarf_tear_shield_b",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,700,weight(3.5)|abundance(95)|difficulty(4)|hit_points(360)|body_armor(16)|spd_rtng(82)|weapon_length(60),imodbits_shield_good,],
["dwarf_shield_c","Dwarven_Fighting_Shield",[("dwarf_fighting_shield_a",0),("dwarf_fighting_shield_b",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(2)|abundance(94)|difficulty(3)|hit_points(310)|body_armor(18)|spd_rtng(88)|weapon_length(40),imodbits_shield_good,],
["dwarf_shield_d","Dwarven_Round_Shield",[("dwarf_round_shield_n",0),("dwarf_round_shield_e",imodbits_shield_good)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,250,weight(3)|abundance(90)|difficulty(0)|hit_points(300)|body_armor(16)|spd_rtng(90)|weapon_length(35),imodbits_shield_good,],
["north_round_shield","Northmen_Round_Shield",[("dwarf_round_shield_n",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,200,weight(3)|abundance(90)|difficulty(0)|hit_points(290)|body_armor(14)|spd_rtng(95)|weapon_length(35),imodbits_shield_good,],
#all shields from here free, May 2018
["free_dwarf_shield_g","Dwarven_Shield",[("dale_shield_b",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(3)|hit_points(700)|body_armor(10)|spd_rtng(82)|weapon_length(60),imodbits_shield_good,],
["free_dwarf_shield_i","Dwarven_Shield",[("dale_shield_i",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(3)|hit_points(700)|body_armor(10)|spd_rtng(82)|weapon_length(60),imodbits_shield_good,],
["free_dwarf_shield_j","Dwarven_Shield",[("dale_shield_j",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(3)|hit_points(700)|body_armor(10)|spd_rtng(82)|weapon_length(60),imodbits_shield_good,],
["free_dwarf_shield_k","Dwarven_Shield",[("dwarf_round_shield_n",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,400,weight(3)|hit_points(700)|body_armor(10)|spd_rtng(82)|weapon_length(60),imodbits_shield_good,],
["woodmen_heavy","Mirkwood_Armor",[("woodman_chieftain",0),("woodman_chieftain_cloak",imodbit_cloak),("woodman_chieftain_light",imodbits_armor_bad),("woodman_chieftain_heavy",imodbits_armor_good),("woodman_chieftain_heavy_cloak",imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2100,weight(18)|abundance(96)|head_armor(0)|body_armor(34)|leg_armor(12)|difficulty(13),imodbits_armor|imodbit_lordly|imodbit_cloak,],

#WEAPONS###########

["dwarf_sword_a","Dwarf_Sword",[("dwarf_sword_a",0),("scab_dwarf_sword_a",ixmesh_carry),("dwarf_sword_b",imodbits_weapon_good),("scab_dwarf_sword_b",imodbits_weapon_good|ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn,440,weight(1.25)|abundance(91)|difficulty(0)|spd_rtng(103)|weapon_length(66)|swing_damage(29,cut)|thrust_damage(21,pierce),imodbits_weapon_good],
["dwarf_sword_b","Beorning_Shortsword",[("beorning_seax",0),("beorning_seax_sheath",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn,440,weight(1.25)|abundance(90)|difficulty(0)|spd_rtng(105)|weapon_length(58)|swing_damage(31,cut)|thrust_damage(21,pierce),imodbits_weapon_good],

#next two not used by troops
["dwarf_sword_c","Dwarf_Sword",[("dwarf_sword_c",0),("scab_dwarf_sword_c",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn,440,weight(1.25)|abundance(91)|difficulty(0)|spd_rtng(103)|weapon_length(66)|swing_damage(29,cut)|thrust_damage(21,pierce),imodbits_weapon_good],
["dwarf_sword_d","Dwarf_Sword",[("dwarf_sword_d",0),("scab_dwarf_sword_d",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_shop,itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn,420,weight(1.25)|abundance(91)|difficulty(0)|spd_rtng(103)|weapon_length(58)|swing_damage(29,cut)|thrust_damage(21,pierce),imodbits_weapon_good],

["dwarf_battle_axe","Dwarf_Battle_Axe",[("dwarf_battle_axe",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,400,weight(2)|abundance(93)|difficulty(11)|spd_rtng(94)|weapon_length(61)|swing_damage(43,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
["dwarf_great_axe","Dwarf_Great_Axe",[("dwarf_great_axe",0),("dwarf_great_axe",0),("dwarf_great_axe_2",imodbits_weapon_good)],itp_type_two_handed_wpn|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through,itc_nodachi|itcf_carry_axe_back,540,weight(6)|abundance(94)|difficulty(16)|spd_rtng(86)|weapon_length(102)|swing_damage(47,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
["dwarf_great_mattock","Dwarf_Great_Mattock",[("dwarf_great_mattock",0),("dwarf_great_mattock",imodbit_plain),("dwarf_war_mattock",imodbits_weapon_good)],itp_type_two_handed_wpn|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,500,weight(5)|abundance(92)|difficulty(15)|spd_rtng(89)|weapon_length(94)|swing_damage(32,pierce)|thrust_damage(0,pierce),imodbits_weapon_good],
["dwarf_great_pick","Dwarf_Great_Pick",[("dwarf_great_pick",0),("dwarf_great_pick",0),("dwarf_war_pick",imodbits_weapon_good),("dwarf_war_pick_old",imodbit_old|imodbit_strong)],itp_type_two_handed_wpn|itp_unique|itp_shop|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_unbalanced,itc_nodachi|itcf_carry_axe_back,400,weight(5)|abundance(93)|difficulty(14)|spd_rtng(94)|weapon_length(90)|swing_damage(30,pierce)|thrust_damage(0,pierce),imodbits_weapon_good],
["dwarf_throwing_axe_reward","Erebor_Flying_Axes",[("dwarf_throw_axe_2",0)],itp_type_thrown|itp_unique|itp_primary|itp_bonus_against_shield|itp_can_penetrate_shield,itcf_throw_axe,1000,weight(5)|difficulty(4)|shoot_speed(34)|spd_rtng(99)|weapon_length(37)|thrust_damage(55,pierce)|accuracy(94)|max_ammo(6),imodbits_thrown,[] ],
["dwarf_mattock","Dwarf_Mattock",[("dwarf_mattock",imodbit_plain),("dwarf_mattock",0),("dwarf_adz",imodbits_weapon_good)],itp_type_two_handed_wpn|itp_shop|itp_primary|itp_wooden_parry|itp_cant_use_on_horseback,itc_bastardfalchion|itcf_carry_axe_left_hip,200,weight(3)|abundance(90)|difficulty(12)|spd_rtng(103)|weapon_length(52)|swing_damage(25,pierce)|thrust_damage(0,pierce),imodbits_weapon_good],
["dwarf_hand_axe","Dwarf_Short_Axe",[("dwarf_1h_axe",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_secondary|itp_bonus_against_shield|itp_wooden_parry,itc_scimitar|itcf_carry_axe_left_hip,200,weight(2)|abundance(90)|difficulty(10)|spd_rtng(97)|weapon_length(54)|swing_damage(36,cut)|thrust_damage(0,pierce),imodbits_weapon_good],
["dwarf_throwing_axe","Dwarf_Throwing_Axes",[("dwarf_throw_axe",0),("dwarf_throw_axe_quiver", ixmesh_carry),("dwarf_throw_axe_inventory", ixmesh_inventory)],itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield|itp_can_penetrate_shield,itcf_throw_axe|itcf_carry_quiver_front_right|itcf_show_holster_when_drawn,300,weight(5)|difficulty(2)|shoot_speed(26)|spd_rtng(99)|weapon_length(35)|thrust_damage(65,cut)|accuracy(90)|max_ammo(4),imodbits_thrown,[] ],
["dwarf_spear","Dwarf_Spear",[("dwarf_spear",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry,itc_spear_upstab,350,weight(2.25)|abundance(90)|difficulty(9)|spd_rtng(98)|weapon_length(140)|thrust_damage(26,pierce)|swing_damage(20,blunt),imodbits_weapon_good],
["dwarf_spear_b","Dwarf_Pike",[("dwarf_spear_b",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry,itc_lance_upstab,400,weight(2.25)|abundance(91)|difficulty(11)|spd_rtng(95)|weapon_length(165)|thrust_damage(29,pierce),imodbits_weapon_good],
["dwarf_spear_c","Dwarf_Longaxe",[("dwarf_longaxe",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_crush_through|itp_unbalanced,itc_cutting_spear,700,weight(6.5)|abundance(93)|difficulty(16)|spd_rtng(83)|weapon_length(150)|swing_damage(44,cut)|thrust_damage(27,pierce),imodbits_weapon_good],
#HELMS######### 
["dwarf_helm_coif","Dwarf_Coif",[("DwarfHelmCoif",imodbit_plain),("DwarfHelmCoif",0),("DwarfHelmCoifMask",imodbit_reinforced),("DwarfHelmCoifMask_B",imodbit_lordly)],itp_type_head_armor|itp_shop,0,400,weight(1)|abundance(90)|head_armor(20)|body_armor(0)|difficulty(9),imodbits_armor|imodbit_lordly],
["dwarf_nasal_b","Dwarf_Nasal_Helm",[("DwarfHelmConical_BChain",0)],itp_type_head_armor|itp_shop,0,1100,weight(3)|abundance(92)|head_armor(33)|body_armor(0)|difficulty(0),imodbits_armor|imodbit_lordly],
["north_skullcap","North_Skullcap",[("north_skullcap_bad",imodbits_armor_bad),("north_skullcap_ok",imodbit_plain),("north_skullcap_ok",0),("north_skullcap_good",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,600,weight(2)|abundance(91)|head_armor(25)|body_armor(0)|difficulty(9),imodbits_armor|imodbit_lordly|imodbit_cracked],
["dwarf_helm_kettle","Dwarf_Kettle_Helm",[("DwarfHelmConicalChain",imodbit_plain),("DwarfHelmConicalChain",0),("DwarfHelmConicalMask",imodbit_lordly)],itp_type_head_armor|itp_shop,0,1200,weight(4)|abundance(93)|head_armor(35)|body_armor(0)|difficulty(14),imodbits_armor|imodbit_lordly],
["dwarf_helm_fris","Dwarf_Frisian_Helm",[("DwarfHelmFrisianChain",imodbit_plain),("DwarfHelmFrisianChain",0),("DwarfHelmFrisianMask_A",imodbit_reinforced),("DwarfHelmFrisianMask_B",imodbit_lordly)],itp_type_head_armor|itp_shop,0,1400,weight(5)|abundance(94)|head_armor(37)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly],
["north_leather_skullcap","North_Light_Skullcap",[("north_leather_skullcap",imodbit_plain),("north_leather_skullcap",0),("north_leather_skullcap_bad",imodbits_armor_bad),("north_leather_skullcap_good",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,400,weight(1)|abundance(90)|head_armor(20)|body_armor(0)|difficulty(0),imodbits_armor|imodbit_cracked],
["dwarf_hood","Dwarf_Hood",[("DwarfHelmHood",0)],itp_type_head_armor|itp_shop,0,70,weight(1)|abundance(90)|head_armor(12)|body_armor(0)|difficulty(0),imodbits_elf_cloth],
["dwarf_nasal","Dwarf_Nasal_Tophelm",[("DwarfHelmIronheadNasal",imodbit_plain),("DwarfHelmIronheadNasal",0),("DwarfHelmIronheadNasal_reinf",imodbit_reinforced),("DwarfHelmIronheadFace",imodbit_lordly)],itp_type_head_armor|itp_shop,0,1400,weight(5)|abundance(94)|head_armor(37)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly],
["north_nasal_helm","North_Nasal_Helm",[("north_nasal",imodbit_plain),("north_nasal",0),("north_nasal_good",imodbits_armor_good)],itp_type_head_armor|itp_shop,0,1000,weight(4)|abundance(92)|head_armor(32)|body_armor(0)|difficulty(13),imodbits_armor|imodbit_lordly],
#next one only for reward item. NPCs use imod -> witchkinghelm
["dwarf_helm_p","Dwarf_King_Helm",[("DwarfHelmKingCrown",0)],itp_type_head_armor|0,0,2500,weight(9)|abundance(100)|head_armor(50)|body_armor(0)|difficulty(21),imodbits_armor|imodbit_lordly],
["dwarf_miner","Dwarf_Light_Helm",[("DwarfHelmMinerCap",imodbit_plain),("DwarfHelmMinerCap",0),("DwarfHelmMiner",imodbit_reinforced),("DwarfHelmMiner",imodbit_hardened)],itp_type_head_armor|itp_shop,0,200,weight(1)|abundance(90)|head_armor(14)|body_armor(0)|difficulty(0),imodbits_elf_cloth],
["north_chieftain","North_Chieftain_Helm",[("north_nasal_good",imodbit_plain)],itp_type_head_armor|itp_shop,0,1150,weight(5)|abundance(94)|head_armor(34)|body_armor(0)|difficulty(15),imodbits_armor|imodbit_lordly],
["dwarf_helm_round","Dwarf_Round_Helm",[("DwarfHelmRoundChain",imodbit_plain),("DwarfHelmRoundChain",0),("DwarfHelmRoundMask",imodbits_elf_armor)],itp_type_head_armor|itp_shop,0,1200,weight(4)|abundance(93)|head_armor(35)|body_armor(0)|difficulty(14),imodbits_armor|imodbit_lordly],
["dwarf_helm_sallet","Dwarf_Sallet",[("DwarfHelmSalletChain",imodbit_plain),("DwarfHelmSalletChain",0),("DwarfHelmSalletSargeant",imodbits_elf_armor)],itp_type_head_armor|itp_shop,0,1800,weight(8)|abundance(95)|head_armor(42)|body_armor(0)|difficulty(21),imodbits_armor|imodbit_lordly],
#########ARMOR##########
["dwarf_armor_d","Iron_Hills_Coat_of_Scales",[("dwarven_scale_mail",imodbit_plain),("dwarven_scale_mail",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2908,weight(32)|abundance(95)|head_armor(0)|body_armor(44)|leg_armor(10)|difficulty(20),imodbits_elf_armor,],
["dwarf_armor_a","Erebor_Surcoat_over_Mail",[("dwarven_tunic_over_mail_2",0),("dwarven_tunic_over_mail_1",imodbits_armor|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1508,weight(13)|abundance(92)|head_armor(0)|body_armor(29)|leg_armor(13)|difficulty(12),imodbits_armor|imodbit_lordly,],
["leather_dwarf_armor","Dwarven_Padded_Coat",[("dwarven_paddedlongcoat",imodbit_plain)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1208,weight(16)|abundance(92)|head_armor(0)|body_armor(30)|leg_armor(8)|difficulty(11),imodbits_armor|imodbit_lordly,],
["dwarf_armor_b","Erebor_Tunic_over_Mail",[("dwarf_tunicmail",0),("dwarf_tunicmail_scale",imodbits_armor|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,1808,weight(16)|abundance(93)|head_armor(0)|body_armor(34)|leg_armor(11)|difficulty(14),imodbits_armor|imodbit_lordly,],
["leather_dwarf_armor_b","Dwarven_Padded_Jerkin",[("dwarf_padtunic",0),("dwarf_padmail",imodbits_elf_cloth)],itp_type_body_armor|itp_covers_legs|itp_shop,0,908,weight(10)|head_armor(0)|body_armor(18)|leg_armor(8)|difficulty(0),imodbits_armor|imodbit_lordly,],
["dwarf_armor_c","Erebor_Scale_Mail",[("dwarf_scalemail_light",0),("dwarf_scalemail",imodbits_armor|imodbit_lordly)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2408,weight(28)|abundance(95)|head_armor(2)|body_armor(42)|leg_armor(12)|difficulty(18),imodbits_elf_armor,],
["dwarf_vest","Dwarven_Tunic",[("dwarf_tunic_erebor",0),("dwarf_tunic_ironhills",imodbits_elf_cloth)],itp_type_body_armor|itp_covers_legs|itp_shop,0,258,weight(5)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0),imodbits_armor|imodbit_lordly,],
["dwarf_vest_b","Iron_Hills_Mail",[("dwarf_mail",0)],itp_type_body_armor|itp_covers_legs|itp_shop,0,2008,weight(22)|abundance(94)|head_armor(0)|body_armor(36)|leg_armor(10)|difficulty(17),imodbits_armor|imodbit_lordly,],
["dwarf_pad_boots","Dwarven_Padded_Boots",[("fi_boot13_dwarf",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,508,weight(2)|abundance(90)|leg_armor(15)|difficulty(0),imodbits_armor|imodbit_lordly],
["dwarf_chain_boots","Dwarven_Mail_Chausses",[("dwarf_chain_boots",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,1408,weight(4)|abundance(92)|leg_armor(25)|difficulty(12),imodbits_armor|imodbit_lordly],
["dwarf_scale_boots","Dwarven_Scale_Boots",[("dwarf_scale_boots",0)],itp_type_foot_armor|itp_shop|itp_attach_armature,0,2008,weight(8)|abundance(94)|leg_armor(30)|difficulty(15),imodbits_armor|imodbit_lordly],

["good_mace","Mace",[("good_mace",0)],itp_type_one_handed_wpn|itp_primary|itp_shop|itp_wooden_parry|itp_wooden_attack,itc_scimitar|itcf_carry_mace_left_hip,250,weight(2.5)|abundance(91)|difficulty(11)|spd_rtng(90)|weapon_length(67)|swing_damage(25,blunt),imodbits_weapon_bad],

#next one unused (was planned for shield painting?)
["free_far_harad_shield_paint","Wicker_Shield",[("far_harad_c_giles",0)],itp_type_shield|itp_wooden_parry|itp_shop,itcf_carry_kite_shield,200,weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield,[(ti_on_init_item,[(cur_item_set_tableau_material, "tableau_far_harad_shield",0),])]],
#free, Jan 2017, -> rohan_armor_th:
["free_nazgulrobe","Nazgul_Robe",[("nazgulrobe",0),("old_nazgulrobe",imodbit_old)],itp_type_body_armor|itp_covers_legs|itp_covers_head|itp_replaces_helm|itp_civilian,0,1,weight(5)|head_armor(60)|body_armor(70)|leg_armor(70)|difficulty(0),0,],
#free Dec 2019, keep just a bit, players might have it in their party
["free_werewolf","Werewolf",    [("mm_warg_a",0)],   itp_type_horse|itp_unique, 0, 1200, hit_points(130)|body_armor(30)|horse_speed(60)|horse_maneuver(60)|horse_charge(25)|horse_scale(100)|difficulty(10),imodbits_none,[]],
#BANNERS  
# TODO: PLEASE DO NOT CHANGE BANNER ORDER, THIS IS A PLANNED FEATURE FOR THE MORALE SYSTEM. -CC #
["mordor_banner","Mordor_Banner",[("banner_mordor",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_wooden_parry|itp_cant_use_on_horseback, itc_banner,1000,weight(3)|difficulty(0)|spd_rtng(90)|weapon_length(120)|swing_damage(20,blunt)|thrust_damage(25,blunt),imodbits_weapon_wood],
["isengard_banner","Isengard_banner",[("banner_isengard",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_wooden_parry|itp_cant_use_on_horseback, itc_banner,1000,weight(3)|difficulty(0)|spd_rtng(90)|weapon_length(120)|swing_damage(20,blunt)|thrust_damage(25,blunt),imodbits_weapon_wood],
["woodelf_banner","Mirkwood_Banner",[("banner_mirkwood",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_wooden_parry|itp_cant_use_on_horseback, itc_banner,1000,weight(3)|difficulty(0)|spd_rtng(100)|weapon_length(120)|swing_damage(20,blunt)|thrust_damage(35,pierce),imodbits_weapon_good],
["lorien_banner","Lothlorien_Banner",[("banner_lorien",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_wooden_parry|itp_cant_use_on_horseback, itc_banner,1000,weight(3)|difficulty(0)|spd_rtng(100)|weapon_length(120)|swing_damage(20,blunt)|thrust_damage(35,pierce),imodbits_weapon_good],
["imladris_banner","Imladris_Banner",[("banner_rivendell",0)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_wooden_parry|itp_cant_use_on_horseback, itc_banner,1000,weight(3)|difficulty(0)|spd_rtng(100)|weapon_length(120)|swing_damage(20,blunt)|thrust_damage(35,pierce),imodbits_weapon_good],
["gondor_lance_banner","Gondor_Lance_With_Banner",[("banner_lance_gondor",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable, itc_banner,1000,weight(3)|difficulty(0)|spd_rtng(90)|weapon_length(217)|thrust_damage(28,pierce),imodbits_weapon_good],
["amroth_lance_banner","Dol_Amroth_Lance_With_Banner",[("banner_lance_dolamroth",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable, itc_banner,1000,weight(3)|difficulty(0)|spd_rtng(90)|weapon_length(217)|thrust_damage(28,pierce),imodbits_weapon_good],
["rohan_lance_banner_sun","Rohan_Lance_With_Sun_Banner",[("banner_lance_rohan_b",0)],itp_type_polearm|itp_no_blur|itp_shop|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable, itc_banner,1000,weight(3)|difficulty(0)|spd_rtng(90)|weapon_length(217)|thrust_damage(30,pierce),imodbits_weapon_good],
["rohan_lance_banner_horse","Rohan_Lance_With_Horse_Banner",[("banner_lance_rohan_a",0)],itp_type_polearm|itp_no_blur|itp_primary|itp_spear|itp_penalty_with_shield|itp_wooden_parry|itp_couchable, itc_banner,1000,weight(3)|difficulty(0)|spd_rtng(90)|weapon_length(217)|thrust_damage(30,pierce),imodbits_weapon_good],
#both free, Jan 2017, ->rohan_armor_th:
["free_merry_outfit","hobbit_outfit",[("merry",0)],itp_type_body_armor|itp_covers_legs|itp_unique,0,1,weight(1)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0),0,],
["free_pippin_outfit","hobbit_outfit",[("pippin",0)],itp_type_body_armor|itp_covers_legs|itp_unique,0,1,weight(1)|head_armor(0)|body_armor(0)|leg_armor(0)|difficulty(0),0,],

#Trolls and Ents
["ent_body","Ent_Body",[("ent_body",0),("olog_body",imodbit_rusty),("olog_body_b",imodbit_tattered),("isen_olog_body",imodbit_old),("isen_olog_body_b",imodbit_cheap),],itp_no_pick_up_from_ground|itp_type_body_armor|itp_covers_legs|itp_unique,0,1,weight(250)|head_armor(0)|body_armor(55)|leg_armor(0)|difficulty(25),0,],
["ent_head_helm","Ent_Head",[("ent_head1",0),("olog_head",imodbit_hardened),("olog_head_b",imodbit_reinforced),("olog_head_c",imodbit_lordly),("ent_head1",imodbit_smelling),("ent_head2",imodbit_rotten),("ent_head3",imodbit_day_old),("isen_olog_head",imodbit_bent),("isen_olog_head_b",imodbit_old),("isen_olog_head_c",imodbit_cheap)],itp_type_head_armor|itp_unique,0,1,weight(250)|head_armor(60)|difficulty(30),0],
["troll_head","troll_head",[("ent_head2",0),("troll_head",imodbit_rotten),("troll_head_b",imodbit_two_day_old),("troll_head_c",imodbit_day_old),("gunda_troll_head",imodbit_smelling),("gunda_troll_head_b",imodbit_fresh),("gunda_troll_head_c",imodbit_large_bag),("mordor_troll_head",imodbit_thick),("mordor_troll_head_b",imodbit_hardened)],itp_type_head_armor|itp_unique,0,1,weight(250)|head_armor(40)|difficulty(30),0],
["troll_body","troll_body",[("troll_body",0),("gunda_troll_body",imodbit_thick),("mordor_troll_body",imodbit_hardened),("troll_body",imodbit_day_old),("gunda_troll_body_berta",imodbit_rotten),],itp_no_pick_up_from_ground|itp_type_body_armor|itp_covers_legs|itp_unique,0,10,weight(250)|head_armor(0)|body_armor(40)|leg_armor(0)|difficulty(25),0,],
["ent_feet_boots","Ent_Feet",[("ent_foot",0),("troll_feet",imodbit_cracked),("gunda_troll_feet",imodbit_rusty),("mordor_troll_feet",imodbit_bent),("olog_feet",imodbit_hardened),("olog_feet",imodbit_thick)],itp_type_foot_armor|itp_unique,0,1,weight(250)|head_armor(0)|body_armor(0)|leg_armor(60)|difficulty(30),0],
["ent_hands","Ent_Hands",[("ent_hand_L",0),("olog_hand_L",imodbit_large_bag),("isen_olog_hand_L",imodbit_rotten),("troll_handL",imodbit_cracked),("gunda_troll_handL",imodbit_rusty),("mordor_troll_handL",imodbit_bent)],itp_type_hand_armor|itp_unique,0,1,weight(250)|body_armor(1)|difficulty(30),0],
["fur_gloves_reward","Hunter_Gloves",[("narf_demi_gauntlets_fur_L",0)],itp_type_hand_armor|itp_unique,0,2000,weight(0.2)|body_armor(3)|difficulty(0),imodbits_none,[]],
["empty_hands","empty_hands",[("dummy_mesh",0)],itp_type_hand_armor|itp_unique|itp_no_pick_up_from_ground,0,130,weight(225)|body_armor(1)|difficulty(0),0],
["empty_legs","empty_legs",[("dummy_mesh_skinned",0)],itp_type_foot_armor|itp_unique|itp_no_pick_up_from_ground,0,130,weight(225)|leg_armor(1)|difficulty(0),0],
["empty_head","empty head",[("dummy_mesh",0),("chieftainhelm",imodbit_old), ("pointedhelmet", imodbit_poor)],itp_type_head_armor|itp_unique|itp_covers_beard|itp_covers_head|itp_no_pick_up_from_ground,0,1,weight(250)|head_armor(50)|difficulty(0),0],

#### TLD REWARD ITEMS BEGIN
# magic items begin
["ent_water","Strange_Bowl_of_Water",[("ent_water",0)],itp_unique|itp_type_goods,0,200,weight(2)|abundance(0)|0,imodbits_none],
["map","Maps_of_Middle_Earth",[("middle_earth_map",0)],itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["athelas_reward","Dried_Athelas_Leaves",[("athelas_plant",0)],itp_type_goods|itp_consumable,0,1000,weight(0.2)|abundance(0)|max_ammo(3),imodbits_none],
["phial_reward","Light_of_Galadriel",[("galadriel_light",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["scroll_reward","On_the_Fall_of_Gondolin",[("quenya_scroll",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["hammer_reward","Smith's_Hammer",[("smith_hammer",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["khand_knife_reward","Khand_Sacrificial_Knife",[("khand_sacrificial_knife",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["angmar_whip_reward","Master's_Whip",[("AngmarWhip",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["horn_gondor_reward","Horn_of_Gondor",[("GondorHorn",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["harad_totem_reward","Harad_Totem",[("harad_totem",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["elven_amulet_reward","Elven_Amulet",[("elven_amulet",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["torque_reward","Evil_Torque",[("reward_torque",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["orc_brew","Orc_Brew",[("orc_brew",0)],itp_type_goods|itp_consumable,0,1000,weight(0.2)|abundance(0)|max_ammo(5),imodbits_none],
["rohan_saddle","Saddle",[("RohanSaddle",0),("RohanSaddle",imodbit_lordly),("rhunsaddle",imodbit_heavy),("haradsaddle",imodbit_masterwork)],itp_unique|itp_type_goods,0,5000,weight(4)|abundance(0)|0,imodbits_none],
["mearas_reward","Mearh_Stallion",[("mearh",0)],itp_type_horse|itp_unique,0,4000,hit_points(180)|body_armor(45)|difficulty(5)|horse_speed(50)|horse_maneuver(50)|horse_charge(40)|horse_scale(105)|abundance(100),imodbits_horse_basic|0],
["shield_of_tuor","Shield_of_Tuor",[("Avelium_shield_of_tuor",0)],itp_type_shield|itp_wooden_parry|itp_unique,itcf_carry_kite_shield,4000,weight(4)|abundance(100)|difficulty(5)|hit_points(450)|body_armor(22)|spd_rtng(84)|weapon_length(70),imodbits_none,],
#["sword_of_arathorn","Arathorn's_Sword",[("aragorn_sword",0),("scab_aragorn_sword",ixmesh_carry)],itp_type_two_handed_wpn|itp_primary|itp_bonus_against_shield|itp_unique,itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,2000,weight(2.05)|difficulty(15)|spd_rtng(110)|weapon_length(120)|swing_damage(40,pierce)|thrust_damage(30,pierce),imodbits_weapon_good],
["riv_armor_reward","Rivendell_Decorated_Armor",[("rivendellrewardarmour",0)],itp_type_body_armor|itp_covers_legs|0,0,4200,weight(24)|abundance(100)|head_armor(2)|body_armor(44)|leg_armor(21)|difficulty(15),imodbits_armor|imodbit_lordly,],
["westernesse1h_reward","Sword_of_Westernesse",[("westernesse_1h",0),("scab_1h_westernesse",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_unique,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,3000,weight(1.25)|difficulty(15)|spd_rtng(117)|weapon_length(77)|swing_damage(38,pierce)|thrust_damage(45,pierce),imodbits_weapon_good],
["westernesse2h_reward",	"Sword_of_Westernesse",	[("westernesse_2h",0),("scab_2h_westernesse",ixmesh_carry)],	itp_type_two_handed_wpn|itp_primary|itp_unique,	itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,200,	weight(2.5)	|difficulty(18)	|spd_rtng(110)	|weapon_length(106)	|swing_damage(45,pierce)	|thrust_damage(45,pierce)	,imodbits_weapon_good],
["mirkwood_sword_reward","Greenwood_Relic_Sword",[("mirkwood_sword",0),("scab_mirkwood_sword",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield|itp_unique,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,200,weight(1.5)|difficulty(12)|spd_rtng(110)|weapon_length(90)|swing_damage(42,pierce)|thrust_damage(45,pierce),imodbits_weapon_good],
["nazgul_sword",	"Wicked_Sword",	[("nazgul_sword_giles",0),("scab_nazgul_sword_giles",ixmesh_carry)],itp_type_two_handed_wpn|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_unique|itp_crush_through,	itc_bastardsword|itcf_carry_sword_back|itcf_show_holster_when_drawn,200,	weight(4.5)	|difficulty(18)	|spd_rtng(103)	|weapon_length(112)	|swing_damage(50,pierce)	|thrust_damage(45,pierce)	,imodbits_weapon_good],
["cooking_cauldron","Cooking_Cauldron",[("cauldron_a",0)],itp_type_goods,0,1000,weight(3)|abundance(0)|0,imodbits_none],
["eorl_cavalry_sword","Sword_of_Eorl",[("eorl_cavalry_sword_b_longer",0)],itp_type_two_handed_wpn|itp_primary|itp_bonus_against_shield|itp_unique,itc_bastardsword|itcf_carry_sword_left_hip,3000,weight(3)|difficulty(18)|spd_rtng(97)|weapon_length(110)|swing_damage(52,cut)|thrust_damage(22,pierce),imodbits_weapon_good],
["garlic_reward","Garlic",[("garlic.9",0)],itp_type_goods,0,1000,weight(3)|abundance(0)|0,imodbits_none],
["silmarillion_reward","Silmarillion",[("JIKBookClosed",0)],itp_unique|itp_type_goods,0,1000,weight(3)|abundance(0)|0,imodbits_none],
["herbarium_reward","Middle_Earth_Herbarium",[("JIKBookOpen",0)],itp_unique|itp_type_goods,0,1000,weight(3)|abundance(0)|0,imodbits_none],
["book_of_moria","Book_of_Mazarbul",[("JIKBookClosed",0)],itp_unique|itp_type_goods,0,1000,weight(3)|abundance(0)|0,imodbits_none],
["ring_a_reward","Tulcarisil",[("reward_ring_a",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["ring_b_reward","Finwarisil",[("reward_ring_b",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["dale_bow_reward","Bow_of_Bard",[("GA_BowE_Longbow_A",0),("GA_BowE_Longbow_A_Carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_two_handed|itp_unique|itp_cant_use_on_horseback,itcf_shoot_bow|itcf_carry_bow_back,3000,weight(1.5)|difficulty(5)|shoot_speed(69)|spd_rtng(90)|thrust_damage(28,pierce)|accuracy(100),0,[] ],
["tome_of_knowledge","Tome_of_Arcane_Knowledge",[("JIKBookOpen_dark",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["orc_idol_reward","Idol_of_the_First_Orc",[("orc_idol",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
["crebain_reward","Crebain",[("prop_reward_crebain",0)],itp_unique|itp_type_goods,0,1000,weight(1)|abundance(0)|0,imodbits_none],
["miruvor_reward","Miruvor_Flask",[("reward_miruvor",0)],itp_type_goods|itp_consumable,0,1000,weight(5)|abundance(0)|max_ammo(8),imodbits_none],
["wheeled_cage","Giant_Wheeled_Cage",[("wheeled_cage",0)],itp_unique|itp_type_goods,0,1000,weight(250)|abundance(0)|0,imodbits_none],
["orc_throwing_axes_reward","Gundabad_Flying_Axes",[("orc_throwing_axe",0)],itp_type_thrown|itp_unique|itp_primary|itp_bonus_against_shield|itp_can_penetrate_shield,itcf_throw_axe,150,weight(4)|difficulty(1)|shoot_speed(30)|spd_rtng(103)|weapon_length(33)|thrust_damage(55,cut)|max_ammo(6),imodbits_thrown],
["corsair_throwing_dagger_reward","Poisoned_Throwing_Daggers",[("corsair_throwing_dagger",0)],itp_type_thrown|itp_unique|itp_primary|itp_can_penetrate_shield,itcf_throw_knife,200,weight(3.5)|difficulty(0)|shoot_speed(26)|spd_rtng(110)|weapon_length(0)|thrust_damage(50,cut)|max_ammo(10),imodbits_thrown],
["dwarf_shield_reward","Shield_of_Kheled-zaram",[("mithril_shield",0)],itp_type_shield|itp_wooden_parry|itp_unique,itcf_carry_kite_shield,4000,weight(4)|abundance(100)|difficulty(5)|hit_points(450)|body_armor(35)|spd_rtng(82)|weapon_length(60),imodbits_none,],
["dwarf_great_axe_reward","Dwarf_Sharp_Axe",[("dwarf_great_axe_2",0),("dwarf_great_axe_2_dain",imodbit_rotten)],itp_type_polearm|itp_no_blur|itp_unique|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_wooden_parry|itp_cant_use_on_horseback|itp_crush_through|itp_can_knock_down,itc_nodachi|itcf_carry_axe_back,700,weight(6)|difficulty(18)|spd_rtng(90)|weapon_length(110)|swing_damage(55,pierce)|thrust_damage(0,pierce),imodbits_none],
["isen_uruk_heavy_reward","Uruk-hai_General_Armor",[("urukhai_isen_plate_c1",0)],itp_type_body_armor|itp_covers_legs|itp_unique,0,2802,weight(38)|abundance(96)|head_armor(2)|body_armor(44)|leg_armor(15)|difficulty(18),imodbits_none,],
["lorien_bow_reward","Noldorin_Bow",[("Vyrn_bow_1_shortened",0),("Vyrn_bow_1_shortened",ixmesh_carry)],itp_type_bow|itp_primary|itp_unique,itcf_shoot_bow|itcf_carry_bowcase_left,3000,weight(1.5)|difficulty(5)|shoot_speed(54)|spd_rtng(96)|thrust_damage(21,pierce)|accuracy(93),0,[] ],
["elven_cloak","Elven_Cloak",[("elven_cloak",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],
#["lorien_sword_reward","Galadhrim_Sword",[("lorien_sword_hand_and_half",0),("scab_lorien_sword_hand_and_half",ixmesh_carry)],itp_type_two_handed_wpn|itp_primary|itp_unique,itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,900,weight(2.5)|difficulty(0)|spd_rtng(115)|weapon_length(103)|swing_damage(43,cut)|thrust_damage(33,pierce),imodbits_none],
["dale_sword_reward","Dale_Royal_Sword",[("Mandible_royal_sword",0),("Mandible_royal_sword_scabbard",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary|itp_unique,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,500,weight(1.25)|difficulty(12)|spd_rtng(97)|weapon_length(110)|swing_damage(48,cut)|thrust_damage(30,pierce),imodbits_none],
["dale_armor_reward","Dale_Noblemen_Mail",[("dale_reward",0)],itp_type_body_armor|itp_covers_legs|itp_unique,0,2600,weight(25)|abundance(100)|head_armor(4)|body_armor(36)|leg_armor(15)|difficulty(20),imodbits_none,],
["leather_gloves_reward","Archer_Gloves",[("CWE_gloves_king_L",0),("CWE_gloves_a_black_L",imodbit_crude),("ent_hand_L",imodbit_tattered),("olog_hand_L",imodbit_rusty),("isen_olog_hand_L",imodbit_old)],itp_type_hand_armor|itp_unique,0,2000,weight(0.2)|body_armor(3)|difficulty(0),imodbits_none,[]],
["beorn_shield_reward","Beorning_Shield",[("beorning_shield",0),("gandstaff_shield",imodbit_crude),],itp_type_shield|itp_wooden_parry|itp_unique,itcf_carry_round_shield,4000,weight(4.5)|abundance(100)|difficulty(3)|hit_points(340)|body_armor(18)|spd_rtng(95)|weapon_length(55),imodbits_shield,],
["beorn_axe_reward","Bear_Club",[("beorning_club",0)],itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_wooden_attack|itp_crush_through|itp_can_knock_down|itp_unique,itc_scimitar|itcf_carry_mace_left_hip,2000,weight(4.5)|difficulty(12)|spd_rtng(93)|weapon_length(67)|swing_damage(32,blunt),imodbits_weapon_good],
["drums_of_the_deep","Drums_of_the_Deep",[("moria_drum",0)],itp_unique|itp_type_goods,0,1000,weight(0.2)|abundance(0)|0,imodbits_none],

["khamul_helm","Helm_of_Khamul",[("helmet_khamul_small_new",0)],itp_type_head_armor|itp_unique,0,3000,weight(10)|abundance(100)|head_armor(50)|body_armor(0)|difficulty(23),0],
["black_arrows_reward","Black_Arrows",[("khazad_orc_arrow_2",0),("khazad_orc_arrow_2.lod2",ixmesh_flying_ammo),("khazad_orc_arrow_2_quiver",ixmesh_carry),("rohan_arrow2_black",imodbit_masterwork),("rohan_arrow2_black_flying",ixmesh_flying_ammo|imodbit_masterwork),("rohan_quiver2_black",ixmesh_carry|imodbit_masterwork)],itp_type_arrows|itp_unique|itp_can_penetrate_shield|itp_no_pick_up_from_ground|itp_crush_through,itcf_carry_quiver_back_right,2000,weight(3)|thrust_damage(3,cut)|max_ammo(25)|weapon_length(95),imodbits_missile,[]],
["leather_boots_reward","Hunter_Boots",[("got_stark_hanter_boots",0)],itp_type_foot_armor|itp_unique,0,200,weight(1)|leg_armor(22)|difficulty(0),imodbits_cloth],
#["sarustaff","Wizards_Staff",[("sarustaff",0)],itp_primary|itp_wooden_parry|itp_type_polearm|itp_no_blur|itp_spear|itp_penalty_with_shield|itp_wooden_attack,itc_staff,1,weight(2.5)|difficulty(0)|spd_rtng(103)|weapon_length(118)|swing_damage(50,blunt)|thrust_damage(40,blunt),0],
["rohan_armor_th","Rohan_Royal_Armor",[("theoden_armour",0),("dno_priest_3_1_dark",imodbit_well_made),("dm_nazgulrobe",imodbit_cheap),("tld_robe_generic_dress",imodbit_old),("pippin",imodbit_battered),("merry",imodbit_chipped),("dno_priest_3_1",imodbit_rotten),("dno_priest_3_final",imodbit_bent), ("old_nazgulrobe",imodbit_old),("galadriel",imodbit_rusty)],itp_type_body_armor|itp_covers_legs,0,4800,weight(35)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(25)|difficulty(18),imodbits_armor|imodbit_lordly,],
["wilderness_cowl","Hunter_Cowl",[("got_stark_hood",0)],itp_type_head_armor|itp_unique|itp_fit_to_head,0,1000,weight(1)|head_armor(12)|difficulty(0),imodbits_armor,[]],
["prisoner_coll_chain","Prisoner_Chains",[("prisoner_coll_chain",0)],itp_type_head_armor|itp_doesnt_cover_hair,0,10,weight(10)|head_armor(2)|difficulty(0),0],
["witchking_helmet","Sorcerer's_Mask",[("witchking_helmet",0),("glorfindelhair",imodbit_rotten),("DwarfHelmKingCrown",imodbit_old),("tiara",imodbit_well_made)],itp_type_head_armor|itp_unique,0,3000,weight(6)|abundance(100)|head_armor(30)|body_armor(5)|difficulty(18),0],
# let   witchking_helmet  be the last item (mtarini)
["free_lorien_royal_armor","Lorien_Royal_Armor",[("lorien_royal",0)],itp_type_body_armor|itp_covers_legs,0,4000,weight(26)|abundance(100)|head_armor(1)|body_armor(46)|leg_armor(17)|difficulty(15),imodbits_armor|imodbit_lordly,],
["feet_chains","Feet Chains",[("chains_full",0)],itp_type_foot_armor|itp_attach_armature,0,200,weight(10)|leg_armor(0)|difficulty(0),imodbits_none],
["feet_chains_dwarf","Feet Chains",[("chains_full_dwarf",0)],itp_type_foot_armor|itp_attach_armature,0,200,weight(10)|leg_armor(0)|difficulty(0),imodbits_none],

["spider","Spider",[("spider",0)], itp_type_horse|itp_unique|itp_disable_agent_sounds, 0, 1200, hit_points(60)|body_armor(30)|difficulty(3)|horse_speed(50)|horse_maneuver(75)|horse_charge(25),imodbits_none,[]],
["bear","Bear",    [("bear_2",0)],   itp_type_horse|itp_unique, 0, 1200, hit_points(130)|body_armor(48)|horse_speed(50)|horse_maneuver(48)|horse_charge(25)|horse_scale(120)|difficulty(10),imodbits_none,[]],
["wolf","Wolf",    [("wolf",0)],   itp_type_horse|itp_unique, 0, 1200, hit_points(50)|body_armor(25)|horse_speed(50)|horse_maneuver(50)|horse_charge(25)|horse_scale(85)|difficulty(10),imodbits_none,[]],
["werewolf","Werewolf",    [("mm_warg_a",0)],   itp_type_horse|itp_unique, 0, 1200, hit_points(130)|body_armor(35)|horse_speed(60)|horse_maneuver(60)|horse_charge(35)|horse_scale(100)|difficulty(10),imodbits_none,[]],

["thrush_reward","Thrush",[("prop_reward_thrush",0)],itp_unique|itp_type_goods,0,1000,weight(1)|abundance(0)|0,imodbits_none],
["gauntlets_reward","Iron_Fists",[("narf_finger_gauntlets_L",0),("CWE_gauntlets_arabs_a_dwarf_L",imodbit_lordly),],itp_type_hand_armor|itp_unique,0,2000,weight(2)|body_armor(4)|difficulty(15),imodbits_none,[]],

#last item for MnB
["save_compartibility_item10","INVALID_ITEM",[("practice_sword",0)],itp_type_goods,0,3,weight(1.5)|abundance(90)|0,imodbits_none],

] + (is_a_wb_item==1 and [

#Padded Cloth Custom
["gondor_custom", "Custom Gondor", [("gondor_knight",0)], itp_type_body_armor|itp_covers_legs|itp_unique,0,1500,weight(20)|head_armor(0)|body_armor(35)|leg_armor(9)|difficulty(0),imodbits_armor|imodbit_lordly,
 [custom_reskin("itm_gondor_custom")]], 

["stones_siege",         "Siege Stones", [("gon_castle_h_stairs_b",0)], itp_type_thrown |itp_unique|itp_primary ,itcf_throw_stone, 10 , weight(5)|difficulty(1)|spd_rtng(50) | shoot_speed(4) | thrust_damage(28 ,  blunt)|max_ammo(20)|weapon_length(200),imodbits_none,
[
    (ti_on_missile_hit,
      [
	  (try_begin),
		#Solid Round Script
        #pos1 - Missile hit position
        #param_1 - Shooter agent
		(store_trigger_param_1,":shooter"),
    	(set_fixed_point_multiplier, 100),
		(copy_position, pos63, pos1),
		(particle_system_burst,"psys_piedra_dust",pos1,1),
		(try_for_agents,":agent",pos63,300),
	      (neg|agent_is_ally,":agent"),
	      (agent_is_active,":agent"),
	      (agent_is_alive,":agent"),
	      (neq,":agent",":shooter"),

	      (assign, reg0, 5),			   

	      (agent_get_position, pos62, ":agent"),
	      (get_distance_between_positions, ":distance", pos63, pos62),

	      (try_begin),
	      	(lt, ":distance", 200),
	      	(store_random_in_range, reg0, 30, 41),
	      	(assign, ":hit_anim", "anim_strike_fly_back"),
	      (else_try),
	      	(is_between, ":distance", 200, 300),
	      	(store_random_in_range, reg0, 15, 21),
	      	(assign, ":hit_anim", "anim_strike_legs_front"),
	      (else_try),
	      	(ge, ":distance", 300),
	      	(store_random_in_range, reg0, 5, 10),
	      	(assign, ":hit_anim", "anim_strike_legs_front"),
	      (try_end),

	      (set_show_messages, 0),
	      (agent_deliver_damage_to_agent,":shooter",":agent", reg0),
	      (set_show_messages, 1),
	      (agent_set_animation, ":agent", ":hit_anim"),
	      (try_begin),
	        (get_player_agent_no, ":player"),
	        (eq, ":agent", ":player"),
	        (display_message, "@Received {reg0} damage."),
	      (try_end),
	      (val_add, reg10, 1), #count number agents got hit
	      (play_sound,"snd_shield_broken"),
      	(try_end),
		(display_message, "@Siege Weapon damaged {reg10} agents", color_bad_news),
		(assign, reg10, 0),
	(try_end),
	]),
]],

["beorn_axe_no_attack","Beorning_Axe", [("beorning_axe",0)],itp_type_polearm|itp_no_blur|itp_two_handed|itp_primary|itp_bonus_against_shield,itc_parry_polearm|itcf_carry_axe_back,9, weight(5)|spd_rtng(91) | weapon_length(76)|swing_damage(0,blunt) | thrust_damage(0,blunt),imodbits_none],

#Civilian items, 
#WB civilian items
["tabard_b_wb","Tabard",[("tabard_b",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["nobleman_outfit_b_new_wb","Nobleman Outfit",[("nobleman_outfit_b_new",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["peasant_man_a_wb","Peasant_Outfit",[("peasant_man_a",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["leather_jerkin_wb","Leather_Jerkin",[("ragged_leather_jerkin",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,300,weight(6)|head_armor(0)|body_armor(10)|leg_armor(6)|difficulty(0),imodbits_cloth,[]],
["white_tunic_c_wb","Tunic_Jacket",[("coarse_tunic_a_new",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["white_tunic_a_wb","White_Tunic",[("shirt_a",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["red_tunic_wb","Red_Tunic",[("rich_tunic_a",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["fur_coat_wb","Dale_Coat",[("dale_coat",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,400,weight(6)|head_armor(0)|body_armor(13)|leg_armor(6)|difficulty(0),imodbits_cloth,[]],
["fur_hat_a_new_wb","Fur_Hat",[("fur_hat_a_new",0)],itp_type_head_armor|itp_fit_to_head|itp_doesnt_cover_hair|itp_civilian,0,100,weight(1)|head_armor(12)|difficulty(0),imodbits_armor,[]],
["noel_hat_a_wb","Fur_Hat",[("noel_hat_a",0)],itp_type_head_armor|itp_fit_to_head,0,100,weight(1)|head_armor(12)|difficulty(0),imodbits_armor,[]],
["peasant_dress_b_new_wb","Blue Dress",[("peasant_dress_b_new",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["sarranid_lady_dress_wb","Blue Dress",[("sarranid_lady_dress",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["sar_robe_b_wb","Robe",[("sar_robe_b",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],

# TLD civilian items
["black_dress_wb","Black_Dress",[("gondor_dress_a",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,500,weight(3)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0),imodbits_cloth,[]],
["blackwhite_dress_wb","Lady_Dress",[("gondor_dress_b",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,500,weight(3)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0),imodbits_cloth,[]],
["white_tunic_b_wb","Simple_Tunic",[("gondor_tunic_b",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["blue_tunic_wb","Blue_Tunic",[("dale_tunic",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["black_tunic_wb","Black_Tunic",[("gondor_tunic",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["green_tunic_wb","Green_Tunic",[("rohan_tunic",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(3)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
#not used on walkers
#["leather_apron","Leather_Apron",[("smith_leather_apron",0)],itp_type_body_armor|itp_covers_legs|itp_civilian|itp_shop,0,50,weight(3)|head_armor(0)|body_armor(8)|leg_armor(7)|difficulty(0),imodbits_cloth,[]],
["green_dress_wb","Green_Dress",[("rohan_dress",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,500,weight(6)|head_armor(0)|body_armor(10)|leg_armor(6)|difficulty(0),imodbits_cloth,[]],
["gondor_fine_outfit_dress_wb","Fine_Outfit",[("gondor_fine_outfit_dress",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,500,weight(3)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0),imodbits_cloth,[]],
["rohan_fine_outfit_dale_dress_wb","Fine_Outfit",[("rohan_fine_outfit_dale_dress",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,500,weight(3)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0),imodbits_cloth,[]],
["robe_generic_dress_wb","Robe",[("tld_robe_generic_dress",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,500,weight(3)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0),imodbits_cloth,[]],
["wimple_a_wb","Wimple",[("gondor_wimple_a",0)],itp_type_head_armor|itp_civilian|itp_fit_to_head,0,10,weight(0.5)|head_armor(4)|difficulty(0),imodbits_cloth,[]],
["wimple_with_veil_wb","Wimple",[("gondor_wimple_b",0)],itp_type_head_armor|itp_civilian|itp_fit_to_head,0,10,weight(0.5)|head_armor(4)|difficulty(0),imodbits_cloth,[]],
["fine_hat_wb","Fine_Hat",[("gondor_fine_fem_hat",0)],itp_type_head_armor|itp_civilian,0,10,weight(0.5)|head_armor(4)|difficulty(0),imodbits_cloth,[]],
["rohan_tunic_a_wb","Rohan_Tunic",[("L_roh_shirt_M1",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(6)|leg_armor(3)|difficulty(0),imodbits_cloth,[]],
["rohan_tunic_b_wb","Rohan_Tunic",[("L_roh_long_shirt_cape_M4",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,100,weight(2)|head_armor(0)|body_armor(6)|leg_armor(4)|difficulty(0),imodbits_cloth,[]],

["ent_head_helm2","Ent_Head",[("ent_head2",0),],itp_type_head_armor|itp_unique,0,1,weight(250)|head_armor(60)|difficulty(30),0],
["ent_head_helm3","Ent_Head",[("ent_head3",0),],itp_type_head_armor|itp_unique,0,1,weight(250)|head_armor(60)|difficulty(30),0],

#civilian tools
["civilian_hammer","Hammer",[("civilian_hammer_khazad",0)],itp_type_one_handed_wpn|itp_primary,itc_scimitar|itcf_carry_mace_left_hip,300,weight(4.5)|spd_rtng(75)|weapon_length(120)|swing_damage(1,blunt),0],
["civilian_woodaxe_1h","Axe",[("axe_c",0)],itp_type_one_handed_wpn|itp_primary,itc_scimitar|itcf_carry_mace_left_hip,300,weight(4.5)|spd_rtng(75)|weapon_length(100)|swing_damage(1,blunt),0],
["civilian_woodaxe_2h","Heavy_Axe",[("2_handed_axe",0)],itp_type_polearm|itp_no_blur|itp_primary|itp_two_handed,itcf_overswing_polearm|itcf_slashright_twohanded,500,weight(4.5)|spd_rtng(65)|weapon_length(250)|swing_damage(1,cut),0],
["civilian_war_mattock","Mattock",[("civilian_war_mattock",0)],itp_type_polearm|itp_no_blur|itp_primary|itp_two_handed,itc_nodachi|itcf_carry_axe_back,500,weight(4.5)|spd_rtng(60)|weapon_length(250)|swing_damage(1,cut),0],
["civilian_great_mattock","Mattock",[("civilian_great_mattock",0)],itp_type_polearm|itp_no_blur|itp_primary|itp_two_handed,itc_nodachi|itcf_carry_axe_back,500,weight(4.5)|spd_rtng(65)|weapon_length(250)|swing_damage(1,cut),0],
["civilian_adz","Mattock",[("civilian_adz",0)],itp_type_polearm|itp_no_blur|itp_primary|itp_two_handed,itc_nodachi|itcf_slashright_twohanded,500,weight(4.5)|spd_rtng(70)|weapon_length(250)|swing_damage(1,cut),0],
["civilian_pickaxe","Mattock",[("civilian_pickaxe",0)],itp_type_polearm|itp_no_blur|itp_primary|itp_two_handed,itcf_overswing_polearm|itcf_slashright_twohanded|itcf_carry_axe_back,500,weight(4.5)|spd_rtng(65)|weapon_length(180)|swing_damage(1,cut),0],
["civilian_shovel","Shovel",[("civilian_shovel",0)],itp_type_polearm|itp_no_blur|itp_primary|itp_spear,itc_spear_upstab,350,weight(2.25)|spd_rtng(60)|weapon_length(70)|thrust_damage(1,pierce)|swing_damage(1,blunt),0],
["nazgul_robe_wb","Nazgul_robe",[("old_nazgulrobe",0)],itp_type_body_armor|itp_covers_legs|itp_civilian,0,500,weight(3)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0),imodbits_cloth,[]],

["civilian_carry_amphora","Amphora",[("amphora_carry",0)],itp_type_one_handed_wpn|itp_primary,itc_scimitar,300,weight(4.5)|spd_rtng(1000)|weapon_length(1)|swing_damage(1,blunt),0],
["civilian_carry_sack","Sack",[("sack_carry",0)],itp_type_one_handed_wpn|itp_primary,itc_scimitar,300,weight(4.5)|spd_rtng(1000)|weapon_length(1)|swing_damage(1,blunt),0],
["civilian_carry_wood_heap","Fire Wood",[("wood_heap_b_carry",0)],itp_type_one_handed_wpn|itp_primary,itc_scimitar,300,weight(4.5)|spd_rtng(1000)|weapon_length(1)|swing_damage(1,blunt),0],
["civilian_carry_wood","Wood",[("ado_wood_carry",0)],itp_type_one_handed_wpn|itp_primary,itc_scimitar,300,weight(4.5)|spd_rtng(1000)|weapon_length(1)|swing_damage(1,blunt),0],
["civilian_carry_wood2","Wood",[("ado_wood_carry",0)],itp_type_two_handed_wpn|itp_primary,itc_scimitar,300,weight(4.5)|spd_rtng(1000)|weapon_length(1)|swing_damage(1,blunt),0],


#non-ridable animals
["animal_spider","Spider",[("spider",0)], itp_unique|itp_disable_agent_sounds, 0, 1200, hit_points(60)|body_armor(30)|difficulty(3)|horse_speed(50)|horse_maneuver(75)|horse_charge(25),imodbits_none,[]],
["animal_bear","Bear",    [("bear_2",0)],   itp_unique, 0, 1200, hit_points(130)|body_armor(48)|horse_speed(50)|horse_maneuver(48)|horse_charge(25)|horse_scale(120)|difficulty(10),imodbits_none,[]],
["animal_wolf","Wolf",    [("wolf",0)],   itp_unique, 0, 1200, hit_points(50)|body_armor(25)|horse_speed(50)|horse_maneuver(50)|horse_charge(25)|horse_scale(85)|difficulty(10),imodbits_none,[]],
["animal_werewolf","Werewolf",    [("mm_warg_a",0)],   itp_unique, 0, 1200, hit_points(130)|body_armor(35)|horse_speed(60)|horse_maneuver(60)|horse_charge(35)|horse_scale(100)|difficulty(10),imodbits_none,[]],
] or []) + [ 

]
