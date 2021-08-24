INSERT INTO category("name", "path", code, "disabled") VALUES
('Últimas',	'ultimas',	36,	false),
('Jundiaí',	'jundiai',	8, false),
('Política', 'politica', 12, false),
('Economia', 'economia', 16, false),
('Polícia',	'policia', 80,	false),
('Esportes', 'esportes', 20, false),
('Cultura',	'cultura', 24,	false),
('Hype', 'hype', 84, false),
('Opinião',	'opiniao', 111,	false);

INSERT INTO "user" (email, "password", full_name) 
VALUES ('test@test.com', '$2b$12$inWs/XiTm9BigxY7kbCATurDV2j/aNnLGJKYW7Du0zuDJIyQUNWCu', 'Choccobo Amarelo')