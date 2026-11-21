# FinSight AI

**Intelligent Expense Classification, Income Management and AI Budget Prediction System**

FinSight AI is a Flask + MySQL financial management application with a JavaScript frontend. It supports personal and group expenses, machine-learning expense classification, historical income tracking, planned savings, category-level spending forecasts and personalized financial reminders.

## Features

### Personal finance
- Record expenses with the actual transaction date, category, source and notes.
- Filter transactions by month and category.
- Record effective-dated monthly salary history.
- Record one-time bonuses, incentives and other income separately from recurring salary.
- Compare monthly salary, additional income, total income, expenses, planned savings and spendable balance.
- Configure automatic savings as a fixed amount or a percentage of salary, with an optional percentage of bonus income.

### AI and machine learning
- Auto-classify transactions with the existing Naive Bayes text classifier.
- Predict category-level spending using historical expenses, Weighted Moving Average and Linear Trend analysis.
- Consider effective-dated salary revisions when calculating future spendable budgets.
- Keep bonuses as one-time income instead of treating them as recurring salary.
- Generate personalized saving tips with Google Gemini when configured; use deterministic rule-based tips when Gemini is unavailable.
- Retain existing anomaly detection, ML Insights and AI Assistant functionality.

### Budgeting and reminders
- AI Budget Prediction module with expected salary, additional income, predicted expenses, automatic savings, spendable budget and category-level recommended limits.
- Recommended category limits use predicted spending plus a modest buffer, capped by the spendable budget. When there is insufficient history, the app does not invent category limits.
- Persistent in-app daily, weekly and monthly reminders, plus category budget warnings.
- Optional browser notifications while the application is open and browser permission has been granted.

### Existing group functionality
- Groups, shared expenses, equal/percentage/custom splits, comments, receipt uploads and settlement workflows.
- Real-time group activity through Flask-SocketIO.

## Tech stack

- Python, Flask, Flask-Login, Flask-SocketIO
- MySQL 8.0 and mysql-connector-python
- Scikit-learn and the existing FinSight ML modules
- Google Gemini API (optional for AI-generated saving tips)
- HTML, CSS and vanilla JavaScript
- APScheduler for local scheduled reminders

## Setup on Windows / VS Code

### 1. Create or confirm the MySQL database

In MySQL Workbench, connect to your local MySQL Server and execute:

```sql
CREATE DATABASE IF NOT EXISTS finsight_ai
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 2. Configure environment variables

Copy `.env.example` to `.env` in this project folder and edit the values:

```env
SECRET_KEY=replace-with-a-long-random-secret
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=finsight_ai
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
```

`GEMINI_API_KEY` is optional. Without it, the Saving Advisor uses rule-based recommendations. Never commit or share `.env`.

### 3. Create a virtual environment and install dependencies

Open the VS Code terminal in the folder containing `run.py`:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks virtual environment activation, run this in the same terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 4. Start the application

Make sure MySQL Server is running, then execute:

```powershell
python run.py
```

Open `http://localhost:5000` in your browser. Keep the terminal running while using the application. Press `Ctrl + C` to stop Flask and the reminder scheduler.

## Upgrade an existing FinSight AI database

1. Back up the `finsight_ai` database in MySQL Workbench before upgrading.
2. Extract the updated project into a new folder. Keep the original project until the upgrade works.
3. Copy your existing `.env` file into the new `finsight-ai` folder. The distributed ZIP intentionally does not contain `.env` so your database password and API key remain private.
4. Activate the new project's virtual environment (or create one) and run `pip install -r requirements.txt`.
5. Start the app using `python run.py`.
6. The startup routine keeps existing tables and applies `migrations/001_finance_upgrade.sql` once. The migration creates the new finance and notification tables and seeds the current month's salary from the legacy `users.monthly_income` value.
7. Sign in with your existing account. Your existing user, expenses, groups, budgets and savings goals are not intentionally cleared or recreated.

### Important historical-data limitation

The original database stored one `users.monthly_income` value and did not preserve historical salary changes or bonus income. The upgrade can seed the current month's salary from that legacy value, but it cannot reconstruct missing older salary or bonus records. Use **Income & History** to enter the correct salary amount for each missing effective month and add real historical bonuses. Use the transaction date field when entering past expenses. The application does not fabricate historical records.

## How the new finance rules work

- **Salary history:** A salary record takes effect from the selected month onward. Updating a December salary does not rewrite October or November.
- **Bonus and incentives:** Additional income is counted only in the month of its transaction date. It never changes recurring salary.
- **Automatic savings:** Savings are reserved from income before calculating the spendable budget. For example, a 20% savings setting on a ₹50,000 salary reserves ₹10,000 and leaves ₹40,000 spendable. Saving a percentage of bonuses is optional.
- **No double-counting:** A savings reservation is a budget allocation, not a second income item or a bank transfer. Actual savings goal contributions remain in the existing Savings Goals module.
- **Prediction:** Expense predictions are based on up to six previous months of user-share expense history. A salary revision changes the income and spendable-budget context. A one-time bonus does not become recurring income or automatically inflate predicted expenses.
- **Notifications:** APScheduler writes reminders to MySQL while `python run.py` is running. Notifications are not guaranteed when the local application is stopped. Browser notifications require permission and the website to remain open; always-on push delivery would require a separate Web Push service and service worker.

## New finance API endpoints

- `GET /api/finance/income?month=YYYY-MM`
- `POST /api/finance/income`
- `DELETE /api/finance/income/<id>`
- `POST /api/finance/salary`
- `GET /api/finance/history?months=2&end_month=YYYY-MM`
- `GET /api/finance/savings-settings`
- `PUT /api/finance/savings-settings`
- `GET /api/finance/budget-prediction?month=YYYY-MM`
- `GET /api/finance/saving-tips?month=YYYY-MM`
- `GET /api/finance/notifications`
- `PATCH /api/finance/notifications/<id>/read`
- `PATCH /api/finance/notifications/read-all`
- `GET /api/finance/notification-preferences`
- `PUT /api/finance/notification-preferences`

## Validation performed for this update

- Python source compilation completed successfully.
- JavaScript syntax checks completed successfully for `app.js` and `finance.js`.
- Existing focused unit tests for budget allocation and savings-goal calculations passed.
- A mocked finance-forecast smoke test confirmed that a scheduled salary increase and one-time bonus are reflected separately in total income, savings reserve and spendable budget.

Database integration still needs to be verified on the user's local MySQL installation using their `.env` credentials.

## Reports, reviewed budget plans and AI insights (additional update)

This update adds the following workflows on top of the income-history and savings upgrade:

### Reports

- Open **Reports** and choose a month.
- The report includes salary and additional income, expense transactions (including the logged-in user's share of group expenses), category totals, budgets versus actual spending, automatic savings reserved, and savings-goal contributions.
- Click **Download PDF** to download a monthly PDF report. `reportlab` is included in `requirements.txt` and is installed with the normal dependency command.

### Generate My Budget Plan

- Open **Budgets**, choose the month and click **Generate My Budget Plan**.
- The plan analyzes the previous three completed months using the existing WMA + Linear Trend predictor, retrieves salary/additional income and reserves automatic savings first.
- Review/edit the proposed category limits. The generated plan is a draft only; it does not save budgets.
- Click **Apply Budget** to save the reviewed category budgets. Click **Discard plan** to abandon it without changes.

### AI Budget Optimizer

- The optimizer compares each saved category limit with actual expense shares for the selected month.
- It may suggest transferring unused planned amount from a category with remaining budget to one that is over budget.
- Select the recommendations to accept and click **Accept selected adjustments**. Use **Reject recommendations** to dismiss the current suggestions without changing saved budgets.

### AI Expense Insights

- Open **AI Expense Insights**, select a month and click **Analyze spending**.
- The analysis compares individual transactions and category totals with the preceding three months. It uses the existing Z-score anomaly detector plus category-baseline thresholds to flag unusual patterns.
- These are review flags and are not fraud determinations. The user should confirm whether a flagged transaction is expected and categorized correctly.

### Upgrade / running

From the `finsight-ai` project folder:

```powershell
python -m pip install -r requirements.txt
python run.py
```

The existing automatic database migration mechanism remains in use; these additions do not require a new SQL migration. Back up the MySQL database before replacing an earlier project folder. Keep the existing `.env` file and do not place it in a shared ZIP.
