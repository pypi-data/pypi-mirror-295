import requests
import random

class ApiClient:
    def __init__(self, api_key="demokey", access_key="", base_url="https://7km5vhnbvd.execute-api.ca-central-1.amazonaws.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.access_key = access_key

    def collect_questions(self):
        endpoint = f"{self.base_url}/questions"
        headers = {
            "Content-Type": "application/json",
            # It's recommended to send the API key in the headers, as this method is prioritized.
            "Authorization": self.api_key
        }
        data = {
            # Alternatively api_key can be in data
            "api_key": self.api_key
        }
        try:
            response = requests.post(endpoint, json=data, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def calculate_score(self, answers):
        endpoint = f"{self.base_url}/score"
        headers = {
            "Content-Type": "application/json",
            # It's recommended to send the API key in the headers, as this method is prioritized.
            "Authorization": self.api_key
        }
        data = {
            # Alternatively api_key can be in data
            "api_key": self.api_key,
            "answers": answers
        }
        try:
            response = requests.post(endpoint, json=data, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def check_answers_for_questions(questions, answers):
        # Create a set of all question texts from the answers dictionary
        answered_questions = set(answer['question'] for answer in answers.values())

        # Initialize a list to store questions without answers
        questions_without_answers = []

        # Iterate over each question in the questions list
        for question in questions:
            question_text = question.get('question')
            # Check if the question text exists in the answered_questions set
            if question_text not in answered_questions:
                questions_without_answers.append(question_text)

        # Return the list of questions without answers
        return questions_without_answers

    @staticmethod
    def generate_mock_answers(questions):
        mock_answers = {}

        for idx, question in enumerate(questions):
            question_text = question.get('question')
            answers = question.get('answers', [])

            if answers:
                # Randomly select an answer from the available options
                mock_answer = random.choice(answers)['value']
            else:
                # If no specific answers are provided, generate a default value
                # For example, for yes/no questions or open-ended, set a default
                mock_answer = 'default'

            # Add the mock answer to the mock_answers dictionary
            mock_answers[idx] = {'answer': str(mock_answer), 'question': question_text}

        return mock_answers


# Example usage
# api_key = "your_api_key_here"
# api_wrapper = ApiGatewayWrapper(api_key)
# questions = api_wrapper.collect_questions()
#
# if questions is not None:
#     print("Questions collected successfully:")
#     print(questions)
# else:
#     print("Failed to collect questions.")