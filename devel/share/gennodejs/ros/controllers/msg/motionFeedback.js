// Auto-generated. Do not edit!

// (in-package controllers.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class motionFeedback {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.actual_position = null;
    }
    else {
      if (initObj.hasOwnProperty('actual_position')) {
        this.actual_position = initObj.actual_position
      }
      else {
        this.actual_position = new geometry_msgs.msg.Twist();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type motionFeedback
    // Serialize message field [actual_position]
    bufferOffset = geometry_msgs.msg.Twist.serialize(obj.actual_position, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type motionFeedback
    let len;
    let data = new motionFeedback(null);
    // Deserialize message field [actual_position]
    data.actual_position = geometry_msgs.msg.Twist.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 48;
  }

  static datatype() {
    // Returns string type for a message object
    return 'controllers/motionFeedback';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9e54b00c7d8e976a3c9bd4ca7cb24983';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
    #Define a feedback message
    geometry_msgs/Twist actual_position
    
    
    
    ================================================================================
    MSG: geometry_msgs/Twist
    # This expresses velocity in free space broken into its linear and angular parts.
    Vector3  linear
    Vector3  angular
    
    ================================================================================
    MSG: geometry_msgs/Vector3
    # This represents a vector in free space. 
    # It is only meant to represent a direction. Therefore, it does not
    # make sense to apply a translation to it (e.g., when applying a 
    # generic rigid transformation to a Vector3, tf2 will only apply the
    # rotation). If you want your data to be translatable too, use the
    # geometry_msgs/Point message instead.
    
    float64 x
    float64 y
    float64 z
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new motionFeedback(null);
    if (msg.actual_position !== undefined) {
      resolved.actual_position = geometry_msgs.msg.Twist.Resolve(msg.actual_position)
    }
    else {
      resolved.actual_position = new geometry_msgs.msg.Twist()
    }

    return resolved;
    }
};

module.exports = motionFeedback;