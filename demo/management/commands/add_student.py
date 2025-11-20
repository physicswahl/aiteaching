from django.core.management.base import BaseCommand
from demo.models import Student
import math

class Command(BaseCommand):
    help = 'Add one student with math=5, reading_writing=1'
    
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
    
    def neural_network(self, x1, x2):
        """Same neural network as in populate_students"""
        w11 = 2.0
        w21 = 2.0
        w12 = 5.0
        w22 = -2.0
        b1 = -15.7
        b2 = -0.3
        wo1 = 3.0
        wo2 = 2.4
        bo = -2.9
        
        h1 = self.sigmoid(w11 * x1 + w21 * x2 + b1)
        h2 = self.sigmoid(w12 * x1 + w22 * x2 + b2)
        
        z = wo1 * h1 + wo2 * h2 + bo
        y = self.sigmoid(z)
        
        return y <= 0.5
    
    def handle(self, *args, **kwargs):
        # Students to add
        students_to_add = [
            {"name": "Student A", "math": 2.5, "reading_writing": 5.5},
            {"name": "Student B", "math": 4.0, "reading_writing": 2.9}
        ]
        
        for student_data in students_to_add:
            name = student_data["name"]
            math = student_data["math"]
            reading_writing = student_data["reading_writing"]
            
            # Calculate eligibility using neural network
            eligible = self.neural_network(math, reading_writing)
            
            # Create the student
            Student.objects.create(
                name=name,
                math_performance=math,
                reading_writing_performance=reading_writing,
                eligible_for_support=eligible
            )
            
            eligibility_text = "Eligible for support" if eligible else "Not eligible for support"
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully added student: {name}\n'
                    f'Math: {math}, Reading/Writing: {reading_writing}\n'
                    f'Classification: {eligibility_text}\n'
                )
            )
