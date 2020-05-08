;; Auto-generated. Do not edit!


(when (boundp 'controllers::motionFeedback)
  (if (not (find-package "CONTROLLERS"))
    (make-package "CONTROLLERS"))
  (shadow 'motionFeedback (find-package "CONTROLLERS")))
(unless (find-package "CONTROLLERS::MOTIONFEEDBACK")
  (make-package "CONTROLLERS::MOTIONFEEDBACK"))

(in-package "ROS")
;;//! \htmlinclude motionFeedback.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass controllers::motionFeedback
  :super ros::object
  :slots (_actual_position ))

(defmethod controllers::motionFeedback
  (:init
   (&key
    ((:actual_position __actual_position) (instance geometry_msgs::Twist :init))
    )
   (send-super :init)
   (setq _actual_position __actual_position)
   self)
  (:actual_position
   (&rest __actual_position)
   (if (keywordp (car __actual_position))
       (send* _actual_position __actual_position)
     (progn
       (if __actual_position (setq _actual_position (car __actual_position)))
       _actual_position)))
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Twist _actual_position
    (send _actual_position :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Twist _actual_position
       (send _actual_position :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Twist _actual_position
     (send _actual_position :deserialize buf ptr-) (incf ptr- (send _actual_position :serialization-length))
   ;;
   self)
  )

(setf (get controllers::motionFeedback :md5sum-) "9e54b00c7d8e976a3c9bd4ca7cb24983")
(setf (get controllers::motionFeedback :datatype-) "controllers/motionFeedback")
(setf (get controllers::motionFeedback :definition-)
      "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
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
")



(provide :controllers/motionFeedback "9e54b00c7d8e976a3c9bd4ca7cb24983")

