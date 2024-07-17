

from kedro.runner import SequentialRunner

from kedro.io import DataCatalog, MemoryDataset
from kedro.pipeline import Pipeline
from kedro.pipeline.node import Node
from collections import Counter
from itertools import chain

from pluggy import PluginManager
class BacktrackRunner(SequentialRunner):

    start_node_names = _find_nodes_to_resume_from(
        pipeline=pipeline,
        unfinished_nodes=remaining_nodes,
        catalog=catalog,
    )


    def _run(
        self,
        pipeline: Pipeline,
        catalog: DataCatalog,
        hook_manager: PluginManager,
        session_id: str | None = None,
    ) -> None:
        """The method implementing sequential pipeline running.

        Args:
            pipeline: The ``Pipeline`` to run.
            catalog: The ``DataCatalog`` from which to fetch data.
            hook_manager: The ``PluginManager`` to activate hooks.
            session_id: The id of the session.

        Raises:
            Exception: in case of any downstream node failure.
        """
        if not self._is_async:
            self._logger.info(
                "Using synchronous mode for loading and saving data. Use the --async flag "
                "for potential performance gains. https://docs.kedro.org/en/stable/nodes_and_pipelines/run_a_pipeline.html#load-and-save-asynchronously"
            )
        nodes = pipeline.nodes
        done_nodes = set()

        load_counts = Counter(chain.from_iterable(n.inputs for n in nodes))

        for exec_index, node in enumerate(nodes):
            try:
                run_node(node, catalog, hook_manager, self._is_async, session_id)
                done_nodes.add(node)
            except Exception:
                self._suggest_resume_scenario(pipeline, done_nodes, catalog)
                raise

            # decrement load counts and release any data sets we've finished with
            for dataset in node.inputs:
                load_counts[dataset] -= 1
                if load_counts[dataset] < 1 and dataset not in pipeline.inputs():
                    catalog.release(dataset)
            for dataset in node.outputs:
                if load_counts[dataset] < 1 and dataset not in pipeline.outputs():
                    catalog.release(dataset)

            self._logger.info(
                "Completed %d out of %d tasks", exec_index + 1, len(nodes)
            )
