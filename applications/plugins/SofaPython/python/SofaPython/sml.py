import Sofa

import os.path
import math
import xml.etree.ElementTree as etree 

import Quaternion
import Tools
from Tools import listToStr as concat
import units

def parseIdName(obj,objXml):
    """ set id and name of obj
    """
    obj.id = objXml.attrib["id"]
    obj.name = obj.id
    if not objXml.find("name") is None:
        obj.name = objXml.find("name").text

class Model:

    class Mesh:

        class Group:
            pass
        
        def __init__(self, meshXml):
            self.format = meshXml.find("source").attrib["format"]
            self.source = meshXml.find("source").text
        
            self.group=dict()
            self.data=dict()
            for g in meshXml.iter("group"):
                self.group[g.attrib["id"]] = Mesh.Group()
                self.group[g.attrib["id"]].index = Tools.strToListInt(g.find("index").text)
                self.group[g.attrib["id"]].data = dict()
                for d in g.iter("data"):
                    self.group[g.attrib["id"]].data[d.attrib["name"]]=parseData(d)                    
    
    class Rigid:
        def __init__(self, objXml):
            parseIdName(self,objXml)
            self.position=Tools.strToListFloat(objXml.find("position").text)
            self.mesh = None
            if not objXml.find("density") is None:
                self.density=float(objXml.find("density").text)
            if not objXml.find("mass") is None:
                self.mass = float(objXml.find("mass").text)
            
    #class JointGeneric:
        #def __init__(self, name="Unknown",object1,offset1,object2,offset2):
        #pass
    class Deformable:
        def __init__(self,objXml):
            parseIdName(self,objXml)
            self.position = Tools.strToListFloat(objXml.find("position").text)
            self.mesh = None
            self.indices=dict()
            self.weights=dict()
    
    dofIndex={"x":0,"y":1,"z":2,"rx":3,"ry":4,"rz":5}
    
    def __init__(self, filename, name=None):
        self.name=os.path.basename(filename)
        self.modelDir = os.path.dirname(filename)
        self.units=dict()
        self.meshes=dict()
        self.rigids=dict()
        #self.rigidsbyType=dict()
        self.jointGenerics=dict()
        self.deformables=dict()
        #self.deformablesByType=dict()
        
        with open(filename,'r') as f:
            # TODO automatic DTD validation could go here, not available in python builtin ElementTree module
            modelXml = etree.parse(f).getroot()
            if name is None:
                self.name = modelXml.attrib["name"]

            # units
            self.parseUnits(modelXml)
            # meshes
            for m in modelXml.iter("mesh"):
                if not m.find("source") is None:
                    if m.attrib["id"] in self.meshes:
                        print "WARNING: sml.Model: mesh id {0} already defined".format(m.attrib["id"])
                    mesh = Model.Mesh(m)
                    sourceFullPath = os.path.join(self.modelDir,mesh.source)
                    if os.path.exists(sourceFullPath):
                        mesh.source=sourceFullPath
                    else:
                        print "WARNING: sml.Model: mesh not found:", mesh.source
                    self.meshes[m.attrib["id"]] = mesh
                    
            # rigids
            for r in modelXml.iter("rigid"):
                if r.attrib["id"] in self.rigids:
                    print "ERROR: sml.Model: rigid defined twice, id:", r.attrib["id"]
                    continue
                rigid=Model.Rigid(r)
                self.parseMesh(rigid, r)
                self.rigids[rigid.id]=rigid
            
            # joints
            #self.parseJoints(modelXml)
            
            #deformable
            for d in modelXml.iter("deformable"):
                if d.attrib["id"] in self.deformables:
                    print "ERROR: sml.Model: deformable defined twice, id:", d.attrib["id"]
                    continue
                deformable=Model.Deformable(d)
                self.parseMesh(deformable, d)
                mesh=deformable.mesh # shortcut
                for s in d.iter("skinning"):
                    if not s.attrib["rigid"] in self.rigids:
                        print "ERROR: sml.Model: skinning for deformable {0}: rigid {1} is not defined".format(name, s.attrib["rigid"])
                        continue
                    currentBone = self.rigids[s.attrib["rigid"]].boneIndex
                    if not (s.attrib["group"] in mesh.group and s.attrib["weight"] in mesh.group[s.attrib["group"]].data):
                        print "ERROR: sml.Model: skinning for deformable {0}: group {1} - weight {2} is not defined".format(name, s.attrib["group"], s.attrib["weight"])
                        continue
                    group = mesh.group[s.attrib["group"]]
                    weight = group.data[s.attrib["weight"]]
                    for index,weight in zip(group.index, weight):
                        if not index in indices:
                            indices[index]=list()
                            weights[index]=list()
                        deformable.indices[index].append(currentBone)
                        deformable.weights[index].append(weight)
                self.deformables[deformable.id]=deformable

    def parseUnits(self, modelXml):
        xmlUnits = modelXml.find("units")
        if not xmlUnits is None:
            for u in xmlUnits.attrib:
                self.units[u]=xmlUnits.attrib[u]
                
    def parseMesh(self, obj, objXml):
        if not objXml.find("mesh") is None:
            meshId = objXml.find("mesh").attrib["id"]
            if meshId in self.meshes:
                obj.mesh = self.meshes[meshId]
            else:
                print "ERROR: sml.Model: object {0} references undefined mesh {1}".format(obj.name, meshId)

    #def parseJointGenerics(self,modelXml): 
        #for j in modelXml.iter("jointGeneric"):
            #joint=JointGeneric()
            #parseIdName(joint,j)

            #if j.attrib["id"] in self.joints:
                #print "ERROR: sml.Model: joint defined twice, id:", j.attrib["id"]
                #continue

            #frames=list()
            #for o in j.iter("object"):
                #if not o.find("offset") is None:
                    #frames.append(self.addOffset("offset_{0}".format(name), o.attrib["id"], o.find("offset")))
                #else:
                    #frames.append(self.rigids[o.attrib["id"]])
            
            #if len(frames) != 2:
                #logging.error("ERROR: Compliant.sml.scene: generic joint expect two objects, {0} specified".format(len(frames)))

            ## dofs
            #mask = [1] * 6
            #for dof in j.iter("dof"):
                #mask[dofIndex[dof.attrib["index"]]]=0
                ##TODO limits !

            #self.jointGeneric[r.attrib["id"]]=rigid

            #joint = StructuralAPI.GenericRigidJoint(name, frames[0].node, frames[1].node, mask)
            #self.jointGenerics[j.attrib["id"]] = joint
            
def insertVisual(parentNode,obj,color):
    node = parentNode.createChild("node_"+obj.name)
    translation=obj.position[:3]
    rotation = Quaternion.to_euler(obj.position[3:])  * 180.0 / math.pi
    Tools.meshLoader(node, obj.mesh.source, name="loader_"+obj.name, translation=concat(translation),rotation=concat(rotation))
    node.createObject("OglModel",src="@loader_"+obj.name, color=color)
    
def setupUnits(myUnits):
    message = "units:"
    for quantity,unit in myUnits.iteritems():
        exec("units.local_{0} = units.{0}_{1}".format(quantity,unit))
        message+=" "+quantity+":"+unit
    print message

class BaseScene:
    class Param:
        pass
    def __init__(self,parentNode,model):
        self.model=model
        self.param=BaseScene.Param()
        self.nodes = dict() # to store special nodes
        self.node=parentNode.createChild(self.model.name)

class SceneDisplay(BaseScene):
    def __init__(self,parentNode,model):
        BaseScene.__init__(self,parentNode,model)
        self.param.rigidColor="1. 0. 0."
        self.param.deformableColor="0. 1. 0."
   
    def createScene(self):
        model=self.model # shortcut
        for rigid in model.rigids.values():
            print "Display rigid:",rigid.name
            insertVisual(self.node, rigid, self.param.rigidColor)
        
        for deformable in model.deformables.values():
            print "Display deformable:",deformable.name
            insertVisual(self.node, deformable, self.param.deformableColor)
            