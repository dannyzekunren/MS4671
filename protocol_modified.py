from opentrons import protocol_api

# Protocol metadata - required for all protocols
metadata = {
    'protocolName': 'Basic Liquid Handling',
    'author': 'Student Name',
    'description': 'Simple protocol for learning OT-2 operation',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):
    """
    This function defines what the robot will do.
    It's called automatically when the protocol runs.
    """
    
    # 1. Load labware (define what equipment is on the deck)
    # Slot numbers 1-11 refer to positions on the robot deck
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '1')
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '11')
    reservoir = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '3')
    
    # 2. Load pipette (define which pipette to use)
    # 'right' or 'left' refers to the pipette mount position
    pipette = protocol.load_instrument(
        'p300_single_gen2', 
        'left', 
        tip_racks=[tiprack]
    )
    
    # 3. Protocol steps (define the liquid handling operations)
    
    # Pick up a tip
    pipette.pick_up_tip()
    
    # Aspirate 20μL from reservoir well A1
    pipette.aspirate(20, reservoir['A3'])
    
    # Dispense 20μL to plate well A1
    pipette.dispense(20, plate['A1'])
    
    # Repeat for multiple wells
    for well in ['A2', 'A3', 'A4', 'A5', 'A6']:
        pipette.aspirate(20, reservoir['A3'])
        pipette.dispense(20, plate[well])
    
    # Drop the tip when finished
    pipette.drop_tip()