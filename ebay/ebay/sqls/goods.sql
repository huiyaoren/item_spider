CREATE TABLE IF NOT EXISTS `goods_{0}` (
    `id` VARCHAR(100) NOT NULL COMMENT '商品id',
    `platform` VARCHAR(20) NOT NULL DEFAULT 'ebay' COMMENT '平台',
    `site` VARCHAR(255) DEFAULT NULL COMMENT '商品所属站点',
    `title` VARCHAR(255) NOT NULL COMMENT '商品信息',
    `default_image` VARCHAR(255) DEFAULT NULL COMMENT '主图',
    `other_images` TEXT COMMENT '商品其他图片，json格式',
    `price` DECIMAL(10,2) NOT NULL DEFAULT '0.00' COMMENT '商品售价',
    `currency` VARCHAR(255) DEFAULT NULL COMMENT '货币符号',
    `total_sold` INT(11) NOT NULL DEFAULT '0' COMMENT '总销量',
    `hit_count` INT(11) DEFAULT NULL COMMENT '访问量',
    `goods_category` VARCHAR(255) NOT NULL COMMENT '商品分类',
    `goods_url` VARCHAR(255) DEFAULT NULL COMMENT '商品页面访问地址',
    `shop_name` VARCHAR(255) DEFAULT NULL COMMENT '店铺名称',
    `shop_feedback_score` INT(11) DEFAULT NULL COMMENT '店铺评分',
    `shop_feedback_percentage` DOUBLE(10,2) DEFAULT NULL COMMENT '店铺好评率',
    `shop_open_time` TIMESTAMP NULL DEFAULT NULL COMMENT '店铺开张时间',
    `publish_time` TIMESTAMP NULL DEFAULT NULL COMMENT '上架时间',
    `weeks_sold` INT(11) NOT NULL DEFAULT '0' COMMENT '周销量',
    `weeks_sold_money` DOUBLE(20,2) DEFAULT '0.00' NOT NULL COMMENT '近7天销售金额',
    `day_sold` INT(11) NOT NULL DEFAULT '0' COMMENT '当日销量',
    `last_weeks_sold` INT(11) DEFAULT NULL COMMENT '上上周销量',
    `trade_increase_rate` DOUBLE(10,4) DEFAULT NULL COMMENT '交易增幅比率，比如：0.1256 表示12.56%',
    `is_hot` ENUM('0','1') DEFAULT '0' COMMENT '是否爆款，0-否，1-是',
    `is_new` ENUM('0','1') DEFAULT '0' COMMENT '是否新品，0-否，1-是',
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
    PRIMARY KEY (`id`),
    KEY `idx_title` (`title`(250)) COMMENT '商品标题',
    KEY `idx_goods_category` (`goods_category`(250)),
    KEY `idx_shop_name` (`shop_name`(250)),
    KEY `idx_price` (`price`) USING BTREE COMMENT '售价',
    KEY `idx_weeks_sold` (`weeks_sold`) COMMENT '商品周销量',
    KEY `idx_trade_increase_rate` (`trade_increase_rate`) COMMENT '交易增幅',
    KEY `idx_shop_open_time` (`shop_open_time`),
    KEY `idx_total_sold` (`total_sold`) USING BTREE COMMENT '总销量'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COMMENT='商品表';