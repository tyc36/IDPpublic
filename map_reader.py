import json

class MapReader:
    def __init__(self, map_file="map1.json"):

        with open(map_file, 'r') as f:
            self.data = json.load(f)

        self.path_by_id = {
            "CW": {},
            "CCW": {}
        }

        for direction in ("CW", "CCW"):
            for item in self.data[direction]:
                pattern = item["pattern"]
                if isinstance(pattern, str):
                    item["pattern"] = tuple(int(x) for x in pattern)
                self.path_by_id[direction][item["id"]] = item

        self.loop = self.data.get("loop", False)

    def get_node(self, node_id, direction=0):
        dir_key = "CW" if direction == 1 else "CCW"
        return self.path_by_id[dir_key][node_id]

    def get_pattern(self, node_id, direction=0):
        return self.get_node(node_id, direction)["pattern"]

    def get_actions(self, node_id, direction=0):

        node = self.get_node(node_id, direction)
        return [
            node.get("action"),
            node.get("optional_action")  # returns None if no such key
        ]

    def get_action(self, node_id, direction=0): #basically useless function, old code
        return self.get_actions(node_id, direction)[0]

    def get_optional_action(self, node_id, direction=0): #basically useless function, old code
        return self.get_actions(node_id, direction)[1]

    def get_type(self, node_id, direction=0):
        return self.get_node(node_id, direction)["type"]
