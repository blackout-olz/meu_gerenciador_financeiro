WITH new_user AS (
  INSERT INTO users (name, cpf, email, phone, birth, password_hash, monthly_income_estimate)
  VALUES ('Ana Silva', '12345678901', 'ana.silva@email.com', '11987654321', '1995-04-12', '$2a$12$eImiTXuWVxfM37uY4JANjOL.8/gA7HashFake', 500000)
  RETURNING id
),
new_categories AS (
  INSERT INTO categories (name, user_id, type, icon)
  SELECT c.name, new_user.id, c.type::transaction_type, c.icon
  FROM new_user, (VALUES
    ('Salário', 'INCOME', 'wallet'),
    ('Alimentação', 'EXPENSE', 'utensils'),
    ('Transporte', 'EXPENSE', 'car')
  ) AS c(name, type, icon)
  RETURNING id, name, user_id
)
INSERT INTO transactions (user_id, categorie_id, amount, type, description, date)
SELECT
  c.user_id,
  c.id,
  t.amount,
  t.type::transaction_type,
  t.description,
  t.date
FROM new_categories c
JOIN (VALUES
  ('Salário', 500000, 'INCOME', 'Pagamento Mensal', CURRENT_TIMESTAMP - INTERVAL '5 days'),
  ('Alimentação', 4550, 'EXPENSE', 'Almoço Restaurante', CURRENT_TIMESTAMP - INTERVAL '2 days'),
  ('Transporte', 2000, 'EXPENSE', 'Recarga Bilhete Único', CURRENT_TIMESTAMP - INTERVAL '1 day')
) AS t(category_name, amount, type, description, date)
ON c.name = t.category_name;