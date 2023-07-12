/*
 Navicat Premium Data Transfer

 Source Server         : MySql
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : localhost:3306
 Source Schema         : recovery

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

 Date: 11/07/2023 12:15:54
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for articles
-- ----------------------------
DROP TABLE IF EXISTS `articles`;
CREATE TABLE `articles`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标题',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `author` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '作者userid',
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '内容',
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '图片/视频地址',
  `type` int NOT NULL DEFAULT 0 COMMENT '0：图片，1：视频',
  `class_` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '类别',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_articles_userinfo_1`(`author` ASC) USING BTREE,
  CONSTRAINT `fk_articles_userinfo_1` FOREIGN KEY (`author`) REFERENCES `userinfo` (`openid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for collect
-- ----------------------------
DROP TABLE IF EXISTS `collect`;
CREATE TABLE `collect`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `article_id` int NOT NULL COMMENT '文章id',
  `collector_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '收藏者userid',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_collect_articles_1`(`article_id` ASC) USING BTREE,
  INDEX `fk_collect_userinfo_1`(`collector_id` ASC) USING BTREE,
  CONSTRAINT `fk_collect_articles_1` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_collect_userinfo_1` FOREIGN KEY (`collector_id`) REFERENCES `userinfo` (`openid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments`  (
  `id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'id',
  `commenter` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '评论用户userid',
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '评论内容',
  `post_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '绑定帖子',
  `comment_time` datetime NOT NULL COMMENT '评论时间',
  `parent` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '父级评论',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_comments_comments_1`(`parent` ASC) USING BTREE,
  INDEX `fk_comments_posts_1`(`post_id` ASC) USING BTREE,
  INDEX `fk_comments_userinfo_1`(`commenter` ASC) USING BTREE,
  CONSTRAINT `fk_comments_userinfo_1` FOREIGN KEY (`commenter`) REFERENCES `userinfo` (`openid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_comments_comments_1` FOREIGN KEY (`parent`) REFERENCES `comments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_comments_posts_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for detail_info
-- ----------------------------
DROP TABLE IF EXISTS `detail_info`;
CREATE TABLE `detail_info`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `task` int NOT NULL COMMENT '任务id',
  `finish_date` datetime NOT NULL COMMENT '完成日期',
  `score` float NOT NULL COMMENT '评分',
  `evaluation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '评价文件',
  `video` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '视频名称',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_date_task`(`finish_date` ASC, `task` ASC) USING BTREE,
  INDEX `fk_detail_task_1`(`task` ASC) USING BTREE,
  CONSTRAINT `fk_detail_task_1` FOREIGN KEY (`task`) REFERENCES `task_info` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for doctor_info
-- ----------------------------
DROP TABLE IF EXISTS `doctor_info`;
CREATE TABLE `doctor_info`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
  `occupation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '职称',
  `hospital` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '工作单位',
  `department` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '科室',
  `userid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户id',
  `phone` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '联系电话',
  `profile` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '简介',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `fk_doctorinfo_userinfo_1`(`userid` ASC) USING BTREE,
  UNIQUE INDEX `fk_doctorinfo_phone`(`phone` ASC) USING BTREE,
  CONSTRAINT `fk_doctorinfo_userinfo_1` FOREIGN KEY (`userid`) REFERENCES `userinfo` (`openid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for likes
-- ----------------------------
DROP TABLE IF EXISTS `likes`;
CREATE TABLE `likes`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `post_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '帖子id',
  `userid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_likes_posts_1`(`post_id` ASC) USING BTREE,
  INDEX `fk_likes_userinfo_1`(`userid` ASC) USING BTREE,
  CONSTRAINT `fk_likes_userinfo_1` FOREIGN KEY (`userid`) REFERENCES `userinfo` (`openid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_likes_posts_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for patient_info
-- ----------------------------
DROP TABLE IF EXISTS `patient_info`;
CREATE TABLE `patient_info`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
  `age` int NOT NULL COMMENT '年龄',
  `gender` int NOT NULL DEFAULT 0 COMMENT '性别（0：未设置，1：男，2：女）',
  `marriage` int NOT NULL DEFAULT 0 COMMENT '婚姻（0：保密，1：未婚，2：已婚）',
  `userid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户id',
  `phone` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '联系电话',
  `occupation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '职业',
  `nationality` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '民族',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `fk_patientinfo_userinfo_1`(`userid` ASC) USING BTREE,
  UNIQUE INDEX `fk_patientinfo_phone`(`phone` ASC) USING BTREE,
  CONSTRAINT `fk_patientinfo_userinfo_1` FOREIGN KEY (`userid`) REFERENCES `userinfo` (`openid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for posts
-- ----------------------------
DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts`  (
  `id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'id',
  `creator` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '创建者userid',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `views` int NOT NULL COMMENT '浏览量',
  `stars` int NOT NULL COMMENT '点赞数',
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '内容',
  `pictures` json NULL COMMENT '图片地址',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_posts_userinfo_1`(`creator` ASC) USING BTREE,
  CONSTRAINT `fk_posts_userinfo_1` FOREIGN KEY (`creator`) REFERENCES `userinfo` (`openid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for task_info
-- ----------------------------
DROP TABLE IF EXISTS `task_info`;
CREATE TABLE `task_info`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `status` int NOT NULL DEFAULT 0 COMMENT '任务状态（0：待接收，1：进行中，2：已完成）',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '任务描述',
  `create_time` datetime NOT NULL COMMENT '发布时间',
  `deadline` date NOT NULL COMMENT '任务期限',
  `doctor` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '发布医生',
  `patient` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '接收患者',
  `training_root` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '训练视频文件夹',
  `evaluate_root` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '模型评估输出文件夹',
  `circle_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '训练周期',
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '任务类型',
  `difficulty` int NOT NULL DEFAULT 0 COMMENT '任务难度（0：易，1：中，2：难）',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_task_doctor_1`(`doctor` ASC) USING BTREE,
  INDEX `fk_task_patient_1`(`patient` ASC) USING BTREE,
  CONSTRAINT `fk_task_doctor_1` FOREIGN KEY (`doctor`) REFERENCES `doctor_info` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_task_patient_1` FOREIGN KEY (`patient`) REFERENCES `patient_info` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user_bind
-- ----------------------------
DROP TABLE IF EXISTS `user_bind`;
CREATE TABLE `user_bind`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `doctor` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '医生userid',
  `patient` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '患者userid',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_user_bind_doctor_info_1`(`doctor` ASC) USING BTREE,
  INDEX `fk_user_bind_patient_info_1`(`patient` ASC) USING BTREE,
  CONSTRAINT `fk_user_bind_doctor_info_1` FOREIGN KEY (`doctor`) REFERENCES `doctor_info` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_bind_patient_info_1` FOREIGN KEY (`patient`) REFERENCES `patient_info` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for userinfo
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo`  (
  `openid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'openid',
  `nickname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '昵称',
  `type` int NOT NULL DEFAULT 0 COMMENT '用户类型（0：未设置，1：管理员，2：患者，3：医生）',
  `session_key` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '会话密钥',
  `img` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '图片地址',
  PRIMARY KEY (`openid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
