import maya.cmds as cmds
from utility_pm import snap_a_to_b  # Utility_pm written by Anarygyros Sarafopoulos
from utility_pm import aim_pivots

def makeGrpFunc(*pArgs):

    '''create a parent group to offset trans/rot/scale values of selected obj. Primarily for zeroing out animation controls.

        On Exit: 
        Group will be created with the same translation, rotation and scale values as the selected object.
        Object will be parented to the group, and (if applicable) the group re-parented to what the original object was parented to.
        Selected object's channel attributes freed up. 
        Best used as shelf item.
     
     For example:
        'pCube1'
        -> 'pCube2'

        'pCube1'
        -> 'pCube2_offsetGrp'
        ---> 'pCube2'''
    
    # Boolean marker to note if selected object had a non-world parent.
    parentCheck = False

    # Save selected object in var,  
    selected = cmds.ls(selection=True)

    # Check to see if object is parented to non-world parent.
    if cmds.listRelatives(p=True) != None:                       # List will evaluate to 'None' if the world is the parent.
        returnLoc = cmds.listRelatives(p=True)                   # Variable to hold where to parent the offsetGrp back to to return things back to position.
        parentCheck = True

    # Deselect everything so group is created at world origin
    cmds.select(d=True)
    grp = cmds.group(em=True)

    # Lecturer-provided utility scripts, matching group to selected obj's translations etc. Parent selected obj to the grp.
    snap_a_to_b(grp, selected[0]) 
    aim_pivots(selected[0], grp)
    cmds.parent(selected[0], grp)

    # If selected obj was originally a child, parent the offsetGrp back to that location
    if parentCheck == True:
        cmds.parent(grp, "%s" % returnLoc[0])

    # And give the group a rename to "[selected_obj]_offsetGrp"
    cmds.rename(grp, "%s" % selected[0] +"_offsetGrp")