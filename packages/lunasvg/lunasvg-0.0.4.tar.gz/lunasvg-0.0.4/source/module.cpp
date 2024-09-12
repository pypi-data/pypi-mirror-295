#include <lunasvg.h>
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

static PyTypeObject Matrix_Type = { PyVarObject_HEAD_INIT(NULL, 0) };
static PyTypeObject Box_Type = { PyVarObject_HEAD_INIT(NULL, 0) };
static PyTypeObject Bitmap_Type = { PyVarObject_HEAD_INIT(NULL, 0) };
static PyTypeObject Element_Type = { PyVarObject_HEAD_INIT(NULL, 0) };
static PyTypeObject Document_Type = { PyVarObject_HEAD_INIT(NULL, 0) };

typedef struct {
    PyObject_HEAD
    lunasvg::Matrix matrix;
} Matrix_Object;

static PyObject* Matrix_Create(lunasvg::Matrix matrix);

static PyObject* Matrix_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    lunasvg::Matrix matrix;
    if(!PyArg_ParseTuple(args, "|ffffff:Matrix.__init__", &matrix.a, &matrix.b, &matrix.c, &matrix.d, matrix.e, matrix.f))
        return NULL;
    return Matrix_Create(matrix);
}

static void Matrix_dealloc(Matrix_Object* self)
{
    Py_TYPE(self)->tp_free(self);
}

static PyObject* Matrix_repr(Matrix_Object* self)
{
    char buf[256];
    PyOS_snprintf(buf, sizeof(buf), "lunasvg.Matrix(%g, %g, %g, %g, %g, %g)",
        self->matrix.a, self->matrix.b, self->matrix.c, self->matrix.d, self->matrix.e, self->matrix.f);
    return PyUnicode_FromString(buf);
}

static PyObject* Matrix_mul(Matrix_Object* self, PyObject* other)
{
    if(Py_TYPE(self) != Py_TYPE(other))
        Py_RETURN_NOTIMPLEMENTED;
    return Matrix_Create(self->matrix * ((Matrix_Object*)other)->matrix);
}

static PyObject* Matrix_imul(Matrix_Object* self, PyObject* other)
{
    if(Py_TYPE(self) != Py_TYPE(other))
        Py_RETURN_NOTIMPLEMENTED;
    self->matrix *= ((Matrix_Object*)other)->matrix;
    Py_INCREF(self);
    return (PyObject*)self;
}

static PyObject* Matrix_inv(Matrix_Object* self)
{
    return Matrix_Create(self->matrix.inverse());
}

static PyNumberMethods Matrix_as_number = {
    .nb_multiply = (binaryfunc)Matrix_mul,
    .nb_invert = (unaryfunc)Matrix_inv,
    .nb_inplace_multiply = (binaryfunc)Matrix_imul
};

static Py_ssize_t Matrix_length(Matrix_Object* self)
{
    return 6;
}

static PyObject* Matrix_item(Matrix_Object* self, Py_ssize_t index)
{
    switch(index) {
    case 0:
        return PyFloat_FromDouble(self->matrix.a);
    case 1:
        return PyFloat_FromDouble(self->matrix.b);
    case 2:
        return PyFloat_FromDouble(self->matrix.c);
    case 3:
        return PyFloat_FromDouble(self->matrix.d);
    case 4:
        return PyFloat_FromDouble(self->matrix.e);
    case 5:
        return PyFloat_FromDouble(self->matrix.f);
    default:
        PyErr_SetString(PyExc_IndexError, "Matrix index out of range");
        return NULL;
    }
}

static PySequenceMethods Matrix_as_sequence = {
    .sq_length = (lenfunc)Matrix_length,
    .sq_item = (ssizeargfunc)Matrix_item
};

static PyObject* Matrix_multiply(Matrix_Object* self, PyObject* args)
{
    Matrix_Object* matrix_ob;
    if(!PyArg_ParseTuple(args, "|O!", &Matrix_Type, &matrix_ob)) {
        return NULL;
    }

    self->matrix.multiply(matrix_ob->matrix);
    Py_INCREF(self);
    return (PyObject*)self;
}

static PyObject* Matrix_translate(Matrix_Object* self, PyObject* args)
{
    float tx, ty;
    if(!PyArg_ParseTuple(args, "ff", &tx, &ty)) {
        return NULL;
    }

    self->matrix.translate(tx, ty);
    Py_INCREF(self);
    return (PyObject*)self;
}

static PyObject* Matrix_scale(Matrix_Object* self, PyObject* args)
{
    float sx, sy;
    if(!PyArg_ParseTuple(args, "ff", &sx, &sy)) {
        return NULL;
    }

    self->matrix.scale(sx, sy);
    Py_INCREF(self);
    return (PyObject*)self;
}

static PyObject* Matrix_rotate(Matrix_Object* self, PyObject* args)
{
    float angle, cx = 0.f, cy = 0.f;
    if(!PyArg_ParseTuple(args, "f|ff", &angle, &cx, &cy)) {
        return NULL;
    }

    self->matrix.rotate(angle, cx, cy);
    Py_INCREF(self);
    return (PyObject*)self;
}

static PyObject* Matrix_shear(Matrix_Object* self, PyObject* args)
{
    float shx, shy;
    if(!PyArg_ParseTuple(args, "ff", &shx, &shy)) {
        return NULL;
    }

    self->matrix.scale(shx, shy);
    Py_INCREF(self);
    return (PyObject*)self;
}

static PyObject* Matrix_translated(PyTypeObject* type, PyObject* args)
{
    float tx, ty;
    if(!PyArg_ParseTuple(args, "ff", &tx, &ty)) {
        return NULL;
    }

    return Matrix_Create(lunasvg::Matrix::translated(tx, ty));
}

static PyObject* Matrix_scaled(PyTypeObject* type, PyObject* args)
{
    float sx, sy;
    if(!PyArg_ParseTuple(args, "ff", &sx, &sy)) {
        return NULL;
    }

    return Matrix_Create(lunasvg::Matrix::scaled(sx, sy));
}

static PyObject* Matrix_rotated(PyTypeObject* type, PyObject* args)
{
    float angle, cx = 0.f, cy = 0.f;
    if(!PyArg_ParseTuple(args, "f|ff", &angle, &cx, &cy)) {
        return NULL;
    }

    return Matrix_Create(lunasvg::Matrix::rotated(angle, cx, cy));
}

static PyObject* Matrix_sheared(PyTypeObject* type, PyObject* args)
{
    float shx, shy;
    if(!PyArg_ParseTuple(args, "ff", &shx, &shy)) {
        return NULL;
    }

    return Matrix_Create(lunasvg::Matrix::scaled(shx, shy));
}

static PyObject* Matrix_invert(Matrix_Object* self, PyObject* args)
{
    self->matrix.invert();
    Py_INCREF(self);
    return (PyObject*)self;
}

static PyObject* Matrix_inverse(Matrix_Object* self, PyObject* args)
{
    return Matrix_Create(self->matrix.inverse());
}

static PyObject* Matrix_reset(Matrix_Object* self, PyObject* args)
{
    self->matrix.reset();
    Py_RETURN_NONE;
}

static PyMethodDef Matrix_methods[] = {
    {"multiply", (PyCFunction)Matrix_multiply, METH_VARARGS},
    {"rotate", (PyCFunction)Matrix_rotate, METH_VARARGS},
    {"scale", (PyCFunction)Matrix_scale, METH_VARARGS},
    {"shear", (PyCFunction)Matrix_shear, METH_VARARGS},
    {"translate", (PyCFunction)Matrix_translate, METH_VARARGS},
    {"rotated", (PyCFunction)Matrix_rotated, METH_VARARGS | METH_CLASS},
    {"scaled", (PyCFunction)Matrix_scaled, METH_VARARGS | METH_CLASS},
    {"sheared", (PyCFunction)Matrix_sheared, METH_VARARGS| METH_CLASS},
    {"translated", (PyCFunction)Matrix_translated, METH_VARARGS| METH_CLASS},
    {"invert", (PyCFunction)Matrix_invert, METH_NOARGS},
    {"inverse", (PyCFunction)Matrix_inverse, METH_NOARGS},
    {"reset", (PyCFunction)Matrix_reset, METH_NOARGS},
    {NULL}
};

static PyMemberDef Matrix_members[] = {
    {"a", T_FLOAT, offsetof(Matrix_Object, matrix.a), 0, NULL},
    {"b", T_FLOAT, offsetof(Matrix_Object, matrix.b), 0, NULL},
    {"c", T_FLOAT, offsetof(Matrix_Object, matrix.c), 0, NULL},
    {"d", T_FLOAT, offsetof(Matrix_Object, matrix.d), 0, NULL},
    {"e", T_FLOAT, offsetof(Matrix_Object, matrix.e), 0, NULL},
    {"f", T_FLOAT, offsetof(Matrix_Object, matrix.f), 0, NULL},
    {NULL}
};

PyObject* Matrix_Create(lunasvg::Matrix matrix)
{
    Matrix_Object* matrix_ob = PyObject_New(Matrix_Object, &Matrix_Type);
    matrix_ob->matrix = matrix;
    return (PyObject*)matrix_ob;
}

typedef struct {
    PyObject_HEAD
    lunasvg::Box box;
} Box_Object;

static PyObject* Box_Create(lunasvg::Box box);

static PyObject* Box_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    lunasvg::Box box;
    if(!PyArg_ParseTuple(args, "|ffff:Box.__init__", &box.x, &box.y, &box.w, &box.h))
        return NULL;
    return Box_Create(box);
}

static void Box_dealloc(Box_Object* self)
{
    PyObject_Del(self);
}

static PyObject* Box_repr(Box_Object* self)
{
    char buf[256];
    PyOS_snprintf(buf, sizeof(buf), "lunasvg.Box(%g, %g, %g, %g)", self->box.x, self->box.y, self->box.w, self->box.h);
    return PyUnicode_FromString(buf);
}

static PyObject* Box_transform(Box_Object* self, PyObject* args)
{
    Matrix_Object* matrix_ob;
    if(!PyArg_ParseTuple(args, "|O!", &Matrix_Type, &matrix_ob)) {
        return NULL;
    }

    self->box.transform(matrix_ob->matrix);
    Py_INCREF(self);
    return (PyObject*)self;
}

static PyObject* Box_transformed(Box_Object* self, PyObject* args)
{
    Matrix_Object* matrix_ob;
    if(!PyArg_ParseTuple(args, "|O!", &Matrix_Type, &matrix_ob)) {
        return NULL;
    }

    return Box_Create(self->box.transformed(matrix_ob->matrix));
}

static Py_ssize_t Box_length(Box_Object* self)
{
    return 4;
}

static PyObject* Box_item(Box_Object* self, Py_ssize_t index)
{
    switch(index) {
    case 0:
        return PyFloat_FromDouble(self->box.x);
    case 1:
        return PyFloat_FromDouble(self->box.y);
    case 2:
        return PyFloat_FromDouble(self->box.w);
    case 3:
        return PyFloat_FromDouble(self->box.h);
    default:
        PyErr_SetString(PyExc_IndexError, "Box index out of range");
        return NULL;
    }
}

static PySequenceMethods Box_as_sequence = {
    .sq_length = (lenfunc)Box_length,
    .sq_item = (ssizeargfunc)Box_item
};

static PyMethodDef Box_methods[] = {
    {"transform", (PyCFunction)Box_transform, METH_VARARGS},
    {"transformed", (PyCFunction)Box_transformed, METH_VARARGS},
    {NULL}
};

static PyMemberDef Box_members[] = {
    {"x", T_FLOAT, offsetof(Box_Object, box.x), 0, NULL},
    {"y", T_FLOAT, offsetof(Box_Object, box.y), 0, NULL},
    {"w", T_FLOAT, offsetof(Box_Object, box.w), 0, NULL},
    {"h", T_FLOAT, offsetof(Box_Object, box.h), 0, NULL},
    {NULL}
};

PyObject* Box_Create(lunasvg::Box box)
{
    Box_Object* box_ob = PyObject_New(Box_Object, &Box_Type);
    box_ob->box = box;
    return (PyObject*)box_ob;
}

typedef struct {
    PyObject_HEAD
    PyObject* data;
    lunasvg::Bitmap bitmap;
} Bitmap_Object;

static PyObject* Bitmap_Create(PyObject* data, lunasvg::Bitmap bitmap);

static PyObject* Bitmap_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    int width, height;
    if(!PyArg_ParseTuple(args, "ii:Bitmap.__init__", &width, &height))
        return NULL;
    lunasvg::Bitmap bitmap(width, height);
    if(bitmap.isNull()) {
        PyErr_SetString(PyExc_MemoryError, "out of memory");
        return nullptr;
    }

    return Bitmap_Create(nullptr, std::move(bitmap));
}

static void Bitmap_dealloc(Bitmap_Object* self)
{
    self->bitmap.~Bitmap();
    Py_XDECREF(self->data);
    Py_TYPE(self)->tp_free(self);
}

static PyObject* Bitmap_create_for_data(PyTypeObject* type, PyObject* args)
{
    PyObject* data;
    int width, height, stride;
    if(!PyArg_ParseTuple(args, "Oiii", &data, &width, &height, &stride))
        return NULL;
    Py_buffer buffer;
    if(PyObject_GetBuffer(data, &buffer, PyBUF_WRITABLE) == -1)
        return NULL;
    if(height * stride > buffer.len) {
        PyBuffer_Release(&buffer);
        PyErr_SetString(PyExc_ValueError, "buffer is not long enough");
        return NULL;
    }

    lunasvg::Bitmap bitmap((uint8_t*)buffer.buf, width, height, stride);
    if(bitmap.isNull()) {
        PyErr_SetString(PyExc_MemoryError, "out of memory");
        return nullptr;
    }

    PyObject* bitmap_ob = Bitmap_Create(nullptr, std::move(bitmap));
    PyBuffer_Release(&buffer);
    return bitmap_ob;
}

static PyObject* Bitmap_data(Bitmap_Object* self, PyObject* args)
{
    return PyMemoryView_FromObject((PyObject*)self);
}

static PyObject* Bitmap_width(Bitmap_Object* self, PyObject* args)
{
    return PyLong_FromLong(self->bitmap.width());
}

static PyObject* Bitmap_height(Bitmap_Object* self, PyObject* args)
{
    return PyLong_FromLong(self->bitmap.width());
}

static PyObject* Bitmap_stride(Bitmap_Object* self, PyObject* args)
{
    return PyLong_FromLong(self->bitmap.stride());
}

static PyObject* Bitmap_clear(Bitmap_Object* self, PyObject* args)
{
    unsigned int color;
    if(!PyArg_ParseTuple(args, "I", &color)) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    self->bitmap.clear(color);
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}

static PyObject* Bitmap_write_to_png(Bitmap_Object* self, PyObject* args)
{
    PyObject* file_ob;
    if(!PyArg_ParseTuple(args, "O&", PyUnicode_FSConverter, &file_ob)) {
        return NULL;
    }

    bool success = false;
    Py_BEGIN_ALLOW_THREADS
    success = self->bitmap.writeToPng(PyBytes_AS_STRING(file_ob));
    Py_END_ALLOW_THREADS
    Py_DECREF(file_ob);
    if(!success) {
        PyErr_SetString(PyExc_IOError, "Failed to write PNG file.");
        return NULL;
    }

    Py_RETURN_NONE;
}

static int Bitmap_buffer(Bitmap_Object* self, Py_buffer* view, int flags)
{
    void* data = self->bitmap.data();
    int height = self->bitmap.height();
    int stride = self->bitmap.stride();
    return PyBuffer_FillInfo(view, (PyObject*)self, data, height * stride, 0, flags);
}

static PyBufferProcs Bitmap_as_buffer = {
    (getbufferproc)Bitmap_buffer,
    NULL
};

static PyMethodDef Bitmap_methods[] = {
    {"create_for_data", (PyCFunction)Bitmap_create_for_data, METH_VARARGS | METH_CLASS},
    {"data", (PyCFunction)Bitmap_data, METH_NOARGS},
    {"width", (PyCFunction)Bitmap_width, METH_NOARGS},
    {"height", (PyCFunction)Bitmap_height, METH_NOARGS},
    {"stride", (PyCFunction)Bitmap_stride, METH_NOARGS},
    {"clear", (PyCFunction)Bitmap_clear, METH_VARARGS},
    {"write_to_png", (PyCFunction)Bitmap_write_to_png, METH_VARARGS},
    {NULL}
};

static PyObject* Bitmap_Create(PyObject* data, lunasvg::Bitmap bitmap)
{
    Bitmap_Object* bitmap_ob = PyObject_New(Bitmap_Object, &Bitmap_Type);
    new (&bitmap_ob->bitmap) lunasvg::Bitmap(std::move(bitmap));
    bitmap_ob->data = data;
    Py_XINCREF(bitmap_ob->data);
    return (PyObject*)bitmap_ob;
}

typedef struct {
    PyObject_HEAD
    PyObject* document_ob;
    lunasvg::Element element;
} Element_Object;

static void Element_dealloc(Element_Object* self)
{
    Py_DECREF(self->document_ob);
    Py_TYPE(self)->tp_free(self);
}

static PyObject* Element_has_attribute(Element_Object* self, PyObject* args)
{
    const char* name;
    if(!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

    if(self->element.hasAttribute(name))
        Py_RETURN_TRUE;
    Py_RETURN_FALSE;
}

static PyObject* Element_get_attribute(Element_Object* self, PyObject* args)
{
    const char* name;
    if(!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

    return PyUnicode_FromString(self->element.getAttribute(name).data());
}

static PyObject* Element_set_attribute(Element_Object* self, PyObject* args)
{
    const char* name;
    const char* value;
    if(!PyArg_ParseTuple(args, "ss", &name, &value)) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    self->element.setAttribute(name, value);
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}

static PyObject* Element_render(Element_Object* self, PyObject* args)
{
    Bitmap_Object* bitmap_ob;
    Matrix_Object* matrix_ob = nullptr;
    if(!PyArg_ParseTuple(args, "O!|O!", &Bitmap_Type, &bitmap_ob, &Matrix_Type, &matrix_ob)) {
        return NULL;
    }

    lunasvg::Matrix matrix;
    if(matrix_ob) {
        matrix = matrix_ob->matrix;
    }

    Py_BEGIN_ALLOW_THREADS
    self->element.render(bitmap_ob->bitmap, matrix);
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}

static PyObject* Element_render_to_bitmap(Element_Object* self, PyObject* args, PyObject* kwds)
{
    static const char* kwlist[] = { "width", "height", "background_color", NULL };
    int width = -1, height = -1;
    unsigned int background_color = 0;
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "|iiI", (char**)kwlist, &width, &height, &background_color)) {
        return NULL;
    }

    lunasvg::Bitmap bitmap;
    Py_BEGIN_ALLOW_THREADS
    bitmap = self->element.renderToBitmap(width, height, background_color);
    Py_END_ALLOW_THREADS
    if(bitmap.isNull()) {
        PyErr_SetString(PyExc_ValueError, "invalid element size");
        return nullptr;
    }

    return Bitmap_Create(nullptr, std::move(bitmap));
}

static PyObject* Element_get_local_matrix(Element_Object* self, PyObject* args)
{
    return Matrix_Create(self->element.getLocalMatrix());
}

static PyObject* Element_get_global_matrix(Element_Object* self, PyObject* args)
{
    return Matrix_Create(self->element.getGlobalMatrix());
}

static PyObject* Element_get_local_bounding_box(Element_Object* self, PyObject* args)
{
    return Box_Create(self->element.getLocalBoundingBox());
}

static PyObject* Element_get_global_bounding_box(Element_Object* self, PyObject* args)
{
    return Box_Create(self->element.getGlobalBoundingBox());
}

static PyObject* Element_get_bounding_box(Element_Object* self, PyObject* args)
{
    return Box_Create(self->element.getBoundingBox());
}

static PyObject* Element_document(Element_Object* self, PyObject* args)
{
    Py_INCREF(self->document_ob);
    return self->document_ob;
}

static PyMethodDef Element_methods[] = {
    {"has_attribute", (PyCFunction)Element_has_attribute, METH_VARARGS},
    {"get_attribute", (PyCFunction)Element_get_attribute, METH_VARARGS},
    {"set_attribute", (PyCFunction)Element_set_attribute, METH_VARARGS},
    {"render", (PyCFunction)Element_render, METH_VARARGS},
    {"render_to_bitmap", (PyCFunction)Element_render_to_bitmap, METH_VARARGS | METH_KEYWORDS},
    {"get_local_matrix", (PyCFunction)Element_get_local_matrix, METH_VARARGS},
    {"get_global_matrix", (PyCFunction)Element_get_global_matrix, METH_VARARGS},
    {"get_local_bounding_box", (PyCFunction)Element_get_local_bounding_box, METH_VARARGS},
    {"get_global_bounding_box", (PyCFunction)Element_get_global_bounding_box, METH_VARARGS},
    {"get_bounding_box", (PyCFunction)Element_get_bounding_box, METH_VARARGS},
    {"document", (PyCFunction)Element_document, METH_NOARGS},
    {NULL}
};

typedef struct {
    PyObject_HEAD
    std::unique_ptr<lunasvg::Document> document;
} Document_Object;

static PyObject* Element_Create(Document_Object* document_ob, lunasvg::Element element)
{
    Element_Object* element_ob = PyObject_New(Element_Object, &Element_Type);
    element_ob->document_ob = (PyObject*)document_ob;
    element_ob->element = element;
    Py_INCREF(element_ob->document_ob);
    return (PyObject*)element_ob;
}

static PyObject* Document_Create(std::unique_ptr<lunasvg::Document> document);

static PyObject* Document_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    PyObject* file_ob;
    if(!PyArg_ParseTuple(args, "O&", PyUnicode_FSConverter, &file_ob)) {
        return NULL;
    }

    std::unique_ptr<lunasvg::Document> document;
    Py_BEGIN_ALLOW_THREADS
    document = lunasvg::Document::loadFromFile(PyBytes_AS_STRING(file_ob));
    Py_END_ALLOW_THREADS
    return Document_Create(std::move(document));
}

static void Document_dealloc(Document_Object* self)
{
    self->document.~unique_ptr<lunasvg::Document>();
    Py_TYPE(self)->tp_free(self);
}

static PyObject* Document_load_from_data(PyTypeObject* type, PyObject* args)
{
    const char* data;
    if(!PyArg_ParseTuple(args, "s", &data))
        return NULL;
    std::unique_ptr<lunasvg::Document> document;
    Py_BEGIN_ALLOW_THREADS
    document = lunasvg::Document::loadFromData(data);
    Py_END_ALLOW_THREADS
    return Document_Create(std::move(document));
}

static PyObject* Document_width(Document_Object* self, PyObject* args)
{
    return PyFloat_FromDouble(self->document->width());
}

static PyObject* Document_height(Document_Object* self, PyObject* args)
{
    return PyFloat_FromDouble(self->document->height());
}

static PyObject* Document_bounding_box(Document_Object* self, PyObject* args)
{
    return Box_Create(self->document->boundingBox());
}

static PyObject* Document_update_layout(Document_Object* self, PyObject* args)
{
    Py_BEGIN_ALLOW_THREADS
    self->document->updateLayout();
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}

static PyObject* Document_render(Document_Object* self, PyObject* args)
{
    Bitmap_Object* bitmap_ob;
    Matrix_Object* matrix_ob = nullptr;
    if(!PyArg_ParseTuple(args, "O!|O!", &Bitmap_Type, &bitmap_ob, &Matrix_Type, &matrix_ob)) {
        return NULL;
    }

    lunasvg::Matrix matrix;
    if(matrix_ob) {
        matrix = matrix_ob->matrix;
    }

    Py_BEGIN_ALLOW_THREADS
    self->document->render(bitmap_ob->bitmap, matrix);
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}

static PyObject* Document_render_to_bitmap(Document_Object* self, PyObject* args, PyObject* kwds)
{
    static const char* kwlist[] = { "width", "height", "background_color", NULL };
    int width = -1, height = -1;
    unsigned int background_color = 0;
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "|iiI", (char**)kwlist, &width, &height, &background_color)) {
        return NULL;
    }

    lunasvg::Bitmap bitmap;
    Py_BEGIN_ALLOW_THREADS
    bitmap = self->document->renderToBitmap(width, height, background_color);
    Py_END_ALLOW_THREADS
    if(bitmap.isNull()) {
        PyErr_SetString(PyExc_ValueError, "invalid document size");
        return nullptr;
    }

    return Bitmap_Create(nullptr, std::move(bitmap));
}

static PyObject* Document_get_element_by_id(Document_Object* self, PyObject* args)
{
    const char* id;
    if(!PyArg_ParseTuple(args, "s", &id)) {
        return NULL;
    }

    lunasvg::Element element;
    Py_BEGIN_ALLOW_THREADS
    element = self->document->getElementById(id);
    Py_END_ALLOW_THREADS
    if(element.isNull())
        Py_RETURN_NONE;
    return Element_Create(self, element);
}

static PyObject* Document_document_element(Document_Object* self, PyObject* args)
{
    return Element_Create(self, self->document->documentElement());
}

static PyMethodDef Document_methods[] = {
    {"load_from_data", (PyCFunction)Document_load_from_data, METH_VARARGS | METH_CLASS},
    {"width", (PyCFunction)Document_width, METH_NOARGS},
    {"height", (PyCFunction)Document_height, METH_NOARGS},
    {"bounding_box", (PyCFunction)Document_bounding_box, METH_NOARGS},
    {"update_layout", (PyCFunction)Document_update_layout, METH_NOARGS},
    {"render", (PyCFunction)Document_render, METH_VARARGS},
    {"render_to_bitmap", (PyCFunction)Document_render_to_bitmap, METH_VARARGS | METH_KEYWORDS},
    {"get_element_by_id", (PyCFunction)Document_get_element_by_id, METH_VARARGS},
    {"document_element", (PyCFunction)Document_document_element, METH_NOARGS},
    {NULL}
};

static PyObject* Document_Create(std::unique_ptr<lunasvg::Document> document)
{
    if(document == nullptr) {
        PyErr_SetString(PyExc_ValueError, "Failed to load document from data.");
        return nullptr;
    }

    Document_Object* document_ob = PyObject_New(Document_Object, &Document_Type);
    new (&document_ob->document) std::unique_ptr<lunasvg::Document>(std::move(document));
    return (PyObject*)document_ob;
}

static PyObject* module_add_font_face_from_file(PyObject* self, PyObject* args)
{
    return nullptr;
}

static PyObject* module_add_font_face_from_data(PyObject* self, PyObject* args)
{
    return nullptr;
}

static PyMethodDef module_methods[] = {
    {"add_font_face_from_file", (PyCFunction)module_add_font_face_from_file, METH_VARARGS},
    {"add_font_face_from_data", (PyCFunction)module_add_font_face_from_data, METH_VARARGS},
    {NULL}
};

static struct PyModuleDef module_definition = {
    PyModuleDef_HEAD_INIT,
    "lunasvg",
    0,
    0,
    module_methods,
    0,
    0,
    0,
    0,
};

PyMODINIT_FUNC PyInit__lunasvg(void)
{
    Matrix_Type.tp_name = "lunasvg.Matrix";
    Matrix_Type.tp_basicsize = sizeof(Matrix_Object);
    Matrix_Type.tp_dealloc = (destructor)Matrix_dealloc;
    Matrix_Type.tp_repr = (reprfunc)Matrix_repr;
    Matrix_Type.tp_as_number = &Matrix_as_number;
    Matrix_Type.tp_as_sequence = &Matrix_as_sequence;
    Matrix_Type.tp_flags = Py_TPFLAGS_DEFAULT;
    Matrix_Type.tp_methods = Matrix_methods;
    Matrix_Type.tp_members = Matrix_members;
    Matrix_Type.tp_new = (newfunc)Matrix_new;
    if(PyType_Ready(&Matrix_Type) < 0) {
        return nullptr;
    }

    Box_Type.tp_name = "lunasvg.Box",
    Box_Type.tp_basicsize = sizeof(Box_Object);
    Box_Type.tp_dealloc = (destructor)Box_dealloc;
    Box_Type.tp_repr = (reprfunc)Box_repr;
    Box_Type.tp_as_sequence = &Box_as_sequence;
    Box_Type.tp_flags = Py_TPFLAGS_DEFAULT;
    Box_Type.tp_methods = Box_methods;
    Box_Type.tp_members = Box_members;
    Box_Type.tp_new = (newfunc)Box_new;
    if(PyType_Ready(&Box_Type) < 0) {
        return nullptr;
    }

    Bitmap_Type.tp_name = "lunasvg.Bitmap";
    Bitmap_Type.tp_basicsize = sizeof(Bitmap_Object);
    Bitmap_Type.tp_dealloc = (destructor)Bitmap_dealloc;
    Bitmap_Type.tp_as_buffer = &Bitmap_as_buffer;
    Bitmap_Type.tp_flags = Py_TPFLAGS_DEFAULT;
    Bitmap_Type.tp_methods = Bitmap_methods;
    Bitmap_Type.tp_new = (newfunc)Bitmap_new;
    if(PyType_Ready(&Bitmap_Type) < 0) {
        return nullptr;
    }

    Element_Type.tp_name = "lunasvg.Element";
    Element_Type.tp_basicsize = sizeof(Element_Object);
    Element_Type.tp_dealloc = (destructor)Element_dealloc;
    Element_Type.tp_flags = Py_TPFLAGS_DEFAULT;
    Element_Type.tp_methods = Element_methods;
    if(PyType_Ready(&Element_Type) < 0) {
        return nullptr;
    }

    Document_Type.tp_name = "lunasvg.Document";
    Document_Type.tp_basicsize = sizeof(Document_Object);
    Document_Type.tp_dealloc = (destructor)Document_dealloc;
    Document_Type.tp_flags = Py_TPFLAGS_DEFAULT;
    Document_Type.tp_methods = Document_methods;
    Document_Type.tp_new = (newfunc)Document_new;
    if(PyType_Ready(&Document_Type) < 0) {
        return nullptr;
    }

    PyObject* module = PyModule_Create(&module_definition);
    if(module == NULL) {
        return NULL;
    }

    Py_INCREF(&Matrix_Type);
    Py_INCREF(&Box_Type);
    Py_INCREF(&Bitmap_Type);
    Py_INCREF(&Element_Type);
    Py_INCREF(&Document_Type);

    PyModule_AddObject(module, "Matrix", (PyObject*)&Matrix_Type);
    PyModule_AddObject(module, "Box", (PyObject*)&Box_Type);
    PyModule_AddObject(module, "Bitmap", (PyObject*)&Bitmap_Type);
    PyModule_AddObject(module, "Element", (PyObject*)&Element_Type);
    PyModule_AddObject(module, "Element", (PyObject*)&Element_Type);
    PyModule_AddObject(module, "Document", (PyObject*)&Document_Type);

    PyModule_AddIntConstant(module, "LUNASVG_VERSION", LUNASVG_VERSION);
    PyModule_AddIntConstant(module, "LUNASVG_VERSION_MINOR", LUNASVG_VERSION_MINOR);
    PyModule_AddIntConstant(module, "LUNASVG_VERSION_MICRO", LUNASVG_VERSION_MICRO);
    PyModule_AddIntConstant(module, "LUNASVG_VERSION_MAJOR", LUNASVG_VERSION_MAJOR);
    PyModule_AddStringConstant(module, "LUNASVG_VERSION_STRING", LUNASVG_VERSION_STRING);

    PyModule_AddStringConstant(module, "version", LUNASVG_VERSION_STRINGIZE(PYLUNASVG_VERSION_MAJOR, PYLUNASVG_VERSION_MINOR, PYLUNASVG_VERSION_MICRO));
    PyModule_AddObject(module, "version_info", Py_BuildValue("(iii)", PYLUNASVG_VERSION_MAJOR, PYLUNASVG_VERSION_MINOR, PYLUNASVG_VERSION_MICRO));
    return module;
}
