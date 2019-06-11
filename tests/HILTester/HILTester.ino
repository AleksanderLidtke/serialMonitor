/* This Arduino code is supposed to run together with a corresponding
 * SerialMonitor test script. The test script will send a command to the Arduino
 * to execute a given test case (send certain data through the serial port).
 * The test script will then compare the data that if received to the expected
 * results in order to determine whether the test has been successful or not.
 * */

void sendOutOfRange(void)
/* Send three messgages, one of which (0x110000 = 0x10FFFF+1) exceeds Unicode
range in Python 3. */
{
	Serial.write(0x10FFFE); // Unicode range - 1
	Serial.write(0x10FFFF); // Unicode range
	Serial.write(0x110000); // Unicode range + 1

	// Wait for the outgoing buffer to be cleared.
 	Serial.flush();
}

void sendSequences(void)
/* Send various sequences of bytes with 0x00 in different places. Send
each byte one at a time formatted in the raw binary representation. */
{
	// Test data from Python test-script. Various end cases.
	// goodHex=[b'\x80\x81\x82',b'\x80\x00\x82',b'\x80\x82\x00',b'\x00\x80\x82',
	// b'\x80\xA0\x00\x82\xA1',b'\x80\x82\xA1\x00',b'\x00\xA1\x80\x82',
	// b'\x00\xAF\x80\x82',b'\x00\xAF\x00\x00',b'\x00\x00\xAF\x00']

	// Send the data one byte at a time.
 	Serial.write(0x80);Serial.write(0x81);Serial.write(0x82);
 	Serial.write(0x80);Serial.write(0x00);Serial.write(0x82);
 	Serial.write(0x80);Serial.write(0x82);Serial.write(0x00);
	Serial.write(0x00);Serial.write(0x80);Serial.write(0x82);
	Serial.write(0x80);Serial.write(0xA0);Serial.write(0x00);Serial.write(0x82);Serial.write(0xA1);
	Serial.write(0x80);Serial.write(0x82);Serial.write(0xA1);Serial.write(0x00);
	Serial.write(0x00);Serial.write(0xA1);Serial.write(0x80);Serial.write(0x82);
	Serial.write(0x00);Serial.write(0xAF);Serial.write(0x80);Serial.write(0x82);
	Serial.write(0x00);Serial.write(0xAF);Serial.write(0x00);Serial.write(0x00);
	Serial.write(0x00);Serial.write(0x00);Serial.write(0xAF);Serial.write(0x00);

	// Wait for the outgoing buffer to be cleared.
 	Serial.flush();
}

void sendLongs(void)
/* Send two-byte integers from 256 to 65535 inclusive (0x0100 to 0xFFFF). Do it
in steps of 500 to speed up the test w/o loss of generality and end cases. Send
each long one at a time formatted in the raw binary representation. */
{
	long thisByte = 256; // 0x0100, smallest two-byte int.

	while(thisByte<65535) // Go through all ints until 0xFFFFF.
	{
		// Print thisByte unaltered, i.e. the raw binary version of the byte.
		Serial.write(thisByte);
		Serial.flush(); // Wait for the outgoing buffer to be cleared.

		// Go on to the next long but in large steps to speed things up.
		thisByte+=500;
	}
}

void sendNonASCII(void)
/* Send several non-ASCII bytes (128+, 0x80 to 0xFF, i.e. no longer ASCII but
still one byte.). This also covers extended ASCII range and unicode Latin script
codes. Send each byte one at a time formatted in the raw binary representation. */
{
	// Sequence of bytes to be sent during this test case.
	int bytesToSend[] = {128,129,130,138,139,143,159,160,161,200,240,254,255};

	for(int i=0;i<13;i++)
	{
	  // Send this byte unaltered, i.e. the raw binary version of the byte.
	  Serial.write(bytesToSend[i]);
	  Serial.flush(); // Wait for the outgoing buffer to be cleared.
	}
}

void sendASCIITable(void)
/* Send all ASCII characters from 33 to 126 ('!' to '~'), inclusive. Send each
byte one at a time formatted in the raw binary representation. */
{
	// First visible ASCIIcharacter '!' is number 33 but start from 0.
	int thisByte = 0;

	while(thisByte<128) // Go through all characters until 0x7f=128.
						 // Last readable character is '~'=126.
	{
	  // Print thisByte unaltered, i.e. the raw binary version of the byte.
	  Serial.write(thisByte);
	  Serial.flush(); // Wait for the outgoing buffer to be cleared.

	  // Go on to the next character.
	  thisByte++;
	}
}

void sendOne(void)
/* Send '1' ASCII character, followed by a 0x00 and 0 integers. */
{
	Serial.print("1"); // Send ASCII character.
	Serial.write(0x01); // Hex number.
	Serial.write(1); // Decimal number.
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void sendZero(void)
/* Send '0' ASCII character, followed by a 0x00 and 0 integers. */
{
	Serial.print("0"); // Send ASCII character.
	Serial.write(0x00); // Hex number.
	Serial.write(0); // Decimal number.
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void sendA(void)
/* Send 'A' character, followed by a 0x41 and 65 (corresponding ASCII code in hex and decimal). */
{
	Serial.print("A"); // Send ASCII.
	Serial.write(0x41); // Send binary data.
	Serial.write(65); // ASCII code.
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void setup()
/* Setup the Arduino - just open the serial port. */
{
	// Open the serial port @ 9600 baud rate.
	Serial.begin(9600);
}

void loop()
/* Main loop - wait, receive commands to execute a particular test, and delegate
* the said test to a particular function. */
{
	char cmdChar = '0'; // Which test case to execute. 0 - do nothing.
	// Wait until there's something in the serial port to read.
	if (Serial.available() > 0)
	{
		// Read the incoming serial data.
		cmdChar = Serial.read();
		// Execute the chosen test case.
		switch(cmdChar)
		{
			case '0': // Default - do nothing special, use this to make sure that the Arduino is working.
				Serial.print("Arduino reachable."); // Send ASCII characters.
				Serial.flush(); // Wait for the outgoing buffer to be cleared.
				break;
			case 'A': // Simplest test.
				sendA();
				break;
			case 'Z': // Another simple test.
				sendZero();
				break;
			case 'O': // Another simple test.
				sendOne();
				break;
			case 'S': // Send an entire ASICC table.
				sendASCIITable();
				break;
			case 'N': // Send several non-ASICC bytes.
				sendNonASCII();
				break;
			case 'L': // Send two-byte integers.
				sendLongs();
				break;
			case 'Q': // Send sequences of bytes.
				sendSequences();
				break;
			case 'R': // Send one message that exceeds Unicode range (and two others).
				sendOutOfRange();
				break;
		}
	}
}
