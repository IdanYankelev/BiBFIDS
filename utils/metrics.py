number_expansions = 0.0
number_nodes = 0.0
State = None
Search = None


def reset_metrics():
    global number_expansions, number_nodes
    number_expansions = 0.0
    number_nodes = 0.0


def increase_number_expansions():
    global number_expansions
    number_expansions += 1.0


def increase_number_nodes():
    global number_nodes
    number_nodes += 1.0


def set_state(state):
    global State  # Use the global keyword to modify the global variable
    State = state


def set_search(search):
    global Search
    Search = search


def start_search(*args, **kwargs):
    global Search  # Use the global keyword to modify the global variable
    return Search(*args, **kwargs)


def get_state(*args, **kwargs):
    global State  # Use the global keyword to modify the global variable
    return State(*args, **kwargs)


def get_number_expansions():
    global number_expansions
    return number_expansions


def get_percentage():
    global number_expansions, number_nodes
    return number_expansions / number_nodes if number_nodes != 0 else 0
