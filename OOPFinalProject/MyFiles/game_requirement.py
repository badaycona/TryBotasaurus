class Requirement:
    def __init__(self, OS : str, CPU : str, RAM : str, GPU : str, DirectX : str, Storage : str, AdditionalNotes : str):
        self.OS = OS
        self.CPU = CPU
        self.RAM = RAM
        self.GPU = GPU
        self.DirectX = DirectX
        self.Storage = Storage
        self.AdditionalNotes = AdditionalNotes

class Game:
    def __init__(self, Name: str, Minimum: Requirement, Recommended: Requirement):
        self.Name = Name
        self.Minimum = Minimum
        self.Recommended = Recommended
    def __str__(self):
        return_list = [self.Name, 'Minimum configuration:',f'OS : {self.Minimum.OS}', f'CPU : {self.Minimum.CPU}', f'RAM : {self.Minimum.RAM}', f'GPU : {self.Minimum.GPU}', f'DirectX : {self.Minimum.DirectX}', f'Storage : {self.Minimum.Storage}', f'Additional Notes : {self.Minimum.AdditionalNotes}', 'Recommended configuration:', f'OS : {self.Recommended.OS}', f'CPU : {self.Recommended.CPU}', f'RAM : {self.Recommended.RAM}', f'GPU : {self.Recommended.GPU}', f'DirectX : {self.Recommended.DirectX}', f'Storage : {self.Recommended.Storage}', f'Additional Notes : {self.Recommended.AdditionalNotes}']
        return '\n'.join(return_list)