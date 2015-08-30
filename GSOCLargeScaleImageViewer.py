from __main__ import vtk, qt, ctk, slicer
import sys
sys.path.append('/usr/lib/python2.7/dist-packages/')
import openslide
from openslide import OpenSlide as OS
import numpy as np

class GSOCLargeScaleImageViewer:
  def __init__(self, parent):
    parent.title = "GSOC Large Scale Image Viewer"
    parent.categories = ["Utilities"]
    parent.dependencies = []
    parent.contributors = [] 
    parent.helpText = """Large scale image viewer. Visualization for multiresolution 2D images"""
    parent.acknowledgementText = """ I give my thanks first of all to the Google Summer of Code organizers, and my mentor PhD. Yi Gao, from Stony Brook University, for giving me the opportunity to participate in this project.
    It has been a unique learning experience, one i would hope to repeat, should the chance arise.""" 
    self.parent = parent


class GSOCLargeScaleImageViewerWidget:
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
    RenderButton = qt.QPushButton("Show Render Window")
    RenderButton.toolTip = "Show Render Window"
    self.mainFormLayout.addWidget(RenderButton)
    RenderButton.connect('clicked(bool)', self.onShowWindow)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.RenderButton = RenderButton
    
    # make reference to the window displaying the last pressed key
    self.RenderWindow= QtCustomWindow()

  def onFileButtonClicked(self):
    filename = self.FileSelector.getOpenFileName()
    self.RenderWindow.filename=filename
    self.RenderWindow.initUI()


  def onShowWindow(self):
    if self.RenderWindow.isHidden():
        self.RenderWindow.show()

class QtCustomWindow( qt.QWidget ):
    def __init__( self, parent = None ) :
        qt.QWidget.__init__( self, parent )
        self.current_x=0
        self.current_y=0
        #read region always works in the level 0 reference for reading locations
        self.current_zoom=0
        self.image_width=750
        self.image_height=750
        self.setWindowTitle('Large scale image viewing module')
        self.resize(self.image_width,self.image_height)
        self.hbox = qt.QHBoxLayout(self)
        self.lbl = qt.QLabel(self)
        sp=qt.QSizePolicy() # Size policy setting
        sp.setHorizontalPolicy(qt.QSizePolicy.Ignored)
        sp.setVerticalPolicy(qt.QSizePolicy.Ignored)
        self.lbl.setSizePolicy(sp)
        self.setLayout(self.hbox)
        self.filename=None
      
        #
        #self.mouseInitialPosition
        self.panningLock=False
        self.zoomingLock=False
        self.resizeLock=True
        
        self.initUI()
        
        
    def initUI(self):      
        # initialize the widget, make the openslide object pointing to the
        # multilevel image and initialize the view to the top left corner

        if self.filename is not None:
            # openSlide object
            self.osr = OS(self.filename)
            self.level_count = self.osr.level_count
            self.current_x=0
            self.current_y=0
            self.current_zoom=self.level_count-1
            self.level_dimensions=self.osr.level_dimensions
            self.step =int(64*self.osr.level_downsamples[self.current_zoom])
            self.hbox.addWidget(self.lbl)
            self.updatePixmap()
            self.show()
            self.resizeLock=False
        
        
    def updatePixmap(self):
        self.panningLock=True
        
        im=self.osr.read_region((self.current_x,self.current_y),self.current_zoom,(self.image_width,self.image_height))
        
        data = im.tostring('raw', 'RGBA')
        image = qt.QImage(data, im.size[0], im.size[1], qt.QImage.Format_ARGB32)
        pix = qt.QPixmap.fromImage(image)
        self.lbl.setPixmap(pix)
        self.lbl.show()
        
        self.panningLock=False      
    def keyPressEvent( self, event ) :
        key = event.text()
        if key=="s":
            
            self.current_y += self.step 
            self.current_y = min(self.current_y,int(
                self.level_dimensions[0][1]-self.image_height*self.osr.level_downsamples[self.current_zoom]))
        elif key=="w":
            #larger steps for zoomed out images
            self.current_y -= self.step
            self.current_y = max(0, self.current_y)
        elif key=="a":
            #larger steps for zoomed out images
            self.current_x -= self.step
            self.current_x = max(0, self.current_x)
        elif key=="d":
            #larger steps for zoomed out images
            self.current_x += self.step
            self.current_x = min(self.current_x,int(
                self.level_dimensions[0][0]-self.image_width*self.osr.level_downsamples[self.current_zoom]))
        elif key=="q":
            new_zoom = min(self.current_zoom+1,self.level_count-1)
            self.updateCorner(new_zoom)           
            
        elif key=="e":
            new_zoom = max(self.current_zoom-1,0)
            self.updateCorner(new_zoom)

#         print "x: %s" % self.current_x
#         print "y: %s" % self.current_y
#         print "zoom: %s" % self.current_zoom
#         print "downsample: %s" % self.osr.level_downsamples[self.current_zoom]
        self.updatePixmap()
    def updateCorner(self,new_zoom, new_center=None):
        #updates the current_x and current_y values to preserve the desired image center
        
        if new_center:
            center_x=new_center[0]
            center_y=new_center[1]            
        else:
            center_x=self.image_width /2
            center_y=self.image_height /2
        
        
        #while zooming
        self.current_x=int(self.current_x + center_x *self.osr.level_downsamples[self.current_zoom]- self.image_width /2  * self.osr.level_downsamples[new_zoom])
        self.current_y=int(self.current_y + center_y *self.osr.level_downsamples[self.current_zoom]- self.image_height /2 * self.osr.level_downsamples[new_zoom])
        #update step size and current zoom
        self.current_zoom=new_zoom
        
        #larger steps for zoomed out images
        self.step =int(64*self.osr.level_downsamples[self.current_zoom])

################################################################################
################################################################################
    def mousePressEvent(self, QMouseEvent):
        #cursor =qt.QCursor()
        position = QMouseEvent.pos()
        xpos = QMouseEvent.x()
        ypos = QMouseEvent.y()

        self.mouseInitialPosition=np.array([QMouseEvent.x(), QMouseEvent.y()])


       
    def mouseMoveEvent(self, QMouseEvent):
        #cursor =qt.QCursor()
        
        if self.panningLock:
            return
        
        
        currentPosition=np.array([QMouseEvent.x(), QMouseEvent.y()])
        difference=self.mouseInitialPosition-currentPosition
        self.mouseInitialPosition=currentPosition 
          
          
        self.current_x= self.current_x + int(difference[0]*self.osr.level_downsamples[self.current_zoom])
        self.current_x = max(0, self.current_x)
        self.current_x = min(self.current_x,int(
            self.level_dimensions[0][0]-self.image_width*self.osr.level_downsamples[self.current_zoom]))
        
        self.current_y= self.current_y + int(difference[1]*self.osr.level_downsamples[self.current_zoom])
        self.current_y = max(0, self.current_y) 
        self.current_y = min(self.current_y,int(
            self.level_dimensions[0][1]-self.image_height*self.osr.level_downsamples[self.current_zoom]))
            
        self.updatePixmap()
        
    def wheelEvent(self,QMouseEvent):      
        new_zoom = min(max(self.current_zoom- QMouseEvent.delta()/120,0), self.level_count-1)
        
        if new_zoom != self.current_zoom:
            new_center=[0,0]
            new_center[0]= int(QMouseEvent.x())
            new_center[1]= int(QMouseEvent.y())

            
            self.updateCorner(new_zoom, new_center)
            self.updatePixmap()

    def resizeEvent(self,event):
         
        if self.resizeLock:
            return
         
        self.resizeLock=True
        
        difw=event.size().width()-event.oldSize().width()
        difh = event.size().height()-event.oldSize().height()
          
        self.image_width+=difw
        self.image_height+=difh
        self.updatePixmap()
        self.resizeLock=False
        
