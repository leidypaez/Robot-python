robot_art = r"""
      0: {head_name}
      Is available: {head_status}
      Attack: {head_attack}                              
      Defense: {head_defense}
      Energy consumption: {head_energy_consump}
      Plus power: {head_plus_power}
              ^
              |                  |1: {weapon_name}
              |                  |Is available: {weapon_status}
     ____     |    ____          |Attack: {weapon_attack}
    |oooo|  ____  |oooo| ------> |Defense: {weapon_defense}
    |oooo| '    ' |oooo|         |Energy consumption: {weapon_energy_consump}
    |0000|        |0000|         |Plus power: {weapon_plus_power}        
    |oooo|/\_||_/\|oooo|          
    `----' / __ \  `----'           |2: {left_arm_name}
   '/  |#|/\/__\/\|#|  \'           |Is available: {left_arm_status}
   /  \|#|| |/\| ||#|/  \           |Attack: {left_arm_attack}
  / \_/|_|| |/\| ||_|\_/ \          |Defense: {left_arm_defense}
 |_\/    O\=----=/O    \/_|         |Energy consumption: {left_arm_energy_consump}
 <_>      |=\__/=|      <_> ------> |Plus power: {left_arm_plus_power}  
 <_>      |------|      <_>         |3: {right_arm_name}
 | |   ___|======|___   | |         |Is available: {right_arm_status}
// \\ / |O|======|O| \  //\\        |Attack: {right_arm_attack}
|  |  | |O+------+O| |  |  |        |Defense: {right_arm_defense}
|\/|  \_+/        \+_/  |\/|        |Energy consumption: {right_arm_energy_consump}
\__/  _|||        |||_  \__/        |Plus power: {right_arm_plus_power}  
      | ||        || |          |4: {left_leg_name} 
     [==|]        [|==]         |Is available: {left_leg_status}
     [===]        [===]         |Attack: {left_leg_attack}
      >_<          >_<          |Defense: {left_leg_defense}
     || ||        || ||         |Energy consumption: {left_leg_energy_consump}
     || ||        || || ------> |Plus power: {left_leg_plus_power} 
     || ||        || ||         |5: {right_leg_name}
   __|\_/|__    __|\_/|__       |Is available: {right_leg_status}
  /___n_n___\  /___n_n___\      |Attack: {right_leg_attack}
                                |Defense: {right_leg_defense}
                                |Energy consumption: {right_leg_energy_consump}
                                |Plus power: {right_leg_plus_power} 
                                
"""
class Part:
  def __init__(self, name:str, part_detaches, attack_level:int=0, defense_level:int=0, energy_consumption:int=0):
    self.name = name
    self.attack_level = attack_level
    self.defense_level = defense_level
    self.energy_consumption = energy_consumption
    self.part_detaches = part_detaches
    self.plus_power = 0


  def get_status_dic(self):
    formatted_name = self.name.replace(" ", "_").lower()
    return {
        '{}_name'.format(formatted_name): self.name.upper(),
        '{}_status'.format(formatted_name): self.is_avalible(),
        '{}_attack'.format(formatted_name): self.attack_level,
        '{}_defense'.format(formatted_name): self.defense_level,
        '{}_energy_consump'.format(formatted_name): self.energy_consumption,
        '{}_plus_power'.format(formatted_name): self.plus_power
    }

  def is_avalible(self):
    return not self.defense_level <= 0
  
colors = {
      'Black':'\x1b[90m',
      'Blue': '\x1b[94m',
      'Cyan': '\x1b[96m',
      'Green': '\x1b[92m',
      'Magenta': '\x1b[95m',
      'Red': '\x1b[91m',
      'White': '\x1b[97m',
      'Yellow': '\x1b[93m'
}
class Robot:
  #método constructor
  def __init__(self, name, color_code):
    #atributos
    self.name = name
    self.color_code = color_code
    self.energy = 20
    self.parts = [
        Part('Head',part_detaches='synthovisor_cortex', attack_level=5, defense_level=10, energy_consumption=5),
        Part('Weapon',part_detaches='electro_arows', attack_level=15, defense_level=0, energy_consumption=20),
        Part('Left Arm',part_detaches='cyber_module' ,attack_level=6, defense_level=3, energy_consumption=10),
        Part('Right Arm',part_detaches='cyber_module' ,attack_level=9, defense_level=2, energy_consumption=15),
        Part('Left Leg',part_detaches='elemental_piece' ,attack_level=3, defense_level=20, energy_consumption=12),
        Part('Right Leg',part_detaches='elemental_piece' ,attack_level=5, defense_level=7, energy_consumption=7)
    ]
    self.inventory = []#[{'name': 'synthovisor_cortex', 'amount': 1}] inventrory.values() -> [ 'synthovisor_cortex', 1]
    self.deffense_absolute = False
  #limpiamos el método
  def great(self):
    print('my name is:', self.name)

  def print_energy(self):
    print('We have', self.energy, 'percent energy left')
  
  #modificación para usar el método add_inventory

  def attack(self, enemy_robot, part_to_use:int, part_to_attack:int):
    if(enemy_robot.deffense_absolute):
      self.energy -= self.parts[part_to_use].energy_consumption
      enemy_robot.deffense_absolute = False
      return
    part_attack = enemy_robot.parts[part_to_attack]
    self.add_inventory(part_attack.part_detaches)
    part_attack.defense_level -= (self.parts[part_to_use].attack_level + self.parts[part_to_use].plus_power)
    for part in self.parts:
      part.plus_power = 0
    self.energy -= self.parts[part_to_use].energy_consumption

  def is_on(self):
    return self.energy > 0
  
  def is_there_avalible_parts(self):
    for part in self.parts:
      if(part.is_avalible()):
        return True
    return False
  
  def print_status(self):
    print(self.color_code)
    str_robot = robot_art.format(**self.get_part_status())
    self.great()
    self.print_energy()
    print(str_robot)
    print(colors['White'])
  
  def get_part_status(self):
    part_status = {}
    for part in self.parts:
      status_dic = part.get_status_dic()
      part_status.update(status_dic)
    return part_status
  
  #para dar funcionalidad de no atacar ni usar partes que no esten disponibles
  def can_use_part(self,part_to_use:int):
    return self.parts[part_to_use].is_avalible()

  def is_energy_suffi_to_use_part(self, part_to_use:int):
    return self.energy - self.parts[part_to_use].energy_consumption <= 0
  #***************************************Tarea**********************************
  #método para llenar el inventario,
  def add_inventory(self, name_element_inventory):#ejemplo de part_to_add = {'name_part_of_inventory':valor}
    for element in self.inventory:
      if name_element_inventory in element.values():
        element['amount'] +=1 
        return
    self.inventory.append({'name':name_element_inventory, 'amount': 1})  

  def print_inventory(self):
    print('******************************your inventory is:****************************')
    self.check_values_on_inventory()
    contador = 1
    for element in self.inventory:
      name_format =element['name'].replace("_", " ")
      print(f"{contador}) {name_format} has: {element['amount']}")
    
  def check_values_on_inventory(self):
    for element in self.inventory:
      if element['amount'] ==0:
        self.inventory.remove(element)
        
  def fuse_power(self, name_element_inventory:int, part_to_fution:Part):#argumentos, algo del invemtario y con lo que queremos fusionar
    values_name=['synthovisor_cortex','cyber_module','elemental_piece','electro_arows']
    values_inventory=self.inventory[name_element_inventory].values()
    print(values_inventory)
    if (values_name[0] in values_inventory): #->{'name':valor_one, 'amount':valor_two }.values -> [valor_one, valor_two]
      part_to_fution.attack_level += 5
      self.inventory[name_element_inventory]['amount'] -=1
      return
    if(values_name[1] in values_inventory):
      part_to_fution.defense_level += 5
      self.inventory[name_element_inventory]['amount'] -=1
      return
    if(values_name[2] in values_inventory):
      self.deffense_absolute = True
      self.inventory[name_element_inventory]['amount'] -=1
      return
    if(values_name[3] in values_inventory):
      for part in self.parts:
        part.plus_power = 10
      self.inventory[name_element_inventory]['amount'] -=1
      return

# método para utilizar elemental piece y electro arows
# robot_one = Robot('Jarvis', colors['Cyan'])
# robot_two = Robot('Friday', colors['Red'])
# print(robot_one.print_status())
# robot_one.attack(robot_two, 0, 1)
# robot_one.print_inventory()
# print(robot_one.inventory)
# robot_two.print_status()
# robot_one.fuse_power(name_element_inventory=0, part_to_fution=0)
# print(robot_one.parts[0].plus_power)


def play():
  playing = True
  print('Welcome to the game')
  robot_one = Robot('Jarvis', colors['Cyan'])
  robot_two = Robot('Friday', colors['Yellow'])
  rount = 0
  while playing:
    if(rount % 2 == 0):
      current_robot = robot_one
      enemy_robot = robot_two
    else:
      current_robot = robot_two
      enemy_robot = robot_one
    current_robot.print_status()
    print('Rount', rount + 1)
    see_to_inventory=input('enter 1 if you want to see the inventory: ')
    if(see_to_inventory == '1'):
      current_robot.print_inventory()
      if len(current_robot.inventory)==0:
        print("you don't have any pieces")
        input()
        continue
      select=input('do you want to use some the inventory?, select 1 if is "yes" or enter any keys for "no"')
      if(select == '1'):
        want_to_use=int(input(' what do you want to use the inventory?'))
        part_to_use = int(input('select a part, this option only works for these inventory items(synthovisor cortex, cyber module)'))
        current_robot.fuse_power(want_to_use - 1,current_robot.parts[part_to_use])
      continue
      

    print('what part should i use to attack?')
    part_to_use = input('Choose a number part: ')
    part_to_use_int = int(part_to_use)
    is_part_to_use_ok = current_robot.can_use_part(part_to_use_int)
    if(not is_part_to_use_ok):
      print(f'you cannot use this {current_robot.parts[part_to_use_int].name} part,  because this part have level defense is minor than zero')
      input()
      continue

    energy_current_robot = current_robot.is_energy_suffi_to_use_part(part_to_use_int)
    if(energy_current_robot):
      print(f'By use the {current_robot.parts[part_to_use_int].name} part your energy is less than or equal to zero')
      print('The winner is ',enemy_robot.name)
      return
    enemy_robot.print_status()
    print('which part of the enemy shloud we attack')
    part_to_attack = input('Choose a enemy part to attack : ')
    part_to_attack_int = int(part_to_attack)

    current_robot.attack(enemy_robot, part_to_use_int, part_to_attack_int)
    this_part_enemy_ok = enemy_robot.can_use_part(part_to_attack_int)
    if(not this_part_enemy_ok):
      print(f'you cannot attack this {enemy_robot.parts[part_to_attack_int].name} part,  because this part have level defense is minor than zero')
      input()
      continue
    rount +=1
    if(not enemy_robot.is_on() or enemy_robot.is_there_avalible_parts()==False):
      playing= False
      print('Congratulations, you won')
      print(current_robot.name)

play()
