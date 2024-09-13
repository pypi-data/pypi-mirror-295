// Cytosim was created by Francois Nedelec. Copyright 2007-2017 EMBL.
/**
 This is a program to analyse simulation results:
 it reads a trajectory-file, and provides a python interface to it.
   
   * @TODO :    - manage to return ObjectSet from simul, in order to not necessitate frame()
                - bead and sphere
                - live player + python ? o_O
                - specialized classes, including dynamic spaces
                - and so on and so forth
*/


/**

  To use in python : move the cytosim...._.so file to a folder with *.cmo files
    We recommend using cym/aster.cym for a demo.
   
    Then run : 
        
    import cytosim
    sim = cytosim.open()
    sim.prop.timestep 
    frame = cytosim.load(0)
    fibers = frame["microtubule"]
    fibers.prop.segmentation = 1.337    # <- Yes, yes, yes.
    fibers[0].points()
    fibers[0].id()
    fibers[0].join(fibers[1]) # <- yes, indeed
    core = frame["core"][0]
    core.points()
    while frame.loaded:
        print(frame.time)
        frame = frame.next()
         

    OR, IN LIVE MODE !

    sim = cytosim.start('cym/aster.cym')
    fibers = sim.fibers
    fibers[0].join(fibers[1])    # <- Yes, yes, yes. 
    sim.run(10)
     
    # etc...
*/

/*
@TODO : an interface for FiberSet (problem : cannot iterate because of FiberSet interface)
@TODO : support input arguments
 */
#include "pycytosim.h"

namespace py = pybind11;

/**
 * @brief Open the simulation from the .cmo files
 * @return 
 */
PythonParser * open()
{   
    
    int verbose = 1;
    int prefix = 0;
    
    Glossary arg;

    std::string input = TRAJECTORY;
    std::string str;

    Simul * sim = new Simul;
    
    unsigned period = 1;

    arg.set(input, ".cmo") || arg.set(input, "input");    
    if ( arg.use_key("-") ) verbose = 0;

    PythonParser * pyParse = new PythonParser(*sim);

    try
    {
        RNG.seed();
        sim->loadProperties();
        pyParse->activate(input);
        Cytosim::all_silent();
        
    }
    catch( Exception & e )
    {
        std::clog << "Aborted: " << e.what() << '\n';
        return nullptr;
    }

    return pyParse;
}

/**
 * @brief Starts a simulation from a config file fname
 * @param fname
 * @return 
 */
PythonParser * start(std::string fname) {
    int n = fname.length();
    char inp[n] ;
    std::strcpy(inp, fname.c_str());
    Glossary arg;
    arg.read_string(inp,2);
    
    if ( ! arg.use_key("+") )
    {
        Cytosim::out.open("messages.cmo");
        Cytosim::log.redirect(Cytosim::out);
        Cytosim::warn.redirect(Cytosim::out);
    }
    
    Simul * simul = new Simul;
    
    try {
        simul->initialize(arg);
    }
    catch( Exception & e ) {
        print_magenta(std::cerr, e.brief());
        std::cerr << '\n' << e.info() << '\n';
    }
    catch(...) {
        print_red(std::cerr, "Error: an unknown exception occurred during initialization\n");
    }
    
    time_t sec = TicToc::seconds_since_1970();
    
    std::string file = simul->prop->config_file;
    std::string setup = file;
    
    PythonParser * pyParse = new PythonParser(*simul);
    pyParse->activate();
    
    return pyParse;
}

/**
 * @brief A python module to run or play cytosim
 * @return 
 */
PYBIND11_MODULE(cytosim, m) {
    m.doc() = 
				"import cytosim \n"
				"parser = cytosim.open() \n"
                "sim = parser.simul \n"
                "sim.prop.timestep \n"
                "parser.load(0) \n"
                "frame = parser.frame() \n"
                "fibers = frame['microtubule'] \n"
                "print(len(fibers)) \n"
                "while parser.next(): \n"
                "    print(sim.time()) \n"
                " \n"
                "# --- OR --- \n"
                " \n"
                "parser = cytosim.start('cym/aster.cym') \n"
                "sim = parser.simul \n"
                "fibers = sim.fibers \n"
                "fibers[0].join(fibers[1]) \n"
                "parser.run(10) \n"; // optional module docstring
    
    /// Loading properties into the module
    load_thread_classes(m);
    load_interface_classes(m);
    load_object_classes(m);
    load_meca_classes(m);
    load_point_classes(m);
    auto pysim = load_simul_classes(m);
    load_glossary_classes(m);
    load_solid_classes(m);
    load_fiber_classes(m);
    load_hand_classes(m);
    load_space_classes(m);
    load_single_classes(m);
    load_couple_classes(m);
    load_organizer_classes(m);
    
    /// We declare object groups
    // We can later add additional def to any of these groups
    //auto fibs = declare_group(m, ObjGroup<Fiber,FiberProp>(), ObjVec<Fiber>(), "Fiber");
    auto fibs = declare_group(m, ObjGroup<Fiber,FiberProp>(), "FiberGroup");
    auto sols = declare_group(m, ObjGroup<Solid,SolidProp>(), "SolidGroup");
    auto spas = declare_group(m, ObjGroup<Space,SpaceProp>(), "SpaceGroup");
    auto beds = declare_group(m, ObjGroup<Bead,BeadProp>(), "BeadGroup");
    auto sfrs = declare_group(m, ObjGroup<Sphere,SphereProp>(), "SphereGroup");
    auto orgs = declare_group(m, ObjGroup<Organizer,Property>(), "OrganizerGroup");
    auto sins = declare_group(m, ObjGroup<Single,SingleProp>(), "SingleGroup");
    auto cous = declare_group(m, ObjGroup<Couple,CoupleProp>(), "CoupleGroup");
    
    declare_lattice(m, (uint8_t)1, "Lattice_uint8");
    declare_lattice(m, (uint16_t)1, "Lattice_uint16");
    declare_lattice(m, (uint64_t)1, "Lattice_uint64");
    declare_lattice(m, (uint32_t)1, "Lattice_uint32");
    declare_lattice(m, (real)1.0, "Lattice_real");
    
    /// Opens the simulation from *.cmo files
    m.def("open", &open, "@PYD;C:PyCytosim;T:loads simulation from object files", PYREF);
    m.def("start", &start, "@PYD;C:PyCytosim;T:loads simulation from config files", PYREF);
    m.def("str_to_glos", &str_to_glos, "@PYD;C:PyCytosim;T:converts string to Glossary");


    
}

