"""
Protocol Generator for Bayesian Optimization Color Mixing
Generates dynamic protocol files with embedded data for each BO iteration
"""
import pandas as pd
import os
import json
from typing import Dict, List, Union

def generate_protocol_from_csv(csv_file_path: str, iteration_number: int, output_dir: str = ".") -> str:
    """
    Generate a protocol file from CSV data for a specific BO iteration
    
    Args:
        csv_file_path: Path to the CSV file containing BO data
        iteration_number: BO iteration number (e.g., 1 for BO_R1)
        output_dir: Directory to save the protocol file
        
    Returns:
        str: Path to the generated protocol file
    """
    
    # Read the CSV data
    try:
        df = pd.read_csv(csv_file_path)
        print(f"✅ Loaded CSV data from {csv_file_path}")
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return None
    
    # Convert DataFrame to dictionary format
    bo_data = {
        'colorA': df['colorA'].tolist(),
        'colorB': df['colorB'].tolist(), 
        'colorC': df['colorC'].tolist(),
        'DispensePos': df['DispensePos'].tolist()
    }
    
    # Generate the protocol filename
    protocol_filename = f"color_mixing_BO{iteration_number}.py"
    protocol_path = os.path.join(output_dir, protocol_filename)
    
    # Read the base protocol template
    base_protocol_path = "color_mixing.py"
    try:
        with open(base_protocol_path, 'r') as f:
            protocol_content = f.read()
    except Exception as e:
        print(f"❌ Error reading base protocol: {e}")
        return None
    
    # Replace the BO_DATA section with actual data
    data_section = f"""    # BO ITERATION DATA - BO{iteration_number}
    BO_DATA = {json.dumps(bo_data, indent=8).replace('{', '{\n        ').replace('}', '\n    }')}"""
    
    # Find and replace the BO_DATA section
    import re
    pattern = r'    # BO ITERATION DATA - WILL BE REPLACED DYNAMICALLY\n    BO_DATA = \{[^}]+\}'
    updated_content = re.sub(pattern, data_section, protocol_content, flags=re.MULTILINE | re.DOTALL)
    
    # Update the protocol name in metadata
    updated_content = updated_content.replace(
        "'protocolName': 'Color Liquid Mixing - Bayesian Optimization',",
        f"'protocolName': 'Color Liquid Mixing - BO Iteration {iteration_number}',"
    )
    
    # Save the generated protocol
    try:
        with open(protocol_path, 'w') as f:
            f.write(updated_content)
        print(f"✅ Generated protocol file: {protocol_path}")
        return protocol_path
    except Exception as e:
        print(f"❌ Error writing protocol file: {e}")
        return None

def generate_protocol_from_dataframe(df: pd.DataFrame, iteration_number: int, output_dir: str = ".") -> str:
    """
    Generate a protocol file directly from a DataFrame for a specific BO iteration
    
    Args:
        df: DataFrame containing BO data with columns: colorA, colorB, colorC, DispensePos
        iteration_number: BO iteration number
        output_dir: Directory to save the protocol file
        
    Returns:
        str: Path to the generated protocol file
    """
    
    # Convert DataFrame to dictionary format
    bo_data = {
        'colorA': df['colorA'].tolist(),
        'colorB': df['colorB'].tolist(), 
        'colorC': df['colorC'].tolist(),
        'DispensePos': df['DispensePos'].tolist()
    }
    
    print(f"✅ Processing DataFrame data for BO{iteration_number}")
    print(f"Data shape: {df.shape}")
    print(f"Experiments: {len(bo_data['colorA'])}")
    
    # Generate the protocol filename
    protocol_filename = f"color_mixing_BO{iteration_number}.py"
    protocol_path = os.path.join(output_dir, protocol_filename)
    
    # Read the base protocol template
    base_protocol_path = "color_mixing.py"
    try:
        with open(base_protocol_path, 'r') as f:
            protocol_content = f.read()
    except Exception as e:
        print(f"❌ Error reading base protocol: {e}")
        return None
    
    # Replace the BO_DATA section with actual data
    data_section = f"""    # BO ITERATION DATA - BO{iteration_number}
    BO_DATA = {json.dumps(bo_data, indent=8).replace('{', '{\n        ').replace('}', '\n    }')}"""
    
    # Find and replace the BO_DATA section
    import re
    pattern = r'    # BO ITERATION DATA - WILL BE REPLACED DYNAMICALLY\n    BO_DATA = \{[^}]+\}'
    updated_content = re.sub(pattern, data_section, protocol_content, flags=re.MULTILINE | re.DOTALL)
    
    # Update the protocol name in metadata
    updated_content = updated_content.replace(
        "'protocolName': 'Color Liquid Mixing - Bayesian Optimization',",
        f"'protocolName': 'Color Liquid Mixing - BO Iteration {iteration_number}',"
    )
    
    # Save the generated protocol
    try:
        with open(protocol_path, 'w') as f:
            f.write(updated_content)
        print(f"✅ Generated protocol file: {protocol_path}")
        return protocol_path
    except Exception as e:
        print(f"❌ Error writing protocol file: {e}")
        return None

def update_csv_data_handler(csv_file_path: str, robot_filename: str = None) -> str:
    """
    Updated version of upload_csv_data that generates protocol files instead of uploading CSV
    
    Args:
        csv_file_path: Path to the CSV file
        robot_filename: Not used anymore, kept for compatibility
        
    Returns:
        str: Path to the generated protocol file
    """
    try:
        # Extract iteration number from filename (e.g., BO_R1.csv -> 1)
        import re
        match = re.search(r'BO_R(\d+)', csv_file_path)
        if match:
            iteration_number = int(match.group(1))
        else:
            iteration_number = 0  # Default to 0 if no iteration found
        
        # Generate protocol file from CSV
        protocol_path = generate_protocol_from_csv(csv_file_path, iteration_number)
        
        if protocol_path:
            # Also load and display the data for verification
            df = pd.read_csv(csv_file_path)
            print(f"✅ CSV data processed successfully!")
            print(f"Data shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print("First few rows:")
            print(df.head())
            print(f"📄 Protocol file generated: {protocol_path}")
            return protocol_path
        else:
            return None
            
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_file_path}")
        return None
    except Exception as e:
        print(f"❌ Error processing CSV: {e}")
        return None

# Example usage and testing functions
def test_protocol_generation():
    """Test the protocol generation with sample data"""
    
    # Test with the existing BO_R0.csv
    csv_path = "./data/BO_R0.csv"
    protocol_path = generate_protocol_from_csv(csv_path, 0)
    
    if protocol_path:
        print(f"✅ Test successful! Generated: {protocol_path}")
    else:
        print("❌ Test failed!")
        
    return protocol_path

def create_sample_bo_data():
    """Create sample BO data for testing"""
    
    # Sample data for BO_R1
    bo_r1_data = {
        'colorA': [120.5, 85.3, 45.7, 95.2],
        'colorB': [110.8, 135.6, 98.4, 125.1],
        'colorC': [75.2, 88.9, 145.3, 102.7],
        'DispensePos': ['A1', 'A2', 'A3', 'A4']
    }
    
    # Create DataFrame and save as CSV
    df = pd.DataFrame(bo_r1_data)
    csv_path = "./data/BO_R1.csv"
    df.to_csv(csv_path, index=False)
    print(f"✅ Created sample BO_R1.csv at {csv_path}")
    
    # Generate protocol from this data
    protocol_path = generate_protocol_from_csv(csv_path, 1)
    return protocol_path

if __name__ == "__main__":
    # Test the protocol generation
    print("🧪 Testing protocol generation...")
    test_protocol_generation()
    
    # Create and test with sample BO_R1 data
    print("\n🧪 Creating sample BO_R1 data...")
    create_sample_bo_data()
