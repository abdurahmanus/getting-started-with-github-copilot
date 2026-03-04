import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_all_activities_returns_success(self, client, fresh_activities):
        """
        Arrange: None (uses default fixture data)
        Act: Make GET request to /activities
        Assert: Response is 200 and contains all activities
        """
        # Arrange
        expected_activity_count = 9
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == expected_activity_count
    
    def test_get_activities_includes_activity_details(self, client, fresh_activities):
        """
        Arrange: None
        Act: Get activities
        Assert: Each activity has required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert all(field in activity_data for field in required_fields)
    
    def test_get_activities_includes_participants(self, client, fresh_activities):
        """
        Arrange: None
        Act: Get activities
        Assert: Participants list is included for each activity
        """
        # Arrange
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list)
            assert len(activity_data["participants"]) > 0  # All test activities have participants


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_successful_for_available_activity(self, client, fresh_activities):
        """
        Arrange: Use Debate Team which has 1 participant and space for more
        Act: Sign up a new student
        Assert: Response is 200 and participant is added
        """
        # Arrange
        activity_name = "Debate Team"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert email in fresh_activities[activity_name]["participants"]
    
    def test_signup_returns_success_message(self, client, fresh_activities):
        """
        Arrange: Debate Team activity
        Act: Sign up new student
        Assert: Response contains success message
        """
        # Arrange
        activity_name = "Debate Team"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_signup_fails_for_nonexistent_activity(self, client, fresh_activities):
        """
        Arrange: Use a nonexistent activity name
        Act: Try to sign up
        Assert: Response is 404
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_fails_for_duplicate_enrollment(self, client, fresh_activities):
        """
        Arrange: Chess Club has michael@mergington.edu already signed up
        Act: Try to sign up the same student again
        Assert: Response is 400 with error message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in participants
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_increments_participant_count(self, client, fresh_activities):
        """
        Arrange: Get initial participant count for Debate Team
        Act: Sign up new student
        Assert: Participant count increased by 1
        """
        # Arrange
        activity_name = "Debate Team"
        email = "newstudent@mergington.edu"
        initial_count = len(fresh_activities[activity_name]["participants"])
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert len(fresh_activities[activity_name]["participants"]) == initial_count + 1


class TestUnregisterFromActivity:
    """Tests for POST /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_successful_for_enrolled_student(self, client, fresh_activities):
        """
        Arrange: Chess Club has michael@mergington.edu enrolled
        Act: Unregister the student
        Assert: Response is 200 and participant is removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert email not in fresh_activities[activity_name]["participants"]
    
    def test_unregister_returns_success_message(self, client, fresh_activities):
        """
        Arrange: Programming Class has emma@mergington.edu
        Act: Unregister the student
        Assert: Response contains success message
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_unregister_fails_for_nonexistent_activity(self, client, fresh_activities):
        """
        Arrange: Use a nonexistent activity
        Act: Try to unregister
        Assert: Response is 404
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_fails_for_non_enrolled_student(self, client, fresh_activities):
        """
        Arrange: Try to unregister student not in Debate Team
        Act: Unregister non-enrolled email
        Assert: Response is 400 with error message
        """
        # Arrange
        activity_name = "Debate Team"
        email = "notstudent@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_decrements_participant_count(self, client, fresh_activities):
        """
        Arrange: Get initial count for Drama Club
        Act: Unregister a student
        Assert: Count decreased by 1
        """
        # Arrange
        activity_name = "Drama Club"
        email = "sarah@mergington.edu"
        initial_count = len(fresh_activities[activity_name]["participants"])
        
        # Act
        client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert len(fresh_activities[activity_name]["participants"]) == initial_count - 1
    
    def test_unregister_frees_up_spot_for_new_signup(self, client, fresh_activities):
        """
        Arrange: Unregister a student from Tennis Club, then sign up new one
        Act: Unregister then signup
        Assert: Both operations succeed
        """
        # Arrange
        activity_name = "Tennis Club"
        to_remove = "alex@mergington.edu"
        to_add = "newstudent@mergington.edu"
        
        # Act
        remove_response = client.post(f"/activities/{activity_name}/unregister?email={to_remove}")
        signup_response = client.post(f"/activities/{activity_name}/signup?email={to_add}")
        
        # Assert
        assert remove_response.status_code == 200
        assert signup_response.status_code == 200
        assert to_remove not in fresh_activities[activity_name]["participants"]
        assert to_add in fresh_activities[activity_name]["participants"]
