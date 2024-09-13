#include "aster.h"
#include "aster_prop.h"
#include "bundle.h"
#include "bundle_prop.h"
#include "fake.h"
#include "fake_prop.h"
#include "nucleus.h"
#include "nucleus_prop.h"
#include <pybind11/pybind11.h>
#include "python_utilities.h"
//#include <pybind11/numpy.h>
//#include <pybind11/stl.h>
namespace py = pybind11;

class Aster;
class Organizer;
class Object;

/// a utility to enrich the cytosim python module
void load_organizer_classes(py::module_ &m) {
    py::class_<Buddy>(m, "Buddy");
    
     /// Python interface to Organizer
    py::class_<Organizer,Object,Buddy>(m, "Organizer")
        .def("build", [](Organizer * org, std::string how, Simul & sim) {
            Glossary glos = Glossary(how); return org->build(glos, sim); } )
        .def("nbOrganized",  [](const Organizer * org) {return org->nbOrganized() ;})
        .def("nbOrganized",  [](Organizer * org, size_t n) {return org->nbOrganized(n) ;})
        .def("focus", &Organizer::organized)
        .def("grasp",  [](Organizer * org, Mecable * mec) {return org->grasp(mec) ;})
        .def("grasp",  [](Organizer * org, Mecable * mec, size_t n) {return org->grasp(mec,n) ;})
        .def("goodbye", &Organizer::goodbye)
        .def("addOrganized", &Organizer::addOrganized)
        .def("eraseOrganized", &Organizer::eraseOrganized)
        .def("mobile", &Organizer::mobile)
        .def("position", [](const Organizer * org) {return to_numpy(org->position());}, PYOWN)
        .def("positionP", [](const Organizer * org, unsigned i) {return to_numpy(org->positionP(i));}, PYOWN)
        .def("step", &Organizer::step)
        .def("dragCoefficient",  [](Organizer * org) {return org->dragCoefficient() ;})
        .def("getLink",  [](const Organizer * org, int n) {
            Vector V,W; 
            org->getLink((size_t)n,V,W);
            return std::vector<pyarray>{to_numpy(V),to_numpy(W)}; }, PYOWN)
        .def("next",  [](Organizer * org) {return org->next() ;})
        .def("prev",  [](Organizer * org) {return org->prev() ;});

    py::class_<Aster,Organizer>(m, "Aster")
        .def("solid",  [](const Aster * org) {return org->solid() ;})
        .def("position", [](const Aster * org) {return to_numpy(org->position());}, PYOWN)
        .def("nbFibers",  [](const Aster * org) {return org->nbFibers() ;})
        .def("fiber",  [](const Aster * org, int n) {return org->fiber((size_t)n) ;})
        .def("posLink1",  [](const Aster * org, int n) {return to_numpy(org->posLink1((size_t)n)) ;}, PYOWN)
        .def("posLink2",  [](const Aster * org, int n) {return to_numpy(org->posLink2((size_t)n)) ;}, PYOWN)
        .def("posFiber1",  [](const Aster * org, int n) {return to_numpy(org->posFiber1((size_t)n)) ;}, PYOWN)
        .def("posFiber2",  [](const Aster * org, int n) {return to_numpy(org->posFiber2((size_t)n)) ;}, PYOWN)
        .def("getLink1",  [](const Aster * org, int n) {
            Vector V,W; 
            org->getLink1((size_t)n,V,W);
            return std::vector<pyarray>{to_numpy(V),to_numpy(W)};}, PYOWN)
        .def("getLink2",  [](const Aster * org, int n) {
            Vector V,W; 
            org->getLink2((size_t)n,V,W);
            return std::vector<pyarray>{to_numpy(V),to_numpy(W)}; }, PYOWN)
        .def("getLink",  [](const Aster * org, int n) {
            Vector V,W; 
            org->getLink((size_t)n,V,W);
            return std::vector<pyarray>{to_numpy(V),to_numpy(W)}; }, PYOWN)
        .def("property",  [](const Aster * org) {return org->property() ;});
        
    py::class_<Bundle,Organizer>(m, "Bundle");
    
    py::class_<Fake,Organizer>(m, "Fake")
        .def("solid", &Fake::solid);
        
    py::class_<Nucleus,Organizer>(m, "Nucleus")
        .def("sphere", &Nucleus::sphere) 
        .def("fiber", &Nucleus::fiber);
    
    py::class_<AsterProp,Property>(m, "AsterProp")
        .def("stiffness",  [](AsterProp * prop) {return to_numpy_raw(prop->stiffness, 1, 2); }, PYOWN)
        .def_readwrite("focus", &AsterProp::focus)
        .def_readwrite("fiber_rate", &AsterProp::fiber_rate)
        .def_readwrite("fiber_spec", &AsterProp::fiber_spec);
    
    py::class_<BundleProp,Property>(m, "BundleProp")
        .def_readwrite("stiffness", &BundleProp::stiffness)
        .def_readwrite("overlap", &BundleProp::overlap)
        .def_readwrite("focus", &BundleProp::focus)
        .def_readwrite("fiber_rate", &BundleProp::fiber_rate)
        .def_readwrite("fiber_type", &BundleProp::fiber_type)
        .def_readwrite("fiber_spec", &BundleProp::fiber_spec)
        .def_readwrite("fiber_prob", &BundleProp::fiber_prob);
        
    py::class_<FakeProp,Property>(m, "FakeProp")
        .def_readwrite("stiffness", &FakeProp::stiffness);
    
    py::class_<NucleusProp,Property>(m, "NucleusProp")
        .def_readwrite("stiffness", &NucleusProp::stiffness);
}

