import maya.cmds as cmds
import functools


def createCtrlGUI():
    
    myWin = cmds.window(title="Create NURB Control", width = 300, height = 70)
    rowColumn = cmds.rowColumnLayout(nc=3, cw=[(1, 300), (2, 10), (3,130)], columnAttach=[(1, "both", 2), (2, "left", 3), (3, "both", 5)], cs=(2, 2), rs=(2,2))
    
    cmds.text("Controls:", al="left", parent = rowColumn)
    cmds.separator(style="none", parent = rowColumn) 
    cmds.text("Functions:", al="left", parent = rowColumn)
    
    row1 = cmds.rowLayout(numberOfColumns=3, p=rowColumn, cw3=(100,100,100))
    cmds.button(label="Locator",command=functools.partial(locator), parent=row1, width = 100)
    cmds.button(label="Circle", command=functools.partial(nurbCircle), parent=row1, width = 100)
    cmds.button(label="Sphere", command=functools.partial(nurbSphere), parent = row1, width = 100)
    cmds.separator(style="single", parent = rowColumn)
    cmds.button(label="Freeze Selected", command="cmds.makeIdentity(apply=True)", parent = rowColumn)
    
    row2 = cmds.rowLayout(numberOfColumns=3, p=rowColumn, cw3=(100,100,100))
    cmds.button(label="Square", command=functools.partial(nurbSquare), parent = row2, width = 100)
    cmds.button(label="Cube", command=functools.partial(nurbCube), parent = row2, width = 100)
    cmds.button(label="Pyramid", command=functools.partial(nurbPyramid), parent = row2, width = 100)
    cmds.separator(style="single", parent = rowColumn)
    cmds.button(label="Match to Selected", command="cmds.matchTransform()", parent = rowColumn)
    
    row3 = cmds.rowLayout(numberOfColumns=3, p=rowColumn, cw3=(100,100,100))
    cmds.button(label="Diamond", command=functools.partial(nurbDiamond), parent = row3, width = 100)
    cmds.separator(style="single", parent = rowColumn)
    cmds.button(label="Select CVs", parent = rowColumn, command=functools.partial(cvSelect))  
        
    cmds.separator(style="double", parent = rowColumn)  
    cmds.separator(style="double", parent = rowColumn) 
    cmds.separator(style="double", parent = rowColumn) 
    
    colourRow = cmds.rowLayout(numberOfColumns=2, p=rowColumn, cw2=(100,100))
    cmds.text("Colour:", al="left", parent = colourRow)
    cmds.optionMenu("colDropdown", parent = colourRow, changeCommand=functools.partial(sliderChange))
    cmds.menuItem("Index")
    cmds.menuItem("RGB")
    cmds.separator(style="single", parent = rowColumn)
    cmds.button(label="Update Colour", parent = rowColumn, command=functools.partial(colUpdate))
    
    sliderColumn = cmds.columnLayout(w=300, adj=True, parent = rowColumn)                #Ugly implementation, but both sliders are technically
    cmds.colorIndexSliderGrp("index", parent = sliderColumn, min=1, max=32, value=1, h=20)    # Drawn at all times, we just change the column width
    cmds.colorSliderGrp("rgb", parent = sliderColumn, h=1)                                # Depending on which is selected.
    
    cmds.separator(style="single", parent = rowColumn)
    cmds.button(label="Close", command=functools.partial(closeWindow,myWin), parent = rowColumn)
    
    cmds.showWindow(myWin)     

def locator(*pArgs):
    locator = cmds.spaceLocator()
    cleanupCtrl("locator1", locator[0])

def nurbCircle(*pArgs):
    circleCurve = cmds.circle()
    cleanupCtrl("nurbsCircle1", circleCurve[0])
    
def nurbSquare(*pArgs):
    square = cmds.nurbsSquare()
    cleanupCtrl("nurbsSquare1", square[0])

def nurbSphere(*pArgs):
    circle1 = cmds.circle()
    
    circle2 = cmds.circle()
    cmds.xform(r=True, ro=[90,0,0])

    circle3 = cmds.circle()
    cmds.xform(r=True, ro=[0,90,0])
    
    freeze(circle1[0], circle2[0], circle3[0])
    cleanupCtrl("nurbsSphere1", circle1[0], circle2[0], circle3[0])
    
def nurbCube(*pArgs):
    square1 = cmds.nurbsSquare()
    cmds.xform(r=True, t=[-0.5,0,0], ro=[0,90,0])
    
    square2 = cmds.nurbsSquare()
    cmds.xform(r=True, t=[0.5,0,0], ro=[0,-90,0])
    
    square3 = cmds.nurbsSquare()
    cmds.xform(r=True, t=[0,0,-0.5])
    
    square4 = cmds.nurbsSquare()
    cmds.xform(r=True, t=[0,0,0.5])
    
    freeze(square1[0], square2[0], square3[0], square4[0])
    cleanupCtrl("nurbsCube1", square1[0], square2[0], square3[0], square4[0])
    
def nurbPyramid(*pArgs):
    
    dirList = ["top", "left", "bottom", "right"]
    xcoordList = (0.5, 0.5, -0.5, -0.5)
    zcoordList = (0.5, 0-.5, -0.5, 0.5)
    pivotList = ([45,0,-45], [0,-45,-45], [-45,0,-45], [0,45,-45])
    
    pyrSides = cmds.nurbsSquare()
    
    cmds.xform(r=True, ro=[90,0,0])

    for i in range(len(dirList)):
        relativeList = cmds.listRelatives(pyrSides[0])
        cmds.rename(relativeList[i], "%s%s" % (dirList[i], pyrSides[0]))
        cmds.move(xcoordList[i], 0, zcoordList[i],  "%s%s.scalePivot" % (dirList[i], pyrSides[0]), "%s%s.rotatePivot" % (dirList[i], pyrSides[0]), absolute=True)
        cmds.select("%s" % dirList[i] + "%s" % pyrSides[0])
        cmds.xform(r=True, ro=pivotList[i])
        
    pyrBase = cmds.nurbsSquare()
    cmds.xform(r=True, ro=[90,0,0])
    
    freeze(pyrSides[0], pyrBase[0])
    cleanupCtrl("nurbsPyramid1", pyrSides[0], pyrBase[0])
    
    
def nurbDiamond(*pArgs):
    
    nurbPyramid()
    cmds.pickWalk(direction="up")
    bottomHalf = cmds.ls(selection=True)
    
    nurbPyramid()
    cmds.pickWalk(direction="up")
    topHalf = cmds.ls(selection=True)
    cmds.xform(r=True, ro=[180,0,0])
    
    
    freeze(topHalf[0])
    cleanupCtrl("nurbsDiamond1", bottomHalf[0], topHalf[0])
    
def cleanupCtrl(name, *pArgs):

    newGrp = cmds.group(em=True)                #Create new grp curves to be parented to
    holdGrp = cmds.group(em=True)
    pArgsList = pArgs                            #List all additional args
      
    for i in range(len(pArgsList)):                #For each arg
        
        pArgsCurves = cmds.listRelatives(pArgsList[i])        # List all children
        cmds.parent(pArgsCurves, holdGrp, shape=True, relative=True)  # Send to holding grp.
        cmds.delete(pArgsList[i])
        
    updatedName = cmds.rename(newGrp, name)                # Repeats same operation inefficiently but shorter in the long run
    pArgsCurves = cmds.listRelatives(holdGrp) 
        
    for i in range(len(pArgsCurves)):
        
        currentVal = pArgsCurves[i]                            #Since all curves thrown blindly into holdGrp
        pArgsCurves[i] = cmds.listRelatives(pArgsCurves[i])    #Need to sort transforms from shapes (we want the latter)
        if pArgsCurves[i] is None:                                #This will attempt to find shapes, nullifed if fail.
            pArgsCurves[i] = currentVal

        cmds.parent(pArgsCurves[i], updatedName, shape=True, relative=True)    #Parent to new root grp
        cmds.rename(pArgsCurves[i], "%s" % updatedName + "Ctrl1")   
             
                                                                                # Kill additional args' empty grps
    cmds.delete(updatedName, constructionHistory=True)                            # Clear history
    cmds.delete(holdGrp)                                                          #Rename node 
    cmds.select(updatedName)                                                        # Rename each curve to avoid clashes later  
    
def freeze(*pArgs):
    cmds.select(pArgs)
    cmds.makeIdentity(apply=True) 

def sliderChange(*pArgs):

    tracker = cmds.optionMenu("colDropdown", q=True, value=True) 

    if tracker == "Index":
        cmds.colorIndexSliderGrp("index", edit=True, h=20)
        cmds.colorSliderGrp("rgb", edit=True, h=1)
        
    if tracker == "RGB":
        cmds.colorIndexSliderGrp("index", edit=True, h=1)
        cmds.colorSliderGrp("rgb", edit=True, h=20)
        
def colUpdate(*pArgs):
    
    tracker = cmds.optionMenu("colDropdown", q=True, value=True) 
    shapeList = cmds.ls(sl=True)
    
    for i in range(len(shapeList)):
        cmds.setAttr("%s.overrideEnabled" % shapeList[i], 1)
        
        if tracker == "Index":
            index = cmds.colorIndexSliderGrp("index", q=True, value=True)
            cmds.setAttr("%s.overrideRGBColors" % shapeList[i], 0)
            cmds.setAttr("%s.overrideColor" % shapeList[i], index-1)
            
        if tracker == "RGB":
            rgb = cmds.colorSliderGrp("rgb", q=True, rgbValue=True)
            cmds.setAttr("%s.overrideRGBColors" % shapeList[i], 1)
            
            cmds.setAttr("%s.overrideColorRGB" % shapeList[i], rgb[0], rgb[1], rgb[2])
        
        
def cvSelect(*pArgs):
    
    selected = cmds.ls(sl=True)
    cmds.select(clear=True)
    for i in range(len(selected)):
        shapes = cmds.listRelatives(selected[0], s=True)  
        for i in range(len(shapes)):
            spans = cmds.getAttr("%s.spans" % shapes[i])
            degree = cmds.getAttr("%s.degree" % shapes[i])
            numCVs = (spans+degree) - 1
            
            cmds.select("%s.cv[0:%i]" % (shapes[i], numCVs), add=True)
        
def closeWindow(myWin, *pArgs ):
    if cmds.window(myWin, exists=True):
        cmds.deleteUI(myWin) 
        
createCtrlGUI()