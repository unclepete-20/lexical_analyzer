# Definición de la clase DFA.
class DFA(object):

    # Método constructor de DFA que recibe estados, alfabeto, estado inicial, estado de aceptación y mapeo de transiciones.
    def __init__(self, states, alphabet, initial_state, acceptance_states, mapping):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.acceptance_states = acceptance_states
        self.mapping = mapping
        

    # Método para simular un DFA.
    def simulate(self, input_string):
            
        # Se obtiene el estado actual.
        current_state = self.initial_state

        # Se recorre la cadena de entrada.
        for symbol in input_string:

            # Se obtiene el estado actual con el símbolo actual.
            current_transition = self.mapping.get(current_state, False)

            if (current_transition == False):
                return False

            current_state = current_transition.get(symbol, False)

            if ((type(current_state) == bool) and (current_state == False)):
                return False

        # Se retorna si el estado actual es de aceptación.
        return (current_state in self.acceptance_states)