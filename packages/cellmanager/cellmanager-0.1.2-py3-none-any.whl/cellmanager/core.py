from pathlib import Path
from typing import Literal
from warnings import warn

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from anytree import LevelOrderGroupIter, LevelOrderIter, Node, RenderTree, find, findall
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text


class CellNode(Node):
    def __init__(self, name, parent=None, children=None, **kwargs):
        super().__init__(name, parent, children)
        
        self.color = kwargs.get("color", "#000000")
        self.markers = kwargs.get("markers", [])
        self.organ = kwargs.get("organ", "PanCancer")       
    
    def update(self, **kwargs):
        if "color" in kwargs:
            self.color = kwargs["color"]
        if "markers" in kwargs:
            self.markers = kwargs["markers"]
        if "organ" in kwargs:
            self.organ = kwargs["organ"]
            
    def filter_markers(self, markers: list[str]):
        self.markers = [marker for marker in self.markers if marker in markers]
        if len(self.markers) == 0:
            warn(f"Aftering filtering, {self.name} has no markers left")


class CellManager:
    def __init__(self, filepath: str | Path, ) -> None:
        with open(filepath, "rb") as f:
            data = tomllib.load(f)
        self.cell_tree = self.create_cell_tree(data)
        self.level_table_rendered = False

    def create_cell_tree(self, data: dict) -> None:
        root = CellNode(name="Cell")
        create_tree(data=data, parent=root)
        return root
    
    def render_tree(self,):
        for pre, _, node in RenderTree(self.cell_tree):
            print(f"{pre}{node.name}")
    
    def render_level_table(self,):
        self.level_table_rendered = True
        self.level_order_group = [children for children in LevelOrderGroupIter(self.cell_tree)]
        
        table = Table(title="Level")
        table.add_column("Level", justify="center")
        table.add_column("cell type", justify="center")

        for idx, cell_types in enumerate(self.level_order_group):
            if idx == 0:
                continue
            text = Text()
            for i, cell_type in enumerate(cell_types):
                text.append(
                    f"{cell_type.name} | " if i < len(cell_types) - 1 else f"{cell_type.name}", 
                    style=Style(color=cell_type.color, bold=True)
                )
            table.add_row(Text(str(idx)), text)
            table.add_section()
            
        console = Console()
        console.print(table)
        
    def render_markers_table(self,):
        table = Table(title="Markers")
        table.add_column("Cell type", justify="center")
        table.add_column("Markers", justify="center", max_width=80)
        for level_group in self.level_order_group[1:]:
            for node in level_group:
                table.add_row(Text(node.name, style=Style(bold=True, color=node.color)), Text(", ".join(node.markers)))
                table.add_section()
        console = Console()
        console.print(table)
    
    def render_cluster_table(self, cluster: str):
        table = Table(title=cluster)
        table.add_column("Cell type", justify="center")
        table.add_column("Markers", justify="center", max_width=80)
        for node in find(self.cell_tree, filter_=lambda x: x.name == cluster).children:
            table.add_row(Text(node.name, style=Style(bold=True, color=node.color)), Text(", ".join(node.markers)))
            table.add_section()
        console = Console()
        console.print(table)
    
    def filter_markers(self, markers: list[str]):
        for node in LevelOrderIter(self.cell_tree):
            node.filter_markers(markers)

    def query(self, by: Literal["level", "cluster", "list"], key: str | list[str], info: Literal["color", "markers", "both"] = "markers", output_format: Literal["dict", "list"] = "dict", include_major: bool = False):
        if by == "level":
            if not self.level_table_rendered:
                raise ValueError("Level table has not been rendered yet, please call render_level_table() first")
            assert isinstance(key, int) and key > 0, "key must be an integer if by is 'level', and must be greater than 0"
            data = findall(self.cell_tree, filter_=lambda x: x in self.level_order_group[key])
        elif by == "cluster":
            assert isinstance(key, str), "key must be a string if by is 'cluster'"
            major_cell_type = find(self.cell_tree, filter_=lambda x: x.name == key)
            if major_cell_type:
                data = major_cell_type.children if not include_major else [major_cell_type] + list(major_cell_type.children)
            else:
                raise ValueError(f"Cell type {key} not found")
        elif by == "list":
            assert isinstance(key, list), "key must be a list if by is 'list'"
            data = findall(self.cell_tree, filter_=lambda x: x.name in key)
        else:
            raise ValueError("Unexpected value for `by`")
        
        if info in ["color", "markers"]:
            if output_format == "dict":
                return {node.name: getattr(node, info) for node in data}
            elif output_format == "list":
                return [node.name for node in data], [getattr(node, info) for node in data]
        else: # info == "both"
            if output_format == "dict":
                return {node.name: {"color": getattr(node, "color"), "markers": getattr(node, "markers")} for node in data}
            elif output_format == "list":
                return [node.name for node in data], [getattr(node, "color") for node in data], [getattr(node, "markers") for node in data]
            
    def add_cell_type(self, cell_properties: list[dict[str, str | list[str]]], force_update: bool = False):
        for cell_property in cell_properties:
            parent = find(self.cell_tree, lambda x: x.name == cell_property["parent"])
            if parent is None:
                raise ValueError(f"Cell type {cell_property['parent']} not found")
            cell_property.update({"parent": parent})

            node = find(self.cell_tree, lambda x: x.name == cell_property["name"])
            if node:
                warn(f"Cell type {cell_property['name']} already exists, if `force_update` is True, it will be overwritten, otherwise it will be skipped")
                if force_update:
                    node.update(**cell_property)
            else:
                CellNode(**cell_property)
                
            
def create_tree(data: dict, parent: str | None = None):
    for key, value in data.items():
        if isinstance(value, dict):
            node = CellNode(name=key, parent=parent, color=value.get("color", "#000000"), markers=value.get("markers", []))
            
            for sub_key, sub_value in value.items():
                if sub_key in ["color", "markers"]:
                    continue
                elif isinstance(sub_value, dict):
                    create_tree({sub_key: sub_value}, node)
                else:
                    raise ValueError(f"Please check the information about {sub_value} in {sub_key}")
