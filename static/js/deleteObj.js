//<button class="delete-btn" data-course-id="1">Delete</button>

document.querySelectorAll('.delete-btn-course').forEach(button => {
    button.addEventListener('click', function() {
        const courseId = this.getAttribute('data-course-id');
        const confirmDelete = confirm("Are you sure you want to delete this course?");
        
        if (confirmDelete) {
            deleteCourse(courseId);
        }
    });
});

function deleteCourse(courseId) {
    fetch(`/teacher/course/delete/${courseId}/`, {
        method: 'DELETE', // or 'POST' if you are using a form submission
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for Django
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            // Optionally remove the course from the UI
            const courseElement = document.getElementById(`course-${courseId}`);
            if (courseElement) {
                alert("course deleted successfully!");
                courseElement.remove();
            } else {
                alert("There was an issue deleting the course.");
            }
        }  
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while trying to delete the course. CATCH");
    });
}






//<button class="delete-btn" data-unit-id="1">Delete</button>

document.querySelectorAll('.delete-btn-unit').forEach(button => {
    button.addEventListener('click', function() {
        const unitId = this.getAttribute('data-unit-id');
        const confirmDelete = confirm("Are you sure you want to delete this unit?");
        
        if (confirmDelete) {
            deleteUnit(unitId);
        }
    });
});

function deleteUnit(unitId) {
    fetch(`/teacher/unit/delete/${unitId}/`, {
        method: 'DELETE', // or 'POST' if you are using a form submission
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for Django
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            // Optionally remove the course from the UI
            const courseElement = document.getElementById(`course-${courseId}`);
            if (courseElement) {
                alert("course deleted successfully!");
                courseElement.remove();
            } else {
                alert("There was an issue deleting the course.");
            }
        }  
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while trying to delete the course. CATCH");
    });
}


//<button class="delete-btn" data-lesson-id="1">Delete</button>

document.querySelectorAll('.delete-btn-lesson').forEach(button => {
    button.addEventListener('click', function() {
        const lessonId = this.getAttribute('data-lesson-id');
        const confirmDelete = confirm("Are you sure you want to delete this lesson?");
        
        if (confirmDelete) {
            deleteLesson(lessonId);
        }
    });
});

function deleteLesson(lessonId) {
    fetch(`/teacher/lesson/delete/${lessonId}/`, {
        method: 'DELETE', // or 'POST' if you are using a form submission
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for Django
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            // Optionally remove the lesson from the UI
            const lessonElement = document.getElementById(`lesson-${lessonId}`);
            if (lessonElement) {
                alert("lesson deleted successfully!");
                lessonElement.remove();
            } else {
                alert("There was an issue deleting the lesson.");
            }
        }  
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while trying to delete the lesson. CATCH");
    });
}






// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}