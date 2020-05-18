from databaseconnect import clear_table

print("---------------------------------------")
print("          CLEARING TABLES")
print("---------------------------------------")
print("             Options Menu")
print("1. ALL TABLES")
print("2. chat_table")
print("3. question_table and statement_table")
print("Enter the respective option (1 or 2 or 3) according to the above menu:")

option = int(input())

if option == 1:
    clear_table("chat_table")
    clear_table("directions_table")
    clear_table("question_table")
elif option == 2:
    clear_table("chat_table")
elif option == 3:
    clear_table("question_table")
else:
    print("Invalid option")
