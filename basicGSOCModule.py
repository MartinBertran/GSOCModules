from __main__ import vtk, qt, ctk, slicer
import sys
sys.path.append('/usr/lib/python2.7/dist-packages/')
import openslide
from openslide import OpenSlide as OS

class basicGSOCModule:
  def __init__(self, parent):
    parent.title = "basicGSOCModule"
    parent.categories = ["Quantification"]
    parent.dependencies = []
    parent.contributors = [] 
    parent.helpText = """basicGSOCModule, scripted loadable extension"""
    parent.acknowledgementText = """""" # replace with organization, grant and thanks.
    self.parent = parent


class basicGSOCModuleWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Collapsible button
    self.mainCollapsibleButton = ctk.ctkCollapsibleButton()
    self.mainCollapsibleButton.text = "Window loading button"
    self.layout.addWidget(self.mainCollapsibleButton)

    # Layout within the laplace collapsible button
    self.mainFormLayout = qt.QFormLayout(self.mainCollapsibleButton)

    # Input 
    self.FileButton = qt.QPushButton("Select file")
    self.FileButton.toolTip = "Select file"
    self.mainFormLayout.addWidget(self.FileButton)
    self.FileButton.connect('clicked(bool)', self.onFileButtonClicked)
    self.FileSelector=qt.QFileDialog()

    # Show button
    KeyboardButton = qt.QPushButton("Show PopUp")
    KeyboardButton.toolTip = "Show PopUp"
    self.mainFormLayout.addWidget(KeyboardButton)
    KeyboardButton.connect('clicked(bool)', self.onShowWindow)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.KeyboardButton = KeyboardButton
    
    # make reference to the window displaying the last pressed key
    self.KeyboardWindow= KeyboardInputWindow()
    self.KeyboardWindow.show()

  def onFileButtonClicked(self):
    archivo = self.FileSelector.getOpenFileName()
    print archivo
    #detect vendor
    print openslide.OpenSlide.detect_format(archivo)
    # openSlide object
    osr = OS(archivo)
    #print basic info, levels go from 0 (highest resolution) to lvl_count -1
    print "level count: %s" % osr.level_count
    width, height = osr.dimensions
    print "dimensions of level 0 slide %s" % (tuple(width,height))
    #level_dimension list
    #ldim=osr.level_dimensions
    #level downsample list
    #ldown=osr.level_downsamples  

  def onShowWindow(self):
    if self.KeyboardWindow.isHidden():
        self.KeyboardWindow.show()

class KeyboardInputWindow( qt.QWidget ):
    def __init__( self, parent = None ) :
        qt.QWidget.__init__( self, parent )
        self.setGeometry( 100, 200, 600, 300 )
        self.setWindowTitle( "Ps" )
        self.initUI()
    def initUI(self):      
        #
        hbox = qt.QHBoxLayout(self)
        pixmap = qt.QPixmap("/home/martin/Downloads/redrock.jpeg")
        #
        lbl = qt.QLabel(self)
        lbl.setPixmap(pixmap)
        #
        hbox.addWidget(lbl)
        self.setLayout(hbox)
        #
        self.move(300, 200)
        self.setWindowTitle('Red Rock')
        self.show()        
        
        



