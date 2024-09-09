#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "kdtree.hpp"
#include "kdtree_g.hpp"


#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)


namespace py = pybind11;

template <typename T, dim_t dims, bool use_gpu>
struct KDTree
{
    int levels;
    PartitionInfo<T, dims>* partition_info;
    PartitionInfoDevice<T, dims>* partition_info_d;

    //For repeated queries, local buffers will avoid reallocation of the necessary buffers
    /*T* dist_buf = NULL;
    point_i_t* knn_idx_buf = NULL;
    point_i_knn_t nr_nns_buf = 0;*/

    KDTree(const py::array_t<T, py::array::c_style | py::array::forcecast>& points_ref, const int levels)
    {
        const auto dims_arr = points_ref.shape(1);
        const T* points_raw = points_ref.data();
        const auto nr_points = points_ref.shape(0);

        {
            py::gil_scoped_release release;
            this->levels = levels;
            assert(dims_arr == dims);

            partition_info = new PartitionInfo<T, dims>(std::move(createKDTree<T, dims>(points_raw, nr_points, levels)));

            if (use_gpu)
            {
                partition_info_d = copyPartitionToGPU<T, dims>(*partition_info);
            }
        }
    }

    py::array_t<point_i_t> get_shuffled_inds() const
    {
        const auto shuffled_inds = partition_info->shuffled_inds;
        auto shuffled_inds_arr = py::array_t<point_i_t>(partition_info->nr_points, shuffled_inds);
        return std::move(shuffled_inds_arr);
    }

    py::array_t<T> get_structured_points() const
    {
        const auto structured_points = partition_info->structured_points;
        auto structured_points_arr = py::array_t<T>(partition_info->nr_points * dims, structured_points->data());
        structured_points_arr.resize(std::vector<ptrdiff_t>{ partition_info->nr_points, dims });
        return std::move(structured_points_arr);
    }

    void query_recast(const T* points_query, const size_t nr_query_points, const point_i_knn_t nr_nns_searches, T* dist_arr, point_i_knn_t* knn_idx)
    {
        {
            py::gil_scoped_release release;
            if (use_gpu)
            {
                KDTreeKNNGPUSearch<T, T, dims>(partition_info_d,
                    nr_query_points, reinterpret_cast<const std::array<T, dims>*>(points_query),
                    dist_arr, knn_idx, nr_nns_searches);
            }
            else
            {
                KDTreeKNNSearch<T, T, dims>(*partition_info,
                    nr_query_points, reinterpret_cast<const std::array<T, dims>*>(points_query),
                    dist_arr, knn_idx, nr_nns_searches);
            }
        }
    }

    void query(const size_t points_query_ptr, const size_t nr_query_points, const point_i_knn_t nr_nns_searches, const size_t dist_arr_ptr, const size_t knn_idx_ptr)
    {
        //Necessary for CUDA raw pointers being passed around. They can NOT be converted to a py::array_t
        T* points_query = reinterpret_cast<T*>(points_query_ptr);
        T* dist_arr = reinterpret_cast<T*>(dist_arr_ptr);
        point_i_knn_t* knn_idx = reinterpret_cast<point_i_knn_t*>(knn_idx_ptr);
        this->query_recast(points_query, nr_query_points, nr_nns_searches, dist_arr, knn_idx);
    }

    ~KDTree()
    {
        delete partition_info;

        if (use_gpu)
            freePartitionFromGPU(partition_info_d);
    }
};

#define KDTREE_INSTANTIATION(T, dims, use_gpu, name) (py::class_< KDTree<T, dims, use_gpu>, std::shared_ptr< KDTree<T, dims, use_gpu>>>(mod, name) \
                                                .def(py::init<py::array_t<T>, int>(), py::arg("points_ref"), py::arg("levels")) \
                                                .def("get_shuffled_inds", &KDTree<T, dims, use_gpu>::get_shuffled_inds, "Returns the shuffled indices to translate from local to global indices") \
                                                .def("get_structured_points", &KDTree<T, dims, use_gpu>::get_structured_points, "Returns the ordered points how they are used in the KD-Tree") \
                                                .def("query", &KDTree<T, dims, use_gpu>::query, py::arg("points_query_ptr"), py::arg("nr_query_points"), py::arg("nr_nns_searches"), \
                                                                                                py::arg("dist_arr_ptr"), py::arg("knn_idx_ptr")), \
                                                                                                "Queries the KNN from the KD-Tree and puts the results in the array pointed to by dist_arr_ptr and knn_idx_ptr")

bool check_for_gpu()
{
#ifdef GPU_AVAILABLE //Set inside CMake
    return true;
#else
    return false;
#endif
}

PYBIND11_MODULE(torch_knn, mod) {
    mod.doc() = R"pbdoc(
        This package implements the torch KD-Tree in C++/CUDA.
        -----------------------

        .. currentmodule:: torch_knn

        .. autosummary::
           :toctree: _generate

           KDTreeCPU3DF
           check_for_gpu
    )pbdoc";

    KDTREE_INSTANTIATION(float, 3, false, "KDTreeCPU3DF");
    KDTREE_INSTANTIATION(double, 3, false, "KDTreeCPU3D");
    KDTREE_INSTANTIATION(float, 3, true, "KDTreeGPU3DF");
    KDTREE_INSTANTIATION(double, 3, true, "KDTreeGPU3D");

    KDTREE_INSTANTIATION(float, 2, false, "KDTreeCPU2DF");
    KDTREE_INSTANTIATION(double, 2, false, "KDTreeCPU2D");
    KDTREE_INSTANTIATION(float, 2, true, "KDTreeGPU2DF");
    KDTREE_INSTANTIATION(double, 2, true, "KDTreeGPU2D");

    KDTREE_INSTANTIATION(float, 1, false, "KDTreeCPU1DF");
    KDTREE_INSTANTIATION(double, 1, false, "KDTreeCPU1D");
    KDTREE_INSTANTIATION(float, 1, true, "KDTreeGPU1DF");
    KDTREE_INSTANTIATION(double, 1, true, "KDTreeGPU1D");

    mod.def("check_for_gpu", &check_for_gpu, "Check if the library was compiled with GPU support");

#ifdef VERSION_INFO //Set by cmake
    mod.attr("__version__") = VERSION_INFO; //MACRO_STRINGIFY(VERSION_INFO);
#else
    mod.attr("__version__") = "dev";
#endif
}
