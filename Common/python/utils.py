from __future__ import print_function
import FWCore.ParameterSet.Config as cms
from collections import defaultdict

def getParameterDependencies(parameter):
    ret = []
    if (type(parameter) == cms.string):
       ret += [parameter.value()]
    elif (type(parameter) == cms.vstring):
       for _parStr in parameter:
           ret += [str(_parStr)]
    elif (type(parameter) == cms.InputTag):
       ret += [parameter.getModuleLabel()]
    elif (type(parameter) == cms.VInputTag):
       for parameterTag in parameter:
           if isinstance(parameterTag, str):
              parameterTag = cms.InputTag(parameterTag)
           ret += [parameterTag.getModuleLabel()]
    elif (type(parameter) == cms.PSet):
       for _psetParName in parameter.parameterNames_():
           ret += getParameterDependencies(parameter.getParameter(_psetParName))
    elif (type(parameter) == cms.VPSet):
       for _parPSet in parameter:
           for _psetParName in _parPSet.parameterNames_():
               ret += getParameterDependencies(_parPSet.getParameter(_psetParName))
    return ret

def moduleDependencyDictFromSequence(process, sequence):
    ret = {}
    for _modname in getattr(process, sequence).moduleNames():
        ret[_modname] = []
        if not hasattr(process, _modname):
           raise RuntimeError(_modname)
        _mod = getattr(process, _modname)
        for _ikey in _mod.parameters_():
            if not hasattr(_mod, _ikey):
               raise RuntimeError(_modname+'.'+_ikey)
            ret[_modname] += getParameterDependencies(getattr(_mod, _ikey))
        # remove duplicates
        ret[_modname] = sorted(list(set(ret[_modname])))
        # retain only labels corresponding to a member of process (ignore dependencies from collections in input EDM file)
        ret[_modname] = [_tmp for _tmp in ret[_modname] if (_tmp and hasattr(process, _tmp))]
    # verify absence of self-dependencies and circular-dependencies
    for _modname in ret:
        for _dep in ret[_modname]:
            if _dep == _modname:
               raise RuntimeError('list of dependencies for element "'+_modname+'" includes the element itself')
            if _dep in ret and _modname in ret[_dep]:
               raise RuntimeError('circular dependency between "'+_modname+'" and "'+_dep+'"')
    return ret

# ref: https://www.codespeedy.com/topological-sorting-in-python/
class Graph:
    def __init__(self, directed=True):
        self.graph = defaultdict(list)
        self.directed = directed
    def addEdge(self, frm, to):
        self.graph[frm].append(to)
        if self.directed is False:
            self.graph[to].append(frm)
        else:
            self.graph[to] = self.graph[to]
    def topoSortVisit(self, s, visited, sortlist):
        visited[s] = True
        for i in self.graph[s]:
            if not visited[i]:
               self.topoSortVisit(i, visited, sortlist)
        sortlist.insert(0, s)
    def topoSort(self):
        visited = {i: False for i in self.graph}
        sortlist = []
        for v in self.graph:
            if not visited[v]:
               self.topoSortVisit(v, visited, sortlist)
        return sortlist

def orderedListOfModuleNamesFromSequence(process, sequence):
    depeDict = moduleDependencyDictFromSequence(process, sequence)
    depeGraph = Graph(directed=True)
    moduleNames = sorted(list(getattr(process, sequence).moduleNames()))
    for _tmp in depeDict:
        for _tmp2 in depeDict[_tmp]:
            if _tmp2 in moduleNames:
               depeGraph.addEdge(moduleNames.index(_tmp2), moduleNames.index(_tmp))
    return [moduleNames[_tmp] for _tmp in depeGraph.topoSort()]
