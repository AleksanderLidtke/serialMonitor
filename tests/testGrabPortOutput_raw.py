#!/usr/bin/python3
""" Test the SerialMonitor.grabPortOutput without using actual hardware.
Focus on the raw outputFormat.

.. module:: SerialMonitor
   :platform: Unix, Windows
   :synopsis: Trial automated testing of the message passing through a serial port.

.. moduleauthor:: Alek, Artur

"""
import unittest, time
import SerialMonitor as sm

TEST_PORT = 'loop://' # Type of the test port. This one is a simple RX <-> TX
	# type to be used for unit testing.
	# https://pyserial.readthedocs.io/en/latest/url_handlers.html#loop

class Tests(unittest.TestCase):

	def setUp(self):
		""" Prepare resources for testing. """
		import SerialMonitor as sm
		import time

		# Test port settings. Default and representative of what the SM does.
		self.BaudRate = 9600
		self.currentStopBits = sm.serial.STOPBITS_ONE
		self.currentParity = sm.serial.PARITY_EVEN
		self.currentByteSize = sm.serial.EIGHTBITS

		# Create a port that we'll write test messages into and see if the sm
		# responds correctly.
		self.fixture = sm.serial.serial_for_url(url=TEST_PORT,
												 baudrate=self.BaudRate,
												 timeout=2,
												 stopbits=self.currentStopBits,
												 parity=self.currentParity,
												 bytesize=self.currentByteSize
											 	)

	def tearDown(self):
		""" Done testing, get rid of the test resources."""
		del self.fixture

	def testRawEmptyMessage(self):
		""" Send an empty message with raw outputFormat. """
		notNeeded=self.fixture.read(1) # Empty the port.
		self.assertEqual(self.fixture.read(1),b'',
						msg='Need an empty buffer before running this test case.')
		# port.inWaiting will be 0, so grabPortOutput will just proceed to return
		# the input outputBuffer and the default (empty) output.
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		self.assertEqual(rawOutput[0],'',msg='Expected empty string as output.')
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testRawGoodByte_0(self):
		""" Send a single raw byte with two different representations of '0'. """
		self.fixture.write(b'\x00')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should just get whatever we've put in, but in a raw string representation.
		self.assertEqual(rawOutput[0],'\x00',msg='Expected \\x00.')
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

		self.fixture.write(b'0')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should just get whatever we've put in, but in a raw string representation.
		self.assertEqual(rawOutput[0],'0',msg="Expected '0'.")
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testRawGoodByte_1(self):
		""" Send a single raw byte with two different representations of '1'. """
		self.fixture.write(b'\x01')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should just get whatever we've put in, but in a raw string representation.
		self.assertEqual(rawOutput[0],'\x01',msg='Expected \\x01.')
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

		self.fixture.write(b'1')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should just get whatever we've put in, but in a raw string representation.
		self.assertEqual(rawOutput[0],'1',msg="Expected '1'.")
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testRawGoodByte_0x41(self):
		""" Send a single raw byte with two different representations of
		ASCII 'A' = 0x41. """
		self.fixture.write(b'\x41')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should just get whatever we've put in, but in a raw string representation.
		self.assertEqual(rawOutput[0],'\x41',msg="Expected \\x41 ('A').")
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

		self.fixture.write(b'A')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should just get whatever we've put in, but in a raw string representation.
		self.assertEqual(rawOutput[0],'A',msg="Expected 'A'.")
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testRawGoodByte_fullASCIITable(self):
		""" Send a valid raw message, one valid ASCII byte at a time. Some will
		be sent and read as hex codes of bytes, others as ASCII characters. """
		for i in range(0,128): # From 0x00 to 0x7F.
			# Avoid implicit casting in the serial module - need to send bytes.
			# Easiest to convert int i to ASCII and then to bytes.
			self.fixture.write(bytes(chr(i),'ASCII'))
			time.sleep(0.1) # In case there's a delay (to be expected on Windows).
			hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
			# print(i,hexOutput[0],bytes(chr(i),'ASCII'),chr(i)) # To eyeball the results.
			# Should just get whatever we've put in, but in a string representation.
			self.assertEqual(hexOutput[0],chr(i),msg='Expected {}.'.format(chr(i)))
			# 'raw' option should leave outputBuffer unchanged.
			self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
			# Should have no warnings.
			self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
			# The port should be empty now.
			self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testRawGoodByte_nonASCIIInts(self):
		""" Valid raw message - one integer above the ASCII range at a time.
		Also covers extended ASCII range and unicode Latin script codes. """
		# Below are bytes, expected results of the monitor and their decimal
		# representations up to 255 - getting them programmatically is a bit of
		# a pain, so use https://www.rapidtables.com/convert/number/hex-to-ascii.html
		goodHex=[b'\x80',b'\x81',b'\x82',b'\x8A',b'\x8B',b'\x8F',b'\x9F',b'\xA0',
			b'\xA1',b'\xC8',b'\xF0',b'\xFE',b'\xFF']
		goodAns=['\x80','\x81','\x82','\x8a','\x8b','\x8f','\x9f','\xa0','\xa1',
			'\xc8','\xf0','\xfe','\xff']
		goodDec=[128,129,130,138,139,143,159,160,161,200,240,254,255]
		for i in range(len(goodDec)): # 0x80 to 0xFF, i.e. no longer ASCII but still one byte.
			self.fixture.write(goodHex[i])
			time.sleep(0.1) # In case there's a delay (to be expected on Windows).
			hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
			# print(hexOutput[0],goodAns[i],goodDec[i]) # To eyeball the results.
			# Should just get whatever we've put in, but in a string representation.
			self.assertEqual(hexOutput[0],goodAns[i],msg='Expected {}.'.format(goodAns[i]))
			# 'raw' option should leave outputBuffer unchanged.
			self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
			# Should have no warnings.
			self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
			# The port should be empty now.
			self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	#TODO test is port.inWaiting==0, should return the input outputBuffer - (empty dataStr) DONE
	#TODO test raw output with:
		# 1) valid and invalid ASCII characters,                                            DONE
		# 2) valid unicode characters,                                                      DONE
		# 3) valid and invalid numbers,                                                     DONE
		# 4) empty dataStr, - (port.inWaiting==0)                                           DONE
		# 5) sequences of many bytes with \0x00 in various places,
		# 6) long integers.
		# 7) replacing non-unicode bytes in case of UnicodeDecodeError
	#TODO test formatted output with:
		# 1) valid and invalid ASCII characters,
		# 2) valid and invalid unicode characters,
		# 3) valid and invalid numbers,
		# 4) empty dataStr,
		# 5) valid and invalid formatitng of the dataStr,
		# 5) sequences of many bytes.
	#TODO should try sending various representations of the same bytes to make              DONE
	    # sure they're all understood.
	#TODO add some checks on other inputs - port and outputBuffer
if __name__ == '__main__':
	unittest.main()
