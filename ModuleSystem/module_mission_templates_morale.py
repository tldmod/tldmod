from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *

tld_morale_triggers = [
     (0, 0, 2, [(key_clicked, key_t),(eq, "$tld_option_morale", 1)], [
(call_script, "script_coherence"),    
(call_script, "script_healthbars"),       
         ]),
      
(1, 0, ti_once, [(eq, "$tld_option_morale", 1)], [
(call_script, "script_coherence"),    
         ]),						
      
(15, 0, 10, [(eq, "$tld_option_morale", 1)], [
(call_script, "script_coherence"),    
(call_script, "script_morale_check"),    
         ]),
(5, 0, 3, [(eq, "$tld_option_morale", 1)], [
(call_script, "script_coherence"),    
(call_script, "script_rout_check"),       
         ]),]