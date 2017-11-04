#pragma once
#using <mscorlib.dll>
#using <System.dll>
#include<iostream>
ref class SocketTransfer {
public:
	SocketTransfer(System::Int32 port);
	int startListening();
	int transfer(std::string datai);
private:
	System::Net::Sockets::TcpListener^ server;
	System::Net::Sockets::NetworkStream^ stream;
};