#include "single.h"
#include "picket.h"
#include "picket_long.h"
#include "wrist.h"
#include "wrist_long.h"
#include <pybind11/pybind11.h>
#include "python_utilities.h"
//#include <pybind11/numpy.h>
//#include <pybind11/stl.h>
namespace py = pybind11;

class Single;
class Object;



/**
 @defgroup PySingle Single
  A group functions to facilitate usage of Single in PyCytosim
   
    @ingroup PyUtilities
 */

/// Converts an object to a Single if possible;
/**
 * @brief Converts an object to a Single if possible
 
  [python]$ `single = cytosim.Single.toSingle(obj) ` \n
 * @param obj
 * @return Single 

 
 @ingroup PySingle
 */
Single* toSingle(Object * obj)
{
    if ( obj  &&  obj->tag() == 's' )
        return static_cast<Single*>(obj);
    return nullptr;
}

/// a utility to enrich the cytosim python module
void load_single_classes(py::module_ &m) {
    /// Python interface to HandMonitor
	py::class_<HandMonitor>(m, "HandMonitor")
		.def("allowAttachment", &HandMonitor::allowAttachment)
		.def("afterAttachment", &HandMonitor::afterAttachment)
		.def("beforeDetachment", &HandMonitor::beforeDetachment)
		.def("otherHand", &HandMonitor::otherHand)
        .def("otherPosition",  [](HandMonitor * monitor, Hand const * h) 
            {return to_numpy(monitor->otherPosition(h));}, PYOWN)
        .def("otherDirection",  [](HandMonitor * monitor, Hand const * h) 
            {return to_numpy(monitor->otherDirection(h));}, PYOWN)
        .def("linkRestingLength", &HandMonitor::linkRestingLength)
		.def("linkStiffness", &HandMonitor::linkStiffness)
        .def("nucleatorID", &HandMonitor::nucleatorID);
    
     /// Python interface to single
    py::class_<Single,Object, HandMonitor>(m, "Single")
        .def("toSingle",  [](Object * s) {return toSingle(s);}, PYREF)
        .def("state", &Single::state)
        .def("__getitem__",[](Single *s, int i) { // We can call Single[0]  to get the first hand ! thus couple[0].attachEnd(...) is available
            if (i==0) {return s->hand();} else {throw py::index_error(); }
            return (Hand*)nullptr;} 
            , PYREF)
        .def("__len__",  [](Single * s) {return (int)1;})
        .def("hand", &Single::hand, PYREF)
        .def("attached", &Single::attached)
        .def("fiber", &Single::fiber, PYREF)
        .def("abscissa", &Single::abscissa)
        .def("posHand",  [](Single * s) {return to_numpy(s->posHand());}, PYOWN)
        .def("dirFiber",  [](Single * s) {return to_numpy(s->dirFiber());}, PYOWN)
        .def("attach", &Single::attach)
        .def("attachEnd",  [](Single * s, Fiber *f, int end) {return s->attachEnd(f,static_cast<FiberEnd>(end));})
        .def("moveToEnd",  [](Single * s, int end) {return s->moveToEnd(static_cast<FiberEnd>(end));})
        .def("detach", &Single::detach)
        .def("position",  [](Single * s) {return to_numpy(s->position());}, PYOWN)
        .def("mobile", &Single::mobile)
        .def("translate",  [](Single * s, pyarray vec) 
            {   Vector p = to_vector(vec);
                return s->translate(p);})
        .def("setPosition",  [](Single * s, pyarray vec) 
            {   Vector p = to_vector(vec);
                return s->setPosition(p);})
        .def("randomizePosition", &Single::randomizePosition)
        .def("posFoot",  [](Single * s) {return to_numpy(s->posFoot());}, PYOWN)
        .def("sidePos",  [](Single * s) {return to_numpy(s->sidePos());}, PYOWN)
        .def("base", &Single::base)
        .def("mobile", &Single::mobile)
        .def("force",  [](Single * s) {return to_numpy(s->force());}, PYOWN)
        .def("stepF", &Single::stepF)
        .def("stepA", &Single::stepA)
        .def("next", &Single::next)
        .def("prev", &Single::prev)
        .def("confineSpace", &Single::confineSpace);
        
        

    py::class_<SingleProp,Property>(m, "SingleProp")
        .def_readwrite("hand", &SingleProp::hand)
        .def_readwrite("stiffness", &SingleProp::stiffness)
        .def_readwrite("length", &SingleProp::length)
        .def_readwrite("diffusion", &SingleProp::diffusion)
        .def_readwrite("fast_diffusion", &SingleProp::fast_diffusion)
        .def_readwrite("confine", &SingleProp::confine)
        .def_readwrite("confine_space", &SingleProp::confine_space)
        .def_readwrite("activity", &SingleProp::activity)
        .def_readwrite("hand_prop", &SingleProp::hand_prop);
    
     py::class_<SingleSet,ObjectSet>(m, "SingleSet")
		.def("__getitem__",[](SingleSet * set, int i) {
				int s = set->size();
                if (i<0) {i+=s;} // Python time negative indexing
				if (i >= s or i<0) {
					 throw py::index_error();
				}
				Single * obj = set->firstID();
				while (i) {
					--i; // I know this is slow, but ...
					obj = set->nextID(obj); 
				}
				return obj;
             }, PYREF);
             
    py::class_<Picket,Single>(m, "Picket")
        .def("beforeDetachment", &Picket::beforeDetachment)
        .def("linkStiffness", &Picket::linkStiffness);
	py::class_<PicketLong,Picket>(m, "PicketLong");
    py::class_<Wrist,Single>(m, "Wrist");
    py::class_<WristLong,Wrist>(m, "WristLong");
        
}

