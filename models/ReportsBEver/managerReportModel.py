from Models.ReportsBEver.managereportsBE import ReportModel


class ReportController:

    def get_occupancy_data(self, city=None):
        rows = ReportModel.get_occupancy_report(city)
        return [{
            "apartment": r[0],
            "type":      r[1],
            "rent":      f"£{float(r[2]):,.2f}",
            "status":    r[3],
            "city":      r[4],
            "tenants":   r[5]
        } for r in rows]

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

    def get_maintenance_data(self):
        rows = ReportModel.get_maintenance_report()
        total_cost = 0.0
        total_hours = 0
        data = []

        for r in rows:
            cost  = float(r[4]) if r[4] else 0.0
            hours = int(r[3])   if r[3] else 0
            total_cost  += cost
            total_hours += hours
            data.append({
                "id":    r[0],
                "apt":   r[1],
                "date":  str(r[2]),
                "hours": hours,
                "cost":  f"£{cost:,.2f}",
                "notes": r[5]
            })

        summary = {
            "total_cost":  f"£{total_cost:,.2f}",
            "total_hours": str(total_hours)
        }
        return data, summary
