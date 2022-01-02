import maya.cmds as cmds
import functools


def createCtrlGUI():
    ''' Gui window setup'''

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
    
    # Want to have an Index and RGB Slider available and able to seamlessly swap between them.
    # Implementation seems very hack-y: both sliders are 'visible' at all times
    # But their heights are swapped depending upon which is active. Results in only one being actually seen at a time.

    sliderColumn = cmds.columnLayout(w=300, adj=True, parent = rowColumn)                             
    cmds.colorIndexSliderGrp("index", parent = sliderColumn, min=1, max=32, value=1, h=20)            
    cmds.colorSliderGrp("rgb", parent = sliderColumn, h=1)
    
    cmds.separator(style="single", parent = rowColumn)
    cmds.button(label="Close", command=functools.partial(closeWindow,myWin), parent = rowColumn)
    
    cmds.showWindow(myWin)     

def locator(*pArgs):
    ''' creates locator and applies universal 'clean' func to it 
    
        On Exit: 
        Locator created at origin with no construction history'''

    locator = cmds.spaceLocator()
    cleanupCtrl("locator1", locator[0])


def nurbCircle(*pArgs):
    ''' creates nurbsCircle and applies universal 'clean' func to it  
    
        On Exit: 
        nurbCircle created at origin with no construction history'''

    circleCurve = cmds.circle()
    cleanupCtrl("nurbsCircle1", circleCurve[0])

    
def nurbSquare(*pArgs):
    ''' creates nurbsSquare and applies universal 'clean' func to it  
    
        On Exit: 
        nurbSquare created at origin with no construction history'''

    square = cmds.nurbsSquare()
    cleanupCtrl("nurbsSquare1", square[0])


def nurbSphere(*pArgs):
    ''' creates a "nurbsSphere" using 3 nurbsCircles and applies universal 'clean' func to it  
    
        On Exit: 
        nurbsSphere created at origin as single object with no construction history'''

    circle1 = cmds.circle()
    circle2 = cmds.circle()
    cmds.xform(r=True, ro=[90,0,0])
    circle3 = cmds.circle()
    cmds.xform(r=True, ro=[0,90,0])
    
    freeze(circle1[0], circle2[0], circle3[0])
    cleanupCtrl("nurbsSphere1", circle1[0], circle2[0], circle3[0])

    
def nurbCube(*pArgs):
    ''' creates a "nurbsCube" using 4 nurbsSquares and applies universal 'clean' func to it 
    
        On Exit: 
        nurbCube created at origin as single object with no construction history'''

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
    ''' creates a "nurbsPyramid" using 2 nurbsSquares and applies universal 'clean' func to it 
    
        On Exit: 
        nurbPyramid created at origin as single object with no construction history'''
    
    # The four lists are used to transform and format each edge of a nurbsSquare into the angled 'point' of the pyramid.
    dirList = ["top", "left", "bottom", "right"]
    xcoordList = (0.5, 0.5, -0.5, -0.5)
    zcoordList = (0.5, 0-.5, -0.5, 0.5)
    pivotList = ([45,0,-45], [0,-45,-45], [-45,0,-45], [0,45,-45])
    
    pyrSides = cmds.nurbsSquare()
    
    cmds.xform(r=True, ro=[90,0,0])

    for i in range(len(dirList)):

        # Rename each edge and position according to placement.
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
    ''' creates a "nurbsDiamond" using 2 nurbsDiamond and applies universal 'clean' func to it 
    
        On Exit: 
        nurbsDiamond created at origin as single object with no construction history'''
    
    # Create 2 pyramids and label their edges as either the top or bottom of the diamond, and rotate the latter upside-down.
    nurbPyramid()
    cmds.pickWalk(direction="up")
    bottomHalf = cmds.ls(selection=True)
    
    nurbPyramid()
    cmds.pickWalk(direction="up")
    topHalf = cmds.ls(selection=True)
    cmds.xform(r=True, ro=[180,0,0])
    
    # Bottom half already frozen as it hasn't been altered since creation, and pyramids are already frozen at creation.
    freeze(topHalf[0])
    cleanupCtrl("nurbsDiamond1", bottomHalf[0], topHalf[0])
    
def cleanupCtrl(name, *pArgs):
    ''' cleanup function to remove construction leftovers and parent multiple individual curves under a single group/shape
        
        name: final name of the shape when process is finished (e.g. "nurbsPyramid1")
        
        On Exit:
        All individual curves comprising the complex shapes are parented under a single group.'''

    #Create new grps for curves to be parented to
    newGrp = cmds.group(em=True)                
    holdGrp = cmds.group(em=True)
    
    #List all args provided.
    pArgsList = pArgs                            
      
    for i in range(len(pArgsList)):
        # Create list of all children of items in list and parent them to a temporary holding group.
        # The original parent groups to these children are deleted.
        pArgsCurves = cmds.listRelatives(pArgsList[i])
        cmds.parent(pArgsCurves, holdGrp, shape=True, relative=True)
        cmds.delete(pArgsList[i])

    # Rename final group to given name and initialize variable with updated name.
    # I.e it attempts "nurbsSphere1", but if that already exists, it will be automatically renamed to "nurbsSphere2"
    # name would still equal "nurbsSphere1" but updatedName would hold "nurbsSphere2"        
    updatedName = cmds.rename(newGrp, name)

    # All children were thrown into holding group, we need to remove transform nodes and keep shape nodes.
    pArgsCurves = cmds.listRelatives(holdGrp) 
        
    for i in range(len(pArgsCurves)):
        #Since all curves thrown blindly into holdGrp, need to sort any transforms from shapes (we want the latter)
        #Assigns value held in list to temporary holding variable, and reassigns list value to the list of children
        #If there are no children, restore list value to it's original value using temp node.
        # (in short, reassign value to child if the list value has child, do nothing otherwise)
        #When written, transform nodes only had single children in practice, so method worked to remove junk nodes.

        currentVal = pArgsCurves[i]                            
        pArgsCurves[i] = cmds.listRelatives(pArgsCurves[i])
        if pArgsCurves[i] is None:
            pArgsCurves[i] = currentVal

        #Parent list's new contents to final group and re-name each curve to final name to avoid clashes
        cmds.parent(pArgsCurves[i], updatedName, shape=True, relative=True)    
        cmds.rename(pArgsCurves[i], "%s" % updatedName + "Ctrl1")   

    cmds.delete(updatedName, constructionHistory=True)
    cmds.delete(holdGrp)
    cmds.select(updatedName)                                                         
    
def freeze(*pArgs):
    ''' Freeze transformations of all arguments passed to function
    
        On Exit:
        Object named in function call has default keyable values 0'd out.'''

    cmds.select(pArgs)
    cmds.makeIdentity(apply=True) 

def sliderChange(*pArgs):
    ''' Update the GUI colour slider's height when function called (every time dropdown menu is changed)
    
        On Exit:
        The Colour Sliders' heights are adjusted based upon the selected slider option (Index/RGB)
        Whichever one is selected is 'active' and has it's height increased. The other is decreased and impossible to see.'''

    tracker = cmds.optionMenu("colDropdown", q=True, value=True) 

    if tracker == "Index":
        cmds.colorIndexSliderGrp("index", edit=True, h=20)
        cmds.colorSliderGrp("rgb", edit=True, h=1)
        
    if tracker == "RGB":
        cmds.colorIndexSliderGrp("index", edit=True, h=1)
        cmds.colorSliderGrp("rgb", edit=True, h=20)
        
def colUpdate(*pArgs):
    ''' Update colour of selected nurbs Shapes with given RGB or Index Slider colours
    
        On Exit:
        All curves of selected shapes are updated to the selected colour.'''

    tracker = cmds.optionMenu("colDropdown", q=True, value=True) 
    shapeList = cmds.ls(sl=True)
    

    for i in range(len(shapeList)):
        # Enable colour override for selected options if not enabled already.
        cmds.setAttr("%s.overrideEnabled" % shapeList[i], 1)
        
        # Query the colour provided by the index/rgb slider, set the RGB/Index mode in the shape's attributes to match
        # the one used in the GUI, and apply the colour appropriately.
 
        if tracker == "Index":
            index = cmds.colorIndexSliderGrp("index", q=True, value=True)
            cmds.setAttr("%s.overrideRGBColors" % shapeList[i], 0)
            cmds.setAttr("%s.overrideColor" % shapeList[i], index-1)
            
        if tracker == "RGB":
            rgb = cmds.colorSliderGrp("rgb", q=True, rgbValue=True)
            cmds.setAttr("%s.overrideRGBColors" % shapeList[i], 1)
            
            cmds.setAttr("%s.overrideColorRGB" % shapeList[i], rgb[0], rgb[1], rgb[2])
        
        
def cvSelect(*pArgs):
    ''' Allows selection of all of first input nurbsShape's CVs
    
        On Exit: All CVs of first given shape are selected and active.'''

    # Get list of all selected objs, and clear selection 
    selected = cmds.ls(sl=True)
    cmds.select(clear=True)

    # Gets list of shapes in first nurb object
    for i in range(len(selected)):
        shapes = cmds.listRelatives(selected[0], s=True) 

        for i in range(len(shapes)):
            # Get spans and degrees of each shape to calculate num of CVs, and select them additively.

            spans = cmds.getAttr("%s.spans" % shapes[i])
            degree = cmds.getAttr("%s.degree" % shapes[i])
            numCVs = (spans+degree) - 1
            
            cmds.select("%s.cv[0:%i]" % (shapes[i], numCVs), add=True)
        
def closeWindow(myWin, *pArgs ):

    ''' Close gui window
    
        myWin : the specific instance of nurbCtrl's GUI window'''

    if cmds.window(myWin, exists=True):
        cmds.deleteUI(myWin) 
        
createCtrlGUI()