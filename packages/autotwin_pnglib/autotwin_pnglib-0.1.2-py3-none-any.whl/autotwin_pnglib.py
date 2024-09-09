import os
import json
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
import snakes.plugins
import autotwin_gmglib as gmg

from ast import literal_eval
from pyscipopt import Model, quicksum
from neo4j import GraphDatabase

snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import *


def load_data(data_path: str) -> pd.DataFrame:
    """
    Load the data from the csv file
    Args:
        data_path (str): file path of the data
    Returns:
        data (pd.DataFrame): data
    """
    data = pd.read_csv(data_path)
    data = data.fillna(value="epsilon")
    data['state_list'] = data['state_list'].apply(literal_eval)
    if data['state_semantic_list'] is not None:
        data.at[0, 'state_semantic_list'] = literal_eval(data.at[0, 'state_semantic_list'])
    return data


def load_config(config_path: str) -> dict:
    """
    Load the config file
    Args:
        config_path (str): file path of the config file
    Returns:
        config (dict): config
    """
    # Read the config (JSON file) and convert it into a dictionary
    with open(config_path, encoding="utf-8") as config_file:
        config = json.load(config_file)
    return config


def extract_keys(obj: dict, prefix: str = '') -> list:
    """
    Extract keys from a dictionary with recursive method
    Args:
        obj (dict): dict
        prefix (str): concatenated keys
    Returns:
        list
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_prefix = f"{prefix}_{key}" if prefix else key
            yield from extract_keys(value, new_prefix)
    else:
        yield prefix


def extract_values(obj: dict) -> list:
    """
    Extract values from a dictionary with recursive method
    Args:
        obj (dict): dict
    Returns:
        list
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from extract_values(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from extract_values(item)
    else:
        yield obj


def reconstruct_state(config: dict[str, str]):
    """
    Reconstruction of the state of the event log
    Args:
        config (dict): configuration of state reconstruction algorithm
    """
    print('Start extracting the event log from SKG...')
    gmg.import_log(config)
    log = gmg.load_log(config)
    print('Extract event log is done!')

    print('Start reconstructing the state of the system...')
    gmg.generate_model(log, config)
    log.to_csv(config['path']['recons_state'])
    print('Reconstruct the state of the system is done!')


def generate_input_data(log_path: str, input_data_path: str):
    """
    Remove redundant information of the event log and generate input data for Petri net generation algorithm
    Args:
        log_path (str): file path of the reconstructed state log
        input_data_path (str): input data file path
    """
    print('Start generating input data for Petri net generation algorithm...')
    log = pd.read_csv(log_path)
    log_copy = log.copy()

    # create event
    if log_copy['station'].dtype != 'object':
        log_copy['station'] = log_copy['station'].astype(str)
    log_copy['event'] = log_copy['station'].str.cat(log_copy['activity'], sep='_')

    # remove state is None column
    log_copy = log_copy[log_copy['state'].notnull()]
    # convert the string representation of dictionary to actual dictionary
    log_copy.loc[:, 'state'] = log_copy['state'].apply(literal_eval)

    # extract the keys and values of the dictionary
    log_copy.loc[:, 'state_list'] = log_copy.loc[:, 'state'].apply(lambda x: list(extract_values(x)))
    log_copy.loc[:, 'state_semantic_list'] = None
    first_valid_index = log_copy['state'].first_valid_index()
    log_copy.at[first_valid_index, 'state_semantic_list'] = list(extract_keys(log_copy.at[first_valid_index, 'state']))

    # here is using domain knowledge to handle the state
    state_array = np.array(log_copy['state_list'].tolist())
    state_sematic_array = np.array(log_copy.at[first_valid_index, 'state_semantic_list'])

    max_state = np.amax(state_array, axis=0)

    # delete the max state is 0 column
    state_array = np.delete(state_array, np.argwhere(max_state == 0), axis=1)
    state_sematic_array = np.delete(state_sematic_array, np.argwhere(max_state == 0))

    # find the machine index
    indices = np.char.find(state_sematic_array, '_M_')
    machine_index = np.argwhere(indices != -1)
    machine_busy_state = state_array[:, machine_index.flatten()]

    # unique_counts is a dictionary where the keys are the column indices and the values occurred numbers in that column
    unique_counts = {}
    for i in range(machine_busy_state.shape[1]):
        unique_values, counts = np.unique(machine_busy_state[:, i], return_counts=True)
        unique_values, counts = unique_values.tolist(), counts.tolist()
        unique_counts[state_sematic_array[machine_index[i, 0]]] = dict(zip(unique_values, counts))

    # handle the state
    max_state = np.amax(state_array, axis=0)
    # calculate the buffer level state
    diff_array = max_state - state_array
    # convert machine idle state to 0-1 state
    for index in machine_index.flatten():
        mask = state_array[:, index] == 0
        diff_array[mask, index] = 1
        diff_array[~mask, index] = 0

    new_state = np.ones((state_array.shape[0], state_array.shape[1] * 2), dtype=int)
    new_state[:, 0::2] = state_array
    new_state[:, 1::2] = diff_array

    # handle the state semantic
    state_sematic_array = np.char.replace(state_sematic_array, '_B_', '_Buffer_Level_')
    state_sematic_array = np.char.replace(state_sematic_array, '_M_', '_Machine_Busy_')
    state_sematic_diff_array = state_sematic_array.copy()
    state_sematic_diff_array = np.char.replace(state_sematic_diff_array, '_Buffer_Level_', '_Buffer_Slot_')
    state_sematic_diff_array = np.char.replace(state_sematic_diff_array, '_Machine_Busy_', '_Machine_Idle_')

    new_state_semantic = np.empty((state_sematic_array.shape[0] * 2,), dtype=state_sematic_array.dtype)
    new_state_semantic[0::2] = state_sematic_array
    new_state_semantic[1::2] = state_sematic_diff_array

    log_copy['state_list'] = new_state.tolist()
    log_copy.at[first_valid_index, 'state_semantic_list'] = new_state_semantic.tolist()

    log_copy.to_csv(input_data_path, columns=['event', 'state_list', 'state_semantic_list'], index=False)
    print('Generate input data is done!')


class Algorithm:
    """
    Petri nets generation algorithm.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Args:
            data (dataframe): input data
        """
        self.dim_state_vector = len(data['state_list'][0])  # dimension of the state vector
        self.num_place_bar = len(data['state_list'][0])  # upper bound of the number of the places
        self.initial_state = data['state_list'][0]  # initial state vector

        # parameters of Petri net
        self.num_places = None
        self.num_trans = None
        self.place = []  # place list
        self.place_without_semantic = []  # place list without semantic
        self.trans = []  # transition list
        self.trans_without_semantic = []  # transition list without semantic
        self.input_matrix = None  # input incidence matrix
        self.output_matrix = None  # output incidence matrix
        self.inhibitor_matrix = None  # inhibitor incidence matrix
        self.initial_marking = None  # initial marking
        self.lambda_inverse_func = {}  # associated transitions of each event

        self.petri_net = {
            'place': self.place,
            'transition': self.trans,
            'input_matrix': self.input_matrix,
            'output_matrix': self.output_matrix,
            'initial_marking': self.initial_marking,
            'lambda_inverse_func': self.lambda_inverse_func
        }

        # parameters used in the identification algorithm
        self.z = {}  # the number of associated transitions of each event, for example,  self.z = {'e1': 3, 'e2': 1}
        # associated to each occurring events storing the difference yi-yi-1 that is employed to infer the transition
        # first dimension: sequential order of the event, second dimension: number of places, third dimension: 1
        self.k = np.zeros((1, self.dim_state_vector, 1), dtype=int)
        self.event_list = []  # all events list, for example, E = ['e0', 'e1', ..., 'e9']
        self.Y = np.array(self.initial_state, dtype=int).reshape(1, self.dim_state_vector, 1)  # storing output vectors
        self.M = np.array(self.initial_state, dtype=int).reshape(
            1, self.dim_state_vector, 1)  # storing marking vectors (after firing corresponding transitions)

    def generate_model(self, data) -> dict:
        """
        Generate model according to the input data
        Args:
            data (dataframe): input data
        Returns:
            model (dict): Petri nets model
        """
        print('Start generating Petri nets model...')
        print('Mining the transitions and places...')

        for index, row in data.iterrows():
            if index == 0:
                pass
            else:
                self.mine_transitions(index - 1, row['event'], row['state_list'])
        self.trans_without_semantic = ['T' + str(i + 1) for i in range(self.trans.__len__())]
        self.mine_places(data)

        print('Mine the transitions and places is done!')
        print('Start solving the linear programming problem to get the incidence matrices...')

        # offline identification algorithm
        for i in range(self.dim_state_vector, self.num_place_bar + 1):
            try:
                self.compute_incidence_matrices(i)
            except Exception as error:
                print(str(error))

        print('Solve the linear programming problem is done!')
        print('Generate Petri nets model is done!')
        return self.petri_net

    def mine_transitions(self, event_order: int, event: str, output: list[int]):
        """
        Mine transitions according to the event its introduced state changes, add semantic to the transitions
        Args:
            event_order (int): event sequential order
            event (str): input event
            output (list): output vector
        """
        if event not in self.event_list:
            # event occurs for the first time
            beta = 1
            self.event_list.append(event)
            self.z[event] = 1
            new_trans_name = 'T' + '_' + event + '_' + str(beta)
            self.lambda_inverse_func[event] = [new_trans_name]
            self.trans.append(new_trans_name)
            # diff = np.subtract(np.array(output).reshape(self.q, 1), self.Y[event_order]).reshape(1, self.q, 1)
            self.k = np.vstack(
                (self.k,
                 np.subtract(np.array(output).reshape(self.dim_state_vector, 1), self.Y[event_order]).reshape(1, self.dim_state_vector, 1)))
            self.Y = np.vstack((self.Y, np.array(output).reshape(1, self.dim_state_vector, 1)))
            if event_order == 0:
                pass
            else:
                self.M = np.vstack((self.M, self.Y[event_order].reshape(1, self.dim_state_vector, 1)))
        else:
            # event occurred previously
            flag = 0
            for i in range(self.k.shape[0]):
                # checking whether the transition is a new transition
                # diff = np.subtract(np.array(output).reshape(self.q, 1), self.Y[event_order]).reshape(1, self.q, 1)
                if (self.k[i] == np.subtract(np.array(output).reshape(self.dim_state_vector, 1), self.Y[event_order])).all():
                    beta = i
                    flag = 1
                    self.z[event] += 1
            if flag == 0:
                # A new transition must be associated to the event
                self.z[event] += 1
                beta = self.lambda_inverse_func[event].__len__() + 1
                self.k = np.vstack(
                    (self.k,
                     np.subtract(np.array(output).reshape(self.dim_state_vector, 1), self.Y[event_order]).reshape(1, self.dim_state_vector,
                                                                                                                  1)))
                new_trans_name = 'T' + '_' + event + '_' + str(beta)
                self.lambda_inverse_func[event].append(new_trans_name)
                self.trans.append(new_trans_name)
                self.Y = np.vstack((self.Y, np.array(output).reshape(1, self.dim_state_vector, 1)))
                self.M = np.vstack((self.M, self.Y[event_order].reshape(1, self.dim_state_vector, 1)))
            else:
                # A fired transition is associated to the event
                self.Y = np.vstack((self.Y, np.array(output).reshape(1, self.dim_state_vector, 1)))

    def mine_places(self, data: pd.DataFrame):
        """
        Mine places and add semantic to the places
        Args:
            data (dataframe): input data
        """
        self.place = data['state_semantic_list'][0]
        self.place_without_semantic = ['P' + str(i + 1) for i in range(self.place.__len__())]

    def compute_incidence_matrices(self, num_places: int):
        """
        Compute incidence matrices of the Petri net
        Args:
            num_places (int): number of places
        """
        lp_model = Model()  # building linear programming problem model
        lp_model.setIntParam('display/verblevel', 0)  # disable the output of the solver

        self.num_trans = len(self.trans)  # calculating the number of transitions after the mining process
        if self.dim_state_vector == self.num_place_bar:
            self.num_places = self.dim_state_vector
            initial_marking = np.array(self.initial_state).reshape(self.num_places, 1)  # assuming initial_state is pre-defined
        else:
            self.num_places = num_places
            # adding initial_marking as variables since initial state not predefined in this case
            initial_marking = np.array(
                [lp_model.addVar(vtype="INTEGER", name=f"initial_marking_{i}", lb=0) for i in
                 range(self.num_places)]).reshape((self.num_places, 1))

        # setting variables of the model
        input_matrix = np.array(
            [[lp_model.addVar(vtype="INTEGER", name=f"input_matrix_{i}_{j}", lb=0) for j in range(self.num_trans)] for i in
             range(self.num_places)])
        output_matrix = np.array(
            [[lp_model.addVar(vtype="INTEGER", name=f"output_matrix_{i}_{j}", lb=0) for j in range(self.num_trans)] for i in
             range(self.num_places)])

        M = self.M.transpose(1, 0, 2)  # marking matrix, dimension: m×n
        M = np.squeeze(M, axis=-1)
        marking_change = self.k[1:].transpose(1, 0, 2)  # marking change matrix, dimension: m×n
        marking_change = np.squeeze(marking_change, axis=-1)

        # constraint: transitions are all connected
        for j in range(self.num_trans):
            lp_model.addCons(
                quicksum(output_matrix[i][j] for i in range(self.num_places)) + quicksum(
                    input_matrix[i][j] for i in range(self.num_places)) >= 1)

        # constraint: places are all connected
        for i in range(self.num_places):
            lp_model.addCons(quicksum(output_matrix[i][j] for j in range(self.num_trans)) + quicksum(
                input_matrix[i][j] for j in range(self.num_trans)) >= 1)

        # constraint: enabling condition
        for i in range(self.num_places):
            for j in range(self.num_trans):
                lp_model.addCons(input_matrix[i][j] <= M[i][j])

        # constraint: firing condition
        for i in range(self.num_places):
            for j in range(self.num_trans):
                lp_model.addCons(output_matrix[i][j] - input_matrix[i][j] == marking_change[i][j])

        # setting objective function
        lp_model.setObjective(
            quicksum(quicksum(input_matrix[i][j] + output_matrix[i][j] for j in range(self.num_trans)) for i in range(self.num_places)),
            'minimize')

        # solving the problem
        lp_model.optimize()

        # checking lp model status
        if lp_model.getStatus() == 'infeasible':
            raise Exception('Model is infeasible!')
        elif lp_model.getStatus() == 'unbounded':
            raise Exception('Model is unbounded!')
        else:
            # extracting solution values
            self.input_matrix = np.array(
                [[lp_model.getVal(input_matrix[i, j]) for j in range(self.num_trans)] for i in range(self.num_places)])
            self.output_matrix = np.array(
                [[lp_model.getVal(output_matrix[i, j]) for j in range(self.num_trans)] for i in range(self.num_places)])
            if not isinstance(initial_marking, np.ndarray):
                self.initial_marking = np.array([lp_model.getVal(initial_marking[i, 0]) for i in range(self.num_places)]).reshape(
                    self.num_places, 1)
            else:
                self.initial_marking = initial_marking

    def save_model(self, file_path):
        """
        Save the identified Petri net model to JSON and PNML files
        Args:
            file_path: file path to save the model
        """
        file_path = os.path.join(file_path, 'parameters')
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        self.create_math_model(file_path)
        self.create_pnml(file_path)

    def create_math_model(self, file_path: str):
        """
        Create math model of identified Petri nets and save it into JSON file
        Args:
            file_path: file path to save the JSON file
        """
        if self.inhibitor_matrix is not None:
            model_paras = {
                'place': self.place,
                'transition': self.trans,
                'input_matrix': self.input_matrix.tolist(),
                'output_matrix': self.output_matrix.tolist(),
                'inhibitor_matrix': self.inhibitor_matrix.tolist(),
                'initial_marking': self.initial_marking.tolist(),
                'lambda_inverse_func': self.lambda_inverse_func
            }
        else:
            model_paras = {
                'place': self.place,
                'transition': self.trans,
                'input_matrix': self.input_matrix.tolist(),
                'output_matrix': self.output_matrix.tolist(),
                'initial_marking': self.initial_marking.tolist(),
                'lambda_inverse_func': self.lambda_inverse_func
            }

        with open(os.path.join(file_path, 'model.json'), 'w') as f:
            json.dump(model_paras, f)

    def create_pnml(self, file_path: str):
        """
        Create Petri Net Markup Language (PNML) of identified Petri net and save it into XML files
        Args:
            file_path: file path to save the XML file
        """
        # define namespaces
        ET.register_namespace('', "http://www.pnml.org/version-2009/grammar/pnml")

        # create the root element with updated XML declaration
        pnml = ET.Element('pnml', xmlns="http://www.pnml.org/version-2009/grammar/pnml")
        net = ET.SubElement(pnml, 'net', id="PT", type="http://www.pnml.org/version-2009/grammar/ptnet")
        page = ET.SubElement(net, 'page', id="page1")

        # add places with initial markings
        for i, place in enumerate(self.place):
            place_element = ET.SubElement(page, 'place', id=place)
            name = ET.SubElement(place_element, 'name')
            ET.SubElement(name, 'text').text = place
            initial = ET.SubElement(place_element, 'initialMarking')
            ET.SubElement(initial, 'text').text = str(int(self.initial_marking[i]))

        # add transitions
        for transition in self.trans:
            transition_element = ET.SubElement(page, 'transition', id=transition)
            name = ET.SubElement(transition_element, 'name')
            ET.SubElement(name, 'text').text = transition

        # add arcs (input, output, inhibitor)
        def add_arcs(matrix, source, target, arc_type="normal"):
            for j, row in enumerate(matrix):
                for k, val in enumerate(row):
                    if val > 0:
                        if arc_type == "input":
                            arc_id = f"{arc_type}_{source[j]}_to_{target[k]}"
                            arc = ET.SubElement(page, 'arc', id=arc_id, source=source[j], target=target[k])
                            inscription = ET.SubElement(arc, 'inscription')
                            ET.SubElement(inscription, 'text').text = str(int(matrix[j, k]))
                        if arc_type == "output":
                            arc_id = f"{arc_type}_{target[k]}_to_{source[j]}"
                            arc = ET.SubElement(page, 'arc', id=arc_id, source=target[k], target=source[j])
                            inscription = ET.SubElement(arc, 'inscription')
                            ET.SubElement(inscription, 'text').text = str(int(matrix[j, k]))
                        if arc_type == "inhibitor":
                            arc_id = f"{arc_type}_{source[j]}_to_{target[k]}"
                            arc = ET.SubElement(page, 'arc', id=arc_id, source=source[j], target=target[k])
                            inscription = ET.SubElement(arc, 'inscription')
                            ET.SubElement(inscription, 'text').text = str(int(matrix[j, k]))
                            # Add type element for inhibitor arcs
                            type_element = ET.SubElement(arc, 'type')
                            type_element.set('value', 'inhibitor')

        add_arcs(self.input_matrix, self.place, self.trans, arc_type="input")
        add_arcs(self.output_matrix, self.place, self.trans, arc_type="output")
        if self.inhibitor_matrix is not None:
            add_arcs(self.inhibitor_matrix, self.place, self.trans, arc_type="inhibitor")

        # write to file with specified encoding
        file_name = os.path.join(file_path, 'model.pnml')
        tree = ET.ElementTree(pnml)
        tree.write(file_name, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def load_model(file_path: str) -> dict[str, any]:
        """
        Load Petri net model from JSON files
        Args:
            file_path (str): file path of the model
        Returns:
            model (dict): Petri net model
        """
        file_path = os.path.join(file_path, 'parameters')
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        with open(os.path.join(file_path, 'model.json'), 'r') as f:
            model = json.load(f)

        return model

    def show_model(self, file_path, engine='dot', add_semantic=True):
        """
        Show Petri nets with SNAKES package
        Args:
            file_path: path to save the model
            engine: engine (dot, neato, circo, fdp, sfdp, twopi) to draw the model, default: dot
            add_semantic: whether to add semantic to the places and transitions
        """
        file_path = os.path.join(file_path, 'pictures')
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        net = PetriNet('Identified Petri Nets')

        # add places and transitions
        if add_semantic:
            # add places and transitions with semantic
            for m, place_name in enumerate(self.place):
                net.add_place(Place(place_name, self.initial_marking[m]))
            for n, trans_name in enumerate(self.trans):
                net.add_transition(Transition(trans_name))

            # add input arc
            pre_index = np.nonzero(self.input_matrix)
            for j in range(pre_index[0].size):
                value = self.input_matrix[pre_index[0][j], pre_index[1][j]]
                place_name = self.place[pre_index[0][j]]
                trans_name = self.trans[pre_index[1][j]]
                net.add_input(place_name, trans_name, Value(value))

            # add output arc
            post_index = np.nonzero(self.output_matrix)
            for k in range(post_index[0].size):
                value = self.output_matrix[post_index[0][k], post_index[1][k]]
                place_name = self.place[post_index[0][k]]
                trans_name = self.trans[post_index[1][k]]
                net.add_output(place_name, trans_name, Value(value))

            # draw the model
            # engine: neato: horizontal drawings of directed graphs , dot: hierarchical/vertical or layered drawings of
            # directed graphs, circo: circular layout, fdp, sfdp, twopi
            net.draw(os.path.join(file_path, 'model_with_semantic_{}.pdf'.format(engine)), engine=engine)
            net.draw(os.path.join(file_path, 'model_with_semantic_{}.png'.format(engine)), engine=engine)
        else:
            for m, place_name in enumerate(self.place_without_semantic):
                net.add_place(Place(place_name, self.initial_marking[m]))
            for n, trans_name in enumerate(self.trans_without_semantic):
                net.add_transition(Transition(trans_name))

            # add input arc
            pre_index = np.nonzero(self.input_matrix)
            for j in range(pre_index[0].size):
                value = self.input_matrix[pre_index[0][j], pre_index[1][j]]
                place_name = self.place_without_semantic[pre_index[0][j]]
                trans_name = self.trans_without_semantic[pre_index[1][j]]
                net.add_input(place_name, trans_name, Value(value))

            # add output arc
            post_index = np.nonzero(self.output_matrix)
            for k in range(post_index[0].size):
                value = self.output_matrix[post_index[0][k], post_index[1][k]]
                place_name = self.place_without_semantic[post_index[0][k]]
                trans_name = self.trans_without_semantic[post_index[1][k]]
                net.add_output(place_name, trans_name, Value(value))

            # draw the model
            net.draw(os.path.join(file_path, 'model_without_semantic_{}.pdf'.format(engine)), engine=engine)
            net.draw(os.path.join(file_path, 'model_without_semantic_{}.png'.format(engine)), engine=engine)

    def export_model(self, model, config):
        """Export a graph model to a Neo4j database.
        Args:
            model: Petri net model
            config: Configuration.
        Returns:
            PetriNet node ID
        """
        print('Start exporting the Petri net model to Neo4j...')
        uri = config['neo4j']['uri']
        username = config['neo4j']['username']
        password = config['neo4j']['password']
        driver = GraphDatabase.driver(uri, auth=(username, password))

        num_places = len(model['place'])
        print(f'Number of places: {num_places}')
        num_transitions = len(model['transition'])
        print(f'Number of transitions: {num_transitions}')
        num_arcs = np.nonzero(model['input_matrix'])[0].shape[0] + np.nonzero(model['output_matrix'])[0].shape[0]
        print(f'Number of arcs: {num_arcs}')

        # create Petri net nodes in Neo4j
        with driver.session() as session:
            petri_net_id = session.write_transaction(self.create_petri_net_skg, model)

        # link Petri net nodes with system nodes
        with driver.session() as session:
            session.write_transaction(self.link_petri_net_to_system, model)

        driver.close()
        print('Export the Petri net model to Neo4j is done!')

        return petri_net_id

    @staticmethod
    def create_petri_net_skg(tx, petri_net: dict[str, any]):
        """
        Create Petri net nodes in Neo4j
        Args:
            tx: Transaction
            petri_net: Petri net data
        Returns:
            PetriNet node ID
        """
        # create the PetriNet node
        result = tx.run("MERGE (pn:PetriNet {sysId: 'PetriNet'}) RETURN elementId(pn) AS eid")
        petri_net_id = result.single()["eid"]

        # create nodes for places and connect them to the PetriNet node
        for place in petri_net['place']:
            tx.run(
                """
                MATCH (pn:PetriNet {sysId: 'PetriNet'})
                MERGE (pl:Place {sysId: $place_id})
                ON CREATE SET pl.sysId = $place_id
                MERGE (pl)-[:IS_PART_OF]->(pn)
                """,
                place_id=place
            )

        # create nodes for transitions and connect them to the PetriNet node
        for transition in petri_net['transition']:
            type_value = 'EXIT' if 'EXIT' in transition else 'ENTER' if 'ENTER' in transition else None
            sub_type_value = None
            if 'AR' in transition:
                sub_type_value = 'AR'
            elif 'AP' in transition:
                sub_type_value = 'AP'
            elif 'BP' in transition:
                sub_type_value = 'BP'
            elif 'BR' in transition:
                sub_type_value = 'BR'

            tx.run(
                """
                MATCH (pn:PetriNet {sysId: 'PetriNet'})
                MERGE (tr:Transition {sysId: $transition_id})
                ON CREATE SET tr.sysId = $transition_id, tr.type = $type, tr.subType = $sub_type
                MERGE (tr)-[:IS_PART_OF]->(pn)
                """,
                transition_id=transition,
                type=type_value,
                sub_type=sub_type_value
            )

        # create relationships for input arcs
        for i, place in enumerate(petri_net['place']):
            for j, transition in enumerate(petri_net['transition']):
                weight = petri_net['input_matrix'][i][j]
                if weight > 0:
                    tx.run(
                        """
                        MATCH (p:Place {sysId: $place_id}), (t:Transition {sysId: $transition_id})
                        MERGE (p)-[:INPUT {weight: $weight}]->(t)
                        """,
                        place_id=place, transition_id=transition, weight=weight
                    )

        # Create relationships for output arcs
        for i, place in enumerate(petri_net['place']):
            for j, transition in enumerate(petri_net['transition']):
                weight = petri_net['output_matrix'][i][j]
                if weight > 0:
                    tx.run(
                        """
                        MATCH (p:Place {sysId: $place_id}), (t:Transition {sysId: $transition_id})
                        MERGE (t)-[:OUTPUT {weight: $weight}]->(p)
                        """,
                        place_id=place, transition_id=transition, weight=weight
                    )

        # Add 'token' attributes to all Place nodes
        for i, place in enumerate(petri_net['place']):
            token_value = petri_net['initial_marking'][i][0]
            tx.run("MATCH (p:Place {sysId: $place_id}) SET p.token = $token", place_id=place, token=token_value)

        # Add 'PetriNetFeature' label to all Place nodes
        tx.run("MATCH (p:Place) SET p:PetriNetFeature")

        # Add 'PetriNetFeature' label to all Transition nodes
        tx.run("MATCH (t:Transition) SET t:PetriNetFeature")

        return petri_net_id

    @staticmethod
    def link_petri_net_to_system(tx, petri_net):
        """
        Link Petri net nodes to system nodes in Neo4j
        Args:
            tx: Transaction
            petri_net: Petri net data
        """
        # link Place nodes to corresponding Station nodes
        for place in petri_net['place']:
            station_id = place.split('_')[0]
            tx.run(
                """
                MATCH (p:Place {sysId: $place_id}), (st:Station {sysId: $station_id})
                MERGE (p)-[:IS_MODEL_OF]->(st)
                """,
                place_id=place,
                station_id=station_id
            )

        # Link Transition nodes to corresponding Sensor nodes
        for transition in petri_net['transition']:
            station_id = transition.split('_')[1]
            tx.run(
                """
                MATCH (t:Transition {sysId: $transition_id}), (se:Sensor)-[:PART_OF]->(st:Station {sysId: $station_id})
                WHERE t.type = se.type
                  AND (
                       t.subType = se.subType OR 
                       (t.subType IS NULL AND se.subType IS NULL) OR 
                       se.subType IS NULL
                      )
                MERGE (t)-[:LABELLED_BY]->(se)
                """,
                transition_id=transition,
                station_id=station_id
            )
