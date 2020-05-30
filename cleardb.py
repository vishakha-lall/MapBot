from databaseconnect import clear_table

print("---------------------------------------")
print("          CLEARING TABLES")
print("---------------------------------------")
print("             Options Menu")
print("1. ALL TABLES")
print("2. `chat_table`")
print("3. `directions_table`")
print("4. `question_table` and `statement_table`")
print("Enter the respective option (1 or 2 or 3 or 4) according to the above menu:")

option = int(input())

if option == 1:
    clear_table("chat_table")
    clear_table("directions_table")
    clear_table("question_table")
    # automatically deletes `statement_table` with it
elif option == 2:
    clear_table("chat_table")
elif option == 3:
    clear_table("directions_table")
elif option == 4:
    clear_table("question_table")
    # automatically deletes `statement_table` with it
else:
    print("Invalid option")
