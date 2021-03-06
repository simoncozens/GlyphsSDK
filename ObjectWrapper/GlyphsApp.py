# encoding: utf-8

from AppKit import *
from Foundation import *

import time, math, sys, os, string, re
from sets import Set


__all__ = ["Glyphs", "GetFile", "GSMOVE", "GSLINE", "GSCURVE", "GSOFFCURVE", "GSSHARP", "GSSMOOTH", "TOPGHOST", "STEM", "BOTTOMGHOST", "TTANCHOR", "TTSTEM", "TTALIGN", "TTINTERPOLATE", "TTDIAGONAL", "CORNER", "CAP", "TTDONTROUND", "TTROUND", "TTROUNDUP", "TTROUNDDOWN", "TRIPLE", "DRAWFOREGROUND", "DRAWBACKGROUND", "DRAWINACTIVE", "TEXT", "ARROW", "CIRCLE", "PLUS", "MINUS", "divideCurve", "distance", "addPoints", "subtractPoints", "GetFolder", "GetSaveFile", "GetOpenFile", "Message", "LogToConsole"]


class Proxy(object):
	def __init__(self, owner):
		self._owner = owner
	def __repr__(self):
		"""Return list-lookalike of representation string of objects"""
		strings = []
		for currItem in self:
			strings.append("%s" % (currItem))
		return "(%s)" % (', '.join(strings))
	def __len__(self):
		Values = self.values()
		if Values is not None:
			return len(Values)
		return 0
	def __iter__(self):
		Values = self.values()
		if Values is not None:
			for element in Values:
				yield element
	def index(self, Value):
		return self.values().index(Value)


##################################################################################
#
#
#
#           GSApplication
#
#
#
##################################################################################


Glyphs = NSApplication.sharedApplication()


'''
:mod:`GSApplication`
===============================================================================

The mothership. Everything starts here.

.. code-block:: python

	print Glyphs

.. code-block:: python

	<Glyphs.app>

	
.. class:: GSApplication()

Properties

.. autosummary::

	font
	fonts
	defaults
	scriptAbbrevations
	scriptSuffixes
	languageScripts
	languageData
	unicodeRanges
	editViewWidth
	handleSize
	versionString
	versionNumber
	buildNumber
	

	
Functions

.. autosummary::

	open()
	showMacroWindow()
	clearLog()
	showGlyphInfoPanelWithSearchString()
	glyphInfoForName()
	glyphInfoForUnicode()
	niceGlyphName()
	productionGlyphName()
	ligatureComponents()
	redraw()
	showNotification()
	
	
----------
Properties
----------
'''
GSApplication.currentDocument = property(lambda self: NSApplication.sharedApplication().currentFontDocument())

GSApplication.documents = property(lambda self: AppDocumentProxy(self))

def Glyphs__repr__(self):
	return '<Glyphs.app>'
GSApplication.__repr__ = Glyphs__repr__;

def currentFont():
	try:
		doc = NSApplication.sharedApplication().currentFontDocument()
		return doc.font
	except:
		pass
	return None

# by Yanone
GSApplication.font = property(lambda self: currentFont())

'''.. attribute:: font
	
	:return: The active :class:`GSFont` object or None.
	:rtype: :class:`GSFont`
	
	.. code-block:: python

		# topmost open font
		font = Glyphs.font

'''



GSApplication.fonts = property(lambda self: AppFontProxy(self))


'''.. attribute:: fonts
	
	:return: All open :class:`Fonts <GSFont>`.
	:rtype: list of :class:`GSFont` objects
	
	.. code-block:: python

		# access all open fonts
		for font in Glyphs.fonts:
			print font.familyName
			
		# add a font
		
		font = GSFont()
		font.familyName = "My New Fonts"
		Glyphs.fonts.append(font)
		
'''

class DefaultsProxy(Proxy):
	def __getitem__(self, Key):
		return NSUserDefaults.standardUserDefaults().objectForKey_(Key)
	def __setitem__(self, Key, Value):
		NSUserDefaults.standardUserDefaults().setObject_forKey_(Value, Key)
	def __repr__(self):
		return "<Userdefaults>"

GSApplication.defaults = property(lambda self: DefaultsProxy(self))

'''.. attribute:: defaults
	
	A dict like object for storing preferences. You can get and set key-value pairs.
	
	Please be careful with your keys. Use a prefix that uses the reverse domain name. e.g. "com.MyName.foo.bar".
	
	.. code-block:: python
	
		# Check for whether or not a preference exists, because has_key() doesn't work in this PyObjC-brigde
		if Glyphs.defaults["com.MyName.foo.bar"] == None:
			# do stuff

		# Get and set values
		value = Glyphs.defaults["com.MyName.foo.bar"]
		Glyphs.defaults["com.MyName.foo.bar"] = newValue
	
	'''


class BoolDefaultsProxy(DefaultsProxy):
	def __getitem__(self, Key):
		return NSUserDefaults.standardUserDefaults().boolForKey_(Key)
	def __setitem__(self, Key, Value):
		NSUserDefaults.standardUserDefaults().setBool_forKey_(Value, Key)

GSApplication.boolDefaults = property(lambda self: BoolDefaultsProxy(self))

class IntDefaultsProxy(DefaultsProxy):
	def __getitem__(self, Key):
		return NSUserDefaults.standardUserDefaults().integerForKey_(Key)
	def __setitem__(self, Key, Value):
		NSUserDefaults.standardUserDefaults().setInteger_forKey_(Value, Key)

GSApplication.intDefaults = property(lambda self: IntDefaultsProxy(self))

GSApplication.scriptAbbrevations = property(lambda self: GSGlyphsInfo.scriptAbrevations())

'''.. attribute:: scriptAbbrevations
	
	A dictionary with script name to abbreviation mapping, e.g. 'arabic': 'arab'
	
	:rtype: dict`
	'''

GSApplication.scriptSuffixes = property(lambda self: GSGlyphsInfo.scriptSuffixes())

'''.. attribute:: scriptSuffixes
	
	A dictionary with glyphs name suffixes for scripts and their respective script names, e.g. 'cy': 'cyrillic'
	
	:rtype: dict`
	'''

GSApplication.languageScripts = property(lambda self: GSGlyphsInfo.languageScripts())

'''.. attribute:: languageScripts
	
	A dictionary with language tag to script tag mapping, e.g. 'ENG': 'latn'
	
	:rtype: dict`
	'''

GSApplication.languageData = property(lambda self: GSGlyphsInfo.languageData())

'''.. attribute:: languageData
	
	A list of dictionaries with more detailed language informations.
	
	:rtype: list`
	'''

GSApplication.unicodeRanges = property(lambda self: GSGlyphsInfo.unicodeRanges())

'''.. attribute:: unicodeRanges
	
	Names of unicode ranges.
	
	:rtype: list`
	'''

def Glyphs_setUserDefaults(self, key, value):
	self.defaults[key] = value

GSApplication.editViewWidth = property(lambda self: self.intDefaults["GSFontViewWidth"], lambda self, value: Glyphs_setUserDefaults(self, "GSFontViewWidth", int(value)))
'''.. attribute:: editViewWidth
	Width of glyph edit view. Corresponds to the "Width of editor" setting from the Preferences.
	
	:type: int'''

GSApplication.handleSize = property(lambda self: self.intDefaults["GSHandleSize"], lambda self, value: Glyphs_setUserDefaults(self, "GSHandleSize", int(value)))
'''.. attribute:: handleSize
	Size of Bezier handles in Glyph Edit View. Possible value are 0–2. Corresponds to the "Handle size" setting from the Preferences.
	
	To use the handle size for drawing in plugins, you need to convert the handle size to a point size, and divide by the view's scale factor. See example below.
	
	.. code-block:: python
	
		# Calculate handle size
		handSizeInPoints = 5 + Glyphs.handleSize * 2.5 # (= 5.0 or 7.5 or 10.0)
		scaleCorrectedHandleSize = handSizeInPoints / Glyphs.font.currentTab.scale

		# Draw point in size of handles
		point = NSPoint(100, 100)
		NSColor.redColor.set()
		rect = NSRect((point.x - scaleCorrectedHandleSize * 0.5, point.y - scaleCorrectedHandleSize * 0.5 ), (scaleCorrectedHandleSize, scaleCorrectedHandleSize))
		bezierPath = NSBezierPath.bezierPathWithOvalInRect_(rect)
		bezierPath.fill()

	:type: int'''


GSApplication.versionString = NSBundle.mainBundle().infoDictionary()["CFBundleShortVersionString"]

'''.. attribute:: versionString

	String containing Glyph.app's version number. May contain letters also, like '2.3b'. To check for a specific version, use .versionNumber below.
	
	:type: string'''


def Glyphs_FloatVersion(self):
	m = re.match(r"(\d+)\.(\d+)", self.versionString)
	return float(str(m.group(1)) + '.' + str(m.group(2)))

GSApplication.versionNumber = property(lambda self: Glyphs_FloatVersion(self))

'''.. attribute:: versionNumber

	Glyph.app's version number. Use this to check for version in your code.
	
	.. code-block:: python
	
		# Code valid for Glyphs.app v2.1 and above:
		if Glyphs.versionNumber >= 2.1:
			# do stuff
		
		# Code for older versions
		else:
			# do other stuff


	:type: float'''


GSApplication.buildNumber = int(NSBundle.mainBundle().infoDictionary()["CFBundleVersion"])

'''.. attribute:: buildNumber

	Glyph.app's build number.
	
	Especially if you're using Glyphs' preview builds, this number may be more important to you than the version number. The build number increases with every released build and is the most significant evidence of new Glyphs versions, while the version number is artificially chosen and may stay at the same number for some time, until a decision is made to release a new set of features under a new version number.
	
	:type: int'''


'''
---------
Functions
---------
'''

def OpenFont(self, Path, showInterface=True ):
	URL = NSURL.fileURLWithPath_(Path)
	Doc = NSDocumentController.sharedDocumentController().openDocumentWithContentsOfURL_display_error_(URL, showInterface, None)[0]
	if Doc is not None:
		return Doc.font
	return None
	
GSApplication.open = OpenFont

'''.. function:: open(Path)
	
	Opens a document
	
	:param Path: The path where the document is located.
	:type Path: str
	:return: The opened document object or None.
	:rtype: :class:`GSFont`'''

def __ShowMacroWindow(self):
	GSApplication.delegate(self).showMacroWindow()

GSApplication.showMacroWindow = __ShowMacroWindow

'''.. function:: showMacroWindow
	
	Opens the macro window

'''

def __ClearLog(self):
	GSApplication.delegate(self).clearConsole()

GSApplication.clearLog = __ClearLog

'''.. function:: clearLog
	
	Deletes the content of the console in the macro window
	
'''


def __showGlyphInfoPanelWithSearchString__(self, String):
	GSApplication.delegate(self).showGlyphInfoPanelWithSearchString_(String)

GSApplication.showGlyphInfoPanelWithSearchString = __showGlyphInfoPanelWithSearchString__

'''.. function:: showGlyphInfoPanelWithSearchString(String)
	
	Shows the Glyph Info window with a preset search string
	
	:param String: The search term
	
	'''

def _glyphInfoForName(self, String):
	if type(String) is int:
		String = "%04X" % String
	return GSGlyphsInfo.glyphInfoForName_(String)

GSApplication.glyphInfoForName = _glyphInfoForName

'''.. function:: glyphInfoForName(String)
	
	Generates :class:`GSGlyphInfo` object for given glyph name.
	
	:param String: Glyph name
	:return: :class:`GSGlyphInfo`
	
	'''

def _glyphInfoForUnicode(self, String):
	return GSGlyphsInfo.glyphInfoForUnicode_(String)

GSApplication.glyphInfoForUnicode = _glyphInfoForUnicode

'''.. function:: glyphInfoForUnicode(Unicode)
	
	Generates :class:`GSGlyphInfo` object for given hex unicode.
	
	:param String: Hex unicode
	:return: :class:`GSGlyphInfo`
	
	'''

def _niceGlyphName(self, String):
	return GSGlyphsInfo.niceGlyphNameForName_(String)
GSApplication.niceGlyphName = _niceGlyphName

'''.. function:: niceGlyphName(Name)
	
	Converts glyph name to nice, human readable glyph name (e.g. afii10017 or uni0410 to A-cy)
	
	:param string: glyph name
	:return: string
	
	'''

def _productionGlyphName(self, String):
	return GSGlyphsInfo.productionGlyphNameForName_(String)
GSApplication.productionGlyphName = _productionGlyphName

'''.. function:: productionGlyphName(Name)
	
	Converts glyph name to production glyph name (e.g. afii10017 or A-cy to uni0410)
	
	:param string: glyph name
	:return: string
	
	'''

def _ligatureComponents(self, String):
	return GSGlyphsInfo._componentsForLigaName_(String)
GSApplication.ligatureComponents = _ligatureComponents

'''.. function:: ligatureComponents(String)
	
	If defined as a ligature in the glyph database, this function returns a list of glyph names that this ligature could be composed of.
	
	:param string: glyph name
	:return: list
	
	.. code-block:: python
	
		print Glyphs.ligatureComponents('allah-ar')

		(
		    "alef-ar",
		    "lam-ar.init",
		    "lam-ar.medi",
		    "heh-ar.fina"
		)
	'''

# available in Glyphs 2 (786)
def __addCallback__(self, target, operation):
	GSApplication.delegate().addCallback_forOperation_(target, operation)
GSApplication.addCallback = __addCallback__

def __removeCallback___(self, target, operation = None):
	if operation != None:
		GSApplication.delegate().removeCallback_forOperation_(target, operation)
	else:
		GSApplication.delegate().removeCallback_(target)
GSApplication.removeCallback = __removeCallback___

DRAWFOREGROUND = "DrawForeground"
DRAWBACKGROUND = "DrawBackground"
DRAWINACTIVE = "DrawInactive"


def __redraw__(self):
	NSNotificationCenter.defaultCenter().postNotificationName_object_("GSRedrawEditView", None)
GSApplication.redraw = __redraw__

'''.. function:: redraw()
	
	Redraws all Edit views and Preview views.
	
	'''

def Glyphs_showNotification(self, title, message):
	notification = NSUserNotification.alloc().init()
	notification.setTitle_(title)
	notification.setInformativeText_(message)
	NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
	
GSApplication.showNotification = Glyphs_showNotification;

'''.. function:: showNotification(title, message)
	
	Shows the user a notification in Mac's Notification Center.
	

	.. code-block:: python
	
		Glyphs.showNotification('Export fonts', 'The export of the fonts was successful.')
		

	'''



GSMOVE = 17
GSLINE = 1
GSCURVE = 35
GSOFFCURVE = 65
GSSHARP = 0
GSSMOOTH = 100

TOPGHOST = -1
STEM = 0
BOTTOMGHOST = 1
TTANCHOR = 2
TTSTEM = 3
TTALIGN = 4
TTINTERPOLATE = 5
TTDIAGONAL = 6
CORNER = 16
CAP = 17

TTDONTROUND = 4,
TTROUND = 0,
TTROUNDUP = 1,
TTROUNDDOWN = 2,
TRIPLE = 128,

#annotations:
TEXT = 1
ARROW = 2
CIRCLE = 3
PLUS = 4
MINUS = 5


# Reverse lookup for __repr__
nodeConstants = {
	17: 'GSMOVE',
	1: 'GSLINE',
	35: 'GSCURVE',
	65: 'GSOFFCURVE',
	0: 'GSSHARP',
	100: 'GSSMOOTH',
}
hintConstants = {
	-1: 'TopGhost',
	0: 'Stem',
	1: 'BottomGhost',
	2: 'TTAnchor',
	3: 'TTStem',
	4: 'TTAlign',
	5: 'TTInterpolate',
	6: 'TTDiagonal',
	16: 'Corner',
	17: 'Cap',
}



GSElement.x = property(lambda self: self.pyobjc_instanceMethods.position().x,
	lambda self, value: self.setPosition_(NSMakePoint(value, self.y)))

GSElement.y = property(lambda self: self.pyobjc_instanceMethods.position().y,
	lambda self, value: self.setPosition_(NSMakePoint(self.x, value)))

GSElement.layer = property(lambda self: self.parent)

class AppDocumentProxy (Proxy):
	"""The list of documents."""
	def __getitem__(self, Key):
		if type(Key) is int:
			Values = self.values()
			if Key < 0:
				Key = len(Values) + Key
			return Values[Key]
		else:
			raise(KeyError)
	def values(self):
		docs = []
		for doc in self._owner.orderedDocuments():
			if doc.isKindOfClass_(NSClassFromString("GSDocument")):
				docs.append(doc)
		return docs

class AppFontProxy (Proxy):
	"""The list of fonts."""
	def __getitem__(self, Key):
		if type(Key) is int:
			Values = self.values()
			if Key < 0:
				Key = len(Values) + Key
			return Values[Key]
		else:
			raise(KeyError)
	def values(self):
		fonts = []
		for doc in self._owner.orderedDocuments():
			if doc.isKindOfClass_(NSClassFromString("GSDocument")):
				fonts.append(doc.font)
		return fonts
	def append(self, font):
		doc = Glyphs.documentController().openUntitledDocumentAndDisplay_error_(True, None)[0]
		doc.setFont_(font)

GSDocument.font = property(lambda self: self.valueForKey_("font"),
						   lambda self, value: self.setFont_(value))

#	''.. attribute:: font
#		The active :class:`Font <GSFont>`.
#		:type: list''





class FontGlyphsProxy (Proxy):
	"""The list of glyphs. You can access it with the index or the glyph name.
	Usage: 
		Font.glyphs[index]
		Font.glyphs[name]
		for glyph in Font.glyphs:
		...
	"""
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.glyphAtIndex_(Key)
		else:
			return self._owner.glyphForName_(Key)
	def __setitem__(self, Key, Glyph):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.removeGlyph_( self._owner.glyphAtIndex_(Key) )
			self._owner.addGlyph_(Glyph)
		else:
			self._owner.removeGlyph_( self._owner.glyphForName_(Key) )
			self._owner.addGlyph_(Glyph)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.removeGlyph_( self._owner.glyphAtIndex_(Key) )
		else:
			self._owner.removeGlyph_( self._owner.glyphForName_(Key) )
	def __contains__(self, item):
		return self._owner.indexOfGlyph_(item) < NSNotFound #indexOfGlyph_ returns NSNotFound which is some very big number
	def keys(self):
		return self._owner.pyobjc_instanceMethods.glyphs().valueForKeyPath_("@unionOfObjects.name")
	def values(self):
		return self._owner.pyobjc_instanceMethods.glyphs()
	def items(self):
		Items = []
		for Value in self._owner.pyobjc_instanceMethods.glyphs():
			Key = Value.name
			Items.append((Key, Value))
		return Items
	def has_key(self, Key):
		return self._owner.glyphForName_(Key) != None
	def append(self, Glyph):
		self._owner.addGlyph_(Glyph)
	def __len__(self):
		return self._owner.count()


class FontFontMasterProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.fontMasterAtIndex_(Key)
		elif type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			return self._owner.fontMasterForId_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, FontMaster):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.replaceFontMasterAtIndex_withFontMaster_(Key, FontMaster)
		elif type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			OldFontMaster = self._owner.fontMasterForId_(Key)
			self._owner.removeFontMaster_(OldFontMaster)
			return self._owner.addFontMaster_(FontMaster)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.removeFontMasterAtIndex_(Key)
		else:
			OldFontMaster = self._owner.fontMasterForId_(Key)
			return self._owner.removeFontMaster_(OldFontMaster)
	def __iter__(self):
		for index in range(self._owner.countOfFontMasters()):
			yield self._owner.fontMasterAtIndex_(index)
	def __len__(self):
		return self._owner.countOfFontMasters()
	def values(self):
		return self._owner.pyobjc_instanceMethods.fontMasters()
	


class FontInstancesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.instanceAtIndex_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, Class):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.replaceObjectInInstancesAtIndex_withObject_(Key, Class)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.removeObjectFromInstancesAtIndex_(Key)
	def __iter__(self):
		for index in range(self._owner.countOfInstances()):
			yield self._owner.instanceAtIndex_(index)
	def append(self, Instance):
		self._owner.addInstance_(Instance)
	def __len__(self):
		return self._owner.countOfInstances()
	def values(self):
		return self._owner.pyobjc_instanceMethods.instances()
	

class CustomParametersProxy(Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			return self._owner.objectInCustomParametersAtIndex_(Key)
		else:
			return self._owner.customValueForKey_(Key)
	def __setitem__(self, Key, Parameter):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			Value = self._owner.objectInCustomParametersAtIndex_(Key)
			if Value is not None:
				Value.setValue_(Parameter)
		else:
			self._owner.setCustomParameter_forKey_(Parameter, Key)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.removeObjectFromCustomParametersAtIndex_(Key)
		else:
			self._owner.removeObjectFromCustomParametersForKey_(Key)
	def __iter__(self):
		for index in range(self._owner.countOfCustomParameters()):
			yield self._owner.objectInCustomParametersAtIndex_(index)
	def append(self, Parameter):
		self._owner.addCustomParameter_(Parameter)
	def __len__(self):
		return self._owner.countOfCustomParameters()
	def values(self):
		return self._owner.pyobjc_instanceMethods.customParameters()
	

class FontClassesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.objectInClassesAtIndex_(Key)
		elif type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			if len(Key) > 0:
				return self._owner.classForTag_(Key)
		raise(KeyError)
	def __setitem__(self, Key, Class):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.replaceObjectInClassesAtIndex_withObject_(Key, Class)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.removeObjectFromClassesAtIndex_(Key)
		elif type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			Class = self._owner.classForTag_(Key)
			if Class is not None:
				return self._owner.removeClass_(Class)
	def __iter__(self):
		for index in range(self._owner.countOfClasses()):
			yield self._owner.objectInClassesAtIndex_(index)
	def append(self, Class):
		 # print "append Class", Class
		self._owner.addClass_(Class)
	def __len__(self):
		return self._owner.countOfClasses()
	def values(self):
		return self._owner.pyobjc_instanceMethods.classes()
	

class FontFeaturesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.featureAtIndex_(Key)
		if type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			return self._owner.featureForTag_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, Feature):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.replaceFeatureAtIndex_withFeature_(Key, Feature)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.removeFeatureAtIndex_(Key)
		elif type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			Feature = self._owner.featureForTag_(Key)
			if Feature is not None:
				return self._owner.removeFeature_(Feature)
	def __iter__(self):
		for index in range(self._owner.countOfFeatures()):
			yield self._owner.featureAtIndex_(index)
	def append(self, Feature):
		#print "append", Node
		self._owner.addFeature_(Feature)

	def __len__(self):
		return self._owner.countOfFeatures()
	def text(self):
		LineList = []
		for Feature in self._owner.pyobjc_instanceMethods.features():
			LineList.append("feature ")
			LineList.append(Feature.name)
			LineList.append(" {\n")
			LineList.append("    "+Feature.code)
			LineList.append("\n} ")
			LineList.append(Feature.name)
			LineList.append(" ;\n")
		return "".join(LineList)
	def values(self):
		return self._owner.pyobjc_instanceMethods.features()
	


class FontFeaturePrefixesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.objectInFeaturePrefixesAtIndex_(Key)
		if type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			return self._owner.featurePrefixForTag_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, Feature):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.replaceObjectInFeaturePrefixesAtIndex__withObject_(Key, Feature)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.removeObjectFromFeaturePrefixesAtIndex_(Key)
		elif type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			FeaturePrefix = self._owner.featurePrefixForTag_(Key)
			if FeaturePrefix is not None:
				return self._owner.removeFeaturePrefix_(FeaturePrefix)
	def append(self, Feature):
		#print "append", Node
		self._owner.addFeaturePrefix_(Feature)
	def text(self):
		LineList = []
		for Prefixe in self._owner.pyobjc_instanceMethods.featurePrefixes():
			LineList.append("# "+Prefixe.name)
			LineList.append(Prefixe.code)
		return "".join(LineList)
	def values(self):
		return self._owner.pyobjc_instanceMethods.featurePrefixes()

class LayersIterator:
	def __init__(self, owner):
		self.curInd = 0
		self._owner = owner
	def __iter__(self):
		return self
	def next(self):
		if self._owner.parent:
			if self.curInd >= self._owner.countOfLayers():
				raise StopIteration
			if self.curInd < self._owner.parent.countOfFontMasters():
				FontMaster = self._owner.parent.fontMasterAtIndex_(self.curInd)
				Item = self._owner.layerForKey_(FontMaster.id)
			else:
				ExtraLayerIndex = self.curInd - self._owner.parent.countOfFontMasters()
				Index = 0
				ExtraLayer = None
				while ExtraLayerIndex >= 0:
					ExtraLayer = self._owner.pyobjc_instanceMethods.layers().objectAtIndex_(Index)
					if ExtraLayer.layerId != ExtraLayer.associatedMasterId:
						ExtraLayerIndex = ExtraLayerIndex - 1
					Index = Index + 1
				Item = ExtraLayer
			self.curInd += 1
			return Item
		else:
			if self.curInd >= self._owner.countOfLayers():
				raise StopIteration
			Item = self._owner.pyobjc_instanceMethods.layers().objectAtIndex_(self.curInd)
			self.curInd += 1
			return Item
		return None

class GlyphLayerProxy (Proxy):
	def __getitem__(self, Key):
			if type(Key) is int:
				if Key < 0:
					Key = self.__len__() + Key
				if self._owner.parent:
					if Key < self._owner.parent.countOfFontMasters():
						FontMaster = self._owner.parent.fontMasterAtIndex_(Key)
						return self._owner.layerForKey_(FontMaster.id)
					else:
						ExtraLayerIndex = Key - len(self._owner.parent.masters)
						Index = 0
						ExtraLayer = None
						while ExtraLayerIndex >= 0:
							ExtraLayer = self._owner.pyobjc_instanceMethods.layers().objectAtIndex_(Index)
							if ExtraLayer.layerId != ExtraLayer.associatedMasterId:
								ExtraLayerIndex = ExtraLayerIndex - 1
							Index = Index + 1
						return ExtraLayer
				else:
					return self._owner.pyobjc_instanceMethods.layers().objectAtIndex_(Key)
			else:
				return self._owner.layerForKey_(Key)
	def __setitem__(self, Key, Layer):
		if type(Key) is int and self._owner.parent:
			if Key < 0:
				Key = self.__len__() + Key
			FontMaster = self._owner.parent.fontMasterAtIndex_(Key)
			return self._owner.setLayer_forKey_(Layer, FontMaster.id)
		else:
			return self._owner.setLayer_forKey_(Layer, Key)
	def __delitem__(self, Key):
		if type(Key) is int and self._owner.parent:
			if Key < 0:
				Key = self.__len__() + Key
			Layer = self.__getitem__(Key)
			return self._owner.removeLayerForKey_(Layer.layerId)
		else:
			return self._owner.removeLayerForKey_(Key)
	def __iter__(self):
		return LayersIterator(self._owner)
	def __len__(self):
		return self._owner.countOfLayers()
	def values(self):
		return self._owner.pyobjc_instanceMethods.layers().allValues()
	def append(self, Layer):
		if not Layer.associatedMasterId:
			Layer.associatedMasterId = self._owner.parent.masters[0].id
		self._owner.setLayer_forKey_(Layer, NSString.UUID())

class LayerComponentsProxy (Proxy):
	def __getitem__(self, Key):
		return self._owner.componentAtIndex_(Key)
	def __setitem__(self, Key, Component):
		self._owner.setComponent_atIndex_(Component, Key)
	def __delitem__(self, Key):
		self._owner.removeComponentAtIndex_(Key)
	def append(self, Component):
		self._owner.addComponent_(Component)
	def values(self):
		return self._owner.pyobjc_instanceMethods.components()

class LayerGuideLinesProxy (Proxy):
	def __getitem__(self, Key):
		return self._owner.guideLineAtIndex_(Key)
	def __setitem__(self, Key, Component):
		self._owner.setGuideLine_atIndex_(Component, Key)
	def __delitem__(self, Key):
		self._owner.removeGuideLineAtIndex_(Key)
	def append(self, GuideLine):
		self._owner.addGuideLine_(GuideLine)
	def values(self):
		return self._owner.pyobjc_instanceMethods.guideLines()

class LayerAnnotationProxy (Proxy):
	def __getitem__(self, Key):
		return self._owner.objectInAnnotationsAtIndex_(Key)
	def __setitem__(self, Key, Annotation):
		self._owner.insertObject_inAnnotationsAtIndex_(Annotation, Key)
	def __delitem__(self, Key):
		self._owner.removeObjectFromAnnotationsAtIndex_(Key)
	def append(self, Annotation):
		self._owner.addAnnotation_(Annotation)
	def values(self):
		return self._owner.pyobjc_instanceMethods.annotations()



class LayerHintsProxy (Proxy):
	def __getitem__(self, Key):
		return self._owner.hintAtIndex_(Key)
	def __setitem__(self, Key, Component):
		self._owner.setHint_atIndex_(Component, Key)
	def __delitem__(self, Key):
		self._owner.removeObjectFromHintsAtIndex_(Key)
	def append(self, GuideLine):
		self._owner.addHint_(GuideLine)
	def values(self):
		return self._owner.pyobjc_instanceMethods.hints()




class LayerAnchorsProxy (Proxy):
	"""layer.anchors is a dict!!!"""
	def __getitem__(self, Key):
		if type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			return self._owner.anchorForName_(Key)
		else:
			raise KeyError
	def __setitem__(self, Key, Anchor):
		if type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			Anchor.setName_(Key)
			self._owner.addAnchor_(Anchor)
		else:
			raise TypeError
	def __delitem__(self, Key):
		if type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			self._owner.removeAnchorWithName_(Key)
		else:
			raise TypeError
	def items(self):
		Items = []
		for key in self.keys():
			Value = self._owner.anchorForName_(Key)
			Items.append((Key, Value))
		return Items
	def values(self):
		if self._owner.pyobjc_instanceMethods.anchors() is not None:
			return self._owner.pyobjc_instanceMethods.anchors().allValues()
		else:
			return [];
	def keys(self):
		if self._owner.pyobjc_instanceMethods.anchors() is not None:
			return self._owner.pyobjc_instanceMethods.anchors().allKeys()
		else:
			return []
	def append(self, Anchor):
		self._owner.addAnchor_(Anchor)
	def __len__(self):
		#print "count"
		return self._owner.anchorCount()




class LayerPathsProxy (Proxy):
	def __getitem__(self, idx):
		if idx < 0:
			idx = self._owner.pathCount() + idx
		return self._owner.pathAtIndex_(idx)
	def __setitem__(self, idx, Path):
		if idx < 0:
			idx = self._owner.pathCount() + idx
		self._owner.setPath_atIndex_(Path, idx)
	def __delitem__(self, idx):
		if idx < 0:
			Key = self._owner.pathCount() + idx
		self._owner.removePathAtIndex_(idx)
	def append(self, Path):
		self._owner.addPath_(Path)
	def values(self):
		return self._owner.pyobjc_instanceMethods.paths()



class LayerSelectionProxy (Proxy):
	def __getitem__(self, idx):
		return self._owner.pyobjc_instanceMethods.selection().objectAtIndex_(idx)
	def values(self):
		return self._owner.pyobjc_instanceMethods.selection().array()
	def append(self, object):
		self._owner.pyobjc_instanceMethods.addSelection_(object)
	def remove(self, object):
		self._owner.pyobjc_instanceMethods.removeObjectFromSelection_(object)



class PathNodesProxy (Proxy):
	def __getitem__(self, i):
		#print "__getitem__", i
		return self._owner.nodeAtIndex_(i)
	def __setitem__(self, i, Node):
		#print "__setitem__", i, Node
		self._owner.setNode_atIndex_(Node, i)
	def __delitem__(self, i):
		#print "__delitem__", i
		self._owner.removeNodeAtIndex_(i)
	def append(self, Node):
		#print "append", Node
		self._owner.addNode_(Node)
	def values(self):
		return self._owner.pyobjc_instanceMethods.nodes()





class FontTabsProxy (Proxy):
	def __getitem__(self, Key):
		if self._owner.parent:
			if type(Key) is int:
				if Key < 0:
					Key = self.__len__() + Key
				return self._owner.parent.windowController().tabBarControl().viewControllers()[Key + 1]
			else:
				raise(KeyError)
		else:
			raise Exception("The font is not connected to a document object")
	def __setitem__(self, Key, Tab):
		if type(Key) is int:
			raise(NotImplementedError)
		else:
			raise(KeyError)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			Tab = self._owner.parent.windowController().tabBarControl().viewControllers()[Key + 1]
			self._owner.parent.windowController().tabBarControl().closeTabItem_(Tab)
		else:
			raise(KeyError)
	def __iter__(self):
		for index in range(self.__len__()):
			yield self.__getitem__(index)
	def __len__(self):
		return len(self._owner.parent.windowController().tabBarControl().viewControllers()) - 1
	def values(self):
		return self._owner.parent.windowController().tabBarControl().viewControllers()[1:]


# Function shared by all user-selectable elements in a layer (nodes, anchors etc.)
def ObjectInLayer_selected(self):
	try:
		return self in self.layer.selection
	except:
		return False

def SetObjectInLayer_selected(self, state):

	# Add to selection
	if state == True and not self in self.layer.selection:
		self.layer.selection.append(self)

	# Remove
	elif state == False and self in self.layer.selection:
		self.layer.selection.remove(self)



##################################################################################
#
#
#
#           GSFont
#
#
#
##################################################################################

		
'''
:mod:`GSFont`
===============================================================================

Implementation of the font object. This object is host to the :class:`Masters <GSFontMaster>` used for interpolation. Even when no interpolation is involved, for the sake of object model consistency there will still be one master and one instance representing a single font.

Also, the :class:`Glyphs <GSGlyph>` are attached to the Font object right here, not one level down to the masters. The different master's glyphs are available as :class:`Layers <GSLayer>` attached to the :class:`Glyph <GSGlyph>` objects which are attached here.

.. class:: GSFont()

Properties

.. autosummary::

	parent
	masters
	instances
	glyphs
	classes
	features
	featurePrefixes
	copyright
	designer
	designerURL
	manufacturer
	manufacturerURL
	versionMajor
	versionMinor
	date
	familyName
	upm
	note
	kerning
	userData
	grid
	gridSubDivisions
	gridLength
	disablesNiceNames
	customParameters
	selectedLayers
	selectedFontMaster
	masterIndex
	currentText
	tabs
	currentTab
	filepath

Functions

.. autosummary::
	
	save()
	close()
	disableUpdateInterface()
	enableUpdateInterface()
	kerningForPair()
	setKerningForPair()
	removeKerningForPair()
	newTab()

----------
Properties
----------

'''


def Font__new__(typ, *args, **kwargs):
	if len(args) > 0 and (type(args[0]) == type(str) or type(args[0]) == type(unicode)):
		path = args[0]
		URL = NSURL.fileURLWithPath_(path)
		typeName = NSWorkspace.sharedWorkspace().typeOfFile_error_(path, None)
		Doc = GSDocument.alloc().initWithContentsOfURL_ofType_error_(URL, typeName, None)
		if Doc is not None:
			return Doc.font()
		raise("Unable to open font")
	else:
		return GSFont.alloc().init()
GSFont.__new__ = Font__new__

def Font__init__(self, path=None):
	pass

GSFont.__init__ = Font__init__

def Font__repr__(self):
	return "<GSFont \"%s\" v%s.%s with %s masters and %s instances>" % (self.familyName, self.versionMajor, self.versionMinor, len(self.masters), len(self.instances))
GSFont.__repr__ = Font__repr__


GSFont.parent = property(lambda self: self.valueForKey_("parent"))
'''.. attribute:: parent
	Returns the internal NSDocument document. Readonly.
	:type: NSDocument
	'''

GSFont.masters = property(lambda self: FontFontMasterProxy(self),
						  lambda self, value: self.setFontMasters_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: masters
	Collection of :class:`GSFontMaster <GSFontMaster>`.
	:type: list
	'''

GSFont.instances = property(lambda self: FontInstancesProxy(self),
							lambda self, value: self.setInstances_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: instances
	Collection of :class:`GSInstance <GSInstance>`.
	:type: list
'''

GSFont.glyphs = property(lambda self: FontGlyphsProxy(self),
						 lambda self, value: self.setGlyphs_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: glyphs
	Collection of :class:`GSGlyph <GSGlyph>`. Returns a list, but you may also call glyphs using index or glyph name as key.
	.. code-block:: python
		# Access all glyphs
		for glyph in font.glyphs:
			print glyph
		<GSGlyph "A" with 4 layers>
		<GSGlyph "B" with 4 layers>
		<GSGlyph "C" with 4 layers>
		...

		# Access one glyph
		print font.glyphs['A']
		<GSGlyph "A" with 4 layers>
		
		# Add a glyph
		font.glyphs.append(GSGlyph('adieresis'))
		
		# Duplicate a glyph under a different name
		newGlyph = font.glyphs['A'].copy()
		newGlyph.name = 'A.alt'
		font.glyphs.append(newGlyph)

		# Delete a glyph
		del(font.glyphs['A.alt'])

	:type: list, dict'''
GSFont.classes = property(lambda self: FontClassesProxy(self),
						  lambda self, value: self.setClasses_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: classes
	Collection of :class:`GSClass <GSClass>` objects, representing OpenType glyph classes.
	:type: list
	
	.. code-block:: python
	
		# add a class
		font.classes.append(GSClass('uppercaseLetters', 'A B C D E'))
	
		# access all classes
		for class in font.classes:
			print class.name
	
		# access one class
		print font.classes['uppercaseLetters'].code
	
		# delete a class
		del(font.classes['uppercaseLetters'])
'''
GSFont.features = property(lambda self: FontFeaturesProxy(self),
						   lambda self, value: self.setFeatures_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: features
	Collection of :class:`GSFeature <GSFeature>` objects, representing OpenType features.
	:type: list

	.. code-block:: python
	
		# add a feature
		font.features.append(GSFeature('liga', 'sub f i by fi;'))
	
		# access all features
		for feature in font.features:
			print feature.code
	
		# access one feature
		print font.features['liga'].code
	
		# delete a feature
		del(font.features['liga'])
'''

GSFont.featurePrefixes = property(lambda self: FontFeaturePrefixesProxy(self),
								  lambda self, value: self.setFeaturePrefixes_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: featurePrefixes
	Collection of :class:`GSFeaturePrefix <GSFeaturePrefix>` objects, containing stuff that needs to be outside of the OpenType features.
	:type: list

	.. code-block:: python
	
		# add a prefix
		font.featurePrefixes.append(GSFeaturePrefix('LanguageSystems', 'languagesystem DFLT dflt;'))
	
		# access all prefixes
		for prefix in font.featurePrefixes:
			print prefix.code
	
		# access one prefix
		print font.featurePrefixes['LanguageSystems'].code
	
		# delete
		del(font.featurePrefixes['LanguageSystems'])
'''

GSFont.copyright = property(lambda self: self.valueForKey_("copyright"), lambda self, value: self.setValue_forKey_(value, "copyright"))
'''.. attribute:: copyright
	:type: unicode'''
GSFont.designer = property(lambda self: self.valueForKey_("designer"), lambda self, value: self.setValue_forKey_(value, "designer"))
'''.. attribute:: designer
	:type: unicode'''
GSFont.designerURL = property(lambda self: self.valueForKey_("designerURL"), lambda self, value: self.setValue_forKey_(value, "designerURL"))
'''.. attribute:: designerURL
	:type: unicode'''
GSFont.manufacturer = property(lambda self: self.valueForKey_("manufacturer"), lambda self, value: self.setValue_forKey_(value, "manufacturer"))
'''.. attribute:: manufacturer
	:type: unicode'''
GSFont.manufacturerURL = property(lambda self: self.valueForKey_("manufacturerURL"), lambda self, value: self.setValue_forKey_(value, "manufacturerURL"))
'''.. attribute:: manufacturerURL
	:type: unicode'''
GSFont.versionMajor = property(lambda self: self.valueForKey_("versionMajor"), lambda self, value: self.setValue_forKey_(value, "versionMajor"))
'''.. attribute:: versionMajor
	:type: int'''
GSFont.versionMinor = property(lambda self: self.valueForKey_("versionMinor"), lambda self, value: self.setValue_forKey_(value, "versionMinor"))
'''.. attribute:: versionMinor
	:type: int'''
GSFont.date = property(lambda self: self.valueForKey_("date"), lambda self, value: self.setValue_forKey_(value, "date"))
'''.. attribute:: date
	:type: NSDate
	.. code-block:: python
		print font.date
		2015-06-08 09:39:05 +0000
		
		# set date to now
		font.date = NSDate.date()
'''
GSFont.familyName = property(lambda self: self.valueForKey_("familyName"), 
							 lambda self, value: self.setFamilyName_(value))
'''.. attribute:: familyName
	Family name of the typeface.
	:type: unicode'''
GSFont.upm = property(lambda self: self.valueForKey_("unitsPerEm"), lambda self, value: self.setValue_forKey_(value, "unitsPerEm"))
'''.. attribute:: upm
	Units per Em
	:type: int'''
GSFont.note = property(lambda self: self.valueForKey_("note"), 
							 lambda self, value: self.setValue_forKey_(value, "note"))
'''.. attribute:: note
	:type: unicode'''
GSFont.kerning = property(lambda self: self.valueForKey_("kerning"), lambda self, value: self.setKerning_(value))
'''.. attribute:: kerning
	A multi-level dictionary. The first level's key is the :class:`GSFontMaster`.id (each master has its own kerning), the second level's key is the :class:`GSGlyph <GSGlyph>`.id or class id (@MMK_L_XX), the third level's key is again a glyph id or class id (@MMK_R_XX). The values are the actual kerning values.
	
	To set a value, is is better to use the method :class:`GSFont`.setKerningForPair(). This ensures a better data integrity (and is faster).
	:type: dict
'''
GSFont.userData = property(lambda self: self.pyobjc_instanceMethods.userData(), lambda self, value: self.setUserData_(value))
'''.. attribute:: userData
	A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.
	:type: dict
	.. code-block:: python
		# set value
		font.userData['rememberToMakeCoffee'] = True
'''
GSFont.disablesNiceNames = property(lambda self: self.valueForKey_("disablesNiceNames").boolValue(), lambda self, value: self.setValue_forKey_(value, "disablesNiceNames"))
'''.. attribute:: disablesNiceNames
	Corresponds to the "Don't use nice names" setting from the Info dialogue.
	:type: bool'''
GSFont.customParameters = property(			lambda self: CustomParametersProxy(self))
'''.. attribute:: customParameters
	The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.
	.. code-block:: python
		
		# access all parameters
		for parameter in font.customParameters:
			print parameter
		
		# set a parameter
		font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'

		# delete a parameter
		del(font.customParameters['trademark'])
	
	:type: list, dict'''
GSFont.grid = property(lambda self: self.valueForKey_("gridMain").intValue(), lambda self, value: self.setValue_forKey_(value, "gridMain"))
'''.. attribute:: grid
	Corresponds to the "Grid spacing" setting from the Info dialogue.
	:type: int'''
GSFont.gridSubDivisions = property(lambda self: self.valueForKey_("gridSubDivision").intValue(), lambda self, value: self.setValue_forKey_(value, "gridSubDivision"))
'''.. attribute:: gridSubDivisions
	Corresponds to the "Grid sub divisions" setting from the Info dialogue.
	:type: int'''
GSFont.gridLength = property(lambda self: self.valueForKey_("gridLength").floatValue())
'''.. attribute:: gridLength
	Ready calculated size of grid for rounding purposes. Result of division of grid with gridSubDivisions.
	:type: float'''

GSFont.selectedLayers = property(lambda self: self.parent.selectedLayers())
'''.. attribute:: selectedLayers
	Returns a list of all selected layers in the active tab.
	:type: list'''

GSFont.selectedFontMaster = property(lambda self: self.parent.selectedFontMaster())
'''.. attribute:: selectedFontMaster
	Returns the active master (selected in the toolbar).
	:type: :class:`GSFontMaster <GSFontMaster>`'''

GSFont.masterIndex = property(lambda self: self.parent.masterIndex(),
							  lambda self, Index: self.parent.windowController().setMasterIndex_(Index % self.countOfFontMasters()))
'''.. attribute:: masterIndex
	Returns the index of the active master (selected in the toolbar).
	:type: int'''

def __current_Text__(self):
	try:
		return self.parent.windowController().activeEditViewController().graphicView().displayString()
	except:
		pass
	return None
def __set__current_Text__(self, String):
	#if String is None:
	#	String = ""
	self.parent.windowController().activeEditViewController().graphicView().setDisplayString_(String)

GSFont.currentText = property(lambda self: __current_Text__(self),
							  lambda self, value: __set__current_Text__(self, value))
'''.. attribute:: currentText
	The text of the current edit view. 
	
	Unencoded and none ASCII glyphs will use a slash and the glyph name. (e.g: /a.sc). Setting unicode strings works.
	
	:type: unicode'''


# Tab interaction:

GSFont.tabs = property(lambda self: FontTabsProxy(self))


'''.. attribute:: tabs
	List of open edit view tabs in UI, as list of :class:`GSEditViewController` objects.
	
	.. code-block:: python
		
		# open new tab with text
		font.newTab('hello')
		
		# access all tabs
		for tab in font.tabs:
			print tab
			
		# close last tab
		del(font.tabs[-1])
	
	:type: list'''

def __GSFont__currentTab__(self):
	return self.parent.windowController().activeEditViewController()
	
def __GSFont__set_currentTab__(self, TabItem):
	self.parent.windowController().tabBarControl().selectTabItem_(TabItem)

GSFont.currentTab = property(lambda self: __GSFont__currentTab__(self),
							lambda self, value: __GSFont__set_currentTab__(self, value))


'''.. attribute:: currentTab
	Active edit view tab.
	
	:type: :class:`GSEditViewController`'''


def Font_filepath(self):
	if self.parent is not None and self.parent.fileURL() is not None:
		return self.parent.fileURL().path()
	else:
		return None
GSFont.filepath = property(lambda self: Font_filepath(self))
'''.. attribute:: filepath
	On-disk location of GSFont object.
	:type: unicode'''

'''
---------
Functions
---------
'''


def Font__save__(self, path=None):
	if self.parent is not None:
		if path is None:
			self.parent.saveDocument_(None)
		else:
			URL = NSURL.fileURLWithPath_(path)
			self.parent.writeSafelyToURL_ofType_forSaveOperation_error_(URL, self.parent.fileType(), 1, objc.nil)
	elif path is not None:
		Doc = GSDocument.alloc().init()
		Doc.font = self
		URL = NSURL.fileURLWithPath_(path)
		if path.endswith('.glyphs'):
			typeName = "com.schriftgestaltung.glyphs"
		elif path.endswith('.ufo'):
			typeName = "org.unifiedfontobject.ufo"
		Doc.writeSafelyToURL_ofType_forSaveOperation_error_(URL, typeName, 1, objc.nil)
	else:
		raise("Now path set")
		
GSFont.save = Font__save__
'''.. function:: save([filePath])
	
	Saves the font.
	if no path is given, it saves to the existing location.

	:param filePath: Optional file path
	:type filePath: str
	'''

def Font__close__(self, ignoreChanges=True):
	if self.parent:
		if ignoreChanges:
			self.parent.close()
		else:
			self.parent.canCloseDocumentWithDelegate_shouldCloseSelector_contextInfo_(None, None, None)
GSFont.close = Font__close__

'''.. function:: close([ignoreChanges = False])
	
	Closes the font

	:param ignoreChanges: Optional. Ignore changes to the font upon closing
	:type ignoreChanges: bool
	'''


'''.. function:: disableUpdateInterface()
	
	Call this before you do big changes to the font, or to its glyphs. Make sure that you call Font.enableUpdateInterface() when you are done.
	
	'''
'''.. function:: enableUpdateInterface()
	
	This re-enables the interface update. Only makes sense to call if you have disabled it earlier.
	
	'''



def kerningForPair(self, FontMasterID, LeftKeringId, RightKerningId ):
	if not LeftKeringId[0] == '@':
		LeftKeringId = self.glyphs[LeftKeringId].id
	if not RightKerningId[0] == '@':
		RightKerningId = self.glyphs[RightKerningId].id
	return self.kerningForFontMasterID_LeftKey_RightKey_(FontMasterID, LeftKeringId, RightKerningId)
GSFont.kerningForPair = kerningForPair
'''.. function:: kerningForPair(FontMasterId, LeftKey, RightKey)
	
	This returns the kerning value for the two specified glyphs (LeftKey or RightKey is the glyphname) or a kerning group key (@MMK_X_XX).
	
	:param FontMasterId: The id of the FontMaster
	:type FontMasterId: str
	:param LeftKey: either a glyph name or a class name
	:type LeftKey: str
	:param RightKey: either a glyph name or a class name
	:type RightKey: str
	:return: The kerning value
	:rtype: float

	.. code-block:: python
		
		# print kerning between w and e for currently selected master
		font.kerningForPair(font.selectedFontMaster.id, 'w', 'e')
		-15.0

		# print kerning between group T and group A for currently selected master
		# ('L' = left side of the pair and 'R' = left side of the pair)
		font.kerningForPair(font.selectedFontMaster.id, '@MMK_L_T', '@MMK_R_A')
		-75.0

		# in the same font, kerning between T and A would be zero, because they use group kerning instead.
		font.kerningForPair(font.selectedFontMaster.id, 'T', 'A')
		9.22337203685e+18 # (this is the maximum number for 64 bit. It is used as an empty value)
'''

def setKerningForPair(self, FontMasterID, LeftKeringId, RightKerningId, Value):
	if not LeftKeringId[0] == '@':
		LeftKeringId = self.glyphs[LeftKeringId].id
	if not RightKerningId[0] == '@':
		RightKerningId = self.glyphs[RightKerningId].id
	self.setKerningForFontMasterID_LeftKey_RightKey_Value_(FontMasterID, LeftKeringId, RightKerningId, Value)
GSFont.setKerningForPair = setKerningForPair
'''.. function:: setKerningForPair(FontMasterId, LeftKey, RightKey, Value)
	
	This sets the kerning for the two specified glyphs (LeftKey or RightKey is the glyphname) or a kerning group key (@MMK_X_XX).
	
	:param FontMasterId: The id of the FontMaster
	:type FontMasterId: str
	:param LeftKey: either a glyph name or a class name
	:type LeftKey: str
	:param RightKey: either a glyph name or a class name
	:type RightKey: str
	:param Value: kerning value
	:type Value: float

	.. code-block:: python
		# set kerning for group T and group A for currently selected master
		# ('L' = left side of the pair and 'R' = left side of the pair)
		font.setKerningForPair(font.selectedFontMaster.id, '@MMK_L_T', '@MMK_R_A', -75)
'''

def removeKerningForPair(self, FontMasterID, LeftKeringId, RightKerningId):
	if LeftKeringId[0] != '@':
		try:
			LeftKeringId = self.glyphs[LeftKeringId].id
		except:
			pass
	if RightKerningId[0] != '@':
		try:
			RightKerningId = self.glyphs[RightKerningId].id
		except:
			pass
	self.removeKerningForFontMasterID_LeftKey_RightKey_(FontMasterID, LeftKeringId, RightKerningId)
GSFont.removeKerningForPair = removeKerningForPair
'''.. function:: removeKerningForPair(FontMasterId, LeftKey, RightKey)
	
	Removes the kerning for the two specified glyphs (LeftKey or RightKey is the glyphname) or a kerning group key (@MMK_X_XX).
	
	:param FontMasterId: The id of the FontMaster
	:type FontMasterId: str
	:param LeftKey: either a glyph name or a class name
	:type LeftKey: str
	:param RightKey: either a glyph name or a class name
	:type RightKey: str

	.. code-block:: python
		# remove kerning for group T and group A for all masters
		# ('L' = left side of the pair and 'R' = left side of the pair)
		for master in font.masters:
			font.removeKerningForPair(master.id, '@MMK_L_T', '@MMK_R_A')
'''

def __GSFont__addTab__(self, tabText = ""):
	if self.parent:
		self.parent.windowController().addTabWithString_(tabText)

GSFont.newTab = __GSFont__addTab__

'''.. function:: newTab([tabText])
	
	Opens a new tab in the current document window, optionally with text
	
	:param tabText: Text or glyph names with '/'
'''





##################################################################################
#
#
#
#           GSFontMaster
#
#
#
##################################################################################


'''

:mod:`GSFontMaster`
===============================================================================

Implementation of the master object. This corresponds with the "Masters" pane in the Font Info.

In Glyphs.app the glyphs of each master are reachable not here, but as :class:`Layers <GSLayer>` attached to the :class:`Glyphs <GSGlyph>` attached to the :class:`Font <GSFont>` object. See info graphic on top for better understanding.

.. class:: GSFontMaster()

'''

def FontMaster__new__(typ, *args, **kwargs):
	return GSFontMaster.alloc().init()
GSFontMaster.__new__ = FontMaster__new__;

def FontMaster__init__(self):
	pass
GSFontMaster.__init__ = FontMaster__init__;

def FontMaster__repr__(self):
	return "<GSFontMaster \"%s\" width %s weight %s>" % (self.name, self.widthValue, self.weightValue)
GSFontMaster.__repr__ = FontMaster__repr__;

'''

Properties

.. autosummary::

	id
	name
	weight
	width
	weightValue
	widthValue
	customValue
	customName
	ascender
	capHeight
	xHeight
	descender
	italicAngle
	verticalStems
	horizontalStems
	alignmentZones
	blueValues
	otherBlues
	guides
	userData
	customParameters

----------
Properties
----------

'''

GSFontMaster.id = property(lambda self: self.valueForKey_("id"), lambda self, value: self.setId_(value))
'''.. attribute:: id
	Used to identify :class:`Layers <GSLayer>` in the Glyph

	see :attr:`GSGlyph.layers <layers>`

	.. code-block:: python
		# ID of first master
		print font.masters[0].id
		3B85FBE0-2D2B-4203-8F3D-7112D42D745E
		
		# use this master to access the glyph's corresponding layer
		print glyph.layers[font.masters[0].id]
		<GSLayer "Light" (A)>
	
	:type: unicode'''
GSFontMaster.name = property(lambda self: self.valueForKey_("name"), lambda self, value: self.setName_(value))
'''.. attribute:: name
	Name of the master. This is a combination of GSFontMaster.weight and GSFontMaster.width and is a human readable identification of each master, e.g. "Bold Condensed".
	:type: string'''
GSFontMaster.weight = property(lambda self: self.valueForKey_("weight"), lambda self, value: self.setValue_forKey_(value, "weight"))
'''.. attribute:: weight
	Human readable weight name, chosen from list in Font Info. For actual position in interpolation design space, use GSFontMaster.weightValue.
	:type: string'''
GSFontMaster.width = property(lambda self: self.valueForKey_("width"), lambda self, value: self.setValue_forKey_(value, "width"))
'''.. attribute:: width
	Human readable width name, chosen from list in Font Info. For actual position in interpolation design space, use GSFontMaster.widthValue.
	:type: string'''
GSFontMaster.weightValue = property(lambda self: self.valueForKey_("weightValue"), lambda self, value: self.setValue_forKey_(value, "weightValue"))
'''.. attribute:: weightValue
	Value for interpolation in design space.
	:type: float'''
GSFontMaster.widthValue = property(lambda self: self.valueForKey_("widthValue"), lambda self, value: self.setValue_forKey_(value, "widthValue"))
'''.. attribute:: widthValue
	Value for interpolation in design space.
	:type: float'''
GSFontMaster.customName = property(lambda self: self.valueForKey_("custom"), lambda self, value: self.setValue_forKey_(value, "custom"))
'''.. attribute:: customName
	The name of the custom interpolation dimension.
	:type: string'''
GSFontMaster.customValue = property(lambda self: self.valueForKey_("customValue"), lambda self, value: self.setValue_forKey_(value, "customValue"))
'''.. attribute:: customValue
	Value for interpolation in design space.'''
GSFontMaster.ascender = property(lambda self: self.valueForKey_("ascender"), lambda self, value: self.setValue_forKey_(value, "ascender"))
'''.. attribute:: ascender
	:type: float'''
GSFontMaster.capHeight = property(lambda self: self.valueForKey_("capHeight"), lambda self, value: self.setValue_forKey_(value, "capHeight"))
'''.. attribute:: capHeight
	:type: float'''
GSFontMaster.xHeight = property(lambda self: self.valueForKey_("xHeight"), lambda self, value: self.setValue_forKey_(value, "xHeight"))
'''.. attribute:: xHeight
	:type: float'''
GSFontMaster.descender = property(lambda self: self.valueForKey_("descender"), lambda self, value: self.setValue_forKey_(value, "descender"))
'''.. attribute:: descender
	:type: float'''
GSFontMaster.italicAngle = property(lambda self: self.valueForKey_("italicAngle"), lambda self, value: self.setValue_forKey_(value, "italicAngle"))
'''.. attribute:: italicAngle
	:type: float'''
GSFontMaster.verticalStems = property(lambda self: self.valueForKey_("verticalStems"), lambda self, value: self.setValue_forKey_(value, "verticalStems"))
'''.. attribute:: verticalStems
	The vertical stems. This is a list of numbers. 
	:type: list'''
GSFontMaster.horizontalStems = property(lambda self: self.valueForKey_("horizontalStems"), lambda self, value: self.setValue_forKey_(value, "horizontalStems"))
'''.. attribute:: horizontalStems
	The horizontal stems. This is a list of numbers. 
	:type: list'''
GSFontMaster.alignmentZones = property(lambda self: self.valueForKey_("alignmentZones"), lambda self, value: self.setValue_forKey_(value, "alignmentZones"))
#GSFontMaster.alignmentZones = property(lambda self: self.mutableArrayValueForKey_("alignmentZones"), lambda self, value: self.setValue_forKey_(value, "alignmentZones"))
'''.. attribute:: alignmentZones
	Collection of :class:`GSAlignmentZone <GSAlignmentZone>`.
	:type: list'''

def FontMaster_blueValues(self):
	return GSGlyphsInfo.blueValues_(self.alignmentZones)
GSFontMaster.blueValues = property(lambda self: FontMaster_blueValues(self))
'''.. attribute:: blueValues
	PS hinting Blue Values calculated from the master's alignment zones. Read only.
	:type: list'''
def FontMaster_otherBlues(self):
	return GSGlyphsInfo.otherBlues_(self.alignmentZones)
GSFontMaster.otherBlues = property(lambda self: FontMaster_otherBlues(self))
'''.. attribute:: otherBlues
	PS hinting Other Blues calculated from the master's alignment zones. Read only.
	:type: list'''

# new (guidelines at layers are also called just 'guides')
GSFontMaster.guides = property(lambda self: self.valueForKey_("guideLines"), lambda self, value: self.setValue_forKey_(value, "guideLines"))
# keep for compatibility
GSFontMaster.guideLines = GSFontMaster.guides
'''.. attribute:: guides
	Collection of :class:`GSGuideLine <GSGuideLine>`. These are the font-wide (actually master-wide) red guidelines. For glyph-level guidelines (attached to the layers) see :attr:`GSLayer`.guides
	:type: list'''
GSFontMaster.userData = property(lambda self: self.pyobjc_instanceMethods.userData(), lambda self, value: self.setValue_forKey_(value, "userData"))
'''.. attribute:: userData
	A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the date will not be recoverable from the saved file.
	:type: dict
	.. code-block:: python
		# set value
		font.masters[0].userData['rememberToMakeTea'] = True
'''
GSFontMaster.customParameters = property(lambda self: CustomParametersProxy(self))
'''.. attribute:: customParameters
	The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.
	
	.. code-block:: python
		
		# access all parameters
		for parameter in font.masters[0].customParameters:
			print parameter
		
		# set a parameter
		font.masters[0].customParameters['underlinePosition'] = -135

		# delete a parameter
		del(font.masters[0].customParameters['underlinePosition'])
	
	:type: list, dict'''

##################################################################################
#
#
#
#           GSElement
#
#
#
##################################################################################


GSElement.selected = property(	lambda self: ObjectInLayer_selected(self) )


##################################################################################
#
#
#
#           GSAlignmentZone
#
#
#
##################################################################################


'''
	
:mod:`GSAlignmentZone`
===============================================================================

Implementation of the alignmentZone object.

There is no distinction between Blue zones and other Zones. All negative zone (except the one with position 0) will be exported as Other zones.

The zone for the baseline should have position 0 (zero) and a negative width.

.. class:: GSAlignmentZone([pos, size])

	:param pos: The position of the zone
	:param size: The size of the zone
'''

def AlignmentZone__new__(typ, *args, **kwargs):
	return GSAlignmentZone.alloc().init()
GSAlignmentZone.__new__ = AlignmentZone__new__;

def AlignmentZone__init__(self, pos = 0, size = 20):
	self.setPosition_(pos)
	self.setSize_(size)

GSAlignmentZone.__init__ = AlignmentZone__init__;

def AlignmentZone__repr__(self):
	#return "<GSAlignmentZone pos %s size %s>" % (self.position, self.size)
	return "<GSAlignmentZone pos %s size %s>" % (self.position(), self.size())
GSAlignmentZone.__repr__ = AlignmentZone__repr__;


'''
Properties

.. autosummary::

	position
	size
	
	
----------
Properties
----------
	
'''

GSAlignmentZone.position = property(lambda self: self.valueForKey_("position"), lambda self, value: self.setPosition_(value))
'''.. attribute:: position
	
	:type: int
	
	'''
GSAlignmentZone.size = property(lambda self: self.valueForKey_("size"), lambda self, value: self.setSize_(value))
'''.. attribute:: size
	
	:type: int
'''




##################################################################################
#
#
#
#           GSInstance
#
#
#
##################################################################################


'''

:mod:`GSInstance`
===============================================================================

Implementation of the instance object. This corresponds with the "Instances" pane in the Font Info.

.. class:: GSInstance()

'''

def Instance__new__(typ, *args, **kwargs):
	return GSInstance.alloc().init()
GSInstance.__new__ = Instance__new__;

def Instance__init__(self):
	pass
GSInstance.__init__ = Instance__init__;

def Instance__repr__(self):
	return "<GSInstance \"%s\" width %s weight %s>" % (self.name, self.widthValue, self.weightValue)
GSInstance.__repr__ = Instance__repr__;


'''
Properties

.. autosummary::


	active
	name
	weight
	width
	weightValue
	widthValue
	customValue
	isItalic
	isBold
	linkStyle
	familyName
	preferredFamily
	preferredSubfamilyName
	windowsFamily
	windowsStyle
	windowsLinkedToStyle
	fontName
	fullName
	customParameters
	instanceInterpolations
	manualInterpolation
	
Functions
	
.. autosummary::
	
	generate()

----------
Properties
----------

'''

GSInstance.active = property(lambda self: self.valueForKey_("active").boolValue(), lambda self, value: self.setValue_forKey_(value, "active"))
'''.. attribute:: active
	:type: bool'''
GSInstance.name = property(lambda self: self.valueForKey_("name"), lambda self, value: self.setName_(value))
'''.. attribute:: name
	Name of instance. Corresponds to the "Style Name" field in the font info. This is used for naming the exported fonts.
	:type: string'''
GSInstance.weight = property(lambda self: self.valueForKey_("weightClass"), lambda self, value: self.setValue_forKey_(value, "weightClass"))
'''.. attribute:: weight
	Human readable weight name, chosen from list in Font Info. For actual position in interpolation design space, use GSInstance.weightValue.
	:type: string'''
GSInstance.width = property(lambda self: self.valueForKey_("widthClass"), lambda self, value: self.setValue_forKey_(value, "widthClass"))
'''.. attribute:: width
	Human readable width name, chosen from list in Font Info. For actual position in interpolation design space, use GSInstance.widthValue.
	:type: string'''
GSInstance.weightValue = property(lambda self: self.valueForKey_("interpolationWeight"), lambda self, value: self.setValue_forKey_(value, "interpolationWeight"))
'''.. attribute:: weightValue
	Value for interpolation in design space.
	:type: float'''
GSInstance.widthValue = property(lambda self: self.valueForKey_("interpolationWidth"), lambda self, value: self.setValue_forKey_(value, "interpolationWidth"))
'''.. attribute:: widthValue
	Value for interpolation in design space.
	:type: float'''
GSInstance.customValue = property(lambda self: self.valueForKey_("interpolationCustom"), lambda self, value: self.setValue_forKey_(value, "interpolationCustom"))
'''.. attribute:: customValue
	Value for interpolation in design space.
	:type: float'''
GSInstance.isItalic = property(lambda self: self.valueForKey_("isItalic").boolValue(), lambda self, value: self.setValue_forKey_(value, "isItalic"))
'''.. attribute:: isItalic
	Italic flag for style linking
	:type: bool'''
GSInstance.isBold = property(lambda self: self.valueForKey_("isBold").boolValue(), lambda self, value: self.setValue_forKey_(value, "isBold"))
'''.. attribute:: isBold
	Bold flag for style linking
	:type: bool'''
GSInstance.linkStyle = property(lambda self: self.valueForKey_("linkStyle"), lambda self, value: self.setValue_forKey_(value, "linkStyle"))
'''.. attribute:: linkStyle
	Linked style
	:type: string'''
GSInstance.familyName = property(lambda self: self.valueForKey_("familyName"), lambda self, value: self.setCustomParameter_forKey_(value, "familyName"))
'''.. attribute:: familyName
	familyName
	:type: string'''
GSInstance.preferredFamily = property(lambda self: self.valueForKey_("preferredFamily"), lambda self, value: self.setCustomParameter_forKey_(value, "preferredFamily"))
'''.. attribute:: preferredFamily
	preferredFamily
	:type: string'''
GSInstance.preferredSubfamilyName = property(lambda self: self.valueForKey_("preferredSubfamilyName"), lambda self, value: self.setCustomParameter_forKey_(value, "preferredSubfamilyName"))
'''.. attribute:: preferredSubfamilyName
	preferredSubfamilyName
	:type: string'''
GSInstance.windowsFamily = property(lambda self: self.valueForKey_("windowsFamily"), lambda self, value: self.setCustomParameter_forKey_(value, "styleMapFamilyName"))
'''.. attribute:: windowsFamily
	windowsFamily
	:type: string'''
GSInstance.windowsStyle = property(lambda self: self.valueForKey_("windowsStyle"))
'''.. attribute:: windowsStyle
	windowsStyle
	This is computed from "isBold" and "isItalic". Readonly.
	:type: string'''
GSInstance.windowsLinkedToStyle = property(lambda self: self.valueForKey_("windowsLinkedToStyle"))
'''.. attribute:: windowsLinkedToStyle
	windowsLinkedToStyle. Readonly.
	:type: string'''
GSInstance.fontName = property(lambda self: self.valueForKey_("fontName"), lambda self, value: self.setCustomParameter_forKey_(value, "postscriptFontName"))
'''.. attribute:: fontName
	fontName (postscriptFontName)
	:type: string'''
GSInstance.fullName = property(lambda self: self.valueForKey_("fullName"), lambda self, value: self.setCustomParameter_forKey_(value, "postscriptFullName"))
'''.. attribute:: linkStyle
	fullName (postscriptFullName)
	:type: string'''

GSInstance.customParameters = property(lambda self: CustomParametersProxy(self))
'''.. attribute:: customParameters
	The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.
	
	.. code-block:: python
		
		# access all parameters
		for parameter in font.instances[0].customParameters:
			print parameter
		
		# set a parameter
		font.instances[0].customParameters['hheaLineGap'] = 10

		# delete a parameter
		del(font.instances[0].customParameters['hheaLineGap'])
	
	:type: list, dict'''

GSInstance.instanceInterpolations = property(lambda self: self.pyobjc_instanceMethods.instanceInterpolations(), lambda self, value: self.setInstanceInterpolations_(value))
'''.. attribute:: instanceInterpolations
	A dict that contains the interpolation coefficents for each master.
	This is automatcially updated if you change interpolationWeight, interpolationWidth, interpolationCustom. It contains FontMaster IDs as keys and coeffients for that master as values.
	Or, you can set it manually if you set manualInterpolation to True. There is no UI for this, so you need to do that with a script.
	:type: dict
	'''

GSInstance.manualInterpolation = property(lambda self: self.valueForKey_("manualInterpolation"), lambda self, value: self.setValue_forKey_(value, "manualInterpolation"))
'''.. attribute:: manualInterpolation
	Disables automatic calculation of instanceInterpolations
	This allowes manual setting of instanceInterpolations.
	:type: bool
	'''


'''
---------
Functions
---------


.. function:: generate([Format, FontPath, AutoHint, RemoveOverlap, UseSubroutines, UseProductionNames])
	
	Exports the instance.
	
	:param str Format: 'OTF' or 'TTF'. Default: 'OTF'
	:param str FontPath: The destination path for the final fonts. If None, it uses the default location set in the export dialog
	:param bool AutoHint: If autohinting should be applied. Default: True
	:param bool RemoveOverlap: If overlaps should be removed. Default: True
	:param bool UseSubroutines: If to use subroutines for CFF. Default: True
	:param bool UseProductionNames: If to use production names. Default: True
	:return: On success, True, on failure error message.
	:rtype: bool/list


	.. code-block:: python
		
		# export all instances as OpenType (.otf) to user's font folder

		exportFolder = '/Users/myself/Library/Fonts'
		
		for instance in Glyphs.font.instances:
			instance.generate(FontPath = exportFolder)
			
		Glyphs.showNotification('Export fonts', 'The export of %s was successful.' % (Glyphs.font.familyName))
'''


class _ExporterDelegate_ (NSObject):
	def init(self):
		self = super(_ExporterDelegate_, self).init()
		self.result = True
		return self
	
	def collectResults_(self, Error): # Error might be a NSString or a NSError
		if Error.__class__.__name__ == "NSError":
			String = Error.localizedDescription()
			if Error.localizedRecoverySuggestion().length() > 0:
				String = String.stringByAppendingString_(Error.localizedRecoverySuggestion())
			Error = unicode(String)
		self.result = Error

def __Instance_Export__(self, Format = "OTF", FontPath = None, AutoHint = True, RemoveOverlap = True, UseSubroutines = True, UseProductionNames = True):
	
	if Format == "OTF":
		Format = 0
	else:
		Format = 1 # 0 == OTF, 1 = TTF
	Font = self.font()
	Exporter = NSClassFromString("GSExportInstanceOperation").alloc().initWithFont_instance_format_(Font, self, Format)
	if FontPath is None:
		FontPath = NSUserDefaults.standardUserDefaults().objectForKey_("OTFExportPath")

	Exporter.setInstallFontURL_(NSURL.fileURLWithPath_(FontPath))
	# the following parameters can be set here or directly read from the instance.
	Exporter.setAutohint_(AutoHint)
	Exporter.setRemoveOverlap_(RemoveOverlap)
	Exporter.setUseSubroutines_(UseSubroutines)
	Exporter.setUseProductionNames_(UseProductionNames)

	Exporter.setTempPath_(os.path.expanduser("~/Library/Application Support/Glyphs/Temp/")) # this has to be set correctly.

	Delegate = _ExporterDelegate_.alloc().init() # the collectResults_() method of this object will be called on case the exporter has to report a problem.
	Exporter.setDelegate_(Delegate)
	Exporter.main()
	return Delegate.result

GSInstance.generate = __Instance_Export__




##################################################################################
#
#
#
#           GSCustomParameter
#
#
#
##################################################################################


'''
	
:mod:`GSCustomParameter`
===============================================================================

Implementation of the Custom Parameter object. It stores a name/value pair.

You can append GSCustomParameter objects for example to GSFont.customParameters, but this way you may end up with duplicates.
It is best to access the custom parameters through its dictionary interface like this:
.. code-block:: python
	
	# access all parameters
	for parameter in font.customParameters:
		print parameter
	
	# set a parameter
	font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'

	# delete a parameter
	del(font.customParameters['trademark'])

.. class:: GSCustomParameter([name, value])
	
	:param name: The name
	:param size: The value
'''

def CustomParameter__new__(typ, *args, **kwargs):
	return GSCustomParameter.alloc().init()

GSCustomParameter.__new__ = CustomParameter__new__;

def CustomParameter__init__(self, name, value):
	self.setName_(name)
	self.setValue_(value)

GSCustomParameter.__init__ = CustomParameter__init__;

def CustomParameter__repr__(self):
	return "<GSCustomParameter %s: %s>" % (self.name, self.value)
GSCustomParameter.__repr__ = CustomParameter__repr__;


'''
Properties

.. autosummary::

	name
	value
	
	
----------
Properties
----------
	
	'''

GSCustomParameter.name = property(lambda self: self.valueForKey_("name"), lambda self, value: self.setName_(value))
'''.. attribute:: name
	
	:type: str
	'''
GSCustomParameter.value = property(lambda self: self.valueForKey_("value"), lambda self, value: self.setValue_(value))
'''.. attribute:: value
	
	:type: str, list, dict, int, float
	
	'''










##################################################################################
#
#
#
#           GSClass
#
#
#
##################################################################################

'''
:mod:`GSClass`
===============================================================================

Implementation of the class object. It is used to store OpenType classes.

For details on how to access them, please look at :class:`GSFont`.classes

.. class:: GSClass([tag, code])

	:param tag: The class name
	:param code: A list of glyph names, separated by space or newline

Properties

.. autosummary::

	name
	code
	automatic

----------
Properties
----------

'''

def Class__new__(typ, *args, **kwargs):
	return GSClass.alloc().init()
GSClass.__new__ = Class__new__;

def Class__init__(self, name = None, code = None):
	if name is not None:
		self.setName_(name)
	if code is not None:
		self.setCode_(code)
GSClass.__init__ = Class__init__;

def Class__repr__(self):
	return "<GSClass \"%s\">" % (self.name)
GSClass.__repr__ = Class__repr__;

GSClass.name = property(lambda self: self.valueForKey_("name"), 
							 lambda self, value: self.setName_(value))
'''.. attribute:: name
	The class name
	:type: unicode'''
GSClass.code = property(lambda self: self.valueForKey_("code"), 
							 lambda self, value: self.setCode_(value))
'''.. attribute:: code
	A string with space separated glyph names.
	:type: unicode
'''
GSClass.automatic = property(lambda self: self.valueForKey_("automatic").boolValue(), 
							 lambda self, value: self.setAutomatic_(value))
'''.. attribute:: automatic
	Define whether this class should be auto-generated when pressing the 'Update' button in the Font Info.
	:type: bool
'''



##################################################################################
#
#
#
#           GSFeaturePrefix
#
#
#
##################################################################################

'''
:mod:`GSFeaturePrefix`
===============================================================================
	
Implementation of the featurePrefix object. It is used to store things that need to be outside of a feature like standalone lookups.

For details on how to access them, please look at :class:`GSFont`.featurePrefixes
	
.. class:: GSFeaturePrefix([tag, code])
	
	:param tag: The Prefix name
	:param code: The feature code in Adobe FDK syntax
	
Properties

.. autosummary::

	name
	code
	automatic

----------
Properties
----------
	
	'''

def FeaturePrefix__new__(typ, *args, **kwargs):
	return GSFeaturePrefix.alloc().init()
GSFeaturePrefix.__new__ = FeaturePrefix__new__;

def FeaturePrefix__init__(self, name = None, code = None):
	if name is not None:
		self.setName_(name)
	if code is not None:
		self.setCode_(code)

GSFeaturePrefix.__init__ = FeaturePrefix__init__;

def FeaturePrefix__repr__(self):
	return "<GSFeaturePrefix \"%s\">" % (self.name)
GSFeaturePrefix.__repr__ = FeaturePrefix__repr__;

GSFeaturePrefix.name = property(lambda self: self.valueForKey_("name"),
						lambda self, value: self.setName_(value))
'''.. attribute:: name
	The FeaturePrefix name
	:type: unicode'''
GSFeaturePrefix.code = property(lambda self: self.valueForKey_("code"),
						lambda self, value: self.setCode_(value))
'''.. attribute:: code
	A String containing feature code.
	:type: unicode
	'''
GSFeaturePrefix.automatic = property(lambda self: self.valueForKey_("automatic").boolValue(),
							 lambda self, value: self.setAutomatic_(value))
'''.. attribute:: automatic
	Define whether this should be auto-generated when pressing the 'Update' button in the Font Ínfo.
	:type: bool
	'''






##################################################################################
#
#
#
#           GSFeature
#
#
#
##################################################################################

'''

:mod:`GSFeature`
===============================================================================

Implementation of the feature object. It is used to implement OpenType Features in the Font Info.

For details on how to access them, please look at :class:`GSFont`.features

.. class:: GSFeature([tag, code])
	
	:param tag: The feature name
	:param code: The feature code in Adobe FDK syntax
	
Properties

.. autosummary::

	name
	code
	automatic
	notes
	
Functions

.. autosummary::

	update()
	

----------
Properties
----------

'''


def Feature__new__(typ, *args, **kwargs):
	#print "new", args, kwargs
	return GSFeature.alloc().init()
GSFeature.__new__ = Feature__new__;

def Feature__init__(self, name = None, code = None):
	if name is not None:
		self.setName_(name)
	if code is not None:
		self.setCode_(code)
	
GSFeature.__init__ = Feature__init__;

def Feature__repr__(self):
	return "<GSFeature \"%s\">" % (self.name)
GSFeature.__repr__ = Feature__repr__;

GSFeature.name = property(lambda self: self.valueForKey_("name"), 
								 lambda self, value: self.setName_(value))
'''.. attribute:: name
	The feature name
	:type: unicode'''

GSFeature.code = property(lambda self: self.valueForKey_("code"), 
								 lambda self, value: self.setCode_(value))
'''.. attribute:: code
	The Feature code in Adobe FDK syntax.
	:type: unicode'''
GSFeature.automatic = property(lambda self: self.valueForKey_("automatic").boolValue(), 
								 lambda self, value: self.setAutomatic_(value))
'''.. attribute:: automatic
	Define whether this feature should be auto-generated when pressing the 'Update' button in the Font Ínfo.
	:type: bool
'''

GSFeature.notes = property(lambda self: self.valueForKey_("notes"),
							   lambda self, value: self.setNotes_(value))
'''.. attribute:: notes
	Some extra text. Is shown in the bottom of the feature window. Contains the stylistic set name parameter
	:type: unicode
	'''

'''

---------
Functions
---------


'''

'''.. function:: update()
	
	Calls the automatic feature code generator for this feature.
	You can use this to update all OpenType features before export.
	
	:return: None

.. code-block:: python
	
	# first update all features
	for feature in font.features:
		if feature.automatic:
			feature.update()
	
	# then export fonts
	for instance in font.instances:
		if instance.active:
			instance.generate()
	
'''











##################################################################################
#
#
#
#           GSSubstitution
#
#
#
##################################################################################


"""

############ NOCH NICHT DOKUMENTIERT WEIL NOCH NICHT AUSGEREIFT ############ 

"""


def Substitution__new__(typ, *args, **kwargs):
	return GSSubstitution.alloc().init()
GSSubstitution.__new__ = Substitution__new__;

def Substitution__init__(self):
	pass
GSSubstitution.__init__ = Substitution__init__;


GSSubstitution.source = property(lambda self: self.valueForKey_("back"), 
								 lambda self, value: self.setBack_(value))
GSSubstitution.source = property(lambda self: self.valueForKey_("source"), 
								 lambda self, value: self.setSource_(value))
GSSubstitution.forward = property(lambda self: self.valueForKey_("fwd"), 
								 lambda self, value: self.setFwd_(value))

GSSubstitution.target = property(lambda self: self.valueForKey_("target"), 
								 lambda self, value: self.setTarget_(value))
GSSubstitution.languageTag = property(lambda self: self.valueForKey_("languageTag"), 
								 lambda self, value: self.setLanguageTag_(value))
GSSubstitution.scriptTag = property(lambda self: self.valueForKey_("scriptTag"), 
								 lambda self, value: self.setScriptTag_(value))











##################################################################################
#
#
#
#           GSGlyph
#
#
#
##################################################################################

'''


:mod:`GSGlyph`
===============================================================================

Implementation of the glyph object.

For details on how to access these glyphs, please see :class:`GSFont`.glyphs

.. class:: GSGlyph([name])

	:param name: The glyph name
	
Properties
	
.. autosummary::

	parent
	layers
	name
	unicode
	string
	id
	category
	subCategory
	script
	glyphInfo
	leftKerningGroup
	rightKerningGroup
	leftMetricsKey
	rightMetricsKey
	export
	color
	colorObject
	note
	selected
	mastersCompatible
	
	
Functions

.. autosummary::

	beginUndo()
	endUndo()
	updateGlyphInfo()

----------
Properties
----------
	
'''


def Glyph__new__(typ, *args, **kwargs):
	return GSGlyph.alloc().init()
GSGlyph.__new__ = Glyph__new__;

def Glyph__init__(self, name=None):
	if name and (isinstance(name, str) or isinstance(name, unicode)):
		self.setName_(name)
GSGlyph.__init__ = Glyph__init__;

def Glyph__repr__(self):
	return "<GSGlyph \"%s\" with %s layers>" % (self.name, len(self.layers))
GSGlyph.__repr__ = Glyph__repr__;

GSGlyph.parent = property(			lambda self: self.valueForKey_("parent"),
									lambda self, value: self.setParent_(value)) 
'''.. attribute:: parent
	Reference to the :class:`GSFont` object.

	:type: :class:`GSFont <GSFont>`
'''
GSGlyph.layers = property(			lambda self: GlyphLayerProxy(self))

'''.. attribute:: layers
	The layers of the glyph, collection of :class:`GSLayer` objects. You can access them either by index or by layer ID, which can be a :attr:`GSFontMaster.id <id>`.
	The layer IDs are usually a unique string chosen by Glyphs.app and not set manually. They may look like this: 3B85FBE0-2D2B-4203-8F3D-7112D42D745E

	:type: list, dict

	.. code-block:: python

		# get active layer
		layer = font.selectedLayers[0]
		
		# get glyph of this layer
		glyph = layer.parent
		
		# access all layers of this glyph
		for layer in glyph.layers:
			print layer.name
			
		# access layer of currently selected master of active glyph ...
		# (also use this to access a specific layer of glyphs selected in the Font View)
		layer = glyph.layers[font.selectedFontMaster.id]
		
		# ... which is exactly the same as:
		layer = font.selectedLayers[0]
	
		# directly access 'Bold' layer of active glyph
		for master in font.masters:
			if master.name == 'Bold':
				id = master.id
				break
		layer = glyph.layers[id]

		# add a new layer
		newLayer = GSLayer()
		newLayer.name = '{125, 100}' # (example for glyph-level intermediate master)
		# you may set the master ID that this layer will be associated with, otherwise the first master will be used
		newLayer.associatedMasterId = font.masters[-1].id # attach to last master
		font.glyphs['a'].layers.append(newLayer)

		# duplicate a layer under a different name
		newLayer = font.glyphs['a'].layers[0].copy()
		newLayer.name = 'Copy of layer'
		# FYI, this will still be the old layer ID (in case of duplicating) at this point
		print newLayer.layerId
		font.glyphs['a'].layers.append(newLayer)
		# FYI, the layer will have been assigned a new layer ID by now, after having been appended
		print newLayer.layerId

		# replace the second master layer with another layer
		newLayer = GSLayer()
		newLayer.layerId = font.masters[1].id # Make sure to sync the master layer ID
		font.glyphs['a'].layers[font.masters[1].id] = newLayer
		
		# delete last layer of glyph
		# (Also works for master layers. They will be emptied)
		del(font.glyphs['a'].layers[-1])

		# delete currently active layer
		del(font.glyphs['a'].layers[font.selectedLayers[0].layerId])
		
'''
GSGlyph.name = property(			lambda self: self.pyobjc_instanceMethods.name(),
									lambda self, value: self.setName_(value))
'''.. attribute:: name
	The name of the glyph. It will be converted to a "nice name" (afii10017 to A-cy) (you can disable this behavior in font info or the app preference)
	:type: unicode
'''

GSGlyph.unicode = property(			lambda self: self.pyobjc_instanceMethods.unicode() )
'''.. attribute:: unicode
	String with the hex Unicode value of glyph, if encoded.
	Read only.
	:type: unicode
'''

def _get_Glyphs_String(self):
	if self.unicode:
		return unichr(int(self.unicode, 16))

GSGlyph.string =		  property( lambda self: _get_Glyphs_String(self))

'''.. attribute:: string
	String representation of glyph, if encoded.
	This is similar to the string representation that you get when copying glyphs into the clipboard.
	:type: unicode
'''
GSGlyph.id = property(				lambda self: str(self.valueForKey_("id")),
									lambda self, value: self.setId_(value))
'''.. attribute:: id
	An unique identifier for each glyph
	:type: unicode'''
GSGlyph.category = property(		lambda self: self.valueForKey_("category"))
'''.. attribute:: category
	The category of the glyph. e.g. 'Letter', 'Symbol'
	:type: unicode
'''
GSGlyph.subCategory = property(		lambda self: self.valueForKey_("subCategory"))
'''.. attribute:: subCategory
	The subCategory of the glyph. e.g. 'Uppercase', 'Math'
	:type: unicode
'''
GSGlyph.script = property(			lambda self: self.valueForKey_("script"))
'''.. attribute:: script
	The script of the glyph, e.g. 'latin', 'arabic'.
	:type: unicode
'''

GSGlyph.glyphInfo = property(lambda self: GSGlyphsInfo.glyphInfoForGlyph_(self))
'''.. attribute:: glyphInfo
	:class:`GSGlyphInfo` object for this glyph with detailed information.
	:type: :class:`GSGlyphInfo`
'''

def __GSGlyph_glyphDataEntryString__(self):
	Unicode = self.unicode
	if Unicode == None or len(Unicode) < 3:
		Unicode = ""
	Decompose = self.layers[0].componentNamesText()
	if Decompose != None and len(Decompose) > 0:
		Decompose = "decompose=\"%s\" " % Decompose
		
	SubCategory = ""
	if self.subCategory != "Other":
		SubCategory = "subCategory=\"%s\" " % self.subCategory
	Anchors = self.layers[0].anchors.keys()
	if len(Anchors) > 0:
		Anchors = "anchors=\"%s\" " % ", ".join(Anchors)
	else:
		Anchors = ""
	GlyphInfo = self.glyphInfo
	Accents = GlyphInfo.accents
	if Accents != None and len(Accents) > 0:
		Accents = "accents=\"%s\"" % ", ".join(Accents)
	else:
		Accents = ""
	Production = Glyphs.productionGlyphName(self.name)
	if len(Production) > 0:
		Production = "production=\"%s\"" % Production
	return "	<glyph unicode=\"%s\" name=\"%s\" %scategory=\"%s\" %sscript=\"%s\" description=\"\" %s%s />" % (Unicode, self.name, Decompose, self.category, SubCategory, self.script, Anchors, Accents)

GSGlyph.glyphDataEntryString = __GSGlyph_glyphDataEntryString__

GSGlyph.leftKerningGroup = property(lambda self: self.valueForKey_("leftKerningGroup"), 
									lambda self, value: self.setLeftKerningGroup_(value))
'''.. attribute:: leftKerningGroup
	The leftKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.
	:type: unicode'''
GSGlyph.rightKerningGroup = property(lambda self: self.valueForKey_("rightKerningGroup"), 
									lambda self, value: self.setRightKerningGroup_(value))
'''.. attribute:: rightKerningGroup
	The rightKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.
	:type: unicode'''
GSGlyph.leftMetricsKey =  property(	lambda self: self.valueForKey_("leftMetricsKey"), 
									lambda self, value: self.setLeftMetricsKey_(value))
'''.. attribute:: leftMetricsKey
	The leftMetricsKey of the glyph. This is a reference to another glyph by name. It is used to synchronize the metrics with the linked glyph.
	:type: unicode'''
GSGlyph.rightMetricsKey = property(	lambda self: self.valueForKey_("rightMetricsKey"), 
									lambda self, value: self.setRightMetricsKey_(value))
'''.. attribute:: rightMetricsKey
	The rightMetricsKey of the glyph. This is a reference to another glyph by name. It is used to synchronize the metrics with the linked glyph.
	:type: unicode'''
GSGlyph.export =		  property( lambda self: self.valueForKey_("export").boolValue(), 
									lambda self, value: self.setExport_(value))

'''.. attribute:: export
	Defines whether glyph will export upon font generation
	:type: bool'''

GSGlyph.color =			  property( lambda self: self.valueForKey_("colorIndex"), 
									lambda self, value: self.setColorIndex_(value))
'''.. attribute:: color
	Color marking of glyph in UI
	:type: int

	.. code-block:: python

		glyph.color = 0		# red
		glyph.color = 1		# orange
		glyph.color = 2		# brown
		glyph.color = 3		# yellow
		glyph.color = 4		# light green
		glyph.color = 5		# dark green
		glyph.color = 6		# light blue
		glyph.color = 7		# dark blue
		glyph.color = 8		# purple
		glyph.color = 9		# magenta
		glyph.color = 10	# light gray
		glyph.color = 11	# charcoal
		glyph.color = 9223372036854775807	# not colored, white
'''

GSGlyph.colorObject =			  property( lambda self: self.valueForKey_("color") )
'''.. attribute:: colorObject
	NSColor object of glyph color, useful for drawing in plugins.
	:type: NSColor

	.. code-block:: python

		# Set Color
		glyph.colorObject.set()
		
		# Get RGB (and alpha) values (as float numbers 0..1, multiply with 256 if necessary)
		R, G, B, A = glyph.colorObject.colorUsingColorSpace_(NSColorSpace.genericRGBColorSpace()).getRed_green_blue_alpha_(None, None, None, None)

		print R, G, B
		0.617805719376 0.958198726177 0.309286683798

		print roun(R * 256), int(G * 256), int(B * 256)
		158 245 245
		
		# Draw layer
		glyph.layers[0].bezierPath.fill()
		

'''


GSGlyph.note =			  property( lambda self: self.valueForKey_("note"), 
									lambda self, value: self.setNote_(value))
'''.. attribute:: note
	:type: unicode'''


def _get_Glyphs_is_selected(self):
	Doc = self.parent.parent
	return Doc.windowController().glyphsController().selectedObjects().containsObject_(self)

def _set_Glyphs_is_selected(self, isSelected):
	ArrayController = self.parent.parent.windowController().glyphsController()
	if isSelected:
		ArrayController.addSelectedObjects_([self])
	else:
		ArrayController.removeSelectedObjects_([self])

GSGlyph.selected =		property( lambda self: _get_Glyphs_is_selected(self),
								  lambda self, value: _set_Glyphs_is_selected(self, value))
'''.. attribute:: selected
	Return True if the Glyph is selected in the Font View. 
	This is different to the property font.selectedLayers which returns the selection from the active tab.
	:type: bool

	.. code-block:: python

		# access all selected glyphs in the Font View
		for glyph in font.glyphs:
			if glyph.selected:
				print glyph
'''

GSGlyph.mastersCompatible = property( lambda self: bool(self.pyobjc_instanceMethods.mastersCompatible()))

'''.. attribute:: mastersCompatible
	Return True when all layers in this glyph are compatible (same components, anchors, paths etc.)
	:type: bool

'''



'''

---------
Functions
---------

'''



def __BeginUndo(self):
	self.undoManager().beginUndoGrouping()

GSGlyph.beginUndo = __BeginUndo

'''

.. function:: beginUndo()
	
	Call this before you do a longer running change to the glyph. Be extra careful to call Glyph.endUndo() when you are finished.
'''

def __EndUndo(self):
	self.undoManager().endUndoGrouping()
GSGlyph.endUndo = __EndUndo

'''.. function:: endUndo()
	
	This closes a undo group that was opened by a previous call of Glyph.beginUndo(). Make sure that you call this for each beginUndo() call.
'''

def __updateGlyphInfo(self, changeName = True):
	GSGlyphsInfo.updateGlyphInfo_changeName_(self, True)
GSGlyph.updateGlyphInfo = __updateGlyphInfo

'''.. function:: updateGlyphInfo(changeName = True)
	
	Updates all information like name, unicode etc. for this glyph.
'''







##################################################################################
#
#
#
#           GSLayer
#
#
#
##################################################################################


'''

:mod:`GSLayer`
===============================================================================

Implementation of the layer object.

For details on how to access these layers, please see :class:`GSGlyph`.layers

.. class:: GSLayer()

Properties

.. autosummary::
	
	parent
	name
	associatedMasterId
	layerId
	components
	guides
	annotations
	hints
	anchors
	paths
	selection
	LSB
	RSB
	TSB
	BSB
	width
	bounds
	selectionBounds
	background
	backgroundImage
	bezierPath

Functions

.. autosummary::
	
	decomposeComponents()
	compareString()
	connectAllOpenPaths()
	copyDecomposedLayer()
	syncMetrics()
	correctPathDirection()
	removeOverlap()
	roundCoordinates()
	addNodesAtExtremes()
	beginChanges()
	endChanges()
	cutBetweenPoints()
	intersectionsBetweenPoints()
	addMissingAnchors()
	clearSelection()
	clearBackground()
	swapForegroundWithBackground()

----------
Properties
----------

	
	'''

def Layer__new__(typ, *args, **kwargs):
	return GSLayer.alloc().init()
GSLayer.__new__ = Layer__new__;

def Layer__init__(self):
	pass
GSLayer.__init__ = Layer__init__;

def Layer__repr__(self):
	try:
		assert self.name
		name = self.name
	except:
		name = 'orphan'
	try:
		assert self.parent.name
		parent = self.parent.name
	except:
		parent = 'orphan'
	return "<%s \"%s\" (%s)>" % (self.className(), name, parent)
GSLayer.__repr__ = Layer__repr__;

GSLayer.parent = property(			lambda self: self.valueForKey_("parent"),
									lambda self, value: self.setParent_(value))
GSBackgroundLayer.parent = property(lambda self: self.valueForKey_("parent"),
									lambda self, value: self.setParent_(value))
'''.. attribute:: parent
	Reference to the :class:`Glyph <GSGlyph>` object that this layer is attached to.
	:type: :class:`GSGlyph <GSGlyph>`
'''

GSLayer.name = property(			lambda self: self.valueForKey_("name"),
									lambda self, value: self.setName_(value)) 
'''.. attribute:: name
	Name of layer
	:type: unicode'''

GSLayer.associatedMasterId = property(lambda self: self.valueForKey_("associatedMasterId"),
									lambda self, value: self.setAssociatedMasterId_(value)) 
'''.. attribute:: associatedMasterId
	The ID of the :class:`FontMaster <GSFontMaster>` this layer belongs to, in case this isn't a master layer. Every layer that isn't a master layer needs to be attached to one master layer.
	:type: unicode

	.. code-block:: python

		# add a new layer
		newLayer = GSLayer()
		newLayer.name = '{125, 100}' # (example for glyph-level intermediate master)
		# you may set the master ID that this layer will be associated with, otherwise the first master will be used
		newLayer.associatedMasterId = font.masters[-1].id # attach to last master
		font.glyphs['a'].layers.append(newLayer)

'''
GSLayer.layerId = property(lambda self: self.valueForKey_("layerId"),
									  lambda self, value: self.setLayerId_(value)) 
'''.. attribute:: layerId
	The unique layer ID is used to access the layer in the :class:`glyphs <GSGlyph>` layer dictionary.
	
	For master layers this should be the id of the :class:`FontMaster <GSFontMaster>`.
	It could look like this: "FBCA074D-FCF3-427E-A700-7E318A949AE5"
	:type: unicode

	.. code-block:: python

		# see ID of active layer
		id = font.selectedLayers[0].layerId
		print id
		FBCA074D-FCF3-427E-A700-7E318A949AE5
		
		# access a layer by this ID
		layer = font.glyphs['a'].layers[id]
		layer = font.glyphs['a'].layers['FBCA074D-FCF3-427E-A700-7E318A949AE5']
		
		# for master layers, use ID of masters
		layer = font.glyphs['a'].layers[font.masters[0].id]

'''


GSLayer.components = property(lambda self: LayerComponentsProxy(self),
							  lambda self, value: self.setComponents_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: components
	Collection of :class:`GSComponent` objects
	:type: list

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# add component
		layer.components.append(GSComponent('dieresis'))

		# add component at specific position
		layer.components.append(GSComponent('dieresis', NSPoint(100, 100)))

		# delete specific component
		for i, component in enumerate(layer.components):
		        if component.componentName == 'dieresis':
		                del(layer.components[i])
		                break
'''

GSLayer.guideLines = property(lambda self: LayerGuideLinesProxy(self),
							  lambda self, value: self.setGuideLines_(NSMutableArray.arrayWithArray_(value)))

GSLayer.guides = property(lambda self: LayerGuideLinesProxy(self),
							  lambda self, value: self.setGuideLines_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: guides
	List of :class:`GSGuideLine` objects.
	:type: list

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# access all guides
		for guide in layer.guides:
			print guide

		# add guideline
		newGuide = GSGuideLine()
		newGuide.position = NSPoint(100, 100)
		newGuide.angle = -10.0
		layer.guides.append(newGuide)

		# delete guide
		del(layer.guides[0])
'''

GSLayer.annotations = property(lambda self: LayerAnnotationProxy(self),
							   lambda self, value: self.setAnnotations_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: annotations
	List of :class:`GSAnnotation` objects.
	:type: list

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# access all annotations
		for annotation in layer.annotations:
			print annotation

		# add new annotation
		newAnnotation = GSAnnotation()
		newAnnotation.type = TEXT
		newAnnotation.text = 'Fuck, this curve is ugly!'
		layer.annotations.append(newAnnotation)

		# delete annotation
		del(layer.annotations[0])
'''


GSLayer.hints = property(lambda self: LayerHintsProxy(self),
						 lambda self, value: self.setHints_(value))
'''.. attribute:: hints
	List of :class:`GSHint` objects.
	:type: list

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# access all hints
		for hint in layer.hints:
			print hint

		## todo: add hint

		# delete hint
		del(layer.hint[0])
'''

GSLayer.anchors = property(lambda self: LayerAnchorsProxy(self))
'''.. attribute:: anchors
	List of :class:`GSAnchor` objects.
	:type: list, dict

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# access all anchors:
		for a in layer.anchors:
			print a

		# add a new anchor
		layer.anchors['top'] = GSAnchor()

		# delete anchor
		del(layer.anchors['top'])
'''

GSLayer.paths = property(	lambda self: LayerPathsProxy(self),
						 lambda self, value: self.setPaths_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: paths
	List of :class:`GSPath <GSPath>` objects.
	:type: list

	.. code-block:: python

		# access all paths
		for path in layer.paths:
			print path

		# delete path
		del(layer.paths[0])
'''

GSLayer.selection = property(	lambda self: LayerSelectionProxy(self))

'''.. attribute:: selection
	List of all selected objects in the glyph. Read only.
	
	This list contains **all selected items**, including **nodes**, **anchors**, **guidelines** etc.
	If you want to work specifically with nodes, for instance, you may want to cycle through the nodes (or anchors etc.) and check whether they are selected. See example below.

	.. code-block:: python

		# access all selected nodes
		for path in layer.paths:
			for node in path.nodes: # (or path.anchors etc.)
				print node.selected

		# clear selection
		layer.clearSelection()
	
	:type: list
'''

GSLayer.LSB = property(		lambda self: self.valueForKey_("LSB").floatValue(),
							lambda self, value: self.setLSB_(float(value)))
'''.. attribute:: LSB
	Left sidebearing
	:type: float
'''

GSLayer.RSB = property(		lambda self: self.valueForKey_("RSB").floatValue(),
							lambda self, value: self.setRSB_(float(value)))
'''.. attribute:: RSB
	Right sidebearing
	:type: float'''

GSLayer.TSB = property(		lambda self: self.valueForKey_("TSB").floatValue(),
							lambda self, value: self.setTSB_(float(value)))
'''.. attribute:: TSB
	Top sidebearing
	:type: float'''

GSLayer.BSB = property(		lambda self: self.valueForKey_("BSB").floatValue(),
							lambda self, value: self.setBSB_(float(value)))
'''.. attribute:: BSB
	Bottom sidebearing
	:type: float'''

GSLayer.width = property(	lambda self: self.valueForKey_("width").floatValue(),
							lambda self, value: self.setWidth_(float(value)))
'''.. attribute:: width
	Glyph width
	:type: float'''

GSLayer.bounds = property(	lambda self: self.pyobjc_instanceMethods.bounds() )

'''.. attribute:: bounds
	Bounding box of whole glyph as NSRect. Read-only.
	:type: NSRect
	
	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# origin
		print layer.bounds.origin.x, layer.bounds.origin.y

		# size
		print layer.bounds.size.width, layer.bounds.size.height
'''

GSLayer.selectionBounds = property(	lambda self: self.boundsOfSelection() )

'''.. attribute:: selectionBounds
	Bounding box of the layer's selection (nodes, anchors, components etc). Read-only.
	:type: NSRect
'''

GSLayer.background = property(lambda self: self.pyobjc_instanceMethods.background())

'''.. attribute:: background
	The background layer
	:type: :class:`GSLayer <GSLayer>`

'''

GSLayer.backgroundImage = property(lambda self: self.pyobjc_instanceMethods.backgroundImage(),
									lambda self, value: self.pyobjc_instanceMethods.setBackgroundImage_(value))

'''.. attribute:: backgroundImage
	The background image. It will be scaled so that 1 em unit equals 1 of the image's pixels.
	:type: :class:`GSBackgroundImage`

	.. code-block:: python

		# set background image
		layer.backgroundImage = GSBackgroundImage('/path/to/file.jpg')

		# remove background image
		layer.backgroundImage = None
'''

GSLayer.bezierPath = property(	 lambda self: self.pyobjc_instanceMethods.bezierPath() )
'''.. attribute:: bezierPath
	
	The layer as an NSBezierPath object. Useful for drawing glyphs in plugins.

	.. code-block:: python
	
		# draw the path into the edit view
		NSColor.redColor().set()
		layer.bezierPath.fill()

	:type: NSBezierPath
'''


'''
---------
Functions
---------

.. function:: decomposeComponents()
	
	Decomposes all components of the layer at once.

.. function:: compareString()
	
	Returns a string representing the outline structure of the glyph, for compatibility comparison.

	:return: The comparison string

	:rtype: string

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		print layer.compareString()
		oocoocoocoocooc_oocoocoocloocoocoocoocoocoocoocoocooc_

.. function:: connectAllOpenPaths()
	
	Closes all open paths when end points are further than 1 unit away from each other.


.. function:: copyDecomposedLayer()
	
	Returns a copy of the layer with all components decomposed.

	:return: A new layer object

	:rtype: :class:`GSLayer <GSLayer>`

.. function:: syncMetrics()
	
	Take over LSB and RSB from linked glyph.

	.. code-block:: python

		# sync metrics of all layers of this glyph
		for layer in glyph.layers:
			layer.syncMetrics()

.. function:: correctPathDirection()
	
	Corrects the path direction.
'''

def RemoveOverlap(self):
	removeOverlapFilter = NSClassFromString("GlyphsFilterRemoveOverlap").alloc().init()
	removeOverlapFilter.runFilterWithLayer_error_(self, None)
GSLayer.removeOverlap = RemoveOverlap

'''
.. function:: removeOverlap()
	
	Joins all contours.
'''

'''
.. function:: roundCoordinates()
	
	Round the positions of all coordinates to the grid (size of which is set in the Font Info).
'''

def Layer_addNodesAtExtremes(self, force = False):
	self.addExtremePoints()

GSLayer.addNodesAtExtremes = Layer_addNodesAtExtremes

'''
.. function:: addNodesAtExtremes()
	
	Add nodes at layer's extrema, e.g. top, bottom etc.
'''





def BeginChanges(self):
	self.setDisableUpdates()
	self.undoManager().beginUndoGrouping()
GSLayer.beginChanges = BeginChanges


'''
.. function:: beginChanges()

	Call this before you do bigger changes to the Layer.
	This will increase performance and prevent undo problems.
	Always call layer.endChanges() if you are finished.
'''

def EndChanges(self):
	self.setEnableUpdates()
	self.undoManager().endUndoGrouping()
GSLayer.endChanges = EndChanges


'''
.. function:: endChanges()

	Call this if you have called layer.beginChanges before. Make sure to group bot calls properly.
'''

def CutBetweenPoints(self, Point1, Point2):
	GlyphsToolOther = NSClassFromString("GlyphsToolOther")
	GlyphsToolOther.cutPathsInLayer_forPoint_endPoint_(self, Point1, Point2)
GSLayer.cutBetweenPoints = CutBetweenPoints


'''	
.. function:: cutBetweenPoints(Point1, Point2)

	Cuts all paths that intersect the line from Point1 to Point2
	
	:param Point1: one point
	:param Point2: the other point

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# cut glyph in half horizontally at y=100
		layer.cutBetweenPoints(NSPoint(0, 100), NSPoint(layer.width, 100))
'''

def IntersectionsBetweenPoints(self, Point1, Point2):
	return self.calculateIntersectionsStartPoint_endPoint_(Point1, Point2)
GSLayer.intersectionsBetweenPoints = IntersectionsBetweenPoints

NSConcreteValue.x = property(lambda self: self.pointValue().x )
NSConcreteValue.y = property(lambda self: self.pointValue().y )

'''
.. function:: intersectionsBetweenPoints(Point1, Point2)

	Return all intersection points between a measurement line and the paths in the layer. This is basically identical to the measurement tool in the UI.
	
	Normally, the first returned point is the starting point, the last returned point is the end point. Thus, the second point is the first intersection, the second last point is the last intersection.
	
	
	:param Point1: one point
	:param Point2: the other point

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# show all intersections with glyph at y=100
		intersections = layer.intersectionsBetweenPoints((-1000, 100), (layer.width+1000, 100))
		print intersections
		
		# left sidebearing at measurement line
		print intersections[1].x

		# right sidebearing at measurement line
		print layer.width - intersections[-2].x
'''

def Layer_addMissingAnchors(self):
	GSGlyphsInfo.updateAnchor_(self)
GSLayer.addMissingAnchors = Layer_addMissingAnchors


'''
.. function:: addMissingAnchors()

	Adds missing anchors defined in the glyph database.
'''


'''
.. function:: clearSelection()

	Unselect all selected items in this layer.
'''

'''
.. function:: clearBackground()

	Remove all paths from background layer.
'''

GSLayer.swapForegroundWithBackground = property(lambda self: self.swapForgroundWithBackground() )

'''
.. function:: swapForegroundWithBackground()

	Swap Foreground layer with Background layer.
'''


def ControlLayer__new__(typ, *args, **kwargs):
	if len(args) > 0:
		return GSControlLayer.alloc().initWithChar_(args[0])
	else:
		return GSControlLayer.alloc().init()
GSControlLayer.__new__ = ControlLayer__new__;

def ControlLayer__init__(self, args):
	pass
GSControlLayer.__init__ = ControlLayer__init__;

def ControlLayer__repr__(self):
	char = self.parent().unicodeChar()
	if char == 10:
		name = "newline"
	elif char == 129:
		name = "placeholder"
	else:
		name = GSGlyphsInfo.niceGlyphNameForName_("uni%.4X" % self.parent().unicodeChar())
	return "<%s \"%s\">" % (self.className(), name)
GSControlLayer.__repr__ = ControlLayer__repr__;

def ControlLayer__newline__():
	return GSControlLayer(10)
GSControlLayer.newline = staticmethod(ControlLayer__newline__);

def ControlLayer__placeholder__():
	return GSControlLayer(129)
GSControlLayer.placeholder = staticmethod(ControlLayer__placeholder__);



def DrawLayerWithPen(self, pen):
	"""draw the object with a RoboFab segment pen"""
	try:
		pen.setWidth(self.width)
		if self.note is not None:
			pen.setNote(self.note)
	except AttributeError:
		# FontTools pens don't have these methods
		pass
	for a in self.anchors:
		a.draw(pen)
	for c in self.paths:
		c.draw(pen)
	for c in self.components:
		c.draw(pen)
	try:
		pen.doneDrawing()
	except AttributeError:
		# FontTools pens don't have a doneDrawing() method
		pass

GSLayer.draw = DrawLayerWithPen

def DrawPointsWithPen(self, pen):
	"""draw the object with a point pen"""
	for a in self.anchors:
		a.drawPoints(pen)
	for c in self.paths:
		c.drawPoints(pen)
	for c in self.components:
		c.drawPoints(pen)

GSLayer.drawPoints = DrawPointsWithPen

def _Clear_(self, contours=True, components=True, anchors=True, guides=True):
	"""Clear all items marked as True from the glyph"""
	if contours:
		self.setPaths_(NSMutableArray.array())
	# if components:
	# 	self.clearComponents()
	# if anchors:
	# 	self.clearAnchors()
	# if guides:
	# 	self.clearHGuides()
	# 	self.clearVGuides()

GSLayer.clear = _Clear_

def _getPen_(self):
	return GSPathPen.alloc().init()

GSLayer.getPen = _getPen_

def _getPointPen_(self):
	#print "Get GSPoint Pen"
	if "GSPen" in sys.modules.keys():
		del(sys.modules["GSPen"])
	from GSPen import GSPointPen
	
	return GSPointPen(self, self)

GSLayer.getPointPen = _getPointPen_

def _invalidateContours_(self):
	pass

GSLayer._invalidateContours = _invalidateContours_







##################################################################################
#
#
#
#           GSAnchor
#
#
#
##################################################################################

'''

:mod:`GSAnchor`
===============================================================================

Implementation of the anchor object.

For details on how to access them, please see :class:`GSLayer`.anchors

.. class:: GSAnchor([name, pt])

	:param name: the name of the anchor
	:param pt: the position of the anchor

Properties

.. autosummary::
	
	position
	name
	selected
	

----------
Properties
----------

'''


def Anchor__new__(typ, *args, **kwargs):
	return GSAnchor.alloc().init()
GSAnchor.__new__ = Anchor__new__;

def Anchor__init__(self, name = None, pt = None):
	if pt:
		self.setPosition_(pt)
	if name:
		self.setName_(name)
GSAnchor.__init__ = Anchor__init__;

def Anchor__repr__(self):
	return "<GSAnchor \"%s\" x=%s y=%s>" % (self.name, self.position.x, self.position.y)
GSAnchor.__repr__ = Anchor__repr__;

GSAnchor.position = property(	lambda self: self.valueForKey_("position").pointValue(),
								lambda self, value: self.setPosition_(value))
'''.. attribute:: position
	The position of the anchor
	:type: NSPoint
	
	.. code-block:: python
	
		# read position
		print layer.anchors['top'].position.x, layer.anchors['top'].position.y

		# set position
		layer.anchors['top'].position = NSPoint(175, 575)

		# increase vertical position by 50 units
		layer.anchors['top'].position = NSPoint(layer.anchors['top'].position.x, layer.anchors['top'].position.y + 50)

'''

GSAnchor.name = property(		lambda self: self.valueForKey_("name"),
								lambda self, value: self.setName_(value))
'''.. attribute:: name
	The name of the anchor
	:type: unicode'''

'''.. attribute:: selected
	Selection state of anchor in UI.

	.. code-block:: python
	
		# select anchor
		layer.anchors[0].selected = True

		# print selection state
		print layer.anchors[0].selected

	:type: bool
'''

def DrawAnchorWithPen(self, pen):
	pen.moveTo(self.position)
	pen.endPath()

GSAnchor.draw = DrawAnchorWithPen




##################################################################################
#
#
#
#           GSComponent
#
#
#
##################################################################################


'''

:mod:`GSComponent`
===============================================================================

Implementation of the component object.
For details on how to access them, please see :class:`GSLayer`.components

.. class:: GSComponent(glyph [, position])
	
	:param glyph: a :class:`GSGlyph` object or the glyph name
	:param position: the position of the component as NSPoint

Properties

.. autosummary::
	
	position
	componentName
	component
	transform
	bounds
	disableAlignment
	anchor
	selected
	
Functions

.. autosummary::
	
	decompose

	
----------
Properties
----------

	'''

def Component__new__(typ, *args, **kwargs):
	return GSComponent.alloc().init()
GSComponent.__new__ = Component__new__;

def Component__init__(self, glyph, offset=(0,0), scale=(1,1), transform=None):
	"""
	transformation: transform matrix as list of numbers
	"""
	if transform is None:
		xx, yy = scale
		dx, dy = offset
		self.transform = (xx, 0, 0, yy, dx, dy)
	else:
		self.transform = transform
		
	if glyph:
		if isinstance(glyph, (str, unicode)):
			self.setComponentName_(glyph)
		elif isinstance(glyph, GSGlyph):
			self.setComponentName_(glyph.name)
		elif isinstance(glyph, "RGlyph"):
			self.setComponentName_(glyph.name)

GSComponent.__init__ = Component__init__;

def Component__repr__(self):
	return "<GSComponent \"%s\" x=%s y=%s>" % (self.componentName, self.position.x, self.position.y)
GSComponent.__repr__ = Component__repr__;

GSComponent.position = property(	lambda self: self.valueForKey_("position").pointValue(),
									lambda self, value: self.setPosition_(value))
'''.. attribute:: position
	The Position of the component.
	:type: NSPoint'''

GSComponent.componentName = property(lambda self: self.valueForKey_("componentName"),
									lambda self, value: self.setComponentName_(value))
'''.. attribute:: componentName
	The glyph name the component is pointing to.
	:type: unicode'''

GSComponent.component = property(	lambda self: self.valueForKey_("component"))
'''.. attribute:: component
	The :class:`GSGlyph` the component is pointing to. This is read only. In order to change the referenced base glyph, set :class:`GSComponent`.componentName to the new glyph name.
	:type: :class:`GSGlyph`
'''

GSComponent.transform = property(	lambda self: self.transformStruct(),
									lambda self, value: self.setTransformStruct_(value))
'''.. attribute:: transform
	
	returns a six number tuple that contrains a transformation matrix: (1, 0, 0, 1, 0, 0) (m11, m12, m21, m22, tX, tY)
	
	:type: NSAffineTransformStruct'''

GSComponent.transformation = property(	lambda self: self.transformStruct(),
									  lambda self, value: self.setTransformStruct_(value))

GSComponent.bounds = property(		lambda self: self.pyobjc_instanceMethods.bounds() )
'''.. attribute:: bounds
	
	Bounding box of the component, read only
	
	:type: NSRect
	
	.. code-block:: python

		component = layer.components[0] # first component

		# origin
		print component.bounds.origin.x, component.bounds.origin.y

		# size
		print component.bounds.size.width, component.bounds.size.height
'''

# keep for compatibility:
GSComponent.disableAlignment = property(lambda self: bool(self.pyobjc_instanceMethods.disableAlignment()),
									lambda self, value: self.setDisableAlignment_(value))
# new:
GSComponent.automaticAlignment = property(lambda self: bool(self.pyobjc_instanceMethods.disableAlignment()),
									lambda self, value: self.setDisableAlignment_(value))
'''.. attribute:: disableAlignment
	
	Defines whether the component is automatically aligned.
	
	:type: bool'''

GSComponent.anchor = property(lambda self: self.pyobjc_instanceMethods.anchor(),
							  lambda self, value: self.setAnchor_(value))
'''.. attribute:: anchor
	
	If more than one anchor/_anchor pair would match, this property can be used to set the anchor to use for automatic alignment
	
	This can be set from the anchor button in the component info box in the UI
	
	:type: unicode'''



'''.. attribute:: selected
	Selection state of component in UI.

	.. code-block:: python
	
		# select component
		layer.components[0].selected = True

		# print selection state
		print layer.components[0].selected

	:type: bool
'''

def DrawComponentWithPen(self, pen):
	pen.addComponent(self.componentName, self.transform)

GSComponent.draw = DrawComponentWithPen



'''


----------
Functions
----------

'''

'''.. function:: decompose()
	
	Decomposes the component.
'''






##################################################################################
#
#
#
#           GSPath
#
#
#
##################################################################################


'''

:mod:`GSPath`
===============================================================================

Implementation of the path object.

For details on how to access them, please see :class:`GSLayer`.paths

If you build a path in code, make sure that the structure is valid. A curve node has to be preceded by two off-curve nodes. And an open path has to start with a line node.

.. class:: GSPath()

Properties

.. autosummary::
	
	parent
	nodes
	segments
	closed
	direction
	bounds
	selected
	bezierPath
	
Functions

.. autosummary::
	
	reverse()
	addNodesAtExtremes()

----------
Properties
----------

	
'''


def Path__new__(typ, *args, **kwargs):
	return GSPath.alloc().init()
GSPath.__new__ = Path__new__;

def Path__init__(self):
	pass
GSPath.__init__ = Path__init__;

def Path__repr__(self):
	return "<GSPath %s nodes and %s segments>" % (len(self.nodes), len(self.segments))
GSPath.__repr__ = Path__repr__;

GSPath.parent = property(		lambda self: self.valueForKey_("parent"),
								lambda self, value: self.setParent_(value)) 
'''.. attribute:: parent
	Reference to the :class:`Layer <GSLayer>` object.

	:type: :class:`GSLayer <GSLayer>`
'''

GSPath.nodes = property(		lambda self: PathNodesProxy(self),
								lambda self, value: self.setNodes_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: nodes
	A list of :class:`GSNode <GSNode>` objects
	:type: list
	
	.. code-block:: python

		# access all nodes
		for path in layer.paths:
			for node in path.nodes:
				print node

	'''
	
GSPath.segments = property(		lambda self: self.valueForKey_("segments"),
						 		lambda self, value: self.setSegments_(value))
'''.. attribute:: segments
	A list of segments as NSPoint objects. Two objects represent a line, four represent a curve. Start point of the segment is included.
	:type: list

	.. code-block:: python

		# access all segments
		for path in layer.paths:
			for segment in path.segments:
				print segment
'''

GSPath.closed = property(		lambda self: self.valueForKey_("closed").boolValue(),
						 		lambda self, value: self.setValue_forKey_(value, "closed"))
'''.. attribute:: closed
	Returns True if the the path is closed
	:type: bool'''

GSPath.direction = property(		lambda self: self.valueForKey_("direction"))
'''.. attribute:: direction
	Path direction. -1 for counter clockwise, 1 for clockwise.
	:type: int'''

GSPath.bounds = property(	 lambda self: self.pyobjc_instanceMethods.bounds() )
'''.. attribute:: bounds
	Bounding box of the path, read only
	:type: NSRect

	.. code-block:: python

		path = layer.paths[0] # first path

		# origin
		print path.bounds.origin.x, path.bounds.origin.y

		# size
		print path.bounds.size.width, path.bounds.size.height
	'''

def Path_selected(self):
	return Set(self.nodes) <= Set(self.parent.selection)

def Path_SetSelected(self, state):
	for node in self.nodes:
		node.selected = state


GSPath.selected = property(	 lambda self: Path_selected(self), lambda self, value: Path_SetSelected(self, value) )
'''.. attribute:: selected
	Selection state of path in UI.

	.. code-block:: python
	
		# select path
		layer.paths[0].selected = True

		# print selection state
		print layer.paths[0].selected

	:type: bool
'''


GSPath.bezierPath = property(	 lambda self: self.pyobjc_instanceMethods.bezierPath() )
'''.. attribute:: bezierPath
	
	The same path as an NSBezierPath object. Useful for drawing glyphs in plugins.

	.. code-block:: python
	
		# draw the path into the edit view
		NSColor.redColor().set()
		layer.paths[0].bezierPath.fill()

	:type: NSBezierPath
'''


'''


----------
Functions
----------

.. function:: reverse()
	
	Reverses the path direction
'''

def DrawPathWithPen(self, pen):
	"""draw the object with a fontTools pen"""
	
	Start = 0
	if self.closed:
		for i in range(len(self)-1, -1, -1):
			StartNode = self.nodeAtIndex_(i)
			if StartNode.type is not GSOFFCURVE:
				pen.moveTo(StartNode.position)
				break
	else:
		for i in range(len(self)):
			StartNode = self.nodeAtIndex_(i)
			if StartNode.type is not GSOFFCURVE:
				pen.moveTo(StartNode.position)
				Start = i + 1
				break
	for i in range(Start, len(self), 1):
		Node = self.nodeAtIndex_(i)
		if Node.type == GSLINE:
			pen.lineTo(Node.position)
		elif Node.type == GSCURVE:
			pen.curveTo(self.nodeAtIndex_(i-2).position, self.nodeAtIndex_(i-1).position, Node.position)
	if self.closed:
		pen.closePath()
	else:
		pen.endPath()
	return

GSPath.draw = DrawPathWithPen


def Path_addNodesAtExtremes(self, force = False):
	self.addExtremes_(force)

GSPath.addNodesAtExtremes = Path_addNodesAtExtremes

'''
.. function:: addNodesAtExtremes()
	
	Add nodes at path's extrema, e.g. top, bottom etc.
'''





##################################################################################
#
#
#
#           GSNode
#
#
#
##################################################################################

'''

:mod:`GSNode`
===============================================================================

Implementation of the node object.

For details on how to access them, please see :class:`GSPath`.nodes


.. class:: GSNode([pt, type])
	
	:param pt: The position of the node.
	:param type: The type of the node, GSLINE, GSCURVE or GSOFFCURVE

Properties

.. autosummary::
	
	position
	type
	connection
	selected

Functions

.. autosummary::
	
	makeNodeFirst()
	toggleConnection()


----------
Properties
----------

	'''



def Node__new__(typ, *args, **kwargs):
	return GSNode.alloc().init()
GSNode.__new__ = Node__new__;

def Node__init__(self, pt = None, type = None):
	if pt:
		self.setPosition_(pt)
	if type:
		self.setType_(type)
GSNode.__init__ = Node__init__;

def Node__repr__(self):
	NodeType = nodeConstants[self.type]
	if self.type != GSOFFCURVE:
		NodeType += " " + nodeConstants[self.connection]
	return "<GSNode x=%s y=%s %s>" % (self.position.x, self.position.y, NodeType)
GSNode.__repr__ = Node__repr__;

GSNode.position = property(			lambda self: self.valueForKey_("position").pointValue(),
								lambda self, value: self.setPosition_(value))
'''.. attribute:: position
	The position of the node.
	:type: NSPoint'''

GSNode.type = property(			lambda self: self.valueForKey_("type"),
								lambda self, value: self.setType_(value))
'''.. attribute:: type
	The type of the node, GSLINE, GSCURVE or GSOFFCURVE
	:type: int'''
GSNode.connection = property(	lambda self: self.valueForKey_("connection"),
								lambda self, value: self.setConnection_(value))
'''.. attribute:: connection
	The type of the connection, GSSHARP or GSSMOOTH
	:type: int
'''

GSNode.layer = property(		lambda self: self.parent.parent)


'''.. attribute:: selected
	Selection state of node in UI.

	.. code-block:: python
	
		# select node
		layer.paths[0].nodes[0].selected = True

		# print selection state
		print layer.paths[0].nodes[0].selected

	:type: bool
'''

def __GSNode__index__(self):
	try:
		return self.parent.indexOfNode_(self)
	except:
		return NSNotFound

GSNode.index = property(	lambda self: __GSNode__index__(self))
'''.. attribute:: index
	Returns the index of the node in the containing path or maxint if it is not in a path.
	:type: int
	'''
def __GSNode__nextNode__(self):
	try:
		index = self.parent.indexOfNode_(self)
		if index < len(self.parent.nodes):
			return self.parent.nodes[index + 1]
	except:
		pass
	return None

GSNode.nextNode = property(	lambda self: __GSNode__nextNode__(self))
'''.. attribute:: nextNode
	Returns the next node in the path or None
	:type: GSNode
	'''

def __GSNode__prevNode__(self):
	try:
		index = self.parent.indexOfNode_(self)
		if index < len(self.parent.nodes):
			return self.parent.nodes[index - 1]
	except:
		pass
	return None

GSNode.prevNode = property(	lambda self: __GSNode__prevNode__(self))
'''.. attribute:: prevNode
	Returns the previous node in the path
	:type: GSNode
	'''


'''	

---------
Functions
---------


.. function:: makeNodeFirst()
	
	Set this node to be the start point of the path

.. function:: toggleConnection()
	
	Toggle between sharp or smooth connections

'''










##################################################################################
#
#
#
#           GSGuideLine
#
#
#
##################################################################################


'''

:mod:`GSGuideLine`
===============================================================================

Implementation of the guide line object.

For details on how to access them, please see :class:`GSLayer`.guides


.. class:: GSGuideLine()

----------
Properties
----------

.. autosummary::
	
	position
	angle
	name
	selected


	'''


def GuideLine__new__(typ, *args, **kwargs):
	return GSGuideLine.alloc().init()
GSGuideLine.__new__ = GuideLine__new__;

def GuideLine__init__(self):
	pass
GSGuideLine.__init__ = GuideLine__init__;

def GuideLine__repr__(self):
	return "<GSGuideLine x=%s y=%s angle=%s>" % (self.position.x, self.position.y, self.angle)
GSGuideLine.__repr__ = GuideLine__repr__;

GSGuideLine.position = property(lambda self: self.valueForKey_("position").pointValue(),
								lambda self, value: self.setPosition_(value))
'''.. attribute:: position
	The position of the node.
	:type: NSPoint'''
GSGuideLine.angle = property(	lambda self: self.valueForKey_("angle").floatValue(),
								lambda self, value: self.setAngle_(float(value)))
'''.. attribute:: angle
	Angle
	:type: float'''
GSGuideLine.name = property(	lambda self: self.valueForKey_("name"),
								lambda self, value: self.setName_(value))
'''.. attribute:: name
	a optional name
	:type: unicode'''

'''.. attribute:: selected
	Selection state of guideline in UI.

	.. code-block:: python
	
		# select guideline
		layer.guidelines[0].selected = True

		# print selection state
		print layer.guidelines[0].selected

	:type: bool
'''


##################################################################################
#
#
#
#           GSAnnotation
#
#
#
##################################################################################


'''

:mod:`GSAnnotation`
===============================================================================

Implementation of the annotation object.

For details on how to access them, please see :class:`GSLayer`.annotations


.. class:: GSAnnotation()

Properties

.. autosummary::
	
	position
	type
	text
	angle
	width

----------
Properties
----------
	
	'''

def Annotation__new__(typ, *args, **kwargs):
	return GSAnnotation.alloc().init()
GSAnnotation.__new__ = Annotation__new__;

def Annotation__init__(self):
	pass
GSAnnotation.__init__ = Annotation__init__;

def Annotation__repr__(self):
	TypeName = "n/a"
	if (self.type == TEXT):
		TypeName = "Text"
	elif (self.type == ARROW):
		TypeName = "Arrow"
	elif (self.type == CIRCLE):
		TypeName = "Circle"
	elif (self.type == PLUS):
		TypeName = "Plus"
	elif (self.type == MINUS):
		TypeName = "Minus"
	return "<%s %s x=%s y=%s>" % (self.className(), TypeName, self.position.x, self.position.y)
GSAnnotation.__repr__ = Annotation__repr__;


GSAnnotation.position = property(lambda self: self.valueForKey_("position").pointValue(),
								 lambda self, value: self.setPosition_(value))
'''.. attribute:: position
	The position of the annotation.
	:type: NSPoint'''

GSAnnotation.type = property(lambda self: self.valueForKey_("type").integerValue(),
								 lambda self, value: self.setType_(value))
'''.. attribute:: type
	The type of the annotation.
	
	Available constants are:
	TEXT
	ARROW
	CIRCLE
	PLUS
	MINUS

	:type: int'''
	
GSAnnotation.text = property(lambda self: self.valueForKey_("text"),
								 lambda self, value: self.setText_(value))
'''.. attribute:: text
	The content of the annotation. Only useful if type == TEXT
	:type: unicode'''
	
GSAnnotation.angle = property(lambda self: self.valueForKey_("angle").floatValue(),
								 lambda self, value: self.setAngle_(value))
'''.. attribute:: angle
	The angle of the annotation.
	:type: float'''

GSAnnotation.width = property(lambda self: self.valueForKey_("width").floatValue(),
								 lambda self, value: self.setWidth_(value))
'''.. attribute:: width
	The width of the annotation.
	:type: float'''




##################################################################################
#
#
#
#           GSHint
#
#
#
##################################################################################


'''

:mod:`GSHint`
===============================================================================

Implementation of the hint object.

For details on how to access them, please see :class:`GSLayer`.hints

.. class:: GSHint()

Properties

.. autosummary::
	
	originNode
	targetNode
	otherNode1
	otherNode2
	type
	horizontal
	selected

----------
Properties
----------

	'''


def Hint__new__(typ, *args, **kwargs):
	return GSHint.alloc().init()
GSHint.__new__ = Hint__new__;

def Hint__init__(self):
	pass
GSHint.__init__ = Hint__init__;

def Hint__repr__(self):
	if self.horizontal:
		direction = "horizontal"
	else:
		direction = "vertical"
	if self.type == BOTTOMGHOST or self.type == TOPGHOST:
		return "<GSHint %s origin=(%s,%s) type=%s>" % (hintConstants[self.type], self.originNode.position.x, self.originNode.position.y, self.type)
	elif self.type == STEM:
		return "<GSHint Stem origin=(%s,%s) target=(%s,%s) %s>" % (self.originNode.position.x, self.originNode.position.y, self.targetNode.position.x, self.targetNode.position.y, direction)
	else:
		return "<GSHint %s %s>" % (hintConstants[self.type], direction)
GSHint.__repr__ = Hint__repr__;

GSHint.originNode = property(	lambda self: self.valueForKey_("originNode"),
								lambda self, value: self.setOriginNode_(value))
'''.. attribute:: originNode
	The the first node this hint is attached to.
	
	:type: :class:`GSNode <GSNode>`
'''
GSHint.targetNode = property(	lambda self: self.valueForKey_("targetNode"),
								lambda self, value: self.setTargetNode_(value))
'''.. attribute:: targetNode
	The the second node this hint is attached to. In case of a ghost hint this value will be empty.
	
	:type: :class:`GSNode`
'''

GSHint.otherNode1 = property(	lambda self: self.valueForKey_("otherNode1"),
								lambda self, value: self.setOtherNode1_(value))
'''.. attribute:: otherNode1
	A third node this hint is attached to. Used for Interpolation or Diagonal hints.
	
	:type: :class:`GSNode`'''
	
GSHint.otherNode2 = property(	lambda self: self.valueForKey_("otherNode1"),
								lambda self, value: self.setOtherNode1_(value))
'''.. attribute:: otherNode2
	A forth node this hint is attached to. Used for Diagonal hints.

	:type: :class:`GSNode`'''

GSHint.type = property(			lambda self: self.valueForKey_("type"),
								lambda self, value: self.setType_(value))
'''.. attribute:: type
	See Constants section at the bottom of the page
	:type: int'''
	
GSHint.horizontal = property(	lambda self: self.valueForKey_("horizontal").boolValue(),
								lambda self, value: self.setHorizontal_(value))
'''.. attribute:: horizontal
	True if hint is horizontal, False if vertical.
	:type: bool'''

'''.. attribute:: selected
	Selection state of hint in UI.

	.. code-block:: python
	
		# select hint
		layer.hints[0].selected = True

		# print selection state
		print layer.hints[0].selected

	:type: bool
'''



##################################################################################
#
#
#
#           GSBackgroundImage
#
#
#
##################################################################################


'''

:mod:`GSBackgroundImage`
===============================================================================

Implementation of background image.

For details on how to access it, please see :class:`GSLayer`.backgroundImage

.. class:: GSBackgroundImage([path])

	:param path: Initialize with an image file (optional)

Properties

.. autosummary::
	
	path
	image
	crop
	locked
	position
	scale
	transform
	
Functions

.. autosummary::

	resetCrop
	scaleWidthToEmUnits
	scaleHeightToEmUnits

----------
Properties
----------

	'''


def BackgroundImage__new__(typ, *args, **kwargs):
	return GSBackgroundImage.alloc().init()
GSBackgroundImage.__new__ = BackgroundImage__new__;

def BackgroundImage__init__(self, path = None):
	if path:
		self.setImagePath_(path)
		self.loadImage()
GSBackgroundImage.__init__ = BackgroundImage__init__;

def BackgroundImage__repr__(self):
	return "<GSBackgroundImage '%s'>" % self.imagePath()
GSBackgroundImage.__repr__ = BackgroundImage__repr__;

def BackgroundImage_setPath(self, path):
	self.setImagePath_(path)
	self.loadImage()

GSBackgroundImage.path = property(	lambda self: self.pyobjc_instanceMethods.imagePath(),
						lambda self, value: BackgroundImage_setPath(self, value))

'''.. attribute:: path
	Path of image file
	:type: unicode
'''

GSBackgroundImage.image = property(	lambda self: self.pyobjc_instanceMethods.image() )

'''.. attribute:: image
	
	:class:`NSImage <NSImage>` object of background image, read only (as in: not settable)
	
	:type: :class:`NSImage <NSImage>`
'''

GSBackgroundImage.crop = property(	lambda self: self.pyobjc_instanceMethods.crop(),
							lambda self, value: self.setCrop_(value)) 
'''.. attribute:: crop
	
	Crop rectangle. This is relative to the image's size in pixels, not the font's em units (just in case the image is scaled to something other than 100%).
	
	:type: :class:`NSRect`

	.. code-block:: python

		# change cropping
		layer.backgroundImage.crop = NSRect(NSPoint(0, 0), NSPoint(1200, 1200))
'''

GSBackgroundImage.locked = property(		lambda self: bool(self.pyobjc_instanceMethods.locked()),
						 		lambda self, value: self.setLocked_(value))
'''.. attribute:: locked
	
	Defines whether image is locked for access in UI.
	
	:type: bool
'''

def BackgroundImage_getPosition(self):
	return NSPoint(self.transform[4], self.transform[5])
def BackgroundImage_setPosition(self, pos):
	self.transform = (self.transform[0], self.transform[1], self.transform[2], self.transform[3], pos.x, pos.y)

GSBackgroundImage.position = property(		lambda self: BackgroundImage_getPosition(self),
						 		lambda self, value: BackgroundImage_setPosition(self, value))

'''.. attribute:: position
	
	Position of image in font's em units.
	
	:type: :class:`NSPoint`

	.. code-block:: python

		# change position
		layer.backgroundImage.position = NSPoint(50, 50)
'''

def BackgroundImage_getScale(self):
	return self.transform[0]
def BackgroundImage_setScale(self, scale):
	self.transform = (float(scale), self.transform[1], self.transform[2], float(scale), self.transform[4], self.transform[5])

GSBackgroundImage.scale = property(		lambda self: BackgroundImage_getScale(self),
						 		lambda self, value: BackgroundImage_setScale(self, value))

'''.. attribute:: scale
	
	Scale factor of image.
	
	A scale factor of 1.0 (100%) means that 1 em unit equals 1 of the image's pixels.
	
	This sets the scale factor for x and y scale simultaneously. For separate scale factors, please use the transormation matrix.
	
	:type: float
'''


GSBackgroundImage.transform = property(		lambda self: self.pyobjc_instanceMethods.transformStruct(),
						 		lambda self, value: self.setTransformStruct_(value))
'''.. attribute:: transform
	
	Transformation matrix.
	
	:type: :class:`NSAffineTransformStruct`

	.. code-block:: python

		# change transformation
		layer.backgroundImage.transform = (
			1.0, # x scale factor
			0.0, # x skew factor
			0.0, # y skew factor
			1.0, # y scale factor
			0.0, # x position
			0.0  # y position
			)


----------
Functions
----------


'''

def BackgroundImage_resetCrop(self):
	self.crop = NSRect(NSPoint(0, 0), self.image.size())
GSBackgroundImage.resetCrop = BackgroundImage_resetCrop


'''.. function:: resetCrop
	
	Resets the cropping to the image's original dimensions.
'''

def BackgroundImage_scaleWidthToEmUnits(self, value):
	self.scale = float(value) / float(self.crop.size.width)
GSBackgroundImage.scaleWidthToEmUnits = BackgroundImage_scaleWidthToEmUnits

'''.. function:: scaleWidthToEmUnits
	
	Scale the image's cropped width to a certain em unit value, retaining its aspect ratio.

	.. code-block:: python

		# fit image in layer's width
		layer.backgroundImage.scaleWidthToEmUnits(layer.width)
		

'''

def BackgroundImage_scaleHeightToEmUnits(self, value):
	self.scale = float(value) / float(self.crop.size.height)
GSBackgroundImage.scaleHeightToEmUnits = BackgroundImage_scaleHeightToEmUnits

'''.. function:: scaleHeightToEmUnits
	
	Scale the image's cropped height to a certain em unit value, retaining its aspect ratio.

	.. code-block:: python

		# position image's origin at descender line
		layer.backgroundImage.position = NSPoint(0, font.masters[0].descender)

		# scale image to UPM value
		layer.backgroundImage.scaleHeightToEmUnits(font.upm)
'''



##################################################################################
#
#
#
#           GSEditViewController
#
#
#
##################################################################################

'''

:mod:`GSEditViewController`
===============================================================================

Implementation of the GSEditViewController object, which represents edit tabs in the UI.

For details on how to access them, please look at :class:`GSFont`.tabs


.. class:: GSEditViewController()

Properties

.. autosummary::

	text
	layers
	scale


----------
Properties
----------

'''

GSEditViewController.text = property(lambda self: self.graphicView().displayString(),
									 lambda self, value: self.graphicView().setDisplayString_(value))
'''

.. attribute:: text
	The text of the tab, either as text or glyph names with / , or mixed.
	
	:type: Unicode

'''





def __GSEditViewController__repr__(self):
	nameString = self.text
	if len(nameString) > 30:
		nameString = nameString[:30] + '...'
	nameString = nameString.replace('\n', '\\n')
	import codecs
	return codecs.encode("<GSEditViewController %s>" % nameString, 'ascii', 'backslashreplace')

GSEditViewController.__repr__ = __GSEditViewController__repr__

def __GSEditViewController_layers__(self):
	try:
		return self.parent.windowController().activeEditViewController().graphicView().displayString()
	except:
		pass
	return None
def __GSEditViewController_set_layers__(self, layers):
	if not (type(layers) is list or "objectAtIndex_" in layers.__class__.__dict__):
		raise ValueError
	string = NSMutableAttributedString.alloc().init()
	Font = self.representedObject()
	for l in layers:
		if l.className() == "GSLayer":
			char = Font.characterForGlyph_(l.parent)
			A = NSAttributedString.alloc().initWithString_attributes_(unichr(char), { "GSLayerIdAttrib" : l.associatedMasterId })
		elif l.className() == "GSBackgroundLayer":
			char = Font.characterForGlyph_(l.parent)
			A = NSAttributedString.alloc().initWithString_attributes_(unichr(char), { "GSLayerIdAttrib" : l.associatedMasterId, "GSShowBackgroundAttrib": True })
		elif l.className() == "GSControlLayer":
			char = l.parent().unicodeChar()
			A = NSAttributedString.alloc().initWithString_(unichr(char))
		else:
			raise ValueError
		string.appendAttributedString_(A)
	self.graphicView().textStorage().setText_(string)

GSEditViewController.layers = property(lambda self: self.graphicView().layoutManager().cachedGlyphs(),
							  lambda self, value: __GSEditViewController_set_layers__(self, value))

'''
.. attribute:: layers
	Alternatively, you can set (and read) a list of :class:`GSLayer` objects. These can be any of the layers of a glyph.
	
	

	:type: list

	.. code-block:: python

		
		font.tabs[0].layers = []
		
		# display all layers of one glyph next to each other
		for layer in font.glyphs['a'].layers:
			font.tabs[0].layers.append(layer)
	
'''

GSEditViewController.scale = property(lambda self: self.graphicView().scale())
'''

.. attribute:: scale
	Scale (zoom factor) of the Edit View. Useful for drawing activity in plugins.
	
	The scale changes with every zoom step of the Edit View. So if you want to draw objects (e.g. text, stroke thickness etc.) into the Edit View at a constant size relative to the UI (e.g. constant text size on screen), you need to calculate the object's size relative to the scale factor. See example below.
	
	.. code-block:: python

		print font.currentTab.scale
		0.414628537193

		# Calculate text size
		desiredTextSizeOnScreen = 10 #pt
		scaleCorrectedTextSize = desiredTextSizeOnScreen / font.currentTab.scale
		
		print scaleCorrectedTextSize
		24.1179733255
		

	:type: float

'''






##################################################################################
#
#
#
#           GSGlyphInfo
#
#
#
##################################################################################


def GSGlyphInfo__new__(typ, *args, **kwargs):
	return GSGlyphInfo.alloc().init()
GSGlyphInfo.__new__ = GSGlyphInfo__new__;
def GSGlyphInfo__init__(self):
	pass
GSGlyphInfo.__init__ = GSGlyphInfo__init__;

def GSGlyphInfo__repr__(self):
	return "<GSGlyphInfo '%s'>" % (self.name)
GSGlyphInfo.__repr__ = GSGlyphInfo__repr__;


'''

:mod:`GSGlyphInfo`
===============================================================================

Implementation of the GSGlyphInfo object.

This contains valuable information from the glyph database. See :class:`GSGlyphsInfo` for how to create these objects.

.. class:: GSGlyphInfo()

Properties

.. autosummary::

	name
	productionName
	category
	subCategory
	components
	accents
	anchors
	unicode
	unicode2
	script
	index
	sortName
	sortNameKeep
	desc
	altNames
	desc


----------
Properties
----------


'''

GSGlyphInfo.name = property(lambda self: self.pyobjc_instanceMethods.name())

'''
.. attribute:: name
	Human readable name of glyph ("nice name")
	:type: unicode
'''

GSGlyphInfo.productionName = property(lambda self: self.pyobjc_instanceMethods.production())

'''
.. attribute:: productionName
	Production name of glyph. Will return a value only if production name differs from nice name, otherwise None.
	:type: unicode
'''

GSGlyphInfo.category = property(lambda self: self.pyobjc_instanceMethods.category())

'''
.. attribute:: category
	This is mostly from the UnicodeData.txt file from unicode.org. Some corrections have been made (Accents, ...)
	e.g: "Letter", "Number", "Punctuation", "Mark", "Separator", "Symbol", "Other"
	:type: unicode
'''

GSGlyphInfo.subCategory = property(lambda self: self.pyobjc_instanceMethods.subCategory())

'''
.. attribute:: subCategory
	This is mostly from the UnicodeData.txt file from unicode.org. Some corrections and additions have been made (Smallcaps, ...)
	e.g: "Uppercase", "Lowercase", "Smallcaps", "Ligature", "Decimal Digit", ...
	:type: unicode
'''

GSGlyphInfo.components = property(lambda self: self.pyobjc_instanceMethods.components())

'''
.. attribute:: components
	This glyph may be composed of the glyphs returned as a list of :class:`GSGlyphInfo` objects.
	:type: list
'''

GSGlyphInfo.accents = property(lambda self: self.pyobjc_instanceMethods.accents())

'''
.. attribute:: accents
	This glyph may be combined with these accents, returned as a list of glyph names
	:type: list
'''

GSGlyphInfo.anchors = property(lambda self: self.pyobjc_instanceMethods.anchors())

'''
.. attribute:: anchors
	Anchors defined for this glyph, as a list of anchor names
	:type: list
'''

GSGlyphInfo.unicode = property(lambda self: self.pyobjc_instanceMethods.unicode())

'''
.. attribute:: unicode
	Unicode value of glyph
	:type: list
'''

GSGlyphInfo.script = property(lambda self: self.pyobjc_instanceMethods.script())

'''
.. attribute:: script
	Script of glyph, e.g: "latin", "cyrillic", "greek"
	:type: unicode

'''

GSGlyphInfo.index = property(lambda self: self.pyobjc_instanceMethods.index())

'''
.. attribute:: index
	Index of glyph in database. Used for sorting in UI.
	:type: unicode

'''

GSGlyphInfo.sortName = property(lambda self: self.pyobjc_instanceMethods.sortName())

'''
.. attribute:: sortName
	Alternative name of glyph used for sorting in UI.
	:type: unicode

'''

GSGlyphInfo.sortNameKeep = property(lambda self: self.pyobjc_instanceMethods.sortNameKeep())

'''
.. attribute:: sortNameKeep
	Alternative name of glyph used for sorting in UI, when using 'keep alternate glyphs together'.
	:type: unicode

'''

GSGlyphInfo.desc = property(lambda self: self.pyobjc_instanceMethods.desc())

'''
.. attribute:: desc
	Unicode description of glyph
	:type: unicode

'''

GSGlyphInfo.altNames = property(lambda self: self.pyobjc_instanceMethods.altNames())

'''
.. attribute:: altNames
	Alternative names for glyphs that are not used but should get recognized.
	:type: unicode

'''










'''

Methods
=======

.. autosummary::

	divideCurve()
	distance()
	addPoints()
	subtractPoints()
	GetOpenFile()
	GetSaveFile()
	Message()
	'''


def divideCurve(P0, P1, P2, P3, t):
	#NSPoint Q0, Q1, Q2, R0, R1;
	Q0x = P0[0] + ((P1[0]-P0[0])*t);
	Q0y = P0[1] + ((P1[1]-P0[1])*t);
	Q1x = P1[0] + ((P2[0]-P1[0])*t);
	Q1y = P1[1] + ((P2[1]-P1[1])*t);
	Q2x = P2[0] + ((P3[0]-P2[0])*t);
	Q2y = P2[1] + ((P3[1]-P2[1])*t);
	R0x = Q0x + ((Q1x-Q0x)*t);
	R0y = Q0y + ((Q1y-Q0y)*t);
	R1x = Q1x + ((Q2x-Q1x)*t);
	R1y = Q1y + ((Q2y-Q1y)*t);
	
	#NSPoint S;
	Sx = R0x + ((R1x-R0x)*t);
	Sy = R0y + ((R1y-R0y)*t);
	#	S: neuer Punkt
	#	R0: Anker 2 zu S
	#	Q0: Anker 1 zu S
	#	R1: Anker  zu N2
	#	Q2: Anker  zu N2
	return (P0, NSMakePoint(Q0x, Q0y), NSMakePoint(R0x, R0y), NSMakePoint(Sx, Sy), NSMakePoint(R1x, R1y), NSMakePoint(Q2x, Q2y), P3)
	#*(q2) = R0;
	#*(q3) = S ;
	#*(r1) = R1;
	#*(r2) = Q2;
	#*(r3) = P3;
'''.. function:: divideCurve(P0, P1, P2, P3, t)
	
	Divides the curve using the De Casteljau's algorithm.
	
	:param P0: The Start point of the Curve (NSPoint)
	:param P1: The first off curve point
	:param P2: The second off curve point
	:param P3: The End point of the Curve
	:param t: The time parameter
	:return: A list of points that represent two curves. (Q0, Q1, Q2, Q3, R1, R2, R3). Note that the "middle" point is only returned once.
	:rtype: list'''
	
	
def distance(P1, P2):
	return math.hypot(P1[0] - P2[0], P1[1] - P2[1])
'''.. function:: distance(P0, P1)
	
	calculates the distance between two NSPoints
	
	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The distance
	:rtype: float'''
	
	
def addPoints(P1, P2):
	return NSMakePoint(P1[0] + P2[0], P1[1] + P2[1])
'''.. function:: addPoints(P1, P2)
	
	Add the points.

	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The sum of both points
	:rtype: NSPoint'''
	
	
def subtractPoints(P1, P2):
	return NSMakePoint(P1[0] - P2[0], P1[1] - P2[1])
'''.. function:: subtractPoints(P1, P2)
	
	Subtracts the points.
	
	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The subtracted point
	:rtype: NSPoint'''
	
def scalePoint(P, scalar):
	return NSMakePoint(P[0] * scalar, P[1] * scalar)
'''.. function:: scalePoint(P, scalar)
	
	Scaled a point.

	:param P: a NSPoint
	:param scalar: The Multiplier
	:return: The multiplied point
	:rtype: NSPoint
'''

def GetSaveFile(message=None, ProposedFileName=None, filetypes=None):
	if filetypes is None:
		filetypes = []
	Panel = NSSavePanel.savePanel().retain()
	if message is not None:
		Panel.setTitle_(message)
	Panel.setCanChooseFiles_(True)
	Panel.setCanChooseDirectories_(False)
	Panel.setAllowedFileTypes_(filetypes)
	if ProposedFileName is not None:
		Panel.setNameFieldStringValue_(ProposedFileName)
	pressedButton = Panel.runModalForTypes_(filetypes)
	if pressedButton == NSOKButton:
		return Panel.filename()
	return None

'''.. function:: GetSaveFile(message=None, ProposedFileName=None, filetypes=None)
	
	Opens a file chooser dialog.
	
	:param message:
	:param filetypes:
	:param ProposedFileName:
	:return: The selected file or None
	:rtype: unicode
'''

def __allValues__(self):
	return self.allValues()
MGOrderedDictionary.items = __allValues__

def __Dict_removeObjectForKey__(self, key):
	if isinstance(key, int):
		if key < 0:
			key += len(self)
			if key < 0:
				raise IndexError("list index out of range")
		self.removeObjectAtIndex_(key)
		return
	self.removeObjectForKey_(key)

MGOrderedDictionary.__delitem__ = __Dict_removeObjectForKey__


#This should be possible but the way pyObjc wrapper works does not allow it.
#http://permalink.gmane.org/gmane.comp.python.pyobjc.devel/5493
#def __Dict__objectForKey__(self, key):
#	if isinstance(key, int):
#		if key < 0:
#			key += len(self)
#			if key < 0:
#				raise IndexError("list index out of range")
#		self.objectAtIndex_(key)
#		return
#	self.objectForKey_(key)
#
#MGOrderedDictionary.__getitem__ = __Dict__objectForKey__


def __Dict__iter__(self):
	Values = self.values()
	if Values is not None:
		for element in Values:
			yield element
MGOrderedDictionary.__iter__ = __Dict__iter__
#MGOrderedDictionary.__len__ = property(lambda self: self.count())

def __Dict__del__(self, key):
	self.removeObjectForKey_(key)
MGOrderedDictionary.__delattr__ = __Dict__del__


def GetFile(message=None, allowsMultipleSelection=False, filetypes=None):
	return GetOpenFile(message, allowsMultipleSelection, filetypes)

def GetOpenFile(message=None, allowsMultipleSelection=False, filetypes=None):
	if filetypes is None:
		filetypes = []
	Panel = NSOpenPanel.openPanel().retain()
	Panel.setCanChooseFiles_(True)
	Panel.setCanChooseDirectories_(False)
	Panel.setAllowsMultipleSelection_(allowsMultipleSelection)
	if message is not None:
		Panel.setTitle_(message)
	if filetypes is not None and len(filetypes) > 0:
		Panel.setAllowedFileTypes_(filetypes)
	pressedButton = Panel.runModalForTypes_(filetypes)
	if pressedButton == NSOKButton:
		if allowsMultipleSelection:
			return Panel.filenames()
		else:
			return Panel.filename()
	return None
'''.. function:: GetOpenFile(message=None, allowsMultipleSelection=False, filetypes=None)
	
	Opens a file chooser dialog.
	
	:param message: A message string.
	:param allowsMultipleSelection: Boolean, True if user can select more than one file
	:param filetypes: list of strings indicating the filetypes, e.g. ["gif", "pdf"]
	
	:return: The selected file or a list of file names or None
	:rtype: unicode or list
'''

def GetFolder(message=None, allowsMultipleSelection=False):
	Panel = NSOpenPanel.openPanel().retain()
	Panel.setCanChooseFiles_(False)
	Panel.setCanChooseDirectories_(True)
	Panel.setAllowsMultipleSelection_(allowsMultipleSelection)
	pressedButton = Panel.runModal()
	if pressedButton == NSOKButton:
		if allowsMultipleSelection:
			return Panel.filenames()
		else:
			return Panel.filename()
	return None

'''.. function:: GetFolder(message=None, allowsMultipleSelection = False)
	
	Opens a folder chooser dialog.
	
	:param message:
	:param allowsMultipleSelection:
	:return: The selected folder or None
	:rtype: unicode
'''

def Message(title, message, OKButton=None):
	Glyphs.showAlert_message_OKButton_(title, message, OKButton)

'''.. function:: Message(title, message, OKButton=None)
	
	Shows a alert panel
	
	:param title:
	:param message:
	:param OKButton:
'''

def LogToConsole(message):
	f = sys._getframe(1)
	title = "<>"
	try:
		title = f.f_code.co_name + " (%d)" % f.f_lineno
	except:
		pass
	NSLog("%s: %s" % (title, message))

'''
Constants
=========

Node types

	GSLINE = 1
		Line node.

	GSCURVE = 35
		Curve node. Make sure that each curve node is preceded by two off-curve nodes.

	GSOFFCURVE = 65
		Off-cuve node

Node connection

	GSSHARP = 0
		Sharp connection.

	GSSMOOTH = 100
		A smooth or tangent node

Hint types

	TOPGHOST = -1
		Top ghost for PS hints
	
	STEM = 0
		Stem for PS hints
	
	BOTTOMGHOST = 1
		Bottom ghost for PS hints
	
	TTANCHOR = 2
		Anchor for TT hints

	TTSTEM = 3
		Stem for TT hints
	
	TTALIGN = 4
		Aling for TT hints

	TTINTERPOLATE = 5
		Interpolation for TT hints

	TTDIAGONAL = 6
		Diagonal for TT hints

	CORNER = 16
		Corner Component

	CAP = 17
		Cap Component
	
Hint Option 
	
	This is only used for TrueType hints.
	
	TTROUND = 0
		Round to grid
		
	TTROUNDUP = 1
		Round up
		
	TTROUNDDOWN = 2
		Round down
		
	TTDONTROUND = 4
		Don’t round at all
		
	TRIPLE = 128
		Indicates a triple hint group. There need to be exactly three horizontal TTStem hints with this setting to take effect.
	
'''
