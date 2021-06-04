#include <Explorer.h>

int main(int argc, char** argv)
{
    ros::init(argc, argv, "pioneer3at_explorer");

    // ros::NodeHandle n("~"); 
    std::string ns = ros::this_node::getNamespace();

    Pioneer pioneer(ns.c_str(), "exploration_server");

    ros::spin();
    return 0;
}