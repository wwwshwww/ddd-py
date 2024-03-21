-- 将来的にサービスを分離させるときの方向性は以下の通り
-- - 主キー id をサービス間で暗黙的に共有
-- - 認証コンテキストのカラムである google_sub を移行
CREATE TABLE `user` (
    `id` BINARY(16) NOT NULL,
    `google_sub` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE `user_session` (
    `id` BINARY(16) NOT NULL,
    `user_id` BINARY(16) NOT NULL,
    `hashed_token` VARCHAR(255) NOT NULL,
    `created_at` DATETIME,
    `last_activity_at` DATETIME,
    `expires_at` DATETIME,
    PRIMARY KEY (`id`),
    CONSTRAINT `user_session_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE `auth_session` (
    `id` BINARY(16) NOT NULL,
    `client_state` VARCHAR(255),
    `expires_at` DATETIME,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE `user_version` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE `user_current_version` (
    `user_id` BINARY(16) NOT NULL,
    `user_version_id` BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (`user_id`, `user_version_id`),
    CONSTRAINT `user_current_version_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
    CONSTRAINT `user_current_version_ibfk_1` FOREIGN KEY (`user_version_id`) REFERENCES `user_version`(`id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE `user_version_history` (
    `user_id` BINARY(16) NOT NULL,
    `user_version_id` BIGINT UNSIGNED NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`, `user_version_id`),
    CONSTRAINT `user_version_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `user_version_history_ibfk_2` FOREIGN KEY (`user_version_id`) REFERENCES `user_version` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;