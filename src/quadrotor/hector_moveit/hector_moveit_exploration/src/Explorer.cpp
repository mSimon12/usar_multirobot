#include <Explorer.h>

Quadrotor::Quadrotor(std::string ns, std::string name) : approach_client(ns + "/approach_server",true), as_(nh,name, boost::bind(&Quadrotor::run, this, _1), false),
    action_name_(name)
{
    approach_client.waitForServer();   
    odom_received = false;
    trajectory_received = false;
    collision = false;
    nh.getParam(ns + "/grid_size",GRID);
    nh.getParam(ns + "/exploration_altitude", exp_altitude);

    patches.resize(GRID,std::vector<int>(GRID,0));
    base_sub = nh.subscribe<nav_msgs::Odometry>(ns + "/ground_truth/state",10,&Quadrotor::poseCallback,this);
    sonar_sub = nh.subscribe<sensor_msgs::Range>(ns + "/sonar_height",10,&Quadrotor::sonarCallback,this);
    // plan_sub = nh.subscribe<moveit_msgs::DisplayTrajectory>(ns + "/move_group/display_planned_path",1,&Quadrotor::planCallback,this);

    gui_ack = nh.advertise<geometry_msgs::Point>(ns + "/orchard_grid_filler",10);
    rate_ack = nh.advertise<std_msgs::Float64>(ns + "/orchard_exploration_rate",1);
    move_group.reset(new moveit::planning_interface::MoveGroupInterface(PLANNING_GROUP));
    robot_model_loader::RobotModelLoader robot_model_loader("robot_description");
    robot_model::RobotModelPtr kmodel = robot_model_loader.getModel();
    
    motor_enable_service = nh.serviceClient<hector_uav_msgs::EnableMotors>(ns + "/enable_motors");
    planning_scene_service = nh.serviceClient<moveit_msgs::GetPlanningScene>(ns + "/get_planning_scene");

    move_group->setPlannerId("RRTConnectkConfigDefault");
    move_group->setNumPlanningAttempts(10);
    move_group->setWorkspace(XMIN,YMIN,ZMIN,XMAX,YMAX,ZMAX);
    
    start_state.reset(new robot_state::RobotState(move_group->getRobotModel()));
    planning_scene.reset(new planning_scene::PlanningScene(kmodel));

    as_.start();    
}

void Quadrotor::poseCallback(const nav_msgs::Odometry::ConstPtr & msg)
{
    odometry_information = msg->pose.pose;
    odom_received = true;
}

void Quadrotor::sonarCallback(const sensor_msgs::Range::ConstPtr & msg)
{
    sonar_information = msg->range;
    sonar_received = true;
}

void Quadrotor::findFrontier()
{
    ROS_INFO("Looking for frontiers");
    moveit_msgs::GetPlanningScene srv;
    srv.request.components.components = moveit_msgs::PlanningSceneComponents::OCTOMAP;
    ros::spinOnce();
    while(!frontiers.empty())
        frontiers.pop();

    if(planning_scene_service.call(srv)){
        this->planning_scene->setPlanningSceneDiffMsg(srv.response.scene);
        octomap_msgs::Octomap octomap = srv.response.scene.world.octomap.octomap;
        octomap::OcTree* current_map = (octomap::OcTree*)octomap_msgs::msgToMap(octomap);
        
        double resolution = current_map->getResolution();
        
        std::vector<std::pair<double, geometry_msgs::Pose> > candidate_frontiers;
        for(octomap::OcTree::leaf_iterator n = current_map->begin_leafs(current_map->getTreeDepth()); n != current_map->end_leafs(); ++n)
        {
            if(!current_map->isNodeOccupied(*n))
            {
                double x_cur = n.getX();
                double y_cur = n.getY();
                double z_cur = n.getZ();
                
                bool frontier = false;

                // Check whether very close point is discovered previously
                bool already_explored = false;
                for(auto a : explored){
                    if((fabs(x_cur - a.position.x) < 8.0) && (fabs(y_cur - a.position.y) < 8.0) && (fabs(z_cur - a.position.z) < 15.0)){
                        already_explored = true;
                        break;
                    }
                }
                //Reject frontiers out of the desired exploration area
                if(x_cur < cur_XMIN + resolution || x_cur > cur_XMAX - resolution
                || y_cur < cur_YMIN + resolution || y_cur > cur_YMAX - resolution
                || z_cur < ZMIN + resolution || z_cur > ZMAX - resolution) continue;

                // Reject the frontiers that are located in the patches who had many frontiers already discovered.
                double xspan = XMAX-XMIN;
                double yspan = YMAX-YMIN;
                int xpatch = (x_cur-XMIN)*GRID/xspan;
                int ypatch = (y_cur-YMIN)*GRID/yspan;
                if(already_explored || patches[xpatch][ypatch]>= PATCH_LIMIT){
                    // if(already_explored) ROS_WARN("NODE ALREADY EXLPORED");
                    // else ROS_WARN("NODE in PATCH LIMIT");
                    continue;
                }
                // ROS_WARN("Possible frontiers");

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
                    // ROS_WARN("FRONTIER!");
                    geometry_msgs::Pose p;
                    p.position.x = x_cur;p.position.y = y_cur;p.position.z = z_cur;
                    p.orientation.w = 1;
                    double dist = sqrt(pow(p.position.x - odometry_information.position.x,2) + pow(p.position.y - odometry_information.position.y,2) + pow(p.position.z - odometry_information.position.z,2));
                    if(dist > 2)
                        candidate_frontiers.push_back({dist,p});
                }
            }
        }

        //Sort candidate frontiers
        std::sort(candidate_frontiers.begin(),candidate_frontiers.end(), 
            [](const DistancedPoint& x, const DistancedPoint& y){
                return x.first > y.first;
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
            // cout << "Frontier point " << i << endl;
            // cout << "x: " << candidate_frontiers[i].second.position.x << endl;
            // cout << "y: " << candidate_frontiers[i].second.position.y << endl;
            // cout << "z: " << candidate_frontiers[i].second.position.z << endl;
        }
    }
}

void Quadrotor::appFeedCb(const trajectory_action_pkg::ExecuteDroneApproachFeedbackConstPtr& feedback)
{
  float h_error = exp_altitude - sonar_information;
  ROS_WARN("Altitude error: %f",h_error);
//   if (abs(h_error) > 0.5){
//       trajectory_action_pkg::ExecuteDroneApproachGoal goal;
//       goal.goal = feedback->current_pose;
//       goal.goal.position.z = odometry_information.position.z + h_error;
      
//       approach_preempted = true;
//       approach_client.cancelAllGoals();

//       //Fix the drone z position
//       approach_client.sendGoal(goal);
//       approach_client.waitForResult();
//       approach_preempted = false;
//   }
}

bool Quadrotor::go(geometry_msgs::Pose& target_)
{
    trajectory_action_pkg::ExecuteDroneApproachGoal goal;
    goal.goal = target_;
    ros::Rate rate(1);

    approach_preempted = false;
    //Execute the motion in a loop to allow corrections on altitude
    do{
        while(approach_preempted) rate.sleep();

        while(!sonar_received)
        rate.sleep();

        while(!odom_received)
            rate.sleep();

        sonar_received = false;
        odom_received = false;

        // Maintain constant distance from the ground
        float h_error = exp_altitude - sonar_information;
        goal.goal.position.z = odometry_information.position.z + h_error;

        float delta_x = target_.position.x - odometry_information.position.x;
        float delta_y = target_.position.y - odometry_information.position.y;
        float yaw = atan(delta_y/delta_x);
        if(delta_y < 0)
            yaw = yaw + atan(1)*4;

        //Set the end yaw of the drone
        myQuaternion.setRPY(0,0,yaw);

        goal.goal.orientation.x = myQuaternion[0];
        goal.goal.orientation.y = myQuaternion[1];
        goal.goal.orientation.z = myQuaternion[2];
        goal.goal.orientation.w = myQuaternion[3];

        ROS_INFO("Send Next Pose Goal");
        approach_client.sendGoal(goal, actionlib::SimpleActionClient<trajectory_action_pkg::ExecuteDroneApproachAction>::SimpleDoneCallback(),
                            actionlib::SimpleActionClient<trajectory_action_pkg::ExecuteDroneApproachAction>::SimpleActiveCallback(),
                            boost::bind(&Quadrotor::appFeedCb,this,_1));
        approach_client.waitForResult();
    }while(approach_preempted);

    this->odom_received = false;
    if (approach_client.getState() == actionlib::SimpleClientGoalState::SUCCEEDED){
        return true;
    }
    return false;
}

void Quadrotor::takeoff()
{
    hector_uav_msgs::EnableMotors srv;
    srv.request.enable = true;
    motor_enable_service.call(srv);
    
    ros::Rate rate(1);


    geometry_msgs::Pose takeoff_pose = odometry_information;
    takeoff_pose.position.z = exp_altitude;
    go(takeoff_pose);
    ROS_INFO("Takeoff successful");
}

void Quadrotor::run(const hector_moveit_exploration::ExecuteDroneExplorationGoalConstPtr &goal)
{
    cur_XMIN = goal->x_min;
    cur_XMAX = goal->x_max;
    cur_YMIN = goal->y_min;
    cur_YMAX = goal->y_max;
    ROS_INFO("EXPLORATION LIMITS:\n x_min: %f;\n x_max: %f;\n t_min: %f;\n y_max: %f;",cur_XMIN,cur_XMAX,cur_YMIN,cur_YMAX);
    
    ros::Rate rate(2);
    while(!odom_received)
        rate.sleep();

    //Ensure the drone is at the assessment height
    if (odometry_information.position.z < exp_altitude)    
        takeoff();

    //Move the drone to the center of the exploration area
    int trials = 0;
    while (odometry_information.position.x < cur_XMIN || odometry_information.position.x > cur_XMAX ||
    odometry_information.position.y < cur_YMIN || odometry_information.position.y > cur_YMAX){

        geometry_msgs::Pose pose = odometry_information;
        pose.position.x = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/(cur_XMAX - cur_XMIN))) + cur_XMIN; 
        pose.position.y = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/(cur_YMAX - cur_YMIN))) + cur_YMIN; 
        pose.position.z = exp_altitude;
        bool move_to_area = go(pose);
        if(move_to_area){
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

        if(frontiers.empty()){
            double xspan = XMAX-XMIN;
            double yspan = YMAX-YMIN;

            int indices_x = (cur_XMAX-cur_XMIN)*GRID/xspan;
            int indices_y = (cur_YMAX-cur_YMIN)*GRID/yspan;

            bool exp_success = true;
            // Verify if all points of the grid have been explored
            for(int x = 0; x<indices_x; x++){
                for(int y = 0; y<indices_y; y++){
                    int xpatch = ((cur_XMIN + x*xspan/GRID) - XMIN)*GRID/xspan;
                    int ypatch = ((cur_YMIN + y*yspan/GRID) - YMIN)*GRID/yspan;
                    if (patches[xpatch][ypatch] < PATCH_LIMIT){
                        exp_success = false;
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
        bool invalid = false;
        for(int i=0;i<invalid_poses.size();i++){
            
            if(sqrt(pow(invalid_poses[i].position.x - _goal.position.x,2) + pow(invalid_poses[i].position.y - _goal.position.y,2) 
                + pow(invalid_poses[i].position.z - _goal.position.z,2)) < 1.5){
                invalid = true;
                invalid_poses.push_back(_goal);
                break;
            }
        }
        if(invalid) continue;
        
        // ROS_ERROR("\n\nALREADY EXPLORED POINTS");
        // for(auto a : explored){
        //     ROS_ERROR_STREAM(a);
        // }

        // ROS_ERROR("\n\nNEXT POINTS");
        // ROS_ERROR_STREAM(_goal);
        
        success = go(_goal);
        if(!success) invalid_poses.push_back(_goal);
        else{
            double xspan = XMAX-XMIN;
            double yspan = YMAX-YMIN;
            int xpatch = (_goal.position.x - XMIN)*GRID/xspan;
            int ypatch = (_goal.position.y - YMIN)*GRID/yspan;
            patches[xpatch][ypatch]++;

            geometry_msgs::Point msg;
            msg.x = xpatch;
            msg.y = ypatch;
            gui_ack.publish(msg);
        }
        feedback_.current_pose = odometry_information;
        as_.publishFeedback(feedback_);

        ros::spinOnce();
        rate.sleep();
    }
    // as_.setAborted(result_);
}