# Purchase Requisition System - Assessment 2

class RequisitionSystem:
    def __init__(self):
        self.requisitions = []
        self.next_id = 10001

    def add_requisition(self, date, staff_id, staff_name, items):
        if date == "" or staff_id == "" or staff_name == "":
            raise ValueError("Fill in all the required fields.")

        if len(items) == 0:
            raise ValueError("Need at least one item.")

        valid_items = []
        for name, cost_val in items:
            if name == "":
                raise ValueError("Item name cannot be blank.")
            
            try:
                c = float(cost_val)
            except:
                raise ValueError("Cost must be a number.")

            if c < 0:
                raise ValueError("Cost can't be negative.")

            valid_items.append((name, c))

        req_id = self.next_id
        self.next_id += 1
        
        total_cost = 0
        for name, c in valid_items:
            total_cost += c

        req = {
            "date": date,
            "requisition_id": req_id,
            "staff_id": staff_id,
            "staff_name": staff_name,
            "items": valid_items,
            "total": total_cost,
            "status": "Pending",
            "approval_reference": "Not available"
        }

        self.requisitions.append(req)
        self.check_approval(req_id)
        return req

    def get_req(self, req_id):
        for r in self.requisitions:
            if r["requisition_id"] == req_id:
                return r
        return None

    def check_approval(self, req_id):
        req = self.get_req(req_id)
        if req is None:
            return False

        t = req["total"]

        if t < 500:
            req["status"] = "Approved"
            req["approval_reference"] = req["staff_id"] + str(req_id % 1000)
        elif t <= 1000:
            req["status"] = "Pending"
            req["approval_reference"] = "Not available"
        else:
            req["status"] = "Not approved"
            req["approval_reference"] = "Not available"

        return True

    def update_status(self, req_id, decision):
        req = self.get_req(req_id)

        if req is None:
            return False, "ID not found."

        if req["status"] != "Pending":
            return False, "Can only review pending ones."

        dec = decision.strip().lower()

        if dec == "approved":
            req["status"] = "Approved"
            req["approval_reference"] = req["staff_id"] + str(req_id % 1000)
            return True, "Approved successfully."
        elif dec in ("not approved", "rejected"):
            req["status"] = "Not approved"
            req["approval_reference"] = "Not available"
            return True, "Marked as not approved."
        else:
            return False, "Type Approved or Not approved."

    def show_all(self):
        if len(self.requisitions) == 0:
            print("\nNo requisitions found.")
            return

        print("\n--- ALL REQUISITIONS ---")
        for r in self.requisitions:
            print("\nDate:", r["date"])
            print("ID:", r["requisition_id"])
            print("Staff ID:", r["staff_id"])
            print("Name:", r["staff_name"])
            print("Items:")
            for name, cost in r["items"]:
                print("  -", name, ": $", cost)
            print("Total: $", r["total"])
            print("Status:", r["status"])
            print("Ref:", r["approval_reference"])

    def get_stats(self):
        sub = len(self.requisitions)
        app = 0
        pend = 0
        rej = 0

        for r in self.requisitions:
            if r["status"] == "Approved":
                app += 1
            elif r["status"] == "Pending":
                pend += 1
            elif r["status"] == "Not approved":
                rej += 1

        print("\n--- STATS ---")
        print("Submitted:", sub)
        print("Approved:", app)
        print("Pending:", pend)
        print("Not approved:", rej)


def get_items_input():
    items = []
    while True:
        name = input("Item name: ").strip()
        if name == "":
            print("Cant be empty")
            continue

        try:
            cost = float(input("Cost ($): "))
            if cost < 0:
                print("No negative numbers")
                continue
        except ValueError:
            print("Enter a valid number")
            continue

        items.append((name, cost))

        more = input("Add another item? (yes/no): ").strip().lower()
        if more != "yes":
            break
    return items


def main():
    system = RequisitionSystem()

    while True:
        print("\n=== Requisition Menu ===")
        print("1. Add Requisition")
        print("2. Manager Review")
        print("3. View All")
        print("4. View Stats")
        print("5. Exit")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            date = input("Date: ").strip()
            staff_id = input("Staff ID: ").strip()
            name = input("Staff Name: ").strip()

            try:
                items = get_items_input()
                r = system.add_requisition(date, staff_id, name, items)
                print("\nAdded! ID:", r["requisition_id"], "| Total: $", r["total"], "| Status:", r["status"])
            except ValueError as e:
                print("Error:", e)

        elif choice == "2":
            pending = [r for r in system.requisitions if r["status"] == "Pending"]
            if len(pending) == 0:
                print("No pending requisitions.")
                continue

            print("\nPending List:")
            for r in pending:
                print("ID:", r["requisition_id"], "|", r["staff_name"], "| Total: $", r["total"])

            try:
                rid = int(input("Enter ID to review: "))
            except ValueError:
                print("Invalid ID number.")
                continue

            dec = input("Decision (Approved/Not approved): ")
            success, msg = system.update_status(rid, dec)
            print(msg)

        elif choice == "3":
            system.show_all()

        elif choice == "4":
            system.get_stats()

        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Wrong choice, try again.")


if __name__ == "__main__":
    main()