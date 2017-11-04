#pragma once
#using <mscorlib.dll>
#using <System.dll>

ref class SocketTransfer {
public:
	SocketTransfer(System::Int32 port);
	int startListening();
	int transfer();
private:
	System::Net::Sockets::TcpListener^ server;
	System::Net::Sockets::NetworkStream^ stream;
};