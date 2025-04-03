import streamlit as st
import pickle
import numpy as np

# Load trained model
with open("bridge_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Load trained scaler
with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

with open("algo2.pkl", "rb") as model_file:
    algo2 = pickle.load(model_file)

# Load trained scaler
with open("scaler2.pkl", "rb") as scaler_file:
    scaler2 = pickle.load(scaler_file)

st.markdown("""
    <h1 style='text-align: center;'>Bridge Condition Prediction using AI</h1>
    <h3 style='text-align: center; font-style: italic;'>by Fred Fayad</h3>
""", unsafe_allow_html=True)

# Add the informational statement with an icon
st.markdown("""
    <p style="font-size:16px;">
        🔍 <strong>This result is based on a machine learning technique and is guaranteed at 75% using a database composed of 400,000 bridges.</strong>
    </p>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='text-align: left;'>📌 Input Features</h2>", unsafe_allow_html=True)

# Define Route Type mapping
route_type_map = {
    "Interstate highway": 1,
    "U.S. numbered highway": 2,
    "State highway": 3,
    "County highway": 4,
    "City street": 5,
    "Federal lands road": 6,
    "State lands road": 7,
    "Other (include toll roads not otherwise indicated or identified above)": 8
}
route_type = st.sidebar.selectbox("Route Type", list(route_type_map.keys()))
# Convert selected value to numerical representation
route_type_encoded = route_type_map[route_type]
level_of_service_map = {
    "None of the below": 0,
    "Mainline": 1,
    "Alternate": 2,
    "Bypass": 3,
    "Spur": 4,
    "Business": 6,
    "Ramp, Wye, Connector, etc.": 7,
    "Service and/or unclassified frontage road": 8
}
level_of_service = st.sidebar.selectbox("Level of Service", list(level_of_service_map.keys()))
level_of_service_encoded = level_of_service_map[level_of_service]
position_on_highway_map = {
    "Inventory Route is not on the Base Network": 0,
    "Inventory Route is on the Base Network": 1
}
position_on_highway = st.sidebar.selectbox("Position on Highway Network", list(position_on_highway_map.keys()))
position_on_highway_encoded = position_on_highway_map[position_on_highway]
location = st.sidebar.selectbox("Location", ["Rural", "Sub-Urban", "Urban"])
# Convert user input to boolean values for each location type
location_map = {
    "Rural": [True, False, False],   # Location_Rural = True, Location_Sub-Urban = False, Location_Urban = False
    "Sub-Urban": [False, True, False],  # Location_Rural = False, Location_Sub-Urban = True, Location_Urban = False
    "Urban": [False, False, True]  # Location_Rural = False, Location_Sub-Urban = False, Location_Urban = True
}

# Get the encoded values
location_encoded = location_map[location]
location_rural, location_sub_urban, location_urban = location_encoded

functional_classification_map = {
    "Rural - Principal Arterial - Interstate": 1,
    "Rural - Principal Arterial - Other": 2,
    "Rural - Minor Arterial": 6,
    "Rural - Major Collector": 7,
    "Rural - Minor Collector": 8,
    "Rural - Local": 9,
    "Urban - Principal Arterial - Interstate": 11,
    "Urban - Principal Arterial - Other Freeways or Expressways": 12,
    "Urban - Other Principal Arterial": 14,
    "Urban - Minor Arterial": 16,
    "Urban - Collector": 17,
    "Urban - Local": 19
}
functional_classification = st.sidebar.selectbox("Functional Classification", list(functional_classification_map.keys()))
functional_classification_encoded = functional_classification_map[functional_classification]
bridge_age = st.sidebar.number_input("Bridge Age from initial construction (years)", min_value=0, max_value=250, value=50, step=1)
lanes_on = st.sidebar.number_input("Number of lanes on the structure", min_value=1, max_value=82, value=5, step=1)
lanes_under = st.sidebar.number_input("Number of lanes under the structure", min_value=0, max_value=99, value=5, step=1)
adt = st.sidebar.number_input("Average Daily Traffic (cars)", min_value=0, max_value=999999, value=5000, step=1)
# Define Design Load mapping
design_load_map = {
    "Other or Unknown (describe on inspection reporting form)": 0,
    "M 9": 1,
    "M 13.5": 2,
    "MS 13.5": 3,
    "M 18": 4,
    "MS 18": 5,
    "MS 18+Mod": 6,
    "Pedestrian": 7,
    "Railroad": 8,
    "MS 22.5": 9
}
design_load = st.sidebar.selectbox("Design Load", list(design_load_map.keys()))
design_load_encoded = design_load_map[design_load]
approachroadwaywidth = st.sidebar.number_input("Approach roadway width", min_value=0, max_value=999, value=500, step=1)
historical_significance_map = {
    "Bridge is on the National Register of Historic Places": 1,
    "Bridge is eligible for the National Register of Historic Places": 2,
    "Bridge is possibly eligible for the National Register of Historic Places (requires further investigation) or is on a State or local historic register": 3,
    "Historical significance is not determinable at this time": 4,
    "Bridge is not eligible for the National Register of Historic Places": 5
}
historical_significance = st.sidebar.selectbox("Historical Significance", list(historical_significance_map.keys()))
historical_significance_encoded = historical_significance_map[historical_significance]
actual_operational_status_map = {
    "Open, no restriction": 0,
    "Open, posting recommended but not legally implemented": 1,
    "Open, would be posted or closed except for temporary shoring": 2,
    "Open, temporary structure in place to carry legal loads while original structure is closed and awaiting replacement or rehabilitation": 3,
    "New structure not yet open to traffic": 4,
    "Bridge closed to all traffic": 5,
    "Posted for load (may include other restrictions such as temporary bridges which are load posted)": 6,
    "Posted for other load-capacity restriction (speed, number of vehicles on bridge, etc.)": 7
}
actual_operational_status = st.sidebar.selectbox("Actual Operational Status", list(actual_operational_status_map.keys()))
actual_operational_status_encoded = actual_operational_status_map[actual_operational_status]
type_of_service_map = {
    "Highway": 1,
    "Railroad": 2,
    "Pedestrian-bicycle": 3,
    "Highway-railroad": 4,
    "Highway-pedestrian": 5,
    "Overpass structure at an interchange or second level of a multilevel interchange": 6,
    "Third level (Interchange)": 7,
    "Fourth level (Interchange)": 8,
    "Building or plaza": 9,
    "Other": 0
}
type_of_service = st.sidebar.selectbox("Type of Service on the Bridge", list(type_of_service_map.keys()))
type_of_service_encoded = type_of_service_map[type_of_service]
type_of_service_under_map = {
    "Highway, with or without pedestrian": 1,
    "Railroad": 2,
    "Pedestrian-bicycle": 3,
    "Highway-railroad": 4,
    "Waterway": 5,
    "Highway-waterway": 6,
    "Railroad-waterway": 7,
    "Highway-waterway-railroad": 8,
    "Relief for waterway": 9,
    "Other": 0
}
type_of_service_under = st.sidebar.selectbox("Type of Service Under the Bridge", list(type_of_service_under_map.keys()))
type_of_service_under_encoded = type_of_service_under_map[type_of_service_under]
structural_material_map = {
    "Concrete": 1,
    "Concrete Continuous": 2,
    "Prestressed Concrete": 5,
    "Prestressed Concrete Continuous": 6
}
structural_material = st.sidebar.selectbox("Structural Material", list(structural_material_map.keys()))
structural_material_encoded = structural_material_map[structural_material]

materials = st.sidebar.multiselect(
    "Bridge Materials", 
    ["Composite", "Prestressed concrete", "Reinforced concrete", "Steel", "Timber"]
)
material_map = {
    "Composite": "Material_Composite",
    "Prestressed concrete": "Material_Prestressed concrete",
    "Reinforced concrete": "Material_Reinforced concrete",
    "Steel": "Material_Steel",
    "Timber": "Material_Timber"
}

# Initialize the encoded materials as False
encoded_materials = {
    "Material_Composite": False,
    "Material_Prestressed concrete": False,
    "Material_Reinforced concrete": False,
    "Material_Steel": False,
    "Material_Timber": False
}

# Update the encoded values based on user input
for material_type in materials:
    encoded_materials[material_map[material_type]] = True

structural_system_map = {
    "Slab": "01",
    "Stringer/Multi-beam or Girder": "02",
    "Girder and Floorbeam System": "03",
    "Tee Beam": "04",
    "Box Beam or Girders - Multiple": "05",
    "Box Beam or Girders - Single or Spread": "06",
    "Frame (except frame culverts)": "07",
    "Orthotropic": "08",
    "Truss - Deck": "09",
    "Truss - Thru": "10",
    "Arch - Deck": "11",
    "Arch - Thru": "12",
    "Suspension": "13",
    "Stayed Girder": "14",
    "Movable - Lift": "15",
    "Movable - Bascule": "16",
    "Movable - Swing": "17",
    "Tunnel": "18",
    "Culvert (includes frame culverts)": "19",
    "Mixed types": "20",
    "Segmental Box Girder": "21",
    "Channel Beam": "22",
    "Other": "00"
}
structural_system = st.sidebar.selectbox("Structural System", list(structural_system_map.keys()))
structural_system_encoded = structural_system_map[structural_system]

system = st.sidebar.multiselect(
    "Bridge System Type", 
    ["Box-girder", "Cable-stayed", "I-girder", "Suspension", "Truss/Arch"]
)
system_map = {
    "Box-girder": "System_Box-girder",
    "Cable-stayed": "System_Cable-stayed",
    "I-girder": "System_I-girder",
    "Suspension": "System_Suspension",
    "Truss/Arch": "System_Truss/Arch"
}

# Initialize the encoded features as False
encoded_systems = {
    "System_Box-girder": False,
    "System_Cable-stayed": False,
    "System_I-girder": False,
    "System_Suspension": False,
    "System_Truss/Arch": False
}

# Update the encoded values based on user input
for system_type in system:
    encoded_systems[system_map[system_type]] = True

numofspans = st.sidebar.number_input("Number of Spans", min_value=0, max_value=607, value=5, step=1)
lenofmaxspans = st.sidebar.number_input("Length of maximum span (meters)", min_value=0, max_value=2327, value=100, step=1)
totalstrlen = st.sidebar.number_input("Total Structure Length (meters)", min_value=0, max_value=23382, value=100, step=1)
deckwidth = st.sidebar.number_input("Deck Width (meters)", min_value=0, max_value=999, value=100, step=1)

restriction_map = {
    "Restriction above the bridge": 0,
    "No restriction above the bridge": 1
}
restriction = st.sidebar.selectbox("Restriction above the bridge", list(restriction_map.keys()))
restriction_encoded = restriction_map[restriction]
vertclrabov = st.sidebar.number_input("Vertical clearance above the bridge (meters) PS: Leave if NA", min_value=0, max_value=31, value=31, step=1)
structure_beneath_map = {
    "Highway beneath structure": 0,
    "Railroad beneath structure": 1,
    "Feature not a highway or railroad": 2
}
structure_beneath = st.sidebar.selectbox("Type of Structure Beneath the Bridge", list(structure_beneath_map.keys()))
structure_beneath_encoded = structure_beneath_map[structure_beneath]
vertclrbelow = st.sidebar.number_input("Vertical clearance under the bridge (meters)", min_value=0, max_value=99, value=31, step=1)
direction_traffic_map = {
    "Highway traffic not carried": 0,
    "1-way traffic": 1,
    "2-way traffic": 2,
    "One lane bridge for 2-way traffic": 3
}
direction_traffic = st.sidebar.selectbox("Direction of Traffic", list(direction_traffic_map.keys()))
direction_traffic_encoded = direction_traffic_map[direction_traffic]
bridge_age_special = st.sidebar.number_input("Bridge Age from reconstruction (years) PS:0 if NA", min_value=0, max_value=250, value=50, step=1)
deck_structure_map = {
    "Concrete Cast-in-Place": 1,
    "Concrete Precast Panels": 2,
    "Open Grating": 3,
    "Closed Grating": 4,
    "Steel plate (includes orthotropic)": 5,
    "Corrugated Steel": 6,
    "Aluminum": 7,
    "Wood or Timber": 8,
    "Other": 9,
    "Not applicable": "N"
}
deck_structure = st.sidebar.selectbox("Deck Structure Type", list(deck_structure_map.keys()))
deck_structure_encoded = deck_structure_map[deck_structure]
wearing_surface_map = {
    "Monolithic Concrete": 1,
    "Integral Concrete": 2,
    "Latex Concrete or similar additive": 3,
    "Low Slump Concrete": 4,
    "Epoxy Overlay": 5,
    "Bituminous": 6,
    "Wood or Timber": 7,
    "Gravel": 8,
    "Other": 9,
    "None": 0,
}
membrane_type_map = {
    "Built-up": 1,
    "Preformed Fabric": 2,
    "Epoxy": 3,
    "Unknown": 8,
    "Other": 9,
    "None": 0,
}

deck_protection_map = {
    "Epoxy Coated Reinforcing": 1,
    "Galvanized Reinforcing": 2,
    "Other Coated Reinforcing": 3,
    "Cathodic Protection": 4,
    "Polymer Impregnated": 6,
    "Internally Sealed": 7,
    "Unknown": 8,
    "Other": 9,
    "None": 0,
}
wearing_surface = st.sidebar.selectbox("Type of Wearing Surface", list(wearing_surface_map.keys()))
membrane_type = st.sidebar.selectbox("Type of Membrane", list(membrane_type_map.keys()))
deck_protection = st.sidebar.selectbox("Deck Protection", list(deck_protection_map.keys()))
wearing_surface_encoded = wearing_surface_map[wearing_surface]
membrane_type_encoded = membrane_type_map[membrane_type]
deck_protection_encoded = deck_protection_map[deck_protection]
adtruck = st.sidebar.number_input("Average Daily Truck Traffic (% of ADT)", min_value=0, max_value=99, value=5, step=1)
Futureadt = st.sidebar.number_input("Future Average Daily Traffic (cars)", min_value=0, max_value=999999, value=5000, step=1)
deckarea = st.sidebar.number_input("Deck Area (sqm)", min_value=0, max_value=350000, value=5000, step=1)
scour_criticality_map = {
    "Bridge not over waterway": 12,
    "Bridge with 'unknown' foundation that has not been evaluated for scour": 11,
    "Bridge over 'tidal' waters that has not been evaluated for scour, but considered low risk": 10,
    "Bridge foundations (including piles) on dry land well above flood water elevations": 9,
    "Bridge foundations determined to be stable for assessed or calculated scour conditions; scour is above top of footing": 8,
    "Countermeasures have been installed to correct a previously existing problem with scour. Bridge is no longer scour critical": 7,
    "Scour calculation/evaluation has not been made (bridge has not yet been evaluated for scour potential)": 6,
    "Bridge foundations determined to be stable for calculated scour conditions; scour within limits of footing or piles": 5,
    "Bridge foundations determined to be stable for calculated scour conditions; field review indicates action is required to protect exposed foundations from effects of additional erosion and corrosion": 4,
    "Bridge is scour critical; bridge foundations determined to be unstable for calculated scour conditions - Scour within limits of footing or piles OR below spread-footing base or pile tips": 3,
    "Bridge is scour critical; field review indicates that extensive scour has occurred at bridge foundations. Immediate action is required to provide scour countermeasures": 2,
    "Bridge is scour critical; field review indicates that failure of piers/abutments is imminent. Bridge is closed to traffic": 1,
    "Bridge is scour critical. Bridge has failed and is closed to traffic": 0
}
scour_criticality = st.sidebar.selectbox("Scour Criticality", list(scour_criticality_map.keys()))
scour_criticality_encoded = scour_criticality_map[scour_criticality]


damage_types = st.sidebar.multiselect(
    "Bridge Damage Types", 
    [
        "Collision", "Construction", "Earthquake", "Environmental Degradation", "Fire", "Flood", 
        "Misc", "Other", "Overload", "Scour", "Storm", "Wind"
    ]
)

# Mapping damage types to their corresponding feature names
damage_map = {
    "Collision": "Type_Collision",
    "Construction": "Type_Construction",
    "Earthquake": "Type_Earthquake",
    "Environmental Degradation": "Type_Environmental Degradation",
    "Fire": "Type_Fire",
    "Flood": "Type_Flood",
    "Misc": "Type_Misc",
    "Other": "Type_Other",
    "Overload": "Type_Overload",
    "Scour": "Type_Scour",
    "Storm": "Type_Storm",
    "Wind": "Type_Wind"
}

# Initialize encoded damage features as False (all features are False initially)
encoded_damage_types = {
    "Type_Collision": False,
    "Type_Construction": False,
    "Type_Earthquake": False,
    "Type_Environmental Degradation": False,
    "Type_Fire": False,
    "Type_Flood": False,
    "Type_Misc": False,
    "Type_Other": False,
    "Type_Overload": False,
    "Type_Scour": False,
    "Type_Storm": False,
    "Type_Wind": False
}

# Update encoded values based on user input
for damage_type in damage_types:
    encoded_damage_types[damage_map[damage_type]] = True


# Prepare input data (before scaling)
input_features = np.array([[
    route_type_encoded,
    level_of_service_encoded,
    position_on_highway_encoded,
    functional_classification_encoded,
    bridge_age,
    lanes_on,
    lanes_under,
    adt,
    design_load_encoded,
    approachroadwaywidth,
    historical_significance_encoded,
    actual_operational_status_encoded,
    type_of_service_encoded,
    type_of_service_under_encoded,
    structural_material_encoded,
    structural_system_encoded,
    numofspans,
    lenofmaxspans,
    totalstrlen,
    deckwidth,
    vertclrabov,
    structure_beneath_encoded,
    vertclrbelow,
    direction_traffic_encoded,
    bridge_age_special,
    deck_structure_encoded,
    wearing_surface_encoded,
    membrane_type_encoded,
    deck_protection_encoded,
    adtruck,
    scour_criticality_encoded,
    Futureadt,
    deckarea,
    restriction_encoded,
]])

# Apply scaling
input_scaled = scaler.transform(input_features)


input_features2 = np.array([[
    lenofmaxspans,
    bridge_age_special,
    lanes_on,
    location_rural, location_sub_urban, location_urban,
    encoded_systems["System_Box-girder"], encoded_systems["System_Cable-stayed"], 
    encoded_systems["System_I-girder"], encoded_systems["System_Suspension"], 
    encoded_systems["System_Truss/Arch"],
    encoded_materials["Material_Composite"], encoded_materials["Material_Prestressed concrete"], 
    encoded_materials["Material_Reinforced concrete"], encoded_materials["Material_Steel"], 
    encoded_materials["Material_Timber"],
    encoded_damage_types["Type_Collision"], encoded_damage_types["Type_Construction"],
    encoded_damage_types["Type_Earthquake"], encoded_damage_types["Type_Environmental Degradation"],
    encoded_damage_types["Type_Fire"], encoded_damage_types["Type_Flood"],
    encoded_damage_types["Type_Misc"], encoded_damage_types["Type_Other"],
    encoded_damage_types["Type_Overload"], encoded_damage_types["Type_Scour"],
    encoded_damage_types["Type_Storm"], encoded_damage_types["Type_Wind"],
]])

input_scaled2 = scaler2.transform(input_features2)



# Apply custom CSS for button styling
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        background-color: #007BFF;
        color: white;
        font-size: 18px;
        padding: 12px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Move the button to the center at the bottom
col1, col2, col3 = st.columns([1, 2, 1])  # Centers button in middle column
with col2:
    if st.button("Predict Condition"):
        prediction = model.predict(input_scaled)[0]  # Get predicted class
        condition_map = {0: ("Poor", "red"), 1: ("Fair", "orange"), 2: ("Good", "green")}
        condition, color = condition_map.get(prediction, ("Unknown", "black"))

        st.write("🏗️ **Predicted Bridge Condition based on Algorithm 1:**")

        # Center and color the predicted bridge condition
        st.markdown(f"""
            <div style="text-align: center; font-size: 60px; font-weight: bold; color: {color};">
                {condition}
            </div>
        """, unsafe_allow_html=True)

        prediction2 = algo2.predict(input_scaled2)[0]  # Get predicted class
        condition_map = {0: ("Trouble", "red"), 1: ("No collapse", "green")}
        condition2, color = condition_map.get(prediction2, ("Unknown", "black"))

        st.write("🏗️ **Predicted Bridge Condition based on Algorithm 2:**")

        # Center and color the predicted bridge condition
        st.markdown(f"""
            <div style="text-align: center; font-size: 60px; font-weight: bold; color: {color};">
                {condition2}
            </div>
        """, unsafe_allow_html=True)

# Run the app using:
# streamlit run app.py



