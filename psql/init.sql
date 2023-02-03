CREATE EXTENSION plpython3u;
CREATE FUNCTION domain_of_url(url text)
  RETURNS TEXT
AS $$
  global url
  return url.split("//")[1].split('/')[0]
$$ LANGUAGE SQL;