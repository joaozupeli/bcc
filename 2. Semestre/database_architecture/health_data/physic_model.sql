CREATE TABLE `especialidade` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `descricao` varchar(255) NOT NULL,
  `created_at` timestamp,
  `deleted_at` timestamp
);

CREATE TABLE `tipo_relatorio` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `descricao` varchar(255) NOT NULL,
  `created_at` timestamp,
  `deleted_at` timestamp
);

CREATE TABLE `medico` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `especialidade` int NOT NULL,
  `CRM` int UNIQUE NOT NULL,
  `created_at` timestamp,
  `deleted_at` timestamp
);

CREATE TABLE `hospital` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `nome_fantasia` varchar(255) NOT NULL,
  `cnpj` varchar(255) NOT NULL,
  `endereco` varchar(255) NOT NULL,
  `created_at` timestamp,
  `deleted_at` timestamp
);

CREATE TABLE `paciente` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `cpf` varchar(255) UNIQUE NOT NULL,
  `created_at` timestamp,
  `updated_at` timestamp,
  `deleted_at` timestamp
);

CREATE TABLE `prontuario` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `paciente_id` int UNIQUE NOT NULL,
  `created_at` timestamp
);

CREATE TABLE `atendimento` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `prontuario_id` int NOT NULL,
  `medico_id` int NOT NULL,
  `hospital_id` int NOT NULL,
  `data` datetime NOT NULL,
  `created_at` timestamp,
  `updated_at` timestamp,
  `deleted_at` timestamp
);

CREATE TABLE `relatorio` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `atendimento_id` int NOT NULL,
  `tipo` int NOT NULL,
  `descricao` text NOT NULL,
  `created_at` timestamp
);

ALTER TABLE `prontuario` ADD FOREIGN KEY (`paciente_id`) REFERENCES `paciente` (`id`);

ALTER TABLE `relatorio` ADD FOREIGN KEY (`atendimento_id`) REFERENCES `atendimento` (`id`);

ALTER TABLE `atendimento` ADD FOREIGN KEY (`prontuario_id`) REFERENCES `prontuario` (`id`);

ALTER TABLE `atendimento` ADD FOREIGN KEY (`medico_id`) REFERENCES `medico` (`id`);

ALTER TABLE `atendimento` ADD FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`id`);

ALTER TABLE `medico` ADD FOREIGN KEY (`especialidade`) REFERENCES `especialidade` (`id`);

ALTER TABLE `relatorio` ADD FOREIGN KEY (`tipo`) REFERENCES `tipo_relatorio` (`id`);
