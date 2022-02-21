CREATE TABLE IF NOT EXISTS mock_apicode
    (api_code_id integer,
      api_code varchar(255),
      api_secret varchar(255),
      wallet_id integer UNIQUE,
    PRIMARY KEY (api_code_id))