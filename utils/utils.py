def user_input(prompt, options):
    while True:
        print(prompt)
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
        try:
            return options[int(input("Enter your choice: ")) - 1]
        except (ValueError, IndexError):
            print("Invalid input. Try again.")
