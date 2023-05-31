import psycopg2
import pandas as pd
from Resources.InternalLoad import InternalLoad


def insert_data_into_database(
        space,
        people_density,
        lighting,
        electric_equipment,
        outdoor_air_per_area,
        outdoor_air_per_person,
        people_density_unit,
        people_activity,
        gas_equipment,
        table_name="InternalLoad"):
    # First, build a connection
    connect = psycopg2.connect(
        database="InternalLoads",
        user="postgres",
        password="pg123",
        port="5432")

    # Set up a cursor
    cursor = connect.cursor()

    space_f, people_density_f, lighting_f, electric_equipment_f, outdoor_air_per_area_f, outdoor_air_per_person_f, \
        people_density_unit_f, people_activity_f, gas_equipment_f = [], [], [], [], [], [], [], [], []
    # data_length = min(len(names), len(teams), len(numbers))
    data_length = len(space)
    for i in range(data_length):
        space_f.extend([space[i]])
        people_density_f.extend([people_density[i]])
        lighting_f.extend([lighting[i]])
        electric_equipment_f.extend([electric_equipment[i]])
        outdoor_air_per_area_f.extend([outdoor_air_per_area[i]])
        outdoor_air_per_person_f.extend([outdoor_air_per_person[i]])
        people_density_unit_f.extend([people_density_unit[i]])
        people_activity_f.extend([people_activity[i]])
        gas_equipment_f.extend([gas_equipment[i]])

    # Command line to write data into table
    table_name = '"' + table_name + '"'
    sql = "INSERT INTO{}(\"space\", \"people_density\", \"lighting\", \"electric_equipment\", " \
          "\"outdoor_air_per_area\", \"outdoor_air_per_person\", \"people_density_unit\", \"people_activity\", " \
          "\"gas_equipment\") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table_name)

    # Group datasets into a list
    data = zip(space_f, people_density_f, lighting_f, electric_equipment_f, outdoor_air_per_area_f,
               outdoor_air_per_person_f, people_density_unit_f, people_activity_f, gas_equipment_f)
    data_list = [list(d) for d in data]

    # Execute
    try:
        cursor.executemany(sql, data_list)
    except Exception as e:
        print(e)

    connect.commit()
    cursor.close()
    connect.close()


def get_internal_load(file_path: str, sheet_name: str = None):

    if sheet_name is not None:
        sheet = sheet_name
    else:
        sheet = "Sheet1"

    df = pd.read_excel(file_path, sheet_name=sheet)

    load = InternalLoad.internal_load_input_json(
        df["space"].values.tolist(),
        df["lighting"].values.tolist(),
        df["electric"].values.tolist(),
        df["ppl_density"].values.tolist(),
        df["activity"].values.tolist(),
        df["OA_per_area"].values.tolist(),
        df["OA_per_ppl"].values.tolist(),
        df["people_unit"].values.tolist())

    return load

# project_spaces = ["Lobby", "Lounge", "Exhibition", "MultiFunctional", "BreakRoom", "SmallConference", "Cafeteria",
#                   "OpenOffice", "ClosedOffice", "BigConference", "Gym", "DocumentRoom"]
# project_people_density = [10, 3, 3, 240, 5, 6, 500, 200, 2, 2, 5, 5]
# project_lighting = [5.6, 7, 7, 8, 10, 8, 8, 8, 8, 8, 8, 3.5]
# project_electric_equipment = [20, 80, 80, 50, 10, 35, 30, 60, 45, 45, 30, 10]
# project_outdoor_air_per_area = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# project_outdoor_air_per_person = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# project_people_density_unit = [2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1]
# project_people_activity = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
# project_gas_equipment = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# insert_data_into_database(
#     project_spaces, project_people_density, project_lighting, project_electric_equipment, project_outdoor_air_per_area,
#     project_outdoor_air_per_person, project_people_density_unit, project_people_activity, project_gas_equipment)


# df = pd.read_excel("D:\\Projects\\OpenStudioDev\\LoadInputs.xlsx", "ExpoTower")
# print(df["space"].values.tolist())
