import openstudio


class ZoneEquipment:

    @staticmethod
    def fan_coil_unit(
            model: openstudio.openstudiomodel.Model,
            name: str = None,):

        equipment = openstudio.openstudiomodel.ZoneHVACFourPipeFanCoil()