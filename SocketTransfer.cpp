#include "SocketTransfer.h"

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
	return 1;
};

int SocketTransfer::transfer(String^ data) {
	// Buffer for reading data
	array<Byte>^bytes = gcnew array<Byte>(256);
	Int32 i;
	array<Byte>^msg = Text::Encoding::ASCII->GetBytes(data);

	// Send back a response.
	stream->Write(msg, 0, msg->Length);
	Console::WriteLine("Sent: {0}", data);
	return 1;
};