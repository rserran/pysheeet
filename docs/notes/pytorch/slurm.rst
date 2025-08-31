.. meta::
    :description lang=en: Collect useful snippets of Slurm
    :keywords: Python, Python3, Slurm


=====
Slurm
=====

Slurm Info
----------

.. code-block:: bash

    # show slurm general info
    sinfo

    # show partition info
    sinfo -s
    sinfo --summarize

    # show partition info
    PARTITION=dev
    sinfo -p ${PARTITION}

    # show nodes in idle state
    sinfo --state=idle

Submit Jobs
-----------

.. code-block:: bash

    # Submit a job to a compute node
    srun -N1 hostname

    # Submit a job on specific nodes
    srun --nodelist=compute-[0-5] hostname

    # Submit a job to a specific partition
    PARTITION=dev
    srun -p ${PARTITION} --nodelist=compute-[0-5] hostname

    # Submit a job via srun on 2 nodes (using dd to simulate a high CPU consume job)
    srun -N2 dd if=/dev/zero of=/dev/null

    # Submit a job with time constrain.
    # - minute
    # - minute:second
    # - hours:minutes:seconds
    # - days-hours
    # - days-hours:minutes
    # - days-hours:minutes:seconds
    #
    # ex: The following job will be timeout after 1m30s
    srun -N2 --time=01:30 dd if=/dev/zero of=/dev/null

    # login to a node
    srun -N 1 --pty /bin/bash

Alloc Nodes
-----------

.. code-block:: bash

    # Allocte 2 nodes and submit a job on those allocated nodes
    salloc -N 2
    srun hostname

    # Allocate nodes on a specific partition
    PARTITION=dev
    salloc -N 2 -p ${PARTITION}

Reservation
-----------

.. code-block:: bash

    # reserve nodes for a user to test
    # - minute
    # - minute:second
    # - hours:minutes:seconds
    # - days-hours
    # - days-hours:minutes
    # - days-hours:minutes:seconds
    #
    # ex: reserve all nodes 120m for maintenance
    scontrol create reservation ReservationName=maintenance \
        starttime=now duration=120 user=root flags=maint,ignore_jobs nodes=ALL

    # must specify reservation; otherwise, the job will not run
    srun --reservation=maintain ping 8.8.8.8 2>&1 > /dev/null

    # show reservations
    scontrol show res

    # delete a reservation
    scontrol delete ReservationName=maintain

Cancel Jobs
-----------

.. code-block:: bash

    # cancel a job
    $ scancel "${jobid}"

    # cancel a job and disable warnings
    $ scancel -q "${jobid}"

    # cancel all jobs which are belong to an account
    $ scancel --account="${account}"

    # cancel all jobs which are belong to a partition
    $ scancel --partition="${partition}"

    # cancel all pending jobs
    $ scancel --state="PENDING"

    # cancel all running jobs
    $ scancel --state="RUNNING"

    # cancel all jobs
    $ squeue -l | awk '{ print $ 1}' | grep '[[:digit:]].*' | xargs scancel

    # cancel all jobs (using state option)
    $ for s in "RUNNING" "PENDING" "SUSPAND"; do scancel --state="$s"; done


Submit Batch Jobs
-----------------

.. code-block:: bash

    #!/bin/bash
    #SBATCH --nodelist=compute-[0-1]
    srun hostname

    # sbatch job.sh

.. code-block:: bash

    #!/bin/bash

    #SBATCH --output=logs/%x_%j.out
    #SBATCH --error=logs/%x_%j.out

    HOSTFILE="hosts_${SLURM_JOB_ID}"
    scontrol show hostnames | sort > "$HOSTFILE"

    # sbatch hostname.sh
