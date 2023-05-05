## Social Media API

<p>RESTful API service that provides functionality for managing a social media system.</p>


<ul>
<li><strong>Authentication:</strong> Secure access to API endpoints using JWT token-based authentication.</li>
<li><strong>Post management:</strong> Full CRUD functionality for managing posts, including creation, retrieval, updating, and deletion. Filter posts by title and content.</li>
<li><strong>User management:</strong> Allow users to register, update their profile information (e.g., bio and avatar), and search for other users by username.</li>
</ul>


# Setup and Installation

<ol>
<li>Clone the repository.
  git clone https://https://github.com/VladyslavCherkashyn/social-meadia-ap-
</li>
<li>Change directory to the project folder.
cd social-media-api</li>
<li>Create a virtual environment and activate it.
python -m venv venv source venv/bin/activate</li>
<li>Install the required packages.
pip install -r requirements.txt</li>
<li>Apply database migrations.
python manage.py migrate</li>
<li>Run the development server.
python manage.py runserver</li>
</ol>


