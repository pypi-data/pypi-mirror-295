# CUDA/Torch KD-Tree K-Nearest Neighbor Operator
This repository implements a KD-Tree on CUDA with an interface for [torch](https://pytorch.org/). It is a port of a previous implementation for tensorflow called [tf_kdtree](https://github.com/thomgrand/tf_kdtree).

The KD-Tree is always generated using the CPU, but is automatically transferred to the GPU for cupy operations there. The KD-Tree implementation will search the k nearest neighbors of each queried point in logarithmic time and is best suited for repeated nearest neighbor queries in a static point cloud.

The algorithms' dimensions are currently defined through template parameters and must be known at compile-time. The present version compiles the library for the dimensionalities 1, 2, 3. See [Compiling additional dimensions](#compiling-additional-dimensions) for instructions on how to compile additional dimensions.

# Usage Examples

```python
from torch_kdtree import build_kd_tree
import torch
from scipy.spatial import KDTree #Reference implementation
import numpy as np

#Dimensionality of the points and KD-Tree
d = 3

#Specify the device on which we will operate
#Currently only one GPU is supported
device = torch.device("cuda")

#Create some random point clouds
points_ref = torch.randn(size=(1000, d), dtype=torch.float32, device=device, requires_grad=True) * 1e3
points_query = torch.randn(size=(100, d), dtype=torch.float32, device=device, requires_grad=True) * 1e3

#Create the KD-Tree on the GPU and the reference implementation
torch_kdtree = build_kd_tree(points_ref)
kdtree = KDTree(points_ref.detach().cpu().numpy())

#Search for the 5 nearest neighbors of each point in points_query
k = 5
dists, inds = torch_kdtree.query(points_query, nr_nns_searches=k)
dists_ref, inds_ref = kdtree.query(points_query.detach().cpu().numpy(), k=k)

#Test for correctness 
#Note that the cupy_kdtree distances are squared
assert(np.all(inds.cpu().numpy() == inds_ref))
assert(np.allclose(torch.sqrt(dists).detach().cpu().numpy(), dists_ref, atol=1e-5))
```

We can also compute the gradient w.r.t. both point-clouds.

```python
(0.5 * torch.sum(dists)).backward()
grad = points_query.grad 
grad_comp = torch.sum((points_query[:, None] - points_ref[inds]), axis=-2)
print(torch.allclose(points_query.grad, grad_comp)) #Should print True
```

# Installation

Prerequisites
-------------
- Python
- Numpy (installed with `setuptools`)
- Torch (installed with `setuptools`)
- Cuda
- g++, or Visual Studio (MacOSX is untested)
- CMake

Build Instruction
-----------------
Clone the repository and fetch the submodule `pybind11`:
```bash
git clone https://github.com/thomgrand/torch_kdtree
cd torch_kdtree
git submodule init
git submodule update
```
The easiest way of installing the library is using `setuptools`:
```bash
pip install .
```


# Tests
After installation, you can run `python -m pytest .` inside the folder tests to verify that the library has been installed correctly.

# Benchmark

We compared the implementation to scipy.spatial.KDTree. Note that the benchmarks do not consider the time to build the KD-Trees, or the transfer to the GPU. Times greater than 1 second not shown.

Test Machine Specs: AMD Ryzen Threadripper 3970X 32x 3.7GHz, 128GB of working memory and a NVidia RTX 3090 GPU.

![alt text](benchmark.png "Benchmark")

To run the benchmark on your computer, simply run `python benchmark/benchmark.py`. This will create `benchmark_results.npz` that can be converted to a figure using `python benchmark/plot_benchmark.py` (will require `matplotlib`).

# Compiling additional dimensions

The dimension of the KD-Tree are compile time dynamic, meaning that the dimensions to be queried need to be known at compile time. By default, the library is compiled for d in [1, 2, 3]. You can add additional dimensions by adding new template dimensions to the pybind11 module in `interface.cpp` (line 115).

To add dimensionality 8 for example, you can add:
```cpp
    KDTREE_INSTANTIATION(float, 8, false, "KDTreeCPU8DF");
    KDTREE_INSTANTIATION(double, 8, false, "KDTreeCPU8D");
    KDTREE_INSTANTIATION(float, 8, true, "KDTreeGPU8DF");
    KDTREE_INSTANTIATION(double, 8, true, "KDTreeGPU8D");
```

This will instantiate the template functions for float and double types both on the CPU and GPU.

# Limitations

- No multi-GPU support
- Int32 KNN indexing inside the library
- Data must be cast to contiguous arrays before processing (automatically done by the library)
- No in-place updates of the KD-Tree. If you modify the point-cloud, you will have to create a new KD-Tree.


# Acknowledgements

If this works helps you in your research, please consider acknowledging the github repository, or citing our [paper](https://arxiv.org/abs/2102.09962) from which the library originated.

```bibtex
@article{grandits_geasi_2021,
	title = {{GEASI}: {Geodesic}-based earliest activation sites identification in cardiac models},
	volume = {37},
	issn = {2040-7947},
	shorttitle = {{GEASI}},
	url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/cnm.3505},
	doi = {10.1002/cnm.3505},
	language = {en},
	number = {8},
	urldate = {2021-08-12},
	journal = {International Journal for Numerical Methods in Biomedical Engineering},
	author = {Grandits, Thomas and Effland, Alexander and Pock, Thomas and Krause, Rolf and Plank, Gernot and Pezzuto, Simone},
	year = {2021},
	keywords = {eikonal equation, cardiac model personalization, earliest activation sites, Hamilton–Jacobi formulation, inverse ECG problem, topological gradient},
	pages = {e3505}
}
```

