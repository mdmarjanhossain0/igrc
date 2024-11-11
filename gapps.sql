CREATE DATABASE gappsdb;
use gappsdb;

CREATE TABLE `findings` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `title` VARCHAR(255),
  `description` VARCHAR(255),
  `mitigation` VARCHAR(255),
  `status` VARCHAR(255) DEFAULT 'open',
  `risk` INT DEFAULT 0,
  `task_id` INT,
  `project_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `lockers` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `name` VARCHAR(255),
  `value` JSON,
  `tenant_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `locker_association` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `locker_id` INT,
  `integration_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `integrations` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `name` VARCHAR(255),
  `url` VARCHAR(255),
  `project_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `tasks` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `name` VARCHAR(255),
  `queue` VARCHAR(255),
  `disabled` BOOLEAN DEFAULT false,
  `last_run` DATETIME,
  `not_before` DATETIME,
  `cron` VARCHAR(255),
  `integration_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `task_results` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `data` JSON,
  `version` VARCHAR(255),
  `task_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `jobs` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `result` JSON,
  `bg_id` INT NOT NULL,
  `tenant_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `tenants` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `name` VARCHAR(64) UNIQUE NOT NULL,
  `logo_ref` VARCHAR(255),
  `contact_email` VARCHAR(255),
  `license` VARCHAR(255),
  `approved_domains` VARCHAR(255),
  `magic_link_login` BOOLEAN DEFAULT false,
  `storage_cap` VARCHAR(255) DEFAULT '10000000',
  `owner_id` INT NOT NULL,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `evidence` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255),
  `description` VARCHAR(255),
  `content` VARCHAR(255),
  `collected_on` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `owner_id` INT,
  `tenant_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `evidence_association` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `control_id` INT,
  `evidence_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `policy_associations` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `policy_id` INT,
  `control_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `frameworks` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `reference_link` VARCHAR(255),
  `guidance` VARCHAR(255),
  `feature_evidence` BOOLEAN DEFAULT false,
  `tenant_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `policies` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `name` VARCHAR(255) NOT NULL,
  `ref_code` VARCHAR(255),
  `description` VARCHAR(255),
  `content` VARCHAR(255),
  `template` VARCHAR(255),
  `version` INT DEFAULT 1,
  `visible` BOOLEAN DEFAULT true,
  `tenant_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `controls` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255),
  `ref_code` VARCHAR(255),
  `abs_ref_code` VARCHAR(255),
  `visible` BOOLEAN DEFAULT true,
  `system_level` BOOLEAN DEFAULT true,
  `category` VARCHAR(255),
  `subcategory` VARCHAR(255),
  `guidance` VARCHAR(255),
  `zreferences` VARCHAR(255),
  `mapping` JSON,
  `vendor_recommendations` JSON,
  `level` INT DEFAULT 1,
  `operational_capability` VARCHAR(255),
  `control_type` VARCHAR(255),
  `dti` VARCHAR(255) DEFAULT 'easy',
  `dtc` VARCHAR(255) DEFAULT 'easy',
  `meta` JSON,
  `framework_id` INT,
  `tenant_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `subcontrols` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255),
  `ref_code` VARCHAR(255),
  `mitigation` VARCHAR(255),
  `guidance` VARCHAR(255),
  `meta` JSON,
  `tasks` JSON,
  `implementation_group` INT,
  `control_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `project_members` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT,
  `project_id` INT,
  `access_level` VARCHAR(255) DEFAULT 'viewer',
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `projects` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255),
  `can_auditor_read_scratchpad` BOOLEAN DEFAULT true,
  `can_auditor_write_scratchpad` BOOLEAN DEFAULT false,
  `can_auditor_read_comments` BOOLEAN DEFAULT true,
  `can_auditor_write_comments` BOOLEAN DEFAULT true,
  `target_level` INT DEFAULT 1,
  `notes` VARCHAR(255),
  `owner_id` INT,
  `tenant_id` INT,
  `framework_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `project_policy_associations` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `policy_id` INT,
  `control_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `project_policies` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `public_viewable` BOOLEAN DEFAULT false,
  `content` VARCHAR(255),
  `version` INT DEFAULT 1,
  `project_id` INT,
  `owner_id` INT,
  `reviewer_id` INT,
  `policy_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `project_controls` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `notes` VARCHAR(255),
  `auditor_notes` VARCHAR(255),
  `project_id` INT,
  `control_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `auditor_feedback` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `title` VARCHAR(255),
  `description` VARCHAR(255),
  `response` VARCHAR(255),
  `is_complete` BOOLEAN DEFAULT false,
  `auditor_complete` BOOLEAN DEFAULT false,
  `owner_id` INT,
  `subcontrol_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `subcontrol_comments` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `message` VARCHAR(255),
  `owner_id` INT,
  `subcontrol_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `control_comments` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `message` VARCHAR(255),
  `owner_id` INT,
  `control_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `project_comments` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `message` VARCHAR(255),
  `owner_id` INT,
  `project_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `project_subcontrols` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `implemented` INT DEFAULT 0,
  `is_applicable` BOOLEAN DEFAULT true,
  `context` VARCHAR(255),
  `notes` VARCHAR(255),
  `auditor_notes` VARCHAR(255),
  `review_status` VARCHAR(255) DEFAULT 'not started',
  `auditor_feedback` VARCHAR(255),
  `process_maturity` INT DEFAULT 0,
  `operator_id` INT,
  `owner_id` INT,
  `subcontrol_id` INT NOT NULL,
  `project_control_id` INT NOT NULL,
  `project_id` INT NOT NULL,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `project_tags` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `project_id` INT,
  `tag_id` INT
);

CREATE TABLE `control_tags` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `control_id` INT,
  `tag_id` INT
);

CREATE TABLE `policy_tags` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `policy_id` INT,
  `tag_id` INT
);

CREATE TABLE `roles` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL DEFAULT '',
  `label` VARCHAR(255) DEFAULT ''
);

CREATE TABLE `user_roles` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT,
  `role_id` INT,
  `tenant_id` INT
);

CREATE TABLE `users` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `is_active` BOOLEAN NOT NULL DEFAULT 1,
  `email` VARCHAR(255) UNIQUE NOT NULL,
  `username` VARCHAR(100) UNIQUE,
  `email_confirmed_at` DATETIME,
  `password` VARCHAR(255) NOT NULL DEFAULT '',
  `last_password_change` DATETIME,
  `first_name` VARCHAR(100) NOT NULL DEFAULT '',
  `last_name` VARCHAR(100) NOT NULL DEFAULT '',
  `super` BOOLEAN NOT NULL DEFAULT 0,
  `built_in` BOOLEAN DEFAULT false,
  `tenant_limit` INT DEFAULT 1,
  `can_user_create_tenant` BOOLEAN NOT NULL DEFAULT 1,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `policy_labels` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `zkey` VARCHAR(255) UNIQUE NOT NULL,
  `value` VARCHAR(255) NOT NULL,
  `owner_id` INT NOT NULL,
  `tenant_id` INT NOT NULL,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `tags` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) UNIQUE,
  `color` VARCHAR(255) DEFAULT 'blue',
  `owner_id` INT NOT NULL,
  `tenant_id` INT NOT NULL,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `questionnaire_guests` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `questionnaire_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `questionnaires` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `name` VARCHAR(255) NOT NULL,
  `vendor` VARCHAR(255),
  `description` VARCHAR(255),
  `enabled` BOOLEAN DEFAULT true,
  `feedback` VARCHAR(255),
  `submitted` BOOLEAN DEFAULT false,
  `published` BOOLEAN DEFAULT false,
  `form` JSON,
  `submission` JSON,
  `owner_id` INT NOT NULL,
  `tenant_id` INT NOT NULL,
  `due_before` DATETIME,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `questionnaire_templates` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `uuid` VARCHAR(255) UNIQUE DEFAULT (UUID()),
  `name` VARCHAR(255) UNIQUE,
  `description` VARCHAR(255) UNIQUE,
  `form` JSON,
  `owner_id` INT NOT NULL,
  `tenant_id` INT NOT NULL,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `config_store` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `zkey` VARCHAR(255),
  `value` VARCHAR(255),
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE TABLE `logs` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `namespace` VARCHAR(255) NOT NULL DEFAULT 'general',
  `log_type` VARCHAR(255) NOT NULL DEFAULT 'info',
  `action` VARCHAR(255) DEFAULT 'unknown',
  `message` VARCHAR(255) NOT NULL,
  `succeeded` BOOLEAN DEFAULT true,
  `meta` JSON,
  `user_id` INT,
  `date_added` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `date_updated` DATETIME
);

CREATE UNIQUE INDEX `task_results_index_0` ON `task_results` (`version`, `task_id`);

CREATE UNIQUE INDEX `evidence_index_1` ON `evidence` (`name`, `tenant_id`);

ALTER TABLE `findings` ADD FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`);

ALTER TABLE `findings` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`);

ALTER TABLE `lockers` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`);

ALTER TABLE `locker_association` ADD FOREIGN KEY (`locker_id`) REFERENCES `lockers` (`id`) ON DELETE CASCADE;

ALTER TABLE `locker_association` ADD FOREIGN KEY (`integration_id`) REFERENCES `integrations` (`id`) ON DELETE CASCADE;

ALTER TABLE `integrations` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`);

ALTER TABLE `tasks` ADD FOREIGN KEY (`integration_id`) REFERENCES `integrations` (`id`);

ALTER TABLE `task_results` ADD FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`);

ALTER TABLE `jobs` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`);

ALTER TABLE `tenants` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `evidence` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `evidence` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`);

ALTER TABLE `evidence_association` ADD FOREIGN KEY (`control_id`) REFERENCES `project_subcontrols` (`id`) ON DELETE CASCADE;

ALTER TABLE `evidence_association` ADD FOREIGN KEY (`evidence_id`) REFERENCES `evidence` (`id`) ON DELETE CASCADE;

ALTER TABLE `policy_associations` ADD FOREIGN KEY (`policy_id`) REFERENCES `policies` (`id`) ON DELETE CASCADE;

ALTER TABLE `policy_associations` ADD FOREIGN KEY (`control_id`) REFERENCES `controls` (`id`) ON DELETE CASCADE;

ALTER TABLE `frameworks` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`);

ALTER TABLE `policies` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`);

ALTER TABLE `controls` ADD FOREIGN KEY (`framework_id`) REFERENCES `frameworks` (`id`);

ALTER TABLE `controls` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`);

ALTER TABLE `subcontrols` ADD FOREIGN KEY (`control_id`) REFERENCES `controls` (`id`);

ALTER TABLE `project_members` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

ALTER TABLE `project_members` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE;

ALTER TABLE `projects` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `projects` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`);

ALTER TABLE `projects` ADD FOREIGN KEY (`framework_id`) REFERENCES `frameworks` (`id`);

ALTER TABLE `project_policy_associations` ADD FOREIGN KEY (`policy_id`) REFERENCES `project_policies` (`id`) ON DELETE CASCADE;

ALTER TABLE `project_policy_associations` ADD FOREIGN KEY (`control_id`) REFERENCES `project_controls` (`id`) ON DELETE CASCADE;

ALTER TABLE `project_policies` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`);

ALTER TABLE `project_policies` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `project_policies` ADD FOREIGN KEY (`reviewer_id`) REFERENCES `users` (`id`);

ALTER TABLE `project_policies` ADD FOREIGN KEY (`policy_id`) REFERENCES `policies` (`id`);

ALTER TABLE `project_controls` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`);

ALTER TABLE `project_controls` ADD FOREIGN KEY (`control_id`) REFERENCES `controls` (`id`);

ALTER TABLE `auditor_feedback` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `auditor_feedback` ADD FOREIGN KEY (`subcontrol_id`) REFERENCES `project_subcontrols` (`id`);

ALTER TABLE `subcontrol_comments` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `subcontrol_comments` ADD FOREIGN KEY (`subcontrol_id`) REFERENCES `project_subcontrols` (`id`);

ALTER TABLE `control_comments` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `control_comments` ADD FOREIGN KEY (`control_id`) REFERENCES `project_controls` (`id`);

ALTER TABLE `project_comments` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `project_comments` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`);

ALTER TABLE `project_subcontrols` ADD FOREIGN KEY (`operator_id`) REFERENCES `users` (`id`);

ALTER TABLE `project_subcontrols` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `project_subcontrols` ADD FOREIGN KEY (`subcontrol_id`) REFERENCES `subcontrols` (`id`);

ALTER TABLE `project_subcontrols` ADD FOREIGN KEY (`project_control_id`) REFERENCES `project_controls` (`id`);

ALTER TABLE `project_subcontrols` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`);

ALTER TABLE `project_tags` ADD FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE;

ALTER TABLE `project_tags` ADD FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE;

ALTER TABLE `control_tags` ADD FOREIGN KEY (`control_id`) REFERENCES `project_controls` (`id`) ON DELETE CASCADE;

ALTER TABLE `control_tags` ADD FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE;

ALTER TABLE `policy_tags` ADD FOREIGN KEY (`policy_id`) REFERENCES `project_policies` (`id`) ON DELETE CASCADE;

ALTER TABLE `policy_tags` ADD FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE;

ALTER TABLE `user_roles` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

ALTER TABLE `user_roles` ADD FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE;

ALTER TABLE `user_roles` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`) ON DELETE CASCADE;

ALTER TABLE `policy_labels` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `policy_labels` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`);

ALTER TABLE `tags` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `tags` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`);

ALTER TABLE `questionnaire_guests` ADD FOREIGN KEY (`questionnaire_id`) REFERENCES `questionnaires` (`id`);

ALTER TABLE `questionnaire_guests` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `questionnaires` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `questionnaires` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`);

ALTER TABLE `questionnaire_templates` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`);

ALTER TABLE `questionnaire_templates` ADD FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`);

ALTER TABLE `logs` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
