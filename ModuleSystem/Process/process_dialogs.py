import string
import types

from header_common import *
from module_info import *
from module_triggers import *
from module_dialogs import *

from process_common import *
from process_operations import *

#swy-- always compile this file in M&B 1.011 mode; no matter what (!)
wb_compile_switch = 0

speaker_pos = 0
ipt_token_pos = 1
sentence_conditions_pos = 2
text_pos = 3
opt_token_pos = 4
sentence_consequences_pos = 5
## Warband voiceover stuff
sentence_voice_over_pos = 6


#-------------------------------------------------------

def save_dialog_states(dialog_states):
  file = open(export_dir + "dialog_states.txt","w", encoding='utf-8')
  for dialog_state in dialog_states:
    file.write("%s\n"%dialog_state)
  file.close()


#def compile_variables(cookies_list):
#  for trigger in triggers:
#    for consequence in trigger[trigger_consequences_pos]:
#      compile_statement(consequence,cookies_list)
#  for sentence in sentences:
#    for consequence in sentence[sentence_consequences_pos]:
#      compile_statement(consequence,cookies_list)
#  for trigger in triggers:
#    for condition in trigger[trigger_conditions_pos]:
#      compile_statement(condition,cookies_list)
#  for sentence in sentences:
#    for condition in sentence[sentence_conditions_pos]:
#      compile_statement(condition,cookies_list)
#  return cookies_list

def save_triggers(variable_list,variable_uses,triggers,tag_uses,quick_strings):
  file = open(export_dir + "triggers.txt","w", encoding='utf-8')
  file.write("triggersfile version 1\n")
  file.write("%d\n"%len(triggers))
  for i in range(len(triggers)):
    trigger = triggers[i]
    trigger_id = "trigger " + str(i)
    file.write("%s %s %s "%(sf(trigger[trigger_check_pos]),sf(trigger[trigger_delay_pos]),sf(trigger[trigger_rearm_pos])))
    save_statement_block(file,0,1,trigger[trigger_conditions_pos]  , variable_list, variable_uses,tag_uses,quick_strings,trigger_id)
    save_statement_block(file,0,1,trigger[trigger_consequences_pos], variable_list, variable_uses,tag_uses,quick_strings,trigger_id)
#    for condition in trigger[trigger_conditions_pos]:
#      save_operation(file,condition,variable_list)
#    file.write(" %d "%(len(trigger[trigger_consequences_pos])))
#    for consequence in trigger[trigger_consequences_pos]:
#      save_operation(file,consequence,variable_list)
    file.write("\n")
  file.close()


#=================================================================
def compile_sentence_tokens(sentences):
  input_tokens = []
  output_tokens = []
  dialog_states = ["start","party_encounter","prisoner_liberated","enemy_defeated","party_relieved","event_triggered","close_window","trade","exchange_members", "trade_prisoners","buy_mercenaries","view_char","training","member_chat","prisoner_chat"]
  dialog_state_usages = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  for sentence in sentences:
    output_token_id = -1
    output_token = sentence[opt_token_pos]
    found = 0
    for i_t in range(len(dialog_states)):
      if output_token == dialog_states[i_t]:
        output_token_id = i_t
        found = 1
        break
    if not found:
      dialog_states.append(output_token)
      dialog_state_usages.append(0)
      output_token_id = len(dialog_states) - 1
    output_tokens.append(output_token_id)
  for sentence in sentences:
    input_token_id = -1
    input_token = sentence[ipt_token_pos]
    found = 0
    for i_t in range(len(dialog_states)):
      if input_token == dialog_states[i_t]:
        input_token_id = i_t
        dialog_state_usages[i_t] = dialog_state_usages[i_t] + 1
        found = 1
        break
    if not found:
      print(sentence[ipt_token_pos])
      print(sentence[text_pos])
      print(sentence[opt_token_pos])
      print("**********************************************************************************")
      print("ERROR: INPUT TOKEN NOT FOUND:" + input_token)
      print("**********************************************************************************")
      print("**********************************************************************************")
    input_tokens.append(input_token_id)
  save_dialog_states(dialog_states)
  for i_t in range(len(dialog_states)):
    if dialog_state_usages[i_t] == 0:
      print("ERROR: Output token not found: " + dialog_states[i_t])
  return (input_tokens, output_tokens)

def create_auto_id(sentence,auto_ids):
    text = convert_to_identifier(sentence[text_pos])
    done = 0
    i = 20
    lt = len(text)
    if (i > lt):
      i  = lt
    auto_id = "dlga_" + text[0:i]
    done = 0
    if auto_id in auto_ids and (auto_ids[auto_id] == text):
      done = 1
    while (i <= lt) and not done:
      auto_id = "dlga_" + text[0:i]
      if auto_id in auto_ids:
        if auto_ids[auto_id] == text:
          done = 1
        else:
          i += 1
      else:      
        done = 1
        auto_ids[auto_id] = text
    if not done:
      number = 1
      new_auto_id = auto_id + str(number)
      while new_auto_id in auto_ids:
        number += 1
        new_auto_id = auto_id + str(number)
      auto_id = new_auto_id
      auto_ids[auto_id] = text
    return auto_id
  
def create_auto_id2(sentence,auto_ids):
    text = sentence[text_pos]
    token_ipt = convert_to_identifier(sentence[ipt_token_pos])
    token_opt = convert_to_identifier(sentence[opt_token_pos])
    done = 0
    auto_id = "dlga_" + token_ipt + ":" + token_opt
    done = 0
    if not auto_id in auto_ids:
      done = 1
    else:
      if auto_id in auto_ids and (auto_ids[auto_id] == text):
        done = 1
    if not done:
      number = 1
      new_auto_id = auto_id + "." + str(number)
      while new_auto_id in auto_ids:
        number += 1
        new_auto_id = auto_id + "." + str(number)
      auto_id = new_auto_id
    auto_ids[auto_id] = text
    return auto_id
 
def save_sentences(variable_list,variable_uses,sentences,tag_uses,quick_strings,input_states,output_states):
  file = open(export_dir + "conversation.txt","w", encoding='utf-8')
  file.write("dialogsfile version 1\n")
  file.write("%d\n"%len(sentences))
  # Create an empty dictionary
  auto_ids = {}
  for i in range(len(sentences)):
    sentence = sentences[i]
    try:
      dialog_id = create_auto_id2(sentence,auto_ids)
      file.write("%s %d %d "%(dialog_id,sentence[speaker_pos],input_states[i]))
      save_statement_block(file, 0, 1, sentence[sentence_conditions_pos], variable_list,variable_uses,tag_uses,quick_strings,dialog_id+" condition block")

      file.write("%s "%(remove_exclamation_marker_on_mb1011(replace_spaces(sentence[text_pos]))))
      if (len(sentence[text_pos]) == 0):
        file.write("NO_TEXT ")
      file.write(" %d "%(output_states[i]))
      save_statement_block(file, 0, 1, sentence[sentence_consequences_pos], variable_list,variable_uses,tag_uses,quick_strings,dialog_id+" consequence block")

      #### Warband voiceover addition
      if (wb_compile_switch == 1):	  
        if (len(sentence) > sentence_voice_over_pos):
          file.write("%s "%sentence[sentence_voice_over_pos])
        else:
          file.write("NO_VOICEOVER ")
      #### end Warband voiceover addition
      file.write("\n")
    except Exception as err:
      print("Error in dialog line:", err)
      print(sentence)
  file.close()

# Registered cookies is a list which enables the order of cookies to remain fixed across changes.
# In order to remove cookies not used anymore, edit the cookies_registery.py and remove all entries.

print("exporting triggers...")
variable_uses = []
variables = load_variables(export_dir,variable_uses)
tag_uses = load_tag_uses(export_dir)
quick_strings = load_quick_strings(export_dir)
#compile_variables(variables)
save_triggers(variables,variable_uses,triggers,tag_uses,quick_strings)
print("exporting dialogs...")
(input_states,output_states) = compile_sentence_tokens(dialogs)
save_sentences(variables,variable_uses,dialogs,tag_uses,quick_strings,input_states,output_states)
save_variables(export_dir,variables,variable_uses)
save_tag_uses(export_dir, tag_uses)
save_quick_strings(export_dir,quick_strings)
#print "finished."
