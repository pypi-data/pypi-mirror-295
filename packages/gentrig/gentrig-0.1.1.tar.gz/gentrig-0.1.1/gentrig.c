#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h>
#include <numpy/ndarraytypes.h>
#include "numpy/ufuncobject.h"
#include "numpy/npy_3kcompat.h"

#define sec(x) (1.0 / cos(x))
#define cot(x) (1.0 / tan(x))

static char types[2] = {NPY_DOUBLE, NPY_DOUBLE};
static char types_poly[3] = {NPY_DOUBLE, NPY_DOUBLE, NPY_DOUBLE};

#define ufuncbp(name, expr)                                                                              \
    static void name##_ufunc(char **args, const npy_intp *dimensions, const npy_intp *steps, void *data) \
    {                                                                                                    \
        npy_intp i;                                                                                      \
        npy_intp n = dimensions[0];                                                                      \
        char *in = args[0], *out = args[1];                                                              \
        npy_intp in_step = steps[0], out_step = steps[1];                                                \
        double x;                                                                                        \
        for (i = 0; i < n; i++)                                                                          \
        {                                                                                                \
            x = *(double *)in;                                                                           \
            *((double *)out) = expr;                                                                     \
            in += in_step;                                                                               \
            out += out_step;                                                                             \
        }                                                                                                \
    }

#define ufuncs(name, expr_sin, expr_cos)                                      \
    ufuncbp(sin##name, expr_sin);                                             \
    ufuncbp(cos##name, expr_cos);                                             \
    ufuncbp(tan##name, (expr_sin) / (expr_cos));                              \
    ufuncbp(csc##name, 1.0 / (expr_sin));                                     \
    ufuncbp(sec##name, 1.0 / (expr_cos));                                     \
    ufuncbp(cot##name, (expr_cos) / (expr_sin));                              \
    PyUFuncGenericFunction funcs_sin##name##_ufunc[1] = {&sin##name##_ufunc}; \
    PyUFuncGenericFunction funcs_cos##name##_ufunc[1] = {&cos##name##_ufunc}; \
    PyUFuncGenericFunction funcs_tan##name##_ufunc[1] = {&tan##name##_ufunc}; \
    PyUFuncGenericFunction funcs_csc##name##_ufunc[1] = {&csc##name##_ufunc}; \
    PyUFuncGenericFunction funcs_sec##name##_ufunc[1] = {&sec##name##_ufunc}; \
    PyUFuncGenericFunction funcs_cot##name##_ufunc[1] = {&cot##name##_ufunc};

#define ufuncs_impl(name)                                                                                                 \
    PyObject *sin##name, *cos##name, *tan##name, *csc##name, *sec##name, *cot##name;                                      \
                                                                                                                          \
    sin##name = PyUFunc_FromFuncAndData(funcs_sin##name##_ufunc, NULL, types, 1, 1, 1, PyUFunc_None, "sin" #name, "", 0); \
    cos##name = PyUFunc_FromFuncAndData(funcs_cos##name##_ufunc, NULL, types, 1, 1, 1, PyUFunc_None, "cos" #name, "", 0); \
    tan##name = PyUFunc_FromFuncAndData(funcs_tan##name##_ufunc, NULL, types, 1, 1, 1, PyUFunc_None, "tan" #name, "", 0); \
    csc##name = PyUFunc_FromFuncAndData(funcs_csc##name##_ufunc, NULL, types, 1, 1, 1, PyUFunc_None, "csc" #name, "", 0); \
    sec##name = PyUFunc_FromFuncAndData(funcs_sec##name##_ufunc, NULL, types, 1, 1, 1, PyUFunc_None, "sec" #name, "", 0); \
    cot##name = PyUFunc_FromFuncAndData(funcs_cot##name##_ufunc, NULL, types, 1, 1, 1, PyUFunc_None, "cot" #name, "", 0); \
                                                                                                                          \
    PyDict_SetItemString(d, "sin" #name, sin##name);                                                                      \
    PyDict_SetItemString(d, "cos" #name, cos##name);                                                                      \
    PyDict_SetItemString(d, "tan" #name, tan##name);                                                                      \
    PyDict_SetItemString(d, "csc" #name, csc##name);                                                                      \
    PyDict_SetItemString(d, "sec" #name, sec##name);                                                                      \
    PyDict_SetItemString(d, "cot" #name, cot##name);                                                                      \
                                                                                                                          \
    Py_DECREF(sin##name);                                                                                                 \
    Py_DECREF(cos##name);                                                                                                 \
    Py_DECREF(tan##name);                                                                                                 \
    Py_DECREF(csc##name);                                                                                                 \
    Py_DECREF(sec##name);                                                                                                 \
    Py_DECREF(cot##name);

ufuncs(p, -cbrt(3.0 * x), pow(cbrt(3.0 * x), 2.0));

ufuncs(l, x, 1.0);

/*
Polygonal Trig is a special case from the macro in
that it includes a second argument for number of sides
*/

#define ufuncbp_poly(name, precalc, expr)                                                                \
                                                                                                         \
    static void name##_ufunc(char **args, const npy_intp *dimensions, const npy_intp *steps, void *data) \
    {                                                                                                    \
        npy_intp i;                                                                                      \
        npy_intp n = dimensions[0];                                                                      \
        char *in1 = args[0], *in2 = args[1], *out = args[2];                                             \
        npy_intp in1_step = steps[0], in2_step = steps[1], out_step = steps[2];                          \
        double x;                                                                                        \
        double y;                                                                                        \
        for (i = 0; i < n; i++)                                                                          \
        {                                                                                                \
            x = *(double *)in1;                                                                          \
            y = *(double *)in2;                                                                          \
            precalc;                                                                                     \
            *((double *)out) = expr;                                                                     \
            in1 += in1_step;                                                                             \
                                                                                                         \
            in2 += in2_step;                                                                             \
            out += out_step;                                                                             \
        }                                                                                                \
    }

#define ufuncs_poly(name, precalc, expr_sin, expr_cos)                        \
    ufuncbp_poly(sin##name, precalc, expr_sin);                               \
    ufuncbp_poly(cos##name, precalc, expr_cos);                               \
    ufuncbp_poly(tan##name, precalc, (expr_sin) / (expr_cos));                \
    ufuncbp_poly(csc##name, precalc, 1.0 / (expr_sin));                       \
    ufuncbp_poly(sec##name, precalc, 1.0 / (expr_cos));                       \
    ufuncbp_poly(cot##name, precalc, (expr_cos) / (expr_sin));                \
    PyUFuncGenericFunction funcs_sin##name##_ufunc[1] = {&sin##name##_ufunc}; \
    PyUFuncGenericFunction funcs_cos##name##_ufunc[1] = {&cos##name##_ufunc}; \
    PyUFuncGenericFunction funcs_tan##name##_ufunc[1] = {&tan##name##_ufunc}; \
    PyUFuncGenericFunction funcs_csc##name##_ufunc[1] = {&csc##name##_ufunc}; \
    PyUFuncGenericFunction funcs_sec##name##_ufunc[1] = {&sec##name##_ufunc}; \
    PyUFuncGenericFunction funcs_cot##name##_ufunc[1] = {&cot##name##_ufunc};

#define ufuncs_impl_poly(name)                                                                                                 \
    PyObject *sin##name, *cos##name, *tan##name, *csc##name, *sec##name, *cot##name;                                           \
                                                                                                                               \
    sin##name = PyUFunc_FromFuncAndData(funcs_sin##name##_ufunc, NULL, types_poly, 1, 2, 1, PyUFunc_None, "sin" #name, "", 0); \
    cos##name = PyUFunc_FromFuncAndData(funcs_cos##name##_ufunc, NULL, types_poly, 1, 2, 1, PyUFunc_None, "cos" #name, "", 0); \
    tan##name = PyUFunc_FromFuncAndData(funcs_tan##name##_ufunc, NULL, types_poly, 1, 2, 1, PyUFunc_None, "tan" #name, "", 0); \
    csc##name = PyUFunc_FromFuncAndData(funcs_csc##name##_ufunc, NULL, types_poly, 1, 2, 1, PyUFunc_None, "csc" #name, "", 0); \
    sec##name = PyUFunc_FromFuncAndData(funcs_sec##name##_ufunc, NULL, types_poly, 1, 2, 1, PyUFunc_None, "sec" #name, "", 0); \
    cot##name = PyUFunc_FromFuncAndData(funcs_cot##name##_ufunc, NULL, types_poly, 1, 2, 1, PyUFunc_None, "cot" #name, "", 0); \
                                                                                                                               \
    PyDict_SetItemString(d, "sin" #name, sin##name);                                                                           \
    PyDict_SetItemString(d, "cos" #name, cos##name);                                                                           \
    PyDict_SetItemString(d, "tan" #name, tan##name);                                                                           \
    PyDict_SetItemString(d, "csc" #name, csc##name);                                                                           \
    PyDict_SetItemString(d, "sec" #name, sec##name);                                                                           \
    PyDict_SetItemString(d, "cot" #name, cot##name);                                                                           \
                                                                                                                               \
    Py_DECREF(sin##name);                                                                                                      \
    Py_DECREF(cos##name);                                                                                                      \
    Py_DECREF(tan##name);                                                                                                      \
    Py_DECREF(csc##name);                                                                                                      \
    Py_DECREF(sec##name);                                                                                                      \
    Py_DECREF(cot##name);

#define calc_k_p                                       \
    double k = floor((x / 2.0) * cot(M_PI / y) + 0.5); \
    double p = ((x / 2.0) * cot(M_PI / y) + 0.5) - floor((x / 2.0) * cot(M_PI / y) + 0.5);

#define expr_sinpoly sec(M_PI / y) * (sin((M_PI / y) * (2 * k - 1)) * (1 - p) + sin((M_PI / y) * (2 * k + 1)) * p)
#define expr_cospoly sec(M_PI / y) * (cos((M_PI / y) * (2 * k - 1)) * (1 - p) + cos((M_PI / y) * (2 * k + 1)) * p)

ufuncs_poly(poly, calc_k_p, expr_sinpoly, expr_cospoly);

static PyMethodDef GentrigMethods[] = {
    {NULL, NULL, 0, NULL} /* Sentinel */
};
static struct PyModuleDef gentrig_module_def = {
    PyModuleDef_HEAD_INIT,
    "_gentrig",
    "Internal \"_gentrig\" module",
    -1,
    GentrigMethods};

PyMODINIT_FUNC PyInit_gentrig(void)
{

    PyObject *m, *d;

    import_array();
    import_umath();

    m = PyModule_Create(&gentrig_module_def);
    if (!m)
        return NULL;

    d = PyModule_GetDict(m);

    ufuncs_impl(p);
    ufuncs_impl(l);
    ufuncs_impl_poly(poly);

    return m;
}
