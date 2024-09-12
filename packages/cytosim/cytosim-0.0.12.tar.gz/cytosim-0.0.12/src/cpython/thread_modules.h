#include "sim_thread.h"
#include <pybind11/pybind11.h>
#include "python_utilities.h"
//#include <pybind11/numpy.h>
//#include <pybind11/stl.h>
namespace py = pybind11;

class SimThread;

/// a utility to enrich the cytosim python module
void load_thread_classes(py::module_ &m) {
    py::class_<SimThread>(m, "SimThread")
        .def("run", &SimThread::run)
        .def("extend_run", &SimThread::extend_run)
        .def("hold", &SimThread::hold)
        .def("child", &SimThread::child)
        .def("lock", &SimThread::lock)
        .def("unlock", &SimThread::unlock)
        .def("trylock", &SimThread::trylock)
        .def("wait", &SimThread::wait)
        .def("signal", &SimThread::signal)
        .def("period", &SimThread::period)
        .def("alive", &SimThread::alive)
        .def("start", &SimThread::start)
        .def("extend", &SimThread::extend)
        .def("step", &SimThread::step)
        .def("stop", &SimThread::stop)
        .def("cancel", &SimThread::cancel)
        .def("restart", &SimThread::restart)
        .def("clear", &SimThread::clear)
        .def("reloadParameters", &SimThread::reloadParameters)
        .def("execute", &SimThread::execute)
        .def("exportObjects", &SimThread::exportObjects)
        .def("openFile", &SimThread::openFile)
        .def("goodFile", &SimThread::goodFile)
        .def("eof", &SimThread::eof)
        .def("rewind", &SimThread::rewind)
        .def("loadFrame", &SimThread::loadFrame)
        .def("loadNextFrame", &SimThread::loadNextFrame)
        .def("loadLastFrame", &SimThread::loadLastFrame)
        .def("currentFrame", &SimThread::currentFrame)
        .def("handle", &SimThread::handle)
        .def("createHandle",  [](SimThread * thr, pyarray pos, real range) 
            {   Vector p = to_vector(pos);
                return thr->createHandle(p,range);})
        .def("selectClosestHandle",  [](SimThread * thr, pyarray pos, real range) 
            {   Vector p = to_vector(pos);
                return thr->selectClosestHandle(p,range);})
        .def("moveHandle",  [](SimThread * thr, pyarray pos) 
            {   Vector p = to_vector(pos);
                return thr->moveHandle(p);})
        .def("moveHandles",  [](SimThread * thr, pyarray pos) 
            {   Vector p = to_vector(pos);
                return thr->moveHandles(p);})
        .def("detachHandle", &SimThread::detachHandle)
        .def("deleteHandles", &SimThread::deleteHandles)
        .def("releaseHandle", &SimThread::releaseHandle)
        .def("openFile", &SimThread::openFile)
        .def("openFile", &SimThread::openFile)
        .def("openFile", &SimThread::openFile);
        
        
   
}
