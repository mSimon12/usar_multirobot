#include <Explorer.h>


int main(int argc, char** argv)
{
    ros::init(argc, argv, "hector_explorer");
    // ros::AsyncSpinner spinner(1);
    // spinner.start();
    // ros::NodeHandle node_handle("~");
    // Quadrotor quad(std::ref(node_handle));

    // ros::NodeHandle n("~"); 
    std::string ns = ros::this_node::getNamespace();
    // ROS_WARN("\n\nNAmespace: [%s]", ns.c_str());

    Quadrotor quad(ns.c_str(), "assessment_server");

    // quad.takeoff();
    // quad.run();
    ros::spin();
    return 0;
}