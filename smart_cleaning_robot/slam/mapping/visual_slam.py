import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import cv2
from cv_bridge import CvBridge
from ORB_SLAM2 import ORB_SLAM2_System  # ORB-SLAM2 연동
import numpy as np

class RobotDogSLAM:
    def __init__(self):
        rospy.init_node('robot_dog_slam', anonymous=True)
        
        # 카메라 이미지 구독
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.image_callback)
        
        # 이동 명령 퍼블리셔
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        
        self.bridge = CvBridge()
        
        # ORB-SLAM2 초기화
        self.slam = ORB_SLAM2_System('Vocabulary/ORBvoc.txt', 'Examples/Monocular/Monocular.yaml', ORB_SLAM2_System.MONOCULAR)
        
        # 초기 속도 설정
        self.vel_msg = Twist()
        self.prev_pose = None
        
    def image_callback(self, data):
        # 카메라 데이터를 SLAM에 입력
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            pose = self.slam.TrackMonocular(cv_image, rospy.get_time())  # SLAM 위치 추정
            
            if pose is not None:
                self.move_robot(pose)
            else:
                self.stop_robot()
            
        except Exception as e:
            rospy.logerr("Error processing image: %s", e)
    
    def move_robot(self, pose):
        # 위치 정보를 사용하여 이동
        if self.prev_pose is not None:
            movement = np.linalg.norm(np.array(pose[:3]) - np.array(self.prev_pose[:3]))  # 이동량 계산
            if movement < 0.1:  # 너무 작은 이동이면 멈춤
                self.stop_robot()
            else:
                self.vel_msg.linear.x = 0.2  # 직진 속도
                self.vel_msg.angular.z = 0.1  # 회전 속도
                self.cmd_pub.publish(self.vel_msg)
        self.prev_pose = pose  # 이전 위치 저장

    def stop_robot(self):
        # 로봇 멈추기
        self.vel_msg.linear.x = 0
        self.vel_msg.angular.z = 0
        self.cmd_pub.publish(self.vel_msg)

    def shutdown(self):
        rospy.loginfo("Shutting down robot...")
        self.stop_robot()
        self.slam.Shutdown()

if __name__ == '__main__':
    try:
        robot_dog = RobotDogSLAM()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass