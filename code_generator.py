from generator_sup import *

def code_gen(token, action):
    return {
        "numeric_label": numeric_label,
        "start_break": start_break,
        "end_break": end_break,
        "until": until,
        "break_func": break_func,
        "pid": pid,
        "pnum": pnum, 
        "start_scope": start_scope,
        "end_scope": end_scope,
        "push_lexeme": push_lexeme,
        "set_var": set_var,
        "set_arr": set_arr,
        "save_func_add": save_func_add, 
        "stop_symbol": stop_symbol,
        
        "label": label,
        "get_temp": get_temp,
        "start_return": start_return,
        "end_return": end_return,
        "return_address": return_address,
        "save_func_atts": save_func_atts,
        "func_backpatching": func_backpatching,
        "pop": pop,
        "save": save,
        "jpf": jpf,
        "jpf_save": jpf_save,
        "jp": jp,
        "return_func": return_func,
        "assign": assign,
        "operation": operation,
        "access_array_index": access_array_index,
        "mult": mult,
        "output": output,
        "call_function": call_function,
        "assign_array_index": assign_array_index,
    }.get(action)(token)
    

