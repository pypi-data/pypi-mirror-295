#include <Python.h>
#include <stdint.h>
#include <stdbool.h>
#include <numpy/arrayobject.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>

#include "incstatspy.h"
#include "incstats.h"

#define PY_SSIZE_T_CLEAN


typedef struct input_args {
  PyArrayObject *data;
  PyArrayObject *buffer;
  PyArrayObject *weights;
  double scalar_weight;
  double scalar_data;
  double *internal_buffer;
  int axis;
  bool input_is_scalar;
  char **kwlist;
  int n_dim_data;
  int n_dim_weights;
  int n_dim_buffer;
  npy_intp *dimensions_data;
  npy_intp *dimensions_weights;
  npy_intp *dimensions_buffer;
  npy_intp length_buffer;
  bool parse_p;
  int p;
  bool standardize;
  bool is_min_or_max;
} input_args_container;


inline static bool increment(npy_intp *idx, npy_intp *n_dims, size_t dims) {
  for (size_t i = 0; i < dims; ++i) {
      if (++idx[i] < n_dims[i]) {
          return false;
      }
      idx[i] = 0;
  }
  return true;
}

inline static bool increment_ignore_axis(npy_intp *idx, npy_intp *n_dims, 
size_t dims, int axis) {
  for (size_t i = 0; i < dims; i++) {
    if (i == axis) {
      continue;
    }

    if (++idx[i] < n_dims[i]) {
      return false;
    }

    idx[i] = 0;
  }

  return true;
}

inline static double *slice_axis(PyArrayObject *obj, npy_intp *pos,
npy_intp *n_dims, size_t dims, int axis, bool *done) {
  double *d_ptr = NULL;
  if(pos[axis] < n_dims[axis]) {
    d_ptr = PyArray_GetPtr(obj, pos);
    pos[axis]++;
  }
  if(pos[axis] == n_dims[axis]) {
    pos[axis] = 0;
    *done = true;
  }
  return d_ptr;
}

static int is_float64(PyObject *obj) {
    // Check if the object is a NumPy array
    if (PyArray_Check(obj)) {
        // Get the type of the array
        int type = PyArray_TYPE((PyArrayObject *)obj);
        // Check if the type is NPY_FLOAT64
        return type == NPY_FLOAT64;
    }
    return 0;
}

static int is_python_float(PyObject *obj) {
  return PyFloat_Check(obj);
}

static int parse_input(PyObject *args, PyObject* kwargs, 
input_args_container *input_args) {
  PyObject *object_raw_data = NULL;
  PyObject *object_raw_weights = NULL;
  PyObject *object_raw_buffer = NULL;
  PyArrayObject *array_float64 = NULL;
  PyArray_Descr *descr = NULL;

  if(input_args->is_min_or_max) {
    if(!PyArg_ParseTupleAndKeywords(args, kwargs, "O|iO", input_args->kwlist, 
    &object_raw_data, &(input_args->axis), &object_raw_buffer)) {
      goto cleanup_error;
    }
  }
  else if(!input_args->parse_p) {
    if(!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OiO", input_args->kwlist, 
    &object_raw_data, &object_raw_weights, &(input_args->axis),
    &object_raw_buffer)) {
      goto cleanup_error;
    }
  }
  else {
    if(!PyArg_ParseTupleAndKeywords(args, kwargs, "Oi|OiOp", input_args->kwlist, 
      &object_raw_data, &input_args->p, &object_raw_weights, &(input_args->axis),
      &object_raw_buffer, &input_args->standardize)) {
        goto cleanup_error;
    }
     input_args->length_buffer = input_args->p + 1 >= 2 ? input_args->p + 1 : 2;
  }
  
  if(object_raw_buffer == Py_None) {
    object_raw_buffer = NULL;
  }

  if(object_raw_data == Py_None) {
    object_raw_data = NULL;
  }

  if(object_raw_weights == Py_None) {
    object_raw_weights = NULL;
  }

  if(input_args->parse_p && input_args->p < 0) {
      PyErr_SetString(PyExc_TypeError, 
      "p must be non negative");
      goto cleanup_error;
  }

  if(!PyArray_Check(object_raw_data)) {
    if(!PyArray_IsAnyScalar(object_raw_data)) {
      PyErr_SetString(PyExc_TypeError, 
      "Argument 1 is not a ndarray or scalar");
      goto cleanup_error;
    }
  }

  if(object_raw_weights != NULL) {
    if(!PyArray_Check(object_raw_weights)) {
      if(!PyArray_IsAnyScalar(object_raw_weights)) {
        PyErr_SetString(PyExc_TypeError, 
        "Argument 2 is not a ndarray or scalar");
        return -1;
      }
    }
  }
  
  if(object_raw_buffer != NULL) {
    if(!PyArray_Check(object_raw_buffer)) {
      PyErr_SetString(PyExc_TypeError, "Argument 3 is not a ndarray");
      return -1;
    }
  }

  if(!PyArray_CheckScalar(object_raw_data) && 
  !PyArray_IsPythonNumber(object_raw_data)) {
    input_args->data = (PyArrayObject *)
    PyArray_FromAny(object_raw_data, NULL, 0, 0, NPY_ARRAY_ALIGNED, NULL);
    if(input_args->data == NULL) {
        PyErr_SetString(PyExc_TypeError,
        "Couldn't convert ndarray");
      goto cleanup_error;
    }
    // Try to convert to float64.
    if(!is_float64((PyObject *)input_args->data)) {
      descr = PyArray_DescrFromType(NPY_FLOAT64);
      if(descr == NULL) {
        goto cleanup_error;
      }
      array_float64 = (PyArrayObject *)PyArray_CastToType(input_args->data, descr, 0);
      Py_XDECREF(input_args->data);
      input_args->data = array_float64;

      if(array_float64 == NULL) {
         PyErr_SetString(PyExc_TypeError, "Couldn't convert to float64");
          goto cleanup_error;
      }
    }
    input_args->n_dim_data = PyArray_NDIM(input_args->data);
  }
  else {
    input_args->input_is_scalar = true;
    if(is_python_float(object_raw_data)) {
      input_args->scalar_data = PyFloat_AsDouble(object_raw_data);
    }
    else if(PyLong_Check(object_raw_data)) {
      input_args->scalar_data = PyLong_AsLong(object_raw_data);
    }
    else {
      input_args->data = (PyArrayObject *)
      PyArray_FromAny(object_raw_data, NULL, 0, 0, NPY_ARRAY_ALIGNED, NULL);
      if(input_args->data == NULL) {
        PyErr_SetString(PyExc_TypeError,
        "Couldn't convert to ndarray");
        goto cleanup_error;
      }
      if(!is_float64((PyObject *) input_args->data)) {
        descr = PyArray_DescrFromType(NPY_FLOAT64);
        if(descr == NULL) {
          goto cleanup_error;
        }
        array_float64 = (PyArrayObject *)PyArray_CastToType(input_args->data, descr, 0);
        Py_XDECREF(input_args->data);
        input_args->data = array_float64;

        if(array_float64 == NULL) {
          PyErr_SetString(PyExc_TypeError, "Couldn't convert to float64");
            goto cleanup_error;
        }
      }
      input_args->scalar_data = *(double*)PyArray_DATA(input_args->data);
    }
  }

  if(object_raw_weights != NULL) {
    if(!PyArray_IsAnyScalar(object_raw_weights) && 
    !PyArray_IsPythonNumber(object_raw_weights)) {
      input_args->weights = (PyArrayObject *)
      PyArray_FromAny(object_raw_weights, NULL, 0, 0, NPY_ARRAY_ALIGNED, NULL);
      if(input_args->weights == NULL) {
        PyErr_SetString(PyExc_TypeError,
        "Couldn't convert ndarray");
        goto cleanup_error;
      }
      if(!is_float64((PyObject *)input_args->weights)) {
        descr = PyArray_DescrFromType(NPY_FLOAT64);
        if(descr == NULL) {
          goto cleanup_error;
        }
        array_float64 = (PyArrayObject *)PyArray_CastToType(input_args->weights, descr, 0);
        Py_XDECREF(input_args->weights);
        input_args->weights = array_float64;

        if(array_float64 == NULL) {
          PyErr_SetString(PyExc_TypeError, "Couldn't convert to float64");
            goto cleanup_error;
        }
      }
      input_args->n_dim_weights = PyArray_NDIM(input_args->weights);
      if(input_args->input_is_scalar) {
        PyErr_SetString(PyExc_TypeError, 
        "Argument 1 is scalar while argument 2 is not");
        goto cleanup_error;
      }
    }
    else {
      if(!input_args->input_is_scalar) {
        PyErr_SetString(PyExc_TypeError, 
        "Argument 2 is scalar while argument 1 is not");
        goto cleanup_error;
      }
      if(is_python_float(object_raw_data)) {
        input_args->scalar_weight = PyFloat_AsDouble(object_raw_weights);
      }
      else if(PyLong_Check(object_raw_data)) {
        input_args->scalar_weight = PyLong_AsLong(object_raw_weights);
      }
      else {
        input_args->weights = (PyArrayObject *)
        PyArray_FromAny(object_raw_weights, NULL, 0, 0, NPY_ARRAY_ALIGNED, NULL);
        if(input_args->weights == NULL) {
            PyErr_SetString(PyExc_TypeError,
            "Couldn't convert ndarray");
            goto cleanup_error;
        }
        if(!is_float64((PyObject *) input_args->weights)) {
          descr = PyArray_DescrFromType(NPY_FLOAT64);
          if(descr == NULL) {
            goto cleanup_error;
          }
          array_float64 = (PyArrayObject *)PyArray_CastToType(input_args->weights, descr, 0);
          Py_XDECREF(input_args->weights);
          input_args->weights = array_float64;

          if(array_float64 == NULL) {
            PyErr_SetString(PyExc_TypeError, "Couldn't convert to float64");
              goto cleanup_error;
          }
        }
        input_args->scalar_weight = *(double*)PyArray_DATA(input_args->weights);
      }
    }
  }

  if(object_raw_weights != NULL) {
    if(input_args->n_dim_data != input_args->n_dim_weights) {
      PyErr_SetString(PyExc_TypeError, 
      "Argument 1 and argument 2 don't have the same number of dimensions");
      goto cleanup_error;
    }
  }

  if(object_raw_buffer != NULL) {
    input_args->buffer = (PyArrayObject *)
    PyArray_FromAny(object_raw_buffer, NULL, 0, 0, 
    NPY_ARRAY_ALIGNED | NPY_ARRAY_WRITEABLE, NULL);     
  }

  if(object_raw_buffer != NULL) {
    input_args->n_dim_buffer = PyArray_NDIM(input_args->buffer);
  }

  if((input_args->axis < 0 || (input_args->axis >= input_args->n_dim_data)
  && !input_args->input_is_scalar)) {
    PyErr_SetString(PyExc_TypeError, 
    "Axis must be non negative and within the dimensions of array");
    goto cleanup_error;
  }
  if(input_args->input_is_scalar) {
    input_args->axis = 0;
  }
  if(object_raw_buffer != NULL) {
    if(input_args->n_dim_buffer != 1) {
      PyErr_SetString(PyExc_TypeError, 
      "Fourth argument is expected to be 1-dimensional");
      goto cleanup_error;
    }
  }

  if(!input_args->input_is_scalar) {
    input_args->dimensions_data = PyArray_DIMS(input_args->data);
    for(size_t i = 0; i < input_args->n_dim_data; i++) {
      if(input_args->dimensions_data[i] == 0) {
        PyErr_SetString(PyExc_TypeError, 
        "Dimensions can't be 0");
        printf("TEST\n");
        goto cleanup_error;
      }
    }
  }
  
  if(object_raw_weights != NULL) {
    if(!input_args->input_is_scalar) {
      input_args->dimensions_weights = PyArray_DIMS(input_args->weights);
    }
    for(size_t i = 0; i < input_args->n_dim_data; i++) {
      if(input_args->dimensions_weights[i] != input_args->dimensions_data[i]) {
        PyErr_SetString(PyExc_TypeError, 
        "Dimensions of argument 1 and argument 2 are not matching!");
        goto cleanup_error;
      }
    }
  }
  
  if(input_args->buffer != NULL) {
    input_args->dimensions_buffer = PyArray_DIMS(input_args->buffer);
  }

  for(int i = 0; i < input_args->n_dim_data; i++) {
    if(i != input_args->axis) {
      input_args->length_buffer *= 
      (input_args->dimensions_data[i] > 0 ? input_args->dimensions_data[i] : 1);
    }
  }

  if(input_args->buffer != (PyArrayObject *)NULL) {
    if(input_args->dimensions_buffer[0] != input_args->length_buffer) {
      PyErr_SetString(PyExc_TypeError, 
      "Fourth argument has wrong length.");
      goto cleanup_error;
    }
  }
  
  input_args->internal_buffer = calloc(input_args->length_buffer, 
  sizeof(double));
  if(input_args->internal_buffer == NULL) {
     PyErr_SetString(PyExc_TypeError, 
     "Couldn't allocate memory for the internal buffer.");
    goto cleanup_error;
  }
  
  if(input_args->buffer != NULL) {
    for(int i = 0; i < input_args->length_buffer; i++) {
      input_args->internal_buffer[i] = 
      *(double *) PyArray_GETPTR1(input_args->buffer, i);
    }
  }

  return 0;
  cleanup_error:
  Py_XDECREF(input_args->data);
  Py_XDECREF(input_args->weights);
  Py_XDECREF(input_args->buffer);
  free(input_args->internal_buffer);
  input_args->data = NULL;
  input_args->weights = NULL;
  input_args->buffer = NULL;
  input_args->internal_buffer = NULL;
  return -1;
}

PyObject *mean(PyObject *self, PyObject *args, PyObject* kwargs)
{
  static char *kwlist[] = {"input", "weights", "axis", "buffer", NULL};
  const int initial_buffer_length = 2;
  input_args_container input_args;
  input_args.data = NULL;
  input_args.buffer = NULL;
  input_args.weights = NULL;
  input_args.scalar_weight = 1.0;
  input_args.scalar_data = 0.0;
  input_args.internal_buffer = NULL;
  input_args.axis = 0;
  input_args.input_is_scalar = false;
  input_args.kwlist = kwlist;
  input_args.n_dim_data = 0;
  input_args.n_dim_weights = 0;
  input_args.n_dim_buffer = -1;
  input_args.dimensions_data = NULL;
  input_args.dimensions_weights = NULL;
  input_args.dimensions_buffer = NULL;
  input_args.length_buffer = initial_buffer_length;
  input_args.parse_p = false;
  input_args.p = -1;
  input_args.is_min_or_max = false;
  bool done = false;
  double *buffer_ptr = NULL;
  PyArrayObject *array_mean = NULL;
  npy_intp *output_dims = NULL;
  PyObject *tuple = NULL;
  npy_intp *pos = NULL;
  
  if(parse_input(args, kwargs, &input_args) == -1) {
    goto cleanup_error;
  }
  

  pos = calloc(input_args.n_dim_data, sizeof(npy_intp));
  if(pos == NULL && input_args.n_dim_data > 0) {
    PyErr_SetString(PyExc_TypeError, 
    "Couldn't allocate memory for index structure.");
    goto cleanup_error;
  }

  buffer_ptr = &input_args.internal_buffer[0];
  if(input_args.n_dim_data == 0) {
    incstats_mean(input_args.scalar_data, input_args.scalar_weight, buffer_ptr);
  }
  else {
    do { 
      done = false;
      while(!done) {
        double weight = 1.0;
        if((PyObject *)input_args.weights != NULL) {
          weight = *(double *)PyArray_GetPtr(input_args.weights, pos);
        }
        double val = *slice_axis(input_args.data, pos, 
        input_args.dimensions_data, input_args.n_dim_data, input_args.axis,
        &done);
        incstats_mean(val, weight, buffer_ptr);
      }
      buffer_ptr += 2;
    } while(!increment_ignore_axis(pos, input_args.dimensions_data, 
    input_args.n_dim_data, input_args.axis));
  }

  if(input_args.n_dim_data > 1) {
    output_dims = malloc(sizeof(npy_intp) * (input_args.n_dim_data - 1));
    if(output_dims == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
    int k = 0;
    for(int i = 0; i < input_args.n_dim_data; i++) {
      if(i != input_args.axis) {
        output_dims[k++] = input_args.dimensions_data[i];
      }
    }
    array_mean = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    if((PyObject *)array_mean == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
  
    free(pos);
    pos = calloc((input_args.n_dim_data - 1), sizeof(npy_intp));
    if(pos == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for index structure.");
      goto cleanup_error;
    }

    buffer_ptr = &input_args.internal_buffer[0];
    do { 
      double result = 0;
      incstats_mean_finalize(&result, buffer_ptr);
      buffer_ptr += 2;
      double *val = PyArray_GetPtr(array_mean, pos);
      *val = result;
    } while(!increment(pos, output_dims, input_args.n_dim_data - 1));
    
  }
  else {
    array_mean = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    if((PyObject *)array_mean == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
     goto cleanup_error;
    }
    buffer_ptr = &input_args.internal_buffer[0];
    double result = 0;
    incstats_mean_finalize(&result, buffer_ptr);
    double *ptr = (double*)PyArray_DATA(array_mean);
    *ptr = result;
  }

  // Create external buffer if it doesn't exist yet.
  if((PyObject *)input_args.buffer == NULL) {
   input_args.buffer = (PyArrayObject *) 
   PyArray_SimpleNew(1, &input_args.length_buffer, NPY_DOUBLE);
    if((PyObject *)array_mean == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for external buffer.");
      goto cleanup_error;
    }
  }
  
  for(int i = 0; i < input_args.length_buffer; i++) {
    double *ptr = PyArray_GETPTR1(input_args.buffer, i);
    *ptr = input_args.internal_buffer[i];
  }

  tuple = PyTuple_New(2);
  if(!tuple) {
    goto cleanup_error;
  }
  PyTuple_SetItem(tuple, 0, (PyObject *)array_mean);
  PyTuple_SetItem(tuple, 1, (PyObject *)input_args.buffer);
  
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  return tuple;

  cleanup_error:
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  Py_XDECREF(array_mean);
  Py_XDECREF(input_args.buffer);
  Py_XDECREF(tuple);
  return NULL;
}

PyObject *variance(PyObject *self, PyObject *args, PyObject* kwargs)
{
  static char *kwlist[] = {"input", "weights", "axis", "buffer", NULL};
  const int initial_buffer_length = 3;
  input_args_container input_args;
  input_args.data = (PyArrayObject *)NULL;
  input_args.buffer = (PyArrayObject *)NULL;
  input_args.weights = (PyArrayObject *)NULL;
  input_args.scalar_weight = 1.0;
  input_args.scalar_data = 0.0;
  input_args.internal_buffer = NULL;
  input_args.axis = 0;
  input_args.input_is_scalar = false;
  input_args.kwlist = kwlist;
  input_args.n_dim_data = 0;
  input_args.n_dim_weights = 0;
  input_args.n_dim_buffer = -1;
  input_args.dimensions_data = NULL;
  input_args.dimensions_weights = NULL;
  input_args.dimensions_buffer = NULL;
  input_args.length_buffer = initial_buffer_length;
  input_args.parse_p = false;
  input_args.p = -1;
  input_args.is_min_or_max = false;
  bool done = false;
  double *buffer_ptr = NULL;
  PyArrayObject *array_mean = (PyArrayObject *) NULL;
  PyArrayObject *array_variance = (PyArrayObject *) NULL;
  npy_intp *output_dims = NULL;
  PyObject *tuple = NULL;
  npy_intp *pos = NULL;

  if(parse_input(args, kwargs, &input_args) == -1) {
    goto cleanup_error;
  }

  pos = calloc(input_args.n_dim_data, sizeof(npy_intp));
  if(pos == NULL && input_args.n_dim_data > 0) {
    PyErr_SetString(PyExc_TypeError, 
    "Couldn't allocate memory for index structure.");
    goto cleanup_error;
  }

  buffer_ptr = &input_args.internal_buffer[0];
  if(input_args.n_dim_data == 0) {
    incstats_variance(input_args.scalar_data, input_args.scalar_weight, buffer_ptr);
  }
  else {
    do { 
      done = false;
      while(!done) {
        double weight = 1.0;
        if((PyObject *)input_args.weights != NULL) {
          weight = *(double *)PyArray_GetPtr(input_args.weights, pos);
        }
        double val = *slice_axis(input_args.data, pos, 
        input_args.dimensions_data, input_args.n_dim_data, input_args.axis,
        &done);
        incstats_variance(val, weight, buffer_ptr);
      }
      buffer_ptr += 3;
    } while(!increment_ignore_axis(pos, input_args.dimensions_data, 
    input_args.n_dim_data, input_args.axis));
  }
  
  if(input_args.n_dim_data > 1) {
    output_dims = malloc(sizeof(npy_intp) * (input_args.n_dim_data - 1));
    if(output_dims == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
    int k = 0;
    for(int i = 0; i < input_args.n_dim_data; i++) {
      if(i != input_args.axis) {
        output_dims[k++] = input_args.dimensions_data[i];
      }
    }
    array_mean = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    array_variance = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    if((PyObject *)array_mean == NULL || (PyObject *)array_variance == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
  
    free(pos);
    pos = calloc((input_args.n_dim_data - 1), sizeof(npy_intp));
    if(pos == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for index structure.");
      goto cleanup_error;
    }

    buffer_ptr = &input_args.internal_buffer[0];
    do { 
      double result[2] = {0};
      incstats_variance_finalize(result, buffer_ptr);
      buffer_ptr += 3;
      double *val = PyArray_GetPtr(array_mean, pos);
      *val = result[0];
      val = PyArray_GetPtr(array_variance, pos);
      *val = result[1];
    } while(!increment(pos, output_dims, input_args.n_dim_data - 1)); 
    
  }
  else {
    array_mean = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    array_variance = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    if((PyObject *)array_mean == NULL || (PyObject *)array_variance == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
    buffer_ptr = &input_args.internal_buffer[0];
    double result[2] = {0};
    incstats_variance_finalize(result, buffer_ptr);
    double *ptr = (double*)PyArray_DATA(array_mean);
    *ptr = result[0];
    ptr = (double*)PyArray_DATA(array_variance);
    *ptr = result[1];
  }

  // Create external buffer if it doesn't exist yet.
  if((PyObject *)input_args.buffer == NULL) {
    input_args.buffer = (PyArrayObject *) PyArray_SimpleNew(1, 
    &input_args.length_buffer, NPY_DOUBLE);
    if((PyObject *)input_args.buffer == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for external buffer.");
     goto cleanup_error;
    }
  }
  
  for(int i = 0; i < input_args.length_buffer; i++) {
    double *ptr = PyArray_GETPTR1(input_args.buffer, i);
    *ptr = input_args.internal_buffer[i];
  }
  
  tuple = PyTuple_New(3);
  if(!tuple) {
    goto cleanup_error;
  }
  PyTuple_SetItem(tuple, 0, (PyObject *)array_mean);
  PyTuple_SetItem(tuple, 1, (PyObject *)array_variance);
  PyTuple_SetItem(tuple, 2, (PyObject *)input_args.buffer);
  
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  return tuple;

  cleanup_error:
  free(pos);
  //free(input_args.internal_buffer);
  //free(output_dims);
  //Py_XDECREF(input_args.data);
  //Py_XDECREF(input_args.weights);
  //Py_XDECREF(array_mean);
  //Py_XDECREF(array_variance);
  //Py_XDECREF(input_args.buffer);
  //Py_XDECREF(tuple);
  return NULL;
}

PyObject *skewness(PyObject *self, PyObject *args, PyObject* kwargs)
{
  static char *kwlist[] = {"input", "weights", "axis", "buffer", NULL};
  const int initial_buffer_length = 4;
  input_args_container input_args;
  input_args.data = (PyArrayObject *)NULL;
  input_args.buffer = (PyArrayObject *)NULL;
  input_args.weights = (PyArrayObject *)NULL;
  input_args.scalar_weight = 1.0;
  input_args.scalar_data = 0.0;
  input_args.internal_buffer = NULL;
  input_args.axis = 0;
  input_args.input_is_scalar = false;
  input_args.kwlist = kwlist;
  input_args.n_dim_data = 0;
  input_args.n_dim_weights = 0;
  input_args.n_dim_buffer = -1;
  input_args.dimensions_data = NULL;
  input_args.dimensions_weights = NULL;
  input_args.dimensions_buffer = NULL;
  input_args.length_buffer = initial_buffer_length;
  input_args.parse_p = false;
  input_args.p = -1;
  input_args.is_min_or_max = false;
  bool done = false;
  double *buffer_ptr = NULL;
  PyArrayObject *array_mean = (PyArrayObject *) NULL;
  PyArrayObject *array_variance = (PyArrayObject *) NULL;
  PyArrayObject *array_skewness = (PyArrayObject *) NULL;
  npy_intp *output_dims = NULL;
  PyObject *tuple = NULL;
  npy_intp *pos = NULL;

  if(parse_input(args, kwargs, &input_args) == -1) {
    goto cleanup_error;
  }

  pos = calloc(input_args.n_dim_data, sizeof(npy_intp));
  if(pos == NULL && input_args.n_dim_data > 0) {
    PyErr_SetString(PyExc_TypeError, 
    "Couldn't allocate memory for index structure.");
    goto cleanup_error;
  }

  buffer_ptr = &input_args.internal_buffer[0];
  if(input_args.n_dim_data == 0) {
    incstats_skewness(input_args.scalar_data, input_args.scalar_weight, buffer_ptr);
  }
  else {
    do { 
      done = false;
      while(!done) {
        double weight = 1.0;
        if((PyObject *)input_args.weights != NULL) {
          weight = *(double *)PyArray_GetPtr(input_args.weights, pos);
        }
        double val = *slice_axis(input_args.data, pos, 
        input_args.dimensions_data, input_args.n_dim_data, input_args.axis,
        &done);
        incstats_skewness(val, weight, buffer_ptr);
      }
      buffer_ptr += 4;
    } while(!increment_ignore_axis(pos, input_args.dimensions_data, 
    input_args.n_dim_data, input_args.axis));
  }
  
  if(input_args.n_dim_data > 1) {
    output_dims = malloc(sizeof(npy_intp) * (input_args.n_dim_data - 1));
    if(output_dims == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
    int k = 0;
    for(int i = 0; i < input_args.n_dim_data; i++) {
      if(i != input_args.axis) {
        output_dims[k++] = input_args.dimensions_data[i];
      }
    }
    array_mean = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    array_variance = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    array_skewness = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    if((PyObject *)array_mean == NULL || (PyObject *)array_variance ==
    NULL || (PyObject *)array_skewness == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
  
    free(pos);
    pos = calloc((input_args.n_dim_data - 1), sizeof(npy_intp));
    if(pos == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for index structure.");
      goto cleanup_error;
    }

    buffer_ptr = &input_args.internal_buffer[0];
    do { 
      double result[3] = {0};
      incstats_skewness_finalize(result, buffer_ptr);
      buffer_ptr += 4;
      double *val = PyArray_GetPtr(array_mean, pos);
      *val = result[0];
      val = PyArray_GetPtr(array_variance, pos);
      *val = result[1];
      val = PyArray_GetPtr(array_skewness, pos);
      *val = result[2];
    } while(!increment(pos, output_dims, input_args.n_dim_data - 1)); 
    
  }
  else {
    array_mean = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    array_variance = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    array_skewness = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    if((PyObject *)array_mean == NULL || (PyObject *)array_variance == 
    NULL || (PyObject *)array_skewness == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
    buffer_ptr = &input_args.internal_buffer[0];
    double result[3] = {0};
    incstats_skewness_finalize(result, buffer_ptr);
    double *ptr = (double*)PyArray_DATA(array_mean);
    *ptr = result[0];
    ptr = (double*)PyArray_DATA(array_variance);
    *ptr = result[1];
    ptr = (double*)PyArray_DATA(array_skewness);
    *ptr = result[2];
  }

  // Create external buffer if it doesn't exist yet.
  if((PyObject *)input_args.buffer == NULL) {
    input_args.buffer = (PyArrayObject *) PyArray_SimpleNew(1, 
    &input_args.length_buffer, NPY_DOUBLE);
    if((PyObject *)input_args.buffer == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for external buffer.");
      goto cleanup_error;
    }
  }
  
  for(int i = 0; i < input_args.length_buffer; i++) {
    double *ptr = PyArray_GETPTR1(input_args.buffer, i);
    *ptr = input_args.internal_buffer[i];
  }

  tuple = PyTuple_New(4);
  if(!tuple) {
    goto cleanup_error;
  }
  PyTuple_SetItem(tuple, 0, (PyObject *)array_mean);
  PyTuple_SetItem(tuple, 1, (PyObject *)array_variance);
  PyTuple_SetItem(tuple, 2, (PyObject *)array_skewness);
  PyTuple_SetItem(tuple, 3, (PyObject *)input_args.buffer);
  
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  return tuple;

  cleanup_error:
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  Py_XDECREF(array_mean);
  Py_XDECREF(array_variance);
  Py_XDECREF(array_skewness);
  Py_XDECREF(input_args.buffer);
  Py_XDECREF(tuple);
  return NULL;
}

PyObject *kurtosis(PyObject *self, PyObject *args, PyObject* kwargs)
{
  static char *kwlist[] = {"input", "weights", "axis", "buffer", NULL};
  const int initial_buffer_length = 5;
  input_args_container input_args;
  input_args.data = (PyArrayObject *)NULL;
  input_args.buffer = (PyArrayObject *)NULL;
  input_args.weights = (PyArrayObject *)NULL;
  input_args.scalar_weight = 1.0;
  input_args.scalar_data = 0.0;
  input_args.internal_buffer = NULL;
  input_args.axis = 0;
  input_args.input_is_scalar = false;
  input_args.kwlist = kwlist;
  input_args.n_dim_data = 0;
  input_args.n_dim_weights = 0;
  input_args.n_dim_buffer = -1;
  input_args.dimensions_data = NULL;
  input_args.dimensions_weights = NULL;
  input_args.dimensions_buffer = NULL;
  input_args.length_buffer = initial_buffer_length;
  input_args.parse_p = false;
  input_args.p = -1;
  input_args.is_min_or_max = false;
  bool done = false;
  double *buffer_ptr = NULL;
  PyArrayObject *array_mean = (PyArrayObject *) NULL;
  PyArrayObject *array_variance = (PyArrayObject *) NULL;
  PyArrayObject *array_skewness = (PyArrayObject *) NULL;
  PyArrayObject *array_kurtosis = (PyArrayObject *) NULL;
  npy_intp *output_dims = NULL;
  PyObject *tuple = NULL;
  npy_intp *pos = NULL;

  if(parse_input(args, kwargs, &input_args) == -1) {
    goto cleanup_error;
  }

  pos = calloc(input_args.n_dim_data, sizeof(npy_intp));
  if(pos == NULL && input_args.n_dim_data > 0) {
    PyErr_SetString(PyExc_TypeError, 
    "Couldn't allocate memory for index structure.");
    goto cleanup_error;
  }

  buffer_ptr = &input_args.internal_buffer[0];
  if(input_args.n_dim_data == 0) {
    incstats_kurtosis(input_args.scalar_data, input_args.scalar_weight, buffer_ptr);
  }
  else {
    do { 
      done = false;
      while(!done) {
        double weight = 1.0;
        if((PyObject *)input_args.weights != NULL) {
          weight = *(double *)PyArray_GetPtr(input_args.weights, pos);
        }
        double val = *slice_axis(input_args.data, pos, 
        input_args.dimensions_data, input_args.n_dim_data, input_args.axis,
        &done);
        incstats_kurtosis(val, weight, buffer_ptr);
      }
      buffer_ptr += 5;
    } while(!increment_ignore_axis(pos, input_args.dimensions_data, 
    input_args.n_dim_data, input_args.axis));
  }
  
  if(input_args.n_dim_data > 1) {
    output_dims = malloc(sizeof(npy_intp) * (input_args.n_dim_data - 1));
    if(output_dims == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
    int k = 0;
    for(int i = 0; i < input_args.n_dim_data; i++) {
      if(i != input_args.axis) {
        output_dims[k++] = input_args.dimensions_data[i];
      }
    }
    array_mean = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    array_variance = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    array_skewness = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    array_kurtosis = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    if((PyObject *)array_mean == NULL || (PyObject *)array_variance ==
    NULL || (PyObject *)array_skewness == NULL || 
    (PyObject *)array_kurtosis == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
  
    free(pos);
    pos = calloc((input_args.n_dim_data - 1), sizeof(npy_intp));
    if(pos == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for index structure.");
      goto cleanup_error;
    }

    buffer_ptr = &input_args.internal_buffer[0];
    do { 
      double result[4] = {0};
      incstats_kurtosis_finalize(result, buffer_ptr);
      buffer_ptr += 5;
      double *val = PyArray_GetPtr(array_mean, pos);
      *val = result[0];
      val = PyArray_GetPtr(array_variance, pos);
      *val = result[1];
      val = PyArray_GetPtr(array_skewness, pos);
      *val = result[2];
      val = PyArray_GetPtr(array_kurtosis, pos);
      *val = result[3];
    } while(!increment(pos, output_dims, input_args.n_dim_data - 1)); 
    
  }
  else {
    array_mean = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    array_variance = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    array_skewness = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    array_kurtosis = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    if((PyObject *)array_mean == NULL || (PyObject *)array_variance == 
    NULL || (PyObject *)array_skewness == NULL || (PyObject *)array_kurtosis == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
    buffer_ptr = &input_args.internal_buffer[0];
    double result[4] = {0};
    incstats_kurtosis_finalize(result, buffer_ptr);
    double *ptr = (double*)PyArray_DATA(array_mean);
    *ptr = result[0];
    ptr = (double*)PyArray_DATA(array_variance);
    *ptr = result[1];
    ptr = (double*)PyArray_DATA(array_skewness);
    *ptr = result[2];
    ptr = (double*)PyArray_DATA(array_kurtosis);
    *ptr = result[3];
  }

  // Create external buffer if it doesn't exist yet.
  if((PyObject *)input_args.buffer == NULL) {
    input_args.buffer = (PyArrayObject *) PyArray_SimpleNew(1, 
    &input_args.length_buffer, NPY_DOUBLE);
    if((PyObject *)input_args.buffer == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for external buffer.");
      goto cleanup_error;
    }
  }
  
  for(int i = 0; i < input_args.length_buffer; i++) {
    double *ptr = PyArray_GETPTR1(input_args.buffer, i);
    *ptr = input_args.internal_buffer[i];
  }  

  tuple = PyTuple_New(5);
  if(!tuple) {
    goto cleanup_error;
  }
  PyTuple_SetItem(tuple, 0, (PyObject *)array_mean);
  PyTuple_SetItem(tuple, 1, (PyObject *)array_variance);
  PyTuple_SetItem(tuple, 2, (PyObject *)array_skewness);
  PyTuple_SetItem(tuple, 3, (PyObject *)array_kurtosis);
  PyTuple_SetItem(tuple, 4, (PyObject *)input_args.buffer);
  
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  return tuple;

  cleanup_error:
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  Py_XDECREF(array_mean);
  Py_XDECREF(array_variance);
  Py_XDECREF(array_skewness);
  Py_XDECREF(array_kurtosis);
  Py_XDECREF(input_args.buffer);
  Py_XDECREF(tuple);
  return NULL;
}

PyObject *central_moment(PyObject *self, PyObject *args, PyObject* kwargs)
{
  static char *kwlist[] = 
  {"input", "p", "weights", "axis", "buffer", "standardize", NULL};
  input_args_container input_args;
  input_args.data = (PyArrayObject *)NULL;
  input_args.buffer = (PyArrayObject *)NULL;
  input_args.weights = (PyArrayObject *)NULL;
  input_args.scalar_weight = 1.0;
  input_args.scalar_data = 0.0;
  input_args.internal_buffer = NULL;
  input_args.axis = 0;
  input_args.input_is_scalar = false;
  input_args.kwlist = kwlist;
  input_args.n_dim_data = 0;
  input_args.n_dim_weights = 0;
  input_args.n_dim_buffer = -1;
  input_args.dimensions_data = NULL;
  input_args.dimensions_weights = NULL;
  input_args.dimensions_buffer = NULL;
  input_args.parse_p = true;
  input_args.p = -1;
  input_args.standardize = false;
  input_args.is_min_or_max = false;
  bool done = false;
  double *buffer_ptr = NULL;
  PyArrayObject **central_moment = (PyArrayObject **) NULL;
  npy_intp *output_dims = NULL;
  PyObject *tuple = NULL;
  npy_intp *pos = NULL;

  if(parse_input(args, kwargs, &input_args) == -1) {
    goto cleanup_error;
  }

  central_moment = calloc((input_args.p + 2), sizeof(PyArrayObject *));
  if(central_moment == NULL) {
     PyErr_SetString(PyExc_TypeError, 
    "Couldn't allocate memory for results.");
    goto cleanup_error;
  }
  pos = calloc(input_args.n_dim_data, sizeof(npy_intp));
  if(pos == NULL && input_args.n_dim_data > 0) {
    PyErr_SetString(PyExc_TypeError, 
    "Couldn't allocate memory for index structure.");
    goto cleanup_error;
  }
  
  buffer_ptr = &input_args.internal_buffer[0];
  if(input_args.n_dim_data == 0) {
    incstats_central_moment(input_args.scalar_data, input_args.scalar_weight, buffer_ptr, input_args.p);
  }
  else {
    do { 
      done = false;
      while(!done) {
        double weight = 1.0;
        if((PyObject *)input_args.weights != NULL) {
          weight = *(double *)PyArray_GetPtr(input_args.weights, pos);
        }
        double val = *slice_axis(input_args.data, pos, 
        input_args.dimensions_data, input_args.n_dim_data, input_args.axis,
        &done);
        incstats_central_moment(val, weight, buffer_ptr, input_args.p);
      }
      buffer_ptr += input_args.p + 1;
    } while(!increment_ignore_axis(pos, input_args.dimensions_data, 
    input_args.n_dim_data, input_args.axis));
  }
  
  if(input_args.n_dim_data > 1) {
    output_dims = malloc(sizeof(npy_intp) * (input_args.n_dim_data - 1));
    if(output_dims == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for mean array.");
      goto cleanup_error;
    }
    int k = 0;
    for(int i = 0; i < input_args.n_dim_data; i++) {
      if(i != input_args.axis) {
        output_dims[k++] = input_args.dimensions_data[i];
      }
    }

    for(int k = 0; k < input_args.p + 2; k++) {
      central_moment[k] = (PyArrayObject *) PyArray_SimpleNew
      ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
      if((PyObject *) central_moment[k] == NULL) {
        PyErr_SetString(PyExc_TypeError, 
        "Couldn't allocate memory for mean array.");
        goto cleanup_error;
      }
    }
  
    free(pos);
    pos = calloc((input_args.n_dim_data - 1), sizeof(size_t));
    if(pos == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for index structure.");
      goto cleanup_error;
    }
  
    double *result = calloc(input_args.p + 2, sizeof(double));
    buffer_ptr = &input_args.internal_buffer[0];
    if(result == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for results.");
      goto cleanup_error;
    }
    do {  
      incstats_central_moment_finalize(result, buffer_ptr, input_args.p, 
      input_args.standardize);
      buffer_ptr += input_args.p + 1;
      for(int k = 0; k < input_args.p + 2; k++) {
        double *val = PyArray_GetPtr(central_moment[k], pos);
        *val = result[k];
      }
    } while(!increment(pos, output_dims, input_args.n_dim_data - 1));
    free(result);
  }
  else {
    for(int k = 0; k < input_args.p + 2; k++) {
      central_moment[k] = (PyArrayObject *) PyArray_SimpleNew
      (0, NULL, NPY_DOUBLE);
      if((PyObject *) central_moment[k] == NULL) {
        PyErr_SetString(PyExc_TypeError, 
        "Couldn't allocate memory for mean array.");
        goto cleanup_error;
      }
    }
    
    buffer_ptr = &input_args.internal_buffer[0];
    double *result = calloc(input_args.p + 2, sizeof(double));
    if(result == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for results.");
      goto cleanup_error;
    }
    incstats_central_moment_finalize(result, buffer_ptr, input_args.p, 
    input_args.standardize);
    for(int k = 0; k < input_args.p + 2; k++) {
      double *val = PyArray_GetPtr(central_moment[k], pos);
      *val = result[k];
    }
    free(result);
  }
  
  // Create external buffer if it doesn't exist yet.
  if((PyObject *)input_args.buffer == NULL) {
    input_args.buffer = (PyArrayObject *) PyArray_SimpleNew(1, 
    &input_args.length_buffer, NPY_DOUBLE);
    if((PyObject *)input_args.buffer == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for external buffer.");
      goto cleanup_error;
    }
  }

  for(int i = 0; i < input_args.length_buffer; i++) {
    double *ptr = PyArray_GETPTR1(input_args.buffer, i);
    *ptr = input_args.internal_buffer[i];
  }
  
  tuple = PyTuple_New(input_args.p + 3);
  if(!tuple) {
    goto cleanup_error;
  }
  
  for(int k = 0; k < input_args.p + 2; k++) {
    PyTuple_SetItem(tuple, k, (PyObject *)central_moment[k]);
  }
  PyTuple_SetItem(tuple, input_args.p + 2, (PyObject *)input_args.buffer);
  
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  free(central_moment);
  return tuple;

  cleanup_error:
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  for(int k = 0; k < input_args.p + 2 && central_moment != NULL; k++) {
    Py_XDECREF(central_moment[k]);
  }
  Py_XDECREF(input_args.buffer);
  Py_XDECREF(tuple);
  free(central_moment);
  return NULL;
}

static void buffer_init(double *buffer, double val, size_t n) {
  for(size_t i = 0; i < n; i++) {
    buffer[i] = val;
  }
}

PyObject *maximum(PyObject *self, PyObject *args, PyObject* kwargs) {
  static char *kwlist[] = {"x", "axis", "buffer", NULL};
  input_args_container input_args;
  input_args.data = (PyArrayObject *)NULL;
  input_args.buffer = (PyArrayObject *)NULL;
  input_args.weights = (PyArrayObject *)NULL;
  input_args.scalar_weight = 1.0;
  input_args.scalar_data = 0.0;
  input_args.internal_buffer = NULL;
  input_args.axis = 0;
  input_args.input_is_scalar = false;
  input_args.kwlist = kwlist;
  input_args.n_dim_data = 0;
  input_args.n_dim_weights = 0;
  input_args.n_dim_buffer = -1;
  input_args.dimensions_data = NULL;
  input_args.dimensions_weights = NULL;
  input_args.dimensions_buffer = NULL;
  input_args.length_buffer = 1;
  input_args.parse_p = false;
  input_args.p = -1;
  input_args.is_min_or_max = true;
  PyArrayObject *array_max = (PyArrayObject *) NULL;
  bool done = false;
  double *buffer_ptr = NULL;
  npy_intp *output_dims = NULL;
  PyObject *tuple = NULL;
  npy_intp *pos = NULL;

  if(parse_input(args, kwargs, &input_args) == -1) {
    goto cleanup_error;
  }

  pos = calloc(input_args.n_dim_data, sizeof(npy_intp));
  if(pos == NULL && input_args.n_dim_data > 0) {
    PyErr_SetString(PyExc_TypeError, 
    "Couldn't allocate memory for index structure.");
    goto cleanup_error;
  }

  if((PyObject *)input_args.buffer == NULL) {
    buffer_init(input_args.internal_buffer, -DBL_MAX, input_args.length_buffer);
  }

  buffer_ptr = &input_args.internal_buffer[0];
  if(input_args.n_dim_data == 0) {
    incstats_max(input_args.scalar_data, buffer_ptr);
  }
  else {
    do { 
      done = false;
      while(!done) {
        double val = *slice_axis(input_args.data, pos, 
        input_args.dimensions_data, input_args.n_dim_data, input_args.axis,
        &done);
        incstats_max(val, buffer_ptr);
      }
      buffer_ptr++;
    } while(!increment_ignore_axis(pos, input_args.dimensions_data, 
    input_args.n_dim_data, input_args.axis));
  }

  if(input_args.n_dim_data > 1) {
    output_dims = malloc(sizeof(npy_intp) * (input_args.n_dim_data - 1));
    if(output_dims == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for max array.");
      goto cleanup_error;
    }
    int k = 0;
    for(int i = 0; i < input_args.n_dim_data; i++) {
      if(i != input_args.axis) {
        output_dims[k++] = input_args.dimensions_data[i];
      }
    }
    array_max = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    if((PyObject *)array_max == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for max array.");
      goto cleanup_error;
    }
  
    free(pos);
    pos = calloc((input_args.n_dim_data - 1), sizeof(npy_intp));
    if(pos == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for index structure.");
      goto cleanup_error;
    }

    buffer_ptr = &input_args.internal_buffer[0];
    do { 
      double *val = PyArray_GetPtr(array_max, pos);
      *val = *buffer_ptr;
      buffer_ptr++;
    } while(!increment(pos, output_dims, input_args.n_dim_data - 1)); 
    
  }
  else {
    array_max = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    if((PyObject *)array_max == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for max array.");
      goto cleanup_error;
    }
    buffer_ptr = &input_args.internal_buffer[0];
    double *ptr = (double*)PyArray_DATA(array_max);
    *ptr = buffer_ptr[0];
  }

  // Create external buffer if it doesn't exist yet.
  if((PyObject *)input_args.buffer == NULL) {
    input_args.buffer = (PyArrayObject *) PyArray_SimpleNew(1, 
    &input_args.length_buffer, NPY_DOUBLE);
    if((PyObject *)input_args.buffer == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for external buffer.");
      goto cleanup_error;
    }
  }
  
  for(int i = 0; i < input_args.length_buffer; i++) {
    double *ptr = PyArray_GETPTR1(input_args.buffer, i);
    *ptr = input_args.internal_buffer[i];
  }

  tuple = PyTuple_New(2);
  if(!tuple) {
    goto cleanup_error;
  }
  PyTuple_SetItem(tuple, 0, (PyObject *)array_max);
  PyTuple_SetItem(tuple, 1, (PyObject *)input_args.buffer);

  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);  
  return tuple;

  cleanup_error:
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  Py_XDECREF(array_max);
  Py_XDECREF(input_args.buffer);
  Py_XDECREF(tuple);
  return NULL;
}

PyObject *minimum(PyObject *self, PyObject *args, PyObject* kwargs) {
  static char *kwlist[] = {"x", "axis", "buffer", NULL};
  input_args_container input_args;
  input_args.data = (PyArrayObject *)NULL;
  input_args.buffer = (PyArrayObject *)NULL;
  input_args.weights = (PyArrayObject *)NULL;
  input_args.scalar_weight = 1.0;
  input_args.scalar_data = 0.0;
  input_args.internal_buffer = NULL;
  input_args.axis = 0;
  input_args.input_is_scalar = false;
  input_args.kwlist = kwlist;
  input_args.n_dim_data = 0;
  input_args.n_dim_weights = 0;
  input_args.n_dim_buffer = -1;
  input_args.dimensions_data = NULL;
  input_args.dimensions_weights = NULL;
  input_args.dimensions_buffer = NULL;
  input_args.length_buffer = 1;
  input_args.parse_p = false;
  input_args.p = -1;
  input_args.is_min_or_max = true;
  PyArrayObject *array_min = (PyArrayObject *) NULL;
  bool done = false;
  double *buffer_ptr = NULL;
  npy_intp *output_dims = NULL;
  PyObject *tuple = NULL;
  npy_intp *pos = NULL;

  if(parse_input(args, kwargs, &input_args) == -1) {
    goto cleanup_error;
  }

  if((PyObject *)input_args.buffer == NULL) {
    buffer_init(input_args.internal_buffer, DBL_MAX, input_args.length_buffer);
  }

  pos = calloc(input_args.n_dim_data, sizeof(npy_intp));
  if(pos == NULL && input_args.n_dim_data > 0) {
    PyErr_SetString(PyExc_TypeError, 
    "Couldn't allocate memory for index structure.");
    goto cleanup_error;
  }

  buffer_ptr = &input_args.internal_buffer[0];
  if(input_args.n_dim_data == 0) {
    incstats_min(input_args.scalar_data, buffer_ptr);
  }
  else {
    do { 
      done = false;
      while(!done) {
        double val = *slice_axis(input_args.data, pos, 
        input_args.dimensions_data, input_args.n_dim_data, input_args.axis,
        &done);
        incstats_min(val, buffer_ptr);
      }
      buffer_ptr++;
    } while(!increment_ignore_axis(pos, input_args.dimensions_data, 
    input_args.n_dim_data, input_args.axis));
  }

  if(input_args.n_dim_data > 1) {
    output_dims = malloc(sizeof(npy_intp) * (input_args.n_dim_data - 1));
    if(output_dims == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for min array.");
      goto cleanup_error;
    }
    int k = 0;
    for(int i = 0; i < input_args.n_dim_data; i++) {
      if(i != input_args.axis) {
        output_dims[k++] = input_args.dimensions_data[i];
      }
    }
    array_min = (PyArrayObject *) PyArray_SimpleNew
    ((input_args.n_dim_data - 1), output_dims, NPY_DOUBLE);
    if((PyObject *)array_min == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for min array.");
      goto cleanup_error;
    }
  
    free(pos);
    pos = calloc((input_args.n_dim_data - 1), sizeof(npy_intp));
    if(pos == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for index structure.");
      goto cleanup_error;
    }

    buffer_ptr = &input_args.internal_buffer[0];
    do { 
      double *val = PyArray_GetPtr(array_min, pos);
      *val = *buffer_ptr;
      buffer_ptr++;
    } while(!increment(pos, output_dims, input_args.n_dim_data - 1)); 
    
  }
  else {
    array_min = (PyArrayObject *) PyArray_SimpleNew
    (0, NULL, NPY_DOUBLE);
    if((PyObject *)array_min == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for min array.");
      goto cleanup_error;
    }
    buffer_ptr = &input_args.internal_buffer[0];
    double *ptr = (double*)PyArray_DATA(array_min);
    *ptr = buffer_ptr[0];
  }

  // Create external buffer if it doesn't exist yet.
  if((PyObject *)input_args.buffer == NULL) {
    input_args.buffer = (PyArrayObject *) PyArray_SimpleNew(1, 
    &input_args.length_buffer, NPY_DOUBLE);
    if((PyObject *)input_args.buffer == NULL) {
      PyErr_SetString(PyExc_TypeError, 
      "Couldn't allocate memory for external buffer.");
      goto cleanup_error;
    }
  }
  
  for(int i = 0; i < input_args.length_buffer; i++) {
    double *ptr = PyArray_GETPTR1(input_args.buffer, i);
    *ptr = input_args.internal_buffer[i];
  }

  tuple = PyTuple_New(2);
  if(!tuple) {
    goto cleanup_error;
  }
  PyTuple_SetItem(tuple, 0, (PyObject *)array_min);
  PyTuple_SetItem(tuple, 1, (PyObject *)input_args.buffer);
  
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  return tuple;

  cleanup_error:
  free(pos);
  free(input_args.internal_buffer);
  free(output_dims);
  Py_XDECREF(input_args.data);
  Py_XDECREF(input_args.weights);
  Py_XDECREF(array_min);
  Py_XDECREF(input_args.buffer);
  Py_XDECREF(tuple);
  return NULL;
}

static PyMethodDef incstats_methods[] = {
    {   
      "mean", (PyCFunction)mean, 
      METH_VARARGS | METH_KEYWORDS,
      "mean(input, weights=None, axis=0, buffer=None)\n"
      "\n"
      "Compute the running mean along the specified axis of the input array.\n"
      "\n"
      "Parameters:\n"
      "  input : array-like\n"
      "      Input data array or scalar.\n"
      "  weights : array-like, optional\n"
      "      Weights for the data points. Must be the same shape as `input`.\n"
      "  axis : int, optional\n"
      "      Axis along which to compute the mean. Default is 0.\n"
      "  buffer : array-like, optional\n"
      "      Buffer for intermediate storage. If not provided, one will be created.\n"
      "\n"
      "Returns:\n"
      "  tuple of ndarray\n"
      "      A tuple containing the computed mean array and the buffer used.\n"
      "\n"
    },
    {
      "variance", (PyCFunction)variance, 
      METH_VARARGS | METH_KEYWORDS, 
      "variance(input, weights=None, axis=0, buffer=None)\n"
      "\n"
      "Compute the running variance along the specified axis of the input array.\n"
      "\n"
      "Parameters:\n"
      "  input : array-like\n"
      "      Input data array or scalar.\n"
      "  weights : array-like, optional\n"
      "      Weights for the data points. Must be the same shape as `input`.\n"
      "  axis : int, optional\n"
      "      Axis along which to compute the variance. Default is 0.\n"
      "  buffer : array-like, optional\n"
      "      Buffer for intermediate storage. If not provided, one will be created.\n"
      "\n"
      "Returns:\n"
      "  tuple of ndarray\n"
      "      A tuple containing the computed variance array and the buffer used.\n"
      "\n"
    },
    {
      "skewness", (PyCFunction)skewness, 
      METH_VARARGS | METH_KEYWORDS,
      "skewness(input, weights=None, axis=0, buffer=None)\n"
      "\n"
      "Compute the running skewness along the specified axis of the input array.\n"
      "\n"
      "Parameters:\n"
      "  input : array-like\n"
      "      Input data array or scalar.\n"
      "  weights : array-like, optional\n"
      "      Weights for the data points. Must be the same shape as `input`.\n"
      "  axis : int, optional\n"
      "      Axis along which to compute the skewness. Default is 0.\n"
      "  buffer : array-like, optional\n"
      "      Buffer for intermediate storage. If not provided, one will be created.\n"
      "\n"
      "Returns:\n"
      "  tuple of ndarray\n"
      "      A tuple containing the computed skewness array and the buffer used.\n"
      "\n"
    },
    {
      "kurtosis", (PyCFunction)kurtosis, 
      METH_VARARGS | METH_KEYWORDS, 
      "kurtosis(input, weights=None, axis=0, buffer=None)\n"
      "\n"
      "Compute the running kurtosis along the specified axis of the input array.\n"
      "\n"
      "Parameters:\n"
      "  input : array-like\n"
      "      Input data array or scalar.\n"
      "  weights : array-like, optional\n"
      "      Weights for the data points. Must be the same shape as `input`.\n"
      "  axis : int, optional\n"
      "      Axis along which to compute the kurtosis. Default is 0.\n"
      "  buffer : array-like, optional\n"
      "      Buffer for intermediate storage. If not provided, one will be created.\n"
      "\n"
      "Returns:\n"
      "  tuple of ndarray\n"
      "      A tuple containing the computed kurtosis array and the buffer used.\n"
      "\n"
    },
    {
      "central_moment", (PyCFunction)central_moment, 
      METH_VARARGS | METH_KEYWORDS,
      "central_moment(input, p, weights=None, axis=0, buffer=None, standardize=False)\n"
      "\n"
      "Compute the central moments up to the p-th order along the specified axis.\n"
      "\n"
      "Parameters:\n"
      "  input : array-like\n"
      "      Input data array or scalar.\n"
      "  p : int\n"
      "      The order of the moment to compute.\n"
      "  weights : array-like, optional\n"
      "      Weights for the data points. Must be the same shape as `input`.\n"
      "  axis : int, optional\n"
      "      Axis along which to compute the central moments. Default is 0.\n"
      "  buffer : array-like, optional\n"
      "      Buffer for intermediate storage. If not provided, one will be created.\n"
      "  standardize : bool, optional\n"
      "      If true, the moments are standardized. Default is false.\n"
      "\n"
      "Returns:\n"
      "  tuple of ndarray\n"
      "      A tuple containing the computed central moments, mean and the buffer used.\n"
      "\n"
    },
    {   
      "max", (PyCFunction)maximum, 
      METH_VARARGS | METH_KEYWORDS,
      "max(x, axis=0, buffer=None)\n"
      "\n"
      "Compute the maximum value(s) along the specified axis of the input array.\n"
      "\n"
      "Parameters:\n"
      "  x : array-like or scalar\n"
      "      Input data. Can be an array or scalar.\n"
      "  axis : int, optional\n"
      "      Axis along which the maximum is computed. Default is 0.\n"
      "  buffer : array-like, optional\n"
      "      An optional buffer to store the computed maximum values. If not provided, an internal buffer will be allocated and returned.\n"
      "\n"
      "Returns:\n"
      "  tuple of ndarray\n"
      "      A tuple containing the computed maximum values and the buffer used.\n"
      "      - max_array: Numpy array containing the maximum values along the specified axis or the scalar max if input was scalar.\n"
      "      - buffer: The buffer used to store the results, either provided externally or created internally.\n"
      "\n"
    },
    {   
      "min", (PyCFunction)minimum, 
      METH_VARARGS | METH_KEYWORDS,
      "min(x, axis=0, buffer=None)\n"
      "\n"
      "Compute the minimum value(s) along the specified axis of the input array.\n"
      "\n"
      "Parameters:\n"
      "  x : array-like or scalar\n"
      "      Input data. Can be an array or scalar.\n"
      "  axis : int, optional\n"
      "      Axis along which the minimum is computed. Default is 0.\n"
      "  buffer : array-like, optional\n"
      "      An optional buffer to store the computed minimum values. If not provided, an internal buffer will be allocated and returned.\n"
      "\n"
      "Returns:\n"
      "  tuple of ndarray\n"
      "      A tuple containing the computed minimum values and the buffer used.\n"
      "      - min_array: Numpy array containing the minimum values along the specified axis or the scalar min if input was scalar.\n"
      "      - buffer: The buffer used to store the results, either provided externally or created internally.\n"
      "\n"
    },
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef incstats_module = {
  PyModuleDef_HEAD_INIT, 
  "incstatspy",
  "A Python C extension for running statistics.\n\n"
  "This module provides efficient implementations for calculating various "
  "running statistics on NumPy arrays using C.\n\n"
  "Available functions:\n"
  "- `mean(input, weights=None, axis=0, buffer=None)`: Computes the running mean.\n"
  "- `variance(input, weights=None, axis=0, buffer=None)`: Computes the running variance.\n"
  "- `skewness(input, weights=None, axis=0, buffer=None)`: Computes the running skewness.\n"
  "- `kurtosis(input, weights=None, axis=0, buffer=None)`: Computes the running kurtosis.\n"
  "- `central_moment(input, p, weights=None, axis=0, buffer=None, standardize=False)`: "
  "Computes central moments up to the p-th order.\n\n"
  "See the module documentation for more details on usage and parameters.",
  -1, 
  incstats_methods
};

/* name here must match extension name, with PyInit_ prefix */
PyMODINIT_FUNC PyInit_incstatspy(void) {
  import_array();
  return PyModule_Create(&incstats_module);
}