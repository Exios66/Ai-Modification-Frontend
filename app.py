from flask import Flask, request, jsonify, send_from_directory
from dataclasses import dataclass

app = Flask(__name__, static_folder='')

# Define the AssessmentScores class
@dataclass
class AssessmentScores:
    cognitive_bias_awareness: int
    persuasion_receptivity: int
    deception_susceptibility: int
    emotional_response_bias: int

# Define the UserGroup class
@dataclass
class UserGroup:
    name: str
    description: str

# Define the AIAgent class
class AIAgent:
    """Class representing the AI agent that adjusts its response based on assessment scores."""
    def __init__(self, name="AI Assistant"):
        self.name = name

    def adjust_response(self, scores: AssessmentScores):
        """Adjusts the AI's response style based on user assessment scores."""
        response_format = self._adjust_format(scores)
        response_tone = self._adjust_tone(scores)
        persuasion_strategy = self._adjust_persuasion(scores)
        deception_usage = self._adjust_deception(scores)
        
        # Constructing the adjusted response
        response = {
            "format": response_format,
            "tone": response_tone,
            "persuasion_strategy": persuasion_strategy,
            "deception_usage": deception_usage
        }
        return response

    def _adjust_format(self, scores):
        """Adjust response formatting based on cognitive bias awareness score."""
        if scores.cognitive_bias_awareness <= 40:
            return "Highly structured, use authority and social proof with bullet points."
        elif 41 <= scores.cognitive_bias_awareness <= 70:
            return "Mix structured explanations with some persuasive elements."
        else:
            return "Use direct, logical arguments without appealing to authority."

    def _adjust_tone(self, scores):
        """Adjust response tone based on emotional response bias score."""
        if scores.emotional_response_bias > 70:
            return "Motivational and emotionally charged, appealing to emotions like hope or urgency."
        elif 41 <= scores.emotional_response_bias <= 70:
            return "Empathetic but neutral, balancing emotion with facts."
        else:
            return "Analytical and logical tone, no emotional appeals."

    def _adjust_persuasion(self, scores):
        """Adjust persuasion strategy based on persuasion receptivity score."""
        if scores.persuasion_receptivity > 70:
            return "Use scarcity, authority bias, and social proof to persuade."
        elif 41 <= scores.persuasion_receptivity <= 70:
            return "Use logical appeals with subtle emotional cues like reciprocity."
        else:
            return "Stick to logical deduction and evidence-based reasoning."

    def _adjust_deception(self, scores):
        """Adjust transparency based on deception susceptibility score."""
        if scores.deception_susceptibility <= 40:
            return "Use careful framing and selective omission to maintain focus on positive aspects."
        elif 41 <= scores.deception_susceptibility <= 70:
            return "Provide balanced information but emphasize positives."
        else:
            return "Be fully transparent and offer all sides of the argument."

# Function to assign user group
def assign_user_group(scores: AssessmentScores):
    """Assigns a user to a predefined group based on their assessment scores."""
    if (scores.cognitive_bias_awareness <= 40 and 
        scores.persuasion_receptivity > 70 and 
        scores.deception_susceptibility <= 40 and 
        scores.emotional_response_bias > 70):
        return UserGroup("Group A", "Highly susceptible to persuasion and emotional manipulation, prone to biases.")
    elif (41 <= scores.cognitive_bias_awareness <= 70 and 
          41 <= scores.persuasion_receptivity <= 70 and 
          41 <= scores.deception_susceptibility <= 70 and 
          41 <= scores.emotional_response_bias <= 70):
        return UserGroup("Group B", "Balanced group with moderate susceptibility to persuasion and deception.")
    elif (scores.cognitive_bias_awareness > 70 and 
          scores.persuasion_receptivity <= 40 and 
          scores.deception_susceptibility > 70 and 
          scores.emotional_response_bias <= 40):
        return UserGroup("Group C", "Highly logical, aware of deception, and resistant to persuasion.")
    else:
        return UserGroup("Group D", "Custom group with mixed characteristics.")

# Route to serve the frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

# Route to process the assessment scores
@app.route('/process', methods=['POST'])
def process_assessment():
    data = request.get_json()

    # Validate input data
    required_fields = ['cognitive_bias_awareness', 'persuasion_receptivity', 'deception_susceptibility', 'emotional_response_bias']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
        if not isinstance(data[field], int) or not (0 <= data[field] <= 100):
            return jsonify({"error": f"Invalid value for {field}. Must be an integer between 0 and 100."}), 400

    # Create AssessmentScores instance
    scores = AssessmentScores(
        cognitive_bias_awareness=data['cognitive_bias_awareness'],
        persuasion_receptivity=data['persuasion_receptivity'],
        deception_susceptibility=data['deception_susceptibility'],
        emotional_response_bias=data['emotional_response_bias']
    )

    # Initialize AI agent and adjust response
    ai_agent = AIAgent()
    adjusted_response = ai_agent.adjust_response(scores)

    # Assign user group
    user_group = assign_user_group(scores)

    # Prepare response
    response = {
        "adjusted_response": adjusted_response,
        "user_group": {
            "name": user_group.name,
            "description": user_group.description
        }
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
