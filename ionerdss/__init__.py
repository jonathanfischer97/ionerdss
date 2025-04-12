# ionerdss/__init__.py

class LazyLoader:
    """Transparent lazy module loader"""
    def __init__(self, module_path, attribute=None):
        self.module_path = module_path
        self.attribute = attribute
        self.loaded_module = None
        self.loaded_attribute = None
    
    def __call__(self, *args, **kwargs):
        """Support calling the lazy-loaded object directly"""
        if self.loaded_attribute is None:
            if self.loaded_module is None:
                import importlib
                self.loaded_module = importlib.import_module(self.module_path, package="ionerdss")
            
            self.loaded_attribute = getattr(self.loaded_module, self.attribute) if self.attribute else self.loaded_module
        
        if callable(self.loaded_attribute):
            return self.loaded_attribute(*args, **kwargs)
        raise TypeError(f"{self.attribute} is not callable")
            
    def __getattr__(self, name):
        """Access attributes of the lazy-loaded module/object"""
        if self.loaded_module is None:
            import importlib
            self.loaded_module = importlib.import_module(self.module_path, package="ionerdss")
        
        if self.attribute:
            if self.loaded_attribute is None:
                self.loaded_attribute = getattr(self.loaded_module, self.attribute)
            return getattr(self.loaded_attribute, name)
        return getattr(self.loaded_module, name)

# Lazily load core classes
Model = LazyLoader('.nerdss_model.model', 'Model')
MoleculeType = LazyLoader('.nerdss_model.model', 'MoleculeType')
MoleculeInterface = LazyLoader('.nerdss_model.model', 'MoleculeInterface')
ReactionType = LazyLoader('.nerdss_model.model', 'ReactionType')
Coords = LazyLoader('.nerdss_model.coords', 'Coords')
PDBModel = LazyLoader('.nerdss_model.pdb_model', 'PDBModel')
DesignModel = LazyLoader('.nerdss_model.design_model', 'DesignModel')
PlantonicSolidsModel = LazyLoader('.nerdss_model.platonic_solids_model', 'PlantonicSolidsModel')
ParseComplexes = LazyLoader('.nerdss_model.complex', 'generate_ode_model_from_pdb')

# Lazily load simulation and analysis modules
Simulation = LazyLoader('.nerdss_simulation.simulation', 'Simulation')
Analysis = LazyLoader('.nerdss_analysis.analysis', 'Analysis')

def configure_plotting():
    """Configure plotting styles - only call this when you're ready to plot."""
    import seaborn as sns
    fontsize = 12
    sns.set_style("ticks")
    sns.set_context("paper", rc={
        "font.size": fontsize,
        "axes.titlesize": fontsize,
        "axes.labelsize": fontsize,
        "xtick.labelsize": fontsize,
        "ytick.labelsize": fontsize,
        "legend.fontsize": fontsize,
        "font.family": "serif"
    })

# Version information - only computed when __version__ is accessed
def _get_version():
    try:
        import pkg_resources
        return pkg_resources.get_distribution("ioNERDSS").version
    except:
        return "unknown"

# Define __version__ as a property
class VersionProperty:
    def __get__(self, obj, objtype=None):
        return _get_version()

class _ModuleProperties:
    __version__ = VersionProperty()

# Apply the properties
import sys
sys.modules[__name__].__class__ = type("ionerdss", (sys.modules[__name__].__class__, _ModuleProperties), {})