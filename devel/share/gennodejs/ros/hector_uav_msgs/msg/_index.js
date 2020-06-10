
"use strict";

let Altimeter = require('./Altimeter.js');
let AttitudeCommand = require('./AttitudeCommand.js');
let Compass = require('./Compass.js');
let ControllerState = require('./ControllerState.js');
let HeadingCommand = require('./HeadingCommand.js');
let HeightCommand = require('./HeightCommand.js');
let MotorCommand = require('./MotorCommand.js');
let MotorPWM = require('./MotorPWM.js');
let MotorStatus = require('./MotorStatus.js');
let PositionXYCommand = require('./PositionXYCommand.js');
let RawImu = require('./RawImu.js');
let RawMagnetic = require('./RawMagnetic.js');
let RawRC = require('./RawRC.js');
let RC = require('./RC.js');
let RuddersCommand = require('./RuddersCommand.js');
let ServoCommand = require('./ServoCommand.js');
let Supply = require('./Supply.js');
let ThrustCommand = require('./ThrustCommand.js');
let VelocityXYCommand = require('./VelocityXYCommand.js');
let VelocityZCommand = require('./VelocityZCommand.js');
let YawrateCommand = require('./YawrateCommand.js');
let LandingAction = require('./LandingAction.js');
let LandingActionFeedback = require('./LandingActionFeedback.js');
let LandingActionGoal = require('./LandingActionGoal.js');
let LandingActionResult = require('./LandingActionResult.js');
let LandingFeedback = require('./LandingFeedback.js');
let LandingGoal = require('./LandingGoal.js');
let LandingResult = require('./LandingResult.js');
let PoseAction = require('./PoseAction.js');
let PoseActionFeedback = require('./PoseActionFeedback.js');
let PoseActionGoal = require('./PoseActionGoal.js');
let PoseActionResult = require('./PoseActionResult.js');
let PoseFeedback = require('./PoseFeedback.js');
let PoseGoal = require('./PoseGoal.js');
let PoseResult = require('./PoseResult.js');
let TakeoffAction = require('./TakeoffAction.js');
let TakeoffActionFeedback = require('./TakeoffActionFeedback.js');
let TakeoffActionGoal = require('./TakeoffActionGoal.js');
let TakeoffActionResult = require('./TakeoffActionResult.js');
let TakeoffFeedback = require('./TakeoffFeedback.js');
let TakeoffGoal = require('./TakeoffGoal.js');
let TakeoffResult = require('./TakeoffResult.js');

module.exports = {
  Altimeter: Altimeter,
  AttitudeCommand: AttitudeCommand,
  Compass: Compass,
  ControllerState: ControllerState,
  HeadingCommand: HeadingCommand,
  HeightCommand: HeightCommand,
  MotorCommand: MotorCommand,
  MotorPWM: MotorPWM,
  MotorStatus: MotorStatus,
  PositionXYCommand: PositionXYCommand,
  RawImu: RawImu,
  RawMagnetic: RawMagnetic,
  RawRC: RawRC,
  RC: RC,
  RuddersCommand: RuddersCommand,
  ServoCommand: ServoCommand,
  Supply: Supply,
  ThrustCommand: ThrustCommand,
  VelocityXYCommand: VelocityXYCommand,
  VelocityZCommand: VelocityZCommand,
  YawrateCommand: YawrateCommand,
  LandingAction: LandingAction,
  LandingActionFeedback: LandingActionFeedback,
  LandingActionGoal: LandingActionGoal,
  LandingActionResult: LandingActionResult,
  LandingFeedback: LandingFeedback,
  LandingGoal: LandingGoal,
  LandingResult: LandingResult,
  PoseAction: PoseAction,
  PoseActionFeedback: PoseActionFeedback,
  PoseActionGoal: PoseActionGoal,
  PoseActionResult: PoseActionResult,
  PoseFeedback: PoseFeedback,
  PoseGoal: PoseGoal,
  PoseResult: PoseResult,
  TakeoffAction: TakeoffAction,
  TakeoffActionFeedback: TakeoffActionFeedback,
  TakeoffActionGoal: TakeoffActionGoal,
  TakeoffActionResult: TakeoffActionResult,
  TakeoffFeedback: TakeoffFeedback,
  TakeoffGoal: TakeoffGoal,
  TakeoffResult: TakeoffResult,
};
