from models.finance_model import FinanceModel


class FinanceController:

    def get_summary(self):
        try:
            row = FinanceModel.get_summary()
            if not row or row[0] == 0:
                return self._empty_summary()

            total, pend, over, paid, pend_n, over_n, paid_n = row
            pend = float(pend or 0)
            over  = float(over  or 0)
            paid  = float(paid  or 0)
            outstanding = pend + over
            revenue     = paid + outstanding
            rate = (paid / revenue * 100) if revenue > 0 else 0

            return {
                "total":       total,
                "pending":     f"£{pend:,.2f}",
                "overdue":     f"£{over:,.2f}",
                "paid":        f"£{paid:,.2f}",
                "outstanding": f"£{outstanding:,.2f}",
                "rate":        f"{rate:.1f}%",
                "pending_n":   pend_n or 0,
                "overdue_n":   over_n or 0,
                "paid_n":      paid_n or 0
            }
        except Exception as e:
            print(f"Finance summary error: {e}")
            return self._empty_summary()

    def _empty_summary(self):
        return {
            "total":       0,
            "pending":     "£0.00",
            "overdue":     "£0.00",
            "paid":        "£0.00",
            "outstanding": "£0.00",
            "rate":        "0%",
            "pending_n":   0,
            "overdue_n":   0,
            "paid_n":      0
        }

    def get_recent_transactions(self):
        try:
            rows = FinanceModel.get_recent_transactions()
            result = []
            for r in rows:
                amt = float(r[1])
                result.append({
                    "invoice": r[0],
                    "amount":  f"£{amt:,.2f}",
                    "due":     str(r[2]),
                    "status":  r[3].capitalize(),
                    "tenant":  r[4],
                    "apt":     r[5]
                })
            return result
        except Exception as e:
            print(f"Finance transactions error: {e}")
            return []

    def get_upcoming_dues(self):
        try:
            rows = FinanceModel.get_upcoming_dues()
            return [{
                "invoice": r[0],
                "amount":  f"£{float(r[1]):,.2f}",
                "due":     str(r[2]),
                "tenant":  r[3],
                "apt":     r[4]
            } for r in rows]
        except Exception as e:
            print(f"Finance dues error: {e}")
            return []