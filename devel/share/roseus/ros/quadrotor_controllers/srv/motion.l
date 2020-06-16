;; Auto-generated. Do not edit!


(when (boundp 'quadrotor_controllers::motion)
  (if (not (find-package "QUADROTOR_CONTROLLERS"))
    (make-package "QUADROTOR_CONTROLLERS"))
  (shadow 'motion (find-package "QUADROTOR_CONTROLLERS")))
(unless (find-package "QUADROTOR_CONTROLLERS::MOTION")
  (make-package "QUADROTOR_CONTROLLERS::MOTION"))
(unless (find-package "QUADROTOR_CONTROLLERS::MOTIONREQUEST")
  (make-package "QUADROTOR_CONTROLLERS::MOTIONREQUEST"))
(unless (find-package "QUADROTOR_CONTROLLERS::MOTIONRESPONSE")
  (make-package "QUADROTOR_CONTROLLERS::MOTIONRESPONSE"))

(in-package "ROS")

(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))




(defclass quadrotor_controllers::motionRequest
  :super ros::object
  :slots (_destination ))

(defmethod quadrotor_controllers::motionRequest
  (:init
   (&key
    ((:destination __destination) (instance geometry_msgs::Twist :init))
    )
   (send-super :init)
   (setq _destination __destination)
   self)
  (:destination
   (&rest __destination)
   (if (keywordp (car __destination))
       (send* _destination __destination)
     (progn
       (if __destination (setq _destination (car __destination)))
       _destination)))
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Twist _destination
    (send _destination :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Twist _destination
       (send _destination :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Twist _destination
     (send _destination :deserialize buf ptr-) (incf ptr- (send _destination :serialization-length))
   ;;
   self)
  )

(defclass quadrotor_controllers::motionResponse
  :super ros::object
  :slots (_succeeded ))

(defmethod quadrotor_controllers::motionResponse
  (:init
   (&key
    ((:succeeded __succeeded) nil)
    )
   (send-super :init)
   (setq _succeeded __succeeded)
   self)
  (:succeeded
   (&optional __succeeded)
   (if __succeeded (setq _succeeded __succeeded)) _succeeded)
  (:serialization-length
   ()
   (+
    ;; bool _succeeded
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _succeeded
       (if _succeeded (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _succeeded
     (setq _succeeded (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass quadrotor_controllers::motion
  :super ros::object
  :slots ())

(setf (get quadrotor_controllers::motion :md5sum-) "5f07416156f9cd98c81988e24b4d6bda")
(setf (get quadrotor_controllers::motion :datatype-) "quadrotor_controllers/motion")
(setf (get quadrotor_controllers::motion :request) quadrotor_controllers::motionRequest)
(setf (get quadrotor_controllers::motion :response) quadrotor_controllers::motionResponse)

(defmethod quadrotor_controllers::motionRequest
  (:response () (instance quadrotor_controllers::motionResponse :init)))

(setf (get quadrotor_controllers::motionRequest :md5sum-) "5f07416156f9cd98c81988e24b4d6bda")
(setf (get quadrotor_controllers::motionRequest :datatype-) "quadrotor_controllers/motionRequest")
(setf (get quadrotor_controllers::motionRequest :definition-)
      "#Request message type
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
---

#Response message type
bool succeeded


")

(setf (get quadrotor_controllers::motionResponse :md5sum-) "5f07416156f9cd98c81988e24b4d6bda")
(setf (get quadrotor_controllers::motionResponse :datatype-) "quadrotor_controllers/motionResponse")
(setf (get quadrotor_controllers::motionResponse :definition-)
      "#Request message type
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
---

#Response message type
bool succeeded


")



(provide :quadrotor_controllers/motion "5f07416156f9cd98c81988e24b4d6bda")


