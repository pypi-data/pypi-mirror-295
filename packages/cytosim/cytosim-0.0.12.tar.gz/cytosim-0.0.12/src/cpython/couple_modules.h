#include "couple.h"
#include "couple_long.h"
#include "bridge.h"
#include "bridge_prop.h"
#include "crosslink.h"
#include "crosslink_prop.h"
#include "crosslink_long.h"
#include "duo.h"
#include "duo_prop.h"
#include "duo_long.h"
#include "fork.h"
#include "fork_prop.h"
#include "shackle.h"
#include "shackle_prop.h"
#include "shackle_long.h"

#include "inventoried.h"
#include "fiber.h"
#include <pybind11/pybind11.h>
#include "python_utilities.h"
//#include <pybind11/numpy.h>
//#include <pybind11/stl.h>
namespace py = pybind11;

class Couple;
class Object;

/**
 @defgroup PyCouple Couple
  A group functions to facilitate usage of Couple in PyCytosim
   
    @ingroup PyUtilities
 */

/// Converts an object to a Couple if possible;
/**
 * @brief Converts an object to a Couple if possible
 
  [python]$ `couple = cytosim.Couple.toCouple(obj) ` \n
 * @param obj
 * @return Couple 

 
 @ingroup PyCouple
 */
Couple* toCouple(Object * obj)
{
    if ( obj  &&  obj->tag() == 'c' )
        return static_cast<Couple*>(obj);
    return nullptr;
}

/// a utility to enrich the cytosim python module
void load_couple_classes(py::module_ &m) {
    py::class_<Couple,Object,HandMonitor>(m, "Couple")
        .def("position",  [](Couple * s) {return to_numpy(s->position());}, PYOWN)
        .def("mobile", &Couple::mobile)
        .def("translate",  [](Couple * s, pyarray dx) {Vector x = to_vector(dx); s->translate(x);})
        .def("setPosition",  [](Couple * s, pyarray pos) {Vector x = to_vector(pos); s->translate(x);})
        .def("randomizePosition", &Couple::randomizePosition)
        .def("active",  [](Couple * s) {return s->active();})
        .def("linking", &Couple::linking)
        .def("state",   &Couple::state)
        .def("configuration",  [](Couple * c, int end, real len) {return c->configuration((FiberEnd)end, len);})
        .def("stiffness",  [](Couple * s) {return s->stiffness();})
        .def("attachedHand",   &Couple::attachedHand)
        .def("force",  [](Couple * s) {return to_numpy(s->force());}, PYOWN)//
        .def("cosAngle",  [](Couple * s) {return s->cosAngle();})
        .def("sidePos",  [](Couple * s) {return to_numpy(s->sidePos());}, PYOWN)
        .def("posFree",  [](Couple * s) {return to_numpy(s->posFree());}, PYOWN)
        // all this definitely should be in the interface to hand
        .def("fiber2",  [](Couple * s) {return s->fiber2();}, PYREF)
        .def("abcissa",  [](Couple * s) {return to_numpy(s->posFree());}, PYOWN)
        .def("toCouple",  [](Object * s) {return toCouple(s);}, PYREF)
        .def("hand1",  [](Couple * s) {return s->hand1();}, PYREF)
        .def("attached1",   &Couple::attached1)
        .def("fiber1",   &Couple::fiber1)
        .def("abscissa1",   &Couple::abscissa1)
        .def("posHand1",  [](Couple * s) {return to_numpy(s->posHand1());}, PYOWN)
        .def("attach1",   &Couple::attach1)
        .def("attachEnd1",  [](Couple * s, Fiber * fib, int end) {return s->attachEnd1(fib, static_cast<FiberEnd>(end));})
        .def("moveToEnd1",  [](Couple * s,int end) {return s->moveToEnd1(static_cast<FiberEnd>(end));})
        .def("hand2",  [](Couple * s) {return s->hand2();}, PYREF)
        .def("attached2",   &Couple::attached2)
        .def("fiber2",   &Couple::fiber2)
        .def("abscissa2",   &Couple::abscissa2)
        .def("posHand2",  [](Couple * s) {return to_numpy(s->posHand2());}, PYOWN)
        .def("attach2",   &Couple::attach2)
        .def("attachEnd2",  [](Couple * s, Fiber * fib, int end) {return s->attachEnd2(fib, static_cast<FiberEnd>(end));})
        .def("moveToEnd2",  [](Couple * s,int end) {return s->moveToEnd2(static_cast<FiberEnd>(end));})
        .def("hand",  [](Couple * s, int i) {
            if (i==0) {return s->hand1();} else {return s->hand2();} ;}
            , PYREF)
        .def("__len__",  [](Couple * s) {return (int)2;})
        .def("__getitem__",[](const Couple *s, int i) { // We can call couple[0]  to get the first hand ! thus couple[0].attachEnd(...) is available
            if (i==0) {return s->hand1();}
            else if (i==1) {return s->hand2();}
            else {  throw py::index_error();}
            return (const Hand*) nullptr; }
            , PYREF);
         
         /**
            @TODO : ADD DETAILS IN SPECIALIZED COUPLE CLASSES
         */
        py::class_<Bridge,Couple>(m, "Bridge");
        py::class_<CoupleLong,Couple>(m, "CoupleLong");
        py::class_<Crosslink,Couple>(m, "Crosslink");
        py::class_<CrosslinkLong,Crosslink>(m, "CrosslinkLong");
        py::class_<Duo,Couple>(m, "Duo");
        py::class_<DuoLong,Duo>(m, "DuoLong");
        py::class_<Fork,Couple>(m, "Fork");
        py::class_<Shackle,Couple>(m, "Shackle");
        py::class_<ShackleLong,Shackle>(m, "ShackleLong");
        
 
         
         
        py::class_<CoupleProp,Property>(m, "CoupleProp")
            .def_readwrite("hand1", &CoupleProp::hand1)
            .def_readwrite("hand2", &CoupleProp::hand2)
            .def_readwrite("stiffness", &CoupleProp::stiffness)
            .def_readwrite("length", &CoupleProp::length)
            .def_readwrite("diffusion", &CoupleProp::diffusion)
            .def_readwrite("fast_diffusion", &CoupleProp::fast_diffusion)
            .def_readwrite("stiff", &CoupleProp::stiff)
            .def_readwrite("specificity", &CoupleProp::specificity)
            .def_readwrite("confine", &CoupleProp::confine)
            .def_readwrite("confine_space", &CoupleProp::confine_space)
            .def_readwrite("activity", &CoupleProp::activity)
            .def_readwrite("hand1_prop", &CoupleProp::hand1_prop)
            .def_readwrite("hand2_prop", &CoupleProp::hand2_prop);
            
            
        py::class_<BridgeProp,CoupleProp>(m, "BridgeProp");
        py::class_<CrosslinkProp,CoupleProp>(m, "CrosslinkProp");
        py::class_<DuoProp,CoupleProp>(m, "DuoProp");
        py::class_<ForkProp,CoupleProp>(m, "ForkProp");
        py::class_<ShackleProp,CoupleProp>(m, "ShackleProp");
        
    py::class_<CoupleSet,ObjectSet>(m, "CoupletSet")
		.def("__getitem__",[](CoupleSet * set, int i) {
				int s = set->size();
                if (i<0) {i+=s;} // Python time negative indexing
				if (i >= s or i<0) {
					 throw py::index_error();
				}
				Couple * obj = set->firstID();
				while (i) {
					--i; // I know this is slow, but ...
					obj = set->nextID(obj); // Maybe objectSet should derive from std::vect ?
				}
				return obj;
             }, PYREF);
}

