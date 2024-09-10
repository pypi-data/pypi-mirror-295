import uuid
from copy import deepcopy
from typing import Any, Dict, List, Union, get_origin

import networkx as nx
from loguru import logger
from pydantic import BaseModel

from plurally import models
from plurally.models import utils
from plurally.models.node import Node
from plurally.models.source.constant import ConstantSource


def is_list_type(schema):
    return hasattr(schema, "annotation") and get_origin(schema.annotation) is list


class Flow:
    def __init__(self, name: str = "") -> None:
        self._flow_id = f"fl-{str(uuid.uuid4())}"
        self.name = name
        self.graph = nx.MultiDiGraph()

    def __contains__(self, node: Node):
        assert isinstance(node, Node)
        return node in self.graph

    def add_node(
        self,
        node: Node,
    ) -> Node:
        if node in self:
            raise ValueError(f"Node with {node.node_id=} already registered")
        self.graph.add_node(node)
        return node

    def update_node(
        self,
        node: Node,
    ) -> Node:
        if node not in self:
            raise ValueError(f"Node with {node.node_id=} not found")
        # self.graph.
        return node

    def get_node(self, node_id: str) -> Node:
        for node in self.graph.nodes:
            if node.node_id == node_id:
                return node
        raise ValueError(f"Node with {node_id=} not found")

    def connect_nodes(
        self,
        src_node: Union[str, "Node"],
        src_handle: str,
        tgt_node: Union[str, "Node"],
        tgt_handle: str,
    ):
        """Connect this node's output to another node's input."""
        if isinstance(src_node, str):
            src_node = self.get_node(src_node)
        if isinstance(tgt_node, str):
            tgt_node = self.get_node(tgt_node)

        if src_node is tgt_node:
            raise ValueError(f"Cannot connect node with itself: {src_node}")

        outputs_annots = src_node.OutputSchema.model_fields
        if src_handle not in outputs_annots:
            raise ValueError(
                f"Output {src_handle} not found in node {src_node}, options are {list(outputs_annots)}"
            )
        for node in (src_node, tgt_node):
            if node not in self:
                raise ValueError(f"{node} was not added to {self}")

        inputs_annots = tgt_node.InputSchema.model_fields
        if tgt_handle not in inputs_annots:
            raise ValueError(
                f"Input {tgt_handle} not found in node {tgt_node}, options are {list(inputs_annots)}"
            )

        # if tgt_handle is not a list and there already is a connection it is False
        if not is_list_type(inputs_annots[tgt_handle]):
            for src, tgt, key in self.graph.in_edges(tgt_node, data=True):
                if key["tgt_handle"] == tgt_handle:
                    raise ValueError(
                        f"Node {tgt_node.name} already has a connection for {tgt_handle}"
                    )

        if not tgt_node.validate_connection(src_node, src_handle, tgt_handle):
            raise ValueError(f"Connection between {src_node} and {tgt_node} is invalid")

        key = f"{src_handle}_{tgt_handle}"
        if (src_node, tgt_node, key) in self.graph.edges:
            raise ValueError(
                f"Connection between {src_node} and {tgt_node} with {src_handle=} and {tgt_handle=} already exists"
            )

        self.graph.add_edge(
            src_node,
            tgt_node,
            src_handle=src_handle,
            tgt_handle=tgt_handle,
            key=key,
        )

    def disconnect_nodes(
        self,
        src_node: Union[str, "Node"],
        src_handle: str,
        tgt_node: Union[str, "Node"],
        tgt_handle: str,
    ):
        """Disconnect this node connection."""
        if isinstance(src_node, str):
            src_node = self.get_node(src_node)
        if isinstance(tgt_node, str):
            tgt_node = self.get_node(tgt_node)
        if src_node is tgt_node:
            raise ValueError(f"Cannot connect node with itself: {src_node}")
        try:
            self.graph.remove_edge(src_node, tgt_node, key=f"{src_handle}_{tgt_handle}")
        except nx.NetworkXError:
            raise ValueError(
                f"Connection between {src_node} and {tgt_node} with {src_handle=} and {tgt_handle=} not found"
            )

    def delete_node(self, node: Union[str, "Node"]):
        """Remove a node from the flow."""
        if isinstance(node, str):
            node = self.get_node(node)
        self.graph.remove_node(node)

    def __call__(self, output_overrides: Dict[str, BaseModel] = None) -> Any:
        output_overrides = output_overrides if output_overrides else {}
        if output_overrides:
            logger.debug(f"Will override for nodes: {','.join(output_overrides)}")
        no_run = set()
        for item in nx.topological_sort(self.graph):
            if not isinstance(item, Node):
                break

            if isinstance(item, ConstantSource):
                # constant source always have outputs and it is not reset at every iteration
                continue

            item.outputs = {}
        for item in nx.topological_sort(self.graph):
            try:
                if not isinstance(item, Node):
                    break
                kwargs = {}
                for src_node, tgt_node, attrs in self.graph.in_edges(item, True):
                    src_handle = attrs["src_handle"]
                    tgt_handle = attrs["tgt_handle"]
                    if src_node.outputs is None:
                        # skip if source node has no outputs
                        logger.debug(
                            f"Aborting execution due to missing outputs from {src_node}"
                        )
                        return

                    src_value = src_node.outputs.get(src_handle)
                    # if it is a list, it should append
                    if is_list_type(tgt_node.InputSchema.model_fields[tgt_handle]):
                        if tgt_handle not in kwargs:
                            kwargs[tgt_handle] = []
                        kwargs[tgt_handle].append(src_value)
                    else:
                        kwargs[tgt_handle] = src_value
                    logger.debug(f"Processing {src_node} -> {tgt_node}")
                    logger.debug(f"Setting {tgt_handle} to {src_value}")

                node_overrides = output_overrides.get(item.node_id)
                if node_overrides:
                    logger.debug(f"Overriding execution of {item}")
                    item.outputs = node_overrides.model_dump()
                else:
                    parent_no_run = item in no_run
                    is_no_run = not kwargs.get("run", True)
                    if parent_no_run or is_no_run:
                        if parent_no_run:
                            logger.debug(
                                f"Skipping {item} - parent was marked as no_run"
                            )
                        if is_no_run:
                            logger.debug(f"Skipping {item} - run is set to False")
                        for node in self.graph.successors(item):
                            no_run.add(node)
                        continue
                    logger.debug(f"Forwarding {item} with {kwargs}")
                    item(**kwargs)
                    logger.debug(f"Finished {item}, outputs: {item.outputs}")
            except Exception as e:
                logger.exception(e)
                raise RuntimeError(
                    f"{type(item).__name__} [{item.name} (id={item.node_id[:4]})]\nfailed: {e}"
                ) from e

    def clear(self):
        for node in self.graph.nodes:
            node.outputs.clear()

    def __str__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, id={self._flow_id[:4]})"

    def serialize(self) -> Dict:
        s = nx.node_link_data(self.graph)
        s["nodes"] = [{**n, "id": n["id"].serialize()} for n in s["nodes"]]
        s["links"] = [
            {**link, "source": link["source"].node_id, "target": link["target"].node_id}
            for link in s["links"]
        ]
        return s

    @classmethod
    def parse(cls, data: Dict) -> "Flow":
        data = deepcopy(data)

        flow = cls()
        nodes = {}
        nodes_list = []
        for n in data["nodes"]:
            node = models.create_node(**n["id"])
            nodes[node.node_id] = node
            nodes_list.append(node)
        data["nodes"] = [{**n, "id": nodes[n["id"]["_node_id"]]} for n in data["nodes"]]
        data["links"] = [
            {**link, "source": nodes[link["source"]], "target": nodes[link["target"]]}
            for link in data["links"]
        ]
        flow.graph = nx.node_link_graph(data)
        return flow

    def __eq__(self, other: "Flow") -> bool:
        return (
            isinstance(other, Flow)
            and self.graph.nodes == other.graph.nodes
            and self.graph.edges == other.graph.edges
        )

    def get_necessary_env_vars(self) -> List[str]:
        env_vars = []
        for node in self.graph.nodes:
            if node.EnvVars:
                env_vars.extend(node.EnvVars.model_fields.keys())
        return env_vars

    def get_issues(self) -> List[str]:
        issues = []
        is_valid = nx.is_directed_acyclic_graph(self.graph)
        if not is_valid:
            issues.append("Graph is not a directed acyclic graph")
        if not self.graph.nodes:
            issues.append("Flow is empty")
        # ensure that all nodes are connected (when handle is not optional)
        for node in self.graph.nodes:
            required_inputs = utils.get_required_fields(node.InputSchema)
            for input_name in required_inputs:
                if not any(
                    [
                        (src, tgt, key)
                        for src, tgt, key in self.graph.in_edges(node, data=True)
                        if key["tgt_handle"] == input_name
                    ]
                ):
                    issues.append(
                        f"Node {node.name} is missing required input {input_name}"
                    )

            if node.EnvVars:
                logger.debug(f"Loading env vars for {node}")
                issues.extend(node.EnvVars.get_issues())

        return issues

    def is_valid(self) -> bool:
        return not self.get_issues()

    def get_source_nodes(self) -> List[Node]:
        if not self.is_valid():
            raise ValueError("Cannot get source nodes on invalid flow")
        return [x for x in self.graph.nodes() if self.graph.in_degree(x) == 0]

    def create_template(self):
        template = self.serialize()
        for node in template["nodes"]:
            kls, *_ = models.MAP[node["id"]["kls"]]

            for sensitive_field in kls.SensitiveFields:
                if sensitive_field in node["id"]:
                    del node["id"][sensitive_field]

        return template
