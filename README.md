<br>
<p align="center">
  <img src="https://fontmeme.com/permalink/231128/6358bae003a72e975f4361219146d2f9.png" alt="Library Logo" width="300" height="50">
</p>

# Library Management System

Welcome to the Minamoto Library Management System! This system provides an easy-to-use platform for users to explore the library's collection, borrow books, manage loans, and more.

## Features

### User Interface
- **Sign Up and Login:**
  - Users can sign up and create accounts, allowing them to log in and access library contents.
  ![enter image description here](https://i.ibb.co/pdXx6Hn/ezgif-5-91c3fb938f.gif)
- **Home Page:**
  - Displays a search bar and a list of available books.
  -  Users can search and filter books by title, author, and category.
  - Recommends books from the category the user borrowed the most.
![enter image description here](https://i.ibb.co/R9V9pms/ezgif-5-b7da9249e3.gif)

### Administrative CLI (Command-Line Interface)

- **Add, Edit, and Delete Books:**
  - Administrators can use the command-line interface to add, edit, and delete books in the database.
- **Add and Delete Users:**
  - Administrators can add and delete user accounts using the command-line interface.

### Loans Management
- **Borrowing Books:**
  - Users can borrow books by providing contact email and loan duration.
  ![enter image description here](https://i.ibb.co/5FT4ZKG/ezgif-5-49a142a289.gif)
- **Loans Page:**
  - Displays active, expired, and historical loans.
  - Users can return active loans directly from the loans page.
  ![enter image description here](https://i.ibb.co/PrrdCcY/ezgif-5-537efc8b67.gif)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/library-management-system.git
   cd library-management-system
   ```
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
 
 3.  **Set up the database URI:**
   -   Open the `__init__.py` script in `/website` folder.
  -   Locate the placeholder `'DB_NAME'` and replace it with the actual URI of your database.
4. **Run the script:**
		```bash
		python main.py
		```

This will set up the necessary files and dependencies to run the Minamoto源 Library Management System.

## 🎉 Usage
- **View Website:**
	- The website can be viewed by reaching the URL that is displayed in the standard output (by default the website runs on the admin's local server).
	![enter image description here](https://i.ibb.co/jRfjw3Z/Screenshot-2023-11-29-025325.png) 

-   **User Interface:**
    -   Users can explore the library, borrow books, and manage loans through the web interface.
    ![enter image description here](https://i.ibb.co/z5XDCxN/Screenshot-2023-11-29-022758.png)![enter image description here](https://i.ibb.co/wLR9yZ1/Screenshot-2023-11-29-022023.png)
    ![enter image description here](https://i.ibb.co/D45vBRX/Screenshot-2023-11-29-022258.png)
    
    -   Use the enhanced search bar with filters to find books by title, author, and category.
    ![enter image description here](https://i.ibb.co/HBvqGvd/Screenshot-2023-11-29-022955.png)
    -   Discover book recommendations based on the category the user borrowed the most.
    ![enter image description here](https://i.ibb.co/pwymBXh/Screenshot-2023-11-29-023109.png)
-   **Command-Line Interface (CLI):**
    -   Administrators can use the command-line interface to add, edit, and delete books and users in the database.
    -  Usage: 
	    ```bash
	    python admin.py [OPTIONS] COMMAND [ARGS]...	
	    ``` 
    - Options:
	    ```bash
	    --help  - Show help and exit.
	    ```
    - Commands:
	    ```bash
	    add-book - Add a new book to the database.
	    add-user - Add a new user to the database.
	    delete-book - Delete a book from the database.
	    delete-user - Delete a user from the database.
	    edit-book - Edit an existing book in the database.
	    ```



## 🤝 Contributing

Contributions are welcome! Please follow these steps to contribute:

1.  Fork the repository.
2.  Create a new branch: `git checkout -b feature/your-feature`.
3.  Commit your changes: `git commit -m 'Add some feature'`.
4.  Push to the branch: `git push origin feature/your-feature`.
5.  Submit a pull request.

## 📝 License

This project is licensed under the [MIT License](https://chat.openai.com/c/LICENSE).

----------

