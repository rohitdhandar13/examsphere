-- EXAMSPHERE SQL (import)
CREATE DATABASE IF NOT EXISTS examsphere;
USE examsphere;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    organization VARCHAR(200),
    apply_link TEXT,
    description TEXT,
    last_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO jobs (title, category, organization, apply_link, description, last_date) VALUES
('IBPS PO Recruitment 2025', 'Banking', 'IBPS', 'https://ibps.in', 'Probationary Officer recruitment for public sector banks.', '2025-02-01'),
('SBI PO Recruitment 2025', 'Banking', 'SBI', 'https://sbi.co.in', 'State Bank of India Probationary Officer recruitment.', '2025-03-10'),
('SSC CHSL 2025', 'SSC', 'Staff Selection Commission', 'https://ssc.nic.in', 'Combined Higher Secondary Level exam.', '2025-01-20'),
('RRB JE 2025', 'Railway', 'Railway Recruitment Board', 'https://rrbcdg.gov.in', 'Junior Engineer recruitment in Indian Railways.', '2025-04-15');

CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    applied_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);
