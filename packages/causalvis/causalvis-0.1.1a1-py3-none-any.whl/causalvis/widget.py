import json
import pandas as pd

import ipywidgets as widgets
from traitlets import Unicode, Dict, List, TraitError

import sys

# The following function is adapted from Anywidget,
# with thanks to Trevor Mantz for figuring this out
_WIDGET_MIME_TYPE = "application/vnd.jupyter.widget-view+json"
_PLAIN_TEXT_MAX_LEN = 110

# The following function is adapted from Anywidget,
# with thanks to Trevor Mantz for figuring this out
def get_repr_metadata():
    if ("google.colab.output" in sys.modules):
        sys.modules["google.colab.output"].enable_custom_widget_manager()

        url = sys.modules["google.colab.output"]._widgets._installed_url  # noqa: SLF001

        if url is None:
            return {}

        return {_WIDGET_MIME_TYPE: {"colab": {"custom_widget_manager": {"url": url}}}}

# The following function is adapted from Anywidget,
# with thanks to Trevor Mantz for figuring this out
def repr_mimebundle(model_id, repr_text):
    """Create a MIME bundle for a widget representation."""
    data = {
        "text/plain": repr_text,
        _WIDGET_MIME_TYPE: {
            "model_id": model_id,
        },
    }
    return data, get_repr_metadata()

class BaseWidget(widgets.DOMWidget):
    """An example widget."""
    _view_name = Unicode('ReactView').tag(sync=True)
    _model_name = Unicode('ReactModel').tag(sync=True)
    _view_module = Unicode('causalvis').tag(sync=True)
    _model_module = Unicode('causalvis').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    component = Unicode().tag(sync=True)
    props = Dict().tag(sync=True)
    value = Unicode('test').tag(sync=True)
    # DAG = Unicode('').tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__()

        self.component = self.__class__.__name__
        self.props = kwargs

    def update_prop(self, prop_name, prop_value):
        self.props = {**self.props, prop_name: prop_value}

    # The following function is adapted from Anywidget,
    # with thanks to Trevor Mantz for figuring this out
    def _repr_mimebundle_(self, **kwargs):  # noqa: ARG002
        plaintext = repr(self)
        if len(plaintext) > _PLAIN_TEXT_MAX_LEN:
            plaintext = plaintext[:110] + "…"
        if self._view_name is None:
            return None  # type: ignore[unreachable]
        return repr_mimebundle(model_id=self.model_id, repr_text=plaintext)

class DAGBaseWidget(widgets.DOMWidget):
    """An example widget."""
    _view_name = Unicode('DAGView').tag(sync=True)
    _model_name = Unicode('DAGModel').tag(sync=True)
    _view_module = Unicode('causalvis').tag(sync=True)
    _model_module = Unicode('causalvis').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    component = Unicode().tag(sync=True)
    props = Dict().tag(sync=True)
    DAG = Dict().tag(sync=True)
    colliders = List().tag(sync=True)
    mediators = List().tag(sync=True)
    confounds = List().tag(sync=True)
    prognostics = List().tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__()

        self.component = self.__class__.__name__
        self.props = kwargs

    def update_prop(self, prop_name, prop_value):
        self.props = {**self.props, prop_name: prop_value}

    # The following function is adapted from Anywidget,
    # with thanks to Trevor Mantz for figuring this out
    def _repr_mimebundle_(self, **kwargs):  # noqa: ARG002
        plaintext = repr(self)
        if len(plaintext) > _PLAIN_TEXT_MAX_LEN:
            plaintext = plaintext[:110] + "…"
        if self._view_name is None:
            return None  # type: ignore[unreachable]
        return repr_mimebundle(model_id=self.model_id, repr_text=plaintext)

class CohortBaseWidget(widgets.DOMWidget):
    """An example widget."""
    _view_name = Unicode('CohortView').tag(sync=True)
    _model_name = Unicode('CohortModel').tag(sync=True)
    _view_module = Unicode('causalvis').tag(sync=True)
    _model_module = Unicode('causalvis').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    component = Unicode().tag(sync=True)
    props = Dict().tag(sync=True)
    selection = Dict().tag(sync=True)
    iselection = Dict().tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__()

        self.component = self.__class__.__name__
        self.props = kwargs

    def update_prop(self, prop_name, prop_value):
        self.props = {**self.props, prop_name: prop_value}

    # The following function is adapted from Anywidget,
    # with thanks to Trevor Mantz for figuring this out
    def _repr_mimebundle_(self, **kwargs):  # noqa: ARG002
        plaintext = repr(self)
        if len(plaintext) > _PLAIN_TEXT_MAX_LEN:
            plaintext = plaintext[:110] + "…"
        if self._view_name is None:
            return None  # type: ignore[unreachable]
        return repr_mimebundle(model_id=self.model_id, repr_text=plaintext)

class VersionHistoryWidget(widgets.DOMWidget):
    """An example widget."""
    _view_name = Unicode('VersionHistoryView').tag(sync=True)
    _model_name = Unicode('VersionHistoryModel').tag(sync=True)
    _view_module = Unicode('causalvis').tag(sync=True)
    _model_module = Unicode('causalvis').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    component = Unicode().tag(sync=True)
    props = Dict().tag(sync=True)
    DAG = Dict().tag(sync=True)
    cohort = List().tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__()

        self.component = self.__class__.__name__
        self.props = kwargs

    def update_prop(self, prop_name, prop_value):
        self.props = {**self.props, prop_name: prop_value}

    # The following function is adapted from Anywidget,
    # with thanks to Trevor Mantz for figuring this out
    def _repr_mimebundle_(self, **kwargs):  # noqa: ARG002
        plaintext = repr(self)
        if len(plaintext) > _PLAIN_TEXT_MAX_LEN:
            plaintext = plaintext[:110] + "…"
        if self._view_name is None:
            return None  # type: ignore[unreachable]
        return repr_mimebundle(model_id=self.model_id, repr_text=plaintext)

"""
Read and convert a networkx graph into a python Dict

Props:
  - nx_graph: graph in networkx format
"""
def load_nx(nx_graph):
  from networkx.readwrite import json_graph
  import networkx as nx

  pos=nx.spring_layout(nx_graph)

  newPos = {}

  # get x, y layout values for each node
  for p in pos:
      value = pos[p]
      newPos[p] = {"x": value[0], "y": value[1]}

  nx.set_node_attributes(nx_graph,newPos)
  data = json_graph.node_link_data(nx_graph, {"link": "links", "source": "source", "target": "target", "name": "name"})

  nodelink = {}
  nodelink["nodes"] = data["nodes"]
  nodelink["links"] = data["links"]

  return nodelink

"""
The following function initializes the DAG widget
Only one of the input props should be specified, if multiple props are provided,
props will be processed in order of preference as listed below
Input props with the most information (graphs) are prioritized
If no input props are provided, the DAG is initialized as an empty svg

Props:
  - graph: Dict, json formatted graph data of {nodes: [...], links: [...]}
  - nx_graph: NetworkX graph
  - attributes: List, attribute names
  - data: pandas DataFrame
""" 
@widgets.register
class DAG(DAGBaseWidget):
    def __init__(self, graph=None, nx_graph=None, attributes=None, data=None, **kwargs):
        
        if graph:
          self.graph = graph
          self.attributes = None
        elif nx_graph:
          self.graph = load_nx(nx_graph)
          self.attributes = None
        elif attributes:
          self.attributes = sorted(attributes, key=str.lower)
          self.graph = None
        elif data is not None:
          self.attributes = sorted(list(data), key=str.lower)
          self.graph = None
        else:
          self.attributes = []
          self.graph = None
        
        super().__init__(
            attributes=self.attributes,
            graph=self.graph,
            **kwargs
        )

@widgets.register
class CohortEvaluator(CohortBaseWidget):
    def __init__(self, unadjustedCohort, adjustedCohort=[], treatment="treatment", propensity="propensity", **kwargs):
        
        self.unadjustedCohort = unadjustedCohort
        self.adjustedCohort = adjustedCohort
        self.treatment = treatment
        self.propensity = propensity

        # print("here", self.data)
        
        super().__init__(
            unadjustedCohort=self.unadjustedCohort,
            adjustedCohort=self.adjustedCohort,
            treatment=self.treatment,
            propensity=self.propensity,
            **kwargs
        )

@widgets.register
class TreatmentEffectExplorer(BaseWidget):
    def __init__(self, data=[], treatment="treatment", outcome="outcome", **kwargs):
        
        self.data = data
        self.treatment = treatment
        self.outcome = outcome

        # print("here", self.data)
        
        super().__init__(
            data=self.data,
            treatment=self.treatment,
            outcome=self.outcome,
            **kwargs
        )

@widgets.register
class VersionHistory(VersionHistoryWidget):
    def __init__(self, effect="effect", **kwargs):
        
        self.versions = []
        self.effect = effect

        # print("here", self.data)
        
        super().__init__(
            versions = self.versions,
            effect = effect,
            **kwargs
        )

    def addVersion(self, v):
        try:
            assert(len(v) == 3)
        except AssertionError:
            raise TraitError("The VersionHistory module expects input in the form of (DAG, Cohort, ATE), got {count}".format(len(newHistory)))
            return

        try:
            assert(type(v[0]) == dict)
        except AssertionError:
            raise TraitError("Invalid DAG type, expected dict")
            return

        try:
            assert(type(v[1]) == pd.core.frame.DataFrame)
        except AssertionError:
            raise TraitError("Invalid Cohort type, expected pandas DataFrame")
            return

        try:
            assert(type(v[2]) == float)
        except AssertionError:
            raise TraitError("Invalid ATE type, expected float")
            return

        newVersion = {}
        newVersion["DAG"] = v[0]
        newVersion["Cohort"] = v[1].to_dict(orient="records")
        newVersion["ATE"] = v[2]

        newVersions = self.versions + [newVersion]

        self.versions = newVersions
        self.update_prop("versions", newVersions)

    def versionCount(self):
        print(len(self.versions))

    def saveVersions(self, filename="./versions.json"):
        # allVersions = []

        # for v in self.versions:
        #     newV = {}
        #     newV["DAG"] = v[0]
        #     newV["Cohort"] = v[1].to_json(orient="records")
        #     newV["ATE"] = v[2]

        #     allVersions.append(newV)

        with open(filename, "w") as f:
            json.dump(self.versions, f)
