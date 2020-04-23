;; Auto-generated. Do not edit!


(when (boundp 'controllers::motion)
  (if (not (find-package "CONTROLLERS"))
    (make-package "CONTROLLERS"))
  (shadow 'motion (find-package "CONTROLLERS")))
(unless (find-package "CONTROLLERS::MOTION")
  (make-package "CONTROLLERS::MOTION"))
(unless (find-package "CONTROLLERS::MOTIONREQUEST")
  (make-package "CONTROLLERS::MOTIONREQUEST"))
(unless (find-package "CONTROLLERS::MOTIONRESPONSE")
  (make-package "CONTROLLERS::MOTIONRESPONSE"))

(in-package "ROS")

(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))




(defclass controllers::motionRequest
  :super ros::object
  :slots (_destination ))

(defmethod controllers::motionRequest
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

(defclass controllers::motionResponse
  :super ros::object
  :slots (_succeeded ))

(defmethod controllers::motionResponse
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

(defclass controllers::motion
  :super ros::object
  :slots ())

(setf (get controllers::motion :md5sum-) "5f07416156f9cd98c81988e24b4d6bda")
(setf (get controllers::motion :datatype-) "controllers/motion")
(setf (get controllers::motion :request) controllers::motionRequest)
(setf (get controllers::motion :response) controllers::motionResponse)

(defmethod controllers::motionRequest
  (:response () (instance controllers::motionResponse :init)))

(setf (get controllers::motionRequest :md5sum-) "5f07416156f9cd98c81988e24b4d6bda")
(setf (get controllers::motionRequest :datatype-) "controllers/motionRequest")
(setf (get controllers::motionRequest :definition-)
      "
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


bool succeeded


")

(setf (get controllers::motionResponse :md5sum-) "5f07416156f9cd98c81988e24b4d6bda")
(setf (get controllers::motionResponse :datatype-) "controllers/motionResponse")
(setf (get controllers::motionResponse :definition-)
      "
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


bool succeeded


")



(provide :controllers/motion "5f07416156f9cd98c81988e24b4d6bda")


