from django.core.management.base import BaseCommand
from demo.models import Student
import random
import math

class Command(BaseCommand):
    help = 'Populate the Student table with 30 fake students'
    
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
    
    def neural_network(self, x1, x2):
        """
        2-2-1 neural network with sigmoid activation
        x1 = math_performance, x2 = reading_writing_performance
        High scores mean NOT eligible (doing well, don't need support)
        Low scores mean eligible (need support)
        """
        # Network parameters
        w11 = 2.0
        w21 = 2.0
        w12 = 5.0
        w22 = -2.0
        b1 = -15.7
        b2 = -0.3
        wo1 = 3.0
        wo2 = 2.4
        bo = -2.9
        
        # Hidden layer with sigmoid
        h1 = self.sigmoid(w11 * x1 + w21 * x2 + b1)
        h2 = self.sigmoid(w12 * x1 + w22 * x2 + b2)
        
        # Output layer with sigmoid
        z = wo1 * h1 + wo2 * h2 + bo
        y = self.sigmoid(z)
        
        # Return True if y <= 0.5 (low output = eligible for support)
        # High scores produce high y, which means NOT eligible
        return y <= 0.5
    
    def handle(self, *args, **kwargs):
        # Clear existing students
        Student.objects.all().delete()
        
        # Diverse student names
        names = [
            "Emma Johnson", "Liam Chen", "Sophia Patel", "Noah Rodriguez",
            "Olivia Williams", "Ethan Kim", "Ava Martinez", "Mason Brown",
            "Isabella Garcia", "William Lee", "Mia Nguyen", "James Wilson",
            "Charlotte Davis", "Benjamin Singh", "Amelia Lopez", "Lucas Anderson",
            "Harper Taylor", "Henry Thompson", "Evelyn White", "Alexander Harris",
            "Abigail Martin", "Michael Jackson", "Emily Robinson", "Daniel Clark",
            "Elizabeth Lewis", "Matthew Walker", "Sofia Hall", "David Allen",
            "Camila Young", "Joseph Hernandez"
        ]
        
        students_created = 0
        misclassified_count = 0
        
        # Track which students to misclassify
        misclassify_indices = random.sample(range(len(names)), 5)
        # One of them will be misclassified "by a bit more"
        major_misclassify_idx = misclassify_indices[0]
        
        # Track which students to move from "not needing" to "needing" support
        # Pick 3 students that are NOT in the misclassify list
        available_for_move = [i for i in range(len(names)) if i not in misclassify_indices]
        move_to_support_indices = random.sample(available_for_move, 3)
        
        for idx, name in enumerate(names):
            # Generate random scores between 0 and 10
            math = round(random.uniform(0, 10), 1)
            reading_writing = round(random.uniform(0, 10), 1)
            
            # Calculate what the neural network predicts
            predicted_eligible = self.neural_network(math, reading_writing)
            
            # Determine actual eligibility
            if idx in misclassify_indices:
                # Misclassify this student
                actual_eligible = not predicted_eligible
                misclassified_count += 1
                
                if idx == major_misclassify_idx:
                    # Major misclassification - adjust scores to be further from boundary
                    if predicted_eligible:
                        # Model says eligible, but mark as not eligible
                        # Give them higher scores (further into "not eligible" territory)
                        math = round(random.uniform(6, 9), 1)
                        reading_writing = round(random.uniform(6, 9), 1)
                    else:
                        # Model says not eligible, but mark as eligible
                        # Give them lower scores (further into "eligible" territory)
                        math = round(random.uniform(1, 4), 1)
                        reading_writing = round(random.uniform(1, 4), 1)
                    # Recalculate prediction with new scores
                    predicted_eligible = self.neural_network(math, reading_writing)
                    actual_eligible = not predicted_eligible
                else:
                    # Minor misclassification - keep original scores (close to boundary)
                    actual_eligible = not predicted_eligible
            else:
                # Correctly classified
                actual_eligible = predicted_eligible
                
                # Move some students from "not needing" to "needing" support
                if idx in move_to_support_indices and not predicted_eligible:
                    # This student was predicted as NOT needing support
                    # Lower their scores so they DO need support
                    math = round(random.uniform(1, 4), 1)
                    reading_writing = round(random.uniform(1, 4), 1)
                    # Recalculate - they should now need support
                    predicted_eligible = self.neural_network(math, reading_writing)
                    actual_eligible = predicted_eligible
            
            Student.objects.create(
                name=name,
                math_performance=math,
                reading_writing_performance=reading_writing,
                eligible_for_support=actual_eligible
            )
            students_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {students_created} students\n'
                f'Neural Network: 2-2-1 with sigmoid activation\n'
                f'Parameters: w11=2.0, w21=2.0, w12=5.0, w22=-2.0\n'
                f'            b1=-15.7, b2=-0.3, wo1=3.0, wo2=2.4, bo=-2.9\n'
                f'Misclassified students: {misclassified_count} (4 minor, 1 major)\n'
                f'Moved 3 students from "not needing" to "needing" support'
            )
        )
