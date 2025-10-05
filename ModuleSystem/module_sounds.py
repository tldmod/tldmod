from header_sounds import *

sounds = [
("click", sf_2d|sf_vol_1,["drum_3.wav"]),
("tutorial_1", sf_2d|sf_vol_7,["tutorial_1.ogg"]),
("tutorial_2", sf_2d|sf_vol_7,["tutorial_2.ogg"]),
("gong", sf_2d|sf_priority_9|sf_vol_7, ["s_cymbals.wav"]),
("quest_taken", sf_2d|sf_priority_9|sf_vol_7, []),
("quest_completed", sf_2d|sf_priority_9|sf_vol_7, ["quest_completed.wav"]),
("quest_succeeded", sf_2d|sf_priority_9|sf_vol_7, ["quest_succeeded.wav"]),
("quest_concluded", sf_2d|sf_priority_9|sf_vol_7, ["quest_concluded.ogg"]),
("quest_failed", sf_2d|sf_priority_9|sf_vol_7, ["quest_failed.wav"]),
("quest_cancelled", sf_2d|sf_priority_9|sf_vol_7, ["quest_cancelled.wav"]),
("rain",sf_2d|sf_priority_10|sf_vol_4|sf_looping, ["rain_1.wav"]),
("money_received",sf_priority_10|sf_vol_6, ["coins_dropped_1.wav"]),
("money_paid",sf_priority_10|sf_vol_10, ["coins_dropped_2.wav"]),
("sword_clash_1", 0,["sword_clank_metal_09.wav","sword_clank_metal_09b.wav","sword_clank_metal_10.wav","sword_clank_metal_10b.wav","sword_clank_metal_12.wav","sword_clank_metal_12b.wav","sword_clank_metal_13.wav","sword_clank_metal_13b.wav"]),
("sword_clash_2", 0,["s_swordClash2.wav"]),
("sword_clash_3", 0,["s_swordClash3.wav"]),
("sword_swing", sf_vol_1|sf_priority_1,["s_swordSwing.wav"]),
("footstep_grass", sf_vol_2|sf_priority_1,["footstep_1.wav","footstep_2.wav","footstep_3.wav","footstep_4.wav"]),
("footstep_wood", sf_vol_3|sf_priority_1,["footstep_wood_1.wav","footstep_wood_2.wav","footstep_wood_4.wav"]),
("footstep_water", sf_vol_3|sf_priority_2,["water_walk_1.wav","water_walk_2.wav","water_walk_3.wav","water_walk_4.wav"]),
("footstep_horse"   ,sf_priority_3, ["s_footstep_horse_2b.wav","s_footstep_horse_3b.wav","s_footstep_horse_4b.wav","s_footstep_horse_5b.wav"]),
("footstep_horse_1b",sf_priority_3, ["s_footstep_horse_3b.wav","s_footstep_horse_4b.wav","s_footstep_horse_5b.wav","s_footstep_horse_5f.wav"]),
("footstep_horse_1f",sf_priority_3, ["s_footstep_horse_2b.wav","s_footstep_horse_2f.wav","s_footstep_horse_3b.wav","s_footstep_horse_3f.wav"]),
("footstep_horse_2b",sf_priority_3, ["s_footstep_horse_2b.wav"]),
("footstep_horse_2f",sf_priority_3, ["s_footstep_horse_2f.wav"]),
("footstep_horse_3b",sf_priority_3, ["s_footstep_horse_3b.wav"]),
("footstep_horse_3f",sf_priority_3, ["s_footstep_horse_3f.wav"]),
("footstep_horse_4b",sf_priority_3, ["s_footstep_horse_4b.wav"]),
("footstep_horse_4f",sf_priority_3, ["s_footstep_horse_4f.wav"]),
("footstep_horse_5b",sf_priority_3, ["s_footstep_horse_5b.wav"]),
("footstep_horse_5f",sf_priority_3, ["s_footstep_horse_5f.wav"]),
("jump_begin", sf_vol_7|sf_priority_9,["jump_begin.wav"]),
("jump_end", sf_vol_3|sf_priority_4,["jump_end.wav"]),
("jump_begin_water", sf_vol_4|sf_priority_9,["jump_begin_water.wav"]),
("jump_end_water", sf_vol_4|sf_priority_9,["jump_end_water.wav"]),
("horse_jump_begin", sf_vol_7|sf_priority_9,["horse_jump_begin.wav"]),
("horse_jump_end", sf_vol_7|sf_priority_9,["horse_jump_end.wav"]),
("horse_jump_begin_water", sf_vol_4|sf_priority_9,["jump_begin_water.wav"]),
("horse_jump_end_water", sf_vol_4|sf_priority_9,["jump_end_water.wav"]),

("release_bow",sf_vol_3|sf_priority_2, ["release_bow_1.wav"]),
("release_crossbow",sf_vol_5, ["wolf_short.wav"]), # to use temporarily to preserve save compartibility
("throw_javelin",sf_vol_3|sf_priority_2, ["throw_javelin_2.wav"]),
("throw_axe",sf_vol_4|sf_priority_2, ["throw_axe_1.wav"]),
("throw_knife",sf_vol_5, ["throw_knife_1.wav"]),
("throw_stone",sf_vol_7, ["throw_stone_1.wav"]),

("reload_crossbow",sf_vol_3, ["pull_bow_1.wav"]), #"reload_crossbow_1.ogg"
("reload_crossbow_continue",sf_vol_5, ["rooster.wav"]), # to use temporarily to preserve save compartibility
("pull_bow",sf_vol_4, ["pull_bow_1.wav"]),
("pull_arrow",sf_vol_5, ["pull_arrow.wav"]),

("arrow_pass_by",0, ["arrow_pass_by_1.wav","arrow_pass_by_2.wav","arrow_pass_by_3.wav","arrow_pass_by_4.wav"]),
("bolt_pass_by",0, ["arrow_pass_by_1.wav"]),#"bolt_pass_by_1.ogg"
("javelin_pass_by",0, ["javelin_pass_by_1.wav","javelin_pass_by_2.wav"]),
("stone_pass_by",sf_vol_9, ["stone_pass_by_1.wav"]),
("axe_pass_by",0, ["axe_pass_by_1.wav","axe_pass_by_2.wav"]),
("knife_pass_by",0, ["knife_pass_by_1.wav"]),
("bullet_pass_by",0, ["arrow_whoosh_1.wav"]),

("incoming_arrow_hit_ground",sf_priority_7|sf_vol_7, ["arrow_hit_ground.wav","arrow_hit_ground_2.wav","arrow_hit_ground_3.wav","incoming_bullet_hit_ground_1.wav"]),
("incoming_bolt_hit_ground",sf_priority_7|sf_vol_7, ["arrow_hit_ground_2.wav","arrow_hit_ground_3.wav","incoming_bullet_hit_ground_1.wav"]),
("incoming_javelin_hit_ground",sf_priority_7|sf_vol_7, ["incoming_javelin_hit_ground_1.wav"]),
("incoming_stone_hit_ground",sf_priority_7|sf_vol_7, ["incoming_stone_hit_ground_1.wav"]),
("incoming_axe_hit_ground",sf_priority_7|sf_vol_7, ["incoming_javelin_hit_ground_1.wav"]),
("incoming_knife_hit_ground",sf_priority_7|sf_vol_7, ["incoming_stone_hit_ground_1.wav"]),
("incoming_bullet_hit_ground",sf_priority_7|sf_vol_7, ["incoming_bullet_hit_ground_1.wav"]),

("outgoing_arrow_hit_ground",sf_vol_2|sf_priority_1, ["outgoing_arrow_hit_ground.wav"]),
("outgoing_bolt_hit_ground",sf_vol_2|sf_priority_1,  ["outgoing_arrow_hit_ground.wav"]),
("outgoing_javelin_hit_ground",sf_vol_3|sf_priority_2, ["outgoing_arrow_hit_ground.wav"]),
("outgoing_stone_hit_ground",sf_vol_3|sf_priority_2, ["incoming_stone_hit_ground_1.wav"]),
("outgoing_axe_hit_ground",sf_vol_3|sf_priority_2, ["incoming_javelin_hit_ground_1.wav"]),
("outgoing_knife_hit_ground",sf_vol_3|sf_priority_2, ["incoming_stone_hit_ground_1.wav"]),
("outgoing_bullet_hit_ground",sf_priority_7|sf_vol_7, ["incoming_bullet_hit_ground_1.wav"]),


("draw_sword",sf_priority_4, ["draw_sword.wav"]),
("put_back_sword",sf_priority_4, ["put_back_sword.wav"]),
("draw_greatsword",sf_priority_4, ["draw_greatsword.wav"]),
("put_back_greatsword",sf_priority_4, ["put_back_sword.wav"]),
("draw_axe",sf_priority_4, ["draw_mace.wav"]),
("put_back_axe",sf_priority_4, ["put_back_to_holster.wav"]),
("draw_greataxe",sf_priority_4, ["draw_greataxe.wav"]),
("put_back_greataxe",sf_priority_4, ["put_back_to_leather.wav"]),
("draw_spear",sf_priority_4, ["draw_spear.wav"]),
("put_back_spear",sf_priority_4, ["put_back_to_leather.wav"]),
("draw_crossbow",sf_priority_4, ["draw_crossbow.wav"]),
("put_back_crossbow",sf_priority_4, ["put_back_to_leather.wav"]),
("draw_revolver",sf_priority_4, ["draw_from_holster.wav"]),
("put_back_revolver",sf_priority_4, ["put_back_to_holster.wav"]),
("draw_dagger",sf_priority_4, ["draw_dagger.wav"]),
("put_back_dagger",sf_priority_4, ["put_back_dagger.wav"]),
("draw_bow",sf_priority_4, ["draw_bow.wav"]),
("put_back_bow",sf_priority_4, ["put_back_to_holster.wav"]),
("draw_shield",sf_priority_4|sf_vol_7, ["draw_shield.wav"]),
("put_back_shield",sf_priority_4|sf_vol_7, ["put_back_shield.wav"]),
("draw_other",sf_priority_4, ["draw_other.wav"]),
("put_back_other",sf_priority_4, ["draw_other2.wav"]),

("body_fall_small",sf_priority_4|sf_vol_7, ["body_fall_small_1.wav","body_fall_small_2.wav"]),
("body_fall_big",sf_priority_4|sf_vol_7, ["body_fall_1.wav","body_fall_2.wav","body_fall_3.wav"]),
("horse_body_fall_begin",sf_priority_6|sf_vol_10, ["horse_body_fall_begin_1.wav"]),
("horse_body_fall_end",sf_priority_6|sf_vol_10, ["horse_body_fall_end_1.wav","body_fall_2.wav","body_fall_3.wav"]),
 
("hit_wood_wood",sf_priority_7|sf_vol_10, ["hit_wood_wood_1.wav","hit_wood_wood_2.wav","hit_wood_wood_3.wav","hit_wood_wood_4.wav","hit_wood_metal_4.wav","hit_wood_metal_5.wav","hit_wood_metal_6.wav"]),#dummy
("hit_metal_metal",sf_priority_7|sf_vol_10, ["hit_metal_metal_3.wav","hit_metal_metal_4.wav",
                                              "hit_metal_metal_5.wav","hit_metal_metal_6.wav","hit_metal_metal_7.wav","hit_metal_metal_8.wav",
                                              "hit_metal_metal_9.wav","hit_metal_metal_10.wav",
                                              "clang_metal_1.wav","clang_metal_2.wav"]),
("hit_wood_metal",sf_priority_7|sf_vol_10, ["hit_metal_metal_1.wav","hit_metal_metal_2.wav","hit_wood_metal_7.wav"]),
("shield_hit_wood_wood",sf_priority_7|sf_vol_10, ["shield_hit_wood_wood_1.wav","shield_hit_wood_wood_2.wav","shield_hit_wood_wood_3.wav"]),
("shield_hit_metal_metal",sf_priority_7|sf_vol_10, ["shield_hit_metal_metal_1.wav","shield_hit_metal_metal_2.wav","shield_hit_metal_metal_3.wav","shield_hit_metal_metal_4.wav"]),
("shield_hit_wood_metal",sf_priority_7|sf_vol_10, ["shield_hit_cut_3.wav","shield_hit_cut_4.wav","shield_hit_cut_5.wav","shield_hit_cut_10.wav"]), #(shield is wood)
("shield_hit_metal_wood",sf_priority_7|sf_vol_10, ["shield_hit_metal_wood_1.wav","shield_hit_metal_wood_2.wav","shield_hit_metal_wood_3.wav"]),#(shield is metal)
("shield_broken",sf_priority_9, ["shield_broken.wav"]),

("hide",0, ["s_hide.wav"]),
("unhide",0, ["s_unhide.wav"]),
("neigh",0, ["silence.wav"]),
("gallop",sf_vol_3, ["horse_gallop_3.wav","horse_gallop_4.wav","horse_gallop_5.wav"]),
("battle",sf_vol_4, ["battle.wav"]), #MV: needed by the engine
("arrow_hit_body",sf_priority_4, ["arrow_hit_body_1.wav","arrow_hit_body_2.wav","arrow_hit_body_3.wav"]),
("metal_hit_low_armor_low_damage",sf_priority_5|sf_vol_9, ["sword_hit_lo_armor_lo_dmg_1.wav","sword_hit_lo_armor_lo_dmg_2.wav","sword_hit_lo_armor_lo_dmg_3.wav"]),
("metal_hit_low_armor_high_damage",sf_priority_5|sf_vol_9, ["sword_hit_lo_armor_hi_dmg_1.wav","sword_hit_lo_armor_hi_dmg_2.wav","sword_hit_lo_armor_hi_dmg_3.wav"]),
("metal_hit_high_armor_low_damage",sf_priority_5|sf_vol_9, ["metal_hit_high_armor_low_damage.wav","metal_hit_high_armor_low_damage_2.wav","metal_hit_high_armor_low_damage_3.wav"]),
("metal_hit_high_armor_high_damage",sf_priority_5|sf_vol_9, ["sword_hit_hi_armor_hi_dmg_1.wav","sword_hit_hi_armor_hi_dmg_2.wav","sword_hit_hi_armor_hi_dmg_3.wav"]),
("wooden_hit_low_armor_low_damage",sf_priority_5|sf_vol_9, ["blunt_hit_low_1.wav","blunt_hit_low_2.wav","blunt_hit_low_3.wav"]),
("wooden_hit_low_armor_high_damage",sf_priority_5|sf_vol_9, ["blunt_hit_high_1.wav","blunt_hit_high_2.wav","blunt_hit_high_3.wav"]),
("wooden_hit_high_armor_low_damage",sf_priority_5|sf_vol_9, ["wooden_hit_high_armor_low_damage_1.wav","wooden_hit_high_armor_low_damage_2.wav"]),
("wooden_hit_high_armor_high_damage",sf_priority_5|sf_vol_9, ["blunt_hit_high_1.wav","blunt_hit_high_2.wav","blunt_hit_high_3.wav"]),
("blunt_hit",sf_priority_5|sf_vol_9, ["punch_1.wav","punch_4.wav","punch_4.wav","punch_5.wav"]),
("player_hit_by_arrow",sf_priority_10|sf_vol_10, ["player_hit_by_arrow.wav"]),
("pistol_shot",sf_priority_10|sf_vol_10, ["fl_pistol.wav"]),

#("encounter_looters",sf_2d|sf_vol_5, ["encounter_river_pirates_5.ogg","encounter_river_pirates_6.ogg","encounter_river_pirates_9.ogg","encounter_river_pirates_10.ogg","encounter_river_pirates_4.ogg"]),
#("encounter_bandits",sf_2d|sf_vol_5, ["encounter_bandit_2.ogg","encounter_bandit_9.ogg","encounter_bandit_12.ogg","encounter_bandit_13.ogg","encounter_bandit_15.ogg","encounter_bandit_16.ogg","encounter_bandit_10.ogg",]),
#("encounter_farmers",sf_2d|sf_vol_5, ["encounter_farmer_2.ogg","encounter_farmer_5.ogg","encounter_farmer_7.ogg","encounter_farmer_9.ogg"]),
("encounter_sea_raiders",sf_2d|sf_vol_5, ["encounter_sea_raider_5.ogg","encounter_sea_raider_9.ogg","encounter_sea_raider_9b.ogg","encounter_sea_raider_10.ogg"]),
("encounter_steppe_bandits",sf_2d|sf_vol_5, ["encounter_steppe_bandit_3.ogg","encounter_steppe_bandit_3b.ogg","encounter_steppe_bandit_8.ogg","encounter_steppe_bandit_10.ogg","encounter_steppe_bandit_12.ogg"]),
#("encounter_nobleman",sf_2d|sf_vol_5, ["encounter_nobleman_1.ogg"]),
#("encounter_vaegirs_ally",sf_2d|sf_vol_5, ["encounter_vaegirs_ally.ogg","encounter_vaegirs_ally_2.ogg"]),
#("encounter_vaegirs_neutral",sf_2d|sf_vol_5, ["encounter_vaegirs_neutral.ogg","encounter_vaegirs_neutral_2.ogg","encounter_vaegirs_neutral_3.ogg","encounter_vaegirs_neutral_4.ogg"]),
#("encounter_vaegirs_enemy",sf_2d|sf_vol_5, ["encounter_vaegirs_neutral.ogg","encounter_vaegirs_neutral_2.ogg","encounter_vaegirs_neutral_3.ogg","encounter_vaegirs_neutral_4.ogg"]),
("sneak_town_halt",sf_2d, ["sneak_halt_1.ogg","sneak_halt_2.ogg"]),
 
("horse_walk"  ,sf_priority_3|sf_vol_9, ["horse_walk_1.wav","horse_walk_2.wav","horse_walk_3.wav","horse_walk_4.wav"]),
("horse_trot"  ,sf_priority_3|sf_vol_4, ["horse_trot_1.wav","horse_trot_2.wav","horse_trot_3.wav","horse_trot_4.wav"]),
("horse_canter",sf_priority_3|sf_vol_6, ["horse_canter_1.wav","horse_canter_2.wav","horse_canter_3.wav","horse_canter_4.wav"]),
("horse_gallop",sf_priority_3|sf_vol_8, ["horse_gallop_6.wav","horse_gallop_7.wav","horse_gallop_8.wav","horse_gallop_9.wav"]),
("horse_breath",sf_priority_3|sf_vol_10,["horse_breath_4.wav","horse_breath_5.wav","horse_breath_6.wav","horse_breath_7.wav"]),
("horse_snort" ,sf_priority_5|sf_vol_7, ["silence.wav"]),
("horse_low_whinny",          sf_vol_9, ["silence.wav"]),
("block_fist",0, ["block_fist_3.wav","block_fist_4.wav"]),
("man_hit_blunt_weak",sf_priority_5|sf_vol_10, ["man_hit_13.wav","man_hit_29.wav","man_hit_32.wav","man_hit_47.wav","man_hit_57.wav"]),
("man_hit_blunt_strong",sf_priority_5|sf_vol_10, ["man_hit_13.wav","man_hit_29.wav","man_hit_32.wav","man_hit_47.wav","man_hit_57.wav"]),
("man_hit_pierce_weak",sf_priority_5|sf_vol_10, ["man_hit_13.wav","man_hit_29.wav","man_hit_32.wav","man_hit_47.wav","man_hit_57.wav"]),
("man_hit_pierce_strong",sf_priority_5|sf_vol_10, ["man_hit_13.wav","man_hit_29.wav","man_hit_32.wav","man_hit_47.wav","man_hit_57.wav"]),
("man_hit_cut_weak",sf_priority_5|sf_vol_10, ["man_hit_13.wav","man_hit_29.wav","man_hit_32.wav","man_hit_47.wav","man_hit_57.wav"]),
("man_hit_cut_strong",sf_priority_5|sf_vol_10, ["man_hit_13.wav","man_hit_29.wav","man_hit_32.wav","man_hit_47.wav","man_hit_57.wav"]),
("man_victory",sf_priority_5|sf_vol_10, ["man_victory_3.wav","man_victory_4.wav","man_victory_5.wav","man_victory_8.wav","man_victory_15.wav","man_victory_49.wav","man_victory_52.wav","man_victory_54.wav","man_victory_57.wav","man_victory_71.wav"]),
("fire_loop",sf_looping|sf_start_at_random_pos, ["CWE_fx_fire_large_01_lp.ogg"]), #"Fire_Torch_Loop3.ogg"
("torch_loop",sf_priority_2|sf_vol_2|sf_looping|sf_start_at_random_pos, ["CWE_fx_fire_embers_02b_lp.ogg"]),
("dummy_hit",sf_priority_9|sf_vol_1, ["shield_hit_cut_3.wav","shield_hit_cut_5.wav"]),
("dummy_destroyed",sf_priority_9, ["shield_broken.wav"]),
#("gourd_destroyed",sf_priority_9, ["shield_broken.wav"]),#TODO
("cow_moo", sf_priority_9|sf_vol_8, ["cow_moo_1.ogg", "silence.wav"]),
#("cow_slaughter", sf_2d|sf_priority_9|sf_vol_8, ["cow_slaughter.ogg"]),
("distant_dog_bark", sf_priority_8|sf_vol_8, ["d_dog1.wav","d_dog2.wav","d_dog3.wav","d_dog7.wav"]),
("donkey", sf_priority_8|sf_vol_5, ["cwe_osiol.ogg", "silence.wav", "silence.wav"]),
#("distant_chicken", sf_priority_8|sf_vol_8, ["d_chicken1.wav","d_chicken2.wav"]),
#from sclavinia mod
("kura",sf_priority_2|sf_vol_4, ["scla_chicken-idle1.wav","scla_chicken-idle2.wav","scla_chicken-idle3.wav","scla_chicken-idle4.wav","scla_chicken-idle5.wav","scla_chicken-idle6.wav","scla_chicken-idle7.wav", "silence.wav", "silence.wav"]),
("pig", sf_priority_4|sf_vol_3, ["scla_cerdo.wav","scla_boar.wav","pk_pig_sound.ogg", "silence.wav"]),
("sheep", sf_priority_4|sf_vol_3, ["sheep_1.wav","sheep_2.wav","sheep_3.wav", "silence.wav"]),
("goat", sf_priority_4|sf_vol_3, ["goat_1.wav","goat_2.wav","goat_3.wav", "silence.wav"]),
# ("distant_blacksmith", sf_2d|sf_priority_8|sf_vol_4, ["d_blacksmith2.wav"]),
# ("arena_ambiance", sf_2d|sf_priority_8|sf_vol_3|sf_looping, ["arena_loop11.ogg"]),
("town_ambiance", sf_2d|sf_priority_8|sf_vol_3|sf_looping, ["town_loop_3.ogg"]),

#TLD start

#tf_male         = 0	# (Dale/Northmen/corsair/bandits)
("man_hit",sf_priority_7|sf_vol_10, ["man_hit_5.wav","man_hit_6.wav","man_hit_7.wav","man_hit_8.wav","man_hit_9.wav","man_hit_10.wav","man_hit_11.wav","man_hit_12.wav","man_hit_13.wav","man_hit_14.wav","man_hit_15.wav",
                                      "man_hit_17.wav","man_hit_18.wav","man_hit_19.wav","man_hit_22.wav","man_hit_29.wav","man_hit_32.wav","man_hit_47.wav","man_hit_57.wav","man_hit_59.wav"]),
("man_die",sf_priority_10,  ["man_death_1.wav","man_death_8.wav","man_death_8b.wav","man_death_11.wav","man_death_14.wav","man_death_16.wav","man_death_18.wav","man_death_21.wav","man_death_29.wav","man_death_40.wav","man_death_44.wav","man_death_46.wav","man_death_48.wav","man_death_64.wav"]),# ["man_fall_1.wav","man_fall_2.wav","man_fall_3.wav","man_fall_4.wav"]),
("man_grunt",sf_priority_6|sf_vol_2, ["man_excercise_1.wav","man_excercise_2.wav","man_excercise_4.wav"]),
("man_breath_hard",sf_priority_3|sf_vol_8, ["man_ugh_1.wav","man_ugh_2.wav","man_ugh_4.wav","man_ugh_7.wav","man_ugh_12.wav","man_ugh_13.wav","man_ugh_17.wav"]),
("man_grunt_long",sf_priority_5|sf_vol_4, ["man_grunt_1.wav","man_grunt_2.wav","man_grunt_3.wav","man_grunt_5.wav","man_grunt_13.wav","man_grunt_14.wav"]),
("man_yell",sf_priority_6|sf_vol_8, ["man_yell_4.wav","man_yell_4_2.wav","man_yell_7.wav","man_yell_9.wav","man_yell_11.wav","man_yell_13.wav","man_yell_15.wav","man_yell_16.wav","man_yell_17.wav","man_yell_20.wav","man_shortyell_4.wav","man_shortyell_5.wav","man_shortyell_6.wav","man_shortyell_9.wav","man_shortyell_11.wav","man_shortyell_11b.wav",
                        "man_yell_b_18.wav","man_yell_22.wav","man_yell_b_21.wav","man_yell_b_22.wav","man_yell_b_23.wav","man_yell_c_20.wav"]),
#TODONOW:
("man_warcry",sf_priority_6, ["man_insult_2.wav","man_insult_3.wav","man_insult_7.wav","man_insult_9.wav","man_insult_13.wav","man_insult_15.wav","man_insult_16.wav"]),

#tf_female       = 1	# all factions
("woman_hit",sf_priority_7, ["woman_hit_2.wav","woman_hit_3.wav",
						  "woman_hit_b_2.wav","woman_hit_b_4.wav","woman_hit_b_6.wav","woman_hit_b_7.wav","woman_hit_b_8.wav",
						  "woman_hit_b_11.wav","woman_hit_b_14.wav","woman_hit_b_16.wav"]),
("woman_die",sf_priority_10, ["woman_fall_1.wav","woman_hit_b_5.wav"]),
#tf_gondor		= 2
("gondor_yell",          sf_priority_6|sf_vol_8, ["gondor_yell_1.wav","gondor_yell_2.wav","gondor_yell_3.wav","gondor_yell_4.wav","gondor_yell_5.wav","gondor_yell_6.wav","man_yell_4.wav","man_yell_4_2.wav","man_yell_7.wav","man_yell_9.wav","man_yell_11.wav","man_yell_13.wav","man_yell_15.wav","man_yell_16.wav","man_yell_17.wav","man_yell_20.wav","man_shortyell_4.wav","man_shortyell_5.wav","man_shortyell_6.wav","man_shortyell_9.wav","man_shortyell_11.wav","man_shortyell_11b.wav",]),
("gondor_victory",       sf_priority_5|sf_vol_10, ["man_victory_3.wav","man_victory_4.wav","man_victory_5.wav","man_victory_8.wav","gondor_victory_1.wav","gondor_victory_2.wav","gondor_victory_3.wav","gondor_victory_4.wav","gondor_victory_5.wav","gondor_victory_6.wav"]),
("gondor_victory_player",sf_priority_5|sf_vol_10, ["gondor_victory_1.wav","gondor_victory_2.wav"]), # for the player, must sound like the same person
#tf_rohan		= 3
("rohan_yell",sf_priority_6|sf_vol_8, ["rohan_yell_1.wav","rohan_yell_2.wav","rohan_yell_3.wav","rohan_yell_4.wav","rohan_yell_5.wav","rohan_yell_6.wav","rohan_yell_7.wav","rohan_yell_8.wav","rohan_yell_9.wav","rohan_yell_10.wav","rohan_yell_11.wav","rohan_yell_12.wav","rohan_yell_13.wav","rohan_yell_14.wav","man_yell_4.wav","man_yell_4_2.wav","man_yell_7.wav","man_yell_9.wav","man_yell_11.wav","man_yell_13.wav","man_yell_15.wav","man_yell_16.wav","man_yell_17.wav","man_yell_20.wav","man_shortyell_4.wav","man_shortyell_5.wav","man_shortyell_6.wav","man_shortyell_9.wav","man_shortyell_11.wav","man_shortyell_11b.wav"]),
("rohan_victory",sf_priority_5|sf_vol_10, ["man_victory_3.wav","man_victory_4.wav","man_victory_5.wav","man_victory_8.wav","rohan_victory_1.wav","rohan_victory_2.wav","rohan_victory_3.wav","rohan_victory_4.wav"]),
#tf_dunland	= 4
("dunlender_yell",sf_priority_6|sf_vol_8, ["dun_yell_1.wav","dun_yell_2.wav","dun_yell_3.wav","dun_yell_4.wav","dun_yell_5.wav","dun_yell_6.wav","dun_yell_7.wav","dun_yell_8.wav","dun_yell_9.wav","dun_yell_10.wav","dun_yell_11.wav","dun_yell_12.wav","dun_yell_13.wav","dun_yell_14.wav","dun_yell_15.wav","dun_yell_16.wav","dun_yell_17.wav","dun_yell_18.wav","dun_yell_19.wav","dun_yell_20.wav","dun_yell_21.wav","dun_yell_22.wav","dun_yell_23.wav","dun_yell_24.wav"]),
("dunlender_victory",sf_priority_5|sf_vol_10, ["dun_victory_1.wav","dun_victory_2.wav","dun_victory_3.wav","dun_victory_4.wav","dun_victory_5.wav","dun_victory_6.wav","dun_victory_7.wav","dun_victory_8.wav","dun_victory_9.wav"]),
#tf_orc = 5 #(orcs, goblins)
("orc_die",sf_priority_10,  ["orc_death_1.wav","orc_death_2.wav","orc_death_3.wav","orc_death_4.wav","orc_death_5.wav","orc_death_6.wav","orc_death_7.wav","orc_death_8.wav"]),
("orc_hit",sf_priority_7|sf_vol_10, ["orc_hit_1.wav","orc_hit_2.wav","orc_hit_3.wav","orc_hit_4.wav","orc_hit_6.wav","orc_hit_7.wav","orc_hit_9.wav","orc_hit_10.wav"]),
("orc_grunt",sf_priority_6|sf_vol_2, ["orc_grunt_1.wav"]), 
("orc_grunt_long",sf_priority_5|sf_vol_4, ["orc_grunt_long_1.wav"]), 
("orc_yell",sf_priority_6|sf_vol_8, ["orc_yell_1.wav","orc_yell_2.wav"]), 
("orc_victory",sf_priority_5|sf_vol_10, ["orc_victory_1.wav","orc_victory_2.wav","orc_victory_3.wav","orc_victory_4.wav","orc_victory_5.wav","orc_victory_6.wav"]), 
#tf_uruk = 6 #(Uruks, Uruk Hai)
("uruk_die",sf_priority_10,  ["uruk_death_01.wav","uruk_death_02.wav","uruk_death_03.wav","uruk_death_04.wav","uruk_death_05.wav","uruk_death_06.wav"]),
("uruk_hit",sf_priority_7|sf_vol_10, ["uruk_hit_01.wav","uruk_hit_02.wav","uruk_hit_03.wav","uruk_hit_04.wav","uruk_hit_05.wav","uruk_hit_06.wav","uruk_hit_07.wav","uruk_hit_08.wav","uruk_hit_09.wav"]),
("uruk_grunt",sf_priority_6|sf_vol_2, ["orc_grunt_1.wav"]), 
("uruk_grunt_long",sf_priority_5|sf_vol_4, ["uruk_shortyell_01.wav","uruk_shortyell_02.wav","uruk_shortyell_03.wav","uruk_shortyell_04.wav","uruk_shortyell_05.wav","uruk_shortyell_06.wav","uruk_shortyell_07.wav",]), 
("uruk_yell",sf_priority_6|sf_vol_8, ["uruk_yell_01.wav","uruk_yell_02.wav","uruk_yell_03.wav","uruk_yell_04.wav","uruk_yell_05.wav","uruk_yell_06.wav","uruk_yell_07.wav","uruk_yell_08.wav","uruk_yell_09.wav","uruk_yell_10.wav","uruk_yell_11.wav","uruk_yell_12.wav"]), 
("uruk_victory",sf_priority_5|sf_vol_10, ["uruk_victory_01.wav","uruk_victory_02.wav","uruk_victory_03.wav","uruk_victory_04.wav","uruk_victory_05.wav","uruk_victory_06.wav","uruk_victory_07.wav","uruk_victory_08.wav","uruk_victory_09.wav","uruk_victory_10.wav","uruk_victory_11.wav","uruk_victory_12.wav","uruk_victory_13.wav","uruk_victory_14.wav","uruk_victory_15.wav","uruk_victory_16.wav","uruk_victory_17.wav"]), 
#tf_harad = 7
("haradrim_yell",sf_priority_6|sf_vol_8, ["har_yell_1.wav","har_yell_2.wav","har_yell_3.wav","har_yell_4.wav","har_yell_5.wav","har_yell_6.wav","har_yell_7.wav","har_yell_8.wav","har_yell_9.wav","har_yell_10.wav"]),
("haradrim_victory",sf_priority_5|sf_vol_10, ["haradrim_victory_1.wav","haradrim_victory_2.wav","haradrim_victory_3.wav","haradrim_victory_4.wav","haradrim_victory_5.wav"]),
("haradrim_die",sf_priority_10,  ["wilhelm.wav","man_death_8.wav","man_death_8b.wav","man_death_11.wav","man_death_14.wav","man_death_16.wav","man_death_18.wav","man_death_21.wav","man_death_29.wav","man_death_40.wav","man_death_44.wav","man_death_46.wav","man_death_48.wav","man_death_64.wav"]),# ["man_fall_1.wav","man_fall_2.wav","man_fall_3.wav","man_fall_4.wav"]),
#tf_easterling	= 8 #(Rhun/khand)
#tf_dwarf = 9
("dwarf_yell",sf_priority_6|sf_vol_8, ["dwarf1.wav","dwarf10.wav","dwarf11.wav","dwarf12.wav","dwarf2.wav","dwarf4.wav","dwarf5.wav","dwarf7.wav","dwarf9.wav","dwarf_01.wav","dwarf_02.wav","dwarf_04.wav","dwarf_05.wav","dwarf_06.wav","dwarf_07.wav",
                        "dwarf_09.wav","man_shortyell_6.wav","man_shortyell_5.wav","man_shortyell_4.wav","man_yell_b_23.wav","man_yell_16.wav","man_yell_4_2.wav","man_yell_13.wav"]),
("dwarf_victory",sf_priority_5|sf_vol_10, ["silence.wav","silence.wav","silence.wav","dwarf8.wav","man_victory_54.wav","man_victory_57.wav","man_victory_71.wav"]),
#tf_troll = 10
("troll_die",sf_priority_10,  ["troll_death_1.wav"]),
("troll_hit",sf_priority_7|sf_vol_10, ["troll_hit_1.wav","troll_hit_1.wav","troll_grunt_2.wav"]), 
("troll_grunt",sf_priority_6|sf_vol_4, ["troll_grunt_1.wav","troll_grunt_2.wav", "troll_growl.wav", "troll_roar.wav"]), 
("troll_grunt_long",sf_priority_5|sf_vol_8, ["troll_grunt_2.wav","troll_hit_2.wav","troll_roar.wav"]), 
("troll_yell",sf_priority_6|sf_vol_8, ["troll_grunt_2.wav","troll_hit_2.wav","troll_roar.wav"]), 
("troll_victory",sf_priority_5|sf_vol_10, ["troll_grunt_2.wav","troll_hit_2.wav","troll_death_1.wav","troll_roar.wav"]), 
#troll_grunt_long = grunt, yell = grunt, 
#tf_dunedain = 11
("dunedain_yell",sf_priority_6|sf_vol_8, ["dunedain_yell_1.wav","dunedain_yell_2.wav","dunedain_yell_3.wav","dunedain_yell_4.wav","dunedain_yell_5.wav","dunedain_yell_6.wav","dunedain_yell_7.wav","dunedain_yell_8.wav","dunedain_yell_9.wav","dunedain_yell_10.wav","man_yell_4.wav","man_yell_4_2.wav","man_yell_7.wav","man_yell_9.wav","man_yell_11.wav","man_yell_13.wav","man_yell_15.wav","man_yell_16.wav","man_yell_17.wav","man_yell_20.wav","man_shortyell_4.wav","man_shortyell_5.wav","man_shortyell_6.wav","man_shortyell_9.wav","man_shortyell_11.wav","man_shortyell_11b.wav"]),
("dunedain_victory",sf_priority_5|sf_vol_10, ["man_victory_71.wav","man_victory_3.wav","man_victory_4.wav","man_victory_5.wav","man_victory_8.wav","dunedain_victory_1.wav","dunedain_victory_2.wav","dunedain_victory_3.wav"]),
("dunedain_victory_player",sf_priority_5|sf_vol_10, ["dunedain_victory_1.wav",]),
#tf_lorien = 12
("lothlorien_yell",sf_priority_6|sf_vol_8, ["man_ugh_17.wav","elf_lothlorien_yell_1.wav","elf_lothlorien_yell_2.wav","elf_lothlorien_yell_3.wav","elf_basic_yell_1.wav","elf_basic_yell_2.wav","elf_basic_yell_3.wav","elf_basic_yell_4.wav","elf_basic_yell_5.wav","elf_basic_yell_6.wav","elf_basic_yell_7.wav","elf_basic_yell_8.wav","elf_basic_yell_9.wav","elf_basic_yell_10.wav"]),
("lothlorien_victory",sf_priority_5|sf_vol_10, ["man_victory_15.wav","elf_basic_yell_1.wav","elf_basic_victory_1.wav","elf_basic_victory_2.wav","elf_basic_victory_3.wav","elf_basic_victory_4.wav","elf_basic_victory_5.wav"]),  
#tf_imladris = 13
("rivendell_yell",sf_priority_6|sf_vol_8, ["man_ugh_17.wav","elf_rivendell_yell_1.wav","elf_rivendell_yell_2.wav","elf_basic_yell_1.wav","elf_basic_yell_2.wav","elf_basic_yell_3.wav","elf_basic_yell_4.wav","elf_basic_yell_5.wav","elf_basic_yell_6.wav","elf_basic_yell_7.wav","elf_basic_yell_8.wav","elf_basic_yell_9.wav","elf_basic_yell_10.wav"]),
("rivendell_victory",sf_priority_5|sf_vol_10, ["man_victory_15.wav","elf_basic_yell_1.wav","elf_basic_victory_1.wav","elf_basic_victory_2.wav","elf_basic_victory_3.wav","elf_basic_victory_4.wav","elf_basic_victory_5.wav"]),  
#tf_woodelf = 14
("mirkwood_yell",sf_priority_6|sf_vol_8, ["man_ugh_17.wav","elf_mirkwood_yell_1.wav","elf_mirkwood_yell_2.wav","elf_basic_yell_1.wav","elf_basic_yell_2.wav","elf_basic_yell_3.wav","elf_basic_yell_4.wav","elf_basic_yell_5.wav","elf_basic_yell_6.wav","elf_basic_yell_7.wav","elf_basic_yell_8.wav","elf_basic_yell_9.wav","elf_basic_yell_10.wav"]),
("mirkwood_victory",sf_priority_5|sf_vol_10, ["man_victory_15.wav","elf_basic_yell_1.wav","elf_basic_victory_1.wav","elf_basic_victory_2.wav","elf_basic_victory_3.wav","elf_basic_victory_4.wav","elf_basic_victory_5.wav"]),  
("mirkwood_victory_player",sf_priority_5|sf_vol_10, ["elf_basic_victory_1.wav","elf_basic_victory_2.wav",]),  
#tf_evil_male = 15

("big_weapon_swing", sf_vol_10|sf_priority_7,["s_big_weaponSwing.wav"]),

("thunder",sf_2d|sf_vol_15, ["thunder.wav"]),
("pull_ballista",sf_vol_8, ["pull_bow_1.ogg"]),
("evil_orders",  sf_vol_3, ["order_form_ranks_(orc).wav"]),
("evil_horn",   sf_vol_10, ["horn_isengard.wav"]),

("nazgul_skreech_long", sf_priority_15|sf_2d|sf_vol_15, ["nazgul_02.wav"]),
("nazgul_skreech_short",sf_priority_15|sf_2d|sf_vol_15, ["nazgul_01.wav"]),

("horror_scream_man"  ,sf_priority_10|sf_vol_10,["horror_scream_man_0.wav","horror_scream_man_1.wav","horror_scream_man_2.wav","horror_scream_man_3.wav","horror_scream_man_4.wav"]),
("horror_scream_woman",sf_priority_10|sf_vol_10,["horror_scream_woman.wav"]),
("horror_scream_orc"  ,sf_priority_10|sf_vol_10,["horror_scream_orc.wav"]),

("warg_lone_woof",   sf_priority_3|sf_vol_5, ["warg_bark01.wav","warg_bark02.wav","warg_bark03.wav","warg_growl01.wav","warg_howl01.wav","warg_howl02.wav","warg_howl03.wav"]),
("horse_snort_again",sf_priority_3|sf_vol_4,  ["horse_snort_1.wav","horse_snort_2.wav","horse_snort_3.wav","horse_snort_4.wav","horse_snort_5.wav"]),

("spear_trap",sf_priority_7|sf_vol_9, ["spear_trap.wav"]),
 
("elf_song"   ,sf_priority_8|sf_vol_7,["elf_elfsong.wav"]), 

("moria_ambiance"           ,sf_priority_8|sf_vol_5|sf_start_at_random_pos|sf_looping, ["moria_loop.wav"]),
("henneth_ambiance"         ,sf_priority_8|sf_vol_3|sf_start_at_random_pos|sf_looping, ["henneth_loop.wav"]),
("goodforest_ambiance"      ,sf_priority_8|sf_vol_3|sf_start_at_random_pos|sf_looping, ["good_forest_loop.wav"]),
("evilforest_ambiance"      ,sf_priority_8|sf_vol_3|sf_start_at_random_pos|sf_looping, ["evil_forest_loop.wav"]),
("water_waves_ambiance"     ,sf_priority_8|sf_vol_3|sf_start_at_random_pos|sf_looping, ["water_waves_loop.wav"]),
("water_splash_ambiance"    ,sf_priority_8|sf_vol_3|sf_start_at_random_pos|sf_looping, ["water_splash_loop.wav"]),
("water_wavesplash_ambiance",sf_priority_8|sf_vol_3|sf_start_at_random_pos|sf_looping, ["water_wavesplash_loop.wav"]),
("wind_ambiance"            ,sf_priority_8|sf_vol_6|sf_start_at_random_pos|sf_looping, ["wind_loop.wav"]),
("isengard_ambiance"        ,sf_priority_8|sf_vol_3|sf_start_at_random_pos|sf_looping, ["isen_loop.wav"]),
("evilmen_ambiance"         ,sf_priority_8|sf_vol_4|sf_start_at_random_pos|sf_looping, ["evil_men_loop.wav"]),
("orcs_ambiance"            ,sf_priority_8|sf_vol_3|sf_start_at_random_pos|sf_looping, ["beast_loop.wav"]),
("morgul_ambiance"          ,sf_priority_8|sf_vol_4|sf_start_at_random_pos|sf_looping, ["morgul_loop.wav"]),
("gondor_ambiance"          ,sf_priority_8|sf_vol_4|sf_start_at_random_pos|sf_looping, ["gondor_people_loop.wav"]),
("rohan_ambiance"           ,sf_priority_8|sf_vol_4|sf_start_at_random_pos|sf_looping, ["rohan_people_loop.wav"]),
("dwarf_ambiance"           ,sf_priority_8|sf_vol_4|sf_start_at_random_pos|sf_looping, ["dwarf_men_loop.wav"]),
("harad_ambiance"           ,sf_priority_8|sf_vol_4|sf_start_at_random_pos|sf_looping, ["harad_loop.wav"]),
("deadmarshes_ambiance"     ,sf_priority_8|sf_vol_4|sf_start_at_random_pos|sf_looping, ["evil_flies_loop.wav"]),
("night_ambiance"           ,sf_priority_8|sf_vol_3|sf_start_at_random_pos|sf_looping, ["night_loop.wav"]),
("neutralforest_ambiance"   ,sf_priority_8|sf_vol_3|sf_start_at_random_pos|sf_looping, ["neutral_forest_loop.wav"]),
("fangorn_ambiance"         ,sf_priority_8|sf_vol_3|sf_start_at_random_pos|sf_looping, ["fangorn_loop.wav"]),

("gondor_occasional",    sf_priority_8|sf_vol_4,["silence.wav","silence.wav","good_eagle01.wav","d_blacksmith2.wav","good_workshop.wav","d_dog7.wav"]),
("elves_occasional",     sf_priority_8|sf_vol_4,["silence.wav","silence.wav","good_bird01.wav","good_bird02.wav","good_bird03.wav","good_bird_wings.wav"]), 
("lorien_occasional",    sf_priority_8|sf_vol_4,["elf_elfsong.wav", "good_bird01.wav","good_bird02.wav","good_bird03.wav","good_bird_wings.wav"]), 
("beorn_occasional",     sf_priority_8|sf_vol_4,["good_bird01.wav","good_bird02.wav","good_bird03.wav","good_workshop.wav","d_saw_short3.wav","d_dog7.wav","d_carpenter1.wav"]), 
("rohan_occasional",     sf_priority_8|sf_vol_4,["rohan01.wav", "rohan02.wav","rohan03.wav","rohan04.wav","good_workshop.wav", "good_eagle01.wav","good_bird01.wav","d_blacksmith2.wav","d_dog7.wav","d_chicken1.wav"]),
("dwarf_occasional",     sf_priority_8|sf_vol_4,["dwarves01.wav", "dwarves02.wav","d_blacksmith2.wav","osgiliath05.wav","osgiliath02.wav"]),
("dale_occasional",      sf_priority_8|sf_vol_4,["silence.wav","silence.wav","good_bird01.wav","good_bird02.wav","good_bird03.wav","good_workshop.wav","good_workshop.wav","d_saw_short3.wav", "d_blacksmith2.wav","d_dog7.wav","dale_bell_1.wav","dale_bell_1_2_combined.wav", "dale_bell_2.wav", "dale_bell_3.wav"]),
("rhun_occasional",      sf_priority_8|sf_vol_4,["rohan01.wav", "rohan02.wav","rohan03.wav","rohan04.wav","evil_crow.wav", "d_saw_short3.wav","d_blacksmith2.wav","d_dog7.wav"]),
("harad_occasional",     sf_priority_8|sf_vol_4,["silence.wav","rohan02.wav","rohan03.wav","rohan04.wav","evil_crow.wav","harad01.wav","harad02.wav","harad03.wav","harad01.wav","harad02.wav","harad03.wav"]),
("umbar_occasional",     sf_priority_8|sf_vol_4,["silence.wav","silence.wav","silence.wav","sea_seagulls.wav", "sea_seaside.wav"]),
("dunland_occasional",   sf_priority_8|sf_vol_4,["silence.wav","evil_crow.wav", "good_eagle01.wav","d_dog1.wav","d_dog2.wav","d_dog3.wav","d_dog7.wav","d_carpenter1.wav"]),
("orc_occasional",       sf_priority_8|sf_vol_4,["silence.wav","evil_crow.wav", "orc_warg.wav","orc_beast01.wav","orc_beast02.wav","orc_beast03.wav"]),
("guldur_occasional",    sf_priority_8|sf_vol_4,["silence.wav","silence.wav","silence.wav","silence.wav","evil_crow.wav","orc_beast01.wav","orc_beast02.wav","orc_beast03.wav"]),
("moria_occasional",     sf_priority_8|sf_vol_8,["silence.wav","silence.wav","silence.wav","moria01.wav","moria02.wav"]),
("isengard_occasional",  sf_priority_8|sf_vol_4,["silence.wav","silence.wav","moria02.wav", "evil_crow.wav","orc_beast01.wav","orc_beast02.wav","orc_beast03.wav", "d_saw_short3.wav","orc_warg.wav","d_blacksmith2.wav","dwarves01.wav","dwarves02.wav","osgiliath04.wav","d_carpenter1.wav"]),
("urukhai_occasional",   sf_priority_8|sf_vol_4,["evil_crow.wav","orc_beast01.wav","orc_beast02.wav","orc_beast03.wav", "orc_warg.wav","d_carpenter1.wav"]),
("seaside_occasional",   sf_priority_8|sf_vol_4,["good_bird01.wav","good_bird02.wav","good_bird03.wav","sea_seagulls.wav", "sea_seaside.wav", "d_blacksmith2.wav"]),
("morgul_occasional",    sf_priority_8|sf_vol_4,["silence.wav","silence.wav","silence.wav","silence.wav","silence.wav","silence.wav","silence.wav","morgul01.wav","morgul02.wav"]),
("eosgi_occasional",     sf_priority_8|sf_vol_4,["orc_beast01.wav","orc_beast02.wav","orc_beast03.wav","osgiliath01.wav","osgiliath02.wav","osgiliath03.wav","osgiliath04.wav","osgiliath05.wav"]),
("wosgi_occasional",     sf_priority_8|sf_vol_4,["silence.wav","silence.wav","osgiliath01.wav","osgiliath02.wav","osgiliath03.wav","osgiliath04.wav","osgiliath05.wav"]),
("tirith_occasional",    sf_priority_8|sf_vol_4,["silence.wav","good_eagle01.wav","d_blacksmith2.wav","silence.wav","silence.wav","dale_bell_1.wav","dale_bell_1_2_combined.wav", "dale_bell_2.wav", "dale_bell_3.wav"]),
("morannon_occasional",  sf_priority_8|sf_vol_4,["silence.wav"]),
("tirith_top_occasional",sf_priority_8|sf_vol_4,["silence.wav","good_eagle01.wav","silence.wav","silence.wav","silence.wav","silence.wav"]),

#yelling in a dialog window
("meeting_elf", sf_priority_2|sf_vol_4, ["elf_rivendell_yell_1.wav","elf_rivendell_yell_2.wav","elf_basic_yell_1.wav","elf_basic_yell_2.wav","elf_basic_yell_3.wav","elf_basic_yell_4.wav","elf_basic_yell_5.wav","elf_basic_yell_6.wav","elf_basic_yell_7.wav","elf_basic_yell_8.wav","elf_basic_yell_9.wav","elf_basic_yell_10.wav"]),
("meeting_uruk",sf_priority_2|sf_vol_4, ["uruk_shortyell_01.wav","uruk_shortyell_02.wav","uruk_shortyell_03.wav","uruk_shortyell_04.wav","uruk_shortyell_05.wav", "uruk_shortyell_06.wav", "uruk_shortyell_07.wav",]),
("meeting_man", sf_priority_2|sf_vol_4, ["man_shortyell_6.wav","man_shortyell_5.wav","man_shortyell_4.wav","man_yell_b_23.wav","man_yell_16.wav","man_yell_4_2.wav","man_yell_13.wav"]),
("meeting_orc", sf_priority_2|sf_vol_4, ["orc_grunt_1.wav", "orc_grunt_long_1.wav", "orc_yell_1.wav","orc_yell_2.wav"]),
#doubles for muted hardcoded sounds
("neigh1",                     sf_vol_2, ["horse_exterior_whinny_01.wav","horse_exterior_whinny_02.wav","horse_exterior_whinny_03.wav","horse_exterior_whinny_04.wav","horse_exterior_whinny_05.wav","horse_whinny.wav"]),
("horse_snort1" ,sf_priority_3|sf_vol_2, ["horse_snort_1.wav","horse_snort_2.wav","horse_snort_3.wav","horse_snort_4.wav","horse_snort_5.wav"]),
("horse_low_whinny1",          sf_vol_4, ["horse_whinny-1.wav","horse_whinny-2.wav"]),
("mount_death",                sf_vol_4, ["horse_snort_4.wav","horse_snort_5.wav"]),

("waterfall" ,sf_priority_15|sf_vol_3|sf_looping|sf_start_at_random_pos, ["CWE_amb_waterfall_medium_01_2d_lp.ogg"]),
("orc_cheer", sf_priority_5|sf_vol_10,                                  ["orc_yell_1.wav","orc_yell_2.wav","orc_grunt_long_1.wav", "orc_victory_1.wav","orc_victory_2.wav","orc_victory_3.wav","orc_victory_4.wav","orc_victory_5.wav","orc_victory_6.wav"]), 
# directional sounds for props
("water_wavesplash_source",sf_priority_9|sf_vol_6|sf_looping|sf_start_at_random_pos, ["water_wavesplash_loop.wav"]),
("water_waves_source"     ,sf_priority_9|sf_vol_15|sf_looping|sf_start_at_random_pos, ["water_waves_loop.wav"]), #very loud, so use sparingly
("water_splash_source"    ,sf_priority_9|sf_vol_15|sf_looping|sf_start_at_random_pos, ["water_splash_loop.ogg"]),
#("fire_loop"             ,sf_priority_9|sf_vol_4|sf_looping|sf_start_at_random_pos, ["Fire_Torch_Loop3.wav"]), #"Fire_Torch_Loop3.ogg"
#("torch_loop"            ,sf_priority_9|sf_vol_4|sf_looping|sf_start_at_random_pos, ["Fire_Torch_Loop3.wav"]),

("lord_dies",       sf_2d|sf_priority_9|sf_vol_7, ["lord_dies.wav"]),
("enemy_lord_dies", sf_2d|sf_priority_9|sf_vol_7, ["enemy_lord_dies.wav"]),
("level_up",        sf_2d|sf_priority_9|sf_vol_7, ["level_up.wav"]),

("spider",     0, ["spider_battle01.wav", "spider_battle2.wav"]),
("spider_die", sf_priority_6|sf_vol_10, ["spider_death.wav"]),

#swy-- new sounds for rank promotion made by Merlkir
("new_rank_evil", sf_2d|sf_vol_7, ["new_rank_evil.wav"]),
("new_rank_good", sf_2d|sf_vol_7, ["new_rank_good.wav"]),

("woman_yell",sf_priority_2|sf_vol_10, ["woman_yell_1.ogg", "woman_yell_2.ogg"]),  

("ghost_ambient_long"         ,sf_2d|sf_priority_15|sf_vol_1|sf_looping, ["ghost_ambient_long02.wav"]),

("bear_strike",   sf_priority_6|sf_vol_10, ["warg_howl02.wav", "warg_howl03.wav", "troll_growl.wav",]),
("spider_strike", sf_priority_6|sf_vol_10, ["spider_battle01.wav", "trollSnarl.wav",]),
("wolf_strike",   sf_priority_6|sf_vol_10, ["warg_growl01.wav", "trollSnarl.wav",]),

("bees_people_ambiance"   	,sf_2d|sf_priority_8|sf_vol_4|sf_looping, ["bees_people.wav"]),
("bees_birds_ambiance"      ,sf_2d|sf_priority_8|sf_vol_5|sf_looping, ["bees_birds.wav"]),

#doubles for muted hardcoded sounds
("camel_sounds", 0,                      ["camelGargle.wav", "camelGroan01.wav", "camelGroan02.wav", "camelRoar01.wav"]),
("camel_death" ,sf_priority_5|sf_vol_7, ["camelDeath01.wav", "camelDeath02.wav", "camelDeath03.wav"]),

("army_good" ,sf_priority_5|sf_vol_9, ["gondor_army.wav"]),
("bell" ,sf_priority_5|sf_vol_7, ["dale_bell_1.wav","dale_bell_1_2_combined.wav", "dale_bell_2.wav", "dale_bell_3.wav"]),
("raven" ,sf_priority_5|sf_vol_7, ["evil_crow.wav"]),
]
