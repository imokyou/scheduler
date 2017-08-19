CREATE DATABASE `schedule_v2` DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

# 日程计划表
# 用于自定义多种不同类型的日程计划
CREATE TABLE IF NOT EXISTS `schedule` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `stype` VARCHAR(16) NOT NULL COMMENT '类型: keepfit, study, life',
    `subject` VARCHAR(512) NOT NULL COMMENT '日程主题',
    `sdate` DATETIME COMMENT '日程的时间',
    `targets` TEXT COMMENT '需要完成的事项',
    `created_at` DATETIME COMMENT'创建时间',
    `updated_at` DATETIME COMMENT '更新时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '日程计划表';

# 日程计划配置表
# 比如说keepfit日程安排几点发送通知消息
CREATE TABLE IF NOT EXISTS `schedule_config` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `schedule_id` INT(11) NOT NULL COMMENT '日程id, 关联schedule表',
    `key` VARCHAR(32) NOT NULL COMMENT '配置的类型: sendtime',
    `value` VARCHAR(256) NOT NULL COMMENT '配置的内容',
    `created_at` DATETIME COMMENT'创建时间',
    `updated_at` DATETIME COMMENT '更新时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '日程计划配置表';

# 代码备忘录表
CREATE TABLE IF NOT EXISTS `code_memo` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `ctype` VARCHAR(11) NOT NULL COMMENT '分类：linux, mysql, python, git',
    `description` VARCHAR(256) NOT NULL COMMENT '简单描述',
    `content` TEXT COMMENT'代码内容',
    `created_at` DATETIME COMMENT'创建时间',
    `updated_at` DATETIME COMMENT '更新时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '代码备忘录表';


# 用户表
# 使用Django自带auth_user表