import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger


logger = setup_logger('db_helper')


@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tung144@@",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s and %s  
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_expense_by_month(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''WITH CTE AS
                        (SELECT *,
                            MONTHNAME(expense_date) as month
                        FROM
                            expense_manager.expenses
                        )
                        SELECT  month, SUM(amount) as total
                        FROM CTE
                        WHERE expense_date BETWEEN  %s AND %s
                        GROUP BY month
                        ORDER BY month DESC''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

if __name__ == "__main__":
    # expenses = fetch_expenses_for_date("2024-08-2")
    # print(expenses)
    # delete_expenses_for_date("2024-08-25")
    # data = fetch_expense_summary("2024-08-01", "2024-08-05")
    # print(data)
    # for record in data:
    #     print(record)
    # print(data)
    data = fetch_expense_by_month("2024-08-01", "2024-09-30")
    print(data)