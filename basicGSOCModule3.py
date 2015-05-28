from __main__ import vtk, qt, ctk, slicer

class basicGSOCModule3:
    def __init__(self, parent):
        parent.title = "basicGSOCModule3"
        parent.categories = ["Quantification"]
        parent.dependencies = []
        parent.contributors = [] 
        parent.helpText = """basicGSOCModule3, scripted loadable extension"""
        parent.acknowledgementText = """""" # replace with organization, grant and thanks.
        self.parent = parent


class basicGSOCModule3Widget:
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
        #instantiate logic class
        #self.logic=basicGSOCModule3Logic()
        
        # Collapsible button
        self.mainCollapsibleButton = ctk.ctkCollapsibleButton()
        self.mainCollapsibleButton.text = "Window loading button"
        self.layout.addWidget(self.mainCollapsibleButton)
    
        # Layout within the laplace collapsible button
        self.mainFormLayout = qt.QFormLayout(self.mainCollapsibleButton)
    
        # Show button
        KeyboardButton = qt.QPushButton("Show PopUp")
        KeyboardButton.toolTip = "Show PopUp"
        self.mainFormLayout.addWidget(KeyboardButton)
        KeyboardButton.connect('clicked(bool)', self.onApply)
    
        # Add vertical spacer
        self.layout.addStretch(1)
    
        # Set local var as instance attribute
        self.KeyboardButton = KeyboardButton
        
        # make reference to the window displaying the last pressed key
        self.KeyboardWindow= KeyboardInputWindow()
        #self.KeyboardWindow.show()
        
        #Get the interactor to the red slice, and set  layout to redslice
        lm = slicer.app.layoutManager()
        lm.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)
        sliceWidget = lm.sliceWidget('Red')
        sliceLogic = sliceWidget.sliceLogic()
        sliceView = sliceWidget.sliceView()
        interactor = sliceView.interactorStyle().GetInteractor()
        #Add the keypressEvent callback
        def key_pressed_callback(obj, event):
            self.key = obj.GetKeySym()
            self.onKeyboardPressed(self.key)
            #KeyboardInputWindow.updatePressedKey(self.KeyboardWindow, self.key)
            #print self.key    
        self.interactorTag = interactor.AddObserver("KeyPressEvent", key_pressed_callback, 1.0)


    def onApply(self):
        if self.KeyboardWindow.isHidden():
            self.KeyboardWindow.show()

    def onKeyboardPressed(self,key):
        def keypress():
            self.KeyboardWindow.show()
            self.KeyboardWindow.updatePressedKey(key)
        options={"w": keypress, "a": keypress,
                  "s": keypress, "d": keypress,
                  "q": keypress, "e": keypress }
        try:
            options[key]()
        except KeyError:
            print "unimportant key, will ignore later"
            print key



class KeyboardInputWindow( qt.QWidget ):
    def __init__( self, parent = None ) :
        qt.QWidget.__init__( self, parent )
        self.setGeometry( 100, 200, 600, 300 )
        self.setWindowTitle( "Pressed Keys" )
        self.code_of_last_pressed_key  =  63  #  The question mark ?
        self.large_font  = qt.QFont( "SansSerif", 20, qt.QFont.Bold )
    #  The following methods will be called by the program
    #  execution system whenever keys of the keyboard are pressed.
    #  They receive a QKeyEvent object as a parameter.
    def paintEvent( self, event ) :
        painter = qt.QPainter()
        painter.begin( self )
        painter.setFont( self.large_font )
        #  The format specifier %c treats an integer value as a character,
        #  but the integer value must be less than 256.
        #  %s converts an object to a string.
        #  %X shows an integer in hexadecimal form.
        if  self.key  <  256  :
            text_to_show_as_string  =  "Last pressed key: %c"  %  \
                                      ( self.key)
        else :
            text_to_show_as_string  =  "Last pressed key: %s"  %  \
                                      ( self.key)
        painter.drawText( 100, 200, text_to_show_as_string )
        painter.end()
    def updatePressedKey(self, key):
        self.key = key
        self.update()

