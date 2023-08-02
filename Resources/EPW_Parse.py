import os
import numpy as np


def import_epw(file_path):
    assert os.path.isfile(file_path), 'Cannot find an epw file at {}'.format(file_path)
    assert file_path.lower().endswith('epw'), '{} is not an .epw file. \n' \
                                              'It does not possess the .epw file extension.'.format(file_path)

    try:
        with open(file_path, 'r') as epwin:
            line = epwin.readlines()
            print(line[1])
    except ValueError:
        pass


class Location:
    def __init__(
            self,
            field_city: str = "-",
            field_province: str = "-",
            field_country: str = "-",
            field_latitude: float = 0,
            field_longitude: float = 0,
            field_timezone: int = 0,
            field_elevation: float = 0,
            field_source: str = "TMY3",
            field_wmo: str = "99999"):

        self._field_city = field_city
        self._field_province = field_province
        self._field_country = field_country
        self._field_source = field_source
        self._field_wmo = field_wmo
        self._field_latitude = field_latitude
        self._field_longitude = field_longitude
        self._field_timezone = field_timezone
        self._field_elevation = field_elevation

    @property
    def city(self):
        return self._field_city

    @property
    def province(self):
        return self._field_province

    @property
    def country(self):
        return self._field_country

    @property
    def latitude(self):
        return self._field_latitude

    @property
    def longitude(self):
        return self._field_longitude

    @property
    def timezone(self):
        return self._field_timezone

    @property
    def elevation(self):
        return self._field_elevation

    @city.setter
    def city(self, city):
        self._field_city = "My City" if not city else str(city)

    @province.setter
    def province(self, province):
        self._field_province = "My Province" if not province else str(province)

    @country.setter
    def country(self, country):
        self._field_country = "My Country" if not country else str(country)

    @latitude.setter
    def latitude(self, lat):
        self._field_latitude = 0 if not lat else float(lat)

    @longitude.setter
    def longitude(self, long):
        self._field_longitude = 0 if not long else float(long)

    @timezone.setter
    def timezone(self, tz):
        self._field_timezone = 0 if not tz else int(tz)

    @elevation.setter
    def elevation(self, elev):
        self._field_elevation = 0 if not elev else int(elev)

    @classmethod
    def from_dict(cls, location):
        keys = ['city', 'state', 'country', 'latitude', 'longitude', 'time_zone', 'elevation']

        if isinstance(location, dict):
            for key in keys:
                if key not in keys:
                    location[key] = None

            return cls(location['city'], location['state'], location['country'], location['latitude'],
                       location['longitude'], location['time_zone'], location['elevation'])
        else:
            raise TypeError("Invalid input type if location dictionary.")

    def to_dict(self):
        return {
            "city": self._field_city,
            "province": self._field_province,
            "country": self._field_country,
            "latitude": self._field_latitude,
            "longitude": self._field_longitude,
            "time_zone": self._field_timezone,
            "elevation": self._field_elevation,
            "source": self._field_source,
            "wmo": self._field_wmo
        }


class DesignCondition:
    def __init__(self, dc_type: int = 1, month: int = 1):
        """
        dc_type: 1.Heating 2.Cooling
        """
        self._dc_type = dc_type
        self._month = month

    @property
    def design_condition_type(self):
        return "Heating" if self._dc_type == 1 else "Cooling"

    @property
    def month(self):
        return self._month


class DesignConditions:
    def __init__(
            self,
            number_of_design_conditions: int = 1,
            design_condition_source: str = "Climate Design Data 2009 ASHRAE Handbook",
            heating_design_condition: DesignCondition = None,
            cooling_design_condition: DesignCondition = None):
        self._number_of_design_conditions = number_of_design_conditions
        self._design_condition_source = design_condition_source
        self._heating_design_condition = heating_design_condition
        self._cooling_design_condition = cooling_design_condition

    @property
    def number_of_design_conditions(self):
        return self._number_of_design_conditions

    def to_string(self):
        string = str(self._number_of_design_conditions) + self._design_condition_source + \
                 "Heating" + str(self._heating_design_condition.month)
        return string


class ExtremePeriod:
    def __init__(self, name: str = None, period_type: int = 1, start_day: str = None, end_day: str = None):
        """
        Period_type: 1.Extreme 2.Typical \n
        Start/End Day: use format "M/D", eg. 7/13
        """
        self._name = name
        self._period_type = period_type
        self._start_day = start_day
        self._end_day = end_day

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name if not name else str(name)

    @property
    def period_type(self):
        return "Extreme" if self._period_type == 1 else "Typical"

    @period_type.setter
    def period_type(self, p_type: int):
        """
        Period_type: 1.Extreme 2.Typical
        """
        self._period_type = p_type if not p_type else int(p_type)

    @property
    def start_day(self):
        return self._start_day

    @start_day.setter
    def start_day(self, day: str):
        self._start_day = day if not day else str(day)

    @property
    def end_day(self):
        return self._end_day

    @end_day.setter
    def end_day(self, day):
        self._end_day = day if not day else str(day)


class ExtremePeriods:
    def __init__(
            self,
            number_of_extreme_periods: int = 6,
            period_1: ExtremePeriod = ExtremePeriod("Summer - Week Nearest Max Temperature For Period", 1, "7/13", "7/19"),
            period_2: ExtremePeriod = ExtremePeriod("Summer - Week Nearest Average Temperature For Period", 2, "8/17", "7/23"),
            period_3: ExtremePeriod = ExtremePeriod("Winter - Week Nearest Min Temperature For Period", 1, "1/20", "1/26"),
            period_4: ExtremePeriod = ExtremePeriod("Winter - Week Nearest Average Temperature For Period", 2, "12/22", "12/28"),
            period_5: ExtremePeriod = ExtremePeriod("Autumn - Week Nearest Average Temperature For Period", 2, "11/3", "11/9"),
            period_6: ExtremePeriod = ExtremePeriod("Spring - Week Nearest Average Temperature For Period", 2, "4/12", "4/18"),):
        self._number_of_extreme_periods = number_of_extreme_periods
        self._period_1 = period_1
        self._period_2 = period_2
        self._period_3 = period_3
        self._period_4 = period_4
        self._period_5 = period_5
        self._period_6 = period_6

    @property
    def number_of_extreme_periods(self):
        return self._number_of_extreme_periods

    @property
    def period_1(self):
        return self._period_1

    @property
    def period_2(self):
        return self._period_2

    @property
    def period_3(self):
        return self._period_3

    @property
    def period_4(self):
        return self._period_4

    @property
    def period_5(self):
        return self._period_5

    @property
    def period_6(self):
        return self._period_6

    def to_string(self):
        string = str(self._number_of_extreme_periods) + "," + \
                 self._period_1.name + "," + self._period_1.period_type + "," + \
                 self._period_1.start_day + "," + self._period_1.end_day + "," + \
                 self._period_2.name + "," + self._period_2.period_type + "," + \
                 self._period_2.start_day + "," + self._period_2.end_day + "," + \
                 self._period_3.name + "," + self._period_3.period_type + "," + \
                 self._period_3.start_day + "," + self._period_3.end_day + "," + \
                 self._period_4.name + "," + self._period_4.period_type + "," + \
                 self._period_4.start_day + "," + self._period_4.end_day + "," + \
                 self._period_5.name + "," + self._period_5.period_type + "," + \
                 self._period_5.start_day + "," + self._period_5.end_day + "," + \
                 self._period_6.name + "," + self._period_6.period_type + "," + \
                 self._period_6.start_day + "," + self._period_6.end_day
        return string


class GroundTemperature:
    def __init__(
            self,
            depth: float = 0.5,
            jan_temp: float = 15,
            feb_temp: float = 15,
            mar_temp: float = 15,
            apr_temp: float = 15,
            may_temp: float = 15,
            jun_temp: float = 15,
            jul_temp: float = 15,
            aug_temp: float = 15,
            sep_temp: float = 15,
            oct_temp: float = 15,
            nov_temp: float = 15,
            dec_temp: float = 15,
            soil_conductivity: float = "",
            soil_density: float = "",
            soil_specific_heat: float = "", ):
        self._depth = depth
        self._soil_conductivity = soil_conductivity
        self._soil_density = soil_density
        self._soil_specific_heat = soil_specific_heat
        self._jan_temp = jan_temp
        self._feb_temp = feb_temp
        self._mar_temp = mar_temp
        self._apr_temp = apr_temp
        self._may_temp = may_temp
        self._jun_temp = jun_temp
        self._jul_temp = jul_temp
        self._aug_temp = aug_temp
        self._sep_temp = sep_temp
        self._oct_temp = oct_temp
        self._nov_temp = nov_temp
        self._dec_temp = dec_temp

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, depth):
        self._depth = depth

    @property
    def soil_conductivity(self):
        return self._soil_conductivity

    @soil_conductivity.setter
    def soil_conductivity(self, conductivity):
        self._soil_conductivity = conductivity

    @property
    def soil_density(self):
        return self._soil_density

    @soil_density.setter
    def soil_density(self, density):
        self._soil_density = density

    @property
    def soil_specific_heat(self):
        return self._soil_density

    @soil_specific_heat.setter
    def soil_specific_heat(self, value):
        self._soil_specific_heat = value

    @property
    def jan_temp(self):
        return self._jan_temp

    @jan_temp.setter
    def jan_temp(self, value):
        self._jan_temp = value

    @property
    def feb_temp(self):
        return self._feb_temp

    @feb_temp.setter
    def feb_temp(self, value):
        self._feb_temp = value

    @property
    def mar_temp(self):
        return self._mar_temp

    @mar_temp.setter
    def mar_temp(self, value):
        self._mar_temp = value

    @property
    def apr_temp(self):
        return self._apr_temp

    @apr_temp.setter
    def apr_temp(self, value):
        self._apr_temp = value

    @property
    def may_temp(self):
        return self._may_temp

    @may_temp.setter
    def may_temp(self, value):
        self._may_temp = value

    @property
    def jun_temp(self):
        return self._jun_temp

    @jun_temp.setter
    def jun_temp(self, value):
        self._jun_temp = value

    @property
    def jul_temp(self):
        return self._jul_temp

    @jul_temp.setter
    def jul_temp(self, value):
        self._jul_temp = value

    @property
    def aug_temp(self):
        return self._aug_temp

    @aug_temp.setter
    def aug_temp(self, value):
        self._aug_temp = value

    @property
    def sep_temp(self):
        return self._sep_temp

    @sep_temp.setter
    def sep_temp(self, value):
        self._sep_temp = value

    @property
    def oct_temp(self):
        return self._oct_temp

    @oct_temp.setter
    def oct_temp(self, value):
        self._oct_temp = value

    @property
    def nov_temp(self):
        return self._nov_temp

    @nov_temp.setter
    def nov_temp(self, value):
        self._nov_temp = value

    @property
    def dec_temp(self):
        return self._dec_temp

    @dec_temp.setter
    def dec_temp(self, value):
        self._dec_temp = value

    def to_dict(self):
        return {
            "depth": self._depth,
        }


# class DesignConditions:
#     def __init__(self):


# epw_path_str = "D:\Projects\OpenStudioDev\CHN_Shanghai.Shanghai.583670_IWEC.epw"
# import_epw(epw_path_str)

loca = Location("Beijing")
loca.country = "China"
loc_dict = loca.to_dict()

gdt = GroundTemperature()
gdt.jan_temp = 15.8

temps = [30, 28, 32, 25, 27, 31, 34]
humids = [88, 79, 90, 75, 85, 83, 96]
winds = [1, 9, 10, 11, 12, 13, 14]

temps = list(map(str, temps))
humids = list(map(str, humids))
winds = list(map(str, winds))

x = np.column_stack([temps, humids, winds])
print(x[0])

path = "D:\\Projects\\OpenStudioDev\\weather.epw"
file = open(path, "w+")
content = x[0]
file.writelines(content)
file.close()

# ep = ExtremePeriods().to_string()
# print(ep)

# print(loc_dict)
# print(gdt.soil_conductivity)
