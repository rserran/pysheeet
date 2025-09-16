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


High Dimension Arithmetic
-------------------------

.. code-block:: python

    >>> x = torch.randn(2,6,2,device=0)
    >>> x
    tensor([[[ 0.1108, -0.0072],
             [-0.0918,  0.4331],
             [-2.0041,  2.1245],
             [ 0.5664, -0.3363],
             [-0.1946,  0.5040],
             [-0.7781,  0.1323]],

            [[ 0.2827, -1.6136],
             [ 0.0897, -0.6297],
             [-0.6671,  1.1886],
             [-0.1337,  2.1926],
             [ 0.5211,  0.6389],
             [ 0.8101, -0.5091]]], device='cuda:0')

    # transpose x's dimension 1, 2
    >>> y = x.transpose(1,2)
    >>> y
    tensor([[[ 0.1108, -0.0918, -2.0041,  0.5664, -0.1946, -0.7781],
             [-0.0072,  0.4331,  2.1245, -0.3363,  0.5040,  0.1323]],

            [[ 0.2827,  0.0897, -0.6671, -0.1337,  0.5211,  0.8101],
             [-1.6136, -0.6297,  1.1886,  2.1926,  0.6389, -0.5091]]],
           device='cuda:0')
    >>> y.shape
    torch.Size([2, 2, 6])

    # high dimension inner product
    >>> x = torch.randn(1,2,3,4, device=0)
    >>> x
    tensor([[[[-0.2240,  0.3207,  0.0817,  0.9671],
              [ 1.3949,  0.2266,  0.6324,  0.0746],
              [ 2.0433, -1.0169,  0.3889, -0.7569]],

             [[-0.7897, -1.2480, -0.4675,  0.9220],
              [ 0.0690, -0.0351, -0.1109, -0.3753],
              [-1.1731,  0.9441,  0.8360,  0.1407]]]], device='cuda:0')
    >>> x @ x.transpose(2,3)
    tensor([[[[ 1.0950, -0.1160, -1.4840],
              [-0.1160,  2.4025,  2.8093],
              [-1.4840,  2.8093,  5.9335]],

             [[ 3.2498, -0.3049, -0.5129],
              [-0.3049,  0.1591, -0.2596],
              [-0.5129, -0.2596,  2.9863]]]], device='cuda:0')

Slicing
-------

.. code-block:: python

    >>> x = torch.randn(2, 3, device=0)
    >>> x
    tensor([[-1.3921,  0.0475,  0.7571],
            [-0.1469, -0.3882,  0.2149]], device='cuda:0')

    # get all rows  of column 1
    >>> x[:, 1]
    tensor([ 0.0475, -0.3882], device='cuda:0')

    # get all columns of raw 1
    >>> x[1, :]
    tensor([-0.1469, -0.3882,  0.2149], device='cuda:0')

    # get scale
    >>> x[1,1].item()
    -0.3882044851779938
    >>> x[1][1].item()
    -0.3882044851779938

    # get x[0-3,0-3]
    >>> x = torch.triu(torch.ones(5, 5))
    >>> x
    tensor([[1., 1., 1., 1., 1.],
            [0., 1., 1., 1., 1.],
            [0., 0., 1., 1., 1.],
            [0., 0., 0., 1., 1.],
            [0., 0., 0., 0., 1.]])
    >>> x[:3,:3]
    tensor([[1., 1., 1.],
            [0., 1., 1.],
            [0., 0., 1.]])

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
