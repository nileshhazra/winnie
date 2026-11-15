"""
SQL Engine for Winnie SQL Playground.
Provides in-memory SQLite database management with rich enterprise schemas,
query execution, EXPLAIN QUERY PLAN parsing, and logical order-of-execution pipeline analysis.
"""

import sqlite3
import time
import re
from typing import Dict, List, Any, Tuple, Optional


class QueryResult:
    def __init__(
        self,
        columns: List[str],
        rows: List[Tuple],
        row_count: int,
        execution_time_ms: float,
        error: Optional[str] = None,
        is_mutation: bool = False,
        rows_affected: int = 0
    ):
        self.columns = columns
        self.rows = rows
        self.row_count = row_count
        self.execution_time_ms = execution_time_ms
        self.error = error
        self.is_mutation = is_mutation
        self.rows_affected = rows_affected

    @property
    def is_success(self) -> bool:
        return self.error is None


class SqlEngine:
    """Manages an in-memory SQLite database instance with multiple enterprise schemas."""

    SCHEMAS = {
        "ecommerce": {
            "name": "E-Commerce & SaaS",
            "code": "ECOM",
            "description": "Customers, Products, Categories, Orders, Order Items, Subscriptions, Payments"
        },
        "tech_hr": {
            "name": "Tech Enterprise / HR",
            "code": "HR",
            "description": "Departments, Employees, Salaries History, Projects, Assignments, Reviews"
        },
        "fintech": {
            "name": "Fintech & Banking",
            "code": "FIN",
            "description": "Accounts, Cards, Merchants, Transactions, Fraud Alerts"
        }
    }

    def __init__(self, default_schema: str = "ecommerce"):
        self.current_schema = default_schema
        self.conn: Optional[sqlite3.Connection] = None
        self.load_schema(default_schema)

    def load_schema(self, schema_key: str):
        """Initializes a fresh in-memory database with the chosen enterprise schema."""
        if schema_key not in self.SCHEMAS:
            schema_key = "ecommerce"
        self.current_schema = schema_key

        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass

        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")

        if schema_key == "ecommerce":
            self._seed_ecommerce_schema()
        elif schema_key == "tech_hr":
            self._seed_tech_hr_schema()
        elif schema_key == "fintech":
            self._seed_fintech_schema()

    def reset_current_schema(self):
        """Resets the currently selected schema to pristine seed state."""
        self.load_schema(self.current_schema)

    # -------------------------------------------------------------------------
    # Query Execution & Plan Analysis
    # -------------------------------------------------------------------------

    def execute_query(self, sql_text: str) -> QueryResult:
        """Executes a single or multi-statement query and returns timing and results."""
        sql_clean = sql_text.strip()
        if not sql_clean:
            return QueryResult([], [], 0, 0.0, error="Empty query.")

        start_time = time.perf_counter()
        try:
            cursor = self.conn.cursor()
            
            # Check if it's a mutation query
            first_word = sql_clean.split()[0].upper() if sql_clean.split() else ""
            is_mutation = first_word in ("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER")

            cursor.execute(sql_clean)
            
            if is_mutation:
                rows_affected = cursor.rowcount
                self.conn.commit()
                elapsed = (time.perf_counter() - start_time) * 1000.0
                return QueryResult(
                    columns=["Status", "Rows Affected"],
                    rows=[("Query executed successfully.", rows_affected)],
                    row_count=1,
                    execution_time_ms=round(elapsed, 2),
                    is_mutation=True,
                    rows_affected=rows_affected
                )

            # SELECT / EXPLAIN query
            columns = [col[0] for col in cursor.description] if cursor.description else []
            rows = [tuple(row) for row in cursor.fetchall()]
            elapsed = (time.perf_counter() - start_time) * 1000.0

            return QueryResult(
                columns=columns,
                rows=rows,
                row_count=len(rows),
                execution_time_ms=round(elapsed, 2)
            )

        except Exception as e:
            elapsed = (time.perf_counter() - start_time) * 1000.0
            return QueryResult([], [], 0, round(elapsed, 2), error=str(e))

    def get_execution_plan(self, sql_text: str) -> List[Dict[str, Any]]:
        """
        Executes EXPLAIN QUERY PLAN and returns parsed nodes with human-friendly
        explanations and optimization flags (e.g. Scan vs Index Search).
        """
        sql_clean = sql_text.strip().rstrip(";")
        if not sql_clean:
            return []

        # Only SELECT/WITH queries can be explained
        explain_sql = f"EXPLAIN QUERY PLAN {sql_clean};"
        try:
            cursor = self.conn.cursor()
            cursor.execute(explain_sql)
            rows = cursor.fetchall()

            plan_nodes = []
            for row in rows:
                # SQLite returns (id, parent, notused, detail) or (selectid, order, from, detail)
                detail = row[-1]
                node_id = row[0]
                parent_id = row[1] if len(row) > 1 else 0

                # Analyze detail for educational insights
                classification = "OTHER"
                badge = "INFO"
                explanation = detail

                detail_upper = detail.upper()
                if "SCAN" in detail_upper:
                    classification = "SCAN"
                    badge = "FULL TABLE SCAN"
                    explanation = (
                        f"{detail} — Reads every single row in the table sequentially without an index. "
                        f"For large production tables, this is an O(N) operation and can cause query slowdowns."
                    )
                elif "SEARCH" in detail_upper and "USING INDEX" in detail_upper:
                    classification = "INDEX_SEARCH"
                    badge = "INDEX SEARCH"
                    explanation = (
                        f"{detail} — Efficiently uses a B-Tree index to pinpoint matching rows in O(log N) time, "
                        f"skipping irrelevant records."
                    )
                elif "SEARCH" in detail_upper and "USING COVERING INDEX" in detail_upper:
                    classification = "COVERING_INDEX"
                    badge = "COVERING INDEX"
                    explanation = (
                        f"{detail} — Optimal performance: All requested columns are found directly inside the index itself, "
                        f"completely avoiding table row lookups."
                    )
                elif "USE TEMP B-TREE" in detail_upper:
                    classification = "TEMP_BTREE"
                    badge = "TEMP B-TREE SORT"
                    explanation = (
                        f"{detail} — SQLite must allocate a temporary in-memory B-Tree to perform an ORDER BY, "
                        f"GROUP BY, or DISTINCT operation because no pre-sorted index is available."
                    )
                elif "COMPOUND QUERY" in detail_upper or "UNION" in detail_upper:
                    classification = "UNION"
                    badge = "COMPOUND QUERY"
                    explanation = f"{detail} — Combines results from multiple subqueries."

                plan_nodes.append({
                    "id": node_id,
                    "parent": parent_id,
                    "detail": detail,
                    "classification": classification,
                    "badge": badge,
                    "explanation": explanation
                })

            return plan_nodes

        except Exception as e:
            return [{
                "id": 0,
                "parent": 0,
                "detail": f"Could not generate query plan: {e}",
                "classification": "ERROR",
                "badge": "ERROR",
                "explanation": str(e)
            }]

    def get_logical_execution_steps(self, sql_text: str) -> List[Dict[str, str]]:
        """
        Deconstructs a SQL query into its procedural logical execution pipeline
        (FROM/JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT/WINDOW -> DISTINCT -> ORDER BY -> LIMIT).
        """
        sql_clean = " ".join(sql_text.split())
        steps = []

        # Standard relational logical sequence
        pipeline_stages = [
            ("WITH", r"\bWITH\b\s+(.+?)(?=\bSELECT\b|\bINSERT\b)", "1. CTE Definition (WITH)",
             "Evaluates Common Table Expressions into temporary named datasets before the main query starts."),
            
            ("FROM", r"\bFROM\b\s+(.+?)(?=\bWHERE\b|\bGROUP\s+BY\b|\bHAVING\b|\bWINDOW\b|\bORDER\s+BY\b|\bLIMIT\b|$)", "2. Data Sources (FROM & JOIN)",
             "Identifies tables, executes cartesian products, and applies ON join predicates to assemble the candidate row stream."),
            
            ("WHERE", r"\bWHERE\b\s+(.+?)(?=\bGROUP\s+BY\b|\bHAVING\b|\bWINDOW\b|\bORDER\s+BY\b|\bLIMIT\b|$)", "3. Row Filter (WHERE)",
             "Filters individual rows against predicates. Rows that evaluate to FALSE or NULL are discarded before any aggregation."),
            
            ("GROUP BY", r"\bGROUP\s+BY\b\s+(.+?)(?=\bHAVING\b|\bWINDOW\b|\bORDER\s+BY\b|\bLIMIT\b|$)", "4. Aggregation (GROUP BY)",
             "Buckets remaining rows into distinct groups based on grouping columns. Calculates aggregate metrics (COUNT, SUM, AVG, MAX)."),
            
            ("HAVING", r"\bHAVING\b\s+(.+?)(?=\bWINDOW\b|\bORDER\s+BY\b|\bLIMIT\b|$)", "5. Group Filter (HAVING)",
             "Filters whole groups based on aggregate results (e.g. HAVING COUNT(*) > 5). Unlike WHERE, this operates on grouped metrics."),
            
            ("SELECT", r"\bSELECT\b\s+(.+?)(?=\bFROM\b|$)", "6. Projection & Window Functions (SELECT)",
             "Evaluates output column expressions, assigns column aliases (AS), and calculates window functions (e.g. ROW_NUMBER, RANK, OVER)."),
            
            ("DISTINCT", r"\bSELECT\s+DISTINCT\b", "7. Deduplication (DISTINCT)",
             "Scans output rows and removes duplicate tuples so every row in the result set is unique."),
            
            ("ORDER BY", r"\bORDER\s+BY\b\s+(.+?)(?=\bLIMIT\b|$)", "8. Sorting (ORDER BY)",
             "Orders the projected result rows according to the specified columns or expressions (ASC or DESC)."),
            
            ("LIMIT", r"\bLIMIT\b\s+(.+)$", "9. Pagination & Slicing (LIMIT / OFFSET)",
             "Limits the final stream to the requested number of rows, optionally skipping the first N rows.")
        ]

        stage_num = 1
        for keyword, pattern, stage_title, description in pipeline_stages:
            match = re.search(pattern, sql_clean, re.IGNORECASE)
            if match or (keyword == "SELECT" and re.search(r"\bSELECT\b", sql_clean, re.IGNORECASE)):
                snippet = match.group(1).strip() if match and match.groups() else ""
                if len(snippet) > 80:
                    snippet = snippet[:77] + "..."
                
                steps.append({
                    "stage_num": stage_num,
                    "keyword": keyword,
                    "title": stage_title,
                    "description": description,
                    "snippet": snippet if snippet else "Active in query"
                })
                stage_num += 1

        return steps

    # -------------------------------------------------------------------------
    # Schema Metadata Inspection
    # -------------------------------------------------------------------------

    def get_schema_info(self) -> Dict[str, Any]:
        """Returns structured metadata for all tables, columns, PKs, and row counts."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
        tables = [row[0] for row in cursor.fetchall()]

        schema_data = {}
        for table in tables:
            # Columns info
            cursor.execute(f"PRAGMA table_info({table});")
            cols_info = cursor.fetchall()
            columns = []
            for col in cols_info:
                columns.append({
                    "cid": col[0],
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "dflt_value": col[4],
                    "pk": bool(col[5])
                })

            # Foreign keys info
            cursor.execute(f"PRAGMA foreign_key_list({table});")
            fk_info = cursor.fetchall()
            fkeys = []
            for fk in fk_info:
                fkeys.append({
                    "from": fk[3],
                    "to_table": fk[2],
                    "to_col": fk[4]
                })

            # Row count
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            row_count = cursor.fetchone()[0]

            schema_data[table] = {
                "columns": columns,
                "foreign_keys": fkeys,
                "row_count": row_count
            }

        return schema_data

    def get_sample_data(self, table_name: str, limit: int = 10) -> QueryResult:
        """Retrieves first N rows of a given table."""
        return self.execute_query(f"SELECT * FROM {table_name} LIMIT {limit};")

    # -------------------------------------------------------------------------
    # Seed Data Generators
    # -------------------------------------------------------------------------

    def _seed_ecommerce_schema(self):
        cur = self.conn.cursor()
        cur.executescript("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        );

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category_id INTEGER,
            price REAL NOT NULL,
            cost REAL NOT NULL,
            stock_quantity INTEGER NOT NULL,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        );

        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            country TEXT NOT NULL,
            segment TEXT NOT NULL,
            signup_date TEXT NOT NULL
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL,
            shipping_city TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        );

        CREATE TABLE order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            discount_pct REAL DEFAULT 0.0,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        );

        CREATE TABLE subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            plan_name TEXT NOT NULL,
            monthly_rate REAL NOT NULL,
            status TEXT NOT NULL,
            start_date TEXT NOT NULL,
            churn_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        );

        CREATE TABLE payments (
            payment_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            payment_date TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
        );

        -- Categories
        INSERT INTO categories VALUES (1, 'Cloud Storage', 'SaaS');
        INSERT INTO categories VALUES (2, 'Developer Tools', 'SaaS');
        INSERT INTO categories VALUES (3, 'Laptops & Hardware', 'Hardware');
        INSERT INTO categories VALUES (4, 'Accessories', 'Hardware');
        INSERT INTO categories VALUES (5, 'Office Furniture', 'Ergonomics');

        -- Products
        INSERT INTO products VALUES (101, 'MacBook Pro M3 14-inch', 3, 1999.00, 1450.00, 42, 1);
        INSERT INTO products VALUES (102, '4K Studio Monitor 27-inch', 3, 699.00, 450.00, 18, 1);
        INSERT INTO products VALUES (103, 'Mechanical Keyboard (Tactile)', 4, 149.00, 75.00, 120, 1);
        INSERT INTO products VALUES (104, 'Precision Wireless Mouse', 4, 89.00, 38.00, 85, 1);
        INSERT INTO products VALUES (105, 'Ergonomic Mesh Chair', 5, 599.00, 320.00, 14, 1);
        INSERT INTO products VALUES (106, 'Electric Standing Desk', 5, 749.00, 410.00, 9, 1);
        INSERT INTO products VALUES (107, 'Cloud Storage 2TB Annual', 1, 120.00, 20.00, 9999, 1);
        INSERT INTO products VALUES (108, 'DevPro Copilot Subscription', 2, 240.00, 35.00, 9999, 1);
        INSERT INTO products VALUES (109, 'Noise-Cancelling Headphones', 4, 349.00, 180.00, 60, 1);
        INSERT INTO products VALUES (110, 'USB-C Thunderbolt Dock 11-in-1', 4, 199.00, 95.00, 35, 1);

        -- Customers
        INSERT INTO customers VALUES (1, 'Alice', 'Chen', 'alice.chen@techcorp.io', 'USA', 'Enterprise', '2023-01-15');
        INSERT INTO customers VALUES (2, 'Bob', 'Martinez', 'bob.m@startuplabs.co', 'USA', 'SMB', '2023-02-20');
        INSERT INTO customers VALUES (3, 'Clara', 'Schmidt', 'c.schmidt@berlin-ai.de', 'Germany', 'Enterprise', '2023-03-10');
        INSERT INTO customers VALUES (4, 'David', 'Kim', 'david.kim@seoul-fin.kr', 'South Korea', 'Consumer', '2023-04-05');
        INSERT INTO customers VALUES (5, 'Elena', 'Rostova', 'elena@nordicdesign.se', 'Sweden', 'SMB', '2023-04-18');
        INSERT INTO customers VALUES (6, 'Frank', 'O''Connor', 'frank@dublinpay.ie', 'Ireland', 'Enterprise', '2023-05-12');
        INSERT INTO customers VALUES (7, 'Grace', 'Hopper', 'grace@computing.org', 'USA', 'Enterprise', '2023-06-01');
        INSERT INTO customers VALUES (8, 'Hiroshi', 'Tanaka', 'tanaka@tokyodev.jp', 'Japan', 'SMB', '2023-06-22');
        INSERT INTO customers VALUES (9, 'Isabella', 'Silva', 'isabella@saopaulo.br', 'Brazil', 'Consumer', '2023-07-08');
        INSERT INTO customers VALUES (10, 'Liam', 'Wilson', 'liam.w@londonvc.co.uk', 'UK', 'Enterprise', '2023-08-14');

        -- Orders
        INSERT INTO orders VALUES (1001, 1, '2023-09-01', 'completed', 2847.00, 'San Francisco');
        INSERT INTO orders VALUES (1002, 2, '2023-09-05', 'completed', 238.00, 'Austin');
        INSERT INTO orders VALUES (1003, 3, '2023-09-12', 'completed', 1999.00, 'Berlin');
        INSERT INTO orders VALUES (1004, 4, '2023-09-18', 'cancelled', 349.00, 'Seoul');
        INSERT INTO orders VALUES (1005, 5, '2023-09-25', 'completed', 1348.00, 'Stockholm');
        INSERT INTO orders VALUES (1006, 1, '2023-10-02', 'completed', 749.00, 'San Francisco');
        INSERT INTO orders VALUES (1007, 7, '2023-10-10', 'completed', 4545.00, 'New York');
        INSERT INTO orders VALUES (1008, 6, '2023-10-15', 'refunded', 699.00, 'Dublin');
        INSERT INTO orders VALUES (1009, 8, '2023-10-21', 'completed', 238.00, 'Tokyo');
        INSERT INTO orders VALUES (1010, 10, '2023-11-04', 'completed', 3897.00, 'London');

        -- Order Items
        INSERT INTO order_items VALUES (1, 1001, 101, 1, 1999.00, 0.0);
        INSERT INTO order_items VALUES (2, 1001, 102, 1, 699.00, 0.0);
        INSERT INTO order_items VALUES (3, 1001, 103, 1, 149.00, 0.0);
        INSERT INTO order_items VALUES (4, 1002, 103, 1, 149.00, 0.0);
        INSERT INTO order_items VALUES (5, 1002, 104, 1, 89.00, 0.0);
        INSERT INTO order_items VALUES (6, 1003, 101, 1, 1999.00, 0.0);
        INSERT INTO order_items VALUES (7, 1004, 109, 1, 349.00, 0.0);
        INSERT INTO order_items VALUES (8, 1005, 105, 1, 599.00, 0.0);
        INSERT INTO order_items VALUES (9, 1005, 106, 1, 749.00, 0.0);
        INSERT INTO order_items VALUES (10, 1006, 106, 1, 749.00, 0.0);
        INSERT INTO order_items VALUES (11, 1007, 101, 2, 1999.00, 0.05);
        INSERT INTO order_items VALUES (12, 1007, 105, 1, 599.00, 0.10);
        INSERT INTO order_items VALUES (13, 1008, 102, 1, 699.00, 0.0);
        INSERT INTO order_items VALUES (14, 1009, 103, 1, 149.00, 0.0);
        INSERT INTO order_items VALUES (15, 1009, 104, 1, 89.00, 0.0);
        INSERT INTO order_items VALUES (16, 1010, 101, 1, 1999.00, 0.0);
        INSERT INTO order_items VALUES (17, 1010, 106, 1, 749.00, 0.0);
        INSERT INTO order_items VALUES (18, 1010, 102, 1, 699.00, 0.0);
        INSERT INTO order_items VALUES (19, 1010, 110, 2, 199.00, 0.0);

        -- Subscriptions
        INSERT INTO subscriptions VALUES (501, 1, 'Enterprise AI Copilot', 499.00, 'active', '2023-02-01', NULL);
        INSERT INTO subscriptions VALUES (502, 2, 'Pro Starter Cloud', 49.00, 'active', '2023-03-01', NULL);
        INSERT INTO subscriptions VALUES (503, 3, 'Enterprise AI Copilot', 499.00, 'active', '2023-03-15', NULL);
        INSERT INTO subscriptions VALUES (504, 4, 'Pro Starter Cloud', 49.00, 'churned', '2023-04-10', '2023-08-10');
        INSERT INTO subscriptions VALUES (505, 5, 'Team Growth Suite', 199.00, 'active', '2023-05-01', NULL);
        INSERT INTO subscriptions VALUES (506, 6, 'Enterprise AI Copilot', 499.00, 'active', '2023-06-01', NULL);
        INSERT INTO subscriptions VALUES (507, 7, 'Enterprise AI Copilot', 499.00, 'active', '2023-06-15', NULL);
        INSERT INTO subscriptions VALUES (508, 8, 'Team Growth Suite', 199.00, 'paused', '2023-07-01', NULL);
        INSERT INTO subscriptions VALUES (509, 9, 'Pro Starter Cloud', 49.00, 'churned', '2023-07-15', '2023-10-15');
        INSERT INTO subscriptions VALUES (510, 10, 'Enterprise AI Copilot', 499.00, 'active', '2023-08-20', NULL);

        -- Payments
        INSERT INTO payments VALUES (7001, 1001, '2023-09-01', 'Credit Card', 2847.00, 'settled');
        INSERT INTO payments VALUES (7002, 1002, '2023-09-05', 'Apple Pay', 238.00, 'settled');
        INSERT INTO payments VALUES (7003, 1003, '2023-09-12', 'Bank Wire', 1999.00, 'settled');
        INSERT INTO payments VALUES (7004, 1005, '2023-09-25', 'Credit Card', 1348.00, 'settled');
        INSERT INTO payments VALUES (7005, 1006, '2023-10-02', 'Credit Card', 749.00, 'settled');
        INSERT INTO payments VALUES (7006, 1007, '2023-10-10', 'Corporate Invoice', 4545.00, 'settled');
        INSERT INTO payments VALUES (7007, 1008, '2023-10-15', 'Apple Pay', 699.00, 'refunded');
        INSERT INTO payments VALUES (7008, 1009, '2023-10-21', 'Credit Card', 238.00, 'settled');
        INSERT INTO payments VALUES (7009, 1010, '2023-11-04', 'Corporate Invoice', 3897.00, 'settled');
        """)
        self.conn.commit()

    def _seed_tech_hr_schema(self):
        cur = self.conn.cursor()
        cur.executescript("""
        CREATE TABLE departments (
            dept_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            budget REAL NOT NULL,
            building TEXT NOT NULL,
            manager_id INTEGER
        );

        CREATE TABLE employees (
            emp_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            dept_id INTEGER,
            job_title TEXT NOT NULL,
            hire_date TEXT NOT NULL,
            salary REAL NOT NULL,
            manager_id INTEGER,
            FOREIGN KEY (dept_id) REFERENCES departments (dept_id),
            FOREIGN KEY (manager_id) REFERENCES employees (emp_id)
        );

        CREATE TABLE salaries_history (
            history_id INTEGER PRIMARY KEY,
            emp_id INTEGER NOT NULL,
            effective_date TEXT NOT NULL,
            salary REAL NOT NULL,
            change_reason TEXT NOT NULL,
            FOREIGN KEY (emp_id) REFERENCES employees (emp_id)
        );

        CREATE TABLE projects (
            project_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            budget REAL NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT,
            priority TEXT NOT NULL
        );

        CREATE TABLE project_assignments (
            assignment_id INTEGER PRIMARY KEY,
            project_id INTEGER NOT NULL,
            emp_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            hours_per_week INTEGER NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects (project_id),
            FOREIGN KEY (emp_id) REFERENCES employees (emp_id)
        );

        CREATE TABLE performance_reviews (
            review_id INTEGER PRIMARY KEY,
            emp_id INTEGER NOT NULL,
            review_year INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            reviewer_id INTEGER NOT NULL,
            summary TEXT,
            FOREIGN KEY (emp_id) REFERENCES employees (emp_id),
            FOREIGN KEY (reviewer_id) REFERENCES employees (emp_id)
        );

        -- Departments
        INSERT INTO departments VALUES (10, 'Core Infrastructure', 2500000.00, 'Building A - Floor 4', 1);
        INSERT INTO departments VALUES (20, 'Product Engineering', 3200000.00, 'Building A - Floor 3', 2);
        INSERT INTO departments VALUES (30, 'Data & Machine Learning', 2800000.00, 'Building B - Floor 2', 3);
        INSERT INTO departments VALUES (40, 'Product Design & UX', 1100000.00, 'Building B - Floor 1', 4);
        INSERT INTO departments VALUES (50, 'Enterprise Sales', 2100000.00, 'Building C - Floor 5', 5);

        -- Employees (with management hierarchy)
        -- VPs & Directors
        INSERT INTO employees VALUES (1, 'Sarah Connor', 'sarah.c@corp.com', 10, 'VP of Infrastructure', '2019-03-01', 245000.00, NULL);
        INSERT INTO employees VALUES (2, 'Alex Mercer', 'alex.m@corp.com', 20, 'VP of Engineering', '2019-06-15', 240000.00, NULL);
        INSERT INTO employees VALUES (3, 'Dr. Raj Patel', 'raj.p@corp.com', 30, 'Head of AI Research', '2020-01-10', 260000.00, NULL);
        INSERT INTO employees VALUES (4, 'Emma Watson', 'emma.w@corp.com', 40, 'Director of Design', '2020-05-18', 195000.00, NULL);
        INSERT INTO employees VALUES (5, 'Marcus Sterling', 'marcus.s@corp.com', 50, 'VP of Global Sales', '2019-11-01', 220000.00, NULL);

        -- Staff & Senior Engineers
        INSERT INTO employees VALUES (6, 'John Doe', 'john.d@corp.com', 10, 'Staff SRE Engineer', '2020-08-01', 185000.00, 1);
        INSERT INTO employees VALUES (7, 'Priya Sharma', 'priya.s@corp.com', 20, 'Staff Software Engineer', '2021-02-15', 180000.00, 2);
        INSERT INTO employees VALUES (8, 'Lucas Silva', 'lucas.s@corp.com', 20, 'Senior Frontend Engineer', '2021-04-10', 155000.00, 7);
        INSERT INTO employees VALUES (9, 'Chloe Bennett', 'chloe.b@corp.com', 20, 'Backend Engineer II', '2022-01-20', 135000.00, 7);
        INSERT INTO employees VALUES (10, 'Michael Chang', 'michael.c@corp.com', 30, 'Staff ML Scientist', '2021-07-01', 195000.00, 3);
        INSERT INTO employees VALUES (11, 'Fatima Al-Mansoor', 'fatima.a@corp.com', 30, 'Data Engineer', '2022-03-15', 145000.00, 10);
        INSERT INTO employees VALUES (12, 'Leo Dubois', 'leo.d@corp.com', 40, 'Senior Product Designer', '2021-09-01', 140000.00, 4);
        INSERT INTO employees VALUES (13, 'Jessica Taylor', 'jessica.t@corp.com', 50, 'Enterprise Account Exec', '2021-11-15', 130000.00, 5);
        INSERT INTO employees VALUES (14, 'Kevin O''Neal', 'kevin.o@corp.com', 10, 'Cloud Security Architect', '2022-06-01', 175000.00, 1);
        INSERT INTO employees VALUES (15, 'Daniel Kim', 'daniel.k@corp.com', 20, 'Junior Software Engineer', '2023-03-01', 105000.00, 7);

        -- Salary Progression
        INSERT INTO salaries_history VALUES (1, 6, '2020-08-01', 160000.00, 'Hire');
        INSERT INTO salaries_history VALUES (2, 6, '2022-08-01', 185000.00, 'Promotion to Staff');
        INSERT INTO salaries_history VALUES (3, 7, '2021-02-15', 155000.00, 'Hire');
        INSERT INTO salaries_history VALUES (4, 7, '2023-02-15', 180000.00, 'Annual Merit Promotion');
        INSERT INTO salaries_history VALUES (5, 8, '2021-04-10', 135000.00, 'Hire');
        INSERT INTO salaries_history VALUES (6, 8, '2022-10-01', 155000.00, 'Promotion to Senior');

        -- Projects
        INSERT INTO projects VALUES (101, 'Kubernetes Multi-Region Mesh', 650000.00, '2023-01-15', '2023-12-31', 'High');
        INSERT INTO projects VALUES (102, 'NextGen Enterprise UI System', 450000.00, '2023-03-01', '2023-10-31', 'High');
        INSERT INTO projects VALUES (103, 'LLM Customer Support Co-pilot', 850000.00, '2023-02-01', '2024-04-30', 'Critical');
        INSERT INTO projects VALUES (104, 'SOC-2 Compliance & Zero Trust', 300000.00, '2023-05-01', '2023-11-30', 'Medium');

        -- Project Assignments
        INSERT INTO project_assignments VALUES (1, 101, 6, 'Tech Lead', 30);
        INSERT INTO project_assignments VALUES (2, 101, 14, 'Security Lead', 20);
        INSERT INTO project_assignments VALUES (3, 102, 7, 'Backend Lead', 25);
        INSERT INTO project_assignments VALUES (4, 102, 8, 'Frontend Lead', 35);
        INSERT INTO project_assignments VALUES (5, 102, 12, 'Lead UX Designer', 30);
        INSERT INTO project_assignments VALUES (6, 103, 10, 'Principal AI Lead', 35);
        INSERT INTO project_assignments VALUES (7, 103, 11, 'Data Pipeline Eng', 30);
        INSERT INTO project_assignments VALUES (8, 103, 9, 'API Integrator', 20);

        -- Performance Reviews
        INSERT INTO performance_reviews VALUES (1, 6, 2022, 5, 1, 'Exceeded expectations leading cloud migration.');
        INSERT INTO performance_reviews VALUES (2, 7, 2022, 5, 2, 'Exceptional architecture design and mentoring junior engineers.');
        INSERT INTO performance_reviews VALUES (3, 8, 2022, 4, 7, 'Delivered frontend refresh ahead of schedule.');
        INSERT INTO performance_reviews VALUES (4, 9, 2022, 4, 7, 'Strong backend contribution, great test coverage.');
        INSERT INTO performance_reviews VALUES (5, 10, 2022, 5, 3, 'Pioneered core LLM pipeline resulting in 3x throughput.');
        INSERT INTO performance_reviews VALUES (6, 12, 2022, 4, 4, 'Modern design system adopted across 8 squads.');
        """)
        self.conn.commit()

    def _seed_fintech_schema(self):
        cur = self.conn.cursor()
        cur.executescript("""
        CREATE TABLE accounts (
            account_id INTEGER PRIMARY KEY,
            account_number TEXT UNIQUE NOT NULL,
            account_type TEXT NOT NULL,
            currency TEXT NOT NULL DEFAULT 'USD',
            balance REAL NOT NULL,
            status TEXT NOT NULL,
            opened_at TEXT NOT NULL
        );

        CREATE TABLE cards (
            card_id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,
            card_last4 TEXT NOT NULL,
            card_type TEXT NOT NULL,
            exp_month INTEGER NOT NULL,
            exp_year INTEGER NOT NULL,
            is_virtual INTEGER DEFAULT 0,
            is_blocked INTEGER DEFAULT 0,
            FOREIGN KEY (account_id) REFERENCES accounts (account_id)
        );

        CREATE TABLE merchants (
            merchant_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            mcc_code INTEGER NOT NULL,
            country TEXT NOT NULL
        );

        CREATE TABLE transactions (
            txn_id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,
            card_id INTEGER,
            merchant_id INTEGER,
            amount REAL NOT NULL,
            currency TEXT NOT NULL DEFAULT 'USD',
            txn_type TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (account_id) REFERENCES accounts (account_id),
            FOREIGN KEY (card_id) REFERENCES cards (card_id),
            FOREIGN KEY (merchant_id) REFERENCES merchants (merchant_id)
        );

        CREATE TABLE fraud_alerts (
            alert_id INTEGER PRIMARY KEY,
            txn_id INTEGER NOT NULL,
            risk_score REAL NOT NULL,
            trigger_reason TEXT NOT NULL,
            status TEXT NOT NULL,
            reviewed_at TEXT,
            FOREIGN KEY (txn_id) REFERENCES transactions (txn_id)
        );

        -- Accounts
        INSERT INTO accounts VALUES (1, 'ACCT-88901', 'Checking', 'USD', 24150.75, 'active', '2021-01-10');
        INSERT INTO accounts VALUES (2, 'ACCT-88902', 'High-Yield Savings', 'USD', 145000.00, 'active', '2021-03-15');
        INSERT INTO accounts VALUES (3, 'ACCT-99201', 'Commercial Business', 'USD', 892400.50, 'active', '2021-06-01');
        INSERT INTO accounts VALUES (4, 'ACCT-33401', 'EUR Treasury', 'EUR', 320150.00, 'active', '2022-02-14');
        INSERT INTO accounts VALUES (5, 'ACCT-44102', 'Personal Checking', 'USD', 3420.20, 'active', '2022-08-20');

        -- Cards
        INSERT INTO cards VALUES (101, 1, '4412', 'Debit', 12, 2027, 0, 0);
        INSERT INTO cards VALUES (102, 1, '8890', 'Virtual Multi-Use', 6, 2026, 1, 0);
        INSERT INTO cards VALUES (103, 3, '1194', 'Corporate Credit', 9, 2028, 0, 0);
        INSERT INTO cards VALUES (104, 5, '7712', 'Debit', 11, 2025, 0, 1);

        -- Merchants
        INSERT INTO merchants VALUES (201, 'Amazon Web Services', 'Cloud Infrastructure', 7372, 'USA');
        INSERT INTO merchants VALUES (202, 'Apple Store 5th Ave', 'Electronics', 5732, 'USA');
        INSERT INTO merchants VALUES (203, 'GitHub Enterprise', 'Software', 7372, 'USA');
        INSERT INTO merchants VALUES (204, 'Delta Air Lines', 'Travel & Flights', 3058, 'USA');
        INSERT INTO merchants VALUES (205, 'Whole Foods Market', 'Groceries', 5411, 'USA');
        INSERT INTO merchants VALUES (206, 'Uber Technologies', 'Transportation', 4121, 'USA');

        -- Transactions
        INSERT INTO transactions VALUES (10001, 1, 101, 205, 142.50, 'USD', 'POS_PURCHASE', 'settled', '2023-10-01 12:30:15');
        INSERT INTO transactions VALUES (10002, 1, 101, 206, 28.40, 'USD', 'ONLINE_PURCHASE', 'settled', '2023-10-02 08:45:00');
        INSERT INTO transactions VALUES (10003, 3, 103, 201, 14850.00, 'USD', 'AUTO_SUBSCRIPTION', 'settled', '2023-10-03 00:00:01');
        INSERT INTO transactions VALUES (10004, 3, 103, 203, 2400.00, 'USD', 'ONLINE_PURCHASE', 'settled', '2023-10-04 14:15:22');
        INSERT INTO transactions VALUES (10005, 1, 102, 202, 2399.00, 'USD', 'ONLINE_PURCHASE', 'settled', '2023-10-05 16:20:00');
        INSERT INTO transactions VALUES (10006, 5, 104, 204, 850.00, 'USD', 'CARD_PRESENT', 'declined', '2023-10-06 18:00:10');
        INSERT INTO transactions VALUES (10007, 3, 103, 204, 1890.00, 'USD', 'ONLINE_PURCHASE', 'settled', '2023-10-07 10:10:05');
        INSERT INTO transactions VALUES (10008, 1, NULL, NULL, 5000.00, 'USD', 'WIRE_TRANSFER', 'settled', '2023-10-08 09:00:00');

        -- Fraud Alerts
        INSERT INTO fraud_alerts VALUES (1, 10006, 0.94, 'Card blocked; unusual location velocity mismatch', 'confirmed_fraud', '2023-10-06 18:05:00');
        INSERT INTO fraud_alerts VALUES (2, 10005, 0.68, 'High single transaction amount on newly created virtual card', 'false_positive_cleared', '2023-10-05 16:25:00');
        """)
        self.conn.commit()
