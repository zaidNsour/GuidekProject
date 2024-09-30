# Guidek

This project Flask-powered API for a Flutter-based Student Assistance App, designed to streamline academic management.
Key features include viewing class locations with GPS, accessing slides and syllabus, using a transaction guide for university processes,and viewing announcements.
Students can also contact admins directly for support, making it an essential tool for managing coursework and campus life efficiently.

## Features

### For Students

- **View Announcements**: Allows students to access important announcements related to academic and campus activities.

- **Request New Classes**: tudents can request to enroll in new classes. The app displays the status of these requests, whether approved or pending.

- **Control Personal Profile**: Students can manage and update their personal information, such as contact details, within their profile.

- **Contact Admin**: Allows students to communicate directly with the admin for assistance or inquiries.

- **Use Transaction Guide**: Guides students through various university procedures, such as course registration, dropping classes, and applying for financial aid.

- **View Common Questions and Answers (FAQ)**: Provides answers to frequently asked questions about academic and administrative processes.

- **Access Slides and Syllabus**: Students can access lecture slides and course syllabi, ensuring they have all the necessary materials for their courses.
- 
- **View Class Location**: Integrates with GPS to help students find classrooms within the university campus.

### For Admins

- **Manage Announcements**: Admins can create, update, and delete announcements for students.

- **Manage Class Requests**: Admins can approve, deny, or update the status of student class requests.
- 
- **Access Admin Dashboard**: Provides admins with access to a comprehensive dashboard where they can manage users, and other administrative functions.

## Tech Stack

- Backend: Flask (Python)
- Frontend: Flutter (for the mobile app)
- Database: SQLite
- Authentication: JWT (JSON Web Token)
-Other Technologies:
  -- Google Maps API (for GPS navigation)
  -- RESTful API principles


## Prerequisites
To run this project, you will need:
- Python 3.12.5
- Flask 2.x
- SQLAlchemy
- JWT

## Getting Started

To run this project locally, follow these steps:

Step 1. Clone the repository:

```bash
git clone https://github.com/zaidNsour//guidek.git
```

Step 2. Navigate into the project directory:
```bash
cd LearnTech
```

Step 3. Install the required dependencies:
 ```bash
   pip install -r requirements.txt
```

Step 4. Set up the following environment variables:
```bash
  export SECRET_KEY=your-secret-key
  export EMAIL_USER=your-email@example.com
  export EMAIL_PASS=your-email-password
```

Step 5. Run the app:
```bash
  flask run
```


## Contributing
 If you'd like to contribute to the project, follow these steps:
 
1- Fork the repository.

2- Create a new branch: 

```bash
git checkout -b feature/new-feature
```

3- Make your changes and commit them:

```bash
git commit -m 'Add new feature'
```

4- Push to the branch: 

```bash
git push origin feature/new-feature
```

5- Submit a pull request.

## License
This project is licensed under the MIT License.
