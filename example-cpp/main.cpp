#include <benchbot/benchbot.hpp>
#include <benchbot/grid_map.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    BenchBot benchbot("http://172.17.0.1:8081/");

    GridMap map = benchbot.getGridMap();
    std::cout << map.width() << ", " << map.height() << std::endl;
    std::cout << map.resolution() << std::endl;
    std::cout << map.getFromMetric(0.0f, 0.0f) << std::endl;
    // std::cout << benchbot.get("command") << std::endl;
    // std::cout << benchbot.send("command", "{\"action\": \"forward\"}")["result"] << std::endl;
    return 0;
}