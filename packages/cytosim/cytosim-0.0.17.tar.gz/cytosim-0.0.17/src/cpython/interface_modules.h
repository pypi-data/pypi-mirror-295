#include <pybind11/pybind11.h>
#include "python_utilities.h"
//#include <pybind11/numpy.h>
//#include <pybind11/stl.h>
namespace py = pybind11;

// @TODO : move stuff to python parser, copy better interface functions !

void execute_run(Interface * inter, py::args args) {
    std::string how = "";
    int many = 1;
    int nargs = args.size();
    if (nargs>0) {
        many = py::cast<int>(args[0]);
    }
    if (nargs>1) {
        how = py::cast<std::string>(args[1]);
    }
    Glossary glos = Glossary(how);
    inter->execute_run(many, glos,0);
}

void execute_change(Interface * inter, std::string & name, std::string & how) {
    Glossary glos = Glossary(how);
    inter->execute_change(name, glos);
}

Glossary * execute_set(Interface * inter, std::string & cat, std::string & name, std::string & how) {
    Glossary * glos = new Glossary(how);
    inter->execute_set(cat, name, *glos);
    return glos;
}

void load_interface_classes(py::module_ &m) {
      
    py::class_<Interface>(m, "Interface","an interface to cytosim")
        .def("hold", &Interface::hold)    
        //.def("execute_new",  [](Interface * inter, py::args args) { // @PYD;C:Interface;T: adds objects to simulation, see provided examples 
        //    return execute_new(inter, args);
        //}, PYMOV)
        .def("execute_new",  [](Interface * inter, std::string const& cat, std::string const& name, Glossary & how, int n) { // @PYD;C:Interface;T: adds objects to simulation, see provided examples 
            Glossary glos = Glossary(how);
            size_t cnt = n;
            return inter->execute_new(cat, name, glos, cnt);
            }, PYMOV)
        .def("execute_new",  [](Interface * inter,  std::string const& name, int n, Space const * spc, std::string const& pos) { // @PYD;C:Interface;T: adds objects to simulation, see provided examples 
            size_t cnt = n;
            return inter->execute_new(name,  cnt, spc, pos);
            }, PYMOV)
        .def("run",  [](Interface * inter, py::args args) { // @PYD;C:Interface;T: runs simulation a given number of steps, see provided examples 
            execute_run(inter, args); })
        .def("execute_run",  [](Interface * inter, py::args args) { // @PYD;C:Interface;T: runs simulation a given number of steps, see provided examples 
            execute_run(inter, args); })
        .def("set",  [](Interface * inter, std::string & cat, std::string & name, std::string & how) { // @PYD;C:Interface;T: defines objects to simulation, see provided examples 
            return execute_set(inter, cat, name, how);
        }, PYMOV)
        .def("execute_set",  [](Interface * inter, std::string & cat, std::string & name, std::string & how) { // @PYD;C:Interface;T: defines objects to simulation, see provided examples 
            return execute_set(inter, cat, name, how);
        }, PYMOV)
        .def("execute_change",  [](Interface * inter, std::string & name, std::string & how) { // @PYD;C:Interface;T: changes objects properties in  simulation, see provided examples 
            return execute_change(inter, name, how); })
        .def("execute_cut",  [](Interface * inter, std::string & name, std::string & where) { // @PYD;C:Simul;T: performes a cut : sim.cut(filament_name, where), see Parser.execute_cut  (C++)
            Glossary glos = Glossary(where);
            inter->execute_cut(name, glos);
            })
        .def("execute_delete",  [](Interface * inter, std::string & name, std::string & how, int number) { // @PYD;C:Simul;T: deletes objects from simulation, see provided examples
            Glossary glos = Glossary(how);
            inter->execute_delete(name, glos, number);
            })
        .def("execute_import",  [](Interface * inter, std::string & file, std::string & what, std::string & how) { // @PYD;C:Simul;T: imports objects from text file, see provided examples
            Glossary glos = Glossary(how);
            inter->execute_import(file, what, glos);
            })
        .def("export",  [](Interface * inter, std::string & file, std::string & what, std::string & how) { // @PYD;C:Simul;T: export objects to text file, see provided examples
            Glossary glos = Glossary(how);
            inter->execute_export(file, what, glos);
            });           
            
    py::class_<Parser,Interface>(m, "Parser","a cytosim parser");
    py::class_<PythonParser,Parser>(m, "PythonParser","Python interface to a parser")
        .def("add",  [](PythonParser * PyParse, py::args args) { // @PYD;C:Interface;T: adds objects to simulation, see provided examples 
            return PyParse->add(args);
        }, PYMOV)
        .def_readwrite("simul", &PythonParser::sim)
        .def_readwrite("thread", &PythonParser::thread)
        .def("load", &PythonParser::load)
        .def_readwrite("thread", &PythonParser::thread)
        .def("frame", &PythonParser::frame, PYMOV)
        .def("next", &PythonParser::next)    
        .def("save", [](PythonParser & pyparse) { // @PYD;C:Simul;T: saves current state to trajectory file
            pyparse.sim->writeObjects(pyparse.sim->prop->trajectory_file,pyparse.is_saved,1);
            if (!pyparse.is_saved) {pyparse.is_saved = 1;};
            pyparse.sim->writeProperties(&pyparse.sim->prop->property_file[0],1);
        });
    
    ///  Python interface to timeframe : behaves roughly as a Python dict of ObjectGroup
    py::class_<Frame>(m, "Timeframe","Python interface to timeframe : behaves as a Python dictionary of Objectsets")
        .def_readwrite("time", &Frame::time)
        .def_readwrite("simul", &Frame::simul)
        .def_readwrite("index", &Frame::index)
        .def_readwrite("loaded", &Frame::loaded)
        .def("update", &Frame::update)
        .def("__iter__", [](Frame &f) {
            return py::make_iterator(f.objects.begin(), f.objects.end());
        }, py::keep_alive<0, 1>())
        .def("keys", [](Frame &f) {  return f.objects.attr("keys")() ; })
        .def("items", [](Frame &f) { return f.objects.attr("items")() ; })
        .def("__getitem__",[](const Frame &f, std::string s) {
                 return f.objects[py::cast(s)];
             }, PYREF);

}
