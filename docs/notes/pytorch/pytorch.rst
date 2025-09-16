.. meta::
    :description lang=en: Collect useful snippets of PyTorch
    :keywords: Python, Python3, PyTorch

=======
PyTorch
=======

Info
----

.. code-block:: python

    # check cuda is available
    >>> import torch
    >>> torch.cuda.is_available()
    True

    # check NCCL version
    >>> torch.cuda.nccl.version()
    (2, 26, 2)

    # check distribution is initialized
    >>> import torch.distributed as dist
    >>> dist.is_initialized()
    False

    # check tensor device
    >>> tensor = torch.tensor([0,1,2,3,4,5])
    >>> tensor.device
    device(type='cpu')

    # bind process to a specific CUDA device
    >>> torch.cuda.set_device(0)
    >>> torch.cuda.current_device()
    0


New Tensors
-----------

.. code-block:: python

    # init CPU tencors
    x = torch.tensor([0,1,2,3,4,5])
    x = torch.empty(2, 2)
    x = torch.rand(2, 2)
    x = torch.ones(2, 2)
    x = torch.zeros(2, 2)

    # init GPU tensors
    device = torch.device("cuda:0")
    tensor = torch.tensor([1,2,3,4,5], device=device)

    # print(tensor)
    # tensor([1, 2, 3, 4, 5], device='cuda:0')

Arithmetic
----------

.. code-block:: python

    >>> x = torch.rand(2, 2, device=0)
    >>> y = torch.rand(2, 2, device=0)
    >>> x
    tensor([[0.2171, 0.7797],
            [0.7265, 0.6759]], device='cuda:0')
    >>> y
    tensor([[0.6766, 0.1862],
            [0.2438, 0.0076]], device='cuda:0')

    # elementwise addition
    >>> x + y
    tensor([[0.8937, 0.9659],
            [0.9703, 0.6834]], device='cuda:0')

    # elementwise substruction
    >>> x - y
    tensor([[-0.4594,  0.5935],
            [ 0.4827,  0.6683]], device='cuda:0')

    # elementwise multiplication
    >>> x * y
    tensor([[0.1469, 0.1452],
            [0.1771, 0.0051]], device='cuda:0')

    # elementwise division
    >>> x / y
    tensor([[ 0.3209,  4.1880],
            [ 2.9796, 89.4011]], device='cuda:0')

    # matric multiplication
    >>> x @ y
    tensor([[0.3370, 0.0463],
            [0.6563, 0.1404]], device='cuda:0')

    # inplace addition
    >>> y.add_(x)
    tensor([[0.8937, 0.9659],
            [0.9703, 0.6834]], device='cuda:0')

    # inplace substruction
    >>> y.sub_(x)
    tensor([[0.6766, 0.1862],
            [0.2438, 0.0076]], device='cuda:0')

    # inplace multiplication
    >>> y.mul_(x)
    tensor([[0.1469, 0.1452],
            [0.1771, 0.0051]], device='cuda:0')

    # inplace division
    >>> y.div_(x)
    tensor([[0.6766, 0.1862],
            [0.2438, 0.0076]], device='cuda:0')


Gradient
--------

.. code-block:: python

    # create a tensor with gradient calculation requirement
    >>> x = torch.randn(3, requires_grad=True, device=0)
    >>> x
    tensor([-1.1442, -0.8709, -0.2581], device='cuda:0', requires_grad=True)

    # copy a tensor from an existing tensor without gradient calculation requirement
    >>> y = x.detach()
    >>> y
    tensor([-1.1442, -0.8709, -0.2581], device='cuda:0')

    # make x becomes a tensor without gradient calculation requirement
    >>> x.requires_grad_(False)
    tensor([-1.1442, -0.8709, -0.2581], device='cuda:0')

    # using a context manager to calculate a tensor without grad requirment
    >>> x = torch.randn(3, requires_grad=True, device=0)
    >>> with torch.no_grad():
    ...     y = x + 1
    ...     print(y)
    ...
    tensor([1.2969, 1.5251, 0.7915], device='cuda:0')

    # without the context manager, the output is
    >>> y = x + 1
    >>> print(y)
    tensor([1.2969, 1.5251, 0.7915], device='cuda:0', grad_fn=<AddBackward0>)

    # calculate a gradient
    >>> x = torch.randn(3, requires_grad=True)
    >>> y = x + 1
    >>> z = y * y * 3
    >>> z = z.mean()
    >>> z.backward() # dz/dx
    >>> print(f"gradient dz/dx: {x.grad}")
    gradient dz/dx: tensor([1.2036, 5.0103, 0.5143])
