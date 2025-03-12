# Go-Postgres

This project is simple CRUD application built in golang and using PostgreSQL as DB.

## Pre-requisite
1. Install golang v1.11 or above.
2. Basic understanding of the golang syntax.
3. Basic understanding of SQL query.
4. Code Editor - VS Code 
5. Postman for testing APIs
  
## PostgreSQL Table

```sql
CREATE TABLE users (
  userid SERIAL PRIMARY KEY,
  name TEXT,
  age INT,
  location TEXT
);
```

