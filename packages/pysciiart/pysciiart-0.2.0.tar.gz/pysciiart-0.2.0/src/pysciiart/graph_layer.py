from typing import List, Optional, Tuple, Any


class LayerModel:
    __layers: List[List[Any]]

    def __init__(self):
        self.__layers = [[]]

    def add(self, item: object) -> None:
        self.__layers[0].append(item)

    def find_item_position(self, item: object) -> Optional[Tuple[int, int]]:
        for layer_index, layer in enumerate(self.__layers):
            try:
                item_index = layer.index(item)
                return layer_index, item_index
            except ValueError as e:
                pass

        return None

    def shift(self, item: object) -> None:
        item_layer_index = self.find_item_position(item)[0]

        if item_layer_index == len(self.__layers) - 1:
            self.__layers.append([])

        self.__layers[item_layer_index].remove(item)
        self.__layers[item_layer_index + 1].append(item)

    def get_layers(self) -> List[List[Any]]:
        return self.__layers
