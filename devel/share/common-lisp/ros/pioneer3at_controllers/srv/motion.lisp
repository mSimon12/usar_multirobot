; Auto-generated. Do not edit!


(cl:in-package pioneer3at_controllers-srv)


;//! \htmlinclude motion-request.msg.html

(cl:defclass <motion-request> (roslisp-msg-protocol:ros-message)
  ((destination
    :reader destination
    :initarg :destination
    :type geometry_msgs-msg:Twist
    :initform (cl:make-instance 'geometry_msgs-msg:Twist)))
)

(cl:defclass motion-request (<motion-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <motion-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'motion-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name pioneer3at_controllers-srv:<motion-request> is deprecated: use pioneer3at_controllers-srv:motion-request instead.")))

(cl:ensure-generic-function 'destination-val :lambda-list '(m))
(cl:defmethod destination-val ((m <motion-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pioneer3at_controllers-srv:destination-val is deprecated.  Use pioneer3at_controllers-srv:destination instead.")
  (destination m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <motion-request>) ostream)
  "Serializes a message object of type '<motion-request>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'destination) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <motion-request>) istream)
  "Deserializes a message object of type '<motion-request>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'destination) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<motion-request>)))
  "Returns string type for a service object of type '<motion-request>"
  "pioneer3at_controllers/motionRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'motion-request)))
  "Returns string type for a service object of type 'motion-request"
  "pioneer3at_controllers/motionRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<motion-request>)))
  "Returns md5sum for a message object of type '<motion-request>"
  "5f07416156f9cd98c81988e24b4d6bda")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'motion-request)))
  "Returns md5sum for a message object of type 'motion-request"
  "5f07416156f9cd98c81988e24b4d6bda")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<motion-request>)))
  "Returns full string definition for message of type '<motion-request>"
  (cl:format cl:nil "#Request message type~%geometry_msgs/Twist destination~%~%~%================================================================================~%MSG: geometry_msgs/Twist~%# This expresses velocity in free space broken into its linear and angular parts.~%Vector3  linear~%Vector3  angular~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'motion-request)))
  "Returns full string definition for message of type 'motion-request"
  (cl:format cl:nil "#Request message type~%geometry_msgs/Twist destination~%~%~%================================================================================~%MSG: geometry_msgs/Twist~%# This expresses velocity in free space broken into its linear and angular parts.~%Vector3  linear~%Vector3  angular~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <motion-request>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'destination))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <motion-request>))
  "Converts a ROS message object to a list"
  (cl:list 'motion-request
    (cl:cons ':destination (destination msg))
))
;//! \htmlinclude motion-response.msg.html

(cl:defclass <motion-response> (roslisp-msg-protocol:ros-message)
  ((succeeded
    :reader succeeded
    :initarg :succeeded
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass motion-response (<motion-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <motion-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'motion-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name pioneer3at_controllers-srv:<motion-response> is deprecated: use pioneer3at_controllers-srv:motion-response instead.")))

(cl:ensure-generic-function 'succeeded-val :lambda-list '(m))
(cl:defmethod succeeded-val ((m <motion-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pioneer3at_controllers-srv:succeeded-val is deprecated.  Use pioneer3at_controllers-srv:succeeded instead.")
  (succeeded m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <motion-response>) ostream)
  "Serializes a message object of type '<motion-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'succeeded) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <motion-response>) istream)
  "Deserializes a message object of type '<motion-response>"
    (cl:setf (cl:slot-value msg 'succeeded) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<motion-response>)))
  "Returns string type for a service object of type '<motion-response>"
  "pioneer3at_controllers/motionResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'motion-response)))
  "Returns string type for a service object of type 'motion-response"
  "pioneer3at_controllers/motionResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<motion-response>)))
  "Returns md5sum for a message object of type '<motion-response>"
  "5f07416156f9cd98c81988e24b4d6bda")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'motion-response)))
  "Returns md5sum for a message object of type 'motion-response"
  "5f07416156f9cd98c81988e24b4d6bda")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<motion-response>)))
  "Returns full string definition for message of type '<motion-response>"
  (cl:format cl:nil "~%#Response message type~%bool succeeded~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'motion-response)))
  "Returns full string definition for message of type 'motion-response"
  (cl:format cl:nil "~%#Response message type~%bool succeeded~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <motion-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <motion-response>))
  "Converts a ROS message object to a list"
  (cl:list 'motion-response
    (cl:cons ':succeeded (succeeded msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'motion)))
  'motion-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'motion)))
  'motion-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'motion)))
  "Returns string type for a service object of type '<motion>"
  "pioneer3at_controllers/motion")