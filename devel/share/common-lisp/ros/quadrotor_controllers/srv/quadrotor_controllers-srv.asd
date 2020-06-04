
(cl:in-package :asdf)

(defsystem "quadrotor_controllers-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :quadrotor_controllers-msg
)
  :components ((:file "_package")
    (:file "motion" :depends-on ("_package_motion"))
    (:file "_package_motion" :depends-on ("_package"))
    (:file "srv1" :depends-on ("_package_srv1"))
    (:file "_package_srv1" :depends-on ("_package"))
  ))