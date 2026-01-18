.. meta::
    :description lang=en: PyTorch distributed training guide covering data parallelism, model parallelism, DDP, FSDP, multi-GPU training, and cluster deployment
    :keywords: Python, Python3, PyTorch, distributed training, DDP, FSDP, data parallel, model parallel, multi-GPU, NCCL, cluster

============================
PyTorch Distributed Training
============================

.. contents:: Table of Contents
    :backlinks: none

Parallelism
-----------

.. code-block:: python

    def parallelism(
        nodes,             # number of nodes
        nproc,             # number of process per node
        tp,                # tensor_model_parallel_size
        etp,               # expert_tensor_parallel_size
        cp,                # context_parallel_size
        ep,                # expert_model_parallel_size
        pp,                # pipeline_model_parallel_size
        vpp,               # virtual_pipeline_model_parallel_size
        gbs,               # global_batch_size
        mbs,               # micro_batch_size
        num_layers,
        num_query_groups,
        num_attention_heads,
        overlap_p2p_comm,
        sequence_parallel,
    ):
        world_size = nodes * nproc
        assert world_size % (tp * pp * cp) == 0
        assert world_size % (etp * pp * ep) == 0

        # data parallel size
        dp = world_size // (tp * pp * cp)
        # expert data parallel size
        edp = world_size // (etp * pp * ep)

        assert gbs % dp == 0, f"{gbs=} should be divisible by {dp=}"
        assert gbs % mbs == 0, f"{gbs=} should be divisible by {mbs=}"

        num_batches = gbs // mbs
        assert num_batches // pp == 0, f"{num_batches=} should be divisible by {pp=}"
        assert gbs % (mbs * dp) == 0, f"{gbs=} should be divisible by {dp=}*{mbs=}"
        assert num_attention_heads % num_query_groups == 0
        assert num_attention_heads % tp == 0
        assert pp <= num_layers, f"{pp=} should be less or equal to {num_layers=}"
        assert vpp <= num_layers
        assert num_layers % (pp * vpp) == 0
        assert sequence_parallel and tp > 1
