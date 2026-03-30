from models.ReportsBEver.financereportsBE import ReportModel


class ReportController:

    def get_financial_data(self):
        rows = ReportModel.get_financial_report()
        total_paid = 0.0
        total_pending = 0.0
        total_overdue = 0.0
        data = []

        for r in rows:
            amt = float(r[1])
            st  = r[3].lower()
            if st == "paid":
                total_paid += amt
            elif st == "pending":
                total_pending += amt
            elif st == "overdue":
                total_overdue += amt
            data.append({
                "invoice": r[0],
                "amount":  f"£{amt:,.2f}",
                "due":     str(r[2]),
                "status":  r[3].capitalize(),
                "tenant":  r[4]
            })

        summary = {
            "paid":        f"£{total_paid:,.2f}",
            "pending":     f"£{total_pending:,.2f}",
            "overdue":     f"£{total_overdue:,.2f}",
            "outstanding": f"£{total_pending + total_overdue:,.2f}"
        }
        return data, summary