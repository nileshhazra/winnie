"""
Step-by-Step Enterprise SQL Learning Plan / Curriculum for Winnie SQL Playground.
Covers fundamental to advanced analytical SQL with modular step-by-step topics,
enterprise explanations, and executable code examples ready to copy/load into the editor.
"""

from typing import List, Dict, Any

SQL_CURRICULUM: List[Dict[str, Any]] = [
    # =========================================================================
    # MODULE 1: FOUNDATIONS & FILTERING
    # =========================================================================
    {
        "id": "sql_101",
        "module": "1. Foundations & Filtering",
        "title": "1.1 Column Projection & Computed Aliases",
        "schema": "ecommerce",
        "summary": "Retrieve specific columns and compute dynamic fields using arithmetic expressions and column aliases.",
        "takeaway": "Selecting only the necessary columns reduces network transfer and memory overhead. Use AS to give computed expressions meaningful names.",
        "code_example": (
            "-- Select specific columns and compute gross margin per unit\n"
            "SELECT \n"
            "  name AS product_name,\n"
            "  price,\n"
            "  cost,\n"
            "  ROUND(price - cost, 2) AS profit_per_unit,\n"
            "  ROUND(((price - cost) / price) * 100, 1) AS margin_percentage\n"
            "FROM products\n"
            "LIMIT 10;\n"
        )
    },
    {
        "id": "sql_102",
        "module": "1. Foundations & Filtering",
        "title": "1.2 Row Filtering with WHERE & Predicates",
        "schema": "ecommerce",
        "summary": "Filter candidate rows before aggregation using WHERE conditions and logical operators (AND, OR, BETWEEN, IN).",
        "takeaway": "The WHERE clause executes at Stage 2 of the relational engine. Rows not matching the predicates are discarded immediately.",
        "code_example": (
            "-- Find completed orders from USA or Germany with order value >= 1000\n"
            "SELECT \n"
            "  c.first_name || ' ' || c.last_name AS customer_name,\n"
            "  c.country,\n"
            "  o.order_id,\n"
            "  o.order_date,\n"
            "  o.total_amount\n"
            "FROM orders o\n"
            "JOIN customers c ON o.customer_id = c.customer_id\n"
            "WHERE o.status = 'completed'\n"
            "  AND c.country IN ('USA', 'Germany')\n"
            "  AND o.total_amount >= 1000.00;\n"
        )
    },
    {
        "id": "sql_103",
        "module": "1. Foundations & Filtering",
        "title": "1.3 Pattern Matching (LIKE) & Null Safety (COALESCE)",
        "schema": "ecommerce",
        "summary": "Match string patterns using wildcards (% and _) and handle missing/null data safely using COALESCE.",
        "takeaway": "In SQL, NULL compared with any value (e.g. col = NULL) yields UNKNOWN, never TRUE. Always use IS NULL or COALESCE.",
        "code_example": (
            "-- Inspect subscription lifecycle and replace null churn dates\n"
            "SELECT \n"
            "  subscription_id,\n"
            "  plan_name,\n"
            "  status,\n"
            "  start_date,\n"
            "  COALESCE(churn_date, 'Active Today') AS end_or_active_status\n"
            "FROM subscriptions\n"
            "WHERE plan_name LIKE '%Copilot%'\n"
            "   OR plan_name LIKE '%Enterprise%';\n"
        )
    },
    {
        "id": "sql_104",
        "module": "1. Foundations & Filtering",
        "title": "1.4 Sorting with ORDER BY & Pagination with LIMIT",
        "schema": "tech_hr",
        "summary": "Sort rows ascending (ASC) or descending (DESC), and implement pagination using LIMIT and OFFSET.",
        "takeaway": "ORDER BY executes at Stage 8 of query processing. If no pre-sorted index exists, the engine allocates a temporary in-memory B-Tree.",
        "code_example": (
            "-- Top 5 highest earning employees in the company\n"
            "SELECT \n"
            "  name,\n"
            "  job_title,\n"
            "  salary,\n"
            "  hire_date\n"
            "FROM employees\n"
            "ORDER BY salary DESC\n"
            "LIMIT 5 OFFSET 0;\n"
        )
    },

    # =========================================================================
    # MODULE 2: AGGREGATIONS & GROUPING
    # =========================================================================
    {
        "id": "sql_201",
        "module": "2. Aggregations & Grouping",
        "title": "2.1 Essential Aggregate Functions",
        "summary": "Compute summary statistics across rows: COUNT, SUM, AVG, MIN, and MAX.",
        "schema": "ecommerce",
        "takeaway": "COUNT(*) counts total rows including nulls, while COUNT(col) only counts non-null values.",
        "code_example": (
            "-- High-level product catalog financial metrics\n"
            "SELECT \n"
            "  COUNT(*) AS total_skus,\n"
            "  ROUND(MIN(price), 2) AS min_price,\n"
            "  ROUND(AVG(price), 2) AS avg_price,\n"
            "  ROUND(MAX(price), 2) AS max_price,\n"
            "  ROUND(SUM(price * stock_quantity), 2) AS total_inventory_value\n"
            "FROM products\n"
            "WHERE is_active = 1;\n"
        )
    },
    {
        "id": "sql_202",
        "module": "2. Aggregations & Grouping",
        "title": "2.2 Multi-Column GROUP BY Aggregations",
        "summary": "Collapse multiple rows into summary buckets according to one or more grouping keys.",
        "schema": "ecommerce",
        "takeaway": "Every non-aggregated column appearing in the SELECT list MUST be included in the GROUP BY clause.",
        "code_example": (
            "-- Revenue breakdown grouped by Category and Department\n"
            "SELECT \n"
            "  c.department,\n"
            "  c.name AS category_name,\n"
            "  COUNT(p.product_id) AS sku_count,\n"
            "  ROUND(AVG(p.price), 2) AS avg_price\n"
            "FROM categories c\n"
            "JOIN products p ON c.category_id = p.category_id\n"
            "GROUP BY c.department, c.name\n"
            "ORDER BY c.department, avg_price DESC;\n"
        )
    },
    {
        "id": "sql_203",
        "module": "2. Aggregations & Grouping",
        "title": "2.3 Post-Aggregation Group Filtering (HAVING vs WHERE)",
        "summary": "Use HAVING to filter aggregated groups after grouping has occurred.",
        "takeaway": "Rule of thumb: WHERE filters individual rows before aggregation; HAVING filters entire groups after aggregation.",
        "code_example": (
            "-- Find customer segments where completed order count > 1\n"
            "SELECT \n"
            "  c.segment,\n"
            "  COUNT(o.order_id) AS total_orders,\n"
            "  ROUND(SUM(o.total_amount), 2) AS total_spend,\n"
            "  ROUND(AVG(o.total_amount), 2) AS avg_order_value\n"
            "FROM customers c\n"
            "JOIN orders o ON c.customer_id = o.customer_id\n"
            "WHERE o.status = 'completed'\n"
            "GROUP BY c.segment\n"
            "HAVING COUNT(o.order_id) > 1\n"
            "ORDER BY total_spend DESC;\n"
        )
    },

    # =========================================================================
    # MODULE 3: RELATIONAL JOINS
    # =========================================================================
    {
        "id": "sql_301",
        "module": "3. Relational Joins",
        "title": "3.1 INNER JOIN Across Related Entities",
        "summary": "Join two tables based on matching foreign key relationships, returning only matching rows.",
        "takeaway": "Indexes on foreign key columns allow the engine to perform lightning-fast B-Tree lookups rather than full nested scans.",
        "code_example": (
            "-- Join orders to customers to inspect who made each order\n"
            "SELECT \n"
            "  o.order_id,\n"
            "  o.order_date,\n"
            "  c.first_name || ' ' || c.last_name AS customer_name,\n"
            "  c.email,\n"
            "  o.total_amount,\n"
            "  o.status\n"
            "FROM orders o\n"
            "INNER JOIN customers c ON o.customer_id = c.customer_id\n"
            "ORDER BY o.order_date DESC;\n"
        )
    },
    {
        "id": "sql_302",
        "module": "3. Relational Joins",
        "title": "3.2 LEFT JOIN for Preserving Base Records",
        "summary": "Retain all rows from the left table even when there are no matching rows in the right table.",
        "takeaway": "Use LEFT JOIN when calculating totals where entities might have zero activity (e.g. departments without employees).",
        "code_example": (
            "-- Department headcount and payroll, preserving empty departments\n"
            "SELECT \n"
            "  d.name AS department_name,\n"
            "  d.building,\n"
            "  COUNT(e.emp_id) AS headcount,\n"
            "  COALESCE(SUM(e.salary), 0) AS total_payroll\n"
            "FROM departments d\n"
            "LEFT JOIN employees e ON d.dept_id = e.dept_id\n"
            "GROUP BY d.dept_id\n"
            "ORDER BY total_payroll DESC;\n"
        )
    },
    {
        "id": "sql_303",
        "module": "3. Relational Joins",
        "title": "3.3 Multi-Table Joins & Order Line Items",
        "summary": "Traverse through associative junction tables to join 3 or more entities.",
        "takeaway": "Order of joins in the query can be rearranged by the query optimizer to minimize the intermediate row set size.",
        "code_example": (
            "-- Detailed invoice line items joining orders, line items, and products\n"
            "SELECT \n"
            "  oi.order_id,\n"
            "  p.name AS product_name,\n"
            "  oi.quantity,\n"
            "  oi.unit_price,\n"
            "  ROUND(oi.quantity * oi.unit_price, 2) AS line_total\n"
            "FROM order_items oi\n"
            "JOIN products p ON oi.product_id = p.product_id\n"
            "ORDER BY oi.order_id, line_total DESC;\n"
        )
    },
    {
        "id": "sql_304",
        "module": "3. Relational Joins",
        "title": "3.4 Self-Joins for Hierarchical Data",
        "summary": "Join a table to itself to resolve recursive parent-child relationships (e.g. Employee to Manager).",
        "takeaway": "Always use unique table aliases (e.g. e for employee, m for manager) to disambiguate identical column names.",
        "code_example": (
            "-- Employee management tree resolving manager names\n"
            "SELECT \n"
            "  e.name AS employee_name,\n"
            "  e.job_title,\n"
            "  COALESCE(m.name, 'Executive Board / CEO') AS manager_name,\n"
            "  COALESCE(m.job_title, 'N/A') AS manager_title\n"
            "FROM employees e\n"
            "LEFT JOIN employees m ON e.manager_id = m.emp_id\n"
            "ORDER BY m.name NULLS FIRST, e.name;\n"
        )
    },

    # =========================================================================
    # MODULE 4: CONDITIONALS & SUBQUERIES
    # =========================================================================
    {
        "id": "sql_401",
        "module": "4. Conditionals & Subqueries",
        "title": "4.1 Conditional Classification with CASE WHEN",
        "summary": "Implement if-then-else logic directly inside SQL SELECT and aggregation expressions.",
        "takeaway": "CASE expressions evaluate sequentially. The first branch with a matching condition determines the output value.",
        "code_example": (
            "-- Categorize employees into compensation bands\n"
            "SELECT \n"
            "  name,\n"
            "  job_title,\n"
            "  salary,\n"
            "  CASE \n"
            "    WHEN salary >= 200000 THEN 'Tier 1: Executive'\n"
            "    WHEN salary >= 150000 THEN 'Tier 2: Staff / Senior'\n"
            "    WHEN salary >= 120000 THEN 'Tier 3: Mid-Level'\n"
            "    ELSE 'Tier 4: Associate'\n"
            "  END AS compensation_band\n"
            "FROM employees\n"
            "ORDER BY salary DESC;\n"
        )
    },
    {
        "id": "sql_402",
        "module": "4. Conditionals & Subqueries",
        "title": "4.2 Subqueries & Row Comparison",
        "summary": "Embed a subquery inside a WHERE or HAVING clause to compare against dynamically calculated metrics.",
        "takeaway": "A non-correlated subquery executes once, caching its result for the outer query.",
        "code_example": (
            "-- Find employees whose salary is above the overall company average\n"
            "SELECT \n"
            "  name,\n"
            "  job_title,\n"
            "  salary,\n"
            "  ROUND((SELECT AVG(salary) FROM employees), 2) AS company_avg_salary\n"
            "FROM employees\n"
            "WHERE salary > (SELECT AVG(salary) FROM employees)\n"
            "ORDER BY salary DESC;\n"
        )
    },

    # =========================================================================
    # MODULE 5: COMMON TABLE EXPRESSIONS (CTEs)
    # =========================================================================
    {
        "id": "sql_501",
        "module": "5. Common Table Expressions (CTEs)",
        "title": "5.1 Modular Pipelines with WITH Clause",
        "summary": "Define temporary named result sets using WITH to write cleaner, more readable queries than nested subqueries.",
        "takeaway": "CTEs improve readability and maintainability. In modern engines, CTEs can be inlined or materialized as temporary views.",
        "code_example": (
            "-- Department salary benchmarks using a clean CTE\n"
            "WITH department_metrics AS (\n"
            "  SELECT \n"
            "    dept_id,\n"
            "    ROUND(AVG(salary), 2) AS avg_dept_salary,\n"
            "    MAX(salary) AS max_dept_salary\n"
            "  FROM employees\n"
            "  GROUP BY dept_id\n"
            ")\n"
            "SELECT \n"
            "  e.name AS employee_name,\n"
            "  d.name AS department_name,\n"
            "  e.salary,\n"
            "  dm.avg_dept_salary,\n"
            "  e.salary - dm.avg_dept_salary AS delta_from_avg\n"
            "FROM employees e\n"
            "JOIN departments d ON e.dept_id = d.dept_id\n"
            "JOIN department_metrics dm ON e.dept_id = dm.dept_id\n"
            "ORDER BY delta_from_avg DESC;\n"
        )
    },
    {
        "id": "sql_502",
        "module": "5. Common Table Expressions (CTEs)",
        "title": "5.2 Multi-Stage Chained CTEs",
        "summary": "Chain multiple CTEs in series to model sequential ETL data transformations.",
        "takeaway": "Separate complex queries into logical steps: extraction -> aggregation -> final filtering and reporting.",
        "code_example": (
            "-- 2-Stage pipeline: Customer spend -> Segment averages\n"
            "WITH customer_spend AS (\n"
            "  SELECT \n"
            "    customer_id,\n"
            "    COUNT(order_id) AS order_count,\n"
            "    SUM(total_amount) AS total_spend\n"
            "  FROM orders\n"
            "  WHERE status = 'completed'\n"
            "  GROUP BY customer_id\n"
            "),\n"
            "spend_with_profiles AS (\n"
            "  SELECT \n"
            "    c.segment,\n"
            "    c.country,\n"
            "    cs.total_spend\n"
            "  FROM customers c\n"
            "  JOIN customer_spend cs ON c.customer_id = cs.customer_id\n"
            ")\n"
            "SELECT \n"
            "  segment,\n"
            "  COUNT(*) AS paying_customers,\n"
            "  ROUND(AVG(total_spend), 2) AS avg_customer_ltv\n"
            "FROM spend_with_profiles\n"
            "GROUP BY segment\n"
            "ORDER BY avg_customer_ltv DESC;\n"
        )
    },

    # =========================================================================
    # MODULE 6: WINDOW FUNCTIONS
    # =========================================================================
    {
        "id": "sql_601",
        "module": "6. Window Functions (Analytical Mastery)",
        "title": "6.1 Ranking Functions (ROW_NUMBER vs DENSE_RANK)",
        "summary": "Assign ordinal rankings to rows within a partition without collapsing rows like GROUP BY does.",
        "takeaway": "ROW_NUMBER() assigns strictly unique integers (1, 2, 3), while DENSE_RANK() gives tied rows the same rank without skipping numbers.",
        "code_example": (
            "-- Rank employees by salary within each department\n"
            "SELECT \n"
            "  d.name AS department_name,\n"
            "  e.name AS employee_name,\n"
            "  e.salary,\n"
            "  ROW_NUMBER() OVER (\n"
            "    PARTITION BY e.dept_id \n"
            "    ORDER BY e.salary DESC\n"
            "  ) AS dept_salary_rank\n"
            "FROM employees e\n"
            "JOIN departments d ON e.dept_id = d.dept_id\n"
            "ORDER BY department_name, dept_salary_rank;\n"
        )
    },
    {
        "id": "sql_602",
        "module": "6. Window Functions (Analytical Mastery)",
        "title": "6.2 Running Totals & Cumulative Aggregates",
        "summary": "Calculate running sums, moving averages, and cumulative balances over ordered streams.",
        "takeaway": "SUM(...) OVER (ORDER BY date ASC) creates a running accumulator from the start of the partition up to the current row.",
        "code_example": (
            "-- Cumulative ledger balance for Bank Account 1\n"
            "SELECT \n"
            "  txn_id,\n"
            "  created_at,\n"
            "  txn_type,\n"
            "  amount,\n"
            "  ROUND(SUM(amount) OVER (\n"
            "    PARTITION BY account_id \n"
            "    ORDER BY created_at ASC\n"
            "  ), 2) AS cumulative_ledger_balance\n"
            "FROM transactions\n"
            "WHERE account_id = 1\n"
            "ORDER BY created_at ASC;\n"
        )
    },
    {
        "id": "sql_603",
        "module": "6. Window Functions (Analytical Mastery)",
        "title": "6.3 Period-over-Period Deltas with LAG & LEAD",
        "summary": "Access values from preceding or succeeding rows without performing expensive self-joins.",
        "takeaway": "LAG(col, 1) retrieves the previous row's value; LEAD(col, 1) retrieves the next row's value.",
        "code_example": (
            "-- Track historical salary growth steps for employee 6\n"
            "SELECT \n"
            "  effective_date,\n"
            "  change_reason,\n"
            "  salary AS current_salary,\n"
            "  LAG(salary, 1) OVER (ORDER BY effective_date ASC) AS previous_salary,\n"
            "  ROUND(salary - LAG(salary, 1) OVER (ORDER BY effective_date ASC), 2) AS salary_increase\n"
            "FROM salaries_history\n"
            "WHERE emp_id = 6\n"
            "ORDER BY effective_date ASC;\n"
        )
    }
]


def get_curriculum_modules() -> List[str]:
    """Returns unique list of module names in order."""
    modules = []
    for t in SQL_CURRICULUM:
        if t["module"] not in modules:
            modules.append(t["module"])
    return modules


def get_topics_for_module(module_name: str) -> List[Dict[str, Any]]:
    """Returns all topics under a specific module."""
    return [t for t in SQL_CURRICULUM if t["module"] == module_name]

def get_topic_by_id(topic_id: str):
    for t in SQL_CURRICULUM:
        if t["id"] == topic_id:
            return t
    return None
