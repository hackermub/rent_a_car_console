
class Car:
    def __init__(self, registerPlateNumber: str, modelName: str, dailyRate: int, *properties):
        self.registerPlateNumber = registerPlateNumber
        self.modelName = modelName
        self.dailyRate = int(dailyRate)
        self.properties = properties[0]
       

    def __str__(self):
        # * Reg. nr: BKV-943, Model: Ford Fiesta, Price per day: 35
        # Properties: Manual Transmission
        output = f"* Reg. nr: {self.registerPlateNumber}, Model: {self.modelName}, Price per day: {self.dailyRate}\nProperties: "
        for prop in self.properties:
            output += f"{prop.strip()}, "
        
        return output[:-2] # Remove last comma
        