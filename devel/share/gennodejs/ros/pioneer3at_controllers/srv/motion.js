// Auto-generated. Do not edit!

// (in-package pioneer3at_controllers.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------


//-----------------------------------------------------------

class motionRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.destination = null;
    }
    else {
      if (initObj.hasOwnProperty('destination')) {
        this.destination = initObj.destination
      }
      else {
        this.destination = new geometry_msgs.msg.Twist();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type motionRequest
    // Serialize message field [destination]
    bufferOffset = geometry_msgs.msg.Twist.serialize(obj.destination, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type motionRequest
    let len;
    let data = new motionRequest(null);
    // Deserialize message field [destination]
    data.destination = geometry_msgs.msg.Twist.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 48;
  }

  static datatype() {
    // Returns string type for a service object
    return 'pioneer3at_controllers/motionRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0ee7a53442725ed49843ff163a1b1b2a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    geometry_msgs/Twist destination
    
    
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
    const resolved = new motionRequest(null);
    if (msg.destination !== undefined) {
      resolved.destination = geometry_msgs.msg.Twist.Resolve(msg.destination)
    }
    else {
      resolved.destination = new geometry_msgs.msg.Twist()
    }

    return resolved;
    }
};

class motionResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.succeeded = null;
    }
    else {
      if (initObj.hasOwnProperty('succeeded')) {
        this.succeeded = initObj.succeeded
      }
      else {
        this.succeeded = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type motionResponse
    // Serialize message field [succeeded]
    bufferOffset = _serializer.bool(obj.succeeded, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type motionResponse
    let len;
    let data = new motionResponse(null);
    // Deserialize message field [succeeded]
    data.succeeded = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'pioneer3at_controllers/motionResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '95e696a0d10686913abb262e0b4cbbcf';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    
    bool succeeded
    
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new motionResponse(null);
    if (msg.succeeded !== undefined) {
      resolved.succeeded = msg.succeeded;
    }
    else {
      resolved.succeeded = false
    }

    return resolved;
    }
};

module.exports = {
  Request: motionRequest,
  Response: motionResponse,
  md5sum() { return '5f07416156f9cd98c81988e24b4d6bda'; },
  datatype() { return 'pioneer3at_controllers/motion'; }
};
