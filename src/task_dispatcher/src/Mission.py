from lxml import etree as ET
import pandas as pd

class Mission(object):
    '''
        Class to create missions, save into a xml file and read it from xml files
    '''

    def __init__(self, name = "mission", pri = "0"):
        '''
            Initialize the mission with a name and execution priority
        '''
        self.id = name
        self.priority = pri
        self.tasks = pd.DataFrame(columns = ['agent', 'position', 'region', 'vs', 'gs', 'maneuver'])

        # XML elements
        self.root = ET.Element("mission")
        ET.SubElement(self.root,"id").text = "{}".format(self.id)
        ET.SubElement(self.root,"priority").text = "{}".format(self.priority)


    def add_task(self, dic):
        '''
            Insert a new task on the mission
        '''

        self.tasks = self.tasks.append(dic, ignore_index=True)
        task = ET.SubElement(self.root,"task")

        # Get required agent
        ET.SubElement(task,"agent").text = "{}".format(dic['agent'])

        # Get pose of the maneuver
        pos = ET.SubElement(task,"position")

        if dic['position']:
            ET.SubElement(pos,"x").text = "{}".format(dic['position']['x'])
            ET.SubElement(pos,"y").text = "{}".format(dic['position']['y'])
            ET.SubElement(pos,"z").text = "{}".format(dic['position']['z'])
            ET.SubElement(pos,"theta").text = "{}".format(dic['position']['theta'])

        # Get region of the maneuver
        reg = ET.SubElement(task,"region")

        if dic['region']:
            ET.SubElement(reg,"origin_x").text = "{}".format(dic['region']['x0'])
            ET.SubElement(reg,"origin_y").text = "{}".format(dic['region']['y0'])
            # ET.SubElement(reg,"origin_z").text = "{}".format(dic['region']['z0'])
            ET.SubElement(reg,"x_size").text = "{}".format(dic['region']['x1'])
            ET.SubElement(reg,"y_size").text = "{}".format(dic['region']['y1'])
            # ET.SubElement(reg,"z_size").text = "{}".format(dic['region']['z1'])

        # Get required VS status along the task execution
        ET.SubElement(task,"vs").text = "{}".format(dic['vs'])

        # Get required GS status along the task execution
        ET.SubElement(task,"gs").text = "{}".format(dic['gs'])

        # Get maneuver that represents the task
        ET.SubElement(task,"maneuver").text = "{}".format(dic['maneuver'])


    def get_std_task(self):
        '''
            Return a dictionary with an standard task
        '''
        return {'agent': None, 'position': None, 'region': None, 'vs': False, 'gs': False, 'maneuver': None}

    
    def save(self, filename):
        '''
            Save the XML file
        '''
        tree = ET.ElementTree(self.root)
        pretty_xml = ET.tostring(tree, encoding="unicode", pretty_print=True)

        myfile = open(filename,"w")
        myfile.write(pretty_xml)
        myfile.close()
  
    
    def load(self, filename):
        '''
            Load the XML file
        '''
        tree = ET.parse(filename)

        self.root = tree.getroot()

        # Create ampty tasks DataFrame
        self.tasks = pd.DataFrame(columns = ['agent', 'position', 'region', 'vs', 'gs', 'maneuver'])

        for m_child in self.root:
            # print(m_child.tag)
            # print(m_child.attrib)
            # print(m_child.text)

            if m_child.tag == 'id':
                self.id = m_child.text
            elif m_child.tag == 'priority':
                self.priority = m_child.text
            elif m_child.tag == 'task':

                # Get tags in a dictionary
                texts={}
                for tags in m_child:
                    texts[tags.tag]=tags.text

                task = self.get_std_task()

                task['agent'] = texts['agent']
                task['vs'] = texts['vs'] == 'True'
                task['gs'] = texts['gs'] == 'True'
                task['maneuver'] = texts['maneuver']

                # Get position values if it exist
                pos = m_child.find("position")

                if pos.text:
                    task['position'] = {}

                    task['position']['x'] = float(pos.find('x').text)
                    task['position']['y'] = float(pos.find('y').text)
                    task['position']['z'] = float(pos.find('z').text)
                    task['position']['theta'] = float(pos.find('theta').text)

                # Get region values if it exist
                reg = m_child.find("region")

                if reg.text:
                    task['region'] = {}
                    
                    task['region']['x0'] = float(reg.find('origin_x').text)
                    task['region']['y0'] = float(reg.find('origin_y').text)
                    # task['region']['z0'] = float(reg.find('origin_z').text)
                    task['region']['x1'] = float(reg.find('x_size').text)
                    task['region']['y1'] = float(reg.find('y_size').text)
                    # task['region']['z1'] = float(reg.find('z_size').text)                 

                self.tasks = self.tasks.append(task, ignore_index=True)
                
                