#include"SocketTransfer.h"

using namespace System;
using namespace System::IO;
using namespace System::Net;
using namespace System::Net::Sockets;
using namespace System::Text;

SocketTransfer::SocketTransfer(Int32 port) {
	IPAddress^ localAddr = IPAddress::Parse("127.0.0.1");

	// TcpListener* server = new TcpListener(port);
	server = gcnew TcpListener(localAddr, port);
}
	
int SocketTransfer::startListening() {
	// Start listening for client requests.
	server->Start();
	String^ data = nullptr;
	// Enter the listening loop.


	Console::Write("Waiting for a connection... ");
	// Perform a blocking call to accept requests.
	// You could also user server.AcceptSocket() here.
	TcpClient^ client = server->AcceptTcpClient();
	Console::WriteLine("Connected!");
	data = nullptr;

	// Get a stream Object* for reading and writing
	stream = client->GetStream();
	
};

int SocketTransfer::transfer() {
	// Buffer for reading data
	array<Byte>^bytes = gcnew array<Byte>(256);
	Int32 i;
	// Loop to receive all the data sent by the client.
	while (i = stream->Read(bytes, 0, bytes->Length))
	{

		// Translate data bytes to a ASCII String*.
		String^ data = Text::Encoding::ASCII->GetString(bytes, 0, i);
		Console::WriteLine("Received: {0}", data);

		// Process the data sent by the client.
		data = data->ToUpper();
		array<Byte>^msg = Text::Encoding::ASCII->GetBytes(data);

		// Send back a response.
		stream->Write(msg, 0, msg->Length);
		Console::WriteLine("Sent: {0}", data);
	}
};