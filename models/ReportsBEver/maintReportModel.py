from Models.ReportsBEver.adminreportsBE import ReportModel


class ReportController:
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