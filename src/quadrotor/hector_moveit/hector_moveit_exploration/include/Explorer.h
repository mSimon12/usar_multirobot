#include <pluginlib/class_loader.h>
#include <ros/ros.h>
#include <tf/tf.h>
#include <stdlib.h>

#include <moveit/robot_model_loader/robot_model_loader.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit/planning_scene/planning_scene.h>

#include <geometry_msgs/Pose.h>
#include <std_msgs/Float64.h>
#include <nav_msgs/Odometry.h>
#include <sensor_msgs/Range.h>
#include <octomap_msgs/conversions.h>

#include <moveit_msgs/DisplayTrajectory.h>
#include <moveit_msgs/GetPlanningScene.h>

#include <actionlib/client/simple_action_client.h>
#include <actionlib/client/simple_client_goal_state.h>
#include <hector_uav_msgs/EnableMotors.h>
#include <hector_moveit_actions/ExecuteDroneTrajectoryAction.h>

#include <octomap/OcTree.h>

#include <actionlib/server/simple_action_server.h>
#include <hector_moveit_exploration/ExecuteDroneExplorationAction.h>
#include <trajectory_action_pkg/ExecuteDroneApproachAction.h>
#include <tf/tf.h>
#include <math.h>

#define _USE_MATH_DEFINES
#include <cmath>
#include <queue>
#define XMIN 0.0
#define XMAX 70.0
#define YMIN 0.0
#define YMAX 70.0
#define ZMIN 0.2
#define ZMAX 30.0

#define EPSILON 1e-4

typedef std::pair<double,geometry_msgs::Pose> DistancedPoint;

class Compare{
    public: 
        bool operator()(DistancedPoint& lhs, DistancedPoint & rhs)
        {
            return lhs.first < rhs.first;
        }
};
typedef std::priority_queue<DistancedPoint,std::vector<DistancedPoint>, Compare> DistancedPointPriorityQueue;

#include <iostream>
#include <chrono>

using namespace std;
using  ns = chrono::nanoseconds;
using get_time = chrono::steady_clock;

#include <omp.h>
#define PATCH_LIMIT 1
class Quadrotor{
    private:
        ros::NodeHandle nh; 
        std::unique_ptr<moveit::planning_interface::MoveGroupInterface> move_group;
        actionlib::SimpleActionClient<trajectory_action_pkg::ExecuteDroneApproachAction> approach_client;
        std::unique_ptr<robot_state::RobotState> start_state;
        std::unique_ptr<planning_scene::PlanningScene> planning_scene;
        double exp_altitude;
        int GRID;
        float cur_XMIN; 
        float cur_XMAX;
        float cur_YMIN; 
        float cur_YMAX; 
    
        bool odom_received,trajectory_received, sonar_received;
        bool isPathValid;
        bool collision;

        // Created by me --------------
        actionlib::SimpleActionServer<hector_moveit_exploration::ExecuteDroneExplorationAction> as_; // NodeHandle instance must be created before this line. Otherwise strange error occurs.
        std::string action_name_;

        // create messages that are used to published feedback/result
        hector_moveit_exploration::ExecuteDroneExplorationFeedback feedback_;
        hector_moveit_exploration::ExecuteDroneExplorationResult result_;

        bool approach_preempted;
        tf::Quaternion myQuaternion;

        // ----------------------------

        geometry_msgs::Pose odometry_information;
        float sonar_information;
        std::vector<geometry_msgs::Pose> trajectory;
        
        std::vector<geometry_msgs::Pose> invalid_poses;
        std::vector<std::vector<int> > patches;
        std::queue<DistancedPoint> frontiers;
        std::vector<geometry_msgs::Pose> explored;

        ros::Subscriber base_sub,plan_sub, sonar_sub;
        ros::Publisher gui_ack,rate_ack;
        ros::ServiceClient motor_enable_service; 
        ros::ServiceClient planning_scene_service;

        moveit_msgs::RobotState plan_start_state;
        moveit_msgs::RobotTrajectory plan_trajectory;
    
        const std::string PLANNING_GROUP = "DroneBody";

        void sonarCallback(const sensor_msgs::Range::ConstPtr & msg);
        void poseCallback(const nav_msgs::Odometry::ConstPtr & msg);

        void findFrontier();

        void appFeedCb(const trajectory_action_pkg::ExecuteDroneApproachFeedbackConstPtr& feedback);
        bool go(geometry_msgs::Pose& target_);
    
    public:
        Quadrotor(std::string ns, std::string name);
        void takeoff();
        void run(const hector_moveit_exploration::ExecuteDroneExplorationGoalConstPtr &goal);
        
};