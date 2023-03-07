from openstudio.openstudiomodel import MaterialVector, Construction, MasslessOpaqueMaterial, SimpleGlazing

class constructiontool:

    # Opaque construction
    @staticmethod
    def opaque(model, name, thermalresistance, roughness="MediumRough"):
        mat = MasslessOpaqueMaterial(model, roughness, thermalresistance)
        mat.setName(name)

        mat_vec = MaterialVector()
        mat_vec.append(mat)

        cons = Construction(model)
        cons.setName(name)
        cons.setLayers(mat_vec)

        return cons

    # Simple Glazing
    @staticmethod
    def simpleglazing(model, name, ufactor, shgc, tv):
        mat = SimpleGlazing(model, ufactor, shgc)
        mat.setName(name)
        mat.setVisibleTransmittance(tv)

        mat_vec = MaterialVector()
        mat_vec.append(mat)

        cons = Construction(model)
        cons.setName(name)
        cons.setLayers(mat_vec)

        return cons