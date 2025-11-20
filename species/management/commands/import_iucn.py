import pandas as pd
from django.core.management.base import BaseCommand
from species.models import Species
import os


class Command(BaseCommand):
    help = 'Import IUCN species data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='IUCN.xlsx',
            help='Path to the IUCN Excel file'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        # If relative path, make it relative to the project root
        if not os.path.isabs(file_path):
            # Go up from species/management/commands to project root (Manim folder)
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            file_path = os.path.join(base_dir, file_path)
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        self.stdout.write(f'Reading data from {file_path}...')
        
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Map status codes
        status_map = {
            'CR': 'CR',
            'EN': 'EN',
            'VU': 'VU',
            'NT': 'NT',
            'LC': 'LC',
            'DD': 'DD',
            'EW': 'EW',
            'EX': 'EX',
        }
        
        created_count = 0
        updated_count = 0
        
        for index, row in df.iterrows():
            # Convert status to uppercase for mapping
            status = str(row['Status']).strip().upper() if pd.notna(row['Status']) else 'DD'
            status = status_map.get(status, 'DD')
            
            # Prepare the data
            species_data = {
                'animal_name': str(row['Animal Name']).strip(),
                'status': status,
                'pop_size': str(row['Pop Size']) if pd.notna(row['Pop Size']) else None,
                'trend': str(row['Trend']).strip() if pd.notna(row['Trend']) else None,
                'decline_rate': float(row['Decline Rate (%)']) if pd.notna(row['Decline Rate (%)']) else None,
                'range_size': str(row['Range Size (km²)']) if pd.notna(row['Range Size (km²)']) else None,
                'locations': str(row['Locations']) if pd.notna(row['Locations']) else None,
                'fragmented': str(row['Fragmented']) if pd.notna(row['Fragmented']) else None,
                'threats': str(row['Threats']) if pd.notna(row['Threats']) else None,
                'extinct_prob': float(row['Extinct Prob (%)']) if pd.notna(row['Extinct Prob (%)']) else None,
            }
            
            # Create or update the species
            species, created = Species.objects.update_or_create(
                animal_name=species_data['animal_name'],
                defaults=species_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {species.animal_name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: {species.animal_name}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nImport complete! Created: {created_count}, Updated: {updated_count}'
        ))
