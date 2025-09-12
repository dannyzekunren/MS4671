# Example of how to use the updated BO loop without CSV upload to OT2
# This shows how to integrate the new protocol generation system

import numpy as np
import pandas as pd
from protocol_generator import generate_protocol_from_dataframe, update_csv_data_handler

# Simulate BO loop with multiple iterations
def run_bo_loop_example():
    """
    Example of running BO loop with dynamic protocol generation
    """
    
    # Target RGB color to match
    RGB_ref = np.array([128, 56, 200])
    print(f"🎯 Target RGB Color: R={RGB_ref[0]}, G={RGB_ref[1]}, B={RGB_ref[2]}")
    
    # Simulate multiple BO iterations
    for iteration in range(3):
        print(f"\n{'='*50}")
        print(f"🔄 BO ITERATION {iteration}")
        print(f"{'='*50}")
        
        # Create sample data for this iteration (in real BO, this would come from optimizer)
        if iteration == 0:
            # Initial data from BO_R0.csv
            csv_file = f"./data/BO_R{iteration}.csv"
        else:
            # Generate new BO suggestions (simulated)
            sample_data = generate_sample_bo_data(iteration)
            csv_file = f"./data/BO_R{iteration}.csv"
            sample_data.to_csv(csv_file, index=False)
            print(f"📊 Generated new BO data for iteration {iteration}")
        
        # Process the CSV and generate protocol
        print(f"📂 Processing: {csv_file}")
        csv_data = update_csv_data_handler(csv_file)
        
        if csv_data is not None:
            # The protocol file is automatically generated
            protocol_file = f"color_mixing_BO{iteration}.py"
            
            print(f"✅ Iteration {iteration} complete!")
            print(f"📄 Protocol ready: {protocol_file}")
            print(f"🧪 Experiments in this batch: {len(csv_data)}")
            
            # Here you would normally:
            # 1. Upload the protocol to OT2
            # 2. Run the experiments
            # 3. Capture images and analyze RGB
            # 4. Feed results back to BO optimizer
            
        else:
            print(f"❌ Failed to process iteration {iteration}")
            break

def generate_sample_bo_data(iteration):
    """Generate sample BO data for testing"""
    
    # Simulate BO suggesting new experiments
    np.random.seed(42 + iteration)  # For reproducible results
    
    n_experiments = 3 + iteration  # Increase experiments each iteration
    
    data = {
        'colorA': np.random.uniform(20, 150, n_experiments).round(1),
        'colorB': np.random.uniform(80, 180, n_experiments).round(1),
        'colorC': np.random.uniform(50, 200, n_experiments).round(1),
        'DispensePos': [f"{chr(65 + i//12)}{1 + i%12}" for i in range(n_experiments)]
    }
    
    return pd.DataFrame(data)

def demonstrate_protocol_content():
    """Show the difference between generated protocols"""
    
    print("\n🔍 PROTOCOL CONTENT COMPARISON")
    print("="*60)
    
    # Check if we have generated protocols
    import os
    protocols = [f for f in os.listdir('.') if f.startswith('color_mixing_BO') and f.endswith('.py')]
    
    for protocol in sorted(protocols)[:2]:  # Show first 2 protocols
        print(f"\n📄 {protocol}:")
        print("-" * 40)
        
        with open(protocol, 'r') as f:
            lines = f.readlines()
            
        # Find and show the BO_DATA section
        in_data_section = False
        data_lines = []
        
        for line in lines:
            if "# BO ITERATION DATA" in line:
                in_data_section = True
                data_lines.append(line.strip())
            elif in_data_section and line.strip().startswith('}'):
                data_lines.append(line.strip())
                break
            elif in_data_section:
                data_lines.append(line.strip())
        
        for line in data_lines[:10]:  # Show first 10 lines of data section
            print(f"  {line}")
        if len(data_lines) > 10:
            print(f"  ... ({len(data_lines)-10} more lines)")

if __name__ == "__main__":
    print("🧪 BO LOOP EXAMPLE WITH DYNAMIC PROTOCOL GENERATION")
    print("="*60)
    
    # Run the example
    run_bo_loop_example()
    
    # Show protocol differences
    demonstrate_protocol_content()
    
    print(f"\n✅ Example complete!")
    print(f"📁 Generated protocol files are ready for OT2 upload")
    print(f"🔄 Each iteration has its own protocol with embedded data")
