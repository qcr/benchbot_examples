#include <benchbot/benchbot.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    BenchBot benchbot("http://172.17.0.1:8081/");

    std::cout << benchbot.get() << std::endl;
    
    std::cout << benchbot.get("image") << std::endl;
    std::cout << benchbot.get("command") << std::endl;
    std::cout << benchbot.send("command", "{\"action\": \"forward\"}")["result"] << std::endl;
    return 0;
}