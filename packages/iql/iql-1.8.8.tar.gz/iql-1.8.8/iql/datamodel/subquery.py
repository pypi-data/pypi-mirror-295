from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, Iterable, Optional

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from .. import options_parser
from ..constants import get_cache
from . import extension
from .querycontainer import IqlQueryContainer

logger = logging.getLogger(__name__)


def get_subqueries_flat(queries: Iterable[SubQuery]) -> Iterable[SubQuery]:
    subqueries_flat = [q_inner for q_outer in queries for q_inner in q_outer.get_subqueries_flat()]
    return subqueries_flat


@dataclass
class SubQuery:
    extension: extension.IqlExtension
    subquery: str
    name: str
    dataframe: Optional[pd.DataFrame] = field(default=None, init=False)
    cache_policy: Optional[Dict[str, object]] = field(default=None, init=False)
    options: Dict[str, object] = field(default_factory=dict, init=False)
    input_data: object = field(default=None, init=False)
    iqc: IqlQueryContainer

    local_dfs: Dict[str, object] = field(default_factory=dict, init=False)

    def get_subqueries_flat(self) -> Iterable[SubQuery]:
        return [self]

    def merge(self):
        # Nothing to do for a single subquery
        pass

    def get_query(self) -> Optional[str]:
        """Returns the first parameter to:
        keyword(query, *params)"""
        if len(self.options) == 0:
            raise ValueError(f"Options not properly passed or parsed ({self.subquery})")

        value, query = next(iter(self.options.items()))

        if query is None:  # unnamed parameter
            return value
        else:
            return query  # type: ignore

    def __post_init__(self):
        try:
            if self.subquery is not None:
                self.options: Dict[str, object] = options_parser.options_to_list(self.subquery)
        except Exception as e:
            logger.exception("Exception in %.50s", self.subquery)
            raise ValueError(f"Parse Exception of {str(self.subquery)[:50]}") from e

    def populate_from_cache(self) -> bool:
        """Returns cached value if it's available"""
        cache_val = self.subquery

        logger.debug("Checking cache for %s, %s", cache_val, type(self))
        if not self.extension.allow_cache_read(self):
            logger.debug("Cache not allowed")
            return False

        df = get_cache().get(key=cache_val, policy=self.cache_policy)
        if df is not None:
            logger.debug("Using cached SubQuery")
            self.dataframe = df  # type: ignore
            return True
        else:
            logger.debug("Not found in cache %s", self.subquery)
            return False

    def save_to_cache(self):
        if not self.extension.allow_cache_save(self):
            return

        cache_val = self.subquery

        if self.dataframe is not None:
            get_cache().save(key=cache_val, data=self.dataframe, policy=self.cache_policy)


@dataclass
class SubQueryGroup(SubQuery):
    """SubQueryGroups represent a set of queries whose outputs will be combined.
    SubQueries are executed in parallel (via get_subqueries_flat),
    so this step is needed to gather the results.

    Our first implementation was to rely on database Unions, but performance wasn't
    great.

    Future: SubQueryGroups could support nesting, only one level supported now."""

    subqueries: Iterable[SubQuery]

    def __post_init__(self):
        self.subquery = None  # type: ignore
        self.options = None  # type: ignore

    def get_subqueries_flat(self) -> Iterable[SubQuery]:
        return self.subqueries

    def get_query(self) -> None:
        raise NotImplementedError("SubQueryGroups do not have/need a query")

    def merge(self):
        """Doesn't handle mismatched schemas when merging parquet files."""
        if self.extension.use_path_replacement():
            files = [  # type: ignore
                self.extension.get_path_replacement(sq, quote=False) for sq in self.subqueries
            ]

            logger.debug("Read %s parquet files", len(files))

            tables = [pq.read_table(f) for f in files]
            logger.debug("Done reading, concatting")

            table = pa.concat_tables(tables)

            outfile = self.extension.get_path_replacement(self, quote=False)
            logger.debug("Writing to final parquet file: %s", outfile)

            pq.write_table(table, outfile)

        else:
            dfs: list[pd.DataFrame] = [sq.dataframe for sq in self.subqueries]  # type: ignore
            logger.debug("Concatting %s", len(dfs))
            if len(dfs) == 1:
                self.dataframe = dfs[0]
            else:
                arrow_tables = [df for df in dfs if isinstance(df, pa.Table)]

                if len(arrow_tables) == len(dfs):
                    logger.debug("Merging py arrow tables")
                    for df in dfs:
                        if df is not None:
                            logger.debug("Table len: %s", df.num_rows)
                    df_combined = pa.concat_tables(dfs)
                    logger.debug("Merged len: %s", len(df_combined))
                    self.dataframe = df_combined
                elif len(arrow_tables) > 0:
                    raise ValueError("Mix of arrow and pandas dfs, not supported")
                else:
                    self.dataframe = pd.concat(dfs)

        logger.debug("Done merging subqueries")
