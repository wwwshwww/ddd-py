-- 将来的にコンテキスト毎にサービスを独立させるとき、user テーブルを以下のようにする
-- - 主キー id をサービス間で暗黙的に共有
-- - 認証コンテキストのカラムである google_sub を移行
-- * resource
CREATE TABLE
    `user` (
        `id` BINARY(16) NOT NULL,
        `google_sub` VARCHAR(255) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `user_uk1` (`google_sub`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * updatable resource in event (パフォーマンス面を考慮)
CREATE TABLE
    `user_session` (
        `id` BINARY(16) NOT NULL,
        `user_id` BINARY(16) NOT NULL,
        `hashed_token` VARCHAR(255) NOT NULL,
        `created_at` DATETIME,
        `last_activity_at` DATETIME,
        `expires_at` DATETIME,
        PRIMARY KEY (`id`),
        CONSTRAINT `user_session_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * event
CREATE TABLE
    `auth_session` (
        `id` BINARY(16) NOT NULL,
        `client_state` VARCHAR(255),
        `started_at` DATETIME NOT NULL,
        `expires_at` DATETIME NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * resource
CREATE TABLE
    `user_version` (
        `id` BINARY(16) NOT NULL,
        `name` VARCHAR(255) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * updatable resource
CREATE TABLE
    `user_current_version` (
        `user_id` BINARY(16) NOT NULL,
        `user_version_id` BINARY(16) NOT NULL,
        PRIMARY KEY (`user_id`, `user_version_id`),
        CONSTRAINT `user_current_version_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
        CONSTRAINT `user_current_version_ibfk_2` FOREIGN KEY (`user_version_id`) REFERENCES `user_version` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * event
CREATE TABLE
    `user_version_history` (
        `user_id` BINARY(16) NOT NULL,
        `user_version_id` BINARY(16) NOT NULL,
        `effective_from` DATETIME NOT NULL,
        PRIMARY KEY (`user_id`, `user_version_id`),
        CONSTRAINT `user_version_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
        CONSTRAINT `user_version_history_ibfk_2` FOREIGN KEY (`user_version_id`) REFERENCES `user_version` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * event
CREATE TABLE
    `post` (
        `id` BINARY(16) NOT NULL,
        `user_version_id` BINARY(16) NOT NULL,
        `content` VARCHAR(1024) NOT NULL,
        `posted_at` DATETIME NOT NULL,
        PRIMARY KEY (`id`),
        CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_version_id`) REFERENCES `user_version` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * updatable event 
CREATE TABLE
    `post_generation` (
        `id` BINARY(16) NOT NULL,
        `user_version_id` BINARY(16) NOT NULL,
        `latest_status` VARCHAR(50) NOT NULL,
        `requested_at` DATETIME NOT NULL,
        PRIMARY KEY (`id`),
        CONSTRAINT `post_generate_request_ibfk_1` FOREIGN KEY (`user_version_id`) REFERENCES `user_version` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * event
CREATE TABLE
    `post_generation_process` (
        `id` BINARY(16) NOT NULL,
        `post_generation_id` BINARY(16) NOT NULL,
        `status` VARCHAR(50) NOT NULL,
        `executed_at` DATETIME NOT NULL,
        PRIMARY KEY (`id`),
        CONSTRAINT `post_generation_process_ibfk_1` FOREIGN KEY (`post_generation_id`) REFERENCES `post_generation` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * event
CREATE TABLE
    `post_generation_process_request` (
        `post_generation_process_id` BINARY(16) NOT NULL,
        CONSTRAINT `post_generation_process_request_ibfk_1` FOREIGN KEY (`post_generation_process_id`) REFERENCES `post_generation_process` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * resource
CREATE TABLE
    `post_generation_process_request_keyword` (
        `post_generation_process_request_id` BINARY(16) NOT NULL,
        `keyword` VARCHAR(255) NOT NULL,
        `position` INT UNSIGNED NOT NULL,
        CONSTRAINT `post_generation_process_request_keyword_ibfk_1` FOREIGN KEY (`post_generation_process_request_id`) REFERENCES `post_generation_process_request` (`post_generation_process_id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * event
CREATE TABLE
    `post_generation_process_respond` (
        `post_generation_process_id` BINARY(16) NOT NULL,
        `result_status` VARCHAR(50) NOT NULL,
        `created_post_id` BINARY(16) NOT NULL,
        CONSTRAINT `post_generation_process_respond_ibfk_1` FOREIGN KEY (`post_generation_process_id`) REFERENCES `post_generation_process` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * resource
CREATE TABLE
    `reaction_preset` (
        `id` BINARY(16) NOT NULL,
        `content` VARCHAR(255) NOT NULL,
        `created_user_version_id` BINARY(16) NOT NULL,
        `created_at` DATETIME NOT NULL,
        PRIMARY KEY (`id`),
        CONSTRAINT `reaction_preset_ibfk_1` FOREIGN KEY (`created_user_version_id`) REFERENCES `user_version` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * event
CREATE TABLE
    `reaction` (
        `id` BINARY(16) NOT NULL,
        `user_version_id` BINARY(16) NOT NULL,
        `post_id` BINARY(16) NOT NULL,
        `reaction_preset_id` BINARY(16) NOT NULL,
        `reacted_at` DATETIME NOT NULL,
        `approval` BOOLEAN NOT NULL,
        PRIMARY KEY (`id`),
        CONSTRAINT `reaction_ibfk_1` FOREIGN KEY (`user_version_id`) REFERENCES `user_version` (`id`) ON DELETE CASCADE,
        CONSTRAINT `reaction_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE,
        CONSTRAINT `reaction_ibfk_3` FOREIGN KEY (`reaction_preset_id`) REFERENCES `reaction_preset` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- * event
CREATE TABLE
    `reaction_approval_history` (
        `reaction_id` BINARY(16) NOT NULL,
        `approval` BOOLEAN NOT NULL,
        `configured_from` DATETIME NOT NULL,
        CONSTRAINT `reaction_approval_history_ibfk_1` FOREIGN KEY (`reaction_id`) REFERENCES `reaction` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;