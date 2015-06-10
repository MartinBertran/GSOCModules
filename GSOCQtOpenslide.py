from __main__ import vtk, qt, ctk, slicer
import sys
sys.path.append('/usr/lib/python2.7/dist-packages/')
import openslide
from openslide import OpenSlide as OS

class GSOCQtOpenslide:
  def __init__(self, parent):
    parent.title = "GSOCQtOpenslide"
    parent.categories = ["Quantification"]
    parent.dependencies = []
    parent.contributors = [] 
    parent.helpText = """GSOCQtOpenslide, scripted loadable extension"""
    parent.acknowledgementText = """""" # replace with organization, grant and thanks.
    self.parent = parent


class GSOCQtOpenslideWidget:
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
    self.KeyboardWindow= QtCustomWindow()
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

class QtCustomWindow( qt.QWidget ):
    def __init__( self, parent = None ) :
        qt.QWidget.__init__( self, parent )
        self.current_x=0
        self.current_y=0
        self.current_zoom=0
        self.image_width=512
        self.image_height=512
        self.setWindowTitle('Red Rock')
        self.hbox = qt.QHBoxLayout(self)
        self.lbl = qt.QLabel(self)
        self.setLayout(self.hbox)
        self.initUI()
    def initUI(self):      
        # initialize the widget, make the openslide object pointing to the
        # multilevel image and initialize the view to the top left corner
        
        archivo=u'/home/martin/Downloads/CMU-1-JP2K-33005.svs'
        # openSlide object
        self.osr = OS(archivo)
        self.level_count = self.osr.level_count
        self.current_x=0
        self.current_y=0
        self.current_zoom=self.level_count-1
        #width, height = osr.dimensions

        

        

        self.hbox.addWidget(self.lbl)
        
        
        #self.move(300, 200)

        
        self.updatePixmap()
        self.show()
    def updatePixmap(self):
        im=self.osr.read_region((self.current_x,self.current_y),self.current_zoom,(self.image_width,self.image_height))
        
        data = im.tostring('raw', 'RGBA')
        image = qt.QImage(data, im.size[0], im.size[1], qt.QImage.Format_ARGB32)
        pix = qt.QPixmap.fromImage(image)
        self.lbl.setPixmap(pix)
        self.lbl.show()      
    def keyPressEvent( self, event ) :
        key = event.text()
        print key
        print type(key)
        #TODO: remember to check the boundaries of the image here
        if key=="w":
            self.current_y += 64
            print "w"
        elif key=="s":
            self.current_y -= 64
            print "s"
        elif key=="a":
            self.current_x -=64
            print "a"
        elif key=="d":
            self.current_x += 64
            print "d"
        self.updatePixmap()



