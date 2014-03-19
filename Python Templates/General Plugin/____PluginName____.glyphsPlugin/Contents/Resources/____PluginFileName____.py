#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

GlyphsPluginProtocol = objc.protocolNamed( "GlyphsPlugin" )

class ____PluginClassName____ ( NSObject, GlyphsPluginProtocol ):
	
	def init( self ):
		"""
		You can add an observer like in the example.
		Do all initializing here.
		"""
		try:
			# Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ) )
			selector = objc.selector( self.advertise, signature="v@:@" )
			NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, selector, "GSDocumentWasSavedSuccessfully", objc.nil() )
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )

	def __del__( self ):
		"""
		Remove all observers you added in init().
		"""
		try:
			NSNotificationCenter.defaultCenter().removeObserver_( self )
		except Exception as e:
			self.logToConsole( "__del__: %s" % str(e) )
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )

	def title( self ):
		"""
		The name as it appears in in the app menu.
		"""
		try:
			return "____PluginMenuName____"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def documentWasSaved( self, sender ):
		"""
		Called when the font is saved
		assuming GSDocumentWasSavedSuccessfully was added to the observer
		"""
		try:
			self.logToConsole( "The document: %@ was saved" % sender.object().displayName() )
		except Exception as e:
			self.logToConsole( "documentWasSaved: %s" % str(e) )

	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "%s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
	