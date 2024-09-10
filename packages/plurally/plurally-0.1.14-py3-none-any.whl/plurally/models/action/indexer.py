import hashlib
from typing import Any, Dict, List

import faiss
import numpy as np
from litellm import embedding
from loguru import logger
from pydantic import BaseModel, Field

from plurally.models.misc import Table
from plurally.models.node import Node
from plurally.models.utils import BaseEnvVars


class IndexDb:

    def __init__(self, index_col: str):
        self.model = "text-embedding-3-small"
        self.index_col = index_col
        self.reset()

    def reset(self):
        self._d = None  # force recompute
        self._data = []
        self._index = faiss.IndexFlatL2(self.d)
        self._data_hash = None

    def get_embeddings(self, inputs: List[str]):
        assert isinstance(inputs, list)
        if inputs:
            assert isinstance(inputs[0], str)

        resp_data = embedding(model=self.model, input=inputs)["data"]

        embds = [resp_data[ix]["embedding"] for ix in range(len(inputs))]
        return np.array(embds).reshape((len(inputs), -1))

    def add(self, inputs: List[Dict[str, str]]):
        try:
            embds = self.get_embeddings([inp[self.index_col] for inp in inputs])
        except KeyError:
            raise ValueError(f"Column {self.index_col} not found in input data")

        self._data.extend(inputs)
        self._index.add(embds)

    def rm(self, ix: List[int]):
        self._data = [d for i, d in enumerate(self._data) if i not in ix]
        self._index.remove_ids(np.array(ix))

    def compute_hash(self, inputs: List[Dict[str, str]]):
        frozensets = [frozenset(d.items()) for d in inputs]
        combined_frozenset = frozenset(frozensets)
        combined_str = str(combined_frozenset).encode()
        return f"{self.model}:{hashlib.sha256(combined_str).hexdigest()}"

    def sync(self, inputs: List[Dict[str, str]]):
        hashed_inputs = self.compute_hash(inputs)
        if self._data_hash == hashed_inputs:
            logger.debug("Data has not changed, skipping sync")
            return
        else:
            logger.debug("Data has changed, syncing")
            # FIXME: This is not efficient, but it's a simple way to do it, ideally, we should only add the new data and remove the old data that is not in the new data
            to_add_data = [d for d in inputs if d not in self._data]
            to_rm_data_ix = [ix for ix, d in enumerate(self._data) if d not in inputs]
            self.rm(to_rm_data_ix)
            self.add(to_add_data)
            self._data_hash = hashed_inputs
            logger.debug(
                f"Synced data, new data hash: {self._data_hash} / ntotal={self._index.ntotal}"
            )

    @property
    def d(self):
        if self._d is None:
            self._d = self.get_embeddings(["check d"]).shape[1]
            logger.debug(f"Setting embedding dimension to {self._d=}")
        return self._d

    def __len__(self):
        return len(self._data)


class Indexer(Node):
    DESC = """
    Finds the most similar rows in a table to a given query using AI powered search.
    """.strip()

    class InitSchema(Node.InitSchema):
        top_k: int = Field(
            5,
            title="Top K",
            description="The number of results to return.",
            examples=[5],
        )
        index_col: str = Field(
            title="Comparison Column",
            description="The column to do comparison on. "
            "For example, if your data is some example incoming emails (column=email) with answers (column=answer), "
            "you might want to index on the email column.",
            examples=["column_name"],
        )

    class OutputSchema(BaseModel):
        values: Table

    class InputSchema(Node.InputSchema):
        knowledge: Table
        query: str

    class EnvVars(BaseEnvVars):
        OPENAI_API_KEY: str = Field(
            None, title="OpenAI API Key", examples=["sk-1234567890abcdef"]
        )

    def __init__(
        self,
        init_inputs: InitSchema,
    ) -> None:
        self._index: IndexDb = None
        self._client = None  # lazy init
        self._model = "text-embedding-3-small"
        self.index_col = init_inputs.index_col
        self.top_k = init_inputs.top_k
        self._d = None
        super().__init__(init_inputs)

    def _sync(self, inputs: List[Dict[str, str]]):
        if self._index is None:
            self._index = IndexDb()
            logger.debug("Init IndexDb")
        self._index.sync(inputs)

    @property
    def client(self):
        if self._client is None:
            self._client = 1
        return self._client

    @property
    def index(self) -> IndexDb:
        if self._index is None:
            self._index = IndexDb(self.index_col)
        return self._index

    def forward(self, node_input: InputSchema) -> Any:
        self.index.sync(node_input.knowledge.data)

        query_embd = self.index.get_embeddings([node_input.query])
        _, indices = self.index._index.search(query_embd, self.top_k)
        self.outputs = {
            "values": Table(data=[self.index._data[ix] for ix in indices[0] if ix > -1])
        }

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            "index_col": self.index_col,
            "top_k": self.top_k,
        }
