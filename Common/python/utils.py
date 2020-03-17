from __future__ import print_function
from collections import defaultdict

import FWCore.ParameterSet.Config as cms

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

def getModuleDependencies(module):
    ret = []
    for _ikey in module.parameters_():
        if not hasattr(module, _ikey):
           raise RuntimeError('key "'+_ikey+'" not found in module: '+module.dumpPython())
        ret += getParameterDependencies(getattr(module, _ikey))
    return ret

def processHasModule(process, module):
    if hasattr(process, module):
       return True

#    for _tmp in process.es_sources_():
#        print(_tmp, '=', getattr(process, _tmp).dumpPython())
#    for _tmp in process.es_prefers_():
#        print(_tmp, '=', getattr(process, _tmp).dumpPython())
#    for _tmp in process.es_producers_():
#        print(_tmp, '=', getattr(process, _tmp).dumpPython())

    return False

def moduleDependencyDictFromSequence(process, sequence):
    ret = {}
    for _modname in getattr(process, sequence).moduleNames():
        if not hasattr(process, _modname):
           raise RuntimeError(_modname)
        ret[_modname] = getModuleDependencies(getattr(process, _modname))
        # remove duplicates
        ret[_modname] = sorted(list(set(ret[_modname])))
        # retain only labels corresponding to a member of process (ignore dependencies from collections in input EDM file)
        ret[_modname] = [_tmp for _tmp in ret[_modname] if (_tmp and processHasModule(process, _tmp))]
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
