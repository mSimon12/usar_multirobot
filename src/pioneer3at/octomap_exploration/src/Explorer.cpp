#include <Explorer.h>

Pioneer::Pioneer(std::string ns, std::string name) : approach_client(ns + "/move_base",true), as_(nh,name, boost::bind(&Pioneer::run, this, _1), false),
    action_name_(name)
{
    approach_client.waitForServer(); 

    odom_received = false;
    trajectory_received = false;
    collision = false;
    nh.getParam(ns + "/grid_size",GRID);

    

    patches.resize(GRID,std::vector<int>(GRID,0));
    base_sub = nh.subscribe<nav_msgs::Odometry>(ns + "/odom",10,&Pioneer::poseCallback,this);

    octomap_client = nh.serviceClient<octomap_msgs::GetOctomap>(ns + "/octomap_full");
    octomap_client.waitForExistence();

    as_.start();    
}

void Pioneer::poseCallback(const nav_msgs::Odometry::ConstPtr & msg)
{
    odometry_information = msg->pose.pose;
    odom_received = true;
}

void Pioneer::findFrontier()
{
    ROS_INFO("Looking for frontiers");
    octomap_msgs::GetOctomap srv;
    ros::spinOnce();
    while(!frontiers.empty())
        frontiers.pop();

    if(octomap_client.call(srv)){
        octomap_msgs::Octomap octomap = srv.response.map;
        octomap::OcTree* current_map = (octomap::OcTree*)octomap_msgs::msgToMap(octomap);
        
        double resolution = current_map->getResolution();
        
        std::vector<std::pair<double, geometry_msgs::Pose> > candidate_frontiers;

        int j = 0;
        bool invalid; 
        for(octomap::OcTree::leaf_iterator n = current_map->begin_leafs(current_map->getTreeDepth()); n != current_map->end_leafs(); ++n)
        {
            if(!current_map->isNodeOccupied(*n))
            {
                double x_cur = n.getX();
                double y_cur = n.getY();
                double z_cur = n.getZ();
                bool frontier = false;

                // cout << "\nPossible frontiers";

                //Reject frontiers out of the desired exploration area
                if((x_cur < (cur_XMIN + resolution)) || (x_cur > (cur_XMAX - resolution))
                || (y_cur < (cur_YMIN + resolution)) || (y_cur > (cur_YMAX - resolution))
                || (z_cur < (ZMIN + resolution)) || (z_cur > (ZMAX - resolution))) continue;

                invalid = false;
                for(int i=0; i<invalid_poses.size(); i++){
                    if(sqrt(pow(invalid_poses[i].position.x - x_cur,2) + pow(invalid_poses[i].position.y - y_cur,2) 
                        + pow(invalid_poses[i].position.z - z_cur,2)) < 0.5){
                        invalid = true;
                        geometry_msgs::Pose p;
                        p.position.x = x_cur;
                        p.position.y = y_cur;
                        p.position.z = z_cur;
                        p.orientation.w = 1;
                        invalid_poses.push_back(p);
                        break;
                    }
                }

                // Reject the frontiers that are located in the patches who had many frontiers already discovered.
                double xspan = XMAX-XMIN;
                double yspan = YMAX-YMIN;
                int xpatch = (x_cur-XMIN)*GRID/xspan;
                int ypatch = (y_cur-YMIN)*GRID/yspan;

                if(invalid || patches[xpatch][ypatch] >= PATCH_LIMIT){
                    continue;
                }

                //Look for frontiers around the current node position
                for (double x_cur_buf = x_cur - resolution; x_cur_buf < x_cur + resolution; x_cur_buf += resolution)
                {   
                    for (double y_cur_buf = y_cur - resolution; y_cur_buf < y_cur + resolution; y_cur_buf += resolution)
                    {
                        octomap::OcTreeNode *n_cur_frontier = current_map->search(x_cur_buf, y_cur_buf, z_cur);
                        if(!n_cur_frontier)
                        {
                            frontier = true;
                        }
                    }
                }
                if(frontier){
                    geometry_msgs::Pose p;
                    p.position.x = x_cur;
                    p.position.y = y_cur;
                    p.position.z = z_cur;
                    p.orientation.w = 1;
                    double dist = sqrt(pow(p.position.x - odometry_information.position.x,2) + pow(p.position.y - odometry_information.position.y,2) + pow(p.position.z - odometry_information.position.z,2));
                    if(dist > 2.0)
                        candidate_frontiers.push_back({dist,p});
                }
            }
            j++;
        }

        //Sort candidate frontiers
        std::sort(candidate_frontiers.begin(),candidate_frontiers.end(), 
            [](const DistancedPoint& x, const DistancedPoint& y){
                return x.first < y.first;
            });

        std::vector<int> indices(candidate_frontiers.size());
        if(candidate_frontiers.size() > 10){
            for(int i=0;i<indices.size();i++)
                indices[i] = i;
            std::random_shuffle(indices.begin(),indices.end());
            indices.erase(indices.begin()+10,indices.end()); 
        }
        int i;
        for(i=0;i<indices.size();i++){
            frontiers.push(candidate_frontiers[i]);
            // cout << "Filtered frontier point " << i << endl;
            // cout << "x: " << candidate_frontiers[i].second.position.x << endl;
            // cout << "y: " << candidate_frontiers[i].second.position.y << endl;
            // cout << "z: " << candidate_frontiers[i].second.position.z << endl;
        }
    }
}

void Pioneer::appFeedCb(const move_base_msgs::MoveBaseFeedbackConstPtr& feedback)
{
    if (as_.isPreemptRequested() || !ros::ok()){         
        approach_client.cancelGoal();
    } 
}

bool Pioneer::go(geometry_msgs::Pose& target_)
{
    move_base_msgs::MoveBaseGoal goal;
    goal.target_pose.header.frame_id = "earth";
    goal.target_pose.pose = target_;
    ros::Rate rate(1);

    approach_preempted = false;
    //Execute the motion in a loop to allow corrections on altitude
    do{
        while(approach_preempted) rate.sleep();

        if (as_.isPreemptRequested() || !ros::ok()) break;

        while(!odom_received)
            rate.sleep();

        odom_received = false;

        float delta_x = target_.position.x - odometry_information.position.x;
        float delta_y = target_.position.y - odometry_information.position.y;
        float yaw = atan(delta_y/delta_x);
        if(delta_y < 0)
            yaw = yaw + atan(1)*4;

        //Set the end yaw of the pioneer
        myQuaternion.setRPY(0,0,yaw);

        goal.target_pose.pose.orientation.x = myQuaternion[0];
        goal.target_pose.pose.orientation.y = myQuaternion[1];
        goal.target_pose.pose.orientation.z = myQuaternion[2];
        goal.target_pose.pose.orientation.w = myQuaternion[3];

        ROS_INFO("Send Next Pose Goal");
        approach_client.sendGoal(goal, actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction>::SimpleDoneCallback(),
                            actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction>::SimpleActiveCallback(),
                            boost::bind(&Pioneer::appFeedCb,this,_1));
        approach_client.waitForResult();
    }while(approach_preempted);

    this->odom_received = false;
    if (approach_client.getState() == actionlib::SimpleClientGoalState::SUCCEEDED){
        return true;
    }
    return false;
}

void Pioneer::run(const octomap_exploration::ExecuteExplorationGoalConstPtr &goal)
{
    double xspan = XMAX-XMIN;
    double yspan = YMAX-YMIN;
    int xpatch, ypatch;

    cout << "\n\nBAZINGA BAZINGA BAZINGA";

    cur_XMIN = goal->x_min;
    cur_XMAX = goal->x_max;
    cur_YMIN = goal->y_min;
    cur_YMAX = goal->y_max;
    ROS_INFO("EXPLORATION LIMITS:\n x_min: %f;\n x_max: %f;\n t_min: %f;\n y_max: %f;",cur_XMIN,cur_XMAX,cur_YMIN,cur_YMAX);

    ros::Rate rate(2);

    //Move the pioneer to the center of the exploration area
    int trials = 0;
    geometry_msgs::Pose pose = odometry_information;

    //Put initial pose as explored point
    explored.push_back(pose);       
    xpatch = (pose.position.x - XMIN)*GRID/xspan;
    ypatch = (pose.position.y - YMIN)*GRID/yspan;
    patches[xpatch][ypatch]++;

    while (odometry_information.position.x < cur_XMIN || odometry_information.position.x > cur_XMAX ||
        odometry_information.position.y < cur_YMIN || odometry_information.position.y > cur_YMAX){

        pose = odometry_information;
        pose.position.x = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/(cur_XMAX - cur_XMIN))) + cur_XMIN; 
        pose.position.y = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/(cur_YMAX - cur_YMIN))) + cur_YMIN; 
        bool move_to_area = go(pose);
        if(move_to_area){
            //Put first pose as explored point
            explored.push_back(pose);       
            xpatch = (pose.position.x - XMIN)*GRID/xspan;
            ypatch = (pose.position.y - YMIN)*GRID/yspan;
            patches[xpatch][ypatch]++;
            break;
        }
        else{
            trials++;
        }
        if (trials >=5){
            as_.setAborted(result_);
            return;
        } 
    }
    
    while(ros::ok()){
        bool success = false;
        findFrontier();

        if (as_.isPreemptRequested() || !ros::ok()){         
                ROS_INFO("%s: Preempted", action_name_.c_str());
                as_.setPreempted();
                break;
        } 

        // Verify if all points of the grid have been explored
        cout << "\nPATCHES:";
        for(int x = 0; x < GRID; x++){
            cout << endl;
            for(int y = 0; y < GRID; y++){
                cout << patches[x][y] << "\t";
            }   
        }

        if(frontiers.empty()){
            bool exp_success = true;
            // Verify if all points of the grid have been explored
            // cout << "FRONTIERS EMPTY";
            for(int x = (cur_XMIN - XMIN)*GRID/xspan; x < (cur_XMAX - XMIN)*GRID/xspan; x++){
                for(int y = (cur_YMIN - YMIN)*GRID/yspan; y < (cur_YMAX - YMIN)*GRID/yspan; y++){
                    // cout << "\nVERIFYING PATCHES";
                    if (patches[x][y] < PATCH_LIMIT){
                        exp_success = false;
                        // cout << "\nEMPTY PATCH";
                        break;
                    }
                }   
            }
            if (exp_success){
                as_.setSucceeded(result_);
                ROS_INFO("Exploration succeded!");
                break;
            }
            else
            {
                as_.setAborted(result_);
                ROS_INFO("Exploration aborted!");
                break;
            }
 
        } 
        geometry_msgs::Pose _goal = frontiers.front().second;
        frontiers.pop();
        explored.push_back(_goal); // Valid or not, make sure that will not be offered as candidate again.
        // bool invalid = false;
        // for(int i=0;i<invalid_poses.size();i++){
            
        //     if(sqrt(pow(invalid_poses[i].position.x - _goal.position.x,2) + pow(invalid_poses[i].position.y - _goal.position.y,2) 
        //         + pow(invalid_poses[i].position.z - _goal.position.z,2)) < 1.0){
        //         invalid = true;
        //         invalid_poses.push_back(_goal);
        //         break;
        //     }
        // }
        // if(invalid) continue;
        
        success = go(_goal);
        if(!success) invalid_poses.push_back(_goal);
        else{
            xpatch = (_goal.position.x - XMIN)*GRID/xspan;
            ypatch = (_goal.position.y - YMIN)*GRID/yspan;
            patches[xpatch][ypatch]++;
        }
        feedback_.current_pose = odometry_information;
        as_.publishFeedback(feedback_);

        ros::spinOnce();
        rate.sleep();
    }
    // as_.setAborted(result_);
}