import pandas as pd

from tree import Tree

UAV_TASKS = ['approach', 'assessment', 'search', 'return_to_base']
UGV_TASKS = ['approach', 'search', 'return_to_base']

WEIGHTS = [1,1,10,1]         # Weight for cost function [tp, rctp, bat, pose]


class DFS(object):

    def __init__(self, robots_info, tasks):
        
        self.search_tree = Tree()               # Creates the Tree
        self.robots = robots_info               # Set of robots
        self.tasks = tasks                      # Set of tasks to be assigned to robots
        self.nodes_count = 1

        self.__buildTree(self.robots, self.tasks,'root')
        self.search_tree.printTree()

    def __buildTree(self, robots, tasks, parent):
        '''
            Function to recursively insert allowed task allocations to the Tree
        '''
        higher_p_allocated = False              # Variable to ensure that the Tree contains only the higher priority tasks on top of it
        for t in tasks.index:
            # If a higher priority task has already being assigned to a robot on this level of the Tree, 
            # there is no need of searching for robots for another task as an option for this level
            if(not higher_p_allocated):
                for r in robots.index:
                    robot_enabled = True        # Variable to verify if the robot fit to the task

                    # Verify if the robot can apply required sensors
                    if ((tasks.loc[t,'vs'] == 'on') and (robots.loc[r,'vs'] == 'nok')):
                        robot_enabled = False

                    if ((tasks.loc[t,'gs'] == 'on') and (robots.loc[r,'gs'] == 'nok')):
                        robot_enabled = False

                    # Verify if the robot is the type required
                    if ((tasks.loc[t,'agent']) and not (tasks.loc[t,'agent'] in r)):
                        robot_enabled = False

                    # Verify if the robot is capable of executing the required task
                    if (('pioneer3at' in r) and not (tasks.loc[t,'maneuver'] in UGV_TASKS)) or (('UAV' in r) and not (tasks.loc[t,'maneuver'] in UAV_TASKS)):
                        robot_enabled = False

                    if robot_enabled:
                        key = "n{}".format(self.nodes_count)
                        self.nodes_count += 1

                        # Get tasks from parent node
                        value = []
                        p_value = self.search_tree.findTreeNode(parent).getValue()
                        if p_value:
                            for v in p_value:
                                value.append(v)
                        value.append((t,r))
                        self.search_tree.insertNode(parent,key, value)
                        ## insert node parent on the recursive call
                        higher_p_allocated = True
                        self.__buildTree(robots.drop(index = r), tasks.drop(index = t), key)
            

    def run(self):
        '''
            Execute the search in depth on the tree
        '''
        print("\nTASKS:\n{}".format(self.tasks))
        print("\nROBOTS:\n{}".format(self.robots))
        
        # Variable that returns the allocated tasks
        allocation = {}
        for t in self.tasks:
            allocation[t] = None

        # Variable to monitor quantity of allocated tasks
        max_tasks = 0
        max_tasks_node = None

        # Create priority queue with fisrt node
        priority_queue = [('root', 0)]

        while priority_queue:
            n = priority_queue.pop()
            node_key = n[0]
            node_cost = n[1]
            node_depth = self.search_tree.getNodeDepth(node_key)           
            node = self.search_tree.findTreeNode(node_key)

            # All robots or tasks have been allocated
            if((node_depth >= len(self.tasks.index)) or (node_depth >= len(self.robots.index))):
                return node

            # Current node is the one with more tasks allocated    
            elif node_depth > max_tasks:
                max_tasks_node = node
                max_tasks = node_depth

            # Get next open nodes
            for ch in node.children:
                task = ch.getValue()[-1][0]
                robot = ch.getValue()[-1][1]
                cost = node_cost + self.costFunction(task, robot)
                priority_queue.append((ch.key, cost))
            
            priority_queue.sort(key=lambda tup: tup[1], reverse = True)

        return max_tasks_node
        

    def costFunction(self, task, robot):
        '''
            Calc the cost of allocating the robot to the task.
        '''
        cost = 0

        # Increase cost due to task priority
        cost += self.tasks.loc[task,'priority'] * WEIGHTS[0]

        # Increase cost due to replacing current task of the robot
        if self.robots.loc[robot,'current_task_id']:
            cost += (10 - self.tasks.loc[self.robots.loc[robot,'current_task_id'],'priority']) * WEIGHTS[1] 

        # Increase cost due to batery level
        cost += (100 - self.robots.loc[robot,'bat'])/100 * WEIGHTS[2]

        # Increase cost due to distance between the robot and the task
        dist = 0
        if self.tasks.loc[task,'position']:
            x_dif = self.robots.loc[robot,'pose']['x'] - self.tasks.loc[task,'position']['x']
            y_dif = self.robots.loc[robot,'pose']['y'] - self.tasks.loc[task,'position']['y']
            z_dif = self.robots.loc[robot,'pose']['z'] - self.tasks.loc[task,'position']['z']

            dist = (x_dif**2 + y_dif**2 + z_dif**2)**(1/2)
         
        elif self.tasks.loc[task,'region']:
            x_dif = self.robots.loc[robot,'pose']['x'] - self.tasks.loc[task,'region']['x0']
            y_dif = self.robots.loc[robot,'pose']['y'] - self.tasks.loc[task,'region']['y0']
            z_dif = self.robots.loc[robot,'pose']['z'] - self.tasks.loc[task,'region']['z0']

            dist = (x_dif**2 + y_dif**2 + z_dif**2)**(1/2)

        cost += dist* WEIGHTS[3]
        
        return cost