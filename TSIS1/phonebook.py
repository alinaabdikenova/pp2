import csv
import json
import os
import psycopg2
from connect import connect


# Load SQL file
def load_sql_file(conn, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        sql = file.read()

    with conn.cursor() as cur:
        cur.execute(sql)

    conn.commit()


# Add contact manually
def add_contact(conn):
    first_name = input("First name: ")
    last_name = input("Last name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group_name = input("Group Family/Work/Friend/Other: ")
    phone = input("Phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    with conn.cursor() as cur:
        # create group if it does not exist
        cur.execute("""
            INSERT INTO groups(name)
            VALUES(%s)
            ON CONFLICT(name) DO NOTHING
        """, (group_name,))

        # get group id
        cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
        group_id = cur.fetchone()[0]

        # insert contact
        cur.execute("""
            INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
            VALUES(%s, %s, %s, %s, %s)
            RETURNING id
        """, (first_name, last_name, email, birthday, group_id))

        contact_id = cur.fetchone()[0]

        # insert phone
        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES(%s, %s, %s)
        """, (contact_id, phone, phone_type))

    conn.commit()
    print("Contact added successfully!")


# Import contacts from CSV
def import_csv(conn):
    filename = input("CSV filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        with conn.cursor() as cur:
            for row in reader:
                group_name = row["group"]

                # create group
                cur.execute("""
                    INSERT INTO groups(name)
                    VALUES(%s)
                    ON CONFLICT(name) DO NOTHING
                """, (group_name,))

                cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                group_id = cur.fetchone()[0]

                # insert contact
                cur.execute("""
                    INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
                    VALUES(%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    row["first_name"],
                    row["last_name"],
                    row["email"],
                    row["birthday"],
                    group_id
                ))

                contact_id = cur.fetchone()[0]

                # insert phone
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES(%s, %s, %s)
                """, (
                    contact_id,
                    row["phone"],
                    row["type"]
                ))

    conn.commit()
    print("CSV imported successfully!")


# Search using PostgreSQL function
def search_contacts(conn):
    query = input("Search: ")

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()

    print_contacts(rows)


# Search by email
def search_by_email(conn):
    email = input("Enter email part: ")

    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE c.email ILIKE %s
        """, ("%" + email + "%",))

        rows = cur.fetchall()

    print_contacts(rows)


# Filter by group
def filter_by_group(conn):
    group_name = input("Enter group name: ")

    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE g.name = %s
        """, (group_name,))

        rows = cur.fetchall()

    print_contacts(rows)


# Sort contacts
def sort_contacts(conn):
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ")

    if choice == "1":
        order = "c.first_name"
    elif choice == "2":
        order = "c.birthday"
    elif choice == "3":
        order = "c.created_at"
    else:
        print("Invalid choice")
        return

    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY {order}
        """)

        rows = cur.fetchall()

    print_contacts(rows)


# Pagination with next / prev / quit
def pagination(conn):
    limit = int(input("Page size: "))
    offset = 0

    while True:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            rows = cur.fetchall()

        print("\n--- Page ---")
        for row in rows:
            print(f"ID: {row[0]} | {row[1]} {row[2]} | Email: {row[3]} | Birthday: {row[4]} | Group: {row[5]}")

        command = input("next / prev / quit: ")

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Invalid command")


# Add phone using stored procedure
def add_phone(conn):
    name = input("Contact first name: ")
    phone = input("New phone: ")
    phone_type = input("Type home/work/mobile: ")

    with conn.cursor() as cur:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    print("Phone added!")


# Move contact to another group
def move_to_group(conn):
    name = input("Contact first name: ")
    group_name = input("New group: ")

    with conn.cursor() as cur:
        cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

    conn.commit()
    print("Contact moved to group!")


# Export all contacts to JSON
def export_json(conn):
    filename = input("JSON filename: ")

    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                c.id,
                c.first_name,
                c.last_name,
                c.email,
                c.birthday,
                g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
        """)

        contacts = cur.fetchall()

        result = []

        for contact in contacts:
            contact_id = contact[0]

            cur.execute("""
                SELECT phone, type
                FROM phones
                WHERE contact_id = %s
            """, (contact_id,))

            phones = cur.fetchall()

            result.append({
                "first_name": contact[1],
                "last_name": contact[2],
                "email": contact[3],
                "birthday": str(contact[4]),
                "group": contact[5],
                "phones": [
                    {
                        "phone": p[0],
                        "type": p[1]
                    }
                    for p in phones
                ]
            })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print("Exported to JSON successfully!")


# Import contacts from JSON
def import_json(conn):
    filename = input("JSON filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    with conn.cursor() as cur:
        for item in data:
            first_name = item["first_name"]
            last_name = item["last_name"]

            # check duplicate by first name and last name
            cur.execute("""
                SELECT id FROM contacts
                WHERE first_name = %s AND last_name = %s
            """, (first_name, last_name))

            existing = cur.fetchone()

            if existing:
                action = input(f"{first_name} {last_name} exists. skip/overwrite: ")

                if action == "skip":
                    continue

                elif action == "overwrite":
                    contact_id = existing[0]

                    # update contact
                    cur.execute("""
                        UPDATE contacts
                        SET email = %s, birthday = %s
                        WHERE id = %s
                    """, (item["email"], item["birthday"], contact_id))

                    # delete old phones
                    cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

                else:
                    continue

            else:
                # create group
                cur.execute("""
                    INSERT INTO groups(name)
                    VALUES(%s)
                    ON CONFLICT(name) DO NOTHING
                """, (item["group"],))

                cur.execute("SELECT id FROM groups WHERE name = %s", (item["group"],))
                group_id = cur.fetchone()[0]

                # insert new contact
                cur.execute("""
                    INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
                    VALUES(%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    item["first_name"],
                    item["last_name"],
                    item["email"],
                    item["birthday"],
                    group_id
                ))

                contact_id = cur.fetchone()[0]

            # insert phones
            for phone in item["phones"]:
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES(%s, %s, %s)
                """, (
                    contact_id,
                    phone["phone"],
                    phone["type"]
                ))

    conn.commit()
    print("JSON imported successfully!")


# Print contacts
def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        print(
            f"ID: {row[0]} | "
            f"Name: {row[1]} {row[2]} | "
            f"Email: {row[3]} | "
            f"Birthday: {row[4]} | "
            f"Group: {row[5]} | "
            f"Phone: {row[6]} | "
            f"Type: {row[7]}"
        )


def main():
    conn = connect()

    if conn is None:
        return

    # load database schema and procedures
    load_sql_file(conn, "schema.sql")
    load_sql_file(conn, "procedures.sql")

    while True:
        print("\n=== TSIS1 PhoneBook ===")
        print("1. Add contact")
        print("2. Import from CSV")
        print("3. Search contacts")
        print("4. Search by email")
        print("5. Filter by group")
        print("6. Sort contacts")
        print("7. Pagination")
        print("8. Add phone")
        print("9. Move to group")
        print("10. Export to JSON")
        print("11. Import from JSON")
        print("12. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_contact(conn)
        elif choice == "2":
            import_csv(conn)
        elif choice == "3":
            search_contacts(conn)
        elif choice == "4":
            search_by_email(conn)
        elif choice == "5":
            filter_by_group(conn)
        elif choice == "6":
            sort_contacts(conn)
        elif choice == "7":
            pagination(conn)
        elif choice == "8":
            add_phone(conn)
        elif choice == "9":
            move_to_group(conn)
        elif choice == "10":
            export_json(conn)
        elif choice == "11":
            import_json(conn)
        elif choice == "12":
            conn.close()
            print("Connection closed.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()