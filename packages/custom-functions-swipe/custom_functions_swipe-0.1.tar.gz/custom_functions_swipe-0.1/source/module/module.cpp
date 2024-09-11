#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>
#include <Eigen/Dense>

namespace py = pybind11;
using Eigen::MatrixXd;
using Eigen::VectorXd;

// Function 1: Divide each row of the matrix by the corresponding diagonal value
py::array_t<double> divide_by_diagonal(py::array_t<double> arr) {
    auto buf = arr.request();
    if (buf.ndim != 2 || buf.shape[0] != buf.shape[1]) {
        throw std::runtime_error("Input should be a square 2D array");
    }

    // Create Eigen matrix from the numpy array
    MatrixXd mat = Eigen::Map<MatrixXd>(static_cast<double*>(buf.ptr), buf.shape[0], buf.shape[1]);

    // Get the diagonal values
    VectorXd diagonal_values = mat.diagonal().array() * -1;  // Invert sign

    // Divide each row by the corresponding diagonal value
    for (int i = 0; i < mat.rows(); ++i) {
        mat.row(i) /= diagonal_values(i);
    }

    // Return the result as numpy array
    return py::array_t<double>(py::buffer_info(
        mat.data(), sizeof(double), py::format_descriptor<double>::format(),
        2, { mat.rows(), mat.cols() }, { sizeof(double) * mat.cols(), sizeof(double) }));
}

// Function 2: Calculate loss based on base share, elasticity, new price, and base price
py::array_t<double> calculate_loss(py::array_t<double> base_share, py::array_t<double> elasticity,
    py::array_t<double> new_price, py::array_t<double> base_price) {
    auto base_buf = base_share.request(), elast_buf = elasticity.request(),
        new_buf = new_price.request(), base_buf2 = base_price.request();

    if (base_buf.ndim != 1 || elast_buf.ndim != 1 || new_buf.ndim != 1 || base_buf2.ndim != 1) {
        throw std::runtime_error("All inputs must be 1D arrays");
    }

    if (base_buf.shape[0] != elast_buf.shape[0] || base_buf.shape[0] != new_buf.shape[0] ||
        base_buf.shape[0] != base_buf2.shape[0]) {
        throw std::runtime_error("All input arrays must have the same length");
    }

    size_t n = base_buf.shape[0];
    VectorXd base = Eigen::Map<VectorXd>(static_cast<double*>(base_buf.ptr), n);
    VectorXd elast = Eigen::Map<VectorXd>(static_cast<double*>(elast_buf.ptr), n);
    VectorXd newp = Eigen::Map<VectorXd>(static_cast<double*>(new_buf.ptr), n);
    VectorXd basep = Eigen::Map<VectorXd>(static_cast<double*>(base_buf2.ptr), n);

    VectorXd loss = base.array() * elast.array() * (newp.array() / basep.array() - 1);
    loss = (basep.array() == newp.array()).select(0, loss);  // Set loss to 0 where base_price == new_price

    return py::array_t<double>(py::buffer_info(
        loss.data(), sizeof(double), py::format_descriptor<double>::format(),
        1, { loss.size() }, { sizeof(double) }));
}

// Function 3: Calculate model share based on base share, loss vector, and coefficient matrix
py::array_t<double> calculate_model_share(py::array_t<double> base_share, py::array_t<double> loss_vector,
    py::array_t<double> coefficient_matrix) {
    auto base_buf = base_share.request(), loss_buf = loss_vector.request(),
        coef_buf = coefficient_matrix.request();

    if (base_buf.ndim != 1 || loss_buf.ndim != 1 || coef_buf.ndim != 2) {
        throw std::runtime_error("base_share and loss_vector must be 1D, coefficient_matrix must be 2D");
    }

    if (coef_buf.shape[0] != coef_buf.shape[1] || coef_buf.shape[0] != base_buf.shape[0]) {
        throw std::runtime_error("Coefficient matrix must be square and match the size of the base_share vector");
    }

    size_t n = base_buf.shape[0];
    VectorXd base = Eigen::Map<VectorXd>(static_cast<double*>(base_buf.ptr), n);
    VectorXd loss = Eigen::Map<VectorXd>(static_cast<double*>(loss_buf.ptr), n);
    MatrixXd coef = Eigen::Map<MatrixXd>(static_cast<double*>(coef_buf.ptr), n, n);

    // Calculate sum_work_vector as negative product of coefficient matrix and loss vector
    VectorXd sum_work_vector = -coef * loss;

    // Calculate model share
    VectorXd model_share = base + sum_work_vector;

    return py::array_t<double>(py::buffer_info(
        model_share.data(), sizeof(double), py::format_descriptor<double>::format(),
        1, { model_share.size() }, { sizeof(double) }));
}

PYBIND11_MODULE(custom_functions, m) {
    m.def("divide_by_diagonal", &divide_by_diagonal, "Divides each row of the input array by its diagonal value");
    m.def("calculate_loss", &calculate_loss, "Calculate the loss for each SKU");
    m.def("calculate_model_share", &calculate_model_share, "Calculate the model share based on base share, loss vector, and coefficient matrix");
}
