/**
 * @file /cruizcore/include/cruizcore/cruizcore_nodelet.hpp
 *
 * @brief Interface for the ros nodelet wrapper around cruizcore.
 *
 * @date 20/08/2010
 **/
/*****************************************************************************
 ** Ifdefs
 *****************************************************************************/

#ifndef KOBUKI_NODELET_HPP_
#define KOBUKI_NODELET_HPP_

/*****************************************************************************
 ** Includes
 *****************************************************************************/

#include <boost/shared_ptr.hpp>

#include <ros/ros.h>
#include <sensor_msgs/JointState.h>
#include <sensor_msgs/Imu.h>
#include <geometry_msgs/Twist.h>
#include <nav_msgs/Odometry.h>
#include <tf/transform_broadcaster.h>

#include <device_nodelet/device_nodelet.hpp>
#include <device_comms/JointCommand.h>
#include <device_comms/JointState.h>
#include <kobuki_comms/SensorData.h>
#include <ecl/sigslots.hpp>
#include <kobuki_driver/kobuki.hpp>

/*****************************************************************************
 ** Namespaces
 *****************************************************************************/

namespace kobuki
{

/*****************************************************************************
 ** Interface
 *****************************************************************************/
/**
 * @brief Pseudo-node for the cruizcore.
 *
 * Configures ros communication types but does not implement the spin loop.
 * This is typically used as part of a library by another process, so the
 * spin loop is adapted elsewhere.
 *
 * This does, however implement all of the cruizcore functionality via the
 * composited cruizcore object. In addition,
 * control loop functionality can be achieved via calling the processInputs()
 * and processOutputs() methods.
 */
class KobukiNodelet : public device_interface::DeviceNodelet
{
public:
  /*********************
   ** C&D
   **********************/
  KobukiNodelet();
  ~KobukiNodelet();

  EIGEN_MAKE_ALIGNED_OPERATOR_NEW

private:
  /******************************************
   ** Device Nodelet Setup
   *******************************************/
  bool init(ros::NodeHandle& nh);
  void advertiseTopics(ros::NodeHandle& nh);
  void subscribeTopics(ros::NodeHandle& nh);

  void publishTransform(const geometry_msgs::Quaternion &odom_quat);
  void publishOdom(const geometry_msgs::Quaternion &odom_quat, const ecl::linear_algebra::Vector3d &pose_update_rates);

  Kobuki kobuki;
  const std::string wheel_left_name;
  const std::string wheel_right_name;

  std::string odom_frame;
  std::string base_frame;
  bool        publish_tf;

  /*********************
  ** Variables
  **********************/
  // Continuously published messages
  geometry_msgs::TransformStamped odom_trans;
  nav_msgs::Odometry odom;
  ecl::Pose2D<double> pose;

  /*********************
   ** Ros Comms
   **********************/
  tf::TransformBroadcaster odom_broadcaster;
  ros::Publisher odom_publisher;
  ros::Publisher wheel_left_state_publisher;
  ros::Publisher wheel_right_state_publisher;
  ros::Publisher sensor_data_publisher;
  ros::Subscriber wheel_left_command_subscriber;
  ros::Subscriber wheel_right_command_subscriber;
  ros::Subscriber velocity_command_subscriber;
  ros::Subscriber kobuki_command_subscriber;

  ecl::Slot<> slot_wheel_state, slot_sensor_data;
  ecl::Signal<const device_comms::JointCommand> sig_joint_command;

  sensor_msgs::JointState joint_states;
  ros::Publisher ir_data_publisher, dock_ir_data_publisher, inertia_data_publisher, imu_data_publisher,
                 cliff_data_publisher, current_data_publisher, magnet_data_publisher, hw_data_publisher,
                 fw_data_publisher, time_data_publisher, st_gyro_data_publisher, eeprom_data_publisher,
                 gp_input_data_publisher, joint_state_publisher;

  ecl::Slot<> slot_ir, slot_dock_ir, slot_inertia, slot_cliff, slot_current, slot_magnet, slot_hw, slot_fw, slot_time,
              slot_st_gyro, slot_eeprom, slot_gp_input;

  ecl::Slot<const std::string&> slot_debug, slot_info, slot_warn, slot_error;

  /*********************
   ** SigSlots
   **********************/
  void publishWheelState();
  void publishSensorData();
  void publishIRData();
  void publishDockIRData();
  void publishInertiaData();
  void publishCliffData();
  void publishCurrentData();
  void publishMagnetData();
  void publishHWData();
  void publishFWData();
  void publishTimeData();
  void publishStGyroData();
  void publishEEPROMData();
  void publishGpInputData();
  void subscribeJointCommandLeft(const device_comms::JointCommand);
  void subscribeJointCommandRight(const device_comms::JointCommand);
  void subscribeVelocityCommand(const geometry_msgs::TwistConstPtr&);
  void subscribeKobukiCommand(const kobuki_comms::CommandConstPtr&);

  /*********************
   ** Ros Logging
   **********************/
  void rosDebug(const std::string &msg)
  {
    ROS_DEBUG_STREAM(msg);
  }
  void rosInfo(const std::string &msg)
  {
    ROS_INFO_STREAM(msg);
  }
  void rosWarn(const std::string &msg)
  {
    ROS_WARN_STREAM(msg);
  }
  void rosError(const std::string &msg)
  {
    ROS_ERROR_STREAM(msg);
  }

  void enable()
  {
    kobuki.run();
    ROS_INFO_STREAM("kobuki enabled.");
  }
  ;

  void disable()
  {
    kobuki.stop();
    ROS_INFO_STREAM("kobuki disable.");
  }
  ;
};

} // namespace cruizcore

#endif /* YCS_DEVICES_CRUIZECORE_NODELET_HPP_ */