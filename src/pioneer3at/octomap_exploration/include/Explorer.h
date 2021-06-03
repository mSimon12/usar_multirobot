#include <pluginlib/class_loader.h>
#include <ros/ros.h>
#include <tf/tf.h>
#include <stdlib.h>

#include <geometry_msgs/Pose.h>
#include <std_msgs/Float64.h>
#include <nav_msgs/Odometry.h>
#include <sensor_msgs/Range.h>
#include <octomap_msgs/conversions.h>
#include <octomap_msgs/Octomap.h>
#include <octomap_msgs/GetOctomap.h>

#include <actionlib/client/simple_action_client.h>
#include <actionlib/client/simple_client_goal_state.h>

#include <octomap/OcTree.h>

#include <move_base_msgs/MoveBaseAction.h>
#include <move_base_msgs/MoveBaseGoal.h>
#include <move_base_msgs/MoveBaseFeedback.h>

#include <octomap_exploration/ExecuteExplorationAction.h>

#include <actionlib/server/simple_action_server.h>

#include <tf/tf.h>
#include <math.h>

#define _USE_MATH_DEFINES
#include <cmath>
#include <queue>
#define XMIN 0.0
#define XMAX 75.0
#define YMIN 0.0
#define YMAX 75.0
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
class Pioneer{
    private:
        ros::NodeHandle nh; 
        actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> approach_client;
        int GRID;
        float cur_XMIN; 
        float cur_XMAX;
        float cur_YMIN; 
        float cur_YMAX; 
    
        bool odom_received,trajectory_received;
        bool isPathValid;
        bool collision;

        // Created by me --------------
        actionlib::SimpleActionServer<octomap_exploration::ExecuteExplorationAction> as_; // NodeHandle instance must be created before this line. Otherwise strange error occurs.
        std::string action_name_;

        // create messages that are used to published feedback/result
        octomap_exploration::ExecuteExplorationFeedback feedback_;
        octomap_exploration::ExecuteExplorationResult result_;

        bool approach_preempted;
        tf::Quaternion myQuaternion;

        // ----------------------------

        geometry_msgs::Pose odometry_information;
        std::vector<geometry_msgs::Pose> trajectory;

        std::vector<geometry_msgs::Pose> invalid_poses;
        std::vector<std::vector<int> > patches;
        std::queue<DistancedPoint> frontiers;
        std::vector<geometry_msgs::Pose> explored;

        ros::Subscriber base_sub;
        // ros::Publisher gui_ack,rate_ack;
        ros::ServiceClient octomap_client;
    
        void poseCallback(const nav_msgs::Odometry::ConstPtr & msg);

        void findFrontier();

        void appFeedCb(const move_base_msgs::MoveBaseFeedbackConstPtr& feedback);
        bool go(geometry_msgs::Pose& target_);
    
    public:
        Pioneer(std::string ns, std::string name);
        // void takeoff();
        void run(const octomap_exploration::ExecuteExplorationGoalConstPtr &goal);
        
};
