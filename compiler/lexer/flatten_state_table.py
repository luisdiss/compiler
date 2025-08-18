from compiler.lexer.raw_state_table import raw_state_table, transiton_classes
import pprint

def flatten_state_table(state_table):
    new_state_table = {}
    for state, state_info in state_table.items():
        new_transitions = {}
        for trans_class, to_state in state_info.get("transitions", {}).items():
            for char in transiton_classes[trans_class]:
                new_transitions[char] = to_state
        new_state_table[state] = {**state_info, "transitions": new_transitions}
    return new_state_table

flattened_state_table = flatten_state_table(raw_state_table)

with open("flattened_state_table.py", "w") as f:
    f.write('flattened_state_table = ')
    f.write(pprint.pformat(flattened_state_table))
    f.write('\n')